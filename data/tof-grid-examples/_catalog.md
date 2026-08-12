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

### MSV000090684
SCIEX <b>TripleTOF 6600</b> — SWATH/DIA <b>BioID</b> proximity-labelling map of nuclear bodies in human cells (Dyakov et al. 2023); one run of a 334-sample deposit. 1.1 GB <code>.wiff</code> → 0.74 GB mzPeak (66%). Filename records the instrument (<code>TOF6600</code>). MassIVE MSV000090684.

### MSV000093587
SCIEX QTOF (model not stated in the deposit) — SWATH/DIA lung proteome of CD-1 mouse offspring after developmental <b>PFAS</b> exposure (PFOS/PFOA/PFHxS mixture). 1.1 GB <code>.wiff</code> → 0.75 GB mzPeak (68%). MassIVE MSV000093587.

### MSV000095995
SCIEX <b>ZenoTOF 7600</b> — <b>top-down</b> proteomics platform with electron-activated dissociation (EAD), reduced RNase B measured in MRM-HR. 0.08 GB <code>.wiff</code>+<code>.wiff.scan</code>+<code>.wiff2</code> → 0.05 GB mzPeak (65%); the native SCIEX reader recovers the uniform-<i>m/z</i> flight-time grid. MassIVE MSV000095995.

### PXD011326
SCIEX <b>TripleTOF 6600</b> — SWATH/DIA proteomics of an <b>iPSC model of early-onset Parkinson's disease</b> (<i>Homo sapiens</i>). 1.75 GB <code>.wiff</code>+<code>.wiff.scan</code> → 1.09 GB mzPeak (62%). Filename records the instrument (<code>SWATH_6600</code>). PRIDE PXD011326.

### PXD071869
SCIEX <b>ZenoTOF 7600</b> — SWATH/DIA benchmarking of biomanufacturing pipelines in <i>Halomonas bluephagenesis</i> and <i>E. coli</i>; the study compares five DIA platforms and this is its SCIEX arm. 2.41 GB <code>.wiff</code>+<code>.wiff.scan</code>+<code>.wiff2</code> → 1.95 GB mzPeak (81%). PRIDE PXD071869.
