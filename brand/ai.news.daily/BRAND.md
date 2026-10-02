# @ai.news.daily brand kit

**Niche:** the latest AI news from around the world: model launches, funding, policy, chips, research, tools.
**Voice:** clear, neutral, fast. A sharp news editor, not a hype account. Facts from the source only;
"reportedly" for anything unconfirmed. No "game-changer", no "revolutionary", no emojis on images.

## Instagram profile
- **Name field:** `AI News | Every 3 Hours`
- **Category:** News & media website (or Digital creator)
- **Profile picture:** `logo.png`
- **Bio:**
  ```
  The latest AI news, every 3 hours ⚡
  Models • Funding • Policy • Chips • Research
  Sources credited on every post
  ```

## Visual system: "Minimal" (implemented in `generator/ai-news/brand.py`, theme `minimal`)
| Token | Value | Use |
|---|---|---|
| Background | `#000000` black | every slide |
| Headline | `#FFFFFF` white | headlines |
| Highlight | `#FFD60A` yellow | important words (wrap them in `[brackets]`), category chip, numbers, brand dot |
| Body | `#A8A8A8` grey | summaries and point text |
| Meta | `#6E6E6E` | source, date, page counter |

**Typography (fixed):**
| Role | Typeface | Setting |
|---|---|---|
| Headline | Inter Tight Bold (700) | 48-68 px, tracking -2.8%, line height 1.08, sentence case |
| Body | Geist Regular | 40-42 px, line height 1.42 |
| Labels (chip, source, date, handle, page) | Geist Mono Medium | 24 px |
| Brand mark | Inter Tight ExtraBold | "AI News" + yellow dot |

Headlines stay moderate and body text stays large, so posts read easily on a phone.
All fonts are OFL and bundled in `generator/ai-news/fonts/`.

**Layout**
- 1080 x 1350 (4:5), JPEG.
- **With a picture:** the article's own image sits in the top 40% as a rounded inset (30 px corners),
  "AI News" pill on it top-left, `IMAGE: <SOURCE>` credit bottom-right. Text fills the bottom 60%.
- **No picture available:** the slide becomes text-only. Never a placeholder or generated image.
- Above every headline: yellow outlined category chip, then `Source · date` in Geist Mono.
- Footer: thin rule, handle bottom-left, date / page counter / `Swipe →` bottom-right.

Alternative themes `newsroom` (Archivo condensed caps) and `editorial` (Instrument Serif) are kept in
`brand.py` for reference; switch with `"theme"` in `generator/ai-news/config.json`.

## Formats (one story per post, always)
| Format | What it is |
|---|---|
| `media_top` | single: article image on top 40%, headline + 1-2 sentence summary below (text-only if no image) |
| `text` | single: headline + summary, no image |
| `carousel` | deep dive on ONE story: cover, 2-3 points (what happened / why it matters / what to watch), sources + follow slide. Needs the Claude writer; without it a single is made instead |

Default rotation (8 runs = 1 day): image, carousel, image, text, image, carousel, image, text.

## Content rules
- One post every 3 hours, always the biggest story not yet covered (ranked by how many outlets cover it, freshness,
  source weight, big names, launch/funding/policy words). Same story from several outlets counts once.
- Stories older than 18 h are ignored. An unposted post older than 6 h is thrown away (news must be fresh).
- Every post credits its source on the image and in the caption.
- Caption: headline, 2-4 sentence summary, `Source:` line, optional question, follow line, up to 12 hashtags.
