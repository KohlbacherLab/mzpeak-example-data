# TOF Grid-Profile Test Corpus

Local corpus of raw vendor files from public proteomics repositories, collected to support mzPeak format development and validation. All data are from QTOF instruments operated in SWATH/DIA (grid/window-acquisition) mode, producing the two-dimensional *m/z × scan* data structure that mzPeak's grid encoding targets.

**Total on-disk size:** ~18 GB  
**Collected:** 2026-06-16  
**Sources:** PRIDE Archive (EBI) and MassIVE (UCSD)

---

## Contents

### SciEx SWATH files (`.wiff` / `.wiff.scan` / `.wiff2`)

| Study | Instrument | Files | Size | Source | Note |
|-------|-----------|-------|------|--------|------|
| [PXD071869](https://www.ebi.ac.uk/pride/archive/projects/PXD071869) | TripleTOF 6600 | `08_SWATH_1E_1H.wiff` + `.wiff.scan` + `.wiff2` | ~2.4 GB | PRIDE | Three-file SciEx run (dual-window) |
| [PXD011326](https://www.ebi.ac.uk/pride/archive/projects/PXD011326) | TripleTOF 6600 | `VD_170826_SWATH_6600_PD_15.wiff` + `.wiff.scan` | ~2.6 GB | PRIDE | Classic two-file SciEx run |
| [MSV000090684](https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?task=MSV000090684) | TripleTOF 6600 | `11410_DGCR8_CBF_BR2_BioID_20181022_TOF6600_SWATH.wiff` + `.wiff.scan` | ~5.4 GB | MassIVE | Large BioID-SWATH run |
| [MSV000090136](https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?task=MSV000090136) | TripleTOF 6600 | `17_16_hpr56_ko_YMR295C_4444_-0.04.wiff` + `.wiff.scan` | ~2.2 GB | MassIVE | Yeast proteome SWATH |
| [MSV000093587](https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?task=MSV000093587) | TripleTOF | `Sample049.wiff` + `.wiff.scan` | ~1.8 GB | MassIVE | |

**File format notes:**
- `.wiff` — small XML/binary metadata wrapper (~5–18 MB); must travel with `.wiff.scan`.
- `.wiff.scan` — main binary mass spectra (~1.8–5.4 GB per run).
- `.wiff2` — second scan file present on some newer acquisitions; same reader handles both.
- These three files must always be kept together as a unit; a `.wiff` without its `.wiff.scan` is unreadable.

### Agilent MassHunter QTOF files (`.d` folders / `.d.zip`)

| Study | Instrument | Files | Size | Source | Note |
|-------|-----------|-------|------|--------|------|
| [PXD059108](https://www.ebi.ac.uk/pride/archive/projects/PXD059108) | Agilent QTOF | `lysate_000008.d.zip` | ~3.9 GB | PRIDE | Largest Agilent run |
| [PXD059765](https://www.ebi.ac.uk/pride/archive/projects/PXD059765) | Agilent QTOF | `CON1_2.d.zip` | ~1.2 GB | PRIDE | |
| [PXD041903](https://www.ebi.ac.uk/pride/archive/projects/PXD041903) | Agilent QTOF | `20190423_Alex7.d.zip` | ~442 MB | PRIDE | |

**File format notes:**
- Agilent raw data is a `.d` directory containing `AcqData/` with binary files: `MSProfile.bin` (profile spectra), `MSPeak.bin` (centroided peaks), `MSScan.bin` (scan index), plus XML metadata.
- PRIDE deposits these as `.d.zip` archives; unzip before reading.
- Key binary files: `MSProfile.bin` (largest, profile mode), `MSPeak.bin` (centroided), `MSScan.bin` (scan metadata index).

---

## Coverage gaps

Two MassIVE Agilent studies were targeted but their data files returned HTTP 500/errors at download time and are not present:

- **MSV000094882** — `Alexander_023_B_30x_pos_121820_136.d`: small metadata files present, large binaries (`MSProfile.bin` 1.79 GB, `MSPeak.bin` 258 MB) missing due to server errors.
- **MSV000084856** — `Au010-VOC1-D1.D`: entire folder missing (all files returned rc=22).

The three PRIDE Agilent studies above are sufficient for format validation purposes.

---

## Usage

These are raw vendor binary files. To read them in Python:

```python
# SciEx .wiff files
import pyteomics.wiff  # or use ProteoWizard msconvert to convert to mzML

# Agilent .d folders (unzip .d.zip first)
# Use ProteoWizard msconvert, agilent.d reader, or pyms-agilent
```

For mzPeak development, convert via ProteoWizard `msconvert` to mzML first, then use the mzPeak reference implementation to encode as `.mzpeak`.

---

## Provenance

All datasets are from publicly available repositories under open access conditions. Original publications associated with each dataset are linked via the study accession pages above.
