# Vendor raw files — size / compression-ratio benchmark references

Original **vendor raw** files (and raw *sizes*) for the mzML-corpus datasets, kept purely to compare
file sizes and compression ratios (raw → mzML → mzPeak). **The converter does NOT convert raw formats**
— raw is a size reference only, never a conversion input. This dir is git-ignored.

## Compression comparison (raw → mzML → mzPeak)

mzPeak sizes are from the default-encoding e2e run (`out/e2e/RESULTS.tsv`); mzML sizes on-disk; raw sizes
from each repo's file API / HEAD. **mzPeak/mzML** is the clean metric (same data, our conversion);
mzPeak/raw is indicative only (raw↔mzML is not always like-for-like).

| dataset | raw MB | mzML MB | mzPeak MB | mzPeak/mzML | mzPeak/raw | raw status |
|---|--:|--:|--:|--:|--:|---|
| agilent-qtof | — | 2.3 | 0.8 | 0.35× | — | Zenodo: mzML-only |
| sciex-qtrap-6500 | — | 3.0 | 0.3 | 0.10× | — | PRIDE: mzML-only |
| agilent-6560-dtims-imqtof | — | 3.3 | 0.3 | 0.09× | — | Zenodo: mzML-only |
| agilent-6490-triplequad | — | 5.3 | 0.9 | 0.17× | — | PRIDE: mzML-only |
| agilent-8890-gc-ei | — | 15.9 | 1.6 | 0.10× | — | MetaboLights: mzML-only |
| thermo-ltq-ft-ultra-fticr | 221 | 30.2 | 5.5 | 0.18× | 0.02× | ✅ `.RAW` on disk |
| bruker-impact-ii-qtof | — | 31.3 | 20.4 | 0.65× | — | MetaboLights: mzML-only |
| shimadzu-lcms-9030-qtof | — | 36.2 | 2.4 | 0.07× | — | MetaboLights: mzML-only |
| bruker-microtof-q2 | — | 56.6 | 36.0 | 0.64× | — | MetaboLights: mzML-only |
| waters-xevo-g2s-qtof | — | 81.8 | 44.8 | 0.55× | — | MetaboLights: mzML-only |
| sciex-zenotof-7600 | 73 | 89.8 | 50.9 | 0.57× | 0.69× | ☑ sized (MassIVE wiff triple) |
| thermo-ltq-xl-iontrap | 70 | 173.5 | 55.6 | 0.32× | 0.80× | ✅ `.raw` on disk |
| thermo-qexactive-plus | — | 242.1 | 98.4 | 0.41× | — | Zenodo: mzML-only |
| sciex-tripletof-6600 | — | 243.1 | 138.1 | 0.57× | — | Zenodo: mzML-only |
| thermo-ltq-orbitrap-velos | 210 | 429.2 | 101.5 | 0.24× | 0.48× | ✅ `.raw` on disk |
| thermo-fusion-lumos | 659 | 588.6 | 156.5 | 0.27× | 0.24× | ☑ size-only (PRIDE) |
| bruker-timstof-pro | **2106** | 1386.5 | 677.2 | 0.49× | 0.32× | ☑ size-only (MassIVE `.d`, 52 files) |
| thermo-orbitrap-astral | **8638** | 6118.4 | 3359.4 | 0.55× | 0.39× | ✅ `.raw` on disk (8.4 GB) |

**Takeaways**
- **mzPeak < source mzML on every dataset** — 0.07×–0.65× (≈1.5×–14× reduction). Tightest on sparse/
  centroided data (Shimadzu 0.07×, Agilent IM/GC/SRM ≤0.17×); loosest on dense profile (Bruker QTOFs ~0.65×).
- **vs vendor raw:** mzPeak is 0.02×–0.80× of the `.raw`/`.d`/`.wiff`. For the two MassIVE giants the vendor
  raw is **larger** than the mzML (timsTOF `.d` 2106 > mzML 1386; Astral `.raw` 8638 > mzML 6118), so mzPeak
  is ~3× smaller than vendor raw there (0.32× / 0.39×). FT-ICR 0.02× = peak-picked mzML vs profile raw.
- **SCIEX is the exception** where mzML > raw: the ZenoTOF `.wiff`+`.wiff.scan`+`.wiff2` triple is a compact
  73 MB vs the 89.8 MB verbose-XML mzML, so mzPeak (50.9 MB) is still 0.69× of even the compact raw.

## Raw files on disk / sizing

| dataset | source | raw | size | state |
|---|---|---|--:|---|
| thermo-ltq-xl (PXD059878) | PRIDE | `.raw` | 70 MB | ✅ on disk |
| thermo-velos (PXD000001) | PRIDE | `.raw` | 210 MB | ✅ on disk |
| thermo-ft-icr (MTBLS3512) | MetaboLights | `.RAW` | 221 MB | ✅ on disk |
| thermo-fusion-lumos (PXD008952) | PRIDE | `.raw` | 659 MB | size-only |
| sciex-zenotof (MSV000095995) | MassIVE/GNPS2 | `.wiff`+`.wiff.scan`+`.wiff2` triple | 73 MB | size-only |
| bruker-timstof (MSV000101607) | MassIVE/GNPS2 | `.d` (SBA415, 52 files) | 2106 MB | size-only (partial on disk) |
| thermo-astral (MSV000100943) | MassIVE/GNPS2 | `.raw` | 8638 MB | ✅ on disk |

Sizes for the MassIVE datasets were determined from the GNPS2 datasetcache file API
(`https://datasetcache.gnps2.org/datasette/database/filename.json?dataset__exact=<MSV…>`, byte size in
field 7), then the files pulled via the MassIVE `DownloadResultFile` endpoint where wanted. The Astral
`.raw` is fully on disk; the timsTOF `.d` and SCIEX `.wiff` triple are recorded **size-only** (the size
is the benchmark deliverable; the multi-GB binaries are optional). The 9 remaining datasets are genuinely
mzML-only deposits (no raw to fetch).
