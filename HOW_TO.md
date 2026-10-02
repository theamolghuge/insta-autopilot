# How to

## Run things on your computer
```bash
pip install pillow                                        # only needed for making images
python scripts/preview.py fin.ance18                      # contact sheet of upcoming posts
python scripts/publish.py --dry-run                       # what would post next (no posting)
python generator/fin.ance18/batch_002.py                  # rebuild week 1 posts into the queue
python generator/selfhelp-theme/make_posts.py generator/selfhelp-theme/week.json out/   # self-help quote images
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

## Folder map
| Path | What |
|---|---|
| `accounts.json` | accounts, times, time zones |
| `content/<id>/queue/` | posts waiting to go out (and already posted ones) |
| `state/<id>.json` | posting log, written by the workflow |
| `generator/fin.ance18/` | finance brand templates, fonts, batch scripts |
| `generator/selfhelp-theme/` | self-help highlighter quote generator + 56 ready quotes |
| `brand/fin.ance18/` | logos, bio, brand rules |
| `scripts/` | publisher, token tools, preview |
| `.github/workflows/` | schedules: publish every 15 min, token refresh every Monday |
