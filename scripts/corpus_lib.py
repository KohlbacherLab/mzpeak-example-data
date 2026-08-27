#!/usr/bin/env python3
"""Shared helpers for the YAML dataset-descriptor harness.

A dataset is one folder  data/<tile>/<id>/  holding a descriptor  <id>.yaml :

    id: PXD000155
    tile: general-ms
    title: Thermo LTQ Velos
    description: ...
    files:
      - {url: https://.../run.raw, path: run.raw, bytes: 16809984}
    convert: {flags: --via-msconvert}      # optional

A tile is one folder  data/<tile>/  with a  _tile.yaml  header (slug/title/icon/accent/...).

As a CLI this resolves a selector to descriptor paths (used by scripts/update.sh):
    python3 scripts/corpus_lib.py --all
    python3 scripts/corpus_lib.py --id PXD000155
    python3 scripts/corpus_lib.py data/general-ms/PXD000155/PXD000155.yaml
prints one  "<descriptor-path>\t<tile>\t<id>"  line per matched dataset.
"""
import os, sys, glob

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "data")


def load(path):
    """Load a descriptor (.yaml/.yml) or a legacy .json."""
    if path.endswith(".json"):
        import json
        return json.load(open(path))
    try:
        import yaml
    except ImportError:
        sys.exit("This needs PyYAML.  Install it:  pip install pyyaml")
    return yaml.safe_load(open(path))


def load_dataset(path):
    """Load a dataset descriptor and make the FOLDER authoritative: id and tile are taken from
    data/<tile>/<id>/, and any id:/tile: written in the file must match (else a clear error). So
    copying the template into the right folder is enough -- you can't silently mis-file a dataset."""
    d = load(path) or {}
    rel = os.path.relpath(os.path.abspath(path), DATA).split(os.sep)
    if len(rel) >= 3:                                    # data/<tile>/<id>/<file>
        for key, val in (("tile", rel[0]), ("id", rel[1])):
            if d.get(key) not in (None, "", val):
                sys.exit(f"{path}: '{key}: {d[key]}' does not match its folder '{val}' — "
                         f"rename the folder/file to the id, or fix the field.")
            d[key] = val
    return d


def tiles():
    return sorted(os.path.basename(os.path.dirname(p))
                  for p in glob.glob(os.path.join(DATA, "*", "_tile.yaml")))


# ── local path -> S3 mapping ────────────────────────────────────────────────────────────────────
# ONE definition of where a corpus file lands in the bucket. All three publishers agree on the
# prefix transform -- data/<tile>/<id>/<rel> -> <tile>/<id>/<rel> -- and differ only in WHICH files
# they upload (sync-s3.sh: *.mzpeak in 5 tiles; update.sh: everything bar *.yaml/*.yml/*.json/
# *.extracted/*.sig; build-corpus-site.sh: _catalog.md for all 6). Keep the transform here so a TOC,
# a conversion target and a sync can never disagree about an object's address.
DEFAULT_BUCKET = os.environ.get("BUCKET", "v09")
DEFAULT_ENDPOINT = os.environ.get("ENDPOINT", "https://object.storage.eu01.onstackit.cloud")


def s3_key(path):
    """data/<tile>/<id>/<rel> -> '<tile>/<id>/<rel>' (POSIX separators, no bucket)."""
    rel = os.path.relpath(os.path.abspath(path), DATA)
    if rel.startswith(os.pardir):
        raise ValueError("%s is outside %s" % (path, DATA))
    return rel.replace(os.sep, "/")


def s3_uri(path, bucket=None):
    return "s3://%s/%s" % (bucket or DEFAULT_BUCKET, s3_key(path))


def public_url(path, endpoint=None, bucket=None):
    """Browsable https URL. Percent-encoded: corpus paths contain spaces and parentheses."""
    try:
        from urllib.parse import quote
    except ImportError:                     # py2 safety net; the harness is py3 everywhere
        from urllib import quote
    ep = (endpoint or DEFAULT_ENDPOINT).rstrip("/")
    return "%s/%s/%s" % (ep, bucket or DEFAULT_BUCKET, quote(s3_key(path)))


def local_path(key):
    """Inverse of s3_key: '<tile>/<id>/<rel>' -> absolute local path under DATA."""
    return os.path.join(DATA, *key.split("/"))


def tile_descriptor(tile):
    return os.path.join(DATA, tile, "_tile.yaml")


def dataset_descriptors(tile="*"):
    """Every dataset descriptor (one per data/<tile>/<id>/ folder)."""
    out = []
    for ext in ("yaml", "yml", "json"):
        out += glob.glob(os.path.join(DATA, tile, "*", "*." + ext))
    return sorted(p for p in set(out) if os.path.basename(p) != "_tile.yaml")


def resolve(args):
    """Selector (--all | --id X | explicit descriptor paths) -> list of descriptor paths."""
    if not args or "--all" in args:
        return dataset_descriptors()
    if "--id" in args:
        wid = args[args.index("--id") + 1]
        hits = [p for p in dataset_descriptors() if load_dataset(p).get("id") == wid]
        if not hits:
            sys.exit(f"no dataset descriptor with id {wid}")
        return hits
    return [a for a in args if a.endswith((".yaml", ".yml", ".json"))]


if __name__ == "__main__":
    for p in resolve(sys.argv[1:]):
        d = load_dataset(p)
        print(f"{p}\t{d['tile']}\t{d['id']}")
