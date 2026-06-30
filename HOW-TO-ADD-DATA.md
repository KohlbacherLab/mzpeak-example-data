# HOW TO ADD / REMOVE A DATASET

Practical guide to the mzpeak-example-data corpus: where things live, and the exact edits to
add a dataset to a tile, wire up its on-demand download, write its description, and remove it.

All paths below are **relative to the repo root** (the directory containing `build_data.sh`).
The repo is self-contained — clone it and everything works; no machine-specific paths required.

---

## 0. Layout

This repo is **describe-don't-store**: it commits descriptions, manifests and scripts, never the
heavy data. The data is *reconstructed* by the scripts and *published* to an object store.

| What | Where | In git? |
|---|---|---|
| Scripts, manifests, download recipes | `scripts/`, `manifest/`, `build_data.sh` | ✅ |
| Per-tile spec: tile + dataset descriptions | `data/<tile>/_catalog.md` | ✅ |
| Downloaded raw + converted `.mzpeak` | `data/<tile>/<dataset>/…` | ❌ (`.gitignore`d) |
| Published site + data objects | `s3://$BUCKET/<tile>/…` (default bucket `v09`) | ❌ |

`.gitignore` excludes every data binary (`*.raw`, `*.mzpeak`, `*.mzML`, `*.wiff*`, `*.d/`, `*.ibd`,
`*.zip`, …) so downloaded/converted files under `data/<tile>/<dataset>/` are never committed, while
each tile's `_catalog.md` is.

### The 6 FIXED tiles

A directory is a tile **only** if it has a `data/<tile>/_catalog.md`. The tiles are fixed.

| Tile dir | slug | download mechanism |
|---|---|---|
| `general-ms` | `general-ms` | open mzML → `scripts/fetch-examples.sh` · vendor raw → `manifest/general-ms-files.tsv` + `scripts/fetch-general-ms.sh` |
| `ims-examples` | `ims` | `manifest/ims-files.tsv` + `scripts/fetch-ims.sh` |
| `imzml-examples` | `imaging` | `scripts/fetch-examples.sh` |
| `sdrf-examples` | `sdrf` | `scripts/fetch-examples.sh` |
| `tof-grid-examples` | `tof-grid` | `manifest/datasets.tsv` + `build_data.sh` (`vendor_tile`) |
| `pwiz-examples` | `pwiz-tests` | `scripts/fetch-examples.sh` + `manifest/pwiz-files.txt` |

### How the site decides what to show

`scripts/make-s3-index.py` builds the site **from the live object-store listing**:

- A **dataset appears on a tile because its files exist** under `s3://$BUCKET/<tile>/<dataset>/`.
- The matching `### <dataset>` block in `data/<tile>/_catalog.md` supplies its **description**.
  No catalog block ⇒ the dataset still shows, just with no description text.
- A **tile appears only if `s3://$BUCKET/<tile>/_catalog.md` exists** (the allowlist gate).

`scripts/build-corpus-site.sh` is the **only** supported way to (re)generate and publish the site.
It reads catalogs from `CATALOG_ROOT` (default: **this repo's `data/`**), uploads the `_catalog.md`
markers, lists the bucket, runs `make-s3-index.py` + `make-ratio-plots.py`, deploys, and prunes stale
pages. Do **not** edit that script, `make-s3-index.py`, or `make-ratio-plots.py`, and never publish
the site any other way.

### Publishing config (object store)

Publishing needs write credentials. All overridable via env (defaults in parentheses):
`ENDPOINT` (StackIT), `BUCKET` (`v09`), `AWS_PROFILE` (`stackit`). Set up the profile once with
`aws configure --profile stackit`. **Downloads need no credentials** (public sources).

---

## (a) Add a dataset to a specific tile

The dataset directory name (e.g. `PXD012345` or `thermo-astral`) is used **identically** in three
places: the local dir `data/<tile>/<dataset>/`, the S3 prefix, and the `### <dataset>` catalog block.

1. **Get the bytes onto S3** under `s3://$BUCKET/<tile>/<dataset>/…`:
   - Download/convert locally into `data/<tile>/<dataset>/` (see (b)), then push:
     ```sh
     export AWS_PROFILE=stackit
     EP=https://object.storage.eu01.onstackit.cloud      # or your $ENDPOINT
     aws --endpoint-url "$EP" s3 cp data/<tile>/<dataset> s3://v09/<tile>/<dataset> --recursive
     ```
   - For the open tiles, converted `.mzpeak` can be pushed with `scripts/sync-s3.sh`.
2. **Describe it** — see (c).
3. **Publish:** `bash scripts/build-corpus-site.sh`

---

## (b) Wire up on-demand download — where the URL goes

Put the URL in the source matching the tile's mechanism (table in §0):

### Open-format example (mzML/imzML/sdrf) — `scripts/fetch-examples.sh`
Add a `dl` line in that tile's `fetch_*` function. Path is relative to `data/<tile>/`:
```sh
dl "https://…/run.mzML"  "<dataset>/run.mzML"
# MassIVE has no range/resume — add the 3rd arg:
dl "$M?file=f.MSV…/peak/run.mzML&forceDownload=true"  "<dataset>/run.mzML" --no-resume
```

### `general-ms` vendor raw — `manifest/general-ms-files.tsv` (read by `fetch-general-ms.sh` → `data/general-ms/<accession>/`)
TAB-separated; `;`-join multi-file units (e.g. `.wiff`+`.wiff.scan`):
```
accession<TAB>repo<TAB>vendor<TAB>unit<TAB>expected_bytes<TAB>url1;url2
```

### `ims-examples` raw — `manifest/ims-files.tsv` (read by `fetch-ims.sh` → `data/ims-examples/<accession>/`)
```
accession<TAB>repo<TAB>vendor<TAB>im_type<TAB>expected_bytes<TAB>url
```

### `tof-grid-examples` vendor raw — `manifest/datasets.tsv` (read by `build_data.sh` `vendor_tile` → `data/<tile>/<dir>/`, then converts)
```
tile<TAB>dir<TAB>accession<TAB>repo<TAB>files(;-sep | "-")<TAB>unpack(zip|none)<TAB>convert_input(path|auto)<TAB>flags<TAB>notes
```
`files="-"` ⇒ no stable URL; the build prints the dataset page to fetch manually.

### `pwiz-examples`
Add the path to `manifest/pwiz-files.txt` (fetched from the public ProteoWizard mirror).

Verify the URL by actually fetching:
```sh
bash scripts/fetch-examples.sh <tile>     # open-format tiles
bash scripts/fetch-general-ms.sh          # general-ms vendor raw
bash scripts/fetch-ims.sh                 # ims raw
./build_data.sh tof-grid-examples         # tof-grid (fetch + convert)
```
(Override the download dir if you keep data elsewhere: `IMS_OUT=…` for `fetch-ims.sh`.)

---

## (c) Descriptions — dataset and tile (both in `data/<tile>/_catalog.md`)

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

### <dataset>              # MUST equal the S3 prefix s3://$BUCKET/<tile>/<dataset>/
<one-paragraph DATASET description: repo · instrument — modality, format, citation>
```

- **Tile description** = frontmatter + blurb + `<b>Provenance.</b>` paragraph.
- **Dataset description** = a `### <dataset>` heading + the paragraph under it.
- The `### <dataset>` name must match the S3 prefix exactly, or the description won't attach.

(A brand-new tile would also need a `make-ratio-plots.py` `ACCENT` entry for its figure colour — but
tiles are fixed, so normally you only add datasets.)

---

## Remove a dataset

1. **S3 data:** `aws --endpoint-url "$EP" s3 rm s3://v09/<tile>/<dataset> --recursive`
2. **Description:** delete the `### <dataset>` block from `data/<tile>/_catalog.md`.
3. **Download recipe:** delete its line/row from the relevant source —
   `fetch-examples.sh` `dl` line, or the `manifest/*-files.tsv` / `datasets.tsv` / `pwiz-files.txt` row.
4. **Local copies (optional):** `rm -rf data/<tile>/<dataset>`.
5. **Publish:** `bash scripts/build-corpus-site.sh` — it re-lists the bucket and auto-prunes stale pages.

To remove an entire **tile**, also delete `s3://v09/<tile>/_catalog.md` (the builder drops it from the allowlist).

---

## One-line recap

> **Bytes on S3** make a dataset *appear*; **`data/<tile>/_catalog.md`** makes it *described*; the
> **fetch source** (`fetch-examples.sh` / `manifest/*.tsv` / `pwiz-files.txt`) makes it *rebuildable*;
> and **`build-corpus-site.sh`** is the *only* thing that publishes any of it.
