# Zenodo 10084132 — LTP-MSI (chilli)

**Source:** Zenodo record **10084132** ("mzML/imzML mass spectrometry imaging test data"),
collection `imzML_LTP.zip`.
**Record:** https://zenodo.org/records/10084132
**ZIP:** https://zenodo.org/api/records/10084132/files/imzML_LTP.zip/content
**Reconstructed by:** `scripts/fetch-examples.sh imzml-examples` (this directory is git-ignored).

Low-temperature-plasma (LTP) mass spectrometry imaging of a chilli sample. Files live under
`imzML_LTP/`.

## Files

| File | Bytes | Role |
|---|--:|---|
| `imzML_LTP/ltpmsi-chilli.imzML` | 11,612,702 | XML metadata + spectrum index |
| `imzML_LTP/ltpmsi-chilli.ibd` | 369,835,008 | binary m/z + intensity sidecar |
| `imzML_LTP/CHJ2.png` | 358,798 | sample photo (optical view) |
| `imzML_LTP/130704_IMGCHJ2.jpg` | 295,479 | the **same** optical view in a second format |

> The two image files are *not* referenced inside the imzML (imzML 1.1 has no standard slot for
> optical images); they are sidecar-by-convention. They are two encodings of one view, **not** two
> distinct optical modalities — for the genuine multi-optical case see
> `../zenodo-18187395-GBM-multimodal`.

See [`docs/CORPUS.md`](../../../docs/CORPUS.md) for the full corpus inventory.

## Known issue — stale `.ibd` SHA-1 in the published imzML (corrected locally 2026-06-06)

The imzML as distributed on Zenodo declares an **`.ibd` SHA-1 that does not match the `.ibd` it
ships with** — a publisher-side inconsistency, not a download/corruption problem:

| | value |
|---|---|
| imzML `IMS:1000091` "ibd SHA-1" (as published) | `173bdf1701ab791b462fdfcbfd2f4ad6c5b26168` ← **stale/wrong** |
| actual `ltpmsi-chilli.ibd` SHA-1 (ours == fresh Zenodo) | `0cba4527f647046b56057c9ceaa0d3326802573a` |

**Verified** the `.ibd` is the correct, complete sidecar (only the declared hash is wrong):
- A fresh `imzML_LTP.zip` re-download from Zenodo is **byte-identical** to the local copy (same SHA-1, same 369,835,008 bytes).
- The imzML's declared UUID (`IMS:1000080` = `686ec248523749d8a17590dde78ab130`) **matches** the `.ibd`'s 16-byte header → correct pairing.
- All 8,332 declared external arrays fit exactly within the file (`max(offset+length) == file size`) → complete, right layout.

The converter's integrity preflight (correctly) hard-fails on the checksum mismatch.

**Fix applied here:** the local copy's imzML `IMS:1000091` value was corrected to the actual `.ibd`
SHA-1 (`0cba4527…`); the `.ibd` itself is **untouched**. The original (published) line was:

```xml
<cvParam cvRef="IMS" accession="IMS:1000091" name="ibd SHA-1" value="173bdf1701ab791b462fdfcbfd2f4ad6c5b26168"/>
```

Alternatively, the unmodified file can be converted with the converter's
`--ignore-incorrect-checksum` flag (downgrades a checksum mismatch to a warning; the UUID match is
still enforced). Worth reporting the stale checksum upstream to the dataset authors.
