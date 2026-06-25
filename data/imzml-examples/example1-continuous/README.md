# Example 1 — continuous

**Source:** ms-imaging.org official "Example Files" (Schramm et al. 2012), via the
`github.com/beny/imzml` mirror (the official page is JS-gated with no stable direct links).
**URL:** https://raw.githubusercontent.com/beny/imzml/master/data/
**Reconstructed by:** `scripts/fetch-examples.sh imzml-examples` (this directory is git-ignored).

Canonical smallest valid imzML file (3×3 pixels), **continuous** mode — a single shared m/z axis
for all pixels. Ideal for fast continuous-path round-trip unit tests.

## Files

| File | Bytes | Role |
|---|--:|---|
| `Example_Continuous.imzML` | 23,129 | XML metadata + spectrum index |
| `Example_Continuous.ibd` | 335,976 | binary m/z + intensity sidecar (UUID-linked to the imzML) |

See [`docs/CORPUS.md`](../../../docs/CORPUS.md) for the full corpus inventory.
