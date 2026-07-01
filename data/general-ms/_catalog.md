---
slug: general-ms
title: General MS Data
icon: 📈
accent: #1558d6
imaging: false
order: 1
---

Non-imaging LC-/GC-MS instrument-vendor examples (Thermo, Bruker, SCIEX, Agilent, Shimadzu, Waters) — published mzML converted to mzPeak.

<b>Provenance.</b> Openly published runs from <b>PRIDE</b>, <b>MetaboLights</b>, <b>MassIVE</b> and <b>Zenodo</b> spanning 6 vendors and the major analyzer classes — Orbitrap, Q-TOF / UHR-QTOF, FT-ICR, pure ion trap, triple-quad (SRM/MRM), QqLIT, TIMS &amp; DTIMS ion mobility, DIA, and GC electron-ionization. Each dataset below names its accession and source publication.

## datasets

### agilent-6490-triplequad
PRIDE PXD041762 · Agilent 6490 triple-quad, SRM/dMRM (COVID-19 plasma).

### agilent-6560-dtims-imqtof
Zenodo 18481720 · Agilent 6560 IM-QTOF — drift-tube ion mobility (DTIMS), CE-MS standard mix.

### agilent-8890-gc-ei
MetaboLights MTBLS11550 · Agilent 8890 GC / 7000D — electron-ionization GC-MS.

### agilent-qtof
Zenodo 18502866 · Agilent 6490 triple-quad dMRM standard mix (chromatogram-only). <i>Note: directory name is legacy; the instrument is a QqQ, not a Q-TOF.</i>

### bruker-impact-ii-qtof
MetaboLights MTBLS12824 · Bruker impact II UHR-QTOF.

### bruker-microtof-q2
MetaboLights MTBLS520 · Bruker micrOTOF-Q II ESI-QTOF (bryophyte seasonal metabolomics; Peters et al. 2018).

### bruker-timstof-pro
MassIVE MSV000101607 · Bruker timsTOF Pro — PASEF / TIMS ion mobility.

### sciex-qtrap-6500
PRIDE PXD066465 · SCIEX QTRAP 6500 — scout-triggered MRM (host-cell proteins).

### sciex-tripletof-6600
Zenodo 17416537 · SCIEX TripleTOF 6600 — DIA / SWATH.

### sciex-zenotof-7600
MassIVE MSV000095995 · SCIEX ZenoTOF 7600 — EAD / Zeno top-down (Searfoss et al. 2025).

### shimadzu-lcms-9030-qtof
MetaboLights MTBLS13204 · Shimadzu LCMS-9030 Q-TOF (seaweed metabolomics).

### waters-pda-uv
ProteoWizard Waters vendor-reader test data · Waters ACQUITY UPLC <b>PDA</b> — the corpus's <b>UV / photodiode-array exemplar</b>: ProteoWizard read the PDA function from a MassLynx <code>.raw</code> and wrote <code>wavelength array</code> (190–500 nm) + <code>electromagnetic radiation</code> (absorption) spectra. Demonstrates mzPeak's UV <code>wavelength_spectra</code> facet — the rare case of UV spectra carried inside the mzML.

### waters-synapt-g2si-hdmse
MetaboLights MTBLS812 · Waters SYNAPT G2-Si HDMS — <b>HDMSe traveling-wave ion mobility</b> (TWIMS); LC-IMS-MS metabolomics of pancreatic-cancer cell lines (Drabik et al.). Per-spectrum drift time (MS:1002476) — the corpus's Waters ion-mobility exemplar, alongside Agilent DTIMS and Bruker timsTOF PASEF.

### thermo-fusion-lumos
PRIDE PXD008952 · Thermo Orbitrap Fusion Lumos — CPTAC NCI-7 TMT (Clark et al. 2018).

### thermo-ltq-ft-ultra-fticr
MetaboLights MTBLS3512 · Thermo LTQ FT Ultra — FT-ICR (marine dissolved organic matter; Liu et al. 2020).

### thermo-ltq-orbitrap-velos
PRIDE PXD000001 · Thermo LTQ Orbitrap Velos — TMT “Erwinia” spike-in, the <b>first ProteomeXchange dataset</b> (Gatto &amp; Christoforou 2013).

### thermo-ltq-xl-iontrap
PRIDE PXD059878 · Thermo LTQ XL — pure linear ion trap (PC4 acetylation; Agrawal et al. 2025).

### thermo-orbitrap-astral
MassIVE MSV000100943 · Thermo Orbitrap Astral — high-throughput DIA plasma proteomics (Coon lab 2025).

### thermo-qexactive-plus
Zenodo 17549994 · Thermo Q Exactive Plus (IBDMDB teaching re-deposit).

### waters-xevo-g2s-qtof
MetaboLights MTBLS1129 · Waters Xevo G2-XS QTof — label-free metabolomics (colon cancer; Cai et al. 2020); also our SDRF fixture.

### MTBLS11742
MetaboLights · Agilent 5977B MSD — flux GC-MS, native vendor raw `.D` (doi:10.1038/s41586-025-08635-6). Broad-vendor demonstrator (raw only).

### MTBLS243
MetaboLights · Agilent 6490 Triple Quadrupole — dynamic-MRM metabolomics, native vendor raw `.d`. Broad-vendor demonstrator (raw only).

### PXD076861
PRIDE · Bruker impact HD — native MS, vendor raw `.d`. Broad-vendor demonstrator (raw only).

### PXD022801
PRIDE / iProX · SCIEX QTRAP 6500+ — MRM metabolome, vendor raw `.wiff`. Broad-vendor demonstrator (raw only).

### PXD065872
PRIDE / jPOST · SCIEX TripleTOF 6600 — SWATH/DIA, vendor raw `.wiff`. Broad-vendor demonstrator (raw only).

### PXD053710
PRIDE · SCIEX ZenoTOF 7600 — Zeno-SWATH exposome, vendor raw `.wiff`. Broad-vendor demonstrator (raw only).

### MTBLS432
MetaboLights · Shimadzu LCMS-IT-TOF — metabolome, native vendor raw `.lcd`. Broad-vendor demonstrator (raw only).

### PXD076001
PRIDE / iProX · Thermo Orbitrap Astral — DIA, native vendor raw `.raw`. Broad-vendor demonstrator (raw only).

### PXD045201
PRIDE · Thermo Orbitrap Eclipse — top-down, native vendor raw `.raw`. Broad-vendor demonstrator (raw only).

### PXD059353
PRIDE · Waters Synapt G2-Si — HDX MS<sup>E</sup>, vendor raw `.raw`. Broad-vendor demonstrator (raw only).

### PXD073126
PRIDE · Waters Synapt XS — HDDDA ion mobility, vendor raw `.raw`. Broad-vendor demonstrator (raw only).

### MSV000090203
MassIVE · Agilent 6560 Q-TOF — lipidomics, native vendor raw `.d` (MassHunter). Broad-vendor demonstrator (raw only; one representative run).

### MSV000084273
MassIVE · Bruker micrOTOF II — secreted-proteins metabolomics, native vendor raw `.d` (BAF). Broad-vendor demonstrator (raw only; one representative run).

### MSV000099123
MassIVE · Bruker timsTOF Pro 2 — proteomics, native vendor raw `.d` (PASEF TDF). Broad-vendor demonstrator (raw only; one representative run).

### MSV000092457
MassIVE · Bruker timsTOF Pro 2 — metabolome, native vendor raw `.d` (TDF). Broad-vendor demonstrator (raw only; one representative run).

### MTBLS5861
MetaboLights · Shimadzu LCMS-9030 Q-TOF — lipidomics (OAD), native vendor raw `.lcd`. Broad-vendor demonstrator (raw only; one representative run).

### MSV000096674
MassIVE · Thermo Orbitrap Astral — DDA-TMT, native vendor raw `.raw`. Broad-vendor demonstrator (raw only; one representative run).

### PXD018751
PRIDE · Thermo LCQ Deca XP — IEF/SCX/RPLC proteomics, vendor raw `.raw` (zip). Broad-vendor demonstrator (raw only; one representative run).

### PXD057269
PRIDE · Thermo TSQ Altis — SRM, vendor raw `.raw`. Broad-vendor demonstrator (raw only; one representative run).

### PXD044023
PRIDE · Bruker amaZon ETD — GeLC-MS, vendor raw `.d` (zip). Broad-vendor demonstrator (raw only; one representative run).
