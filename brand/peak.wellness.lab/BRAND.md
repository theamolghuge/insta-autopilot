# peak.wellness.lab: brand rules for posts

Built the same way as fin.ance18 (simple text posts, a weekly batch, 8 posting slots a day) but runs completely on its own:
own queue, state, token, look, content and posting times. Never reuse fin.ance18 content or styling.
Renderer: `generator/peak.wellness.lab/brand.py` (the fin.ance18 renderer with this brand's colors and fonts).
Batches: copy the latest `generator/peak.wellness.lab/batch_NNN.py` and change only the content lists and `START`.

## Look (don't change)
- Colors: plate `#FBF1EA` ground, navy `#1E2A38` text, tomato `#E5533D` for big numbers and the kicker rule,
  tomato-deep `#B23A27` for small accent text (kickers, "Swipe"), tomato-soft `#FBDCD3` highlighter behind [bracketed] words.
- Night version (navy ground, plate text) for stat posts: `brand.theme(dark=True)`; everything else stays light.
- Type: DM Serif Display for quotes, headings and numbers; DM Sans for subtitles, body text, kicker and footer.
- Formats: `quote` (one sentence, one [highlight]), `stat` (big number + sentence + source note),
  carousel = `cover` + 3-6 `point` slides + `cta`. All 1080 x 1350.
- DM Serif Display has no arrow glyph: don't use "→" or emoji in on-image text.

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
