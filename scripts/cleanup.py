#!/usr/bin/env python3
"""Daily cleanup: delete queue folders whose post is already live on Instagram.

Run by .github/workflows/cleanup.yml once a day, for every account in accounts.json.
- A folder is deleted only if state/<account>.json lists it as posted at least MIN_AGE_HOURS ago.
- Unposted and failed folders are never touched, and state/*.json is never edited, so the posting
  log (media ids, permalinks) is kept and the publisher still knows what went out.
- Queue numbers are never reused: use scripts/next_number.py to pick the next number.

  python scripts/cleanup.py            delete
  python scripts/cleanup.py --dry-run  only list what would be deleted
"""
import argparse, datetime as dt, json, os, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIN_AGE_HOURS = 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    now = dt.datetime.now(dt.timezone.utc)
    cfg = json.loads((ROOT / "accounts.json").read_text())
    removed = 0
    for acc in cfg["accounts"]:
        q = ROOT / "content" / acc["id"] / "queue"
        sp = ROOT / "state" / f"{acc['id']}.json"
        if not q.exists() or not sp.exists():
            continue
        posted = json.loads(sp.read_text()).get("posted", {})
        for item in sorted(p for p in q.iterdir() if p.is_dir()):
            info = posted.get(item.name)
            if not info:
                continue
            when = info.get("posted_at")
            age = (now - dt.datetime.fromisoformat(when)).total_seconds() / 3600 if when else 999
            if age < MIN_AGE_HOURS:
                continue
            print(f"[{acc['id']}] {'would delete' if a.dry_run else 'deleted'} {item.name} "
                  f"(live: {info.get('permalink') or info.get('media_id')})")
            if not a.dry_run:
                shutil.rmtree(item)
            removed += 1
    print(f"{removed} posted folder(s) {'to delete' if a.dry_run else 'deleted'}")
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"changed={'true' if removed and not a.dry_run else 'false'}\n")


if __name__ == "__main__":
    main()
