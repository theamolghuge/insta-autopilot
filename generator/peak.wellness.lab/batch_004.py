"""Batch 004 for @peak.wellness.lab: 14 carousels + 40 single posts (54 posts, 6.75 days of 8 slots).
Same structure as batch_003.py: STATS, QUOTES and CAROUSELS lists, daily pattern S C S S S C S S.
Audience: US and Europe. Food values: USDA FoodData Central (SR Legacy), sums computed below.
Every number claim carries its source. Seasonal: clocks go back in Europe (Oct 25) and the US (Nov 1)."""
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
FOOD = {  # name: (protein g, fiber g, kcal, sugars g)        FDC id
  "tuna_light_water":    (25.51, 0, 116, 0),      # 171986
  "egg_whole":           (12.56, 0, 143, 0.37),   # 171287
  "potato_boiled":       (1.71, 1.8, 86, 0.89),   # 170440
  "green_beans_boiled":  (1.89, 3.2, 35, 3.63),   # 169141
  "chicken_breast":      (31.02, 0, 165, 0),      # 171477
  "peanuts_dry_roasted": (24.35, 8.4, 587, 4.9),  # 173806
  "black_beans_boiled":  (8.86, 8.7, 132, 0.32),  # 173735
  "turkey_93_crumbles":  (27.1, 0, 213, 0),       # 172851
  "lentils_boiled":      (9.02, 7.9, 116, 1.8),   # 172421
  "feta":                (14.21, 0, 265, 0),      # 173420
  "ww_bread":            (12.45, 6.0, 252, 4.34), # 172688
  "cottage_2pct":        (10.45, 0, 81, 4.0),     # 172182
  "baked_beans":         (4.75, 4.1, 94, 7.96),   # 175182
  "ricotta_part_skim":   (11.39, 0, 138, 0.31),   # 171248
  "hemp_hulled":         (31.56, 4.0, 553, 1.5),  # 170148
  "parmesan_grated":     (28.42, 0, 420, 0.07),   # 171247
  "egg_white":           (10.9, 0, 52, 0.71),     # 172183
  "tempeh":              (20.29, 0, 192, 0),      # 174272 (fiber not listed)
  "sardines_oil":        (24.62, 0, 208, 0),      # 175139
  "salmon_pink_canned":  (23.1, 0, 138, 0),       # 175175
  "peanut_butter":       (22.21, 5.0, 598, 10.49),# 172470
  "peas_frozen_boiled":  (5.15, 4.5, 78, 4.4),    # 170017
  "barley_cooked":       (2.26, 3.8, 123, 0.28),  # 170285
  "chia":                (16.54, 34.4, 486, 0),   # 170554
  "split_peas_boiled":   (8.34, 8.3, 118, 2.9),   # 172429
  "granola_homemade":    (13.67, 8.9, 489, 19.8), # 171646
  "oats_dry":            (13.15, 10.1, 379, 0.99),# 173904
  "croissant_butter":    (8.2, 2.6, 406, 11.26),  # 174987
  "english_muffin_ww":   (8.8, 6.7, 203, 8.09),   # 172762
  "jam":                 (0.37, 1.1, 278, 48.5),  # 169641
  "grapes":              (0.72, 0.9, 69, 15.48),  # 174683
  "raisins":             (3.3, 4.5, 299, 65.18),  # 168165
  "potato_chips":        (6.39, 3.1, 532, 0.33),  # 169677
  "choc_chip_cookie":    (5.1, 2.0, 492, 32.9),   # 172716
  "strawberries":        (0.67, 2.0, 32, 4.89),   # 167762
}
G = {  # portion weights in grams (USDA portion lists; * = scaled from a listed portion)
  "egg": 50, "oz": 28.35, "3oz": 85.05, "4oz": 113.4,
  "half_cup_potato": 78, "cup_green_beans": 125, "cup_black_beans": 172, "cup_lentils": 198,
  "slice_ww": 32, "half_cup_cottage": 113, "cup_baked_beans": 254, "half_cup_ricotta": 124,
  "3tbsp_hemp": 30, "half_cup_egg_white": 243 / 2,  # *
  "can_sardines": 92, "2tbsp_pb": 32, "tbsp_pb": 16, "tbsp_jam": 20,
  "cup_peas": 160,  # * 2 x 1/2 cup (80 g)
  "cup_barley": 157, "cup_split_peas": 196,
  "half_cup_granola": 122 / 2, "half_cup_oats": 81 / 2,  # * from 1 cup
  "croissant": 57, "english_muffin": 66,
  "cup_grapes": 151, "box_raisins": 43, "cup_strawberries": 152, "cookie": 10, "medium_potato": 167,
}


def n(food, grams, i=0):
    return FOOD[food][i] * grams / 100

P = lambda f, g: n(f, g, 0)
F = lambda f, g: n(f, g, 1)
K = lambda f, g: n(f, g, 2)
S = lambda f, g: n(f, g, 3)
r = lambda x: int(round(x))

# big salad, 4 ways (protein)
sa_fr = P("tuna_light_water", G["3oz"]) + 2 * P("egg_whole", G["egg"]) + P("potato_boiled", G["half_cup_potato"]) + P("green_beans_boiled", G["cup_green_beans"])
sa_th = P("chicken_breast", G["4oz"]) + P("peanuts_dry_roasted", G["oz"])
sa_mx = P("turkey_93_crumbles", G["3oz"]) + P("black_beans_boiled", G["cup_black_beans"] / 2)
sa_me = P("lentils_boiled", G["cup_lentils"]) + P("feta", G["oz"])
SA = [sa_fr, sa_th, sa_mx, sa_me]
# protein toast, 4 ways (2 slices whole-wheat each)
toast = 2 * P("ww_bread", G["slice_ww"])
to_us = toast + P("cottage_2pct", G["half_cup_cottage"])
to_uk = toast + P("baked_beans", G["cup_baked_beans"] / 2) + P("egg_whole", G["egg"])
to_es = toast + 2 * P("egg_whole", G["egg"])
to_it = toast + P("ricotta_part_skim", G["half_cup_ricotta"])
TO = [to_us, to_uk, to_es, to_it]
# protein add-ons
ad_hemp = P("hemp_hulled", G["3tbsp_hemp"])
ad_parm = P("parmesan_grated", G["oz"])
ad_white = P("egg_white", G["half_cup_egg_white"])
ad_tempeh = P("tempeh", G["3oz"])
# pantry protein
pa_sard = P("sardines_oil", G["can_sardines"])
pa_salm = P("salmon_pink_canned", G["3oz"])
pa_pb = P("peanut_butter", G["2tbsp_pb"])
# freezer and pantry fiber
fi_peas = F("peas_frozen_boiled", G["cup_peas"])
fi_barley = F("barley_cooked", G["cup_barley"])
fi_chia = F("chia", G["oz"])
fi_split = F("split_peas_boiled", G["cup_split_peas"])
# breakfast swaps
gr_k, gr_s = K("granola_homemade", G["half_cup_granola"]), S("granola_homemade", G["half_cup_granola"])
oa_k, oa_s = K("oats_dry", G["half_cup_oats"]), S("oats_dry", G["half_cup_oats"])
cr_k, cr_p = K("croissant_butter", G["croissant"]), P("croissant_butter", G["croissant"])
em_k = K("english_muffin_ww", G["english_muffin"]) + K("egg_whole", G["egg"])
em_p = P("english_muffin_ww", G["english_muffin"]) + P("egg_whole", G["egg"])
jam_p = P("jam", G["tbsp_jam"])
pb1_p = P("peanut_butter", G["tbsp_pb"])
# same calories, more food
rai_k = K("raisins", G["box_raisins"])
grape_cups = rai_k / FOOD["grapes"][2] * 100 / G["cup_grapes"]
chip_k = K("potato_chips", G["oz"])
pot_g = chip_k / FOOD["potato_boiled"][2] * 100
pot_med = pot_g / G["medium_potato"]
cook_k = 2 * K("choc_chip_cookie", G["cookie"])
straw_cups = cook_k / FOOD["strawberries"][2] * 100 / G["cup_strawberries"]

# guideline and study numbers, computed from the published values
sugar_g = 2000 * 0.10 / 4            # WHO: free sugars under 10% of energy; 2,000 kcal day, 4 kcal per g
produce_portions = 400 / 80          # WHO: at least 400 g of fruit and vegetables; 80 g portions
chew_pct = 11.9                      # Li et al. 2011: 11.9% less eaten after 40 vs 15 chews

# sanity checks on the computed numbers
assert all(20 <= x <= 45 for x in SA), SA
assert all(18 <= x <= 24 for x in TO), TO
assert min(fi_peas, fi_barley, fi_chia, fi_split) >= 5.9
assert oa_k < gr_k and em_p > 2 * cr_p and pb1_p > jam_p
assert 1.1 <= grape_cups <= 1.4 and 0.9 <= pot_med <= 1.2 and 1.8 <= straw_cups <= 2.2
assert sugar_g == 50 and produce_portions == 5 and r(chew_pct) == 12

# ------------------------------------------------------------------ content
CAROUSELS = [
  dict(slug="big-salad-4-ways", k="Meal formula", title="One [big salad], four ways",
       sub="Greens + real protein + something hearty + a sharp dressing.",
       cap=f"A salad only holds you to dinner when it has real protein. These have about {r(min(SA))} to {r(max(SA))}g each. Which one is lunch tomorrow? 📌 Save it.\nValues: USDA FoodData Central.",
       pts=[("01", "Salad leaves you hungry? [Build it bigger.]", "Start with greens, then add a real protein, something hearty and a dressing with a kick."),
            ("FR", "[French] salade niçoise", f"3 oz tuna, 2 boiled eggs, 1/2 cup potatoes, 1 cup green beans, olives, mustard dressing. About {r(sa_fr)}g protein."),
            ("TH", "[Thai-style] chicken and peanut", f"4 oz chicken breast, shredded cabbage, carrots, herbs, 1 oz peanuts, lime and chili. About {r(sa_th)}g protein."),
            ("MX", "[Mexican] taco salad", f"3 oz lean ground turkey, 1/2 cup black beans, lettuce, tomato, salsa. About {r(sa_mx)}g protein."),
            ("ME", "[Middle Eastern] lentil salad", f"1 cup lentils, cucumber, tomato, parsley, lemon, 1 oz feta. About {r(sa_me)}g protein.")]),
  dict(slug="protein-add-ons", k="Protein", title="4 easy [protein add-ons]",
       sub="Keep your usual meals. Add one thing.",
       cap="No new recipes, just one extra ingredient in meals you already eat. Which one are you adding this week? 👇\nValues: USDA FoodData Central.",
       pts=[("01", "Low on protein? [Add, don't replace.]", "One add-on turns a light meal into a filling one."),
            (f"{r(ad_white)}g", "1/2 cup [egg whites]", "Whisk them into your usual scrambled eggs or oatmeal while it cooks."),
            (f"{r(ad_tempeh)}g", "3 oz [tempeh]", "Cube it and pan-fry it for stir-fries, bowls and salads."),
            (f"{r(ad_hemp)}g", "3 tbsp [hemp seeds]", "Sprinkle them on yogurt, oats or salad. Nutty and soft."),
            (f"{r(ad_parm)}g", "1 oz grated [parmesan]", "On soup, pasta or roasted vegetables. A lot of flavor too.")]),
  dict(slug="same-calories-more-food", k="Fat loss", title="Same calories, [more food]",
       sub="Pick foods with more water and fiber, and the plate gets bigger.",
       cap="Fat loss feels easier when the portion is big. Same calories, much more on the plate. Save this for your next snack run. 📌\nValues: USDA FoodData Central.",
       pts=[("01", "Small portions [leave you hungry.]", "Foods full of water and fiber give you more to eat for the same calories."),
            ("02", f"A box of raisins or [{grape_cups:.1f} cups of grapes]", f"A small 1.5 oz box of raisins is about {r(rai_k)} calories. That's the same as about {grape_cups:.1f} cups of grapes."),
            ("03", "1 oz of chips or [a whole potato]", f"1 oz of potato chips is about {r(chip_k)} calories, about the same as {r(pot_g)}g of boiled potato. That's a medium potato."),
            ("04", f"2 cookies or [{r(straw_cups)} cups of strawberries]", f"Two medium chocolate chip cookies are about {r(cook_k)} calories. So are about {r(straw_cups)} cups of strawberries."),
            ("05", "You don't have to [give up the treat.]", "Just know which foods fill you up, and lean on them most days.")]),
  dict(slug="wfh-steps", k="Steps", title="Working from home? [Walk on purpose.]",
       sub="No commute means fewer steps. Add them back.",
       cap="Working from home can quietly cut your daily steps. These four put them back without a workout. Which one are you starting tomorrow? 👟",
       pts=[("01", "No commute, [no steps?]", "At home, the walk to the train is gone. You have to put movement back on purpose."),
            ("02", "Take a [fake commute]", "Ten minutes outside before work and ten after. It also marks the end of the workday."),
            ("03", "Use a [small water glass]", "You'll refill it more often. Every trip to the kitchen counts."),
            ("04", "Do [one lap] between meetings", "Around the block or around the house. Two minutes is enough."),
            ("05", "Turn chores into [movement breaks]", "Laundry, dishes or a quick tidy between tasks. It all counts as movement.")]),
  dict(slug="breakfast-swaps", k="Swap this", title="3 breakfast swaps that [last until lunch]",
       sub="Same morning, steadier energy.",
       cap="Breakfast should carry you to lunch. These swaps add protein or cut sugar without making mornings harder. Which one are you trying first?\nValues: USDA FoodData Central.",
       pts=[("01", "Hungry by 10 AM? [Swap one thing.]", "Keep your routine and change the food in it."),
            ("02", "Granola for [plain oats]", f"Per 1/2 cup: granola about {r(gr_k)} calories and {r(gr_s)}g sugar. Plain oats about {r(oa_k)} calories and under 1g sugar. Add fruit yourself."),
            ("03", "A croissant for [an English muffin and egg]", f"A croissant: about {r(cr_k)} calories and {r(cr_p)}g protein. A whole-wheat English muffin with an egg: about {r(em_k)} calories and {r(em_p)}g protein."),
            ("04", "Jam for [peanut butter]", f"Per tablespoon on toast: jam has almost no protein. Peanut butter has about {r(pb1_p)}g, so the toast lasts longer.")]),
  dict(slug="evening-snacking", k="Habits", title="Snacking every evening? [Start earlier.]",
       sub="Night snacking usually starts with the day before it.",
       cap="Evening snacking is rarely about willpower. It's usually a light day of eating catching up with you. Send this to someone who raids the kitchen at 9 PM. 🌙",
       pts=[("01", "The 9 PM kitchen trip [starts at lunch.]", "Under-eating during the day makes the evening much harder."),
            ("02", "Eat a [real dinner]", "Protein, vegetables and a carb. A small salad at 7 PM means snacks at 9."),
            ("03", "Plan [one evening snack]", "If you like something after dinner, pick it ahead of time and enjoy it at the table."),
            ("04", "Close [the kitchen]", "Lights off, dishes done, teeth brushed. A clear end to eating for the day."),
            ("05", "Tired? [Go to bed.]", "Late-night hunger is often just tiredness. Sleep is the better fix.")]),
  dict(slug="fiber-pantry", k="Fiber", title="4 freezer and pantry foods [packed with fiber]",
       sub="Cheap, easy to store, ready when you are.",
       cap="Fiber keeps you full and your energy steady, and you can keep these in the house all month. Which one is going on your list? 🛒\nValues: USDA FoodData Central.",
       pts=[("01", "No fresh food left? [You still have fiber.]", "These keep for weeks and add fiber to any meal."),
            (f"{r(fi_split)}g", "1 cup cooked [split peas]", "Simmer them into a thick soup. No soaking needed."),
            (f"{r(fi_chia)}g", "1 oz [chia seeds]", "Stir them into yogurt or oats. They thicken it as they sit."),
            (f"{r(fi_peas)}g", "1 cup frozen [green peas]", "Into pasta, rice, soup or eggs. Cooked in three minutes."),
            (f"{r(fi_barley)}g", "1 cup cooked [barley]", "Chewy and filling. Use it in soups or instead of rice.")]),
  dict(slug="clocks-go-back", k="Sleep", title="The clocks go back. [Here's how to adjust.]",
       sub="Europe: Sunday, Oct 25. US: Sunday, Nov 1.",
       cap="One extra hour in bed sounds great, until your sleep and appetite feel off all week. Keep your mornings steady and you'll adjust in a few days. Share this with someone who hates the time change. 🕰️",
       pts=[("01", "An extra hour [can still throw you off.]", "Your body clock doesn't change on Sunday just because the clocks do."),
            ("02", "Keep [your wake time]", "Get up at your usual time by the new clock, even on Sunday. Your bedtime will follow."),
            ("03", "Get [morning light]", "Step outside or sit by a window soon after you wake up. It helps reset your clock."),
            ("04", "Eat at [your usual times]", "Breakfast, lunch and dinner on the new clock from day one."),
            ("05", "Dark by 5 PM? [Move your walk.]", "Lunchtime is now the best daylight of the day. Use it.")]),
  dict(slug="toast-4-ways", k="Meal formula", title="[Protein toast], four ways",
       sub="2 slices whole-wheat + a protein topping + something fresh.",
       cap=f"Toast can be a real meal. With the right topping, each of these has about {r(min(TO))} to {r(max(TO))}g of protein. Which country are you trying? 📌\nValues: USDA FoodData Central.",
       pts=[("01", "Toast for lunch? [Top it with protein.]", "Same formula every time: two slices of whole-wheat bread, a protein, something fresh."),
            ("US", "[American] cottage cheese toast", f"1/2 cup cottage cheese, sliced tomato, black pepper. About {r(to_us)}g protein."),
            ("UK", "[British] beans on toast", f"1/2 cup baked beans and a fried egg on top. About {r(to_uk)}g protein."),
            ("ES", "[Spanish] tomato toast with eggs", f"Grated tomato, olive oil and 2 eggs. About {r(to_es)}g protein."),
            ("IT", "[Italian] ricotta toast", f"1/2 cup part-skim ricotta, spinach and lemon zest. About {r(to_it)}g protein.")]),
  dict(slug="myths-4", k="Myth vs fact", title="3 food fears [you can let go of]",
       sub="What the research actually found.",
       cap="Three foods people avoid for no good reason. Which one did you cut out? 👇\nSources: Bertoia et al., PLoS Medicine 2015 · Flores-Mateo et al., Am J Clin Nutr 2013 · Killer, Blannin & Jeukendrup, PLoS ONE 2014.",
       pts=[("01", "Some foods get [a bad name.]", "These three are easy to fit into a fat-loss week."),
            ("02", "Fruit [isn't the problem.]", "In 3 large US studies, each extra daily serving of fruit was linked to about half a pound less weight gain over 4 years. Berries did especially well."),
            ("03", "Nuts [don't add weight on their own.]", "In a review of controlled trials, diets with added nuts didn't raise body weight or waist size."),
            ("04", "Coffee [doesn't dehydrate you.]", "In a study of regular coffee drinkers, four cups a day hydrated about as well as the same amount of water."),
            ("05", "What matters: [the whole diet.]", "Enjoy these foods in normal portions as part of regular meals.")]),
  dict(slug="workday-energy", k="Energy dips", title="An [energy-friendly] workday",
       sub="Small changes from 9 to 5.",
       cap="Your workday shapes your energy more than any single meal. Pick one of these for tomorrow. Save this for Monday. 📌",
       pts=[("01", "Drained by 4 PM? [Look at your workday.]", "How you eat and move at work decides how you feel at night."),
            ("02", "Eat lunch [away from the screen]", "Ten minutes at a table. You'll notice you're full."),
            ("03", "Get [daylight] before 2 PM", "A window seat, a walk outside or a coffee by the door."),
            ("04", "Have a [planned 4 PM snack]", "Fruit and yogurt, or cheese and an apple. Then dinner won't feel urgent."),
            ("05", "Have your [last coffee] after lunch", "Caffeine late in the day can cost you sleep, and tomorrow's energy.")]),
  dict(slug="pantry-protein", k="Protein", title="Protein [from the pantry]",
       sub="For nights when the fridge is empty.",
       cap="Keep a few cans and jars in the cupboard and dinner is always ten minutes away. Save it for your next grocery run. 🛒\nValues: USDA FoodData Central.",
       pts=[("01", "Fridge empty? [Check the cupboard.]", "These keep for months and have real protein."),
            (f"{r(pa_sard)}g", "1 can of [sardines]", "On whole-wheat toast with lemon, or tossed through pasta."),
            (f"{r(pa_salm)}g", "3 oz canned [salmon]", "Mix with a little Greek yogurt and herbs for quick salmon salad."),
            (f"{r(pa_pb)}g", "2 tbsp [peanut butter]", "Stir into a quick peanut noodle sauce or spread on toast.")]),
  dict(slug="track-progress", k="Habits", title="Track progress [without obsessing]",
       sub="Four simple signals beyond the scale.",
       cap="The scale is one number on one day. These four give you a fuller picture and keep you going. Which one will you start tracking? 👇",
       pts=[("01", "The scale [doesn't tell the whole story.]", "Use a few simple signals and look at them over weeks."),
            ("02", "Rate your [energy] every evening", "A quick 1 to 10 score in your notes app. Watch the weekly average."),
            ("03", "Measure [your waist] once a week", "Same day, same time, same spot. It shows fat loss the scale can hide."),
            ("04", "Check your [weekly step average]", "Most phones count steps already. Aim to nudge the average up."),
            ("05", "Look at [the trend], not the day", "Compare this month with last month. Single days are noise.")]),
  dict(slug="travel-days", k="Energy", title="Travel days without [the energy crash]",
       sub="Airports, road trips and long days on the move.",
       cap="Travel days are long, and the food on the way is rarely great. A little planning keeps your energy up. Tag the person you travel with. ✈️",
       pts=[("01", "Long day on the move? [Plan the food.]", "Airport and gas station food is the default. Bring a better one."),
            ("02", "Pack [protein and fiber]", "Nuts, fruit, cheese, a sandwich on whole-wheat bread. Enough for one meal."),
            ("03", "Bring an [empty water bottle]", "Fill it after security or at every stop. Thirst can feel like tiredness."),
            ("04", "Walk [whenever you can]", "Walk the terminal or take a lap at the rest stop. Sitting all day drains you."),
            ("05", "Keep bedtime [close to normal]", "Arriving late? Have a light meal and get to bed as soon as you can.")]),
]

STATS = [  # (number, text, note, caption)
  ("24%", "more hunger after two nights of [4 hours in bed.]", "Spiegel et al., Ann Intern Med, 2004. Vs 10 hours in bed; healthy young men.",
   "Short nights make you hungrier the next day, especially for sweets and starchy snacks. Bedtime is part of the plan. 🌙\nSource: Spiegel et al., Annals of Internal Medicine, 2004."),
  ("323%", "fullness score for boiled potatoes, the highest of [38 common foods.]", "Holt et al., Eur J Clin Nutr, 1995. Satiety index; white bread = 100%.",
   "Boiled potatoes were the most filling food tested, ahead of fish, oats and fruit. Potatoes aren't the problem, the fryer is. 🥔\nSource: Holt et al., European Journal of Clinical Nutrition, 1995."),
  (f"{r(chew_pct)}%", "less eaten at a meal when people chewed each bite [40 times instead of 15.]", f"Li et al., Am J Clin Nutr, 2011. {chew_pct}% less food; young men.",
   "Slower bites, smaller meal, no extra effort. Try putting your fork down between bites tonight.\nSource: Li et al., American Journal of Clinical Nutrition, 2011."),
  ("400", "mg of caffeine a day is the limit [for most healthy adults.]", "FDA, Spilling the Beans, 2024. About 2 to 3 twelve-ounce cups of coffee. EFSA also uses 400 mg.",
   "Coffee is fine. Five big mugs a day and a late afternoon latte might be what's costing you sleep. ☕\nSource: FDA, Spilling the Beans: How Much Caffeine is Too Much?, 2024."),
  ("36%", "more pizza eaten [while watching TV] than without it.", "Blass et al., Physiol Behav, 2006. 71% more mac and cheese.",
   "Eating in front of a screen made people eat more without noticing. Try one screen-free dinner this week. 📺\nSource: Blass et al., Physiology & Behavior, 2006."),
  ("92%", "of restaurant meals had more calories [than one meal needs.]", "Urban et al., J Acad Nutr Diet, 2016. 364 meals from chain and local restaurants.",
   "Eating out is fine. The portion is usually too big for one meal. Box half before you start.\nSource: Urban et al., Journal of the Academy of Nutrition and Dietetics, 2016."),
  ("46", "more minutes of sleep a night for office workers [with windows.]", "Boubekri et al., J Clin Sleep Med, 2014. Vs workplaces without windows.",
   "Daylight during the day helps sleep at night. Take your coffee or calls by a window, or step outside at lunch. ☀️\nSource: Boubekri et al., Journal of Clinical Sleep Medicine, 2014."),
  (f"{r(sugar_g)}g", "of free sugars a day is the WHO limit [on a 2,000-calorie diet.]", "WHO healthy diet guidance: free sugars under 10% of daily energy.",
   "That includes sugar in drinks, sweets, honey and juice, not the sugar in whole fruit or milk. One can of soda covers a big part of it.\nSource: World Health Organization, Healthy diet fact sheet."),
  ("10", "minutes faster to fall asleep after [a warm shower or bath] 1 to 2 hours before bed.", "Haghayegh et al., Sleep Med Rev, 2019. Meta-analysis; warm water, 104-109 °F.",
   "A warm shower in the evening helps your body cool down in time for sleep. Water around 104-109 °F (40-42.5 °C) works best. 🚿\nSource: Haghayegh et al., Sleep Medicine Reviews, 2019."),
  ("450", "calories a day from soda: people [didn't eat less] to make up for it.", "DiMeglio & Mattes, Int J Obes, 2000. Same calories as jelly beans were offset.",
   "Your body barely notices calories you drink. Water, sparkling water or plain coffee and tea are the easy swap.\nSource: DiMeglio & Mattes, International Journal of Obesity, 2000."),
  ("400g", f"of fruit and vegetables a day is the WHO minimum: [{r(produce_portions)} portions.]", "WHO healthy diet guidance. A portion is about 80g.",
   "A handful of berries, a side salad, an apple, a cup of soup vegetables and some peas at dinner. That's five. 🥦\nSource: World Health Organization, Healthy diet fact sheet."),
  ("2-2.5", "liters of water a day from drinks and food: [the EFSA target] for women and men.", "EFSA, Dietary Reference Values for water, 2010.",
   "Food gives you some of it, drinks give you the rest. Keep a bottle where you can see it. 💧\nSource: European Food Safety Authority, Dietary Reference Values for water, 2010."),
]

QUOTES = [  # (text, kicker)
  ("Walk while you [wait for the kettle.]", "Movement"),
  ("Potatoes aren't the problem. [The fryer is.]", "Nutrition"),
  ("A screen at dinner makes [the plate disappear.]", "Habits"),
  ("Every walk counts, [even the short ones.]", "Movement"),
  ("Light in the morning, [sleep at night.]", "Sleep"),
  ("Fruit is the original [grab-and-go snack.]", "Nutrition"),
  ("Eat the vegetables first, [while you're hungriest.]", "Fat loss"),
  ("Done is better than [a perfect meal plan.]", "Habits"),
  ("Canned beans are [the fastest protein] in your kitchen.", "Nutrition"),
  ("Cook once, [eat twice.]", "Habits"),
  ("Energy dips are a signal, [not a character flaw.]", "Energy"),
  ("Restaurant portions are [a suggestion.]", "Fat loss"),
  ("Strong legs make [every walk easier.]", "Movement"),
  ("Boring meals [are allowed.]", "Habits"),
  ("Your last coffee [sets your bedtime.]", "Sleep"),
  ("Liquid calories [don't fill you up.]", "Fat loss"),
  ("The clocks change. [Your wake time doesn't.]", "Sleep"),
  ("Shop the season, [not the trend.]", "Nutrition"),
  ("Most tiredness has [a boring fix.]", "Energy"),
  ("Sit down to eat, [even for a snack.]", "Habits"),
  ("Bedtime is a plan, [not a mood.]", "Sleep"),
  ("Darker evenings? [Brighter lunches.]", "Energy"),
  ("Chew more, [rush less.]", "Fat loss"),
  ("The first bite is for taste. [The tenth is habit.]", "Fat loss"),
  ("Travel days still need [a real breakfast.]", "Habits"),
  ("Your 4 PM snack is [dinner insurance.]", "Fat loss"),
  ("Feeling flat? [Go outside for ten minutes.]", "Energy"),
  ("A warm shower is part of [the wind-down.]", "Sleep"),
]
QUOTE_CAPS = [
  "Kettle on, coffee brewing, microwave running: that's a few minutes of walking you didn't plan. Small moves add up over a day.",
  "Boiled, baked or roasted, potatoes are filling and cheap. Deep-fried and salted is a different food. 🥔",
  "When your eyes are on a screen, you stop noticing how much you've eaten. One screen-free meal a day is a good start.",
  "Five minutes around the block still counts. You don't need a long walk for it to be worth it.",
  "Morning daylight helps set your body clock, so you feel sleepy at the right time at night. Step outside after breakfast.",
  "An apple, a banana, a handful of grapes. No prep, no packaging, real fiber. Keep a bowl where you can see it. 🍎",
  "Start the meal with the salad or the vegetables. You eat more of them when you're hungry, and less of the rest.",
  "A rough plan you follow beats a perfect one you never start. Write three dinners down for this week and go.",
  "Open, rinse, done. A can of chickpeas or black beans adds protein and fiber to a salad, soup or wrap in seconds.",
  "Make double dinner and you have tomorrow's lunch. Fewer decisions, better food. 📌 Save this.",
  "Feeling flat is information: short sleep, a light lunch, too little water or too much sitting. Find the cause and fix that.",
  "Restaurant plates are built to look generous. Eat until you're satisfied and take the rest home.",
  "Squats, lunges and step-ups twice a week make stairs, hills and long walks feel easier. 💪",
  "The same breakfast every day is fine. Repeating meals you like makes healthy eating easier, not worse.",
  "Caffeine can stay in your system for hours. If sleep is rough, move your last coffee to just after lunch. ☕",
  "Soda, juice and sweet coffee drinks add calories without making you less hungry. Drink water, eat your calories.",
  "When the clocks go back, get up at your usual time on the new clock. Your body adjusts faster that way. Europe: Oct 25. US: Nov 1. 🕰️",
  "Apples, pears, squash and cabbage are at their best right now. Buy what's in season and fill the basket.",
  "Low energy usually comes down to sleep, food, water and movement. Not exciting, but very fixable.",
  "Eating standing up or on the go is easy to forget. Sit down, use a plate and you'll notice what you ate.",
  "Pick a bedtime and set an alarm 30 minutes before it to start winding down. Treat it like an appointment. 🌙",
  "Evenings are dark now, so get your daylight at midday. A walk at lunch does more for your energy than a later one.",
  "Slowing down gives your body time to notice you're full. Put the fork down between bites. Share this with a fast eater.",
  "The first bites of a treat taste the best. After that it's mostly autopilot. Enjoy a few and stop there.",
  "Long travel day? Eat a proper breakfast with protein before you leave. The airport options can be a snack, not the meal.",
  "A planned snack at 4 PM means you get to dinner hungry, not starving. Fruit and yogurt or cheese and crackers.",
  "Ten minutes outside, no phone if you can manage it. Fresh air and daylight often beat a second coffee.",
  "A warm shower an hour or two before bed helps your body cool down for sleep. Add it to your evening. 🚿",
]

# ------------------------------------------------------------------ render
START = 122   # set from `python scripts/next_number.py peak.wellness.lab`; re-running rebuilds the same folders


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
