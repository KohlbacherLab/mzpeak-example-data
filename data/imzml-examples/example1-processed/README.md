# Example 1 — processed

**Source:** ms-imaging.org official "Example Files" (Schramm et al. 2012), via the
`github.com/beny/imzml` mirror (the official page is JS-gated with no stable direct links).
**URL:** https://raw.githubusercontent.com/beny/imzml/master/data/
**Reconstructed by:** `scripts/fetch-examples.sh imzml-examples` (this directory is git-ignored).

Canonical smallest valid imzML file (3×3 pixels), **processed** mode — each pixel carries its own
m/z array. Ideal for fast processed-path round-trip unit tests.

## Files

| File | Bytes | Role |
|---|--:|---|
| `Example_Processed.imzML` | 23,160 | XML metadata + spectrum index |
| `Example_Processed.ibd` | 604,744 | binary m/z + intensity sidecar (UUID-linked to the imzML) |

See [`docs/CORPUS.md`](../../../docs/CORPUS.md) for the full corpus inventory.
