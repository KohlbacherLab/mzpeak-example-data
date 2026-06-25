# Zenodo 10084132 — DESI (colorectal adenoma)

**Source:** Zenodo record **10084132** ("mzML/imzML mass spectrometry imaging test data"),
collection `imzML_DESI.zip`.
**Record:** https://zenodo.org/records/10084132
**ZIP:** https://zenodo.org/api/records/10084132/files/imzML_DESI.zip/content
**Reconstructed by:** `scripts/fetch-imzml-examples.sh` (this directory is git-ignored).

Desorption electrospray ionisation (DESI) imaging — **7 separate colorectal-adenoma sections**,
each in its own folder under `imzML_DESI/ColAd_Individual/`. Every section is a
processed/centroid `.imzML` + `.ibd` pair plus a single `.jpg` sample photo. The folder name and
the `.jpg` name encode the four tissue cores laid out in that acquisition (e.g. `40TopL, 10TopR,
30BottomL, 20BottomR`).

## Files (per section, under `imzML_DESI/ColAd_Individual/<section>/`)

| Section folder | `*-centroid.imzML` | `*-centroid.ibd` | optical `.jpg` |
|---|--:|--:|--:|
| `40TopL,10TopR,30BottomL,20BottomR` | 29,193,361 | 66,051,808 | `10,20,30,40.jpg` 375,033 |
| `80TopL, 50TopR, 70BottomL, 60BottomR` | 30,526,495 | 69,569,296 | `50,60,70,80.jpg` 370,923 |
| `120TopL, 90TopR, 110BottomL, 100BottomR` | 29,409,251 | 58,431,760 | `90,100,110,120.jpg` 402,275 |
| `160TopL, 130TopR, 150BottomL, 140BottomR` | 31,615,966 | 44,981,428 | `130,140,150,160.jpg` 330,837 |
| `200TopL, 170TopR, 190BottomL, 180BottomR` | 27,235,773 | 43,947,940 | `170,180,190,200.jpg` 385,596 |
| `240TopL, 210TopR, 230BottomL, 220BottomR` | 32,798,742 | 68,111,608 | `210,220,230,240.jpg` 392,371 |
| `280TopL, 250TopR, 270BottomL, 260BottomR` | 32,803,926 | 71,420,212 | `250,260,270,280.jpg` 396,630 |

> The `.DS_Store` files that may appear in these folders are macOS Finder cruft, not part of the
> deposit. The `.jpg` is a sample photograph, not referenced inside the imzML.

See [`docs/CORPUS.md`](../../../docs/CORPUS.md) for the full corpus inventory.
