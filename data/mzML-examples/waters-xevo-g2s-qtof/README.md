# Waters Xevo G2-XS QTof

**Instrument:** Waters **Xevo G2-XS** QTof (MassLynx 4.1; 2281 spectra).
**Directory-name caveat:** the slot is named `waters-xevo-g2s-qtof` (off by one sub-model). The
in-file `MS:1000126 "Waters instrument model"` value is **empty**, so the file does not encode the
sub-model — **G2-XS** is the model named by the MetaboLights MTBLS1129 record. The name is kept to
preserve the StackIT S3 layout (and the shared `sdrf-examples/MTBLS1129` fixture slug).
**Source:** MetaboLights study **MTBLS1129**.
**URL:** https://ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/MTBLS1129/FILES/QC01.mzML
**Reconstructed by:** `scripts/fetch-mzml-examples.sh` (this directory is git-ignored).

## Files

| File | Bytes | Role |
|---|--:|---|
| `QC01.mzML` | 85,801,170 | indexed mzML |

See [`docs/CORPUS.md`](../../../docs/CORPUS.md) for the full corpus inventory.
