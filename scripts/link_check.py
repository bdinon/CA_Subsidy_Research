#!/usr/bin/env python3
"""
Checks every unique source_url in data/programs.json.

Statuses:
  ok          2xx, page looks real
  redirected  final URL points somewhere materially different
  soft_404    2xx but the page says not found / no longer available
  blocked     401/403/429/5xx or bot wall. NOT proof the page is dead, audit should open it
  dead        404/410 or the host does not resolve
  error       timeout or other failure

Usage:
  python scripts/link_check.py                 # check, write CSV only
  python scripts/link_check.py --apply         # also write link_status into programs.json
  python scripts/link_check.py --limit 20      # quick test
Standard library only. Takes a few minutes for ~750 URLs.
"""

import argparse
import csv
import json
import re
import socket
import threading
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
PROGRAMS_PATH = ROOT / "data" / "programs.json"
REVIEW_DIR = ROOT / "data" / "review"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
SOFT_404 = re.compile(r"page (was )?not found|404|no longer available|has been (removed|moved)|"
                      r"doesn.t exist|cannot be found|file not found", re.I)

host_locks = defaultdict(lambda: threading.Semaphore(2))


def norm(u):
    p = urlparse(u)
    host = p.netloc.lower().removeprefix("www.")
    return host, p.path.rstrip("/").lower()


def check(url, timeout=20):
    host = urlparse(url).netloc
    with host_locks[host]:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                code = resp.status
                final = resp.geturl()
                ctype = resp.headers.get("Content-Type", "")
                body = b""
                if "html" in ctype.lower():
                    body = resp.read(30000)
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                return "dead", e.code, url, f"HTTP {e.code}"
            return "blocked", e.code, url, f"HTTP {e.code}"
        except urllib.error.URLError as e:
            reason = str(e.reason)
            if isinstance(e.reason, socket.gaierror) or "Name or service" in reason or "getaddrinfo" in reason:
                return "dead", 0, url, "DNS failure"
            return "error", 0, url, reason[:120]
        except Exception as e:  # timeouts, resets, ssl
            return "error", 0, url, f"{type(e).__name__}: {str(e)[:100]}"

    if norm(final) != norm(url):
        old_h, old_p = norm(url)
        new_h, new_p = norm(final)
        # homepage dump or different host/path counts as a real redirect
        return "redirected", code, final, f"{old_h}{old_p} -> {new_h}{new_p}"[:200]
    if body:
        text = body.decode("utf-8", errors="ignore")
        m = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
        title = (m.group(1) if m else "").strip()
        if SOFT_404.search(title):
            return "soft_404", code, final, f"title: {title[:100]}"
    return "ok", code, final, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=12)
    args = ap.parse_args()

    programs = json.loads(PROGRAMS_PATH.read_text(encoding="utf-8"))
    urls = sorted({r["source_url"] for r in programs if r.get("source_url")})
    if args.limit:
        urls = urls[: args.limit]
    print(f"Checking {len(urls)} unique URLs with {args.workers} workers")

    results = {}
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for url, res in zip(urls, ex.map(check, urls)):
            results[url] = res

    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = REVIEW_DIR / f"link_check_{stamp}.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["url", "status", "http", "final_url", "detail"])
        for u, (st, code, final, detail) in results.items():
            w.writerow([u, st, code, final, detail])

    print("Results:", dict(Counter(v[0] for v in results.values())))
    print(f"Wrote {out}")

    if args.apply:
        n = 0
        for r in programs:
            res = results.get(r.get("source_url"))
            if res:
                r["link_status"] = res[0]
                n += 1
        PROGRAMS_PATH.write_text(json.dumps(programs, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Applied link_status to {n} records")
    else:
        print("Not applied. Re-run with --apply to write link_status into programs.json.")


if __name__ == "__main__":
    main()
