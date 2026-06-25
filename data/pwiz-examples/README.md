# pwiz-examples

ProteoWizard **vendor-reader test data** — the `Reader_<Vendor>_Test.data`
fixtures shipped with ProteoWizard (ABI, Agilent, Bruker, Mobilion, Shimadzu,
Thermo, UNIFI, Waters). Each vendor dir holds many small `.mzML` exercising
edge cases (IMS combine, centroiding, MRM, HDMSe, SONAR, …).

These are **ProteoWizard project test assets**, not a public MS deposit. Source
of record: the ProteoWizard test corpus (mirrored on the project object store
under `pwiz-examples/`). `build_data.sh` fetches them and converts every
`.mzML` to `.mzpeak`. ~139 files, sub-MB each — container overhead dominates,
so several `.mzpeak` are larger than their tiny `.mzML` source (expected).

Binaries git-ignored. Full provenance: [`../../docs/CORPUS.md`](../../docs/CORPUS.md).
