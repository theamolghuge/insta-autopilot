"""Batch 002 for @peak.wellness.lab: 17 carousels + 50 single posts (8 days of 8 slots + 3).
Same structure as batch_001.py: STATS, QUOTES and CAROUSELS lists, daily pattern S C S S S C S S.
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
FOOD = {  # name: (protein g, fiber g, kcal)
  "chicken_breast_roasted": (31.0, 0, 165),
  "lentils_boiled":         (9.02, 7.9, 116),
  "chickpeas_boiled":       (8.86, 7.6, 164),
  "black_beans_boiled":     (8.86, 8.7, 132),
  "white_beans_boiled":     (9.73, 6.3, 139),
  "salmon_farmed_cooked":   (22.1, 0, 206),
  "egg_whole":              (12.56, 0, 143),
  "greek_yogurt_nonfat":    (10.19, 0, 59),
  "cottage_cheese_2pct":    (10.45, 0, 81),
  "feta":                   (14.21, 0, 264),
  "edamame_prepared":       (11.91, 5.2, 121),
  "shrimp_cooked":          (22.78, 0, 99),
  "quinoa_cooked":          (4.4, 2.8, 120),
  "rice_white_cooked":      (2.69, 0.4, 130),
  "spaghetti_cooked":       (5.8, 1.8, 158),
  "pumpkin_canned":         (1.1, 2.9, 34),
  "acorn_squash_baked":     (1.12, 4.4, 56),
  "pear":                   (0.36, 3.1, 57),
  "apple":                  (0.26, 2.4, 52),
  "peanut_butter":          (25.09, 6.0, 588),
  "pumpkin_seeds":          (30.23, 6.0, 559),
  "mozzarella_part_skim":   (24.26, 0, 254),
  "hummus":                 (7.9, 6.0, 166),
  "baby_carrots":           (0.64, 2.9, 35),
  "sour_cream":             (2.44, 0, 198),
}
G = {  # portion weights in grams (USDA portion lists)
  "cup_lentils": 198, "cup_chickpeas": 164, "cup_black_beans": 172, "cup_white_beans": 179,
  "cup_greek_yogurt": 227, "half_cup_cottage": 113, "oz": 28.35, "4oz": 113.4, "3oz": 85.05,
  "egg": 50, "cup_edamame": 155, "cup_quinoa": 185, "cup_rice": 158, "cup_spaghetti": 140,
  "cup_pumpkin": 245, "cup_acorn": 205, "pear": 178, "apple": 182, "tbsp_pb": 16,
  "2tbsp_hummus": 30, "10_baby_carrots": 100, "quarter_cup_sour_cream": 57.5,
}


def n(food, grams, i=0):
    return FOOD[food][i] * grams / 100

P = lambda f, g: n(f, g, 0)
F = lambda f, g: n(f, g, 1)
K = lambda f, g: n(f, g, 2)
r = lambda x: int(round(x))

# lunch formula, 4 ways
lunch_mex = P("chicken_breast_roasted", G["3oz"]) + P("black_beans_boiled", G["cup_black_beans"] / 2)
lunch_med = P("chickpeas_boiled", G["cup_chickpeas"]) + P("greek_yogurt_nonfat", G["cup_greek_yogurt"] / 2) + P("feta", G["oz"])
lunch_ind = P("lentils_boiled", G["cup_lentils"]) + P("greek_yogurt_nonfat", G["cup_greek_yogurt"] / 2)
lunch_jpn = P("salmon_farmed_cooked", G["4oz"]) + P("edamame_prepared", G["cup_edamame"] / 2)
# 10-minute dinner, 4 ways
din_ita = P("shrimp_cooked", G["4oz"]) + P("white_beans_boiled", G["cup_white_beans"] / 2)
din_mex = 3 * P("egg_whole", G["egg"]) + P("black_beans_boiled", G["cup_black_beans"] / 2)
din_med = P("salmon_farmed_cooked", G["4oz"]) + P("quinoa_cooked", G["cup_quinoa"])
din_ind = P("chicken_breast_roasted", G["4oz"]) + P("rice_white_cooked", G["cup_rice"] / 2)
# 30g protein without meat
nm_yog = P("greek_yogurt_nonfat", G["cup_greek_yogurt"]) + P("pumpkin_seeds", G["oz"])
nm_egg = 3 * P("egg_whole", G["egg"]) + P("cottage_cheese_2pct", G["half_cup_cottage"])
nm_bean = P("black_beans_boiled", G["cup_black_beans"]) + 2 * P("egg_whole", G["egg"])
# fall fiber
fib_pumpkin = F("pumpkin_canned", G["cup_pumpkin"])
fib_acorn = F("acorn_squash_baked", G["cup_acorn"])
fib_pear = F("pear", G["pear"])
fib_lentil_half = F("lentils_boiled", G["cup_lentils"] / 2)
# snacks under 200 calories
sn_apple_pb = K("apple", G["apple"]) + K("peanut_butter", G["tbsp_pb"])
sn_seeds_k, sn_seeds_p = K("pumpkin_seeds", G["oz"]), P("pumpkin_seeds", G["oz"])
sn_pear_mozz = K("pear", G["pear"]) + K("mozzarella_part_skim", G["oz"])
sn_pear_mozz_p = P("mozzarella_part_skim", G["oz"])
sn_carrot_hummus = K("baby_carrots", G["10_baby_carrots"]) + K("hummus", G["2tbsp_hummus"])
# swaps
rice_f, rice_p = F("rice_white_cooked", G["cup_rice"]), P("rice_white_cooked", G["cup_rice"])
quin_f, quin_p = F("quinoa_cooked", G["cup_quinoa"]), P("quinoa_cooked", G["cup_quinoa"])
sc_k, sc_p = K("sour_cream", G["quarter_cup_sour_cream"]), P("sour_cream", G["quarter_cup_sour_cream"])
gy_k, gy_p = K("greek_yogurt_nonfat", G["cup_greek_yogurt"] / 4), P("greek_yogurt_nonfat", G["cup_greek_yogurt"] / 4)
pasta_p, pasta_f = P("spaghetti_cooked", G["cup_spaghetti"]), F("spaghetti_cooked", G["cup_spaghetti"])
mix_p = P("spaghetti_cooked", G["cup_spaghetti"] / 2) + P("lentils_boiled", G["cup_lentils"] / 2)
mix_f = F("spaghetti_cooked", G["cup_spaghetti"] / 2) + F("lentils_boiled", G["cup_lentils"] / 2)
# plant protein
pl_lentil = (P("lentils_boiled", G["cup_lentils"]), F("lentils_boiled", G["cup_lentils"]))
pl_black = (P("black_beans_boiled", G["cup_black_beans"]), F("black_beans_boiled", G["cup_black_beans"]))
pl_chick = (P("chickpeas_boiled", G["cup_chickpeas"]), F("chickpeas_boiled", G["cup_chickpeas"]))
pl_seeds = P("pumpkin_seeds", G["oz"])

# sanity checks on the computed numbers
assert 28 <= lunch_mex <= 40 and 28 <= lunch_med <= 34 and 28 <= lunch_ind <= 32 and 30 <= lunch_jpn <= 38
assert all(x < 200 for x in (sn_apple_pb, sn_seeds_k, sn_pear_mozz, sn_carrot_hummus))
assert all(x >= 5 for x in (fib_pumpkin, fib_acorn, fib_pear, fib_lentil_half))
assert all(x >= 26 for x in (nm_yog, nm_egg, nm_bean))
STEPS_PER_MIN = 100     # Tudor-Locke et al., Br J Sports Med, 2018: ~100 steps/min = moderate walking
walk10 = 10 * STEPS_PER_MIN

# ------------------------------------------------------------------ content
CAROUSELS = [
  dict(slug="lunch-4-ways", k="Meal formula", title="One [high-protein lunch], four ways",
       sub="Protein + beans or grains + vegetables + a sauce you like.",
       cap="Same formula, four cuisines, about 30g of protein each. Pick your favorite for this week. 📌 Save it.\nValues: USDA FoodData Central.",
       pts=[("01", "Bored of the [same chicken salad?]", "Keep the formula, change the flavors. A palm of protein, a fist of beans or grains, half a plate of vegetables, a spoon of sauce."),
            ("MX", "[Mexican] burrito bowl", f"3 oz chicken, 1/2 cup black beans, peppers, salsa, lime. About {r(lunch_mex)}g protein."),
            ("GR", "[Mediterranean] chickpea plate", f"1 cup chickpeas, 1/2 cup Greek yogurt sauce, 1 oz feta, cucumber and tomato. About {r(lunch_med)}g protein."),
            ("IN", "[Indian] dal with raita", f"1 cup lentil dal, 1/2 cup Greek yogurt raita, spinach on the side. About {r(lunch_ind)}g protein."),
            ("JP", "[Japanese] salmon bowl", f"4 oz salmon, 1/2 cup edamame, cucumber, a little rice and sesame. About {r(lunch_jpn)}g protein.")]),
  dict(slug="fall-fiber", k="Fall food", title="4 fall foods with [5g+ fiber]",
       sub="Fiber keeps you full and your energy steady.",
       cap="Fall has some of the most filling food of the year. Which one is on your list this week? 🍂\nValues: USDA FoodData Central.",
       pts=[("01", "Fall food is [built to fill you up.]", "Squash, pears and pumpkin are cheap right now and loaded with fiber. Here's how much."),
            (f"{r(fib_acorn)}g", "1 cup baked [acorn squash]", "Roast it in cubes with olive oil and salt. Great next to chicken or eggs."),
            (f"{r(fib_lentil_half)}g", "1/2 cup [lentils]", "Add them to a fall soup. They bring protein too."),
            (f"{r(fib_pumpkin)}g", "1 cup canned [pumpkin]", "Plain pumpkin, not pie filling. Stir it into oatmeal or chili."),
            (f"{fib_pear:.1f}g", "1 medium [pear]", "Eat the skin. That's where a lot of the fiber is.")]),
  dict(slug="wind-down", k="Sleep", title="A 5-step [wind-down] for better sleep",
       sub="Better sleep tonight means steadier energy tomorrow.",
       cap="Good sleep starts about an hour before bed. Try this routine for one week and see how your mornings feel. 🌙",
       pts=[("01", "Tired all day, [wired at night?]", "Your evening is probably too bright and too busy. Here is a simple routine to fix it."),
            ("02", "Pick a [fixed wake time]", "Same time every day, weekends too. Your bedtime will follow."),
            ("03", "[Dim the lights] an hour before", "Lamps instead of ceiling lights. Your body reads light as daytime."),
            ("04", "Phone [charges outside] the bedroom", "Use a cheap alarm clock. No scrolling in bed."),
            ("05", "Keep the room [cool and dark]", "A cool room and blackout curtains make it easier to stay asleep.")]),
  dict(slug="3000-steps", k="Steps", title=f"Add [{3 * walk10:,} steps] without a workout",
       sub="Three short walks fit into any busy day.",
       cap=f"At a brisk pace you take about {STEPS_PER_MIN} steps a minute, so 10 minutes is about {walk10:,} steps. Three of these and you're done. Tag a walking buddy 👟\nSource: Tudor-Locke et al., Br J Sports Med, 2018.",
       pts=[("01", "No time to exercise? [Walk in pieces.]", f"A brisk 10 minutes is about {walk10:,} steps. You only need three."),
            ("02", "Walk [after lunch]", f"10 minutes outside before you sit back down. About {walk10:,} steps."),
            ("03", "Make [one call a walk]", "Phone calls without a screen share are walking calls now."),
            ("04", "Take [the long way]", "Park at the far end, get off one stop early, use the stairs. It adds up fast.")]),
  dict(slug="myths-2", k="Myth vs fact", title="4 myths that [keep you tired]",
       sub="What the research actually says.",
       cap="4 common beliefs, checked against the studies. Which one did you believe? 👇\nSources: Depner et al., Current Biology 2019 · Li et al., J Food Compos Anal 2017 · Armstrong et al., J Nutr 2012.",
       pts=[("01", "Some of these [sound like good advice.]", "They're repeated everywhere. The studies tell a different story."),
            ("02", "Weekend sleep-ins [don't undo the week.]", "In a lab study, catching up on weekends didn't reverse the effects of short sleep. People still snacked more after dinner."),
            ("03", "Frozen vegetables [are just as good.]", "Frozen produce had similar vitamin levels to fresh, and sometimes more than fresh stored for days."),
            ("04", "Mild thirst [can feel like fatigue.]", "In young women, losing just over 1% of body weight in water lowered mood and raised fatigue."),
            ("05", "Fat loss doesn't need [constant hunger.]", "Protein and fiber at every meal keep you full on fewer calories. You shouldn't feel starving.")]),
  dict(slug="smart-swaps-2", k="Swap this", title="3 swaps for [more protein and fiber]",
       sub="Same meals, better numbers.",
       cap="Tiny changes to dinners you already make. Which swap are you trying first?\nValues: USDA FoodData Central.",
       pts=[("01", "You don't need [a new menu.]", "Keep your favorite meals and change one ingredient."),
            ("02", "White rice for [quinoa]", f"Per cooked cup: rice about {r(rice_p)}g protein and {rice_f:.1f}g fiber. Quinoa about {r(quin_p)}g protein and {r(quin_f)}g fiber."),
            ("03", "Sour cream for [Greek yogurt]", f"Per 1/4 cup: sour cream about {r(sc_k)} calories and {sc_p:.1f}g protein. Nonfat Greek yogurt about {r(gy_k)} calories and {r(gy_p)}g protein."),
            ("04", "Half the pasta for [lentils]", f"One cup of pasta: about {r(pasta_p)}g protein, {r(pasta_f)}g fiber. Half pasta, half lentils: about {r(mix_p)}g protein, {r(mix_f)}g fiber.")]),
  dict(slug="habits-stick", k="Habits", title="How to make a habit [actually stick]",
       sub="Less willpower, more planning.",
       cap="Habits stick when they're small and planned, not when you're motivated. Save this for your next Monday reset. 📌\nSource on if-then plans: Gollwitzer & Sheeran, Adv Exp Soc Psychol, 2006.",
       pts=[("01", "Motivation [runs out by Wednesday.]", "A plan doesn't. Four ways to make a new habit run on autopilot."),
            ("02", "Use an [if-then plan]", "\"If I pour my coffee, then I fill my water bottle.\" Tie it to something you already do."),
            ("03", "Make it [almost too small]", "One walk around the block. One vegetable at dinner. Grow it later."),
            ("04", "Set it up [the night before]", "Shoes by the door, oats in the bowl. Remove the first decision."),
            ("05", "Never [miss twice]", "One missed day is normal. Two in a row is a new habit. Get back the next day.")]),
  dict(slug="3pm-crash", k="Energy dips", title="Why you crash at [3 PM]",
       sub="And the simple fix for each cause.",
       cap="The afternoon slump usually has a cause you can fix. Which one is yours? Comment below 👇",
       pts=[("01", "It's not just [your age.]", "Most afternoon crashes come from four things you can change today."),
            ("02", "Lunch was [mostly fast carbs]", "Add a palm of protein and some vegetables to the same lunch."),
            ("03", "You've [barely had water]", "Coffee all morning, no water. Keep a bottle on your desk."),
            ("04", "You've [sat since 9 AM]", "Stand up and walk for 5 minutes every hour or so."),
            ("05", "You [slept badly]", "Then the crash is a sleep problem. Protect tonight's bedtime.")]),
  dict(slug="dinner-4-ways", k="Meal formula", title="The [10-minute dinner], four ways",
       sub="Quick protein + a carb + something green.",
       cap="Four fast dinners for busy weeknights, about 25 to 37g of protein each. Which cuisine is your go-to? 📌\nValues: USDA FoodData Central.",
       pts=[("01", "Too tired to cook? [Use one formula.]", "Quick protein, a ready carb, a handful of greens. One pan, 10 minutes."),
            ("IT", "[Italian] shrimp and white beans", f"4 oz shrimp, 1/2 cup white beans, garlic, tomatoes, spinach. About {r(din_ita)}g protein."),
            ("MX", "[Mexican] egg and bean tacos", f"3 scrambled eggs, 1/2 cup black beans, salsa, corn tortillas. About {r(din_mex)}g protein."),
            ("GR", "[Greek] salmon and quinoa", f"4 oz salmon, 1 cup quinoa, cucumber, lemon. About {r(din_med)}g protein."),
            ("IN", "[Indian-style] chicken and spinach", f"4 oz chicken with spices, wilted spinach, 1/2 cup rice. About {r(din_ind)}g protein.")]),
  dict(slug="protein-no-meat", k="Protein", title="3 ways to [30g of protein], no meat",
       sub="Easy breakfasts and lunches without chicken.",
       cap="Hitting your protein doesn't need a chicken breast at every meal. Save these for busy mornings. 📌\nValues: USDA FoodData Central.",
       pts=[("01", "Tired of [chicken every day?]", "These hit about 30g of protein with eggs, dairy and beans."),
            (f"{r(nm_yog)}g", "Greek yogurt + [pumpkin seeds]", "1 cup plain nonfat Greek yogurt and 1 oz pumpkin seeds. Add fruit."),
            (f"{r(nm_egg)}g", "Eggs + [cottage cheese]", "3 eggs scrambled with 1/2 cup cottage cheese. Very creamy."),
            (f"{r(nm_bean)}g", "Black beans + [2 eggs]", "1 cup black beans and 2 fried eggs with salsa. Lots of fiber too.")]),
  dict(slug="meal-prep-hour", k="Meal prep", title="One hour on Sunday, [five easy lunches]",
       sub="Cook parts, not recipes. Mix them all week.",
       cap="Prep parts, then mix them into different lunches all week. Save this for Sunday. 📌",
       pts=[("01", "Weekday lunches [decide your afternoons.]", "One hour on Sunday means you're not grabbing whatever's closest at noon."),
            ("02", "A tray of [protein]", "Chicken thighs, salmon or tofu on one sheet pan. 25 minutes in the oven."),
            ("03", "A pot of [grains or beans]", "Quinoa, rice or lentils. Cook once, use all week."),
            ("04", "Two trays of [vegetables]", "Broccoli, peppers, squash. Roast them while the protein cooks."),
            ("05", "One [good sauce]", "Yogurt-herb, peanut-lime or salsa. The sauce is what keeps it from getting boring.")]),
  dict(slug="snacks-under-200", k="Snack list", title="4 snacks under [200 calories]",
       sub="Filling, quick and easy to pack.",
       cap="Snacks that actually hold you to dinner. Which one are you packing tomorrow?\nValues: USDA FoodData Central.",
       pts=[("01", "A good snack [keeps you out of the cookie jar.]", "These are under 200 calories and have protein or fiber."),
            (f"{r(sn_apple_pb)} cal", "Apple + [1 tbsp peanut butter]", "A medium apple and a level tablespoon. Sweet, crunchy, filling."),
            (f"{r(sn_seeds_k)} cal", "1 oz [pumpkin seeds]", f"About {r(sn_seeds_p)}g protein in a small handful. Perfect for fall."),
            (f"{r(sn_pear_mozz)} cal", "Pear + [mozzarella stick]", f"A medium pear and 1 oz part-skim mozzarella. About {r(sn_pear_mozz_p)}g protein."),
            (f"{r(sn_carrot_hummus)} cal", "Baby carrots + [hummus]", "10 baby carrots and 2 tbsp hummus. Crunchy, light, ready in seconds.")]),
  dict(slug="fat-loss-plate", k="Fat loss", title="The [fat-loss plate] in 4 parts",
       sub="No counting. Just build the plate.",
       cap="Use this at home, at work and in restaurants. No app needed. Share it with someone who hates counting calories.",
       pts=[("01", "Hate counting calories? [Build the plate.]", "Four parts. Works for breakfast, lunch and dinner."),
            ("02", "Half: [vegetables]", "Anything green, red or orange. Raw, roasted or in a soup."),
            ("03", "A quarter: [protein]", "Fish, chicken, eggs, tofu, Greek yogurt or beans."),
            ("04", "A quarter: [slow carbs]", "Potatoes, rice, oats, bread or fruit. Yes, carbs stay."),
            ("05", "A thumb of [fat]", "Olive oil, nuts, avocado or cheese. Flavor matters.")]),
  dict(slug="morning-energy", k="Morning", title="A morning routine for [all-day energy]",
       sub="Four steps, about 15 minutes.",
       cap="Small things in the first hour set up the whole day. Which one will you start tomorrow? ☀️",
       pts=[("01", "Your energy is [decided before 9 AM.]", "Four small steps that set up the rest of your day."),
            ("02", "A [big glass of water]", "Before the coffee. You haven't had any for eight hours."),
            ("03", "[Daylight] in the first hour", "Step outside or sit by a window for a few minutes."),
            ("04", "[Protein] at breakfast", "Eggs, Greek yogurt or cottage cheese. It carries you to lunch."),
            ("05", "[Move] before you sit", "A short walk or a few minutes of stretching before the desk.")]),
  dict(slug="plant-protein", k="Protein", title="Plant protein [for beginners]",
       sub="Cheap, filling and easy to cook.",
       cap="Beans and lentils are protein and fiber at the same time. Save this for your next grocery run. 🛒\nValues: USDA FoodData Central (cooked).",
       pts=[("01", "Plants can [carry real protein.]", "Per cooked cup, these are some of the best you can buy."),
            (f"{r(pl_lentil[0])}g", "1 cup [lentils]", f"Plus about {r(pl_lentil[1])}g fiber. Ready in 20 minutes, no soaking."),
            (f"{r(pl_black[0])}g", "1 cup [black beans]", f"Plus about {r(pl_black[1])}g fiber. Great in bowls and tacos."),
            (f"{r(pl_chick[0])}g", "1 cup [chickpeas]", f"Plus about {r(pl_chick[1])}g fiber. Roast them or add them to salads."),
            (f"{r(pl_seeds)}g", "1 oz [pumpkin seeds]", "Sprinkle them on soup, oats or salad for extra protein.")]),
  dict(slug="soup-season", k="Fall food", title="4 soups that [actually fill you up]",
       sub="Protein and fiber in every bowl.",
       cap="Soup season is here. Make a big pot on Sunday and you have lunches for days. Which one first? 🍲",
       pts=[("01", "Soup can be [a full meal.]", "If it has protein and fiber, it holds you for hours. These four do."),
            ("02", "[Lentil] and vegetable", "Red or brown lentils, carrots, tomatoes, cumin. Thick and filling."),
            ("03", "Chicken and [white bean]", "Shredded chicken, cannellini beans, kale, garlic, lemon."),
            ("04", "[Black bean] soup", "Black beans, peppers, onion, lime. Top with Greek yogurt."),
            ("05", "Minestrone [with chickpeas]", "Classic vegetables, a little pasta and a can of chickpeas.")]),
  dict(slug="eating-out", k="Eating out", title="Eat out [without losing progress]",
       sub="Enjoy the meal and still feel good after.",
       cap="One meal out won't undo your week. These habits make it easy. Send this to the friend you eat out with.",
       pts=[("01", "Restaurants [aren't the problem.]", "A few habits make almost any menu work for you."),
            ("02", "Order [protein first]", "Pick the fish, chicken, steak or beans, then choose the sides."),
            ("03", "Ask for [an extra vegetable]", "Swap one side for salad or vegetables. Most places say yes."),
            ("04", "[Sauce on the side]", "You still get the flavor and you decide how much."),
            ("05", "[Water between] drinks", "One glass of water for every drink. You'll feel better tomorrow.")]),
]

STATS = [  # (number, text, note, caption)
  ("66", "days, on average, for a new habit to [feel automatic.]", "Lally et al., Eur J Soc Psychol, 2010. Median; range 18 to 254 days.",
   "Not 21 days. Give a new habit two months before you judge it.\nSource: Lally et al., European Journal of Social Psychology, 2010."),
  ("500", "more calories a day, on average, on an [ultra-processed diet.]", "Hall et al., Cell Metabolism, 2019. Vs an unprocessed diet.",
   "Same people, same offered calories, about 500 more eaten a day on ultra-processed food. Cook a bit more this week. 🍳\nSource: Hall et al., Cell Metabolism, 2019."),
  ("55%", "less fat lost when dieters slept [5.5 hours instead of 8.5.]", "Nedeltcheva et al., Ann Intern Med, 2010.",
   "Same diet, less sleep, less fat lost. Your bedtime is part of the plan. 🌙\nSource: Nedeltcheva et al., Annals of Internal Medicine, 2010."),
  ("441", "fewer calories a day, without trying, when protein made up [30% of calories.]", "Weigle et al., Am J Clin Nutr, 2005.",
   "More protein made people less hungry, so they ate less without counting.\nSource: Weigle et al., American Journal of Clinical Nutrition, 2005."),
  ("10%", "of US adults eat [enough vegetables.]", "Lee et al., CDC MMWR, 2022 (2019 survey data).",
   "Only about 1 in 10. One extra serving a day already puts you ahead. 🥦\nSource: Lee et al., CDC Morbidity and Mortality Weekly Report, 2022."),
  ("35%", "of US adults sleep [less than 7 hours] a night.", "Liu et al., CDC MMWR, 2016.",
   "More than 1 in 3. If that's you, fixing sleep may do more for your energy than any food.\nSource: Liu et al., CDC Morbidity and Mortality Weekly Report, 2016."),
  ("20%", "fewer calories at lunch when people [started with soup.]", "Flood & Rolls, Appetite, 2007.",
   "A bowl of vegetable soup first, and the whole meal got smaller. Good timing for soup season. 🍲\nSource: Flood & Rolls, Appetite, 2007."),
  ("15%", "fewer calories at lunch after [eating an apple first.]", "Flood-Obbagy & Rolls, Appetite, 2009.",
   "A whole apple before lunch filled people up. Apple season makes it easy. 🍎\nSource: Flood-Obbagy & Rolls, Appetite, 2009."),
  ("10", "minutes of walking stairs beat 50 mg of caffeine for [feeling energized.]", "Randolph & O'Connor, Physiology & Behavior, 2017.",
   "Next slump, try the stairs before the coffee.\nSource: Randolph & O'Connor, Physiology & Behavior, 2017 (sleep-deprived young women)."),
  ("2x", "the weight loss for people who kept [daily food records.]", "Hollis et al., Am J Prev Med, 2008. Vs those who kept none.",
   "Writing it down works, even on paper. Try it for one week. 📝\nSource: Hollis et al., American Journal of Preventive Medicine, 2008."),
  ("2", "hours of extra energy after a [10-minute brisk walk.]", "Thayer, J Pers Soc Psychol, 1987. Up to 2 hours; vs a sugary snack.",
   "In this study, a short walk raised energy for up to two hours. The sugary snack didn't last.\nSource: Thayer, Journal of Personality and Social Psychology, 1987."),
  ("15", "minutes of brisk walking cut desk chocolate snacking [about in half.]", "Oh & Taylor, Appetite, 2012.",
   "Craving at your desk? Walk first, decide after.\nSource: Oh & Taylor, Appetite, 2012."),
  ("150", "minutes a week of moderate movement is the [adult minimum.]", "Physical Activity Guidelines for Americans, 2nd ed., HHS, 2018.",
   "That's about 22 minutes a day. Brisk walking counts. 🚶\nSource: Physical Activity Guidelines for Americans, 2nd edition, 2018."),
  ("65%", "less fatigue after 6 weeks of [easy, low-intensity exercise.]", "Puetz, Flowers & O'Connor, Psychother Psychosom, 2008.",
   "Tired people felt less tired after gentle exercise three times a week. Easy counts.\nSource: Puetz, Flowers & O'Connor, Psychotherapy and Psychosomatics, 2008."),
  ("25%", "more muscle building over a day when protein was [spread across meals.]", "Mamerow et al., J Nutr, 2014. About 30g per meal vs mostly at dinner.",
   "Most people eat little protein at breakfast and lots at dinner. Even it out.\nSource: Mamerow et al., Journal of Nutrition, 2014."),
  ("44%", "more weight lost by dieters who drank [2 cups of water] before meals.", "Dennis et al., Obesity, 2010. 500 ml before each meal, 12 weeks.",
   "An easy habit: a big glass of water before you eat. 💧\nSource: Dennis et al., Obesity, 2010."),
  ("8,000", "steps a day: linked to about half the risk of early death [vs 4,000.]", "Saint-Maurice et al., JAMA, 2020.",
   "You don't need 10,000. Getting from 4,000 to 8,000 is where a lot of the benefit is.\nSource: Saint-Maurice et al., JAMA, 2020."),
]

QUOTES = [  # (text, kicker)
  ("Decide dinner [before you're hungry.]", "Habits"),
  ("Tired is not the same as [hungry.]", "Energy"),
  ("Half your plate [should crunch.]", "Fat loss"),
  ("Your future self eats [what you prep today.]", "Habits"),
  ("A short walk is the best [afternoon coffee.]", "Movement"),
  ("You don't need motivation. [You need a default.]", "Habits"),
  ("Beans count as [protein and fiber.]", "Nutrition"),
  ("Eat slowly. Your fullness [needs time] to catch up.", "Fat loss"),
  ("The best diet is the one [you'd eat on a Tuesday.]", "Habits"),
  ("Don't skip lunch to [save room] for dinner.", "Fat loss"),
  ("Your energy follows [your bedtime.]", "Sleep"),
  ("Two good meals beat [one perfect day.]", "Habits"),
  ("Move every hour. [Your 3 PM self] will thank you.", "Energy"),
  ("Fiber is the [quiet hero] of fat loss.", "Fiber"),
  ("Pack lunch [like you mean it.]", "Habits"),
  ("If it's on the counter, [you'll eat it.]", "Habits"),
  ("A late, heavy dinner is [tomorrow's tired morning.]", "Sleep"),
  ("Progress hides in [the boring days.]", "Habits"),
  ("Pick one habit. [Not ten.]", "Habits"),
  ("Add good food before you [take anything away.]", "Nutrition"),
  ("Steps are the [easiest win] of your day.", "Movement"),
  ("A good breakfast starts [the night before.]", "Habits"),
  ("Coffee is not [breakfast.]", "Energy"),
  ("Eat the apple first. [Then decide] on the cookie.", "Fat loss"),
  ("You can't out-eat [a bad night's sleep.]", "Sleep"),
  ("Comfort food can be [high in protein] too.", "Nutrition"),
  ("Darker evenings are a cue for [an earlier bedtime.]", "Sleep"),
  ("Hunger is information, [not an emergency.]", "Fat loss"),
  ("Stairs count [as exercise.]", "Movement"),
  ("A stocked fridge [beats willpower.]", "Habits"),
  ("More color on the plate, [more energy] in the day.", "Nutrition"),
  ("Start small. [Stay long.]", "Habits"),
  ("Busy is a reason to [plan,] not to skip.", "Habits"),
]
QUOTE_CAPS = [
  "Deciding at 7 PM when you're starving usually means takeout. Pick tonight's dinner at lunch.",
  "Before you reach for a snack, ask: am I hungry, or do I need water, a walk or sleep?",
  "Fill half the plate with vegetables first. You eat more food and still eat less overall.",
  "Ten minutes of prep on Sunday saves a lot of bad decisions on Wednesday. 📌 Save this as your reminder.",
  "Afternoon slump? Get outside for 10 minutes before you reach for another cup.",
  "Decide your usual breakfast and lunch once, then stop deciding. Defaults beat willpower.",
  "Lentils, chickpeas and black beans give you both in one scoop. Add a can to soups and salads.",
  "Put the fork down between bites and finish the meal in 20 minutes instead of 5.",
  "If you couldn't eat this way on a busy weekday, it's not your plan. It's a phase.",
  "Skipping lunch usually means a huge dinner and snacking all evening. Eat lunch.",
  "Late nights show up as low energy the next afternoon. Pick a bedtime and protect it.",
  "Don't wait for a perfect day to start. Make your next meal a good one.",
  "Set a reminder to stand up and walk for a few minutes every hour. Your afternoon will feel different.",
  "Beans, berries, oats and vegetables keep you full for longer. Add one more serving today.",
  "Protein, vegetables and something you look forward to. A packed lunch beats the vending machine.",
  "Put fruit on the counter and the snacks in a cupboard. Your kitchen makes a lot of choices for you.",
  "Try to finish dinner a few hours before bed and keep it lighter. Tell us how you sleep.",
  "Nobody posts their ordinary Tuesday. That's where the results come from.",
  "Ten new rules on Monday, zero by Friday. Pick one habit and give it a month.",
  "Start by adding protein, fruit and vegetables. Some of the less helpful food gets crowded out on its own.",
  "Every walk counts, even the short ones. Do you track your steps? 👇",
  "Overnight oats, eggs boiled ahead, yogurt portioned out. Morning you will be grateful.",
  "Coffee on an empty stomach until noon leaves you running on fumes. Add eggs, yogurt or oats.",
  "Something filling first makes the next choice easier. It's not a rule, just a good order.",
  "Short sleep makes almost everything harder, including food choices. Start with bedtime.",
  "Chili with beans, stews with lentils, shepherd's pie with lean meat. Fall food can keep you full.",
  "The evenings are getting darker. Use it as a cue to wind down earlier.",
  "Feeling hungry a bit before a meal is normal. Wait for the meal and make it a good one.",
  "Take the stairs whenever there's a choice. Small climbs add up over a week.",
  "Stock the fridge with ready protein and cut vegetables, and good choices become the easy ones.",
  "Red peppers, leafy greens, berries, carrots. A colorful plate is usually a filling one.",
  "The habit you can keep for years is worth more than the one you can do perfectly for a week.",
  "When your week is packed, plan two simple meals ahead. Busy weeks need a plan the most. 📌 Save this.",
]

# ------------------------------------------------------------------ render
START = 17   # set from `python scripts/next_number.py peak.wellness.lab`; re-running rebuilds the same folders


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
