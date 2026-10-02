# @fin.ance18 brand kit

**Niche:** US personal finance and investing, for beginners and young professionals.
**Voice:** calm, practical, encouraging. Short sentences. No hype, no "get rich quick", no stock tips.

## Instagram profile
- **Name field:** `Money Habits | Investing Tips`
- **Category:** Education (or Digital creator)
- **Profile picture:** `logo_A_green.png` (alternatives: `logo_B_cream.png`, `logo_C_f18.png`)
- **Bio:**
  ```
  Simple money habits that build real wealth 🌱
  📈 Investing, budgeting & retirement, made easy
  💾 Save posts you want to come back to
  Not financial advice
  ```

## Visual system (implemented in `generator/fin.ance18/brand.py`)
| Token | Value | Use |
|---|---|---|
| Background | `#F6F1E7` warm paper | every slide |
| Ink | `#16211B` | main text |
| Accent | `#1F4D3A` deep money green | big numbers, labels, swipe arrow |
| Highlighter | `#BEE8AA` mint | the key phrase, wrap it in `[brackets]` |
| Muted | `#686E64` | footnotes |

- Fonts: DM Serif Display (headlines, numbers), Source Serif 4 (body), Inter (labels). All Google Fonts, OFL licensed, bundled in `generator/fin.ance18/fonts/`.
- Size: 1080 x 1350 (4:5 portrait). JPEG only.
- Every slide: topic label top-left, `@fin.ance18` bottom-left, slide counter bottom-right on carousels. No disclaimer line on the image (it stays in the bio).
- Templates: `quote()`, `stat()`, `cover()`, `point()`, `cta()`.

## Content rules
- Every number is either computed in code (state the assumptions on the slide) or checked against an official source (IRS for limits). Limits change every year: update them each January.
- Growth examples use 7% average annual return, compounded monthly, and say "illustration only" in the caption.
- Daily mix: 8 posts, pattern Single, Carousel, Single, Single, Single, Carousel, Single, Single.
- Caption: one useful line, optional question to drive comments, follow line, 8 hashtags (max 30, max 2,200 characters).
