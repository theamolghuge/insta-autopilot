# peak.wellness.lab: brand rules for posts

Built the same way as fin.ance18 (simple text posts on black, a weekly batch, 8 posting slots a day) but runs completely on its own:
own queue, state, token, look, content and posting times. Never reuse fin.ance18 content or styling.
Renderer: `generator/peak.wellness.lab/brand.py` (the fin.ance18 renderer with this brand's colors and fonts).
Batches: copy the latest `generator/peak.wellness.lab/batch_NNN.py` and change only the content lists and `START`.

## Look (don't change; set 2026-10-14)
- Plain black slides with normal text: white text centred in the middle, `@peak.wellness.lab` small and grey at the bottom centre.
- No typography styling: one font (DM Sans Regular), one size per slide (auto-fitted). No bold, no display
  or serif fonts, no big numbers, no highlighter box, no kicker, rules, page numbers or "Swipe".
  Important words: wrap them in `[brackets]` and they are drawn in tomato `#F2765F` (one phrase per slide is plenty).
The number on stat and point slides is tomato too. Only source notes on stat posts are smaller and grey.
- Colors: black `#000000`, text `#F5F5F2`, tomato `#F2765F` for [important words] and numbers, handle and source notes `#8C8C88`.
- `brand.theme()` still exists so old batches run, but does nothing.
- Formats: `quote` (one sentence, one [highlight]), `stat` (number line + sentence + source note), carousel = `cover` + 3-6 `point` slides + `cta`.
  Each argument becomes its own centred paragraph. All 1080 x 1350.
- Handle position: `HANDLE_POS` in `brand.py` (`"center"`, `"left"` or `"right"`).
- No "→" or emoji in on-image text.

## Who it's for
Busy adults in the **US and Europe** who want more energy and to lose fat through food and daily habits.
US English. Grams for protein/fiber/sugar; cups, tbsp and oz for portions. Western staples first
(Greek yogurt, eggs, oats, chicken, beans, lentils, berries, salmon), other cuisines for variety.

## Content filter
Every post answers yes to: does this help a busy person have more energy or lose fat through food and daily habits?
- Core (~70%): nutrition, energy, fat loss. Supporting (~30%): sleep, movement, habits.
- Off the page: supplements, medical conditions (thyroid, PCOS, diabetes, hormones, medication, weight-loss drugs),
  biohacking, mental health, skincare, heavy gym content, brand names.

## Voice
The smart friend who reads the research so you don't have to. Calm, specific, never preachy. Specific numbers over vague promises.
No exclamation marks on images. Never: clean eating, cheat meal, guilt, toxins, hack, superfood, detox, melts fat, boost metabolism, miracle.

## Facts
- Food numbers from USDA FoodData Central; compute any sums in the batch script.
- Any number claim (study, guideline) needs a real source: in the stat note, and in the caption for carousels/quotes.
  Use real, checkable papers or guidelines only. Not sure it's real? Drop the claim.

## Captions
Short why (1-3 lines), one action (save / share / comment), source line if there's a claim, then the FOOT block from the batch
(follow line + 7 hashtags incl. #peakwellnesslab). Max 2 emoji.

## Weekly mix (8 slots a day, pattern S C S S S C S S)
About 2 carousels + 6 singles a day; among singles roughly 2 quotes per stat.
Rotate: energy dips, protein, fiber, swaps, sleep, steps/walking, habits, myth vs fact, meal formulas.
