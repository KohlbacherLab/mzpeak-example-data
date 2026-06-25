# Bruker impact II — UHR-QTOF

**Instrument:** Bruker **impact II** Ultra-High-Resolution Qq-TOF (UHR-QTOF), LC-MS, negative-mode
HILIC metabolite profiling. Native Bruker **BAF** → mzML. (The PSI-MS CV groups impact II under the
`Bruker Daltonics maXis series` parent term — that is the expected in-file cvParam.)
**New axis:** Bruker's high-res QTOF line, distinct from the existing timsTOF Pro and micrOTOF-Q II.
**Source:** MetaboLights **MTBLS12824** (exercise-trained human muscle), **HILIC** assay.
**URL:** https://ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/MTBLS12824/FILES/21P0055_Tissue_Georges_NEG_N_01_17471.mzML
**License:** EMBL-EBI / MetaboLights open-access · public, no login.
**Reconstructed by:** `scripts/fetch-examples.sh mzML-examples` (this directory is git-ignored).

## Files

| File | Bytes | Role |
|---|--:|---|
| `21P0055_Tissue_Georges_NEG_N_01_17471.mzML` | 32,866,133 | indexed mzML (Bruker impact II, BAF source) |

> MTBLS12824 is multi-platform — its reverse-phase *lipidomics* runs are on a Thermo Q Exactive
> Plus. Only the negative/positive **HILIC** files (`_N_`) are impact II; this is one of them.

See [`docs/CORPUS.md`](../../../docs/CORPUS.md) for the full corpus inventory.
