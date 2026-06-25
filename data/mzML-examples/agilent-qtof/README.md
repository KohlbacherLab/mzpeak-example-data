# Agilent 6490 triple quad (MassHunter dMRM)

**Instrument:** Agilent **6490 triple quadrupole (QqQ)** — dynamic MRM (dMRM), **chromatogram-only**
acquisition. In-file proof: `userParam instrument model="TandemQuadrupole"` + three
`MS:1000081 quadrupole` analyzers, MassHunter 7.0. (The "6490" model number is from the Zenodo
deposit; the file names only "TandemQuadrupole".)
**Directory-name caveat:** the slot is named `agilent-qtof` but the instrument is a **triple quad,
not a Q-TOF** — the name predates the metadata check and is kept to preserve the StackIT S3 layout
(the obvious correct name `agilent-6490-triplequad` is already used by a separate PXD041762 entry).
**Source:** Zenodo record **18502866**.
**URL:** https://zenodo.org/api/records/18502866/files/MRM-standmix-5.mzML/content
**Reconstructed by:** `scripts/fetch-mzml-examples.sh` (this directory is git-ignored).

A useful edge case: **0 spectra, 138 chromatograms** — exercises the writer's chromatogram facet.

## Files

| File | Bytes | Role |
|---|--:|---|
| `MRM-standmix-5.mzML` | 2,390,872 | indexed mzML (chromatogram-only) |

See [`docs/CORPUS.md`](../../../docs/CORPUS.md) for the full corpus inventory.
