# How to

## Run things on your computer
```bash
pip install pillow                                        # only needed for making images
python scripts/preview.py fin.ance18                      # contact sheet of upcoming posts
python scripts/publish.py --dry-run                       # what would post next (no posting)
python generator/fin.ance18/batch_002.py                  # rebuild week 1 posts into the queue
python generator/selfhelp-theme/make_posts.py generator/selfhelp-theme/week.json out/   # self-help quote images
python generator/ai-news/make_post.py --out out/ai-news-test                              # one AI news post, preview only
```

## Easiest: ask Claude
Open a Claude session with this repo attached and say, for example:
- "Make next week's 56 posts for fin.ance18 and push them."
- "Add a new account `my.new.page` in the self-help niche, posting 5 times a day."
- "Change the fin.ance18 posting times to 8am, 12pm and 7pm New York time."
`CLAUDE.md` tells Claude how this repo works.

## Change posting times or pause
Edit `accounts.json`: change `slots` (24h, in the account's `timezone`) or set `"enabled": false`.

## Make a new batch by hand
1. Copy `generator/fin.ance18/batch_002.py` to `batch_003.py`.
2. Replace the content lists and set `START` to the next free number (`ls content/fin.ance18/queue`).
3. Run it, preview, commit and push.

## Post something specific next
Put it in a queue folder whose number is lower than every unposted item, or rename unposted folders.
Each folder needs `01.jpg` (and `02.jpg`... for carousels) plus `caption.txt`.

## Add a new Instagram account (e.g. a self-help theme page)
1. Make the account Professional, add it in your Meta app, generate its token.
2. GitHub > Settings > Secrets > Actions: add `IG_TOKEN_<NAME>`.
3. Add it to `accounts.json` (id, token_secret, timezone, slots, enabled).
4. Create `content/<id>/queue/` with posts. For the self-help style, render quotes with
   `generator/selfhelp-theme/make_posts.py` and put each image in its own folder with a caption.
5. Optionally add `brand/<id>/BRAND.md` so Claude knows the style.

## AI news page
- **Preview without posting:** Actions > AI news > Run workflow > mode `preview`. Download the images from the run.
- **Post one right now:** Actions > AI news > Run workflow > mode `normal` (optionally pick a format).
- **Change the mix of formats:** edit `format_mix` in `generator/ai-news/config.json`
  (`media_top`, `text`, `carousel`, `roundup`).
- **Change how often:** edit the `cron` line in `.github/workflows/ai-news.yml` (e.g. `23 */2 * * *` for every 2 hours).
  The account has no `slots`; the AI news workflow posts by itself and retries a failed post on its next run.
- **Add or remove a news source:** edit `FEEDS` in `generator/ai-news/news.py`.
- **Rename the handle:** change `handle` in `generator/ai-news/config.json` (the account id can stay).

## Folder map
| Path | What |
|---|---|
| `accounts.json` | accounts, times, time zones |
| `content/<id>/queue/` | posts waiting to go out (and already posted ones) |
| `state/<id>.json` | posting log, written by the workflow |
| `generator/fin.ance18/` | finance brand templates, fonts, batch scripts |
| `generator/ai-news/` | AI news collector, writer, brand renderer (fully automatic) |
| `generator/selfhelp-theme/` | self-help highlighter quote generator + 56 ready quotes |
| `brand/fin.ance18/` | logos, bio, brand rules |
| `scripts/` | publisher, token tools, preview |
| `.github/workflows/` | schedules: publish every 15 min, AI news every 3 h, token refresh every Monday |
