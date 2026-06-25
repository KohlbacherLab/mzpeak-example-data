# SDRF example files

Curated SDRF files for the SDRF↔mzPeak integration work (backlog 999.5). **This directory is
git-ignored.** Tracked record: `docs/CORPUS.md` + `scripts/fetch-sdrf-examples.sh`
(`bash scripts/fetch-sdrf-examples.sh` to rebuild).

| Directory | File | Rows | Labels | Pairs with |
|---|---|--:|---|---|
| `MTBLS1129/` | `MTBLS1129.sdrf.tsv` | 264 | label-free | `../mzML-examples/waters-xevo-g2s-qtof/QC01.mzML` (SDRF lists `FILES/QC01.mzML`) |
| `PXD011799/` | `PXD011799.sdrf.tsv` + `…TiO2_TMT_fr8.mzML` | 480 | **TMT 10-plex** (TMT126…TMT131) | matched mzML = PRIDE conversion of SDRF-referenced `TiO2_TMT_fr8.raw` (local raw→mzML fails on Apple Silicon) |

- **MTBLS1129** — ready SDRF↔mzML pair (have the mzML); baseline ingestion fixture.
- **PXD011799** — TMT channel→sample fixture (`comment[label]` model) for the `channel_list` design.

Sources & full provenance: `docs/CORPUS.md`.
