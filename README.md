# Instagram Autopilot

Free, multi-account Instagram auto-poster that runs on GitHub Actions.
Every 15 minutes GitHub checks each account's posting times. When a time has
just passed, the next post in that account's queue is published through the
official Instagram API.

## How it's organised

```
accounts.json                        which accounts, their posting times and time zone
content/<account>/queue/NNNN-name/   one folder per post, published in number order
    01.jpg                           1 image  = single post
    01.jpg ... 10.jpg                2-10     = carousel (same size, JPEG only)
    caption.txt                      caption (max 2,200 characters, 30 hashtags)
state/<account>.json                 what has been posted (written automatically)
generator/<account>/                 brand templates and scripts that make the images
scripts/publish.py                   the poster
scripts/tokens.py                    checks / refreshes access tokens
.github/workflows/                   the schedules
```

Rules the poster follows:
- One post per time slot. If GitHub can't run within 2 hours of a slot, that slot is skipped (no bursts of late posts).
- If the token is broken, nothing is used up; the run fails and GitHub emails you.
- A post that fails 3 times is marked failed in `state/` and skipped.
- Instagram allows at most 100 API posts per account per 24 hours.

## Secrets (Settings > Secrets and variables > Actions)

| Secret | What it is |
|---|---|
| `IG_TOKEN_FIN_ANCE18` | Instagram access token for @fin.ance18 |
| `SECRETS_PAT` | GitHub fine-grained token with **Secrets: read and write** on this repo, so tokens can renew themselves every Monday |

## Manual controls (Actions tab)

- **Publish posts > Run workflow**: `dry-run` shows what would post next, `post-now` posts the next item immediately.
- **Instagram tokens > Run workflow**: `check` tests every token, `refresh` renews them.

## Adding another Instagram account

1. Generate a token for the new account in the same Meta app (it needs to be a Professional account).
2. Add it as a secret, e.g. `IG_TOKEN_MY_NEW_PAGE`.
3. Add an entry to `accounts.json`:
   ```json
   {"id": "my.new.page", "token_secret": "IG_TOKEN_MY_NEW_PAGE",
    "timezone": "America/New_York", "slots": ["08:00", "12:00", "19:00"], "enabled": true}
   ```
4. Put its posts in `content/my.new.page/queue/`.

Set `"enabled": false` to pause an account.
