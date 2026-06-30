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


def tiles():
    return sorted(os.path.basename(os.path.dirname(p))
                  for p in glob.glob(os.path.join(DATA, "*", "_tile.yaml")))


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
        hits = [p for p in dataset_descriptors() if load(p).get("id") == wid]
        if not hits:
            sys.exit(f"no dataset descriptor with id {wid}")
        return hits
    return [a for a in args if a.endswith((".yaml", ".yml", ".json"))]


if __name__ == "__main__":
    for p in resolve(sys.argv[1:]):
        d = load(p)
        print(f"{p}\t{d['tile']}\t{d['id']}")
