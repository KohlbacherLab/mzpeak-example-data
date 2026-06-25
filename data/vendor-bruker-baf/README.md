# vendor-bruker-baf

Bruker **BAF** `.d` acquisitions (Q-TOF; peak arrays behind the `baf2sql_c` SDK)
for the native BAF reader. Public deposit: MetaboLights **MTBLS18**
(`LTI225-41-3neg_1-D,5_01_24321.d`) — see [`../../docs/CORPUS.md`](../../docs/CORPUS.md).

BAF reading needs `libbaf2sql_c.so` (Linux) / `baf2sql_c.dll` (Windows) at
runtime, discovered via `--sdk-lib` or `$TIMSDATA_LIB_DIR` (e.g. a ProteoWizard
`pwiz-bin` dir). No macOS support. `build_data.sh` fetches + converts where the
SDK is available; binaries git-ignored.
