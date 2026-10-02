"""Week 1 batch for @fin.ance18: 14 carousels + 42 single posts.
Writes straight into content/fin.ance18/queue/ continuing the numbering.
Growth figures: monthly contributions, 7% average annual return, compounded monthly.
2026 limits from IRS: 401(k) $24,500, IRA $7,500 (+$1,100 catch-up 50+), HSA $4,400 / $8,750."""
import os, sys, shutil
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from brand import *

ROOT = Path(__file__).resolve().parents[2]
Q = ROOT / "content" / "fin.ance18" / "queue"
TAGS = "#personalfinance #investing #moneytips #financialfreedom #budgeting #wealthbuilding #financialliteracy #moneyhabits"
FOOT = "\n\nFollow @fin.ance18 for one money habit a day.\n.\n.\n" + TAGS + "\n"

# ------------------------------------------------------------------ content
CAROUSELS = [
  dict(slug="5-accounts", k="Money roadmap", title="5 accounts that [build wealth]", sub="Know what each one is for, and use them in the right order.",
       cap="Each account has a different job. 📌 Save this and check which ones you already have.",
       pts=[("01", "[High-yield] savings", "For your emergency fund and short-term goals. Safe, easy to reach, and it earns far more than a regular checking account."),
            ("02", "The [401(k)]", "Invest straight from your paycheck, often with an employer match. The 2026 employee limit is $24,500."),
            ("03", "The [Roth IRA]", "Pay tax now, withdraw tax-free in retirement if you follow the rules. The 2026 limit is $7,500 if your income qualifies."),
            ("04", "The [HSA]", "With an eligible high-deductible health plan: money goes in pre-tax and comes out tax-free for medical costs. 2026: $4,400 self, $8,750 family."),
            ("05", "A [brokerage] account", "No contribution limits and no age rules. Use it for goals beyond retirement once the tax-advantaged accounts are covered.")]),
  dict(slug="50-30-20", k="Budgeting", title="The [50/30/20] budget rule", sub="The simplest budget that actually sticks.",
       cap="If budgets never work for you, start here. Three buckets, that's it. Where does your money go right now? 👇",
       pts=[("50%", "for [needs]", "Rent, groceries, utilities, insurance and minimum debt payments."),
            ("30%", "for [wants]", "Dining out, travel, subscriptions, hobbies. The fun stuff, guilt-free."),
            ("20%", "for [your future]", "Emergency fund, investing and extra debt payments."),
            ("$4K", "take-home [example]", "$2,000 for needs, $1,200 for wants, $800 for your future, every month."),
            ("TIP", "Protect the [20%] first", "If rent is high, trim wants before you cut what goes to savings.")]),
  dict(slug="credit-score", k="Credit", title="What actually [moves your credit score]", sub="The five factors behind your FICO score.",
       cap="Your credit score isn't a mystery. Here's how FICO weighs it. 📌 Save this.",
       pts=[("35%", "Paying [on time]", "Payment history is the biggest factor. One late payment can hurt for years, so set up autopay for at least the minimum."),
            ("30%", "How much you [owe]", "Mostly your credit utilization: card balances compared to your limits. Lower is better."),
            ("15%", "Length of [history]", "Older accounts help. Think twice before closing your oldest card."),
            ("10%", "New [credit]", "Several applications in a short time can lower your score a little."),
            ("10%", "Credit [mix]", "A mix of account types helps slightly. Never take on debt just for this.")]),
  dict(slug="index-funds", k="Investing basics", title="Index funds, [explained simply]", sub="Why so many investors keep it boring.",
       cap="You don't need to pick stocks to build wealth. Here's how index funds work. Do you own one yet?",
       pts=[("01", "Own [the whole market]", "One fund holds hundreds or thousands of companies at once, like everything in the S&P 500."),
            ("02", "Tiny [fees]", "No one is paid to pick stocks, so costs can be very low. Many broad index funds charge under 0.10% a year."),
            ("03", "Built-in [diversification]", "If one company struggles, it's a small slice of what you own."),
            ("04", "You won't beat the market. [You'll be the market.]", "Over long periods, most actively managed funds have trailed their index after fees."),
            ("05", "How to [start]", "Open a brokerage account or check your 401(k), pick a broad low-cost index fund, and automate contributions.")]),
  dict(slug="fee-cost", k="The math", title="How a [1% fee] can cost you six figures", sub="Same savings, same years. Different fees.",
       cap="Fees look tiny, but they compound too. Check the expense ratio of every fund you own. (Illustration only, returns aren't guaranteed.)",
       pts=[("SET", "Same [$500 a month]", "Invested for 30 years. Fund A returns 7% a year after costs. Fund B earns the same but charges 1% more, so you keep 6%."),
            ("A", "About [$610K]", "What Fund A grows to after 30 years."),
            ("B", "About [$502K]", "What Fund B grows to. That extra 1% quietly cost about $108,000."),
            ("TIP", "Check your [expense ratio]", "You'll find it on each fund's page in your 401(k) or brokerage. Lower is usually better.")]),
  dict(slug="emergency-fund", k="Money roadmap", title="How to build an [emergency fund]", sub="The account that keeps a bad day from becoming debt.",
       cap="An emergency fund is the base of everything else. How many months do you have saved? 👇",
       pts=[("01", "Start with [$1,000]", "A small first goal you can hit fast. It already covers many surprise bills."),
            ("02", "Aim for [3 to 6 months]", "Of essential expenses: housing, food, insurance, transport, minimum payments."),
            ("03", "Keep it [separate]", "A high-yield savings account at a different bank is easy to reach but hard to dip into."),
            ("04", "Make it [automatic]", "Schedule a transfer every payday, even if it's only $25."),
            ("05", "Only for [real emergencies]", "Job loss, medical bills, urgent car or home repairs. Not sales.")]),
  dict(slug="roth-vs-traditional", k="Investing basics", title="Roth vs Traditional: [which one?]", sub="It mostly comes down to when you pay the tax.",
       cap="Roth or Traditional? Here's the simple version. Roth IRA contributions have income limits, so check yours.",
       pts=[("01", "Traditional: [tax break now]", "Contributions can lower your taxable income today. You pay income tax when you withdraw in retirement."),
            ("02", "Roth: [tax-free later]", "You pay tax on the money now. Qualified withdrawals in retirement are tax-free."),
            ("03", "Higher bracket later? [Roth often wins.]", "Early in your career, your tax rate is often lower than it will be."),
            ("04", "Lower bracket later? [Traditional often wins.]", "Big earners today may prefer the deduction now."),
            ("05", "Not sure? [Use both.]", "Splitting between Roth and Traditional gives you flexibility in retirement.")]),
  dict(slug="avalanche-vs-snowball", k="Debt", title="Two ways to [crush your debt]", sub="Pick the one you'll actually stick with.",
       cap="Avalanche or snowball? Both work if you keep going. Which one are you using? 👇",
       pts=[("01", "The [avalanche]", "Pay off the highest interest rate first. Mathematically, it saves you the most money."),
            ("02", "The [snowball]", "Pay off the smallest balance first. Quick wins keep you motivated."),
            ("03", "Either way: [minimums on everything]", "Then put every extra dollar on one target until it's gone, and roll that payment to the next."),
            ("04", "The best method is [the one you finish.]", "Consistency beats the perfect plan.")]),
  dict(slug="7-habits", k="Money habits", title="7 habits of people who [build wealth quietly]", sub="None of them require a high income.",
       cap="Wealth is mostly habits repeated for years. How many of these do you already do?",
       pts=[("01", "They [pay themselves first]", "Savings and investing come out before anything else gets spent."),
            ("02", "They [automate] everything", "Bills, savings and investments run on autopilot."),
            ("03", "They spend [less than they earn]", "Every month, no matter how much they make."),
            ("04", "They resist [lifestyle creep]", "A raise goes to their goals first, not a bigger car."),
            ("05", "They invest [in every market]", "Up, down or sideways, the contributions keep going."),
            ("06", "They track their [net worth]", "What gets measured gets improved."),
            ("07", "They keep [learning]", "Books, podcasts, and asking questions before signing anything.")]),
  dict(slug="dca", k="Investing basics", title="Dollar-cost averaging: [no market timing needed]", sub="The stress-free way to invest regularly.",
       cap="You can't control the market. You can control your schedule. 📌 Save this.",
       pts=[("01", "Invest a [fixed amount]", "The same dollar amount on a regular schedule, like every payday."),
            ("02", "Prices high? [You buy fewer shares.]", "Prices low? You buy more. It evens out over time."),
            ("03", "It removes [emotion]", "No guessing, no waiting for the perfect moment that never comes."),
            ("04", "You may [already do it]", "Every 401(k) contribution from your paycheck is dollar-cost averaging.")]),
  dict(slug="sinking-funds", k="Budgeting", title="Sinking funds: [no more surprise expenses]", sub="Save for the bills you know are coming.",
       cap="Most 'surprise' expenses aren't surprises. Plan for them and they stop hurting.",
       pts=[("01", "What it [is]", "A small savings bucket for a known future cost."),
            ("02", "What to [save for]", "Car repairs, holidays, annual subscriptions, insurance premiums, vacations, gifts."),
            ("03", "The [formula]", "Total cost divided by the months until it's due = what to save each month."),
            ("04", "[Example]", "$1,200 holiday budget, 12 months away: save $100 a month and December is already paid for.")]),
  dict(slug="net-worth", k="Money roadmap", title="How to calculate your [net worth]", sub="The one number that shows your real progress.",
       cap="Your income isn't your progress. Your net worth is. Calculate yours this weekend.",
       pts=[("01", "Add up what you [own]", "Cash, investments, retirement accounts, and the realistic value of your home or car."),
            ("02", "Add up what you [owe]", "Credit cards, student loans, car loans, mortgage."),
            ("03", "Own minus owe = [net worth]", "That's it. It can be negative, and that's okay."),
            ("04", "Watch the [direction]", "Early on, the trend matters more than the number. Update it every quarter.")]),
  dict(slug="401k-match", k="Investing basics", title="The 401(k) match is [free money]", sub="Don't leave part of your pay on the table.",
       cap="If your employer offers a match, getting all of it is usually step one. Check your plan's rules and vesting schedule.",
       pts=[("01", "How it [works]", "When you contribute, your employer adds money too, up to a limit."),
            ("02", "Example: [$60K salary]", "Employer matches 50% of what you put in, up to 6% of pay. You contribute $3,600, they add $1,800."),
            ("03", "An instant [50% return]", "On the money you put in to get the match. Hard to find anywhere else."),
            ("$183K", "What $1,800 a year [can become]", "After 30 years at a 7% average annual return. Illustration only."),
            ("TIP", "Check [vesting]", "Some matches only become fully yours after you've stayed a certain number of years.")]),
  dict(slug="lifestyle-creep", k="Money habits", title="How to [beat lifestyle creep]", sub="Earn more without staying stuck.",
       cap="More income doesn't build wealth. A bigger gap between income and spending does.",
       pts=[("01", "Save the [raise first]", "Increase your savings rate before you increase your spending."),
            ("02", "The [half rule]", "Enjoy half of every raise. Send the other half to your goals."),
            ("03", "Wait [30 days]", "For big purchases. If you still want it, plan for it."),
            ("04", "Upgrade [on purpose]", "Spend more on the few things you truly value, and cut the rest."),
            ("05", "Track your [savings rate]", "Not just your income. That's the number that builds wealth.")]),
]

STATS = [
  ("$787K", "is what [$300 a month] from age 25 can grow to by 65.", "7% average annual return. Start at 35 instead and it's about $366K.", "Starting 10 years earlier more than doubles the result. Time is the biggest advantage you have."),
  ("$371K", "is what [$10 a day] invested for 30 years could become.", "About $304 a month at a 7% average annual return. You'd contribute about $109,500.", "Small daily amounts, invested consistently, add up to life-changing money."),
  ("$108K", "is roughly what a [1% fee] can cost you over 30 years.", "$500 a month at 7% vs 6% after fees. Illustration only.", "Check the expense ratio on every fund you own."),
  ("$226K", "from [$100 a week] invested for 20 years.", "7% average annual return. You'd contribute $104,000.", "You don't need a lot to start. You need to start."),
  ("+$305K", "more after 30 years by saving [15% instead of 10%] of a $60K salary.", "$750 vs $500 a month at 7%: about $915K vs $610K.", "A 5% change in your savings rate can change your whole retirement."),
  ("7.2", "years to double your money at a [10% average return.]", "Rule of 72: 72 ÷ 10 = 7.2. An approximation, and returns vary.", "The Rule of 72 is the quickest money math you'll ever learn."),
  ("$18K", "is a 6-month [emergency fund] if your essentials cost $3,000 a month.", "Essentials: housing, food, insurance, transport, minimum payments.", "Work out your number, then start with the first $1,000."),
  ("$1,800", "a year in [free money] from a typical 401(k) match.", "$60K salary, 50% match on up to 6% of pay.", "Make sure you're getting your full match."),
  ("35%", "of your FICO score comes from [paying on time.]", "Payment history is the single biggest factor.", "Set autopay for at least the minimum on every card."),
  ("30%", "credit utilization is the line many experts say to [stay under.]", "Lower is better. Single digits are even stronger.", "Utilization = card balances ÷ credit limits."),
  ("$810K", "from [$1,000 a month] over 25 years.", "7% average annual return. You'd contribute $300,000.", "Consistency plus time is the whole strategy."),
  ("$7,500", "is the 2026 [Roth IRA] contribution limit.", "If your income qualifies. $8,600 if you're 50 or older.", "Have you opened yours yet?"),
]

QUOTES = [
  ("Pay yourself first. [Bills will always find you.]", "Money habits"),
  ("Wealth is what you [don't see.] The car not bought, the money invested instead.", "Mindset"),
  ("Your income is a tool. [Your habits decide] what it builds.", "Money habits"),
  ("Don't save what's left after spending. [Spend what's left after saving.]", "Budgeting"),
  ("Automate your savings. [Willpower is overrated.]", "Money habits"),
  ("A raise is only a raise [if you don't spend it.]", "Mindset"),
  ("Boring investing [builds exciting futures.]", "Investing"),
  ("Debt is borrowing from [your future self.]", "Debt"),
  ("A dollar invested at 25 [works harder than a dollar at 45.]", "Investing"),
  ("Rich isn't a number. [Freedom is.]", "Mindset"),
  ("Know where your money goes, or [it will decide for you.]", "Budgeting"),
  ("Small amounts invested consistently [beat big plans never started.]", "Investing"),
  ("Your net worth grows [when your ego shrinks.]", "Mindset"),
  ("Spend on what you love. [Cut ruthlessly on what you don't.]", "Budgeting"),
  ("An emergency fund turns a crisis into [an inconvenience.]", "Money habits"),
  ("Credit cards reward discipline and [punish everything else.]", "Credit"),
  ("Financial freedom often starts with [a boring spreadsheet.]", "Budgeting"),
  ("Market drops feel scary. [Selling at the bottom is scarier.]", "Investing"),
  ("You don't need a lot to start investing. [You need to start.]", "Investing"),
  ("Comparison is expensive. [Their lifestyle isn't your goal.]", "Mindset"),
  ("Buy assets first. [Treat yourself second.]", "Money habits"),
  ("Your future self is counting on [what you do with this paycheck.]", "Mindset"),
  ("Low fees, broad funds, lots of time. [That's most of the secret.]", "Investing"),
  ("A budget is a plan [for the life you actually want.]", "Budgeting"),
  ("Money saved is [options created.]", "Mindset"),
  ("Early on, the best investment is often [your skills.]", "Mindset"),
  ("Interest works for you or [against you.] Choose your side.", "Debt"),
  ("Track every dollar for one month. [It will change how you see money.]", "Budgeting"),
  ("Being good with money is [mostly about patience.]", "Mindset"),
  ("Looking rich and being rich [are two different goals.]", "Mindset"),
]
QUOTE_CAPS = [
  "Move money to savings the day you get paid, before anything else.",
  "Real wealth is quiet. It's the stuff you chose not to buy.",
  "Two people with the same salary can end up in completely different places.",
  "Flip the order and everything changes.",
  "Set it up once and let it run. Automation beats motivation.",
  "Next raise: decide where it goes before it hits your account.",
  "Index funds, automatic contributions, long time horizon. Not exciting. Very effective.",
  "Every dollar of high-interest debt is a dollar your future self has to pay back with interest.",
  "Time does more of the heavy lifting than the amount does.",
  "The goal isn't a number. It's choices.",
  "Check last month's spending. Anything surprise you?",
  "Start with $25. Increase it later.",
  "Comparison and image spending quietly drain wealth.",
  "Value-based spending: big on what matters, tiny on what doesn't.",
  "Do you have one yet? Even $1,000 is a great start.",
  "Pay the full statement balance every month and cards can work for you.",
  "Tracking isn't glamorous, but it's where control begins.",
  "Downturns are normal. Panic selling locks in the loss.",
  "Your first investment doesn't have to be big. It has to happen.",
  "You're only seeing their highlight reel, not their balance sheet.",
  "Build the base first, then enjoy the rewards.",
  "What's one move you'll make with your next paycheck?",
  "Keep it simple and keep it going.",
  "Budgets aren't about saying no. They're about saying yes to what matters.",
  "Every dollar saved buys you more freedom later.",
  "A new skill or certification can raise your income for decades.",
  "Paying 24% on a card or earning returns in an index fund. Which side are you on?",
  "Try it for 30 days. Just track, don't judge.",
  "Most money mistakes come from impatience.",
  "Stealth wealth is real.",
]

# ------------------------------------------------------------------ render
START = 8   # this batch fills queue items 0008-0063; re-running rebuilds the same folders


def make_item(n, slug):
    d = Q / f"{n:04d}-{slug}"
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    return d


def render_carousel(c, d, seed):
    pts = c["pts"]; total = len(pts) + 2
    cover(c["title"], c["sub"], str(d / "01.jpg"), c["k"], seed=seed)
    for i, (num, head, body) in enumerate(pts, 2):
        point(num, head, body, str(d / f"{i:02d}.jpg"), c["k"], f"{i}/{total}", seed=seed + i)
    cta(str(d / f"{total:02d}.jpg"), c["k"], f"{total}/{total}")
    (d / "caption.txt").write_text(c["cap"] + FOOT)


def main():
    singles = []
    for i, (num, txt, note, cap) in enumerate(STATS):
        singles.append(("stat", (num, txt, note), cap))
    for (txt, k), cap in zip(QUOTES, QUOTE_CAPS):
        singles.append(("quote", (txt, k), cap))
    # spread stats among quotes: every 3rd-4th single is a stat
    stats = [s for s in singles if s[0] == "stat"]; quotes = [s for s in singles if s[0] == "quote"]
    mixed = []
    while stats or quotes:
        for _ in range(3):
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
                    d = make_item(n, "stat-" + num.strip("+$%").replace(",", "").replace(".", "-").lower())
                    stat(num, txt, str(d / "01.jpg"), note=note, seed=seed)
                else:
                    txt, k = args
                    d = make_item(n, "quote")
                    quote(txt, str(d / "01.jpg"), kicker=k, seed=seed)
                (d / "caption.txt").write_text(cap + FOOT)
            else:
                continue
            n += 1; seed += 10
    print("queue now ends at", n - 1)


if __name__ == "__main__":
    main()
