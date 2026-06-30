---
slug: tof-grid
title: TOF Grid-Profile
icon: 📏
accent: #137775
imaging: false
order: 5
---

Time-of-flight <b>profile</b> runs (SCIEX SWATH/DIA, Bruker microTOF, Agilent QTOF) kept with their vendor RAW and the off-box <code>msconvert</code> → profile mzML → mzPeak chain — the corpus behind mzPeak's flight-time grid-encoding evaluation.

<b>Provenance.</b> QTOF runs acquired in SWATH/DIA (grid/window) mode, the 2-D <i>m/z</i> × scan structure the grid encoding targets. SCIEX TripleTOF 6600 SWATH from PRIDE (PXD071869 · PXD011326) and MassIVE (MSV000090684 · MSV000090136 · MSV000093587); a Bruker microTOF-Q BAF run (PXD059108); and two Agilent QTOF deposits (PXD059765 · PXD041903) that are centroid-only at source and so carry RAW without a profile conversion. Each dataset names its accession; all are openly licensed public deposits.

## datasets

### MSV000090136
SCIEX TripleTOF 6600 yeast SWATH

### MSV000090684
SCIEX TripleTOF 6600 BioID-SWATH (~5.4 GB)

### MSV000093587
TripleTOF SWATH

### MSV000095995
SCIEX ZenoTOF 7600 top-down RNase B, MRM-HR (.wiff+.wiff.scan+.wiff2 from raw/); native SCIEX reader produces the uniform-m/z TOF grid

### PXD011326
SCIEX TripleTOF 6600 SWATH (two-file)

### PXD041903
Agilent Q-TOF profile .d (smallest)

### PXD059108
Agilent Q-TOF profile .d

### PXD059765
Agilent Q-TOF profile .d

### PXD071869
SCIEX TripleTOF 6600 dual-window SWATH (wiff+scan+wiff2)
