#!/usr/bin/env python3
"""Print the next free queue number for an account, e.g. `python scripts/next_number.py fin.ance18` -> 64.

Posted folders are deleted by the daily cleanup, so `ls content/<account>/queue | tail -1` is NOT enough:
this also counts every name in state/<account>.json (posted, failed, attempts). Never reuse a number,
or the publisher may think a new post already went out.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def next_number(acc):
    names = []
    q = ROOT / "content" / acc / "queue"
    if q.exists():
        names += [p.name for p in q.iterdir() if p.is_dir()]
    sp = ROOT / "state" / f"{acc}.json"
    if sp.exists():
        st = json.loads(sp.read_text())
        for k in ("posted", "failed", "attempts"):
            names += list(st.get(k, {}))
    nums = [int(m.group(1)) for n in names if (m := re.match(r"(\d{4})-", n))]
    return max(nums, default=0) + 1


if __name__ == "__main__":
    print(next_number(sys.argv[1] if len(sys.argv) > 1 else "fin.ance18"))
