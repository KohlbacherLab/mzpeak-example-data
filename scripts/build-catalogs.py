#!/usr/bin/env python3
"""Generate every data/<tile>/_catalog.md from the YAML descriptors.

  data/<tile>/_tile.yaml      -> the tile header (frontmatter + blurb + provenance)
  data/<tile>/<id>/<id>.yaml  -> one "### <id>" + description per dataset

`_catalog.md` is the GENERATED file that make-s3-index.py consumes -- never hand-edit it; edit the
YAML and re-run this (or scripts/update.sh). Existing dataset order is preserved; datasets with a
new descriptor are appended (sorted).

Usage:  python3 scripts/build-catalogs.py
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus_lib as C


def main():
    for tile in C.tiles():
        t = C.load(C.tile_descriptor(tile))
        front = ("---\n"
                 f"slug: {t['slug']}\n"
                 f"title: {t['title']}\n"
                 f"icon: {t['icon']}\n"
                 f"accent: {t['accent']}\n"
                 f"imaging: {'true' if t.get('imaging') else 'false'}\n"
                 f"order: {t['order']}\n"
                 "---")
        cat = os.path.join(C.DATA, tile, "_catalog.md")
        prev = re.findall(r"^###\s+(.+?)\s*$",
                          open(cat).read().partition("\n## datasets")[2], re.M) if os.path.exists(cat) else []
        ds = {}
        for p in C.dataset_descriptors(tile):
            d = C.load_dataset(p); ds[d["id"]] = d
        order = [i for i in prev if i in ds] + sorted(i for i in ds if i not in prev)

        blocks = []
        for i in order:
            d = ds[i]
            desc = (d.get("description") or "").strip() or f"{d.get('title', i)}."
            blocks.append(f"### {i}\n{desc}")

        body = (t.get("blurb", "").strip() + "\n\n" + t.get("provenance", "").strip()).strip()
        open(cat, "w").write(f"{front}\n\n{body}\n\n## datasets\n\n" + "\n\n".join(blocks) + "\n")
        print(f"  {tile:20} {len(blocks)} datasets")


if __name__ == "__main__":
    main()
