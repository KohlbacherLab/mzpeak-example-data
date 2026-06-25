# vendor-waters

Real Waters **`.raw`** acquisitions (TWIMS ion mobility) for the native MassLynx
reader and the `--via-msconvert` fallback. Public PRIDE deposits (e.g.
**PXD073666**, Synapt TWIMS) — see [`../../docs/CORPUS.md`](../../docs/CORPUS.md)
for accessions and download URLs.

A `.raw` is a **directory** (`_FUNC*.DAT`, `_HEADER.TXT`, …). Native reading runs
on Windows/Linux with the MassLynx DLLs; elsewhere use `--via-msconvert`.
Binaries git-ignored; `build_data.sh` rebuilds them.
