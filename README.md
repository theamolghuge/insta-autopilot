# Instagram Autopilot

Free, multi-account Instagram auto-poster that runs on GitHub Actions.
Every 15 minutes GitHub checks each account's posting times. When a time has
just passed, the next post in that account's queue is published through the
official Instagram API.

See **HOW_TO.md** for everyday jobs (new batches, new accounts, previews) and `brand/` for logos and bio.

## How it's organised

```
accounts.json                        which accounts, their posting times and time zone
content/<account>/queue/NNNN-name/   one folder per post, published in number order (deleted daily once live)
    01.jpg                           1 image  = single post
    01.jpg ... 10.jpg                2-10     = carousel (same size, JPEG only)
    caption.txt                      caption (max 2,200 characters, 30 hashtags)
state/<account>.json                 what has been posted (written automatically)
generator/<account>/                 brand templates and scripts that make the images
generator/ai-news/                   AI news page: collects news, writes and renders one post per run
scripts/publish.py                   the poster
scripts/tokens.py                    checks / refreshes access tokens
.github/workflows/                   the schedules (publish.yml every 15 min, ai-news.yml every 3 h, tokens.yml weekly)
```

Cleanup: `.github/workflows/cleanup.yml` deletes posts that are live once a day, so the repo doesn't keep growing.
New batches take their numbers from `scripts/next_number.py` (numbers are never reused).

Rules the poster follows:
- One post per time slot. If GitHub can't run within 2 hours of a slot, that slot is skipped (no bursts of late posts).
- If the token is broken, nothing is used up; the run fails and GitHub emails you.
- A post that fails 3 times is marked failed in `state/` and skipped.
- Instagram allows at most 100 API posts per account per 24 hours.

## Secrets (Settings > Secrets and variables > Actions)

| Secret | What it is |
|---|---|
| `IG_TOKEN_FIN_ANCE18` | Instagram access token for @fin.ance18 |
| `IG_TOKEN_AI_NEWS_DAILY` | Instagram access token for the AI news page |
| `ANTHROPIC_API_KEY` | optional: only used by the AI news safety net; normal posts are written by the Claude scheduled task |
| `SECRETS_PAT` | GitHub fine-grained token with **Secrets: read and write** on this repo, so tokens can renew themselves every Monday |

## Manual controls (Actions tab)

- **Publish posts > Run workflow**: `dry-run` shows what would post next, `post-now` posts the next item immediately.
- **Instagram tokens > Run workflow**: `check` tests every token, `refresh` renews them.

## Adding another Instagram account

1. Generate a token for the new account in the same Meta app (it needs to be a Professional account).
2. Add it as a secret, e.g. `IG_TOKEN_MY_NEW_PAGE`, and add a matching line `IG_TOKEN_MY_NEW_PAGE: ${{ secrets.IG_TOKEN_MY_NEW_PAGE }}` under `env:` in `publish.yml` and `tokens.yml` (never pass all secrets at once: GitHub blocks that as possibly malicious).
3. Add an entry to `accounts.json`:
   ```json
   {"id": "my.new.page", "token_secret": "IG_TOKEN_MY_NEW_PAGE",
    "timezone": "America/New_York", "slots": ["08:00", "12:00", "19:00"], "enabled": true}
   ```
4. Put its posts in `content/my.new.page/queue/`.

Set `"enabled": false` to pause an account.
