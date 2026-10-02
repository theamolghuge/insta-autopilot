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

## Visual system (implemented in `generator/ai-news/brand.py`)
| Token | Value | Use |
|---|---|---|
| Background | `#000000` black | every slide |
| Text | `#FFFFFF` white | headlines; body is `#D6D6D6` |
| Highlight | `#FFD60A` yellow | the important words (wrap them in `[brackets]`), category tag, numbers, brand dot |
| Muted | `#808080` | date, page counter, source |

- **Typography (fixed):** Space Grotesk Bold for headlines and numbers, Inter for body text,
  JetBrains Mono (uppercase, letter-spaced) for labels. All OFL, bundled in `generator/ai-news/fonts/`.
- Size 1080 x 1350 (4:5), JPEG.
- Every slide: yellow dot + `AI NEWS` top-left, date top-right, handle bottom-left,
  source / page counter / `SWIPE ->` bottom-right, yellow category tag above the headline.
- **With a picture:** the article's own image fills the top 40% (540 px) and fades into black;
  text sits in the bottom 60%. Image credit `IMAGE: <SOURCE>` sits on the picture.
- **Without a picture:** text-only card with a large headline.

## Formats (rotation in `generator/ai-news/config.json` -> `format_mix`)
| Format | What it is |
|---|---|
| `media_top` | single: article image on top 40%, headline + 1-2 sentence summary below |
| `text` | single: headline + summary, no image |
| `carousel` | one big story: cover with image, 2-3 points (what happened / why it matters / what's next), sources + follow slide. Needs the Claude writer |
| `roundup` | top 3-4 stories: numbered list cover, one image slide per story, sources + follow slide |

Default rotation (8 runs = 1 day): image, carousel, image, text, carousel, image, roundup, image.

## Content rules
- One post every 3 hours, always the biggest story not yet covered (ranked by how many outlets cover it, freshness,
  source weight, big names, launch/funding/policy words). Same story from several outlets counts once.
- Stories older than 18 h are ignored. An unposted post older than 6 h is thrown away (news must be fresh).
- Every post credits its source on the image and in the caption.
- Caption: headline, 2-4 sentence summary, `Source:` line, optional question, follow line, up to 12 hashtags.
