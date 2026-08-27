#!/usr/bin/env python3
"""Table of contents for the corpus: every file and the S3 URL it lives at.

Emits `out/toc/CONTENTS.md` (browsable) and `out/toc/contents.csv` (machine-readable), one row per
LEAF FILE -- never per "unit", because a Bruker/Agilent `.d`, a Waters `.raw` and an
`.imzML`+`.ibd` pair are directories/sets that `s3 sync` uploads member by member.

Rows are the UNION of four views, reconciled, because no single one is truthful:

  declared   the descriptor's `files:` list          -- what the corpus says it is made of
  local      what is actually on disk                -- includes conversion output and by-products
  generated  `<convert.input>.mzpeak`                -- never declared, but it is the whole point
  bucket     a live `list-objects-v2`                -- the only authority on what is PUBLISHED

`status` names the disagreement (PUBLISHED / LOCAL_ONLY / DECLARED_ONLY / ORPHAN / SIZE_MISMATCH /
UNRESOLVED) rather than hiding it, and `published_by` records WHICH publisher would upload the file,
since the three disagree on membership:

  sync-s3.sh           only `*.mzpeak`, and only in the 5 publishable tiles (pwiz-examples excluded)
  update.sh            everything except *.yaml/*.yml/*.json/*.extracted/*.sig, no tile filter
  build-corpus-site.sh `_catalog.md` for all 6 tiles

The address transform itself is shared with the conversion and sync paths via
`corpus_lib.s3_key/s3_uri/public_url`, so a TOC entry and an upload can never disagree.

Usage:
    scripts/make-toc.py [--all | --id X | <descriptor>...]
                        [--out DIR] [--format md,csv] [--no-bucket] [--listing FILE] [--strict]
Env: BUCKET=v09  ENDPOINT=...  AWS_PROFILE=stackit
"""
import argparse
import csv
import glob
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus_lib as C  # noqa: E402

# Mirrors update.sh's --exclude list: these never reach the bucket.
NEVER_UPLOADED = (".yaml", ".yml", ".json", ".extracted", ".sig")
# sync-s3.sh TILES (:24) -- pwiz-examples is deliberately absent (kept local).
SYNC_TILES = {"imzml-examples", "general-ms", "sdrf-examples", "ims-examples", "tof-grid-examples"}
# Local droppings that are not corpus content but DO get swept up by update.sh's sync.
BYPRODUCT_SUFFIXES = (".mzpeak.built", ".mzpeak.partial", ".log")


def human(n):
    if n is None:
        return ""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return "%.0f %s" % (n, unit) if unit == "B" else "%.1f %s" % (n, unit)
        n /= 1024.0


def publishers(tile, rel):
    """Which script(s) would upload this file. Empty => nothing publishes it."""
    who = []
    base = os.path.basename(rel)
    if base == "_catalog.md":
        return ["build-corpus-site"]
    if any(base.endswith(x) for x in NEVER_UPLOADED):
        return []
    if rel.endswith(".mzpeak") and tile in SYNC_TILES:
        who.append("sync-s3")
    who.append("update")
    return who


def bucket_listing(use_bucket, listing_file):
    """-> {key: size}. Empty dict when the bucket is not consulted."""
    if listing_file:
        raw = json.load(open(listing_file))
    elif use_bucket:
        cmd = ["aws", "--profile", os.environ.get("AWS_PROFILE", "stackit"),
               "--endpoint-url", C.DEFAULT_ENDPOINT, "s3api", "list-objects-v2",
               "--bucket", C.DEFAULT_BUCKET, "--output", "json"]
        out = subprocess.run(cmd, capture_output=True, text=True)
        if out.returncode != 0:
            sys.stderr.write("warn: bucket listing failed (%s); continuing local-only\n"
                             % (out.stderr or "").strip()[:120])
            return {}
        raw = json.loads(out.stdout or "{}")
    else:
        return {}
    return {o["Key"]: int(o["Size"]) for o in (raw.get("Contents") or [])}


def collect(paths, bucket):
    rows, seen = [], {}

    def put(tile, ds, rel, kind, **kw):
        k = (tile, ds, rel)
        if k in seen:
            seen[k].update({x: v for x, v in kw.items() if v not in (None, "")})
            return seen[k]
        r = {"tile": tile, "id": ds, "rel_path": rel, "kind": kind,
             "bytes_declared": None, "bytes_local": None, "bytes_bucket": None,
             "source_url": "", "note": ""}
        r.update(kw)
        seen[k] = r
        rows.append(r)
        return r

    for p in paths:
        d = C.load_dataset(p)
        tile, ds = d["tile"], d["id"]
        dd = os.path.join(C.DATA, tile, ds)
        cv = d.get("convert") or {}

        for f in (d.get("files") or []):
            rel = str(f.get("path") or "").strip()
            if rel:
                put(tile, ds, rel, "declared",
                    bytes_declared=f.get("bytes"), source_url=str(f.get("url") or ""))

        for root, _, files in os.walk(dd):
            for fn in files:
                ap = os.path.join(root, fn)
                rel = os.path.relpath(ap, dd).replace(os.sep, "/")
                if fn.endswith(NEVER_UPLOADED) and not fn.endswith(".mzpeak.sig"):
                    continue
                kind = ("mzpeak" if rel.endswith(".mzpeak")
                        else "byproduct" if rel.endswith(BYPRODUCT_SUFFIXES)
                        else "declared")
                try:
                    put(tile, ds, rel, kind, bytes_local=os.path.getsize(ap))
                except OSError:
                    pass

        # The conversion output is never declared, but it is what the corpus publishes.
        if not cv.get("skip"):
            unit = find_unit(dd, cv.get("input", "auto"))
            if unit:
                rel = os.path.relpath(os.path.splitext(unit)[0] + ".mzpeak", dd).replace(os.sep, "/")
                put(tile, ds, rel, "mzpeak")
            elif cv:
                put(tile, ds, "<unresolved>.mzpeak", "mzpeak",
                    note="convert.input=%r does not resolve locally" % cv.get("input", "auto"))

    # Reconcile against the bucket, and surface objects nothing accounts for.
    known = {"%s/%s/%s" % (r["tile"], r["id"], r["rel_path"]) for r in rows}
    for r in rows:
        key = "%s/%s/%s" % (r["tile"], r["id"], r["rel_path"])
        if key in bucket:
            r["bytes_bucket"] = bucket[key]
    tiles = set(C.tiles())
    for key, size in sorted(bucket.items()):
        seg = key.split("/")
        if len(seg) < 3 or seg[0] not in tiles or key in known:
            continue
        rows.append({"tile": seg[0], "id": seg[1], "rel_path": "/".join(seg[2:]),
                     "kind": "orphan", "bytes_declared": None, "bytes_local": None,
                     "bytes_bucket": size, "source_url": "",
                     "note": "in bucket, no descriptor/local counterpart"})
    return rows


def find_unit(dd, spec):
    """Same resolution convert-dataset.py uses, kept in sync by import."""
    import importlib.util
    here = os.path.dirname(os.path.abspath(__file__))
    spec_ = importlib.util.spec_from_file_location("cvt", os.path.join(here, "convert-dataset.py"))
    mod = importlib.util.module_from_spec(spec_)
    argv = sys.argv
    sys.argv = ["x"]
    try:
        spec_.loader.exec_module(mod)
    except SystemExit:
        pass
    finally:
        sys.argv = argv
    return mod.find_unit(dd, spec)


def finish(rows):
    for r in rows:
        rel, tile = r["rel_path"], r["tile"]
        who = publishers(tile, rel)
        r["published_by"] = ";".join(who) or "none"
        local, buck, decl = r["bytes_local"], r["bytes_bucket"], r["bytes_declared"]
        if r["kind"] == "orphan":
            r["status"] = "ORPHAN"
        elif rel.startswith("<unresolved>"):
            r["status"] = "UNRESOLVED"
        elif buck is not None and local is not None and buck != local:
            r["status"] = "SIZE_MISMATCH"
        elif buck is not None:
            r["status"] = "PUBLISHED"
        elif local is not None:
            r["status"] = "LOCAL_ONLY"
        else:
            r["status"] = "DECLARED_ONLY"
        key = "%s/%s/%s" % (tile, r["id"], rel)
        r["s3_key"] = key
        r["s3_uri"] = "s3://%s/%s" % (C.DEFAULT_BUCKET, key)
        r["s3_url"] = C.public_url(os.path.join(C.DATA, tile, r["id"], *rel.split("/")))
        r["bytes"] = buck if buck is not None else (local if local is not None else decl)
    rows.sort(key=lambda r: (r["tile"], r["id"], r["rel_path"]))
    return rows


COLS = ["tile", "id", "rel_path", "kind", "status", "published_by",
        "bytes", "bytes_declared", "bytes_local", "bytes_bucket",
        "s3_key", "s3_uri", "s3_url", "source_url", "note"]


def write_csv(rows, path):
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def write_md(rows, path, consulted_bucket):
    from collections import Counter
    st = Counter(r["status"] for r in rows)
    total = sum(r["bytes"] or 0 for r in rows if r["status"] in ("PUBLISHED", "SIZE_MISMATCH"))
    L = []
    L.append("# mzPeak example corpus — table of contents\n")
    L.append("Every file in the corpus and the S3 address it is published at. Generated by "
             "`scripts/make-toc.py`; the address transform is `corpus_lib.s3_key`, the same one "
             "`sync-s3.sh` and `update.sh` use, so these URLs are the real ones.\n")
    L.append("- generated: `%s`" % datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))
    L.append("- bucket: `s3://%s` at `%s`%s" % (C.DEFAULT_BUCKET, C.DEFAULT_ENDPOINT,
             "" if consulted_bucket else "  _(not consulted — local view only)_"))
    L.append("- rows: **%d** across %d datasets · published bytes: **%s**\n"
             % (len(rows), len({(r["tile"], r["id"]) for r in rows}), human(total)))
    L.append("| status | meaning | n |")
    L.append("|---|---|---|")
    for s, m in (("PUBLISHED", "in the bucket, matches local"),
                 ("SIZE_MISMATCH", "in the bucket but a different size than local"),
                 ("LOCAL_ONLY", "on disk, not published"),
                 ("DECLARED_ONLY", "named by the descriptor, not downloaded"),
                 ("ORPHAN", "in the bucket with nothing accounting for it"),
                 ("UNRESOLVED", "output path unknown — `convert.input` does not resolve")):
        if st.get(s):
            L.append("| `%s` | %s | %d |" % (s, m, st[s]))
    L.append("")
    cur = None
    for r in rows:
        if (r["tile"], r["id"]) != cur:
            cur = (r["tile"], r["id"])
            L.append("\n## %s / %s\n" % cur)
            L.append("| file | kind | status | size | S3 URL |")
            L.append("|---|---|---|---|---|")
        L.append("| `%s` | %s | %s | %s | [`%s`](%s) |" % (
            r["rel_path"], r["kind"], r["status"], human(r["bytes"]), r["s3_key"], r["s3_url"]))
    open(path, "w").write("\n".join(L) + "\n")


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("selector", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--id")
    ap.add_argument("--out", default=os.path.join(C.REPO, "out", "toc"))
    ap.add_argument("--format", default="md,csv")
    ap.add_argument("--no-bucket", action="store_true")
    ap.add_argument("--listing")
    ap.add_argument("--strict", action="store_true",
                    help="exit 2 if any ORPHAN/SIZE_MISMATCH/UNRESOLVED row exists")
    a = ap.parse_args(argv)

    sel = list(a.selector)
    if a.all:
        sel.append("--all")
    if a.id:
        sel += ["--id", a.id]
    paths = C.resolve(sel or ["--all"])

    bucket = bucket_listing(not a.no_bucket, a.listing)
    rows = finish(collect(paths, bucket))
    os.makedirs(a.out, exist_ok=True)
    fmts = {f.strip() for f in a.format.split(",")}
    if "csv" in fmts:
        write_csv(rows, os.path.join(a.out, "contents.csv"))
    if "md" in fmts:
        write_md(rows, os.path.join(a.out, "CONTENTS.md"), bool(bucket))

    from collections import Counter
    st = Counter(r["status"] for r in rows)
    print("toc: %d rows -> %s" % (len(rows), a.out))
    for k in ("PUBLISHED", "SIZE_MISMATCH", "LOCAL_ONLY", "DECLARED_ONLY", "ORPHAN", "UNRESOLVED"):
        if st.get(k):
            print("  %-14s %d" % (k, st[k]))
    bad = st.get("ORPHAN", 0) + st.get("SIZE_MISMATCH", 0) + st.get("UNRESOLVED", 0)
    return 2 if (a.strict and bad) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
