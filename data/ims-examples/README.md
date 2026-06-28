# ims-examples — Ion Mobility (IMS)

All ion-mobility–separated MS examples, across every IM technology and vendor:

- **TIMS** (Bruker timsTOF SCP/Pro/HT) — PASEF / diaPASEF
- **TWIMS** (Waters Synapt) and **cyclic IMS** (Waters SELECT SERIES)
- **FAIMS** (Thermo Orbitrap + FAIMS Pro)
- **DTIMS** (Agilent 6560 drift tube)

Existing IM datasets were moved here from `mzML-examples` / `raw-examples`; the ProteoWizard
vendor-reader IM fixtures remain in `pwiz-examples`. Catalog + per-file source URLs:
`manifest/ims-demonstrators.tsv` and `manifest/ims-files.tsv`. Rebuild the downloads with
`scripts/fetch-ims.sh` (≤ 2 raw files per study; one 57 GB cyclic file is manifest-only).
