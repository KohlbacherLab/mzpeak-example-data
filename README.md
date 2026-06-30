# mzPeak example data

The **describe-don't-store** companion to the [mzPeak](https://mzpeak.org) example
corpus. This repository commits the *structure*, *descriptions* and *scripts* for the
full mzPeak validation/benchmark corpus — but **none of the data itself**. Each dataset
is one small YAML descriptor; one command rebuilds every file by downloading from the
original public repositories (PRIDE, MassIVE, MetaboLights, Zenodo, ProteoWizard) and
running [mzPeakConverter](https://github.com/okohlbacher/mzPeakConverter) to (re)generate
the `.mzpeak` files.

> The corpus is ~330 GB of vendor raw + open-format + converted data. Committing it to
> git is neither possible nor useful. Committing *how to rebuild it* is.

## Quickstart

```sh
git clone https://github.com/kohlbacherlab/mzpeak-example-data.git
cd mzpeak-example-data
pip install pyyaml                       # the only dependency of the YAML tooling

scripts/update.sh                                    # rebuild EVERY dataset + publish
scripts/update.sh data/general-ms/PXD000155/PXD000155.yaml   # just one dataset
scripts/update.sh --dry-run                          # local only, do not touch the bucket
```

`update.sh` runs the whole pipeline for the selected datasets and is **idempotent** at
every step: **download → convert → upload → rebuild catalogs → publish site**. Skip steps
with `--no-convert` / `--no-upload` / `--no-publish`.

## Add / remove a dataset

See **[`HOW-TO-ADD-DATA.txt`](HOW-TO-ADD-DATA.txt)**. In short:

```sh
scripts/new-dataset.sh <tile> <id>          # scaffold data/<tile>/<id>/<id>.yaml
$EDITOR data/<tile>/<id>/<id>.yaml          # set title, description, file urls
scripts/update.sh data/<tile>/<id>/<id>.yaml
```

## What's in here

```
.
├── README.md                 # this file
├── HOW-TO-ADD-DATA.txt        # how to add / remove a dataset
├── .gitignore                # commits only YAML + generated _catalog.md; ignores all data
├── cors.json                 # bucket CORS policy (S3 publishing)
├── docs/CORPUS.md            # narrative inventory: every dataset, accession + source
├── data/
│   ├── TEMPLATE.yaml         # copy this to start a new dataset
│   └── <tile>/               # one of: general-ms, ims-examples, imzml-examples,
│       ├── _tile.yaml        #   sdrf-examples, tof-grid-examples, pwiz-examples
│       ├── _catalog.md       #   GENERATED from the YAML (do not hand-edit)
│       └── <id>/<id>.yaml    #   one descriptor per dataset (id/title/desc/files/convert)
└── scripts/
    ├── update.sh             # the one command: download->convert->upload->catalogs->publish
    ├── new-dataset.sh        # scaffold a descriptor from the template
    ├── fetch-dataset.py      # download a dataset's files (idempotent)
    ├── convert-dataset.py    # raw -> mzPeak via mzpeak-convert (idempotent)
    ├── build-catalogs.py     # regenerate every _catalog.md from the YAML
    ├── corpus_lib.py         # shared loader / selector resolver
    ├── build-corpus-site.sh  # canonical site builder (index + per-tile pages + ratio plots)
    ├── make-s3-index.py      # render the site from the live bucket listing (stdlib only)
    ├── make-ratio-plots.py   # per-category compression-ratio figures
    ├── sync-s3.sh            # bulk-sync local .mzpeak to S3
    └── push-index-stackit.sh # rebuild + deploy index.html
```

## Requirements

- `python3` + **PyYAML** (`pip install pyyaml`), `curl`, `unzip`, `git`, and the AWS CLI
  (for upload/publish; downloading needs no credentials).
- **`mzpeak-convert`** for the convert step: set `$MZPEAK_CONVERT`, put it on `PATH`, or
  build it from [mzPeakConverter](https://github.com/okohlbacher/mzPeakConverter). If it
  isn't found, conversion is skipped (download/publish still work).
- **Vendor raw with no cross-platform reader** (SCIEX `.wiff`, Agilent `.d`, Waters `.raw`,
  Bruker `.d`-BAF) converts only on Windows/Linux with the vendor libraries, or anywhere via
  `--via-msconvert` (ProteoWizard). Thermo `.raw` additionally needs a .NET 8+ runtime.

## Publishing to S3

The browsable site is regenerated **from the live bucket listing**, so it always matches
what's actually deposited. `update.sh` does this automatically; to publish without
re-fetching:

```sh
python3 scripts/build-catalogs.py     # YAML        -> _catalog.md
bash    scripts/build-corpus-site.sh  # _catalog.md + bucket -> index.html + per-tile pages
```

`build-corpus-site.sh` is the only supported way to publish the site. Public read is served
by the bucket's root GetObject policy; `cors.json` allows Range requests from the site origin.

## Relationship to other repos

| Repo | Role |
|---|---|
| [mzpeak.org](https://mzpeak.org) | format overview, rationale, draft spec, viewer |
| [HUPO-PSI/mzPeak-specification](https://github.com/HUPO-PSI/mzPeak-specification) | the specification |
| [mzPeakConverter](https://github.com/okohlbacher/mzPeakConverter) | the `mzpeak-convert` CLI this repo drives |
| [mzPeakValidator](https://github.com/okohlbacher/mzPeakValidator) | independent conformance validation |
| **mzpeak-example-data** (here) | reproducible recipe for the example corpus |

## License

[MIT](LICENSE) for the scripts and descriptions. The underlying datasets are third-party
public deposits, each under its own terms — cite the originating accession (see
[`docs/CORPUS.md`](docs/CORPUS.md)).
