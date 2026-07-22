#!/usr/bin/env python3
"""Convert a dataset's raw input to mzPeak, writing <unit>.mzpeak NEXT TO the input. Idempotent.

For each dataset it finds the input unit in data/<tile>/<id>/ -- the descriptor's `convert.input`,
or 'auto' = the first raw unit (.mzML/.imzML/.raw/.d/.wiff/.lcd/.baf) -- and runs mzpeak-convert.
Skips when: the descriptor says `convert.skip: true`, there is no convertible unit (e.g. a kept
.zip or an SDRF .tsv), or the .mzpeak already exists AND was made with the same conversion recipe.
The recipe (input + flags + any convert.* key) is hashed into a `<unit>.mzpeak.sig` stamp; change a
conversion param and the next run reconverts (make-style), while title/description/url edits do not.
Extra flags come from `convert.flags`.

mzpeak-convert is located via $MZPEAK_CONVERT, then PATH, then a local .build/ or a sibling
mzPeakConverter checkout. If none is found, conversion is skipped with a note (not an error).

Usage:  scripts/convert-dataset.py <id>.yaml [...]  |  --all  |  --id <ID>
"""
import os, sys, glob, subprocess, json, hashlib, shlex, time, datetime, platform
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus_lib as C

RAW_GLOBS = ("*.mzML", "*.imzML", "*.raw", "*.RAW", "*.d", "*.wiff", "*.lcd", "*.baf")


def _dsize(p):                                           # bytes of a unit (dir sums, file direct)
    if os.path.isdir(p):
        return sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(p) for f in fs)
    return os.path.getsize(p) if os.path.exists(p) else 0


_CVER = None
def _cver(conv):
    global _CVER
    if _CVER is None:
        try: _CVER = subprocess.run([conv, "--version"], capture_output=True, text=True).stdout.strip() or "?"
        except Exception: _CVER = "?"
    return _CVER


def _bench(row):                                         # append one wall-clock record to the bench TSV
    bp = os.path.join(C.REPO, "out", "bench", "convert-times.tsv")
    os.makedirs(os.path.dirname(bp), exist_ok=True)
    new = not os.path.exists(bp)
    with open(bp, "a") as f:
        if new: f.write("iso_time\tid\ttile\tunit\tconverter\tflags\traw_bytes\tmzpeak_bytes\tseconds\thost\n")
        f.write("\t".join(str(x) for x in row) + "\n")


def _sig(cv):
    """Signature of the conversion RECIPE (input + flags + skip + any convert.* key).
    Changing conversion params changes this; editing title/description/urls does not."""
    return hashlib.sha256(json.dumps(cv, sort_keys=True).encode()).hexdigest()[:16]


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
    d = C.load_dataset(dpath)
    cv = d.get("convert") or {}
    if cv.get("skip"):
        return 0
    dd = os.path.join(C.DATA, d["tile"], d["id"])
    unit = find_unit(dd, cv.get("input", "auto"))
    if not unit:
        return 0                                         # nothing convertible here
    out = os.path.splitext(unit)[0] + ".mzpeak"
    sigf, sig = out + ".sig", _sig(cv)
    if os.path.exists(out):
        old = open(sigf).read().strip() if os.path.exists(sigf) else None
        if old == sig:
            print(f"[{d['id']}] have {os.path.basename(out)} (params unchanged, skip)"); return 0
        if old is None:                                  # legacy .mzpeak with no stamp: adopt, don't mass-reconvert
            open(sigf, "w").write(sig)
            print(f"[{d['id']}] have {os.path.basename(out)} (stamped existing, skip)"); return 0
        print(f"[{d['id']}] params changed ({old}->{sig}) — reconverting")
    if not conv:
        print(f"[{d['id']}] mzpeak-convert not found — set $MZPEAK_CONVERT; skipping"); return 0
    flags = shlex.split(cv.get("flags") or "")   # shlex: quoted paths with spaces stay one arg
    print(f"[{d['id']}] convert {os.path.basename(unit)}")
    t0 = time.time()
    rc = subprocess.run([conv, unit, "-o", out, "--force", *flags]).returncode
    dt = round(time.time() - t0, 1)
    if rc == 0:
        open(sigf, "w").write(sig)
        _bench([datetime.datetime.now().isoformat(timespec="seconds"), d["id"], d["tile"],
                os.path.basename(unit), _cver(conv), cv.get("flags") or "", _dsize(unit),
                os.path.getsize(out) if os.path.exists(out) else 0, dt, platform.node()])
        print(f"[{d['id']}] wrote {os.path.basename(out)} ({dt}s)")
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
