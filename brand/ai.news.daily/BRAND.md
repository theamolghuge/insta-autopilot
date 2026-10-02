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
Post format modelled on the big AI news pages (post-card singles, big-headline carousel covers,
detail in the caption), in our own identity: black, white, yellow highlights, our logo, no verified badge.

| Token | Value | Use |
|---|---|---|
| Background | `#000000` black | every slide |
| Text | `#FFFFFF` white | all slide text |
| Highlight | `#FFD60A` yellow | key words (wrap them in `[brackets]`), logo dot |
| Grey | `#8C8C8C` | handle, source, credits |

**Typography (fixed)**
| Role | Typeface | Setting |
|---|---|---|
| Carousel cover headline | Inter Tight Black (900), ALL CAPS, centred | 56-84 px, line height 1.02 |
| Card text | Inter Tight Medium (500); highlights Inter Tight Bold (700) in yellow | 38-60 px, line height 1.25 |
| Name / handle | Inter Tight Bold 34 px / Geist 28 px grey | |
| Small labels (source, image credit, page) | Geist Mono SemiBold, letter-spaced | 16-22 px |

All fonts are OFL and bundled in `generator/ai-news/fonts/`.

## Templates (1080 x 1350, JPEG)
| Template | Layout |
|---|---|
| **Post card** | round logo + "AI News" + handle at the top, 1-2 sentences, then the article's picture filling the rest (always at least 40% of the slide), credit `IMAGE: <SOURCE>` on the picture. With no picture: text-only, centred, larger, with `SOURCE:` under it |
| **Headline cover** | article picture on top fading into black, centred `AI NEWS •` rule, huge ALL-CAPS headline, `SWIPE FOR MORE` |

## Formats (one story per post, always)
| Format | Slides |
|---|---|
| `single` | one post card |
| `carousel` | headline cover + 2-4 post cards, one fact each, each with its own article picture when there is one |
| `video` | Reel (1080 x 1350, up to 30 s): post card with a video where the picture would be. Uses the company's OWN official clip when there is one (never YouTube/X/TikTok/broadcasters), else a slow zoom over the article picture. Credit `VIDEO: <SOURCE>` |

The caption carries the detail: headline, 4-6 short paragraphs, a question, `Source:` line, follow line, hashtags.
Never a placeholder or generated picture: no real image means a text-only card.

## Content rules
- One post every 3 hours (written by the Claude scheduled task, see `generator/ai-news/CLAUDE_TASK.md`), always the biggest story not yet covered (ranked by how many outlets cover it, freshness,
  source weight, big names, launch/funding/policy words). Same story from several outlets counts once.
- Stories older than 18 h are ignored. An unposted post older than 6 h is thrown away (news must be fresh).
- Every post credits its source on the image and in the caption.
- Caption: headline, 4-6 short paragraphs, question, `Source:` line, follow line, up to 12 hashtags.
