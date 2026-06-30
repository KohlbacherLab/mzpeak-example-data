#!/usr/bin/env python3
"""Download a dataset from its <id>.json description.

Each dataset is described by one JSON (see data/<tile>/<id>/<id>.json):

    {
      "id":          "PXD000155",                 # dataset id == its folder name
      "tile":        "general-ms",                # which tile it belongs to
      "title":       "Thermo LTQ Velos",          # short label
      "description": "...",                        # one sentence
      "files": [                                   # every file to retrieve
        { "url":   "https://.../run.raw",          #   FTP or HTTP, must download the file
          "path":  "run.raw",                      #   where it goes under the dataset folder
          "bytes": 16809984,                       #   optional: verified after download
          "unpack":"zip" }                         #   optional: unzip in place, then drop the zip
      ],
      "convert": { "input": "auto",                # optional: converter hints (not used here)
                   "flags": "--via-msconvert" }
    }

This script creates  <repo>/data/<tile>/<id>/  and fetches every file into it.
It is IDEMPOTENT: a file already present with the right size (or non-empty, when no
size is given) is skipped, so re-running only fetches what is missing.

Usage:
    scripts/fetch-dataset.py <id>.json [<id>.json ...]   # specific dataset(s)
    scripts/fetch-dataset.py --all                       # every data/*/*/*.json
    scripts/fetch-dataset.py --id PXD000155              # find one by id
Requires: curl (and unzip for "unpack":"zip" entries).
"""
import json, os, sys, glob, subprocess, shutil

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "data")


def _size(p):
    return os.path.getsize(p) if os.path.isfile(p) else -1


def _curl(url, target):
    # MassIVE's download endpoint does not support HTTP range/resume; everything else may resume.
    resume = [] if "DownloadResultFile" in url else ["-C", "-"]
    cmd = ["curl", "-fL", "--retry", "5", "--retry-delay", "3", *resume, "-o", target, url]
    rc = subprocess.run(cmd).returncode
    # 33/36 = server refused the resume offset but the local file is already complete.
    if rc in (33, 36) and _size(target) > 0:
        rc = 0
    return rc


def fetch_one(jpath):
    d = json.load(open(jpath))
    tile, ident = d["tile"], d["id"]
    dest = os.path.join(DATA, tile, ident)
    os.makedirs(dest, exist_ok=True)

    # keep a copy of the description alongside the data, so the folder is self-contained
    canon = os.path.join(dest, f"{ident}.json")
    if os.path.abspath(jpath) != os.path.abspath(canon):
        shutil.copy(jpath, canon)

    files = d.get("files", [])
    if not files:
        print(f"[{ident}] description-only (no files listed) — nothing to download")
        return 0

    got = skipped = failed = 0
    for f in files:
        url, rel = f["url"], f["path"]
        target = os.path.join(dest, rel)
        want = f.get("bytes")
        unpack = f.get("unpack")
        marker = target + ".extracted"          # idempotency marker for unpacked archives

        if unpack:
            if os.path.exists(marker):
                skipped += 1
                continue
        elif os.path.isfile(target) and (
            (want is None and _size(target) > 0) or (want is not None and _size(target) == want)
        ):
            skipped += 1
            continue

        os.makedirs(os.path.dirname(target) or dest, exist_ok=True)
        print(f"[{ident}] fetch {rel}")
        if _curl(url, target) != 0:
            print(f"[{ident}] FAIL {rel}")
            failed += 1
            if os.path.isfile(target) and _size(target) == 0:
                os.remove(target)
            continue
        if want is not None and _size(target) != want:
            print(f"[{ident}] WARN {rel}: got {_size(target)} bytes, expected {want}")

        if unpack == "zip":
            subprocess.run(["unzip", "-o", "-q", target, "-d", dest])
            os.remove(target)
            open(marker, "w").close()
        got += 1

    print(f"[{ident}] downloaded={got} skipped={skipped} failed={failed}  ->  {dest}")
    return 1 if failed else 0


def collect(args):
    if "--all" in args:
        return sorted(glob.glob(os.path.join(DATA, "*", "*", "*.json")))
    if "--id" in args:
        wid = args[args.index("--id") + 1]
        hits = [p for p in glob.glob(os.path.join(DATA, "*", "*", "*.json"))
                if json.load(open(p)).get("id") == wid]
        if not hits:
            sys.exit(f"no dataset json with id {wid}")
        return hits
    paths = [a for a in args if a.endswith(".json")]
    if not paths:
        sys.exit(__doc__)
    return paths


def main(argv):
    rc = 0
    for j in collect(argv):
        rc |= fetch_one(j)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
