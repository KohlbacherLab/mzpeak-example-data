#!/usr/bin/env python3
"""Convert a dataset's raw input to mzPeak, writing <unit>.mzpeak NEXT TO the input. Idempotent.

For each dataset it finds the input unit in data/<tile>/<id>/ -- the descriptor's `convert.input`,
or 'auto' = the first raw unit (.mzML/.imzML/.raw/.d/.wiff/.lcd/.baf) -- and runs mzpeak-convert.
Skips when: the descriptor says `convert.skip: true`, there is no convertible unit (e.g. a kept
.zip or an SDRF .tsv), or the .mzpeak already exists. Extra flags come from `convert.flags`.

mzpeak-convert is located via $MZPEAK_CONVERT, then PATH, then a local .build/ or a sibling
mzPeakConverter checkout. If none is found, conversion is skipped with a note (not an error).

Usage:  scripts/convert-dataset.py <id>.yaml [...]  |  --all  |  --id <ID>
"""
import os, sys, glob, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus_lib as C

RAW_GLOBS = ("*.mzML", "*.imzML", "*.raw", "*.RAW", "*.d", "*.wiff", "*.lcd", "*.baf")


def converter():
    from shutil import which
    c = os.environ.get("MZPEAK_CONVERT")
    if c and os.path.exists(c): return c
    if which("mzpeak-convert"): return which("mzpeak-convert")
    for p in (os.path.join(C.REPO, ".build/mzPeakConverter/target/release/mzpeak-convert"),
              os.path.expanduser("~/Claude/mzPeak/mzPeakConverter/target/release/mzpeak-convert")):
        if os.path.exists(p): return p
    return None


def find_unit(dd, spec):
    if spec and spec != "auto":
        p = os.path.join(dd, spec)
        return p if os.path.exists(p) else None
    for g in RAW_GLOBS:                                  # prefer a shallow unit
        hits = sorted(glob.glob(os.path.join(dd, "**", g), recursive=True),
                      key=lambda h: (h.count(os.sep), h))
        if hits: return hits[0]
    return None


def convert_one(dpath, conv):
    d = C.load(dpath)
    cv = d.get("convert") or {}
    if cv.get("skip"):
        return 0
    dd = os.path.join(C.DATA, d["tile"], d["id"])
    unit = find_unit(dd, cv.get("input", "auto"))
    if not unit:
        return 0                                         # nothing convertible here
    out = os.path.splitext(unit)[0] + ".mzpeak"
    if os.path.exists(out):
        print(f"[{d['id']}] have {os.path.basename(out)} (skip)"); return 0
    if not conv:
        print(f"[{d['id']}] mzpeak-convert not found — set $MZPEAK_CONVERT; skipping"); return 0
    flags = (cv.get("flags") or "").split()
    print(f"[{d['id']}] convert {os.path.basename(unit)}")
    rc = subprocess.run([conv, unit, "-o", out, "--force", *flags]).returncode
    if rc == 0:
        print(f"[{d['id']}] wrote {os.path.basename(out)}")
    elif rc == 3:
        print(f"[{d['id']}] SKIP — unsupported on this platform (needs vendor reader / --via-msconvert)")
    else:
        print(f"[{d['id']}] convert FAILED rc={rc}"); return 1
    return 0


def main(argv):
    conv = converter()
    rc = 0
    for p in C.resolve(argv):
        rc |= convert_one(p, conv)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
