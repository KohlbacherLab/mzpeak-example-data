#!/usr/bin/env python3
"""Rebuild every data/<tile>/_catalog.md datasets section from the per-dataset <id>.json files.

The per-dataset JSONs (data/<tile>/<id>/<id>.json) are the single source of truth for dataset
titles and descriptions. This script regenerates the "## datasets" section of each tile catalog
from them:  one  "### <id>"  heading + the json's description, per dataset.

The tile header -- everything ABOVE "## datasets" (frontmatter + blurb + provenance) -- is kept
verbatim; only the dataset list is regenerated. Existing dataset order is preserved; datasets that
have a json but no current entry are appended (sorted), so adding a dataset is just: drop a json,
run this, run build-corpus-site.sh.

Usage:  python3 scripts/build-catalogs.py
"""
import json, os, glob, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "data")


def main():
    for cat in sorted(glob.glob(os.path.join(DATA, "*", "_catalog.md"))):
        tile = os.path.basename(os.path.dirname(cat))
        text = open(cat).read()
        header = text.partition("\n## datasets")[0].rstrip("\n")
        prev = re.findall(r"^###\s+(.+?)\s*$", text.partition("\n## datasets")[2], re.M)

        js = {}
        for jp in glob.glob(os.path.join(DATA, tile, "*", "*.json")):
            d = json.load(open(jp))
            js[d["id"]] = d

        order = [i for i in prev if i in js] + sorted(i for i in js if i not in prev)
        blocks = []
        for i in order:
            d = js[i]
            desc = (d.get("description") or "").strip() or f"{d.get('title', i)}."
            blocks.append(f"### {i}\n{desc}")

        open(cat, "w").write(header + "\n\n## datasets\n\n" + "\n\n".join(blocks) + "\n")
        added = len([i for i in order if i not in prev])
        print(f"  {tile:20} {len(blocks)} datasets ({added} added)")


if __name__ == "__main__":
    main()
