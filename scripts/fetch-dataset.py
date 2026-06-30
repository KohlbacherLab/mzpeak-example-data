#!/usr/bin/env python3
"""Download a dataset's files from its descriptor (data/<tile>/<id>/<id>.yaml).

Creates  data/<tile>/<id>/  and fetches every entry in `files` into it. IDEMPOTENT: a file already
present at the right size (or non-empty, when no size is given) is skipped, so re-running only
fetches what's missing. Handles FTP/HTTP, MassIVE (no resume), and "unpack: zip".

Usage:
    scripts/fetch-dataset.py <id>.yaml [...]   # specific descriptor(s)
    scripts/fetch-dataset.py --all             # every dataset
    scripts/fetch-dataset.py --id PXD000155
Requires: curl (and unzip for "unpack: zip" entries).
"""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus_lib as C


def _size(p):
    return os.path.getsize(p) if os.path.isfile(p) else -1


def _curl(url, target):
    resume = [] if "DownloadResultFile" in url else ["-C", "-"]   # MassIVE has no range/resume
    rc = subprocess.run(["curl", "-fL", "--retry", "5", "--retry-delay", "3", *resume,
                         "-o", target, url]).returncode
    if rc in (33, 36) and _size(target) > 0:   # resume refused but file already complete
        rc = 0
    return rc


def fetch_one(dpath):
    d = C.load(dpath)
    dest = os.path.join(C.DATA, d["tile"], d["id"])
    os.makedirs(dest, exist_ok=True)
    files = d.get("files") or []
    if not files:
        print(f"[{d['id']}] description-only (no files) — nothing to download")
        return 0
    got = skipped = failed = 0
    for f in files:
        url, rel, want, unpack = f["url"], f["path"], f.get("bytes"), f.get("unpack")
        target = os.path.join(dest, rel)
        if not os.path.abspath(target).startswith(os.path.abspath(dest) + os.sep):
            print(f"[{d['id']}] unsafe path {rel!r} — skipped"); failed += 1; continue
        marker = target + ".extracted"
        if unpack and os.path.exists(marker):
            skipped += 1; continue
        if not unpack and os.path.isfile(target) and (
                (want is None and _size(target) > 0) or (want is not None and _size(target) == want)):
            skipped += 1; continue
        os.makedirs(os.path.dirname(target) or dest, exist_ok=True)
        print(f"[{d['id']}] fetch {rel}")
        if _curl(url, target) != 0:
            print(f"[{d['id']}] FAIL {rel}"); failed += 1
            if _size(target) == 0 and os.path.isfile(target): os.remove(target)
            continue
        if want is not None and _size(target) != want:
            print(f"[{d['id']}] WARN {rel}: got {_size(target)} expected {want}")
        if unpack == "zip":
            subprocess.run(["unzip", "-o", "-q", target, "-d", dest])
            os.remove(target); open(marker, "w").close()
        got += 1
    print(f"[{d['id']}] downloaded={got} skipped={skipped} failed={failed}  ->  {dest}")
    return 1 if failed else 0


def main(argv):
    rc = 0
    for p in C.resolve(argv):
        rc |= fetch_one(p)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
