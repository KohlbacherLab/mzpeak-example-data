# Agilent 6560 IM-QTOF — drift-tube ion mobility (DTIMS)

**Instrument:** Agilent **6560** IM-QTOF, **drift-tube ion mobility (DTIMS)**, coupled to an
Agilent 7100 CE front end (CE-MS).
**New axis:** first **drift-tube** ion mobility in the corpus — a distinct IM technology from the
Bruker timsTOF (trapped IM). Verified `MS:1002476 ion mobility drift time` present per spectrum, so
the mobility dimension survives in the mzML.
**Source:** Zenodo **18481720** ("CE-MS test data set").
**URL:** https://zenodo.org/api/records/18481720/files/CEMS_10ppm.mzML/content
**License:** CC-BY-4.0 · public, no login.
**Reconstructed by:** `scripts/fetch-mzml-examples.sh` (this directory is git-ignored).

## Files

| File | Bytes | Role |
|---|--:|---|
| `CEMS_10ppm.mzML` | 3,445,823 | indexed mzML with drift-time arrays (subset: RT 400–900 s, m/z 147–152) |

> The dataset is a deliberately small subset; the `instrument model` cvParam value is left empty
> (model confirmed via the Zenodo record description). Sister file `CEMS_25ppm.mzML` exists.

See [`docs/CORPUS.md`](../../../docs/CORPUS.md) for the full corpus inventory.
