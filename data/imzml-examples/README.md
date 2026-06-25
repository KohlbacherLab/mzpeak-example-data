# imzML example datasets

Frequently-used public MS-imaging example datasets, one directory per source. **This directory is git-ignored** (`data/imzml-examples/` in `.gitignore`) — large binary research data, not committed.

Total: ~3.4 GB · 8 dataset directories · 14 `.imzML`/`.ibd` pairs · 3 optical `.tif` (+1 bright-field `.tif` and 1 H&E `.svs` in the GBM multimodal set).

| Directory | Source | Mode | imzML | ibd | TIFF | Size | Notes |
|---|---|---|:--:|:--:|:--:|--:|---|
| `example1-continuous` | ms-imaging.org Example 1 (beny/imzml mirror) | continuous | 1 | 1 | – | 356 K | 3×3-pixel sanity test |
| `example1-processed` | ms-imaging.org Example 1 (beny/imzml mirror) | processed | 1 | 1 | – | 616 K | 3×3-pixel processed test |
| `PXD001283-HR2MSI-urinary-bladder` | PRIDE PXD001283 | processed | 1 | 1 | ✓ | 833 M | reference real dataset (AP-SMALDI mouse urinary bladder, 10 µm, 260×134) + optical image + results.csv. `.ibd` is hard-linked to `data/HR2MSImouseurinarybladderS096.ibd` |
| `zenodo-DESI` | Zenodo 10084132 | processed (centroid) | 7 | 7 | – | 609 M | 7 DESI colorectal-adenoma sections (`ColAd_Individual/…`) |
| `zenodo-LA-ESI` | Zenodo 10084132 | — | 1 | 1 | ✓ | 557 M | LA-ESI *Arabidopsis* leaf + pre-ablation optical TIFF |
| `zenodo-AP-SMALDI` | Zenodo 10084132 | — | 1 | 1 | ✓ | 842 M | AP-SMALDI mouse urinary bladder + optical TIFF (same specimen family as PXD001283) |
| `zenodo-LTP` | Zenodo 10084132 | — | 1 | 1 | – | 370 M | low-temperature-plasma MSI (chilli) |
| `zenodo-18187395-GBM-multimodal` | Zenodo 18187395 | processed (centroid) | 1\* | 1\* | ✓✓ | 252 M\* | **multi-optical case**: per section, imzML + **two** optical images (H&E whole-slide `.svs` + bright-field `.tif`) + annotation `.xml` + MSI↔histology transform `.xlsx`. \*Default = smallest section `24_Test_P15_r2`; 29 sections available |

## Sources & provenance
- **ms-imaging.org Example 1** (canonical tiny test pair) — mirrored at https://github.com/beny/imzml/tree/master/data
- **PXD001283** — PRIDE/ProteomeXchange: https://www.ebi.ac.uk/pride/archive/projects/PXD001283 (Römpp et al.; the project's acceptance dataset)
- **Zenodo 10084132** "mzML/imzML test data": https://zenodo.org/records/10084132 (DESI, LA-ESI, AP-SMALDI, LTP collections)
- **Zenodo 18187395** GBM MALDI phenomics (CC-BY-4.0): https://zenodo.org/records/18187395 — the only openly-downloadable imzML bundle we found that ships **two** optical images per section. See `docs/CORPUS.md` source #4 for why the usual "multimodal registration" papers (Patterson 2018 / HuBMAP; Liang 2024 image-fusion; Potthoff/Nat.Commun. 2025 OMERO; METASPACE) do not provide one.

## Notes
- These are openly-shared public research datasets, used here as conversion/round-trip test inputs for `mzPeakConverter`.
- The two **Example 1** pairs are the smallest valid imzML files — ideal for fast unit/round-trip tests (continuous vs processed).
- Datasets with an optical `.tif` (PXD001283, LA-ESI, AP-SMALDI) exercise the Q10 single-optical-image / registration path; `zenodo-18187395-GBM-multimodal` exercises the **≥2 optical images per section** path (H&E `.svs` + bright-field `.tif`).
- The `zenodo-DESI` collection contains 7 separate imzML acquisitions under nested folders.
- Knowledge-graph note: `knowledge/data/Example imzML datasets.md`.
