#!/usr/bin/env python3
"""Instagram auto-poster for multiple accounts.

Every run (GitHub Actions, every 15 min) checks each enabled account in
accounts.json. If a posting slot has just passed and hasn't been filled yet,
the next item in that account's queue is published.

Queue layout:  content/<account id>/queue/<NNNN-slug>/
                  01.jpg [02.jpg ...]   -> 1 image = single post, 2-10 = carousel
                  caption.txt
State:         state/<account id>.json  (what has been posted, written by this script)

Only the Python standard library is used.
"""
import argparse, datetime as dt, json, os, sys, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
GRACE_MINUTES = 120          # a slot is skipped if we notice it later than this
MAX_ATTEMPTS = 3             # after this many failures an item is marked failed and skipped
API_BASE = os.environ.get("IG_API_BASE", "https://graph.instagram.com")
ERRORS = []


# ---------------------------------------------------------------- helpers
def log(msg):
    print(msg, flush=True)


def summary(line):
    p = os.environ.get("GITHUB_STEP_SUMMARY")
    if p:
        with open(p, "a") as f:
            f.write(line + "\n")


def load_json(path, default):
    try:
        return json.loads(Path(path).read_text())
    except FileNotFoundError:
        return default


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2) + "\n")


def get_token(name):
    secrets = json.loads(os.environ.get("ALL_SECRETS") or "{}")
    return secrets.get(name) or os.environ.get(name)


class Api:
    def __init__(self, version, token):
        self.base = f"{API_BASE}/{version}"
        self.token = token

    def _call(self, method, path, params=None):
        params = dict(params or {}, access_token=self.token)
        url = f"{self.base}/{path}"
        data = None
        if method == "GET":
            url += "?" + urllib.parse.urlencode(params)
        else:
            data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(url, data=data, method=method)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")
            raise RuntimeError(f"{method} {path} -> HTTP {e.code}: {body}") from None

    def me(self):
        return self._call("GET", "me", {"fields": "user_id,username"})

    def wait_ready(self, container_id, timeout=120):
        start = time.time()
        while time.time() - start < timeout:
            st = self._call("GET", container_id, {"fields": "status_code"}).get("status_code")
            if st == "FINISHED":
                return
            if st in ("ERROR", "EXPIRED"):
                raise RuntimeError(f"container {container_id} status {st}")
            time.sleep(3)
        raise RuntimeError(f"container {container_id} not ready after {timeout}s")

    def publish(self, user_id, image_urls, caption):
        if len(image_urls) == 1:
            c = self._call("POST", f"{user_id}/media", {"image_url": image_urls[0], "caption": caption})["id"]
        else:
            children = []
            for u in image_urls:
                cid = self._call("POST", f"{user_id}/media", {"image_url": u, "is_carousel_item": "true"})["id"]
                children.append(cid)
            for cid in children:
                self.wait_ready(cid)
            c = self._call("POST", f"{user_id}/media",
                           {"media_type": "CAROUSEL", "children": ",".join(children), "caption": caption})["id"]
        self.wait_ready(c)
        media_id = self._call("POST", f"{user_id}/media_publish", {"creation_id": c})["id"]
        try:
            link = self._call("GET", media_id, {"fields": "permalink"}).get("permalink")
        except Exception:
            link = None
        return media_id, link


# ---------------------------------------------------------------- queue / slots
def queue_items(acc_id):
    q = ROOT / "content" / acc_id / "queue"
    if not q.exists():
        return []
    return sorted(p for p in q.iterdir() if p.is_dir())


def validate_item(item):
    imgs = sorted(p for p in item.iterdir() if p.suffix.lower() in (".jpg", ".jpeg"))
    cap_file = item / "caption.txt"
    caption = cap_file.read_text().strip() if cap_file.exists() else ""
    problems = []
    if not imgs:
        problems.append("no .jpg images")
    if len(imgs) > 10:
        problems.append(f"{len(imgs)} images (max 10)")
    if len(caption) > 2200:
        problems.append("caption longer than 2200 characters")
    if caption.count("#") > 30:
        problems.append("more than 30 hashtags")
    return imgs, caption, problems


def latest_slot(now_utc, tz, slots):
    local = now_utc.astimezone(tz)
    cands = []
    for day in (local.date() - dt.timedelta(days=1), local.date()):
        for s in slots:
            h, m = map(int, s.split(":"))
            t = dt.datetime(day.year, day.month, day.day, h, m, tzinfo=tz)
            if t <= local:
                cands.append(t)
    return max(cands) if cands else None


def media_url(path):
    base = os.environ.get("MEDIA_BASE_URL")
    rel = path.relative_to(ROOT).as_posix()
    if base:
        return base.rstrip("/") + "/" + urllib.parse.quote(rel)
    repo = os.environ["GITHUB_REPOSITORY"]
    ref = os.environ.get("GITHUB_SHA", "main")
    return f"https://raw.githubusercontent.com/{repo}/{ref}/{urllib.parse.quote(rel)}"


# ---------------------------------------------------------------- main
def run_account(cfg, acc, now, dry_run, force):
    acc_id = acc["id"]
    state_path = ROOT / "state" / f"{acc_id}.json"
    state = load_json(state_path, {"last_slot": None, "posted": {}, "failed": {}, "attempts": {}})
    tz = ZoneInfo(acc.get("timezone", "UTC"))
    pending = [i for i in queue_items(acc_id) if i.name not in state["posted"] and i.name not in state["failed"]]
    summary(f"| {acc_id} | {len(pending)} posts left in queue |")
    if len(pending) < len(acc["slots"]) * 2:
        log(f"[{acc_id}] WARNING: only {len(pending)} posts left in the queue")

    slot = latest_slot(now, tz, acc["slots"])
    if not force:
        if slot is None:
            return False
        if state.get("last_slot") == slot.isoformat():
            log(f"[{acc_id}] slot {slot:%Y-%m-%d %H:%M %Z} already filled")
            return False
        late = (now - slot).total_seconds() / 60
        if late > GRACE_MINUTES:
            log(f"[{acc_id}] last slot {slot:%H:%M %Z} passed {late:.0f} min ago; waiting for the next one")
            return False
    if not pending:
        log(f"[{acc_id}] queue is empty, nothing to post")
        return False

    item = pending[0]
    imgs, caption, problems = validate_item(item)
    if problems:
        log(f"[{acc_id}] {item.name} is invalid: {'; '.join(problems)}; marking failed")
        state["failed"][item.name] = "; ".join(problems)
        save_json(state_path, state)
        return True
    urls = [media_url(p) for p in imgs]
    kind = "carousel" if len(urls) > 1 else "single"
    log(f"[{acc_id}] posting {item.name} ({kind}, {len(urls)} image(s)) for slot {slot}")
    if dry_run:
        for u in urls:
            log("    " + u)
        log("    caption: " + caption[:80].replace("\n", " ") + "...")
        return False

    token = get_token(acc["token_secret"])
    if not token:
        log(f"[{acc_id}] ERROR: secret {acc['token_secret']} is not set")
        ERRORS.append(acc_id)
        return False
    api = Api(cfg.get("api_version", "v23.0"), token)
    try:
        user_id = api.me()["user_id"]
    except Exception as e:
        # account/token problem: don't count it against the post, just alert
        log(f"[{acc_id}] ERROR: token for this account doesn't work: {e}")
        ERRORS.append(acc_id)
        return False
    try:
        media_id, link = api.publish(user_id, urls, caption)
    except Exception as e:
        n = state["attempts"].get(item.name, 0) + 1
        state["attempts"][item.name] = n
        log(f"[{acc_id}] ERROR publishing {item.name} (attempt {n}): {e}")
        ERRORS.append(acc_id)
        if n >= MAX_ATTEMPTS:
            state["failed"][item.name] = str(e)[:500]
        save_json(state_path, state)
        return True
    state["posted"][item.name] = {"media_id": media_id, "permalink": link,
                                  "posted_at": now.isoformat(), "slot": slot.isoformat() if slot else None}
    if slot:
        state["last_slot"] = slot.isoformat()
    state["attempts"].pop(item.name, None)
    save_json(state_path, state)
    log(f"[{acc_id}] published {item.name}: {link or media_id}")
    summary(f"| {acc_id} | posted {item.name} {link or ''} |")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="show what would be posted, call nothing")
    ap.add_argument("--account", help="only this account id")
    ap.add_argument("--now", help="pretend the time is this ISO timestamp (testing)")
    ap.add_argument("--force", action="store_true", help="post the next item now, ignoring slots")
    a = ap.parse_args()
    cfg = load_json(ROOT / "accounts.json", None)
    now = dt.datetime.fromisoformat(a.now) if a.now else dt.datetime.now(dt.timezone.utc)
    summary("| Account | Status |\n|---|---|")
    changed = False
    for acc in cfg["accounts"]:
        if not acc.get("enabled", True) or (a.account and acc["id"] != a.account):
            continue
        changed |= run_account(cfg, acc, now, a.dry_run, a.force)
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"changed={'true' if changed else 'false'}\n")
    if ERRORS:
        log(f"Finished with errors for: {', '.join(sorted(set(ERRORS)))}")
        sys.exit(1)


if __name__ == "__main__":
    main()
