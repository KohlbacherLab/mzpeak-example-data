# HOW TO ADD / REMOVE A DATASET

Practical guide to the mzpeak-example-data corpus: where things live, and the exact edits to
add a dataset to a tile, wire up its on-demand download, write its description, and remove it.

---

## 0. The two locations (important)

The project is split across **two directories**:

| What | Where | In git? |
|---|---|---|
| Scripts, manifests, per-tile download recipes | **`~/Claude/mzpeak-example-data/`** (the git repo) | ✅ yes |
| `<tile>/_catalog.md` (tile + dataset descriptions) **and the actual data/`.mzpeak`** | **`~/Claude/mzPeak/data/`** (the *working corpus*, `CATALOG_ROOT`) | ❌ no |
| Published site + data objects | **`s3://v09/<tile>/...`** (StackIT object store) | ❌ no |

So a dataset is described by edits in **both** trees, and its bytes live on **S3**.

### The 6 FIXED tiles

A directory is a tile **only** if it has a `<tile>/_catalog.md`. The tiles are fixed; don't invent new ones without reason.

| Tile dir | slug | download mechanism |
|---|---|---|
| `general-ms` | `general-ms` | open mzML → `scripts/fetch-examples.sh` · vendor raw → `manifest/general-ms-files.tsv` + `scripts/fetch-general-ms.sh` |
| `ims-examples` | `ims` | `manifest/ims-files.tsv` + `scripts/fetch-ims.sh` |
| `imzml-examples` | `imaging` | `scripts/fetch-examples.sh` |
| `sdrf-examples` | `sdrf` | `scripts/fetch-examples.sh` |
| `tof-grid-examples` | `tof-grid` | `manifest/datasets.tsv` + `build_data.sh` (`vendor_tile`) |
| `pwiz-examples` | `pwiz-tests` | `scripts/fetch-examples.sh` + `manifest/pwiz-files.txt` |

### How the site decides what to show

`scripts/make-s3-index.py` builds the site **from the live S3 bucket listing**:

- A **dataset appears on a tile because its files exist on S3** under `s3://v09/<tile>/<dataset-dir>/`.
- The matching `### <dataset-dir>` block in `<tile>/_catalog.md` only supplies its **description**.
  No catalog entry ⇒ the dataset still shows, just with no description text.
- A **tile appears only if `s3://v09/<tile>/_catalog.md` exists** (the allowlist gate).

**The only supported way to (re)generate and publish the site is `scripts/build-corpus-site.sh`.**
It uploads the `_catalog.md` markers, lists the bucket, runs `make-s3-index.py` + `make-ratio-plots.py`,
deploys, and prunes stale pages. Do **not** edit that script, `make-s3-index.py`, or `make-ratio-plots.py`,
and never publish the site any other way.

---

## (a) Add a dataset to a specific tile

A dataset directory name (e.g. `PXD012345` or `thermo-astral`) is used **identically** in three places:
the local dir, the S3 prefix, and the `### <name>` catalog block. Keep them the same.

1. **Get the bytes onto S3** under `s3://v09/<tile>/<dataset-dir>/...`:
   - Download locally first (see (b)), into `data/<tile>/<dataset-dir>/` (repo) or
     `~/Claude/mzPeak/data/<tile>/<dataset-dir>/` (corpus), then upload:
     ```sh
     export AWS_PROFILE=stackit
     EP=https://object.storage.eu01.onstackit.cloud
     aws --endpoint-url "$EP" s3 cp <localdir>/<tile>/<dataset-dir> \
         s3://v09/<tile>/<dataset-dir> --recursive
     ```
   - Converted `.mzpeak` for the open tiles can also be pushed via `scripts/sync-s3.sh`.
2. **Describe it** — see (c).
3. **Publish:** `bash scripts/build-corpus-site.sh`

---

## (b) Wire up on-demand download — where the URL goes

Depends on the tile's mechanism (table above). Put the URL in the matching source:

### Open-format example (mzML/imzML/sdrf) — `scripts/fetch-examples.sh`
Add a `dl` line inside that tile's `fetch_*` function. Path is relative to `data/<tile>/`:
```sh
dl "https://…/run.mzML"  "<dataset-dir>/run.mzML"
# MassIVE has no range/resume — add the 3rd arg:
dl "$M?file=f.MSV…/peak/run.mzML&forceDownload=true"  "<dataset-dir>/run.mzML" --no-resume
```

### `general-ms` vendor raw — `manifest/general-ms-files.tsv` (read by `fetch-general-ms.sh`)
TAB-separated; `;`-join multi-file units (e.g. `.wiff`+`.wiff.scan`). Downloads into `data/general-ms/<accession>/`:
```
accession<TAB>repo<TAB>vendor<TAB>unit<TAB>expected_bytes<TAB>url1;url2
```

### `ims-examples` raw — `manifest/ims-files.tsv` (read by `fetch-ims.sh`)
One raw per study; downloads into `~/Claude/mzPeak/data/ims-examples/<accession>/`:
```
accession<TAB>repo<TAB>vendor<TAB>im_type<TAB>expected_bytes<TAB>url
```

### `tof-grid-examples` vendor raw — `manifest/datasets.tsv` (read by `build_data.sh` `vendor_tile`)
Downloads into `data/<tile>/<dir>/`, then converts:
```
tile<TAB>dir<TAB>accession<TAB>repo<TAB>files(;-sep | "-")<TAB>unpack(zip|none)<TAB>convert_input(path|auto)<TAB>flags<TAB>notes
```
`files="-"` ⇒ no stable URL; the build prints the dataset page to fetch manually.

### `pwiz-examples`
Add the path to `manifest/pwiz-files.txt` (fetched from the public ProteoWizard mirror by `fetch-examples.sh`).

After editing, fetch to verify the URL works:
```sh
bash scripts/fetch-examples.sh <tile>        # open-format tiles
bash scripts/fetch-general-ms.sh             # general-ms vendor raw
bash scripts/fetch-ims.sh                    # ims raw
./build_data.sh tof-grid-examples            # tof-grid (fetch + convert)
```

---

## (c) Descriptions — dataset and tile (both in `_catalog.md`)

Edit **`~/Claude/mzPeak/data/<tile>/_catalog.md`**. Structure:

```markdown
---
slug: <url-slug>            # the .html page name; keep unique
title: <Tile Title>
icon: 📈                    # emoji shown on the card
accent: #1558d6             # hex; tile + ratio-figure colour
imaging: false              # true only for the imaging tile
order: 1                    # sort position on the landing page
---

<one-paragraph TILE blurb shown on the card>

<b>Provenance.</b> <one-paragraph provenance: archives, accessions, vendor/analyzer span>

## datasets

### <dataset-dir>          # MUST equal the S3 prefix s3://v09/<tile>/<dataset-dir>/
<one-paragraph DATASET description: repo · instrument — modality, format, citation>
```

- **Tile description** = the frontmatter + blurb + `<b>Provenance.</b>` paragraph.
- **Dataset description** = a `### <dataset-dir>` heading + the paragraph under it.
- The `### <dataset-dir>` name must match the S3 prefix exactly, or the description won't attach.

(A brand-new tile would also need a frontmatter `accent` and a matching key in `make-ratio-plots.py`'s
`ACCENT` dict for its figure colour — but tiles are fixed, so normally you only add datasets.)

---

## Remove a dataset

1. **S3 data:** `aws --endpoint-url "$EP" s3 rm s3://v09/<tile>/<dataset-dir> --recursive`
2. **Description:** delete the `### <dataset-dir>` block from `~/Claude/mzPeak/data/<tile>/_catalog.md`.
3. **Download recipe:** delete its line/row from the relevant source —
   `fetch-examples.sh` `dl` line, or the `manifest/*-files.tsv` / `datasets.tsv` / `pwiz-files.txt` row.
4. **Local copies (optional):** `rm -rf` it from `data/<tile>/<dataset-dir>` and/or `~/Claude/mzPeak/data/<tile>/<dataset-dir>`.
5. **Publish:** `bash scripts/build-corpus-site.sh` — it re-lists the bucket and auto-prunes stale pages.

To remove an entire **tile**, also delete its `s3://v09/<tile>/_catalog.md` marker (the builder then drops it from the allowlist).

---

## One-line recap

> **Bytes on S3** make a dataset *appear*; **`_catalog.md`** makes it *described*; the **fetch source**
> (`fetch-examples.sh` / `manifest/*.tsv` / `pwiz-files.txt`) makes it *rebuildable*; and
> **`build-corpus-site.sh`** is the *only* thing that publishes any of it.
