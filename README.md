# mzPeak example data

The **describe-don't-store** companion to the [mzPeak](https://mzpeak.org) example
corpus. This repository commits the *structure*, *descriptions*, *manifests* and
*scripts* for the full mzPeak validation/benchmark corpus — but **none of the data
itself**. One script, [`build_data.sh`](build_data.sh), reconstructs every file by
downloading from the original public repositories (PRIDE, MassIVE, MetaboLights,
Zenodo, ProteoWizard) and running [mzPeakConverter](https://github.com/okohlbacher/mzPeakConverter)
to (re)generate the `.mzpeak` files.

> The corpus is ~330 GB of vendor raw + open-format + converted data. Committing it
> to git is neither possible nor useful. Committing *how to rebuild it* is.

## Quickstart

```sh
git clone https://github.com/kohlbacherlab/mzpeak-example-data.git
cd mzpeak-example-data

./build_data.sh                 # download every dataset + convert to .mzpeak
./build_data.sh mzML-examples   # just one tile
SKIP_CONVERT=1 ./build_data.sh  # download only, no conversion
```

`build_data.sh` is **idempotent**: already-downloaded files are skipped, and only
missing `.mzpeak` outputs are (re)built. It locates `mzpeak-convert` via
`$MZPEAK_CONVERT`, else clones + `cargo build --release`s mzPeakConverter into
`.build/`.

### Requirements

- `bash`, `curl`, `unzip`, `git`. `python3` is needed for the `pwiz-examples`
  tile (UTF-8-safe URL encoding of its file list).
- **To build `mzpeak-convert` from source** (skipped if you point `$MZPEAK_CONVERT`
  at a prebuilt binary): a **C/C++ toolchain incl. `libstdc++`**, **`cmake`**, and
  **Rust ≥ 1.87 from [rustup](https://rustup.rs)**.
  - Debian/Ubuntu: `sudo apt-get install -y build-essential cmake curl unzip git`,
    then install Rust via rustup.
  - ⚠️ Use **rustup**, not the distro `rustc`/`cargo` (apt) — they're too old for
    this build and shadow rustup. If a distro Rust is present, remove it first:
    `sudo apt-get remove -y rustc cargo`.
  - `build_data.sh` preflights all of the above and prints these exact commands if
    anything is missing (it catches the `-lstdc++` link error and the stale-rustc trap).
- Thermo `.raw` conversion additionally needs a **.NET 8+** runtime.
- **Vendor raw with no cross-platform reader** (SCIEX `.wiff`, Agilent `.d`,
  Waters `.raw`, Bruker `.d`-BAF) only converts on **Windows/Linux** with the
  vendor libraries, or anywhere via `--via-msconvert` (needs ProteoWizard). On
  unsupported platforms those tiles are **fetched and flagged SKIP**, not failed.

## What's in here

```
.
├── README.md              # this file
├── build_data.sh          # ← reconstruct the whole corpus from public repos
├── .gitignore             # ignores every data binary (*.mzpeak/*.mzML/*.d/*.raw/*.wiff/…)
├── cors.json              # bucket CORS policy (S3 publishing)
├── docs/
│   └── CORPUS.md          # the canonical inventory: every dataset, accession + download URL
├── manifest/
│   ├── datasets.tsv       # machine-readable inventory for the tof-grid vendor-raw tile (drives build_data.sh)
│   ├── general-ms-demonstrators.tsv  # curated General MS broad-vendor showcase (accessions + DOIs)
│   └── pwiz-files.txt     # list of ProteoWizard test mzML paths (fetched from the public mirror)
├── data/                  # MIRRORS the archive hierarchy — README.md per tile, NO binaries
│   ├── mzML-examples/     #   non-imaging mzML, one dir per instrument
│   ├── imzml-examples/    #   MS-imaging imzML (+ ibd, optical TIFF)
│   ├── pwiz-examples/     #   ProteoWizard vendor-reader test data
│   ├── sdrf-examples/     #   SDRF/ISA study-design files
│   ├── tof-grid-examples/ #   QTOF SWATH/DIA (TOF-grid encoding)
│   └── demo/              #   one showcase .mzpeak for the website/viewer
└── scripts/
    ├── fetch-examples.sh         # unified downloader: mzML / imzml / sdrf / pwiz (curated, idempotent)
    ├── make-s3-index.py          # build index.html + subpages from the live bucket
    ├── make-ratio-plots.py       # per-category compression-ratio plots
    ├── push-index-stackit.sh     # rebuild index.html + deploy to S3
    └── sync-s3.sh                # sync corpus .mzpeak to S3 + rebuild/deploy index.html
```

Conformance validation is intentionally out of scope here — validate rebuilt
archives with the independent [`mzPeakValidator`](https://github.com/okohlbacher/mzPeakValidator)
(`mzpeak-validate`) tool.

Every dataset's provenance — accession, originating repository, exact files and
download URL — is in **[`docs/CORPUS.md`](docs/CORPUS.md)**. Per-tile `README.md`
files describe each subset.

## Publishing to S3 (index.html)

The browsable site at the object store is regenerated **from the live bucket
listing** — so it always matches what's actually deposited:

```sh
scripts/sync-s3.sh              # sync .mzpeak to s3://v09 + rebuild & deploy index.html
scripts/sync-s3.sh --dry-run    # plan only, nothing transferred
```

`make-s3-index.py` reads the dataset descriptions to render the landing page and
per-category subpages (mass-spec / imaging / sdrf / pwiz-tests) with compression
ratios. Public read is served by the bucket's root GetObject policy; `cors.json`
allows Range requests from the website origin.

## Relationship to other repos

| Repo | Role |
|---|---|
| [mzpeak.org](https://mzpeak.org) | format overview, rationale, draft spec, viewer |
| [HUPO-PSI/mzPeak-specification](https://github.com/HUPO-PSI/mzPeak-specification) | the specification |
| [mzPeakConverter](https://github.com/okohlbacher/mzPeakConverter) | the `mzpeak-convert` CLI this repo drives |
| **mzpeak-example-data** (here) | reproducible recipe for the example corpus |

## License

[MIT](LICENSE) for the scripts and descriptions. The underlying datasets are
third-party public deposits, each under its own terms — cite the originating
accession (see [`docs/CORPUS.md`](docs/CORPUS.md)).
