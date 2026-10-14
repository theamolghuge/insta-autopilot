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
Plain black slides with normal text: white text centred in the middle, `@fin.ance18` small and grey at the bottom centre.
No typography styling: one font (Inter Regular), one size per slide (auto-fitted). No bold, no display
or serif fonts, no big numbers, no highlighter box, no topic label, rules, page numbers or swipe arrow.
Important words: wrap them in `[brackets]` and they are drawn in mint `#BEE8AA` (one phrase per slide is plenty).
The number on stat and point slides is mint too. Only source notes on stat posts are smaller and grey.

| Token | Value |
|---|---|
| Background | `#000000` black |
| Text | `#F5F5F2` |
| Important words, numbers | `#BEE8AA` mint |
| Handle, source notes | `#8C8C88` |

- Size: 1080 x 1350 (4:5 portrait). JPEG only.
- Handle position: `HANDLE_POS` in `brand.py` (`"center"`, `"left"` or `"right"`).
- Templates (unchanged names): `quote()`, `stat()`, `cover()`, `point()`, `cta()`. Each argument becomes its own
  centred paragraph. `kicker`/`page` are accepted but not drawn; `[brackets]` colour the important words.

## Content rules
- Every number is either computed in code (state the assumptions on the slide) or checked against an official source (IRS for limits). Limits change every year: update them each January.
- Growth examples use 7% average annual return, compounded monthly, and say "illustration only" in the caption.
- Daily mix: 8 posts, pattern Single, Carousel, Single, Single, Single, Carousel, Single, Single.
- Caption: one useful line, optional question to drive comments, follow line, 8 hashtags (max 30, max 2,200 characters).
