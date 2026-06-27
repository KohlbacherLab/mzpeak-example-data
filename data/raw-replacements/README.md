# raw-replacements

Small public **vendor raw** inputs that stand in for files whose native readers
can't run on Apple Silicon — they exercise the native Bruker / SCIEX / Waters
reader paths on a CI box. Dir names encode `vendor-...__ACCESSION`; `results.tsv`
carries the raw → mzML → mzPeak sizes/timings.

These are **locally-derived subsets** (truncated for fast CI), so `build_data.sh` does
**not** rebuild them bit-for-bit — recreate from the parent accession per the provenance in:
[`../../docs/CORPUS.md`](../../docs/CORPUS.md).

## ⚠️ Actual vendor: Thermo

Despite the `bruker-*`/`sciex-*`/`waters-*` directory names, **all `*-sub__*` contents are Thermo**
(`.raw` with the `Finnigan` header; mzML via ThermoRawFileParser). They are Thermo placeholder
substitutes for the named vendors. Content-based routers classify these as Thermo; do not trust the
label. See [`../../docs/CORPUS.md`](../../docs/CORPUS.md) → Known mislabeled entries.
