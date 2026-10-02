import os
from brand import *

import sys
out = sys.argv[1] if len(sys.argv) > 1 else "build/batch_001"
os.makedirs(out, exist_ok=True)

# ---- single posts ----
quote("Your salary isn't your wealth. [What you keep and invest] is.", f"{out}/single_01.jpg", seed=1)
quote("A budget isn't a restriction. It's [telling your money where to go] before it disappears.", f"{out}/single_02.jpg", seed=2)
quote("Lifestyle creep is quiet. [Every raise you spend] is a raise you never really kept.", f"{out}/single_03.jpg", seed=3)
stat("$610K", "is roughly what [$500 a month] can grow into over 30 years.", f"{out}/single_04.jpg",
     note="Assumes a 7% average annual return, compounded monthly. Total contributed: $180,000.", seed=4)
quote("Compound interest rewards [patience, not perfect timing.]", f"{out}/single_05.jpg", kicker="Investing", seed=5)

# ---- carousel A: order of operations ----
k = "Money roadmap"
d = f"{out}/carousel_invest_order"; os.makedirs(d, exist_ok=True)
cover("The order to [invest your money]", "Most people do these out of order. Here's a simple sequence to follow.", f"{d}/01.jpg", k, seed=10)
steps = [
    ("Build a [starter emergency fund]", "Park $1,000 to $2,000 in a high-yield savings account so a surprise bill doesn't land on a credit card."),
    ("Grab your [full employer match]", "If your 401(k) offers a match, contribute at least enough to get all of it. It's part of your pay."),
    ("Pay off [high-interest debt]", "Credit cards often charge 20%+ APR. Paying that down is a guaranteed return few investments can beat."),
    ("Grow your safety net to [3 to 6 months]", "Cover your essential expenses so a job loss or emergency never forces you to sell investments."),
    ("Open a [Roth IRA]", "You can contribute up to $7,500 in 2026 if your income qualifies. Qualified withdrawals in retirement are tax-free."),
    ("Raise your [401(k) contributions]", "The 2026 employee limit is $24,500. Work toward it by adding 1% every time you get a raise."),
    ("Invest in a [taxable brokerage]", "Once the tax-advantaged accounts are covered, low-cost index funds keep the rest of your money growing."),
]
n = len(steps) + 2
for i, (h, b) in enumerate(steps, 1):
    point(f"0{i}", h, b, f"{d}/{i+1:02d}.jpg", k, f"{i+1}/{n}", seed=10 + i)
cta(f"{d}/{n:02d}.jpg", k, f"{n}/{n}")

# ---- carousel B: rule of 72 ----
k = "Investing basics"
d = f"{out}/carousel_rule_of_72"; os.makedirs(d, exist_ok=True)
n = 6
cover("The Rule of 72: [how fast your money doubles]", "One simple division you can do in your head.", f"{d}/01.jpg", k, seed=20)
point("72 ÷ r", "Divide 72 by your [annual return.]", "The answer is roughly how many years it takes your money to double.", f"{d}/02.jpg", k, f"2/{n}", seed=21)

c = Canvas(22); c.chrome(k, page=f"3/{n}")
y = 260
y = c.rich("$10,000 invested at [8% a year:]", "display", 76, y, lh=1.18) + 60
for amt, yrs in [("$10,000", "Today"), ("$20,000", "In 9 years"), ("$40,000", "In 18 years"), ("$80,000", "In 27 years")]:
    c.label(amt, M, y, kind="display", size=92, color=ACCENT, spacing=0)
    c.label(yrs, W - M, y + 40, kind="sans", size=34, color=INK, spacing=0, anchor="ra")
    y += 150
c.label("72 ÷ 8 = 9 years per double. Figures are approximate.", M, y + 10, kind="sans", size=24, color=MUTED, spacing=0)
c.save(f"{d}/03.jpg")

quote("You didn't add more money. [Time did the heavy lifting.]", f"{d}/04.jpg", kicker=k, seed=23, page=f"4/{n}")
point("24%", "It works [against you] too.", "Credit card debt at 24% APR doubles in about 3 years if it's left unpaid. 72 ÷ 24 = 3.", f"{d}/05.jpg", k, f"5/{n}", seed=24)
cta(f"{d}/06.jpg", k, f"{n}/{n}")
