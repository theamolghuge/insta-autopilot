#!/usr/bin/env python3
"""Make ONE fresh AI-news post and put it in the account's queue.

Run by .github/workflows/ai-news.yml every 3 hours:
  1. drop unposted news items that have gone stale (news must be fresh)
  2. collect stories from the feeds, group duplicates, rank, skip anything already covered
  3. pick the format for this run from config.json "format_mix"
  4. write the copy (Claude if ANTHROPIC_API_KEY is set, rule-based otherwise)
  5. render slides in the brand (article image on top 40%, text below) + caption.txt
  6. save to content/<account>/queue/NNNN-news-<slug>/ and remember what was covered

Local test without network:
  python generator/ai-news/make_post.py --stories sample.json --out out/ai-news-test
"""
import argparse, datetime as dt, json, os, re, shutil, sys
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))

import news, writer                                   # noqa: E402
from brand import render_still, plain, W, MEDIA_H     # noqa: E402
from art import make_art                              # noqa: E402

CFG = json.loads((HERE / "config.json").read_text())
ACC = CFG["account_id"]
QUEUE = ROOT / "content" / ACC / "queue"
SEEN = ROOT / "content" / ACC / "seen.json"
STATE = ROOT / "state" / f"{ACC}.json"


def log(m):
    print(m, flush=True)


def load(p, default):
    try:
        return json.loads(Path(p).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def slugify(s, n=40):
    return re.sub(r"[^a-z0-9]+", "-", plain(s).lower()).strip("-")[:n].strip("-") or "news"


# ---------------------------------------------------------------- queue housekeeping
def tidy_queue(now, dry):
    """Remove unposted news items older than drop_unposted_after_hours. Returns # fresh pending."""
    state = load(STATE, {})
    done = set(state.get("posted", {})) | set(state.get("failed", {}))
    fresh = 0
    if not QUEUE.exists():
        return 0
    for item in sorted(p for p in QUEUE.iterdir() if p.is_dir()):
        if item.name in done:
            continue
        meta = load(item / "meta.json", {})
        made = meta.get("generated_at")
        age = (now - dt.datetime.fromisoformat(made)).total_seconds() / 3600 if made else 999
        if age > CFG["drop_unposted_after_hours"]:
            log(f"dropping stale unposted item {item.name} ({age:.1f} h old)")
            if not dry:
                shutil.rmtree(item)
        else:
            fresh += 1
    return fresh


def next_number():
    nums = [int(p.name[:4]) for p in QUEUE.glob("[0-9][0-9][0-9][0-9]-*")] if QUEUE.exists() else []
    return max(nums, default=0) + 1


# ---------------------------------------------------------------- images
def story_image(cl):
    """Article's own image (og:image), else the feed's image. None if neither is usable."""
    lead = cl["stories"][0]
    for url in (cl.get("og_image"), lead.get("feed_image")):
        im = news.load_image(url)
        if im is not None:
            return im
    for x in cl["stories"][1:3]:                       # another outlet covering the same story
        img, _ = news.article(x["url"])
        im = news.load_image(img) or news.load_image(x.get("feed_image"))
        if im is not None:
            cl["image_source"] = x["source"]
            return im
    return None


def enrich(cl, offline=False):
    if offline:
        cl.setdefault("text", cl["stories"][0].get("summary", ""))
        return cl
    img, text = news.article(cl["stories"][0]["url"])
    cl["og_image"], cl["text"] = img, text
    return cl


# ---------------------------------------------------------------- rendering
def render(fmt, post, clusters, out, now, offline):
    tz = ZoneInfo(CFG.get("timezone", "UTC"))
    local = now.astimezone(tz)
    date = local.strftime("%d %b %Y").upper()
    files = []

    def img_for(cl, word):
        if offline:                                    # tests: optional stand-in photo, no network
            t = os.environ.get("AI_NEWS_TEST_IMAGE")
            from PIL import Image
            im = Image.open(t).convert("RGB") if t else None
        else:
            im = story_image(cl)
        if im is not None:
            return im, f"IMAGE: {cl.get('image_source') or cl['stories'][0]['source']}"
        return make_art(cl["stories"][0]["url"], word or "AI", W, MEDIA_H), None

    def save(slide, media=None):
        p = out / f"{len(files) + 1:02d}.jpg"
        slide["date"] = date
        render_still(slide, p, media)
        files.append(p)

    if fmt in ("media_top", "text"):
        cl = clusters[0]
        src = cl["sources"][0]
        slide = {"kicker": post["kicker"], "headline": post["headline"], "body": post["body"], "source": src}
        if fmt == "media_top":
            im, credit = img_for(cl, post.get("image_word"))
            save(dict(slide, layout="media_top", credit=credit), im)
        else:
            save(dict(slide, layout="text"))

    elif fmt == "carousel":
        cl = clusters[0]
        pts = post["points"]
        n = 2 + len(pts)
        im, credit = img_for(cl, post.get("image_word"))
        save({"layout": "media_top", "kicker": post["kicker"], "headline": post["headline"],
              "body": post["body"], "swipe": True, "credit": credit}, im)
        for i, p in enumerate(pts, 1):
            save({"layout": "point", "num": f"{i:02d}", "headline": p["heading"], "body": p["body"],
                  "page": f"{i + 1}/{n}"})
        save({"layout": "cta", "sources": cl["sources"][:5], "page": f"{n}/{n}"})

    elif fmt == "roundup":
        n = len(clusters) + 2
        save({"layout": "roundup", "kicker": f"AI Brief · {local:%H:00} {local.tzname()}",
              "headline": post["headline"], "items": post["items"], "swipe": True})
        for i, (cl, sl) in enumerate(zip(clusters, post["slides"]), 2):
            im, credit = img_for(cl, sl["kicker"])
            save({"layout": "media_top", "kicker": sl["kicker"], "headline": sl["headline"], "body": sl["body"],
                  "page": f"{i}/{n}", "credit": credit}, im)
        srcs = []
        for cl in clusters:
            srcs += [s for s in cl["sources"][:2] if s not in srcs]
        save({"layout": "cta", "sources": srcs[:5], "page": f"{n}/{n}"})
    return files


def caption(fmt, post, clusters):
    lines = [plain(post["headline"]), ""]
    lines.append(post.get("caption_summary") or plain(post.get("body", "")))
    lines.append("")
    if fmt == "roundup":
        srcs = []
        for cl in clusters:
            srcs += [s for s in cl["sources"][:2] if s not in srcs]
    else:
        srcs = clusters[0]["sources"][:3]
    lines.append("Source: " + ", ".join(srcs))
    if post.get("question"):
        lines += ["", post["question"]]
    lines += ["", f"Follow {CFG['handle']} for the latest AI news, every 3 hours.", "."]
    tags = []
    for t in post.get("hashtags", []) + CFG["hashtags"]:
        if t.lower() not in tags:
            tags.append(t.lower())
    lines.append(" ".join(tags[:12]))
    return "\n".join(lines)[:2200]


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stories", help="JSON file of stories instead of fetching feeds (testing)")
    ap.add_argument("--out", help="write the post here instead of the queue (testing; nothing is recorded)")
    ap.add_argument("--format", choices=["media_top", "text", "carousel", "roundup"], help="force a format")
    ap.add_argument("--now", help="pretend time (ISO)")
    ap.add_argument("--always", action="store_true", help="make a post even if a fresh one is already waiting")
    a = ap.parse_args()
    now = dt.datetime.fromisoformat(a.now) if a.now else dt.datetime.now(dt.timezone.utc)
    test = bool(a.out)
    offline = bool(a.stories)

    pending = tidy_queue(now, dry=test)
    if pending and not a.always and not test:
        log(f"{pending} fresh post(s) already waiting in the queue; not making another")
        return finish(False)

    log("collecting news...")
    stories = json.loads(Path(a.stories).read_text()) if a.stories else news.collect(log=log)
    seen = load(SEEN, {"urls": {}, "titles": {}, "runs": 0})
    ranked = news.rank(stories, seen, now, CFG["max_story_age_hours"])
    log(f"{len(stories)} stories -> {len(ranked)} fresh, uncovered news items")
    for r in ranked[:6]:
        log(f"  {r['score']:6.3f}  {r['age_h']:4.1f}h  {len(r['sources'])} src  {r['stories'][0]['title'][:90]}")
    if not ranked:
        log("nothing new to post")
        return finish(False)

    mix = CFG["format_mix"]
    fmt = a.format or mix[seen.get("runs", 0) % len(mix)]
    if fmt == "roundup" and len(ranked) < 3:
        fmt = "media_top"
    clusters = ranked[:4] if fmt == "roundup" else ranked[:1]
    for cl in clusters:
        enrich(cl, offline)

    post = writer.write(fmt, clusters, os.environ.get("AI_NEWS_MODEL") or CFG["llm_model"])
    if post is None:                       # deep-dive carousel needs Claude; fall back to a single
        fmt = "media_top"
        post = writer.write(fmt, clusters, CFG["llm_model"])
    if fmt == "media_top" and not offline and story_image(clusters[0]) is None:
        fmt = "text"                       # no real picture: a clean text card beats generic art
    log(f"format: {fmt}, writer: {post['writer']}")

    if test:
        out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
        for f in out.glob("*.jpg"):
            f.unlink()
    else:
        out = QUEUE / f"{next_number():04d}-news-{slugify(post['headline'])}"
        out.mkdir(parents=True)
    files = render(fmt, post, clusters, out, now, offline)
    (out / "caption.txt").write_text(caption(fmt, post, clusters) + "\n")
    (out / "meta.json").write_text(json.dumps({
        "generated_at": now.isoformat(), "format": fmt, "writer": post["writer"],
        "stories": [{"title": c["stories"][0]["title"], "url": c["stories"][0]["url"], "sources": c["sources"],
                     "score": c["score"]} for c in clusters]}, indent=2) + "\n")
    log(f"made {out.relative_to(ROOT) if not test else out} ({len(files)} slide(s))")

    if not test:
        stamp = now.isoformat()
        for cl in clusters:
            for x in cl["stories"]:
                seen["urls"][news.norm_url(x["url"])] = stamp
            seen["titles"][cl["stories"][0]["title"]] = stamp
        cutoff = now - dt.timedelta(days=7)
        for k in ("urls", "titles"):
            seen[k] = {u: t for u, t in seen[k].items() if dt.datetime.fromisoformat(t) > cutoff}
        seen["runs"] = seen.get("runs", 0) + 1
        SEEN.parent.mkdir(parents=True, exist_ok=True)
        SEEN.write_text(json.dumps(seen, indent=1) + "\n")
    return finish(not test)


def finish(created):
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"created={'true' if created else 'false'}\n")


if __name__ == "__main__":
    main()
