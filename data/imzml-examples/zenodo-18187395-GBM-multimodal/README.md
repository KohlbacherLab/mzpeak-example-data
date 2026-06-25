# Zenodo 18187395 — GBM MALDI phenomics (multi-optical-image case)

**Source:** Zenodo record **18187395** — companion data to *"Spatially Informed Feature Selection
and Machine Learning in MALDI Imaging for Cohort-Scale Molecular Tissue Phenomics in
Glioblastoma."*
**Record:** https://zenodo.org/records/18187395
**License:** CC-BY-4.0 (fully open, no login).
**Download pattern:** `https://zenodo.org/api/records/18187395/files/<SECTION>.zip/content`
**Reconstructed by:** `scripts/fetch-examples.sh imzml-examples` (this directory is git-ignored).

The one openly downloadable imzML bundle we found that ships **two optical images of distinct
modalities per section** — the fixture for the ≥2-optical-image extension path. The Zenodo record
holds **29 per-section ZIPs** (20 `Train`, 9 `Test`); the fetch script pulls only the smallest by
default (`24_Test_P15_r2`, ~248 MB ZIP). Add more with
`GBM_SECTIONS="24_Test_P15_r2 16_Train_P10_r2" bash scripts/fetch-examples.sh imzml-examples`.

Each section ZIP has **no section-name parent inside it**, so the fetch script nests it under
`<SECTION>/`. Per-section layout:

```
<SECTION>/
├── imzml/      <name>.imzML + <name>.ibd      MSI (processed / centroid)
├── HE-XML/     <slide>.svs  + <slide>.xml      optical #1: H&E whole-slide + annotations
├── Optical/    <name>_0001.tif                 optical #2: unstained bright-field
└── TM/         <name>.xlsx                      MSI ↔ histology transform parameters
```

## Files — section `24_Test_P15_r2` (default)

| File | Bytes | Role |
|---|--:|---|
| `24_Test_P15_r2/imzml/Test_P15_r2.imzML` | 6,880,543 | XML metadata + spectrum index |
| `24_Test_P15_r2/imzml/Test_P15_r2.ibd` | 54,443,992 | binary m/z + intensity sidecar (UUID + ibd SHA-1 verified) |
| `24_Test_P15_r2/HE-XML/P1_patientset2_102524_104850_aperioID1010549.svs` | 172,633,155 | **optical #1** — Aperio H&E whole-slide image (TIFF-based) |
| `24_Test_P15_r2/HE-XML/P1_patientset2_102524_104850_aperioID1010549.xml` | 1,426,343 | H&E slide annotations |
| `24_Test_P15_r2/Optical/Patientset2_Rep2_0001.tif` | 28,016,776 | **optical #2** — unstained bright-field image |
| `24_Test_P15_r2/TM/Test_P15_r2.xlsx` | 898,916 | MSI ↔ histology registration transform |

## Other sections (not fetched by default)

Smallest `Train` section: `16_Train_P10_r2.zip` (317,544,549 B). Largest: `21_Test_P13_r1.zip`
(1,012,867,228 B). Full 29-section index:
`https://zenodo.org/api/records/18187395/files/directory_tree.txt/content`.

See [`docs/CORPUS.md`](../../../docs/CORPUS.md) (source #4) for why the usual
"multimodal registration" papers (Patterson 2018 / HuBMAP, Liang 2024 image-fusion, Potthoff /
Nat. Commun. 2025 OMERO, METASPACE) do **not** provide such a bundle.
