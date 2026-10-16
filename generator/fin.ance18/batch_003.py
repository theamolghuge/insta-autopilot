"""Batch 003 for @fin.ance18: 3 carousels + 8 single posts (queue 0064-0074), timed for open enrollment season.
Writes straight into content/fin.ance18/queue/ continuing the numbering. Every money figure is computed below.
Growth figures: monthly contributions, 7% average annual return, compounded monthly (illustration only).
Limits checked on irs.gov (2026-10-16):
  - 2027 HSA: $4,500 self-only / $9,000 family; HDHP min deductible $1,750 self-only (Rev. Proc. 2026-24)
  - 2026 single standard deduction $16,100; brackets 10% to $12,400, 12% to $50,400, 22% to $105,700 (Rev. Proc. 2025-32)
  - FICA employee share 7.65% (6.2% Social Security + 1.45% Medicare)."""
import sys, shutil
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from brand import *

ROOT = Path(__file__).resolve().parents[2]
Q = ROOT / "content" / "fin.ance18" / "queue"
FOLLOW = "\n\nFollow @fin.ance18 for one money habit a day.\n.\n.\n"


def money(x):
    return f"${x:,.0f}"


def k(x):
    return f"${round(x / 1000):,}K"


def fv(monthly, years, rate=0.07):
    r, n = rate / 12, years * 12
    return monthly * ((1 + r) ** n - 1) / r


def payoff(balance, apr, payment):
    months, interest = 0, 0.0
    while balance > 0:
        i = balance * apr / 12
        interest += i
        balance = balance + i - payment
        months += 1
    return months, interest


# ------------------------------------------------------------------ figures
# 64: what $25 a week becomes
WK = 25; WK_M = WK * 52 / 12; WK_FV = fv(WK_M, 30); WK_IN = WK * 52 * 30

# 65: open enrollment plan comparison (made-up plans)
A_PREM, A_DED = 120, 1500
B_PREM, B_DED = 60, 4000
A_LOW, B_LOW = A_PREM * 12, B_PREM * 12                  # barely use care
A_HIGH, B_HIGH = A_LOW + A_DED, B_LOW + B_DED            # hit the deductible
HSA_SELF, HSA_FAM, HDHP_MIN = 4500, 9000, 1750

# 68: credit card minimum-ish payment
CC_BAL, CC_APR = 5000, 0.24
CC1_M, CC1_I = payoff(CC_BAL, CC_APR, 150)
CC2_M, CC2_I = payoff(CC_BAL, CC_APR, 300)

# 69: paycheck breakdown, $65K single, 6% traditional 401(k)
SAL = 65000; K401 = SAL * 0.06; FICA = SAL * 0.0765; STD = 16100
TAXABLE = SAL - K401 - STD
FED = 0.10 * min(TAXABLE, 12400) + 0.12 * max(0, min(TAXABLE, 50400) - 12400) + 0.22 * max(0, TAXABLE - 50400)
assert TAXABLE <= 50400  # 12% top bracket assumed in the text below
TAKE = SAL - K401 - FICA - FED
TAKE_M = TAKE / 12
EFF = FED / SAL * 100
PER100 = 100 * (1 - 0.12)   # take-home cost of $100 more into a traditional 401(k) in the 12% bracket

# 70: tax refund
REFUND = 3000; REFUND_M = REFUND / 12

# 71: HSA invested for 20 years
HSA_FV = fv(HSA_SELF / 12, 20); HSA_IN = HSA_SELF * 20

# 73: Fix My Budget (made-up example)
TAKE_HOME = 4200
NOW = dict(rent=1500, car=450, insurance=180, utilities=230, groceries=520, dining=600, subs=95, shopping=425, other=200)
assert sum(NOW.values()) == TAKE_HOME
FIX_DINING = 600 - 350; FIX_SUBS = 95 - 40; FIX_SHOP = 425 - 300; FIX_GROC = 520 - 470
FREED = FIX_DINING + FIX_SUBS + FIX_SHOP + FIX_GROC
TO_EF, TO_ROTH = 300, FREED - 300
FREED_FV = fv(FREED, 10)

# 74: weekly challenge
SUB = 15; SUB_Y = SUB * 12; SUB_FV = fv(SUB, 20)

# ------------------------------------------------------------------ content
TAGS_OE = "#openenrollment #hsa #employeebenefits #personalfinance"
TAGS_CREDIT = "#creditscore #creditcards #debtfree #personalfinance"
TAGS_INV = "#investing #compoundinterest #wealthbuilding #personalfinance"
TAGS_TAX = "#taxes #paycheck #personalfinance #moneytips"
TAGS_BUD = "#budgeting #budget #moneytips #personalfinance"
TAGS_HAB = "#moneyhabits #savingmoney #moneytips #personalfinance"

POSTS = [
  dict(kind="stat", slug="stat-25-week",
       args=(k(WK_FV), f"is what [${WK} a week] invested for 30 years can become.",
             f"About {money(WK_M)} a month at a 7% average annual return, compounded monthly. You'd put in {money(WK_IN)}."),
       cap=f"What $25 a week becomes: about {k(WK_FV)} in 30 years. Less than a takeout order, every week, on autopilot. "
           f"Illustration only, returns aren't guaranteed. What would you skip to invest $25?" + FOLLOW + TAGS_INV),

  dict(kind="carousel", slug="open-enrollment",
       title="Open enrollment: [5 checks] before you click renew",
       sub="Most people re-pick last year's plan in a minute. Give it 20 minutes instead.",
       cap="Open enrollment checklist: health plan, HSA, FSA and insurance, before you click renew. "
           "📌 Save this for when your benefits window opens. Which one do you always skip?" + FOLLOW + TAGS_OE,
       pts=[("1 YEAR", "This choice is [locked in for a year]", "Premiums, deductibles and FSA amounts are mostly set until next open enrollment, unless you have a qualifying life event."),
            ("01", "Compare [total cost], not premiums",
             f"Plan A: {money(A_PREM)}/mo, {money(A_DED)} deductible. Plan B: {money(B_PREM)}/mo, {money(B_DED)} deductible. "
             f"Low-use year: A {money(A_LOW)}, B {money(B_LOW)}. Hit the deductible: A {money(A_HIGH)}, B {money(B_HIGH)}."),
            ("02", "Check the [HSA] option",
             f"For 2027, an HSA-eligible plan needs a deductible of at least {money(HDHP_MIN)} (self-only). "
             f"You can contribute up to {money(HSA_SELF)}, or {money(HSA_FAM)} for family coverage."),
            ("03", "Size your [FSA] carefully", "FSA money is mostly use-it-or-lose-it. Some plans allow a small carryover or grace period. Elect what you'll actually spend."),
            ("04", "Confirm your [doctors and prescriptions]", "Networks and drug lists can change every year. Check yours before you renew."),
            ("05", "Review [life and disability] cover", "Group coverage through work is often cheap. Make sure the amount still fits your life.")]),

  dict(kind="text", slug="myth-carry-balance",
       args=("Myth: carrying a card balance [builds your credit.]",
             "Math: paying the full statement balance builds the same payment history, and costs you $0 in interest."),
       cap="Credit card myth: you don't need to carry a balance to build credit. Use the card, pay it in full, repeat. "
           "Did you ever hear this one?" + FOLLOW + TAGS_CREDIT),

  dict(kind="quote", slug="quote",
       args=("Read your benefits guide once a year. [It's part of your pay.]",),
       cap="Employee benefits are part of your compensation: match, HSA, insurance, sometimes more. "
           "Open enrollment is the week to actually read the guide." + FOLLOW + TAGS_OE),

  dict(kind="stat", slug="stat-cc-payoff",
       args=(f"{CC1_M} months", f"to clear a [{money(CC_BAL)} card] paying $150 a month at {CC_APR*100:.0f}% APR.",
             f"About {money(CC1_I)} in interest. At $300 a month: {CC2_M} months and about {money(CC2_I)}. No new charges."),
       cap=f"Credit card interest, by the numbers: doubling the payment on a {money(CC_BAL)} balance saves about "
           f"{money(CC1_I - CC2_I)} and years of payments. Assumes no new charges and a fixed {CC_APR*100:.0f}% APR." + FOLLOW + TAGS_CREDIT),

  dict(kind="carousel", slug="paycheck-65k",
       title=f"Where a [{money(SAL)} salary] actually goes",
       sub="Single filer, 2026 federal rules, before state and local tax.",
       cap=f"Paycheck breakdown: a {money(SAL)} salary is about {money(TAKE_M)} a month take-home after 401(k), FICA and federal tax. "
           "Assumes single, standard deduction, 6% traditional 401(k), no state tax or premiums. Share it with someone budgeting off their salary." + FOLLOW + TAGS_TAX,
       pts=[(money(TAKE), "is what's left to [spend and save]", f"Out of {money(SAL)}. That's about {money(TAKE_M)} a month. Here's where the rest goes."),
            (money(K401), "goes to your [401(k)]", "A 6% traditional contribution. It's still your money, and it lowers your taxable income."),
            (money(FICA), "for [Social Security and Medicare]", "7.65% FICA on every dollar of pay, including the part that goes into a traditional 401(k)."),
            (money(FED), "in [federal income tax]",
             f"Taxable income: {money(SAL)} − {money(K401)} − {money(STD)} standard deduction = {money(TAXABLE)}. That's {EFF:.1f}% of the salary."),
            ("TIP", "Your top rate is [12%], not 22%",
             f"So each extra $100 into a traditional 401(k) lowers take-home by only about {money(PER100)}.")]),

  dict(kind="text", slug="myth-tax-refund",
       args=("Myth: a big tax refund is [a bonus.]",
             f"Math: a {money(REFUND)} refund is {money(REFUND_M)} a month you lent the government at 0% interest."),
       cap="Tax refund myth: a refund is your own money coming back. If yours is big every year, updating your W-4 "
           f"can put about {money(REFUND_M)} a month back in your paycheck instead. Big refund or small?" + FOLLOW + TAGS_TAX),

  dict(kind="stat", slug="stat-hsa-20y",
       args=(k(HSA_FV), f"from investing the [2027 HSA limit] of {money(HSA_SELF)} a year for 20 years.",
             f"Self-only limit (IRS Rev. Proc. 2026-24). 7% average annual return, {money(HSA_IN)} contributed. Illustration only."),
       cap="HSA investing: many HSAs let you invest the balance, not just hold cash. Pay small medical bills from your budget "
           "and let the account grow. Check your HSA's fees and fund options. Illustration only, returns aren't guaranteed." + FOLLOW + TAGS_OE),

  dict(kind="quote", slug="quote",
       args=("You don't need a perfect budget. [You need one you'll check.]",),
       cap="Budgeting tip: a 10-minute check every Sunday beats a perfect spreadsheet you never open. Pick your day." + FOLLOW + TAGS_BUD),

  dict(kind="carousel", slug="fix-my-budget-4200",
       title=f"Fix My Budget: [{money(TAKE_HOME)} take-home], $0 saved",
       sub="A made-up example. Real leaks, simple fixes.",
       cap=f"Fix My Budget: {money(FREED)} a month found in a {money(TAKE_HOME)} take-home budget without touching rent. "
           "Made-up example, your numbers will differ. Want us to fix a budget like yours next? Comment 'FIX'." + FOLLOW + TAGS_BUD,
       pts=[("$0", "saved each month, [on a decent income]", f"Rent is fine. The problem is lots of small leaks. Here's how we find {money(FREED)} a month."),
            ("NOW", "Where the money [goes today]",
             f"Rent {money(NOW['rent'])}, car {money(NOW['car'])}, groceries {money(NOW['groceries'])}, dining and delivery {money(NOW['dining'])}, "
             f"shopping {money(NOW['shopping'])}, bills and insurance {money(NOW['insurance'] + NOW['utilities'])}, "
             f"subscriptions {money(NOW['subs'])}, other {money(NOW['other'])}."),
            (f"+{money(FIX_DINING)}", "Dining and delivery: [$600 → $350]", "Cook three more nights a week. Still eat out, just on purpose."),
            (f"+{money(FIX_SUBS + FIX_SHOP)}", "Subscriptions and shopping: [set caps]",
             f"Cancel unused subscriptions ({money(NOW['subs'])} → $40) and cap shopping at $300 a month (was {money(NOW['shopping'])})."),
            (f"+{money(FIX_GROC)}", "Groceries: [plan the week]", f"A list and a meal plan cut impulse buys. {money(NOW['groceries'])} → $470."),
            (money(FREED), "a month, [automated on payday]",
             f"{money(TO_EF)} to the emergency fund, {money(TO_ROTH)} to a Roth IRA. {money(FREED)} a month for 10 years at 7% is about {k(FREED_FV)}.")]),

  dict(kind="text", slug="challenge-subscription",
       args=("This week's challenge: [cancel one subscription] you forgot about.",
             f"A $15 one is {money(SUB_Y)} a year. Invested monthly for 20 years at 7%, that's about {money(round(SUB_FV, -2))}."),
       cap="Weekly recap + challenge: this week we covered open enrollment, a paycheck breakdown and a budget fix. "
           "Now check your bank statement for one subscription you don't use and cancel it. Comment 'DONE' when you do." + FOLLOW + TAGS_HAB),
]

# ------------------------------------------------------------------ render
START = 64   # from `python scripts/next_number.py fin.ance18`; this batch fills 0064-0074


def make_item(n, slug):
    d = Q / f"{n:04d}-{slug}"
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    return d


def main():
    n = START
    for p in POSTS:
        if p["kind"] == "carousel":
            d = make_item(n, "carousel-" + p["slug"])
            pts = p["pts"]; total = len(pts) + 2
            cover(p["title"], p["sub"], str(d / "01.jpg"))
            for i, (num, head, body) in enumerate(pts, 2):
                point(num, head, body, str(d / f"{i:02d}.jpg"))
            cta(str(d / f"{total:02d}.jpg"))
        else:
            d = make_item(n, p["slug"])
            a = p["args"]
            if p["kind"] == "stat":
                stat(a[0], a[1], str(d / "01.jpg"), note=a[2])
            elif p["kind"] == "quote":
                quote(a[0], str(d / "01.jpg"))
            else:
                cover(a[0], a[1], str(d / "01.jpg"))
        (d / "caption.txt").write_text(p["cap"] + "\n")
        n += 1
    print("queue now ends at", n - 1)


if __name__ == "__main__":
    main()
