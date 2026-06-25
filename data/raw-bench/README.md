# raw-bench

Vendor **raw** files kept as a size/speed **benchmark** reference: raw → mzML →
mzPeak, with conversion timings. One dir per instrument (accession in the name).
`results.tsv` (generated externally by the converter e2e, not by this repo) records `raw_bytes / mzml_bytes / mzpeak_bytes / *_secs / status`.

SCIEX/Shimadzu/Bruker rows are `BLOCKED_APPLE_SILICON_needs_msconvert` — their
native readers need Windows or ProteoWizard. Thermo `.raw` converts everywhere
(.NET runtime). `build_data.sh` re-fetches the raws and re-runs the benchmark
where the platform allows. See [`../../docs/CORPUS.md`](../../docs/CORPUS.md).
