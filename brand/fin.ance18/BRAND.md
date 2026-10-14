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

## Visual system (implemented in `generator/fin.ance18/brand.py`, changed 2026-10-14)
Plain black slides: text centred in the middle, `@fin.ance18` small at the bottom centre. Nothing else on the slide
(no topic label, no rules, no page numbers, no swipe arrow, no disclaimer).

| Token | Value | Use |
|---|---|---|
| Background | `#000000` black | every slide |
| Ink | `#F5F5F2` | main text |
| Soft | `#C8C8C4` | body text on point slides |
| Accent | `#BEE8AA` mint | big numbers and the key phrase: wrap it in `[brackets]` (coloured, no highlighter box) |
| Muted | `#8C8C88` | handle, source notes |

- Fonts: DM Serif Display (headlines, numbers), Source Serif 4 (quotes, body), Inter (handle, notes). Bundled in `generator/fin.ance18/fonts/`.
- Size: 1080 x 1350 (4:5 portrait). JPEG only.
- Handle position: `HANDLE_POS` in `brand.py` (`"center"`, `"left"` or `"right"`).
- Templates (unchanged names): `quote()`, `stat()`, `cover()`, `point()`, `cta()`. `kicker`/`page` are still accepted but not drawn.

## Content rules
- Every number is either computed in code (state the assumptions on the slide) or checked against an official source (IRS for limits). Limits change every year: update them each January.
- Growth examples use 7% average annual return, compounded monthly, and say "illustration only" in the caption.
- Daily mix: 8 posts, pattern Single, Carousel, Single, Single, Single, Carousel, Single, Single.
- Caption: one useful line, optional question to drive comments, follow line, 8 hashtags (max 30, max 2,200 characters).
