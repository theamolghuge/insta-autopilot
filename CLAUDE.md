# Instagram Autopilot: notes for Claude

This repo auto-publishes Instagram posts for one or more accounts via GitHub Actions.
Read `README.md` (how it runs) and `HOW_TO.md` (common jobs) first.

## When asked to "make next week's posts" for an account
1. Read `brand/<account>/BRAND.md` for voice, visuals and content rules.
2. Copy the latest `generator/<account>/batch_NNN.py` to the next number and write fresh content.
   Do not repeat topics/quotes from earlier batches (grep the earlier batch files).
   Set `START` to the next free queue number (`ls content/<account>/queue | tail -1`).
3. Compute every money figure in code; check yearly limits against irs.gov.
4. Run it, then `python scripts/preview.py <account>` and look at the sheet before committing.
5. Check `python scripts/publish.py --dry-run --account <account>` works.
6. Commit and push to `main`. GitHub Actions picks it up automatically.

## Rules
- Never put access tokens in files, commits or chat. They live only in GitHub secrets.
- Never edit `state/*.json` by hand unless asked; the workflow owns it.
- Don't renumber or delete queue folders that are already listed as posted in `state/`.
- Images: JPEG, same size within a carousel, 2-10 images per carousel.
