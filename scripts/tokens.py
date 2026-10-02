#!/usr/bin/env python3
"""Check or refresh the Instagram access token of every account.

  python scripts/tokens.py check     -> confirms each token works and shows the username
  python scripts/tokens.py refresh   -> extends each token by 60 days and saves it back
                                        to the repository secret (needs SECRETS_PAT)

Long-lived Instagram tokens last 60 days. A token must be at least 24 hours old
to be refreshed, and an expired token cannot be refreshed: a new one has to be
generated in the Meta app dashboard.
"""
import json, os, subprocess, sys, urllib.parse, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API_BASE = os.environ.get("IG_API_BASE", "https://graph.instagram.com")
sys.path.insert(0, str(ROOT / "scripts"))
from publish import get_token, summary  # noqa: E402


def get(url):
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode(errors='replace')}") from None


def main(mode):
    cfg = json.loads((ROOT / "accounts.json").read_text())
    ver = cfg.get("api_version", "v23.0")
    ok = True
    summary(f"| Account | Token {mode} |\n|---|---|")
    for acc in cfg["accounts"]:
        if not acc.get("enabled", True):
            continue
        name, token = acc["token_secret"], get_token(acc["token_secret"])
        if not token:
            print(f"[{acc['id']}] secret {name} is missing"); summary(f"| {acc['id']} | missing secret {name} |"); ok = False
            continue
        try:
            if mode == "check":
                me = get(f"{API_BASE}/{ver}/me?" + urllib.parse.urlencode(
                    {"fields": "user_id,username,account_type", "access_token": token}))
                print(f"[{acc['id']}] OK: @{me.get('username')} ({me.get('account_type')}), user_id {me.get('user_id')}")
                summary(f"| {acc['id']} | OK, @{me.get('username')} |")
            else:
                r = get(f"{API_BASE}/refresh_access_token?" + urllib.parse.urlencode(
                    {"grant_type": "ig_refresh_token", "access_token": token}))
                new, days = r["access_token"], int(r.get("expires_in", 0)) // 86400
                pat = os.environ.get("SECRETS_PAT")
                if pat and os.environ.get("GITHUB_REPOSITORY"):
                    subprocess.run(["gh", "secret", "set", name, "--repo", os.environ["GITHUB_REPOSITORY"]],
                                   input=new.encode(), check=True, env={**os.environ, "GH_TOKEN": pat})
                    print(f"[{acc['id']}] refreshed, valid for {days} more days, secret {name} updated")
                    summary(f"| {acc['id']} | refreshed, {days} days left |")
                else:
                    print(f"[{acc['id']}] refreshed for {days} days, but SECRETS_PAT is not set so the secret was NOT updated")
                    summary(f"| {acc['id']} | refreshed but not saved (no SECRETS_PAT) |")
        except Exception as e:
            ok = False
            print(f"[{acc['id']}] ERROR: {e}")
            print(f"[{acc['id']}] key starts with {token[:4]!r}, length {len(token)}")
            summary(f"| {acc['id']} | ERROR, see log |")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "check")
