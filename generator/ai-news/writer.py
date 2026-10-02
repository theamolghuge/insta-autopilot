"""Turn ranked stories into post copy.

With ANTHROPIC_API_KEY set, Claude writes headline / body / carousel points / caption from the
article text. Without it, a rule-based writer uses the feed's own headline and first sentence.
Both return the same dict shape, so rendering never cares which one ran.
"""
import json, os, re, urllib.request, urllib.error

CATEGORIES = ["Models", "Funding", "Policy", "Research", "Chips", "Tools", "Robotics", "Business", "Safety", "Open Source"]

SYSTEM = """You write posts for an Instagram page that brings people the latest AI news from around the world.
Voice: clear, neutral, fast to read. Like a sharp news editor, not a hype account.
Hard rules:
- Use ONLY facts stated in the provided source text. Never add numbers, dates, names or claims that are not there.
- If something is unconfirmed in the source (a report, a rumour), say "reportedly" or "according to <source>".
- No emojis in on-image text. No clickbait, no "game-changer", no "revolutionary".
- Wrap the 1-4 most important words of each headline in [square brackets]; they are shown in yellow.
  Brackets must be balanced and never nested. Highlight names, numbers, or the key outcome.
- Write in your own words; do not copy sentences from the source.
Reply with JSON only, no markdown fences."""

SCHEMA = {
    "single": """{
  "kicker": one of %(cats)s,
  "headline": "max 12 words, with [highlight]",
  "body": "1-2 sentences, max 32 words: what happened and the key detail",
  "caption_summary": "2-4 short sentences for the caption: what happened, why it matters",
  "question": "one short question to invite comments, or empty string",
  "hashtags": ["3-5 specific hashtags for this story, e.g. #openai"],
  "image_word": "one short word to print on a fallback graphic, e.g. GEMINI"
}""",
    "carousel": """{
  "kicker": one of %(cats)s,
  "headline": "cover headline, max 12 words, with [highlight]",
  "body": "cover line, max 22 words",
  "points": [
    {"heading": "What happened (max 7 words, may use [highlight])", "body": "max 40 words"},
    {"heading": "Why it [matters] or similar, max 7 words", "body": "max 40 words"},
    {"heading": "What to watch next, max 7 words", "body": "max 40 words; only if the source supports it"}
  ],
  "caption_summary": "2-4 short sentences",
  "question": "one short question, or empty string",
  "hashtags": ["3-5 specific hashtags"],
  "image_word": "one short word"
}
Give 2 or 3 points. Drop the third if the source doesn't support it.""",
    "roundup": """{
  "headline": "max 6 words, with [highlight], e.g. 'The AI news [you missed]'",
  "items": ["one line per story, max 9 words each, with [highlight], same order as given"],
  "slides": [{"kicker": one of %(cats)s, "headline": "max 12 words with [highlight]", "body": "max 26 words"}],
  "caption_summary": "one line per story, each starting with a number like '1/'",
  "hashtags": ["3-5 hashtags"]
}
"items" and "slides" have exactly one entry per story, in the given order.""",
}


def _claude(prompt, model, key):
    body = json.dumps({"model": model, "max_tokens": 1800, "system": SYSTEM,
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body, method="POST", headers={
        "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        out = json.loads(r.read())
    text = "".join(b.get("text", "") for b in out.get("content", []) if b.get("type") == "text")
    text = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.M).strip()
    return json.loads(text[text.find("{"): text.rfind("}") + 1])


def _story_block(i, cl):
    lead = cl["stories"][0]
    others = "; ".join(f'{x["source"]}: {x["title"]}' for x in cl["stories"][1:4])
    return (f"STORY {i}\nHeadline ({lead['source']}): {lead['title']}\n"
            f"Also reported by: {others or 'none'}\nPublished: {lead.get('published')}\n"
            f"Feed summary: {lead.get('summary', '')[:800]}\n"
            f"Article text (may be partial): {cl.get('text', '')[:3500]}\n")


def balanced(s):
    depth = 0
    for ch in s:
        depth += ch == "["; depth -= ch == "]"
        if depth < 0 or depth > 1:
            return False
    return depth == 0


def _check(post, fmt, n):
    def fix(s):
        s = " ".join(str(s or "").split())
        return s if balanced(s) else s.replace("[", "").replace("]", "")
    for k in ("headline", "body", "caption_summary", "question"):
        if k in post:
            post[k] = fix(post[k])
    if post.get("kicker") not in CATEGORIES:
        post["kicker"] = "Business" if fmt != "roundup" else None
    if fmt == "carousel":
        pts = [p for p in post.get("points", []) if p.get("heading") and p.get("body")][:3]
        if len(pts) < 2:
            raise ValueError("carousel needs 2+ points")
        post["points"] = [{"heading": fix(p["heading"]), "body": fix(p["body"])} for p in pts]
    if fmt == "roundup":
        if len(post.get("items", [])) != n or len(post.get("slides", [])) != n:
            raise ValueError("roundup length mismatch")
        post["items"] = [fix(x) for x in post["items"]]
        for sl in post["slides"]:
            sl["headline"], sl["body"] = fix(sl.get("headline")), fix(sl.get("body"))
            if sl.get("kicker") not in CATEGORIES:
                sl["kicker"] = "Business"
    tags = [t if t.startswith("#") else "#" + t for t in post.get("hashtags", []) if t]
    post["hashtags"] = [re.sub(r"[^#\w]", "", t.lower()) for t in tags][:5]
    if not post.get("headline"):
        raise ValueError("no headline")
    return post


def write_llm(fmt, clusters, model):
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        return None
    blocks = "\n".join(_story_block(i + 1, c) for i, c in enumerate(clusters))
    prompt = (f"Format: {fmt}\n\n{blocks}\nReturn JSON exactly in this shape:\n"
              + SCHEMA[fmt] % {"cats": json.dumps(CATEGORIES)})
    last = None
    for _ in range(2):
        try:
            return _check(_claude(prompt, model, key), fmt, len(clusters))
        except (urllib.error.URLError, ValueError, KeyError, json.JSONDecodeError) as e:
            last = e
    print(f"  Claude writer failed ({str(last)[:120]}); using rule-based writer")
    return None


# ---------------------------------------------------------------- rule-based fallback
from news import BIG_NAMES  # noqa: E402

KICKER_RULES = [
    ("Funding", r"\b(raises?|funding|valuation|invest\w*|ipo|acquir\w*|billion)\b"),
    ("Policy", r"\b(law|regulat\w*|ban\w*|senate|congress|eu|ai act|government|court|lawsuit|sues?|policy)\b"),
    ("Chips", r"\b(chip\w*|gpu\w*|nvidia|tsmc|semiconductor\w*|data ?cent\w*)\b"),
    ("Robotics", r"\b(robot\w*|humanoid\w*|self-driving|autonomous)\b"),
    ("Research", r"\b(paper|research\w*|study|scientists?|benchmark\w*)\b"),
    ("Safety", r"\b(safety|risk\w*|alignment|deepfake\w*|misuse)\b"),
    ("Open Source", r"\b(open[- ]source|open[- ]weight\w*)\b"),
    ("Models", r"\b(model\w*|gpt-?\w*|gemini|claude|llama|llm\w*|release\w*|launch\w*)\b"),
    ("Tools", r"\b(chatgpt|app|feature|tool\w*|update|copilot|agent\w*)\b"),
]


def kicker_for(text):
    for name, pat in KICKER_RULES:
        if re.search(pat, text, re.I):
            return name
    return "Business"


def auto_highlight(title):
    """Highlight one key run: a known big name, else a money/percent figure, else the first capitalised name."""
    words = title.split()
    if len(words) > 16:
        words = words[:15]; words[-1] = words[-1].rstrip(",;:") + "..."
    pats = [r"^\$?\d[\d,.]*(%|[bmk]|bn)?$", None]
    for i, w in enumerate(words):
        if BIG_NAMES.fullmatch(re.sub(r"[^\w\-]", "", w)) or re.match(r"^\$\d", w):
            j = i
            while j + 1 < len(words) and j - i < 2 and (words[j + 1][:1].isupper() or words[j + 1][:1].isdigit()):
                j += 1
            words[i] = "[" + words[i]; words[j] = words[j] + "]"
            return " ".join(words)
    for i, w in enumerate(words[1:], 1):
        if re.match(pats[0], w, re.I) or (w[:1].isupper() and w.lower() not in ("i", "a")):
            words[i] = "[" + w + "]"
            return " ".join(words)
    return " ".join(words)


def first_sentences(text, max_words=32):
    text = re.sub(r"\s+", " ", text or "").strip()
    text = re.sub(r"(The post .* appeared first on .*|Read more.*|Continue reading.*)$", "", text).strip()
    out = []
    for s in re.split(r"(?<=[.!?])\s+", text):
        if len((" ".join(out + [s])).split()) > max_words:
            break
        out.append(s)
    if not out and text:
        first = re.split(r"(?<=[.!?])\s+", text)[0]
        if len(first.split()) <= max_words + 14:          # keep a whole sentence rather than cut it
            out = [first]
        else:
            out = [" ".join(first.split()[:max_words]).rstrip(",;:") + "..."]
    return " ".join(out)


def write_rules(fmt, clusters):
    if fmt == "roundup":
        slides, items = [], []
        for c in clusters:
            s = c["stories"][0]
            items.append(auto_highlight(s["title"]))
            slides.append({"kicker": kicker_for(s["title"] + " " + s["summary"]),
                           "headline": auto_highlight(s["title"]), "body": first_sentences(s["summary"], 26)})
        return {"headline": "The AI news [you missed]", "items": items, "slides": slides,
                "caption_summary": "\n".join(f"{i}/ {c['stories'][0]['title']}" for i, c in enumerate(clusters, 1)),
                "hashtags": []}
    s = clusters[0]["stories"][0]
    return {"kicker": kicker_for(s["title"] + " " + s["summary"]), "headline": auto_highlight(s["title"]),
            "body": first_sentences(s["summary"], 28), "caption_summary": first_sentences(s["summary"], 60),
            "question": "", "hashtags": [], "image_word": kicker_for(s["title"])}


def write(fmt, clusters, model):
    post = write_llm(fmt, clusters, model)
    if post:
        post["writer"] = "claude"
        return post
    if fmt == "carousel":
        return None                     # a deep-dive carousel needs the model; caller picks another format
    post = write_rules(fmt, clusters)
    post["writer"] = "rules"
    return post
