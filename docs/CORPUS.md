# mzPeakConverter — Validation Data Corpus (Handoff)

This document inventories **all raw vendor data examples** assembled to validate the
**mzPeakConverter** (the `mzpeak-convert` host CLI + the `mzPeakConverter`
reference encoders). It is intended for inclusion in the overall data-corpus documentation
so the validation set can be **reproduced** and **re-fetched**.

Wherever a dataset is a public deposit, the **accession** (PRIDE `PXD…`, MassIVE `MSV…`,
MetaboLights `MTBLS…`, Zenodo record) and the **repository / download URL** are given so the
corpus can be reconstructed from scratch. Datasets that are **private fixtures or vendored test
data** (not publicly downloadable) are flagged explicitly.

## Coverage at a glance

- **Vendors:** Thermo, Bruker, SCIEX, Agilent, Waters, Shimadzu — 6 instrument vendors.
- **Formats exercised:** mzML, imzML (+`.ibd`), Thermo `.raw`, Bruker `.d` (TDF / TSF / BAF),
  SCIEX `.wiff` / `.wiff.scan` / `.wiff2`, Agilent `.d` (MassHunter profile grid), Waters `.raw`
  (TWIMS) + UNIFI test data.
- **Analyzer / modality classes:** Orbitrap (incl. Astral DIA), Q-TOF / UHR-QTOF, TripleTOF
  SWATH/DIA, ZenoTOF (EAD/Zeno trap), FT-ICR, pure ion trap, triple-quadrupole (SRM/MRM), QqLIT,
  ion mobility (TIMS-PASEF, DTIMS, TWIMS), GC-MS / EI, and MS-imaging (AP-SMALDI, DESI, LA-ESI, LTP).

### Conventions used below

- **Where to obtain** lists the canonical public source. The object store
  `https://object.storage.eu01.onstackit.cloud/v09/...` is the project's own re-hostable mirror
  (the `v09` bucket, also reachable via `aws s3 sync s3://v09 data/`); the original public
  accession is always given alongside.
- Sizes are **on-disk** (`du -h`) where the data is present locally, otherwise the recorded
  byte-size benchmark. `.d` / `.wiff` / imzML are multi-file units — size is the whole unit.
- The converter **does not read vendor raw as a conversion input for the size benchmarks** in
  `raw-examples/` (those are size/compression references only). Native readers (Thermo `.raw`,
  Bruker TDF/TSF/BAF, SCIEX `.wiff`, Agilent `.d`, Waters `.raw`) are exercised separately by the
  e2e corpus and the vendor-CI manifest.

---

## Thermo (Thermo Fisher Scientific) — `.raw`

| Instrument / analyzer | Format | Accession | Description | Approx size | Where to obtain |
|---|---|---|---|--:|---|
| (generic Thermo) | `.raw` | mzdata test fixture | `small.RAW` — 48-spectrum smoke-test raw (mzdata reader unit test) | 1.4 MB | Vendored: `mzPeak OpenMS/mzdata/test/data/small.RAW` (mzdata crate test data; **not a public accession**) |
| LTQ Orbitrap Velos | `.raw` | PRIDE **PXD000001** | TMT-labelled *Erwinia carotovora*, DDA (Top10 HCD); the canonical ProteomeXchange demo dataset | 210 MB | PRIDE: https://www.ebi.ac.uk/pride/archive/projects/PXD000001 — file `TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.raw` (`TMT_Erwinia_01.raw`) |
| Orbitrap Fusion Lumos | `.raw` | PRIDE **PXD008952** | CPTAC TMT (`01_CPTAC_TMTS1-NCI7_P_JHUZ_20170509_LUMOS.raw`), DDA proteomics | 659 MB | PRIDE: https://www.ebi.ac.uk/pride/archive/projects/PXD008952 |
| Orbitrap Astral | `.raw` | MassIVE **MSV000100943** | High-throughput plasma proteomics, **DIA** (`20240912_WFB_exp01_magnet_5_0.raw`) | 16 GB (raw on disk; mzML 6.1 GB) | MassIVE/GNPS2: `https://massive.ucsd.edu/ProteoSAFe/DownloadResultFile?file=f.MSV000100943/ccms_peak/RAW/20240912_WFB_exp01_magnet_5_0.mzML&forceDownload=true` (mzML); raw via the MassIVE `DownloadResultFile` endpoint |
| Orbitrap Astral | mzML | MassIVE **MSV000100943** (alt subset) | DIA HAP1 (`20231206_HAP1_1ug_60min_DIA_2Th_5e4_3p5ms_rep03`) — listed under dir `thermo-orbitrap-astral-PXD049028` | (mzML/`.raw` subset) | Thermo Astral DIA reference set; see PXD049028 / MSV000100943 |
| LTQ-FT Ultra | `.RAW` | MetaboLights **MTBLS3512** | FT-ICR metabolomics (`mtab_BIOS_CRAM1620_1_072617_34.RAW`) | 221 MB | MetaboLights: https://www.ebi.ac.uk/metabolights/MTBLS3512 |
| LTQ XL (ion trap) | `.raw` | PRIDE **PXD059878** | Pure ion-trap DDA (`2013_30_Amrutha_050713_1.raw`) | 70 MB | PRIDE: https://www.ebi.ac.uk/pride/archive/projects/PXD059878 |
| Q Exactive Plus (Orbitrap) | mzML | Zenodo 17549994 / PRIDE **PXD077619** | Orbitrap DDA (`160920_SM-AKTWT_509.mzML`; alt `QEP2_11961_RDA_GITR_GA_Afuc_200820` under PXD077619) | 254 MB | Zenodo record 17549994; PRIDE PXD077619 |

---

## Bruker — `.d` (TDF / TSF / BAF)

| Instrument / analyzer | Format | Accession | Description | Approx size | Where to obtain |
|---|---|---|---|--:|---|
| timsTOF (generic) | TDF `.d` | opentims test fixture | `test.d` — 919-spectrum TIMS-PASEF round-trip unit test | 764 KB | Vendored: `OpenMS/OpenMS-build/_deps/opentims-src/pytest/test.d` (opentims project test data; **not a public accession**) |
| timsTOF | TDF `.d` (diaPASEF) | mzdata test fixture | `diaPASEF.d` — diaPASEF TDF reader unit test | 988 KB | Vendored: `mzPeak OpenMS/mzdata/test/data/diaPASEF.d` (mzdata crate test data; **not a public accession**) |
| timsTOF Pro | TDF `.d` (PASEF, ion mobility) | MassIVE **MSV000101607** | `SBA415.d` — TIMS-PASEF proteomics, ion-mobility (52-file `.d`) | 2.1 GB (raw `.d`; mzML 1.45 GB) | MassIVE/GNPS2: `https://massive.ucsd.edu/ProteoSAFe/DownloadResultFile?file=f.MSV000101607/peak/SBA415.mzML&forceDownload=true` (mzML); raw `.d` via MassIVE `DownloadResultFile` |
| timsTOF | TSF `.d` (line-mode), **pos** | private BRFP fixture | `timsTOF_autoMSMS_Urine_6min_pos.d` — autoMSMS urine, positive mode (TSF line-mode reader via ported BRFP rusqlite + zstd `tsf_bin`) | 101 MB | **Private fixture** (`mzPeak/BRFP/fixtures/private/`); not publicly downloadable |
| timsTOF | TSF `.d` (line-mode), **neg** | private BRFP fixture | `timsTOF_autoMSMS_Urine_6min_neg.d` — autoMSMS urine, negative mode | 101 MB | **Private fixture** (`mzPeak/BRFP/fixtures/private/`); not publicly downloadable |
| (Bruker, BAF acquisition) | BAF `.d` | MetaboLights **MTBLS18** | `LTI225-41-3neg_1-D,5_01_24321.d` — BAF metabolomics; round-trip via ported BRFP BAF reader. **Status: skip** (needs vendor SDK FFI; conversion deferred) | 301 MB | MetaboLights MTBLS18: https://www.ebi.ac.uk/metabolights/MTBLS18 (BAF scratch under `BRFP/tmp/baf-e2e/`) |
| micrOTOF-Q II (QTOF) | mzML | MetaboLights **MTBLS520** | `neg_01_Fistax_1-A,2_01_5715.mzML` — Bruker QTOF metabolomics | 59 MB | MetaboLights: https://www.ebi.ac.uk/metabolights/MTBLS520 |
| impact II (UHR-QTOF) | mzML | MetaboLights **MTBLS12824** | `21P0055_Tissue_Georges_NEG_N_01_17471.mzML` — UHR-QTOF | 33 MB | MetaboLights: https://www.ebi.ac.uk/metabolights/MTBLS12824 |

> **mtbls18 e2e fixture:** `LTI225-03-1neg_1-A__7_01_24298.mzML` (real LC-MS run, has TIC chromatogram)
> — converted from MetaboLights **MTBLS18**, used as the host e2e "real LC-MS" mzML input.

---

## SCIEX — `.wiff` / `.wiff.scan` / `.wiff2`

| Instrument / analyzer | Format | Accession | Description | Approx size | Where to obtain |
|---|---|---|---|--:|---|
| TripleTOF 5600 | `.wiff` + `.wiff.scan` | PRIDE **PXD078909** | `SW_F2_2-2` — **SWATH-MS** zebrafish quantitative proteomics (smallest SWATH pair) | 352 MB (`.wiff` 15 MB + `.wiff.scan` 331 MB) | PRIDE FTP: `https://ftp.pride.ebi.ac.uk/pride/data/archive/2026/05/PXD078909/SW_F2_2-2.wiff` + `…/SW_F2_2-2.wiff.scan` · DOI 10.6019/PXD078909 |
| TripleTOF 6600 | `.wiff` + `.wiff.scan` + `.wiff2` | PRIDE **PXD071869** | `08_SWATH_1E_1H` — dual-window SWATH/DIA (TOF-grid candidate) | ~2.4 GB | PRIDE: https://www.ebi.ac.uk/pride/archive/projects/PXD071869 |
| TripleTOF 6600 | `.wiff` + `.wiff.scan` | PRIDE **PXD011326** | `VD_170826_SWATH_6600_PD_15` — classic two-file SWATH | ~2.6 GB | PRIDE: https://www.ebi.ac.uk/pride/archive/projects/PXD011326 |
| TripleTOF 6600 | `.wiff` + `.wiff.scan` | MassIVE **MSV000090684** | `11410_DGCR8_CBF_BR2_BioID_20181022_TOF6600_SWATH` — large BioID-SWATH | ~5.4 GB | MassIVE: https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?task=MSV000090684 |
| TripleTOF 6600 | `.wiff` + `.wiff.scan` | MassIVE **MSV000090136** | `17_16_hpr56_ko_YMR295C_4444_-0.04` — yeast proteome SWATH | ~2.2 GB | MassIVE: https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?task=MSV000090136 |
| TripleTOF | `.wiff` + `.wiff.scan` | MassIVE **MSV000093587** | `Sample049` — TripleTOF SWATH | ~1.8 GB | MassIVE: https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?task=MSV000093587 |
| ZenoTOF 7600 | `.wiff` + `.wiff.scan` + `.wiff2` | MassIVE **MSV000095995** | `20240826_RNAseB_Reduced_50ngul_1ul_MRM_03` — RNAse B reduced, **MRM-HR / EAD** intact-protein LC-MS (`MS:1003293 "ZenoTOF 7600"`); CC0 (doi:10.25345/C51R6NC1Z) | 73 MB (wiff 2.1 MB + wiff.scan 69 MB + wiff2 2.4 MB) | MassIVE: `https://massive.ucsd.edu/ProteoSAFe/DownloadResultFile?file=f.MSV000095995/ccms_peak/20240826_RNAseB_Reduced_50ngul_1ul_MRM_03.mzML&forceDownload=true` (mzML). **Native wiff triple** mirrored on object store: `https://object.storage.eu01.onstackit.cloud/v09/mzML-examples/sciex-zenotof-7600/20240826_RNAseB_Reduced_50ngul_1ul_MRM_03.wiff` (+`.wiff.scan`, +`.wiff2`) |
| QTRAP 6500 (QqLIT) | mzML | PRIDE **PXD066465** | `Drug_substance_3_scheduled_MRM.mzML` — scheduled **MRM** | 3.1 MB | PRIDE: https://www.ebi.ac.uk/pride/archive/projects/PXD066465 |
| TripleTOF 6600 | mzML | Zenodo 17416537 | `12_80.mzML` — TripleTOF reference mzML | 255 MB | Zenodo record 17416537 (mirror: `…/v09/mzML-examples/sciex-tripletof-6600/12_80.mzpeak`) |

---

## Agilent — `.d` (MassHunter profile grid)

| Instrument / analyzer | Format | Accession | Description | Approx size | Where to obtain |
|---|---|---|---|--:|---|
| 6545 Q-TOF LC/MS | `.d` (profile) | PRIDE **PXD041315** | `LMVCS24HC.d` — shotgun proteomics (*C. elegans* / *Cronobacter sakazakii* infection); full `.d` with `MSProfile.bin` (profile) + `MSPeak.bin` (centroid) + `MSScan.bin` | 617 MB | PRIDE: https://www.ebi.ac.uk/pride/archive/projects/PXD041315 (DOI 10.6019/PXD041315); deposited as per-run `.zip` (`LMV_CS_24_h.zip`) |
| Q-TOF | `.d.zip` (profile) | PRIDE **PXD041903** | `20190423_Alex7.d.zip` → `…/AcqData/MSProfile.bin` — smallest Agilent profile-grid `.d` (vendor-CI sample) | 422 MB | PRIDE FTP: `https://ftp.pride.ebi.ac.uk/pride/data/archive/2025/05/PXD041903/20190423_Alex7.d.zip` (unzip in place) |
| Q-TOF | `.d.zip` (profile) | PRIDE **PXD059108** | `lysate_000008.d.zip` — largest Agilent run | ~3.9 GB | PRIDE: https://www.ebi.ac.uk/pride/archive/projects/PXD059108 |
| Q-TOF | `.d.zip` (profile) | PRIDE **PXD059765** | `CON1_2.d.zip` | ~1.2 GB | PRIDE: https://www.ebi.ac.uk/pride/archive/projects/PXD059765 |
| 6490 Triple Quad (QqQ) | mzML | PRIDE **PXD041762** | `REC-2349_P2_F1.mzML` — QqQ / **SRM** (dir slug `agilent-6490-triplequad`) | 5.5 MB | PRIDE: https://www.ebi.ac.uk/pride/archive/projects/PXD041762 |
| 6490 Triple Quad (dMRM) | mzML | Zenodo 18502866 | `MRM-standmix-5.mzML` — **chromatogram-only** dMRM (0 spectra, 138 chromatograms; dir slug `agilent-qtof` is a misnomer) | 2.4 MB | Zenodo record 18502866 |
| 6560 IM-QTOF (DTIMS) | mzML | Zenodo 18481720 | `CEMS_10ppm.mzML` — drift-tube ion mobility (**DTIMS**) | 3.4 MB | Zenodo record 18481720 |
| 8890 GC / 7000D | mzML | MetaboLights **MTBLS11550** | `EFWS-1.mzML` — **GC-MS / EI** | 17 MB | MetaboLights: https://www.ebi.ac.uk/metabolights/MTBLS11550 |

> **Not obtained (coverage gaps in `tof-grid-examples/`):** MassIVE **MSV000094882**
> (`Alexander_023_B_30x_pos_121820_136.d`) and **MSV000084856** (`Au010-VOC1-D1.D`) — large `.bin`
> binaries returned HTTP 500 at download; only stub metadata present. The three PRIDE Agilent
> studies above are sufficient for profile-grid validation.

---

## Waters — `.raw` (TWIMS) + UNIFI test data

| Instrument / analyzer | Format | Accession | Description | Approx size | Where to obtain |
|---|---|---|---|--:|---|
| Synapt (TWIMS ion mobility) | `.raw` | PRIDE **PXD073666** | `20250628_cpB_100000ms_03.raw` — Waters Synapt TWIMS ion-mobility (`_FUNC*.DAT` directory); smallest per-run `.raw.zip` (vendor-CI sample) | ~290 MB | PRIDE FTP: `https://ftp.pride.ebi.ac.uk/pride/data/archive/2026/04/PXD073666/20250628_cpB_100000ms_03.raw.zip` (unzip in place) |
| Synapt G2-Si (HDMSE) | mzPeak (from `.raw`) | (Waters Synapt G2-Si HDMSE source) | `20181203_Capan2_1.mzpeak` — HDMS^E ion-mobility, Capan2 sample (converted artifact kept; source `.raw` not retained locally) | 494 MB (`.mzpeak`) | Local artifact `data/mzML-examples/waters-synapt-g2si-hdmse/`; Waters TWIMS `.raw` source (see PXD073666 for a re-fetchable TWIMS `.raw`) |
| (Waters UNIFI / Q-TOF, HDMSe) | mzML | object-store / pwiz test data | `08Mar17_HDMSe_25fmolMix1_01…` UNIFI `Reader_UNIFI_Test.data` — combineIMS / mobility-filter HDMSe variants (ProteoWizard reader test data) | small | Object store: `https://object.storage.eu01.onstackit.cloud/v09/pwiz-examples/UNIFI/…` (ProteoWizard `Reader_UNIFI_Test` / `Reader_Waters_Test` fixtures) |
| Xevo G2-XS QTof | mzML | MetaboLights **MTBLS1129** | `QC01.mzML` — Waters Q-TOF (dir slug says G2-S; in-file model G2-XS) | 86 MB | MetaboLights: https://www.ebi.ac.uk/metabolights/MTBLS1129 |
| (Waters PDA / UV) | mzML | (Waters LC-PDA) | `QC_LCMS2-2_23_268-1-1.mzML` — PDA/UV optical-detector channel test | small | Local `data/mzML-examples/waters-pda-uv/` |

> **Known gap:** no *public mzML* preserves Waters TWIMS / Cyclic ion mobility with drift intact
> (vendor `.raw` only). The PXD073666 `.raw` above is the re-fetchable TWIMS source for that path.

---

## Shimadzu — `.raw` / mzML

| Instrument / analyzer | Format | Accession | Description | Approx size | Where to obtain |
|---|---|---|---|--:|---|
| LCMS-9030 Q-TOF | raw (size ref) | MetaboLights **MTBLS13204** | `raw-examples/shimadzu-lcms9030-MTBLS13204/raw/` — Shimadzu Q-TOF (new-vendor coverage) | 53 MB | MetaboLights: https://www.ebi.ac.uk/metabolights/MTBLS13204 |
| LCMS-9030 Q-TOF | mzML | MetaboLights **MTBLS13204** | `Blind_P1_pos_012.mzML` — Shimadzu Q-TOF, positive mode | 38 MB | MetaboLights: https://www.ebi.ac.uk/metabolights/MTBLS13204 |

---

## MS-Imaging — imzML (+ `.ibd`)

| Modality / instrument | Format | Accession | Description | Approx size | Where to obtain |
|---|---|---|---|--:|---|
| (imzML spec example) | imzML + ibd, **continuous** | imzML spec example | `Example_Continuous` — 3×3-pixel continuous-mode sanity test (canonical ms-imaging.org Example 1) | 356 KB–652 KB | ms-imaging.org Example 1, mirror: https://github.com/beny/imzml/tree/master/data. e2e fixture: `mzPeakConverter/tests/fixtures/imaging/Example_Continuous.imzML` |
| (imzML spec example) | imzML + ibd, **processed** | imzML spec example | `Example_Processed` — 3×3-pixel processed-mode sanity test | 616 KB–912 KB | ms-imaging.org Example 1 (same as above). e2e fixture: `tests/fixtures/imaging/Example_Processed.imzML` |
| AP-SMALDI (Q Exactive HF) | imzML + ibd + optical TIFF, processed | PRIDE **PXD001283** | `HR2MSImouseurinarybladderS096` — AP-SMALDI HR2MSI **mouse urinary bladder**, 10 µm, 260×134 px, + optical image + results.csv (Römpp et al. acceptance dataset) | 833 MB–1.1 GB | PRIDE: https://www.ebi.ac.uk/pride/archive/projects/PXD001283 |
| AP-SMALDI | imzML + ibd + optical TIFF | Zenodo **10084132** | AP-SMALDI mouse urinary bladder + optical TIFF (same specimen family as PXD001283) | 842 MB–1.1 GB | Zenodo: https://zenodo.org/records/10084132 |
| LA-ESI | imzML + ibd + optical TIFF | Zenodo **10084132** | LA-ESI *Arabidopsis thaliana* leaf (**NEG**) + pre-ablation optical TIFF (`180817 NEG Thaliana leaf` family) | 557 MB–635 MB | Zenodo: https://zenodo.org/records/10084132 |
| DESI | imzML + ibd, processed/centroid | Zenodo **10084132** | 7 DESI colorectal-adenoma sections (`ColAd_Individual/…`) | 609 MB–841 MB | Zenodo: https://zenodo.org/records/10084132 |
| LTP (low-temperature plasma) | imzML + ibd | Zenodo **10084132** | Low-temperature-plasma MSI (chilli) | 370 MB–492 MB | Zenodo: https://zenodo.org/records/10084132 |
| MALDI (GBM multimodal) | imzML + ibd + H&E `.svs` + bright-field TIFF | Zenodo **18187395** | GBM MALDI phenomics — per-section imzML + **two** optical images + annotation XML + MSI↔histology transform (default smallest section `24_Test_P15_r2`; 29 sections available); CC-BY-4.0 | 252 MB–682 MB | Zenodo: https://zenodo.org/records/18187395 |

---

## Plain-mzML test fixtures (committed)

| Purpose | Format | Source | Description | Size | Where to obtain |
|---|---|---|---|--:|---|
| Real LC-MS e2e | mzML | MetaboLights **MTBLS18** | `LTI225-03-1neg_1-A__7_01_24298.mzML` — real LC-MS run with TIC chromatogram | small | `mzPeakConverter (build output)/mtbls18/` (from MTBLS18) |
| Profile f32 | mzML | local fixture | `profile_intensity_f32.mzML` — profile, f32 intensity, no chromatograms | tiny | `mzPeakConverter/tests/fixtures/mzml/` (committed) |
| Profile f64 | mzML | local fixture | `profile_intensity_f64.mzML` — profile, f64 intensity | tiny | `mzPeakConverter/tests/fixtures/mzml/` (committed) |
| pwiz tiny reference | mzML | ProteoWizard | `tiny.pwiz.1.1.mzML` — pwiz reference smoke test | tiny | `mzPeakConverter/tests/fixtures/mzml/` (committed) |

---

## Private / fixture-only vs publicly downloadable

**Publicly downloadable (have an accession):** all PRIDE `PXD…`, MassIVE `MSV…`,
MetaboLights `MTBLS…`, and Zenodo entries above — the large majority of the corpus. PRIDE files
are mirrored at `https://ftp.pride.ebi.ac.uk/...`; MassIVE via the `DownloadResultFile` endpoint
(no HTTP Range/resume); Zenodo via the record pages; MetaboLights via the EBI FTP/MetaboLights UI.
Many converted `.mzpeak` artifacts and several native vendor binaries are additionally mirrored on
the project object store (`https://object.storage.eu01.onstackit.cloud/v09/...`,
`aws s3 sync s3://v09 data/`).

**Private / vendored test fixtures (NOT publicly downloadable):**

- **Bruker timsTOF Urine BRFP fixtures** — `timsTOF_autoMSMS_Urine_6min_pos.d` / `…_neg.d`
  (TSF line-mode), `mzPeak/BRFP/fixtures/private/`. Private; used only for the ported BRFP TSF reader.
- **mzdata test data** — `small.RAW` (Thermo), `diaPASEF.d` (Bruker TDF). Vendored from the mzdata
  crate's `test/data`; no public accession (upstream project test fixtures).
- **opentims test data** — `test.d` (Bruker TDF). Vendored from the opentims project's pytest data;
  no public accession.
- **ProteoWizard reader test data** — UNIFI / Waters `Reader_*_Test.data` HDMSe fixtures (mirrored on
  the v09 object store); these are ProteoWizard project test assets, not a public MS deposit.

---

### Notes on local layout

- Vendor raw size-benchmark references: `data/raw-examples/` (dir names encode
  `vendor-instrument-ACCESSION`, e.g. `thermo-ltq-orbitrap-velos-PXD000001`).
- TOF grid (SWATH/DIA) raw corpus: `data/tof-grid-examples/` (dir names = accession).
- Native Agilent + SCIEX raw: `data/vendor-agilent-sciex/{agilent,sciex}/ACCESSION/`.
- mzML instrument sweep: `data/mzML-examples/` (one dir per instrument; per-dir READMEs
  carry exact bytes + URLs).
- imzML imaging: `data/imzml-examples/` (one dir per source/modality).
- Host e2e corpus index: `mzPeakConverter/tests/corpus.tsv`.
- Vendor-CI download manifest (exact URLs): `mzPeakConverter/tools/vendor_ci_manifest.tsv`.
