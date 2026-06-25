# Thermo Orbitrap Astral (DIA) — PXD049028

**Instrument:** Thermo Orbitrap Astral — single-shot **DIA**, HAP1 cells, 60-min gradient, 2-Th windows.
**Source:** ProteomeXchange **PXD049028** (original `20231206_HAP1_1ug_60min_DIA_2Th_5e4_3p5ms_rep03.raw`,
**22,121,976,843 bytes / 22.12 GB** — the largest single Thermo `.raw` found in a PRIDE + MassIVE survey).
**Conversion:** ThermoRawFileParser `.raw` → profile mzML (`-f 2 --noPeakPicking`) → `mzml2mzpeak`
(744,651 spectra + 1 chromatogram).
**Note:** this is a 2nd Astral entry (distinct from `thermo-orbitrap-astral` / MSV000100943). The 22 GB
`.raw` is **kept on disk** (per the keep-all-RAW policy); the entry holds raw + mzML + mzPeak.

## Files

| File | Bytes | Role |
|---|--:|---|
| `20231206_HAP1_1ug_60min_DIA_2Th_5e4_3p5ms_rep03.raw`    | 22,121,976,843 | vendor RAW (Thermo Astral) — kept on disk |
| `20231206_HAP1_1ug_60min_DIA_2Th_5e4_3p5ms_rep03.mzML`   | 19,714,051,337 | indexed profile mzML (DIA) |
| `20231206_HAP1_1ug_60min_DIA_2Th_5e4_3p5ms_rep03.mzpeak` |  9,177,662,528 | mzPeak |

**Original RAW:** `https://ftp.pride.ebi.ac.uk/pride/data/archive/2024/03/PXD049028/20231206_HAP1_1ug_60min_DIA_2Th_5e4_3p5ms_rep03.raw`

See [`docs/CORPUS.md`](../../../docs/CORPUS.md) for the full corpus inventory.
