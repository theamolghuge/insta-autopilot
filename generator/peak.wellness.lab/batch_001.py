"""Batch 001 for @peak.wellness.lab: 4 carousels + 12 single posts (2 days of 8 slots).
Same structure as generator/fin.ance18/batch_002.py: STATS, QUOTES and CAROUSELS lists, daily pattern S C S S S C S S.
Audience: US and Europe. Food values: USDA FoodData Central. Every number claim carries its source.
Stat posts use the navy "night" version so the grid gets a dark tile now and then."""
import sys, shutil
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import brand
from brand import *

ROOT = Path(__file__).resolve().parents[2]
Q = ROOT / "content" / "peak.wellness.lab" / "queue"
TAGS = "#healthyeating #fatloss #energyfood #highprotein #healthyhabits #nutritiontips #peakwellnesslab"
FOOT = "\n\nFollow @peak.wellness.lab for one simple energy fix a day.\n.\n.\n" + TAGS + "\n"

# breakfast bowl in carousel 1, computed from USDA values
bowl_protein = 23 + 5 + 2 + 1.5      # 1 cup Greek yogurt, 1/2 cup oats, 1 tbsp chia, 1 cup raspberries
bowl_fiber = 0 + 4 + 4 + 8
assert round(bowl_protein) in range(30, 33) and bowl_fiber == 16

# ------------------------------------------------------------------ content
CAROUSELS = [
  dict(slug="energy-breakfast", k="The formula", title="The [energy breakfast] formula",
       sub="Protein + fiber + slow carbs keeps you full until lunch.",
       cap="The breakfast that keeps your energy steady until lunch. 📌 Save this for your weekly meal prep.",
       pts=[("01", "[Protein]: 25 to 35g", "3 eggs, a cup of Greek yogurt or cottage cheese. Protein is what keeps you full."),
            ("02", "[Fiber]: 8g or more", "Berries, chia seeds, spinach. Fiber slows digestion so your energy lasts."),
            ("03", "[Slow carbs]: about a fist", "Oats, whole-grain toast or a corn tortilla. Not a pastry."),
            ("EX", "Example: [Greek yogurt bowl]", f"1 cup Greek yogurt, 1 cup raspberries, 1 tbsp chia, 1/2 cup oats. About {round(bowl_protein)}g protein and {bowl_fiber}g fiber.")]),
  dict(slug="energy-myths", k="Myth vs fact", title="4 myths [draining your energy]",
       sub="What the research actually says.",
       cap="4 energy myths, and what the studies found. Which one surprised you? 👇\nSources: Paluch et al., Lancet Public Health 2022 · Vispute et al., J Strength Cond Res 2011 · Al Khatib et al., Eur J Clin Nutr 2017 · Drake et al., J Clin Sleep Med 2013.",
       pts=[("01", "Under 10,000 steps [still counts.]", "Benefits rise with every 1,000 steps and level off at about 6,000 to 10,000, depending on age."),
            ("02", "Crunches don't [burn belly fat.]", "6 weeks of ab training didn't reduce belly fat. Fat loss doesn't happen in one spot."),
            ("03", "Sleep [drives cravings.]", "After short sleep, people ate about 385 more calories the next day."),
            ("04", "Late coffee [steals sleep.]", "Caffeine 6 hours before bed cut sleep by more than an hour.")]),
  dict(slug="desk-snacks", k="Snack list", title="5 desk snacks with [10g+ protein]",
       sub="No kitchen needed. They hold you until dinner.",
       cap="Desk snacks that actually beat the 4 PM slump. 📌 Save this for your next grocery run.\nValues: USDA FoodData Central.",
       pts=[("18g", "1 cup [edamame]", "Shelled and steamed. Plenty of fiber too."),
            ("15g", "A [Greek yogurt] cup", "Plain, 5.3 oz. Add berries for sweetness."),
            ("13g", "2 [hard-boiled eggs]", "Make a batch on Sunday for the whole week."),
            ("12g", "1/2 cup [cottage cheese]", "Sweet with fruit or savory with black pepper."),
            ("14g", "Milk + [1 oz almonds]", "A cup of milk and a small handful of nuts.")]),
  dict(slug="smart-swaps", k="Swap this", title="4 swaps that [keep you full longer]",
       sub="Same foods you like, small changes.",
       cap="Small swaps, big difference by 4 PM. Which one will you try this week?\nValues: USDA FoodData Central (typical, not one brand).",
       pts=[("01", "Swap juice for [a whole orange]", "About 21g sugar and almost no fiber, vs 12g sugar and 3g fiber."),
            ("02", "Swap a bagel for [eggs on toast]", "About 12g protein, vs about 26g with 3 eggs on 2 slices of whole-grain toast."),
            ("03", "Swap fruit yogurt for [Greek yogurt]", "Fruit yogurt: about 22g sugar, 6g protein. Plain Greek yogurt with berries: about 9g sugar, 15g protein."),
            ("04", "Swap chips for [popcorn]", "3 cups of air-popped popcorn is about 90 calories with 3.5g fiber.")]),
]

STATS = [  # (number, text, note, caption)
  ("25g", "of fiber a day is the target. Most adults get about [15g.]", "WHO guideline (2023): at least 25g of fiber a day for adults.",
   "Fiber keeps you full and your energy steady. Easy way there: berries, beans and oats. 🛒"),
  ("385", "extra calories eaten, on average, the day after [short sleep.]", "Al Khatib et al., Eur J Clin Nutr, 2017 (meta-analysis).",
   "Bad sleep doesn't just make you tired. It makes you hungrier. Protect your sleep and cravings get easier."),
  ("7+", "hours of sleep a night is what adults need for [steady energy.]", "Watson et al., Sleep, 2015 (AASM and Sleep Research Society).",
   "If you're under 7 hours most nights, start there before changing anything else. 🌙"),
  ("2-5", "minutes of light walking after a meal [lowered blood sugar] vs sitting.", "Buffey et al., Sports Medicine, 2022.",
   "The easiest energy habit: walk after you eat. Even a few minutes helps. Ten is better. 🚶"),
]

QUOTES = [  # (text, kicker)
  ("Your 3 PM crash usually [starts at lunch.]", "Energy"),
  ("Protein at breakfast is [the easiest energy upgrade.]", "Nutrition"),
  ("You're not lazy. [You're under-fueled.]", "Energy"),
  ("Eat the fruit. [Skip the juice.]", "Nutrition"),
  ("Sleep is the cheapest [fat-loss tool] you have.", "Sleep"),
  ("Build every meal around [a protein first.]", "Fat loss"),
  ("Consistency beats [the perfect diet.]", "Habits"),
  ("Water first. [Coffee second.]", "Energy"),
]
QUOTE_CAPS = [
  "A lunch that's mostly fast carbs digests quickly, and the dip hits mid-afternoon. Add protein and fiber to the same plate.",
  "Eggs, Greek yogurt or cottage cheese turn a light breakfast into one that lasts until lunch.",
  "Coffee-only mornings and tiny lunches leave nothing in the tank by 4 PM. Fix the plate before the routine.",
  "A whole orange has about 12g sugar and 3g fiber. A cup of juice has about 21g sugar and almost none.",
  "Short sleep makes you hungrier the next day. Seven hours does more than most diets.",
  "Pick the protein first, then add vegetables and carbs around it. You'll be full on less.",
  "The plan you can keep for a year beats the one you quit in a week.",
  "Start the day with a big glass of water before the coffee. Easy win.",
]

# ------------------------------------------------------------------ render
START = 1   # set from `python scripts/next_number.py peak.wellness.lab`; re-running rebuilds the same folders


def make_item(n, slug):
    d = Q / f"{n:04d}-{slug}"
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    return d


def render_carousel(c, d, seed):
    brand.theme(dark=False)
    pts = c["pts"]; total = len(pts) + 2
    cover(c["title"], c["sub"], str(d / "01.jpg"), c["k"], seed=seed)
    for i, (num, head, body) in enumerate(pts, 2):
        point(num, head, body, str(d / f"{i:02d}.jpg"), c["k"], f"{i}/{total}", seed=seed + i)
    cta(str(d / f"{total:02d}.jpg"), c["k"], f"{total}/{total}")
    (d / "caption.txt").write_text(c["cap"] + FOOT)


def main():
    singles = []
    for num, txt, note, cap in STATS:
        singles.append(("stat", (num, txt, note), cap))
    for (txt, k), cap in zip(QUOTES, QUOTE_CAPS):
        singles.append(("quote", (txt, k), cap))
    stats = [s for s in singles if s[0] == "stat"]; quotes = [s for s in singles if s[0] == "quote"]
    mixed = []
    while stats or quotes:
        for _ in range(2):
            if quotes: mixed.append(quotes.pop(0))
        if stats: mixed.append(stats.pop(0))
    # daily pattern for 8 slots: S C S S S C S S
    car = list(CAROUSELS)
    n = START
    seed = 100
    while mixed or car:
        for kind in "SCSSSCSS":
            if kind == "C" and car:
                c = car.pop(0)
                render_carousel(c, make_item(n, "carousel-" + c["slug"]), seed)
            elif kind == "S" and mixed:
                typ, args, cap = mixed.pop(0)
                if typ == "stat":
                    num, txt, note = args
                    brand.theme(dark=True)
                    d = make_item(n, "stat-" + num.strip("+$%").replace(",", "").replace(".", "-").lower())
                    stat(num, txt, str(d / "01.jpg"), note=note, seed=seed)
                else:
                    txt, k = args
                    brand.theme(dark=False)
                    d = make_item(n, "quote")
                    quote(txt, str(d / "01.jpg"), kicker=k, seed=seed)
                (d / "caption.txt").write_text(cap + FOOT)
            else:
                continue
            n += 1; seed += 10
    print("queue now ends at", n - 1)


if __name__ == "__main__":
    main()
