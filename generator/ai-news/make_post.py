#!/usr/bin/env python3
"""Make ONE fresh AI-news post and put it in the account's queue.

Run by .github/workflows/ai-news.yml. Normally the story and copy come from a BRIEF that the Claude
scheduled task pushes to content/<account>/briefs/ (see CLAUDE_TASK.md); this script then fetches the
article image, renders, and queues it. With no brief (safety net) it does everything itself:
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
from brand import render_still, plain               # noqa: E402
import video                                          # noqa: E402

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
def tidy_queue(now, dry, drop_all=False):
    """Remove unposted news items older than drop_unposted_after_hours (or all unposted ones when
    drop_all). Returns how many fresh unposted items are left."""
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
        has_media = any(p.suffix.lower() in (".jpg", ".jpeg", ".mp4") for p in item.iterdir())
        if not has_media:                      # e.g. a video post whose file lived only on a past runner
            log(f"dropping {item.name}: its media isn't here any more")
            if not dry:
                shutil.rmtree(item)
            continue
        if drop_all or age > CFG["drop_unposted_after_hours"]:
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
    if "_img" not in cl:
        cl["_img"] = _find_image(cl)
    return cl["_img"]


def _find_image(cl):
    lead = cl["stories"][0]
    for url in (cl.get("brief_image"), cl.get("og_image"), lead.get("feed_image")):
        im = news.load_image(url)
        if im is not None:
            return im
    for x in cl["stories"][1:3]:                       # another outlet covering the same story
        img, _, _, _ = news.article(x["url"])
        im = news.load_image(img) or news.load_image(x.get("feed_image"))
        if im is not None:
            cl["image_source"] = x["source"]
            return im
    return None


def enrich(cl, offline=False):
    if offline:
        cl.setdefault("text", cl["stories"][0].get("summary", ""))
        cl.setdefault("inline", [])
        cl.setdefault("videos", [])
        return cl
    img, text, inline, videos = news.article(cl["stories"][0]["url"])
    cl["og_image"], cl["text"], cl["inline"] = img, text, inline
    # official clips: only from pages on the announcing company's own site
    domains = CFG.get("official_video_domains", [])
    cl.setdefault("videos", [])
    for x in cl["stories"]:
        page_videos = videos if x is cl["stories"][0] else None
        if not news.is_official(x["url"], domains):
            continue
        if page_videos is None:
            page_videos = news.article(x["url"])[3]
        cl["videos"] += [{"url": v, "page": x["url"], "source": x["source"]} for v in page_videos]
    return cl


def is_single(fmt):
    return fmt in ("single", "media_top", "text")


# ---------------------------------------------------------------- rendering
def render(fmt, post, clusters, out, now, offline):
    """single  -> one post card (article picture under the text, or text-only)
    carousel   -> headline cover + one post card per point (each with its own article picture if any)"""
    files = []
    cl = clusters[0]
    src = cl["sources"][0]
    test_img = os.environ.get("AI_NEWS_TEST_IMAGE") if offline else None

    def main_image():
        if offline:
            from PIL import Image
            return (Image.open(test_img).convert("RGB") if test_img else None), src
        return story_image(cl), cl.get("image_source") or src

    used = set()

    def extra_image(hint):
        """A further picture for an inside slide: the brief's own pick, else an inline article image."""
        if offline:
            return None
        for url in [hint] + cl.get("inline", []):
            if not url or url in used:
                continue
            used.add(url)
            im = news.load_image(url, min_w=500)
            if im is not None:
                return im
        return None

    def save(slide, media=None):
        p = out / f"{len(files) + 1:02d}.jpg"
        render_still(slide, p, media)
        files.append(p)

    if fmt == "video":
        made = make_reel(post, cl, out, offline, main_image)
        if made:
            files.append(made)
            return files
        fmt = "single"                                 # no clip and no picture: plain post card
    if is_single(fmt):
        im, who = main_image() if fmt != "text" else (None, None)
        save({"layout": "card", "text": post["headline"], "source": src,
              "credit": f"Image: {who}" if im is not None else None}, im)
    else:
        pts = post["points"]
        n = 1 + len(pts)
        im, who = main_image()
        save({"layout": "headline", "headline": post["headline"], "swipe": True,
              "credit": f"Image: {who}" if im is not None else None}, im)
        for i, p in enumerate(pts, 2):
            pim = extra_image(p.get("image"))
            save({"layout": "card", "text": p["text"], "page": f"{i}/{n}", "source": src,
                  "credit": f"Image: {src}" if pim is not None else None}, pim)
    return files


def make_reel(post, cl, out, offline, main_image):
    """01.mp4: an official clip inside the post card, else a slow zoom over the article picture.
    Returns the path, or None if neither is possible (then the caller makes a still)."""
    if not video.has_ffmpeg():
        log("ffmpeg missing: making a still instead of a video")
        return None
    src = cl["sources"][0]
    target = out / "01.mp4"
    slide = {"layout": "card", "text": post["headline"]}
    clips = list(cl.get("videos", []))
    if offline and os.environ.get("AI_NEWS_TEST_VIDEO"):
        clips = [{"url": "file://" + os.environ["AI_NEWS_TEST_VIDEO"], "source": src, "page": ""}]
    for c in clips:
        tmp = out / "_clip"
        got = (Path(c["url"][7:]) if c["url"].startswith("file://") else news.download(c["url"], tmp))
        if not got:
            continue
        try:
            video.clip_reel(dict(slide, credit=f"Video: {c.get('source') or src}"), got, target,
                            start=c.get("start", 0), max_len=min(30, float(c.get("length") or 30)))
            log(f"reel from official clip {c['url'][:90]}")
            return target
        except Exception as e:
            log(f"clip unusable ({str(e)[:80]}); trying the next option")
        finally:
            if tmp.exists():
                tmp.unlink()
    im, who = main_image()
    if im is not None:
        video.motion_reel(dict(slide, credit=f"Image: {who}"), im, target)
        log("reel from the article picture (no usable official clip)")
        return target
    return None


def caption(fmt, post, clusters):
    """Slides stay short; the caption carries the detail (4-6 short paragraphs)."""
    lines = [plain(post["headline"]), ""]
    lines.append((post.get("caption_summary") or "").strip())
    lines += ["", post.get("question") or "What do you think?"]
    srcs = clusters[0]["sources"][:3]
    lines += ["", "Source: " + ", ".join(srcs)]
    lines += ["", f"Follow {CFG['handle']} for the latest AI news, every 3 hours.", "."]
    tags = []
    for t in post.get("hashtags", []) + CFG["hashtags"]:
        if t.lower() not in tags:
            tags.append(t.lower())
    lines.append(" ".join(tags[:12]))
    return "\n".join(lines)[:2200]


# ---------------------------------------------------------------- briefs (written by the Claude scheduled task)
BRIEFS = ROOT / "content" / ACC / "briefs"


def pending_briefs():
    return sorted(BRIEFS.glob("*.json")) if BRIEFS.exists() else []


def from_brief(path, now, seen):
    """A brief = the story Claude picked + the copy Claude wrote. Returns (fmt, post, clusters) or None."""
    b = json.loads(Path(path).read_text())
    made = dt.datetime.fromisoformat(b["created_at"].replace("Z", "+00:00"))
    if (now - made).total_seconds() / 3600 > CFG["drop_unposted_after_hours"]:
        log(f"brief {Path(path).name} is older than {CFG['drop_unposted_after_hours']} h; ignoring it")
        return None
    st = b["story"]
    stories = [{"source": st["source"], "title": st["title"], "url": st["url"], "summary": st.get("summary", ""),
                "published": st.get("published"), "feed_image": st.get("image", ""), "weight": 1}]
    stories += [{"source": x["source"], "title": x.get("title", st["title"]), "url": x["url"], "summary": "",
                 "published": None, "feed_image": x.get("image", ""), "weight": 1} for x in b.get("also", [])]
    if any(news.norm_url(x["url"]) in seen.get("urls", {}) for x in stories) or \
            any(news.similar(st["title"], t) >= 0.6 for t in seen.get("titles", {})):
        log(f"brief {Path(path).name}: this story was already covered; ignoring it")
        return None
    fmt = {"media_top": "single"}.get(b.get("format"), b.get("format", "single"))
    if fmt not in ("single", "text", "carousel", "video"):
        fmt = "single"
    post = writer._check(dict(b["post"]), fmt, 1)
    post["writer"] = "claude-task"
    srcs = []
    for x in stories:
        if x["source"] not in srcs:
            srcs.append(x["source"])
    cl = {"stories": stories, "sources": srcs, "score": None, "brief_image": st.get("image"), "videos": []}
    v = st.get("video") or {}
    if isinstance(v, str):
        v = {"url": v}
    if v.get("url"):
        page = v.get("page") or st["url"]
        if news.is_official(page, CFG.get("official_video_domains", [])):
            cl["videos"].append({"url": v["url"], "page": page, "source": v.get("source") or st["source"],
                                 "start": v.get("start", 0), "length": v.get("length", 30)})
        else:
            log(f"brief video ignored: {page} is not an official company page")
    return fmt, post, [cl]


def last_post_age_h(now):
    state = load(STATE, {})
    times = [dt.datetime.fromisoformat(v["posted_at"]) for v in state.get("posted", {}).values() if v.get("posted_at")]
    return (now - max(times)).total_seconds() / 3600 if times else 999


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stories", help="JSON file of stories instead of fetching feeds (testing)")
    ap.add_argument("--brief", help="use this brief file (default: oldest waiting in content/<acc>/briefs/)")
    ap.add_argument("--fallback", action="store_true",
                    help="safety net: only make a post if nothing was posted in the last 2.5 h and no brief is waiting")
    ap.add_argument("--out", help="write the post here instead of the queue (testing; nothing is recorded)")
    ap.add_argument("--format", choices=["single", "text", "carousel", "video"], help="force a format")
    ap.add_argument("--now", help="pretend time (ISO)")
    ap.add_argument("--no-fetch", action="store_true", help="don't download article pages/images (sandbox checks)")
    ap.add_argument("--always", action="store_true", help="make a post even if a fresh one is already waiting")
    a = ap.parse_args()
    now = dt.datetime.fromisoformat(a.now) if a.now else dt.datetime.now(dt.timezone.utc)
    test = bool(a.out)
    offline = bool(a.stories) or a.no_fetch
    seen = load(SEEN, {"urls": {}, "titles": {}, "runs": 0})
    briefs = [Path(a.brief)] if a.brief else ([] if a.stories else pending_briefs())

    result = None
    for bp in briefs:                                   # Claude's briefs come first
        result = from_brief(bp, now, seen)
        if not test:
            bp.unlink(missing_ok=True)                  # used or rejected: either way it's done
        if result:
            log(f"using brief {bp.name}")
            tidy_queue(now, dry=test, drop_all=not test)  # the brief is the freshest pick
            break

    if result is None:
        if a.fallback and last_post_age_h(now) < 2.5:
            log(f"last post was {last_post_age_h(now):.1f} h ago; the safety net isn't needed")
            return finish(False)
        pending = tidy_queue(now, dry=test)
        if pending and not a.always and not test:
            log(f"{pending} fresh post(s) already waiting in the queue; not making another")
            return finish(False)
        log("collecting news...")
        stories = json.loads(Path(a.stories).read_text()) if a.stories else news.collect(log=log)
        ranked = news.rank(stories, seen, now, CFG["max_story_age_hours"])
        log(f"{len(stories)} stories -> {len(ranked)} fresh, uncovered news items")
        for r in ranked[:6]:
            log(f"  {r['score']:6.3f}  {r['age_h']:4.1f}h  {len(r['sources'])} src  {r['stories'][0]['title'][:90]}")
        if not ranked:
            log("nothing new to post")
            return finish(False)
        mix = CFG["format_mix"]
        fmt = a.format or mix[seen.get("runs", 0) % len(mix)]
        clusters = ranked[:1]                  # every post covers exactly one story
        enrich(clusters[0], offline)
        post = writer.write(fmt, clusters, os.environ.get("AI_NEWS_MODEL") or CFG["llm_model"])
        if post is None:                       # a carousel needs Claude's writing; fall back to a single
            fmt = "single"
            post = writer.write(fmt, clusters, CFG["llm_model"])
    else:
        fmt, post, clusters = result
        if a.format:
            fmt = a.format
        enrich(clusters[0], offline)
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
