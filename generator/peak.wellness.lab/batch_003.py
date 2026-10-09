"""Batch 003 for @peak.wellness.lab: 10 carousels + 28 single posts (38 posts, 4.75 days of 8 slots).
Same structure as batch_002.py: STATS, QUOTES and CAROUSELS lists, daily pattern S C S S S C S S.
Audience: US and Europe. Food values: USDA FoodData Central (SR Legacy), sums computed below.
Every number claim carries its source. Stat posts use the navy "night" version."""
import sys, shutil
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import brand
from brand import *

ROOT = Path(__file__).resolve().parents[2]
Q = ROOT / "content" / "peak.wellness.lab" / "queue"
TAGS = "#healthyeating #fatloss #energyfood #highprotein #healthyhabits #nutritiontips #peakwellnesslab"
FOOT = "\n\nFollow @peak.wellness.lab for one simple energy fix a day.\n.\n.\n" + TAGS + "\n"

# ------------------------------------------------------------------ USDA FoodData Central (SR Legacy), per 100 g
FOOD = {  # name: (protein g, fiber g, kcal)                  FDC id
  "egg_whole":              (12.56, 0, 143),   # 171287
  "feta":                   (14.21, 0, 264),   # 173420
  "black_beans_boiled":     (8.86, 8.7, 132),  # 173735
  "white_beans_boiled":     (9.73, 6.3, 139),  # 175203
  "chickpeas_boiled":       (8.86, 7.6, 164),  # 173757
  "greek_yogurt_nonfat":    (10.19, 0, 59),    # 170894
  "cottage_cheese_2pct":    (10.45, 0, 81),    # 173414
  "chicken_breast_roasted": (31.0, 0, 165),    # 171477
  "shrimp_cooked":          (22.78, 0, 99),    # 175180
  "rice_white_cooked":      (2.69, 0.4, 130),  # 168878
  "corn_tortilla":          (5.7, 6.3, 218),   # 175036
  "rye_bread":              (8.5, 5.8, 259),   # 172684
  "smoked_salmon":          (18.3, 0, 117),    # 173687
  "chickpea_flour":         (22.4, 10.8, 387), # 174288
  "ww_bread":               (12.4, 6.0, 252),  # 172688
  "tuna_light_water":       (25.5, 0, 116),    # 171986
  "chicken_thigh_roasted":  (24.8, 0, 179),    # 172388
  "tofu_firm":              (17.3, 2.3, 144),  # 172475
  "oats_dry":               (13.2, 10.1, 379), # 173904
  "raspberries":            (1.2, 6.5, 52),    # 167755
  "avocado":                (2.0, 6.7, 160),   # 171705
  "almonds":                (21.2, 12.5, 579), # 170567
  "sweet_potato_baked":     (2.01, 3.3, 90),   # 168483
  "brussels_boiled":        (2.55, 2.6, 36),   # 169971
  "beef_85_crumbles":       (27.7, 0, 256),    # 174034
  "kidney_beans_boiled":    (8.67, 7.4, 127),  # 175194
  "mashed_potato_milk_butter": (1.86, 1.5, 113),  # 168555
  "cauliflower_boiled":     (1.84, 2.3, 23),   # 170397
  "heavy_cream":            (2.84, 0, 340),    # 170859
}
G = {  # portion weights in grams (USDA portion lists)
  "egg": 50, "oz": 28.35, "3oz": 85.05, "4oz": 113.4, "5oz": 141.75, "6oz": 170.1,
  "cup_black_beans": 172, "cup_white_beans": 179, "cup_chickpeas": 164, "cup_greek_yogurt": 227,
  "half_cup_cottage": 113, "cup_rice": 158, "corn_tortilla": 26, "slice_rye": 32, "slice_ww": 32,
  "half_cup_chickpea_flour": 46, "half_cup_oats_dry": 40.5, "cup_raspberries": 123, "half_avocado": 100.5,
  "medium_sweet_potato": 114, "cup_brussels": 156, "cup_kidney_beans": 177, "cup_mashed_potato": 210,
  "cup_cauliflower": 124, "cup_heavy_cream": 238,
}


def n(food, grams, i=0):
    return FOOD[food][i] * grams / 100

P = lambda f, g: n(f, g, 0)
F = lambda f, g: n(f, g, 1)
K = lambda f, g: n(f, g, 2)
r = lambda x: int(round(x))

# protein breakfast, 4 ways
br_tr = 3 * P("egg_whole", G["egg"]) + P("feta", G["oz"])
br_mx = 2 * P("egg_whole", G["egg"]) + P("black_beans_boiled", G["cup_black_beans"] / 2) + 2 * P("corn_tortilla", G["corn_tortilla"])
br_no = 2 * P("rye_bread", G["slice_rye"]) + P("smoked_salmon", G["3oz"]) + P("egg_whole", G["egg"])
br_in = P("chickpea_flour", G["half_cup_chickpea_flour"]) + P("greek_yogurt_nonfat", G["cup_greek_yogurt"] / 2)
BR = [br_tr, br_mx, br_no, br_in]
# sheet-pan dinner, 4 ways
sp_us = P("chicken_thigh_roasted", G["5oz"]) + P("sweet_potato_baked", G["medium_sweet_potato"]) + P("brussels_boiled", G["cup_brussels"])
sp_gr = P("chicken_breast_roasted", G["4oz"]) + P("chickpeas_boiled", G["cup_chickpeas"] / 2) + P("feta", G["oz"])
sp_mx = P("shrimp_cooked", G["4oz"]) + P("black_beans_boiled", G["cup_black_beans"] / 2) + 2 * P("corn_tortilla", G["corn_tortilla"])
sp_kr = P("tofu_firm", G["6oz"]) + P("rice_white_cooked", G["cup_rice"] / 2)
SP = [sp_us, sp_gr, sp_mx, sp_kr]
# a 30g+ fiber day
fd_b = F("oats_dry", G["half_cup_oats_dry"]) + F("raspberries", G["cup_raspberries"])
fd_l = 2 * F("ww_bread", G["slice_ww"]) + F("avocado", G["half_avocado"])
fd_s = F("almonds", G["oz"])
fd_d = F("sweet_potato_baked", G["medium_sweet_potato"]) + F("brussels_boiled", G["cup_brussels"])
fd_total = fd_b + fd_l + fd_s + fd_d
# a 100g+ protein day
pd_b = 3 * P("egg_whole", G["egg"]) + P("ww_bread", G["slice_ww"])
pd_l = P("tuna_light_water", G["4oz"]) + P("white_beans_boiled", G["cup_white_beans"] / 2)
pd_s = P("cottage_cheese_2pct", G["half_cup_cottage"])
pd_d = P("chicken_thigh_roasted", G["5oz"])
pd_total = pd_b + pd_l + pd_s + pd_d
# comfort-food swaps
chili_beef_k = K("beef_85_crumbles", G["4oz"])
chili_mix_k = K("beef_85_crumbles", G["4oz"] / 2) + K("kidney_beans_boiled", G["cup_kidney_beans"] / 2)
chili_mix_f = F("kidney_beans_boiled", G["cup_kidney_beans"] / 2)
mash_k = K("mashed_potato_milk_butter", G["cup_mashed_potato"])
mash_mix_k = K("mashed_potato_milk_butter", G["cup_mashed_potato"] / 2) + K("cauliflower_boiled", G["cup_cauliflower"] / 2)
cream_k = K("heavy_cream", G["cup_heavy_cream"] / 4)
wbean_k, wbean_f = K("white_beans_boiled", G["cup_white_beans"] / 2), F("white_beans_boiled", G["cup_white_beans"] / 2)

# study numbers, computed from the published values
home_cook_gap = 2301 - 2164                 # Wolfson & Bleich 2015: kcal/day, 0-1 vs 6-7 home dinners a week
KG_TO_LB = 2.20462
ello_ff = 7.9 * KG_TO_LB                    # Ello-Martin et al. 2007: reduced fat + more fruit and vegetables, kg lost in 1 year
ello_rf = 6.4 * KG_TO_LB                    # reduced fat only
prot_lo, prot_hi = 1.2 * 68, 1.6 * 68       # DGA 2025-2030: 1.2-1.6 g/kg; a 150 lb (68 kg) adult

# sanity checks on the computed numbers
assert all(20 <= x <= 30 for x in BR), BR
assert all(28 <= x <= 50 for x in SP), SP
assert fd_total >= 30 and pd_total >= 100
assert chili_mix_k < chili_beef_k and mash_mix_k < mash_k and wbean_k < cream_k
assert home_cook_gap == 137 and r(ello_ff) == 17 and r(ello_rf) == 14

# ------------------------------------------------------------------ content
CAROUSELS = [
  dict(slug="breakfast-4-ways", k="Meal formula", title="The [protein breakfast], four ways",
       sub="Protein + a slow carb + something fresh.",
       cap=f"Same formula, four countries, about {r(min(BR))} to {r(max(BR))}g of protein each. Which one are you making this weekend? 📌 Save it.\nValues: USDA FoodData Central.",
       pts=[("01", "Same eggs [every morning?]", "Keep the formula: protein first, a slow carb, something fresh. Just change the country."),
            ("TR", "[Turkish] menemen", f"3 eggs scrambled with tomatoes, peppers and 1 oz feta. About {r(br_tr)}g protein."),
            ("MX", "[Mexican] huevos rancheros", f"2 eggs, 1/2 cup black beans, 2 corn tortillas, salsa. About {r(br_mx)}g protein."),
            ("NO", "[Nordic] rye and salmon", f"2 slices rye bread, 3 oz smoked salmon, 1 boiled egg, cucumber. About {r(br_no)}g protein."),
            ("IN", "[Indian] besan chilla", f"Chickpea-flour pancakes (1/2 cup flour) with spinach and 1/2 cup Greek yogurt. About {r(br_in)}g protein.")]),
  dict(slug="comfort-swaps", k="Swap this", title="3 swaps for [lighter comfort food]",
       sub="Same cozy dinners, more fiber or fewer calories.",
       cap="Keep your fall favorites and change one ingredient in each. Which one are you trying first? 👇\nValues: USDA FoodData Central.",
       pts=[("01", "Comfort food season [doesn't need a pause.]", "Keep the dishes you love. Change one ingredient in each."),
            ("02", "Chili: half the beef [for beans]", f"4 oz cooked beef: about {r(chili_beef_k)} calories, no fiber. 2 oz beef + 1/2 cup kidney beans: about {r(chili_mix_k)} calories and {r(chili_mix_f)}g fiber."),
            ("03", "Mash: half the potato [for cauliflower]", f"1 cup mashed potatoes: about {r(mash_k)} calories. Half potato, half cauliflower: about {r(mash_mix_k)}."),
            ("04", "Creamy soup: cream [for white beans]", f"1/4 cup heavy cream: about {r(cream_k)} calories. 1/2 cup white beans blended in: about {r(wbean_k)} calories and {r(wbean_f)}g fiber.")]),
  dict(slug="smart-nap", k="Sleep", title="How to nap [without the grogginess]",
       sub="A short nap can rescue a slow afternoon.",
       cap="A short nap beats a long one for most people. Try it on your next slow afternoon and tell us how it went. 😴\nSource: Brooks & Lack, Sleep, 2006.",
       pts=[("01", "Afternoon fog? [Nap the right way.]", "Done right, a nap clears your head. Done wrong, you wake up feeling worse."),
            ("02", "Keep it [short]", "In a sleep lab study, a 10-minute nap gave the best lift with the least grogginess. Longer naps took a while to pay off."),
            ("03", "Nap [before 3 PM]", "A late nap can make it harder to fall asleep tonight."),
            ("04", "[Set an alarm]", "Lie down, set 20 minutes and get up when it rings, even if you didn't fall asleep."),
            ("05", "Need one daily? [Check your nights.]", "Needing a nap every day usually points to short sleep. Fix bedtime first.")]),
  dict(slug="fiber-day", k="Fiber", title="A [30g+ fiber] day, mapped out",
       sub="Four normal meals. No special foods.",
       cap=f"Fiber keeps you full and your energy steady, and it adds up fast with the right basics. This day hits about {r(fd_total)}g. 📌 Save it for your next grocery list.\nValues: USDA FoodData Central.",
       pts=[("01", "Fiber sounds hard. [It's four meals.]", f"Here's a normal day that reaches about {r(fd_total)}g."),
            (f"{r(fd_b)}g", "Breakfast: [oats and raspberries]", "1/2 cup oats (dry), cooked, with 1 cup raspberries on top."),
            (f"{r(fd_l)}g", "Lunch: [avocado toast]", "2 slices whole-wheat bread, 1/2 avocado and two eggs on top for protein."),
            (f"{fd_s:.1f}g", "Snack: [1 oz almonds]", "A small handful. Comes with protein too."),
            (f"{r(fd_d)}g", "Dinner: [sweet potato and sprouts]", "1 medium baked sweet potato and 1 cup Brussels sprouts next to your protein.")]),
  dict(slug="cold-dark-walks", k="Steps", title="Keep walking when it's [cold and dark]",
       sub="Fewer daylight hours, same daily steps.",
       cap="Shorter days don't have to mean fewer steps. Which one will you try this week? Tag your walking buddy 👟",
       pts=[("01", "Shorter days, [same steps.]", "Four ways to keep moving when it's cold and dark out."),
            ("02", "Walk at [lunchtime]", "It's the brightest, warmest part of the day. Ten minutes outside counts."),
            ("03", "Dress in [layers]", "You warm up fast. Gloves and a hat make the first few minutes easy."),
            ("04", "Find an [indoor loop]", "Office stairs, a mall, a big store. Laps inside count the same."),
            ("05", "Be [easy to see]", "After dark, wear something bright or reflective and stick to lit streets.")]),
  dict(slug="myths-3", k="Myth vs fact", title="3 diet rules [you can drop]",
       sub="What the trials actually found.",
       cap="Three rules people follow for years, checked against the trials. Which one did you believe? 👇\nSources: Betts et al., Am J Clin Nutr 2014 · Cameron et al., Br J Nutr 2010 · Gardner et al., JAMA 2018.",
       pts=[("01", "Some rules [just add stress.]", "They sound smart and get repeated everywhere. The trials disagree."),
            ("02", "Breakfast doesn't change [calories burned at rest.]", "In a 6-week trial it was the same with or without breakfast. Breakfast eaters did move more in the morning."),
            ("03", "Six small meals [aren't better than three.]", "On the same calories for 8 weeks, eating 3 or 6 times a day led to the same weight loss."),
            ("04", "Low-carb vs low-fat: [about a tie.]", "In a year-long trial of 609 adults eating mostly whole foods, both groups lost similar weight."),
            ("05", "What matters: [the plan you keep.]", "Pick the eating pattern you can follow on a normal week.")]),
  dict(slug="protein-day", k="Protein", title="What [100g+ of protein] looks like",
       sub="Four normal meals. Real food only.",
       cap=f"Spread across the day, about {r(pd_total)}g of protein is just four ordinary meals. Save this for your next meal plan. 📌\nValues: USDA FoodData Central.",
       pts=[("01", "100g sounds hard. [Spread it out.]", "Put real protein in every meal and one snack. It adds up fast."),
            (f"{r(pd_b)}g", "Breakfast: [3 eggs on toast]", "3 eggs and 1 slice of whole-wheat toast."),
            (f"{r(pd_l)}g", "Lunch: [tuna and white beans]", "4 oz tuna (drained), 1/2 cup white beans, lemon and greens."),
            (f"{r(pd_s)}g", "Snack: [cottage cheese]", "1/2 cup cottage cheese with fruit."),
            (f"{r(pd_d)}g", "Dinner: [chicken thighs]", "5 oz roasted chicken thighs with vegetables and rice.")]),
  dict(slug="restart", k="Habits", title="How to restart [after an off week]",
       sub="No reset Monday needed.",
       cap="Everyone has off weeks. The fix is small and starts with your next meal. Send this to someone who needs it.",
       pts=[("01", "Off track? [Skip the big reset.]", "You don't need a fresh Monday. You need a normal next meal."),
            ("02", "Make [the next meal] normal", "Protein, vegetables and a carb you like. No making up for anything."),
            ("03", "Restock [three basics]", "Eggs, frozen vegetables and a bag of salad. Easy wins at home."),
            ("04", "Bring back [one habit]", "The walk, the packed lunch or the bedtime. Just one this week."),
            ("05", "Ignore [the scale] for a few days", "Salty or late meals add water weight that drops on its own.")]),
  dict(slug="halloween-candy", k="Fall treats", title="Halloween candy, [on your terms]",
       sub="Enjoy it on purpose, not by the handful.",
       cap="Halloween candy is already in every store. You don't need to avoid it, just plan it. Which rule will you use? 🎃",
       pts=[("01", "The candy aisle is open. [Make a plan.]", "A few simple rules keep it a treat instead of a daily habit."),
            ("02", "Buy it [the week of]", "Buying three weeks early means three weeks of a full bowl at home."),
            ("03", "Have it [after a meal]", "You're already full, so one or two pieces feel like enough."),
            ("04", "Pick [your favorites]", "Skip the ones you don't love. Eat the ones you do, slowly."),
            ("05", "Portion it, [then close the bag]", "Put two or three pieces in a bowl. Eating from the bag has no end point.")]),
  dict(slug="sheet-pan-4-ways", k="Meal formula", title="One [sheet-pan dinner], four ways",
       sub="Protein + vegetables + a carb on one tray.",
       cap=f"One tray, one hot oven, about {r(min(SP))} to {r(max(SP))}g of protein each. Which cuisine is first this week? 📌\nValues: USDA FoodData Central.",
       pts=[("01", "Hate doing dishes? [Use one pan.]", "Everything on one tray, 25 to 35 minutes in a hot oven. Change the spices, not the method."),
            ("US", "[American] chicken and sweet potato", f"5 oz chicken thighs, 1 sweet potato, 1 cup Brussels sprouts, paprika. About {r(sp_us)}g protein."),
            ("GR", "[Greek] chicken and chickpeas", f"4 oz chicken breast, 1/2 cup chickpeas, peppers, red onion, oregano, 1 oz feta. About {r(sp_gr)}g protein."),
            ("MX", "[Mexican] shrimp fajitas", f"4 oz shrimp, peppers and onions, 1/2 cup black beans, 2 corn tortillas. About {r(sp_mx)}g protein."),
            ("KR", "[Korean-style] tofu and broccoli", f"6 oz firm tofu, broccoli, garlic, soy and chili, 1/2 cup rice. About {r(sp_kr)}g protein.")]),
]

STATS = [  # (number, text, note, caption)
  ("270", "fewer calories a day when short sleepers [slept about an hour more.]", "Tasali et al., JAMA Intern Med, 2022. 2-week trial; adults who slept under 6.5 hours.",
   "No diet change, just more sleep, and people ate less without trying. Protect tonight's bedtime. 🌙\nSource: Tasali et al., JAMA Internal Medicine, 2022."),
  ("30%", "more eaten at lunch when people got [the biggest portion.]", "Rolls, Morris & Roe, Am J Clin Nutr, 2002. Largest vs smallest serving of the same dish.",
   "People ate more when they were served more. Serve dinner on the plate, not family style.\nSource: Rolls, Morris & Roe, American Journal of Clinical Nutrition, 2002."),
  ("31%", "more fullness after meals with [beans, lentils or chickpeas.]", "Li et al., Obesity, 2014. Meta-analysis of 9 feeding trials.",
   "Pulses fill you up more than the same meal without them. Add a can of beans to this week's soup. 🫘\nSource: Li et al., Obesity, 2014."),
  ("92", "more calories a day lost when people [ate whole grains] instead of refined.", "Karl et al., Am J Clin Nutr, 2017. 6-week trial; more energy left in stool, slightly higher resting burn.",
   "A small daily edge from an easy swap: oats, brown rice and whole-wheat bread instead of white.\nSource: Karl et al., American Journal of Clinical Nutrition, 2017."),
  (f"{home_cook_gap}", "fewer calories a day for people who [cooked dinner at home] most nights.", "Wolfson & Bleich, Public Health Nutr, 2015. 6-7 vs 0-1 home dinners a week (US survey data).",
   "Cooking at home was linked to fewer calories and less sugar. Simple dinners count. 🍳\nSource: Wolfson & Bleich, Public Health Nutrition, 2015."),
  ("2", "days a week of [muscle-strengthening] is the adult guideline.", "Physical Activity Guidelines for Americans, 2nd ed., HHS, 2018.",
   "On top of walking. Squats, push-ups against a counter or bands at home all count. 💪\nSource: Physical Activity Guidelines for Americans, 2nd edition, 2018."),
  ("1.2-1.6", "grams of protein per kg of body weight a day: [the new US target.]", "Dietary Guidelines for Americans, 2025-2030 (USDA and HHS).",
   f"For a 150 lb (68 kg) adult, that's about {r(prot_lo)} to {r(prot_hi)}g a day. Easiest way there: protein at every meal.\nSource: Dietary Guidelines for Americans, 2025-2030."),
  ("202", "fewer calories a day when meals had [extra vegetables] blended in.", "Blatt, Roe & Rolls, Am J Clin Nutr, 2011. Pureed vegetables added to entrees.",
   "Blend spinach into pasta sauce or cauliflower into mac and cheese. More food, fewer calories.\nSource: Blatt, Roe & Rolls, American Journal of Clinical Nutrition, 2011."),
  (f"{r(ello_ff)}", "lb lost in a year when dieters cut fat [and added more produce.]", f"Ello-Martin et al., Am J Clin Nutr, 2007. Vs about {r(ello_rf)} lb on fat cuts alone; less hunger too.",
   "Adding fruit and vegetables helped people eat more food and feel less hungry while losing more. 🥕\nSource: Ello-Martin et al., American Journal of Clinical Nutrition, 2007."),
]

QUOTES = [  # (text, kicker)
  ("Your grocery list is [your real diet plan.]", "Habits"),
  ("Tired by 10 AM? [Look at your breakfast.]", "Energy"),
  ("A walk after dinner beats [a scroll after dinner.]", "Movement"),
  ("Short naps, [clear afternoons.]", "Sleep"),
  ("The scale measures weight, [not progress.]", "Fat loss"),
  ("Hungry an hour after eating? [Add protein.]", "Fat loss"),
  ("Rest days are [part of the plan.]", "Movement"),
  ("Buy the vegetables [you'll actually cook.]", "Nutrition"),
  ("Energy is built [meal by meal.]", "Energy"),
  ("Your afternoon latte might be [dessert.]", "Energy"),
  ("Build strength [twice a week.]", "Movement"),
  ("Make the healthy choice [the lazy choice.]", "Habits"),
  ("One off-plan meal is [just one meal.]", "Habits"),
  ("Snack on purpose, [not on autopilot.]", "Fat loss"),
  ("Darker days still need [daylight.]", "Energy"),
  ("Weekends count. They just [don't decide everything.]", "Habits"),
  ("Serve the food, [then put the pot away.]", "Fat loss"),
  ("Vegetables taste better [roasted.]", "Nutrition"),
  ("Cook from a [short list of favorites.]", "Habits"),
]
QUOTE_CAPS = [
  "What's in your cart is what you'll eat on a busy Wednesday. Plan the list and the week gets easier. 🛒",
  "A mid-morning crash often means breakfast was mostly fast carbs. Add eggs, Greek yogurt or cottage cheese.",
  "Ten minutes outside after dinner, phone in your pocket. Try it three nights this week.",
  "A 10 to 20 minute nap before 3 PM can reset a slow afternoon. Set an alarm so it stays short.",
  "Water, salt and timing move the number day to day. Track your waist, energy and strength too.",
  "If you're hungry again soon after a meal, the plate probably needed more protein. Start there next time.",
  "Walking every day is great. Hard workouts need recovery days so you can keep going. Plan them in.",
  "Pick vegetables you already know how to make. A simple side you'll cook beats a fancy one that wilts.",
  "One good meal won't change your energy. A week of steady meals will. Make the next one count.",
  "Big flavored coffee drinks can carry a lot of sugar. Try a smaller size or plain coffee with milk.",
  "Two short sessions a week: squats, push-ups and rows with bands or weights. Strength makes daily life easier.",
  "Washed fruit at eye level, cut vegetables ready, snacks out of sight. Make the good option the easy one.",
  "A big dinner out doesn't undo a good week. Have a normal breakfast tomorrow and move on. Share this with a friend.",
  "Decide your snack before you're hungry: fruit and yogurt, nuts, cheese and crackers. Then sit down and eat it.",
  "Mornings are getting darker. Get outside for a few minutes around lunch when the light is strongest. ☀️",
  "Enjoy the weekend. A normal Monday breakfast gets you right back on track.",
  "Plate your portion in the kitchen and leave the pot on the stove. Seconds become a real choice, not a reflex.",
  "Hot oven, olive oil, salt, 25 minutes. Broccoli, carrots and Brussels sprouts turn sweet and crispy.",
  "Seven dinners you like and can make on autopilot. Rotate them and stop deciding every night. 📌 Save this.",
]

# ------------------------------------------------------------------ render
START = 84   # set from `python scripts/next_number.py peak.wellness.lab`; re-running rebuilds the same folders


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
