"""Collect AI news from RSS/Atom feeds, group duplicates, rank, and find each story's image.

Standard library only. Feeds that fail are skipped (a dead feed never stops a run).
"""
import datetime as dt, email.utils, gzip, html, io, re, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (compatible; ai-news-autopilot/1.0; +https://github.com/theamolghuge/insta-autopilot)"

# name, url, weight, ai_only (False = filter items by AI keywords)
FEEDS = [
    ("OpenAI", "https://openai.com/news/rss.xml", 1.35, True),
    ("Google", "https://blog.google/technology/ai/rss/", 1.25, True),
    ("Google DeepMind", "https://deepmind.google/blog/rss.xml", 1.3, True),
    ("Hugging Face", "https://huggingface.co/blog/feed.xml", 1.0, True),
    ("TechCrunch", "https://techcrunch.com/category/artificial-intelligence/feed/", 1.15, True),
    ("The Verge", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", 1.15, True),
    ("VentureBeat", "https://venturebeat.com/category/ai/feed/", 1.05, True),
    ("Ars Technica", "https://arstechnica.com/ai/feed/", 1.1, True),
    ("MIT Technology Review", "https://www.technologyreview.com/topic/artificial-intelligence/feed", 1.1, True),
    ("Wired", "https://www.wired.com/feed/tag/ai/latest/rss", 1.05, True),
    ("The Decoder", "https://the-decoder.com/feed/", 1.0, True),
    ("AI News", "https://www.artificialintelligence-news.com/feed/", 0.95, True),
    ("MarkTechPost", "https://www.marktechpost.com/feed/", 0.9, True),
    ("Analytics India Magazine", "https://analyticsindiamag.com/feed/", 0.9, False),
    ("Rest of World", "https://restofworld.org/feed/latest", 1.0, False),
    ("NVIDIA", "https://blogs.nvidia.com/feed/", 1.0, False),
]

AI_WORDS = re.compile(r"\b(ai|a\.i\.|artificial intelligence|llm|gpt|chatgpt|claude|gemini|llama|openai|anthropic|"
                      r"deepmind|machine learning|neural|chatbot|copilot|agentic|agents?|genai|generative|model|"
                      r"robot|robotics|gpu|nvidia|mistral|deepseek|xai|grok|perplexity|qwen)\b", re.I)
BIG_NAMES = re.compile(r"\b(openai|anthropic|claude|google|gemini|deepmind|meta|llama|nvidia|microsoft|apple|"
                       r"amazon|aws|xai|grok|mistral|deepseek|alibaba|qwen|tesla|samsung|chatgpt|gpt-\w+|"
                       r"hugging face|perplexity|tsmc|amd|intel|baidu|tencent|bytedance)\b", re.I)
EVENT_WORDS = re.compile(r"\b(launch\w*|releas\w*|unveil\w*|announc\w*|introduc\w*|raises?|funding|acquir\w*|"
                         r"open[- ]source\w*|ban\w*|lawsuit|sues?|regulat\w*|law|record|billion|breakthrough|"
                         r"new model|beats?|tops?|outage|leak\w*|partnership|deal)\b", re.I)
JUNK = re.compile(r"\b(deal of|% off|sale|discount|coupon|podcast|webinar|sponsored|how to|best \w+ (for|of)|"
                  r"review:|hands-on|tutorial|guide to|newsletter|this week in|quiz)\b", re.I)
STOP = set("a an the of to in on for and or with by at from as is are be its it this that new how why what "
           "will can now has have after over into says said up out".split())

NS = {"media": "http://search.yahoo.com/mrss/", "atom": "http://www.w3.org/2005/Atom",
      "content": "http://purl.org/rss/1.0/modules/content/"}


def fetch(url, limit=3_000_000, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*", "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read(limit)
        if r.headers.get("Content-Encoding") == "gzip":
            data = gzip.decompress(data)
        return data, r.headers.get("Content-Type", ""), r.geturl()


def strip_html(s):
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s or "", flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return " ".join(html.unescape(s).split())


def parse_date(s):
    if not s:
        return None
    s = s.strip()
    try:
        d = email.utils.parsedate_to_datetime(s)
    except Exception:
        try:
            d = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
        except Exception:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=dt.timezone.utc)
    return d.astimezone(dt.timezone.utc)


def _txt(el, *paths):
    for p in paths:
        x = el.find(p, NS)
        if x is not None and (x.text or "").strip():
            return x.text.strip()
    return ""


def parse_feed(xml_bytes, source, weight, ai_only):
    root = ET.fromstring(xml_bytes)
    items = root.findall(".//item") or root.findall(".//atom:entry", NS)
    out = []
    for it in items:
        title = strip_html(_txt(it, "title", "atom:title"))
        link = _txt(it, "link")
        if not link:
            l = it.find("atom:link[@rel='alternate']", NS)
            if l is None:
                l = it.find("atom:link", NS)
            link = l.get("href", "") if l is not None else ""
        desc = strip_html(_txt(it, "description", "atom:summary", "content:encoded", "atom:content"))
        when = parse_date(_txt(it, "pubDate", "atom:published", "atom:updated",
                               "{http://purl.org/dc/elements/1.1/}date"))
        img = ""
        for tag in ("media:content", "media:thumbnail"):
            for m in it.findall(tag, NS):
                if m.get("url") and (m.get("medium") in (None, "image") or tag == "media:thumbnail"):
                    img = m.get("url"); break
            if img:
                break
        if not img:
            enc = it.find("enclosure")
            if enc is not None and (enc.get("type") or "").startswith("image"):
                img = enc.get("url", "")
        if not img:
            m = re.search(r'<img[^>]+src="([^"]+)"', _txt(it, "content:encoded", "description") or "")
            img = m.group(1) if m else ""
        if not title or not link:
            continue
        if not ai_only and not AI_WORDS.search(title + " " + desc[:300]):
            continue
        out.append({"source": source, "weight": weight, "title": title, "url": link.strip(),
                    "summary": desc[:1200], "published": when.isoformat() if when else None, "feed_image": img})
    return out


def collect(feeds=FEEDS, log=print):
    stories = []
    for name, url, w, ai_only in feeds:
        try:
            data, _, _ = fetch(url)
            got = parse_feed(data, name, w, ai_only)
            stories += got
            log(f"  {name}: {len(got)} items")
        except Exception as e:
            log(f"  {name}: skipped ({str(e)[:80]})")
    return stories


# ---------------------------------------------------------------- grouping and ranking
def key_words(title):
    return {w for w in re.findall(r"[a-z0-9][a-z0-9\-\.]+", title.lower()) if w not in STOP and len(w) > 2}


def names(title):
    """Distinctive capitalised names / versioned tokens, minus very common company names."""
    toks = re.findall(r"\b[A-Z][\w\-\.]*[\w]|\b\w*\d\w*\b", title)
    return {t.lower() for t in toks if not BIG_NAMES.fullmatch(t) and t.lower() not in STOP | {"ai"} and len(t) > 1}


def similar(a, b):
    A, B = key_words(a), key_words(b)
    if not A or not B:
        return 0
    s = len(A & B) / min(len(A), len(B))
    if s >= 0.25 and names(a) & names(b):     # e.g. both mention "Argon" -> same launch
        s = max(s, 0.6)
    return s


def norm_url(u):
    p = urllib.parse.urlsplit(u)
    return (p.netloc.replace("www.", "") + p.path).rstrip("/").lower()


def cluster(stories):
    """Group the same news reported by several outlets. Returns list of clusters (lists)."""
    clusters = []
    for s in sorted(stories, key=lambda s: -s["weight"]):
        for c in clusters:
            if any(norm_url(s["url"]) == norm_url(x["url"]) or similar(s["title"], x["title"]) >= 0.6 for x in c):
                c.append(s); break
        else:
            clusters.append([s])
    return clusters


def score(c, now):
    lead = c[0]
    srcs = {x["source"] for x in c}
    ages = [(now - dt.datetime.fromisoformat(x["published"])).total_seconds() / 3600 for x in c if x["published"]]
    age = min(ages) if ages else 12
    text = " ".join(x["title"] for x in c)
    sc = max(x["weight"] for x in c)
    sc *= 1 + 0.55 * (len(srcs) - 1)                       # covered by several outlets = big story
    sc *= 0.5 ** (max(age, 0) / 8)                         # freshness, half-life 8 h
    sc *= 1.35 if BIG_NAMES.search(text) else 1
    sc *= 1.25 if EVENT_WORDS.search(text) else 1
    sc *= 0.35 if JUNK.search(lead["title"]) else 1
    return round(sc, 4), age


def rank(stories, seen, now, max_age_h=18):
    out = []
    for c in cluster(stories):
        sc, age = score(c, now)
        if age > max_age_h:
            continue
        if any(norm_url(x["url"]) in seen.get("urls", {}) for x in c):
            continue
        if any(similar(x["title"], t) >= 0.6 for x in c for t in seen.get("titles", {})):
            continue
        out.append({"score": sc, "age_h": round(age, 1), "stories": c,
                    "sources": sorted({x["source"] for x in c}, key=lambda n: -next(
                        x["weight"] for x in c if x["source"] == n))})
    return sorted(out, key=lambda x: -x["score"])


# ---------------------------------------------------------------- article page: image + text
def article(url):
    """Returns (og_image_url, text_excerpt). Best effort, never raises."""
    try:
        data, ctype, final = fetch(url, limit=1_500_000)
        page = data.decode("utf-8", errors="replace")
    except Exception:
        return "", ""
    img = ""
    for pat in (r'<meta[^>]+(?:property|name)=["\']og:image(?::secure_url)?["\'][^>]*content=["\']([^"\']+)',
                r'<meta[^>]+content=["\']([^"\']+)["\'][^>]*(?:property|name)=["\']og:image["\']',
                r'<meta[^>]+name=["\']twitter:image(?::src)?["\'][^>]*content=["\']([^"\']+)'):
        m = re.search(pat, page, re.I)
        if m:
            img = urllib.parse.urljoin(final, html.unescape(m.group(1)))
            break
    paras = [strip_html(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", page, re.S | re.I)]
    paras = [p for p in paras if len(p) > 80 and "cookie" not in p.lower()]
    return img, " ".join(paras)[:4000]


def load_image(url, min_w=600):
    """Download an image and return a PIL image, or None if it's missing/too small/a logo."""
    if not url:
        return None
    try:
        from PIL import Image
        data, ctype, _ = fetch(url, limit=15_000_000)
        im = Image.open(io.BytesIO(data))
        im.load()
        im = im.convert("RGB")
    except Exception:
        return None
    if im.width < min_w or im.height < 300:
        return None
    ratio = im.width / im.height
    if ratio < 0.5 or ratio > 2.6:
        return None
    # mostly one flat colour = logo/placeholder card
    small = im.resize((32, 32))
    colors = small.getcolors(1024)
    if colors and max(c for c, _ in colors) > 0.7 * 1024:
        return None
    return im
