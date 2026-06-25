# mzML example datasets

Public **non-imaging** mzML datasets spanning a broad variety of instruments, one directory per
instrument. Used by `mzPeakConverter` to exercise the plain-`.mzML` → mzPeak conversion path (the
imaging imzML corpus lives in `../imzml-examples/`). **This directory is git-ignored**
(`data/mzML-examples/` in `.gitignore`) — large binary research data, not committed.

Each instrument directory has its own `README.md` naming the exact source, URL, and file bytes.

Total: ~10.0 GB · 18 instrument directories · 18 `.mzML` files (core 9 + extended 9).

### Core 9 — broad LC-MS instrument sweep (~9.6 GB)

| Directory | Instrument (model) | Source | Size |
|---|---|---|--:|
| `agilent-qtof` | Agilent 6490 triple quad (QqQ; MassHunter dMRM; chromatogram-only) — dir name is a misnomer, see note | Zenodo 18502866 | 2.4 MB |
| `bruker-microtof-q2` | Bruker micrOTOF-Q II (QTOF) | MetaboLights MTBLS520 | 59 MB |
| `waters-xevo-g2s-qtof` | Waters Xevo G2-XS QTof (dir name says G2-S, see note) | MetaboLights MTBLS1129 | 86 MB |
| `thermo-qexactive-plus` | Thermo Q Exactive Plus (Orbitrap) | Zenodo 17549994 | 254 MB |
| `sciex-tripletof-6600` | Sciex TripleTOF 6600 | Zenodo 17416537 | 255 MB |
| `thermo-ltq-orbitrap-velos` | Thermo LTQ Orbitrap Velos | PRIDE PXD000001 | 450 MB |
| `thermo-fusion-lumos` | Thermo Orbitrap Fusion Lumos | PRIDE PXD008952 | 617 MB |
| `bruker-timstof-pro` | Bruker timsTOF Pro (PASEF / ion mobility) | MassIVE MSV000101607 | 1.45 GB |
| `thermo-orbitrap-astral` | Thermo Orbitrap Astral (DIA) | MassIVE MSV000100943 | 6.1 GB |

### Extended 9 — new vendor / analyzer classes / modalities (~407 MB)

| Directory | Instrument (model) | New axis | Source | Size |
|---|---|---|---|--:|
| `shimadzu-lcms-9030-qtof` | Shimadzu LCMS-9030 Q-TOF | **new vendor** | MetaboLights MTBLS13204 | 38 MB |
| `agilent-8890-gc-ei` | Agilent 8890 GC / 7000D | **GC-MS / EI** | MetaboLights MTBLS11550 | 17 MB |
| `agilent-6490-triplequad` | Agilent 6490 Triple Quad | **QqQ / SRM** | PRIDE PXD041762 | 5.5 MB |
| `sciex-qtrap-6500` | Sciex QTRAP 6500 | **QqLIT / MRM** | PRIDE PXD066465 | 3.1 MB |
| `agilent-6560-dtims-imqtof` | Agilent 6560 IM-QTOF | **DTIMS** | Zenodo 18481720 | 3.4 MB |
| `thermo-ltq-ft-ultra-fticr` | Thermo LTQ FT Ultra | **FT-ICR** | MetaboLights MTBLS3512 | 32 MB |
| `thermo-ltq-xl-iontrap` | Thermo LTQ XL | **pure ion trap** | PRIDE PXD059878 | 182 MB |
| `bruker-impact-ii-qtof` | Bruker impact II | UHR-QTOF line | MetaboLights MTBLS12824 | 33 MB |
| `sciex-zenotof-7600` | Sciex ZenoTOF 7600 | newest Sciex (EAD) | MassIVE MSV000095995 | 94 MB |

## Reconstruct on demand

```bash
bash scripts/fetch-examples.sh mzML-examples
```

Idempotent (skips files already present), downloads smallest-first. PRIDE / Zenodo / EBI-FTP
support resume (`curl -C -`); the two **MassIVE** files (Astral, timsTOF) do **not** support HTTP
Range, so they re-download whole on each attempt — let them finish in one go.

## Notes

- These are **openly shared public research datasets** (PRIDE / MassIVE / Zenodo / MetaboLights),
  used here only as conversion test inputs. Cite the original deposits when reusing.
- Coverage spans **6 vendors** (Thermo, Bruker, Sciex, Waters, Agilent, Shimadzu) and analyzer/
  modality classes: Orbitrap, Q-TOF / UHR-QTOF, FT-ICR, pure ion trap, triple-quadrupole (SRM),
  QqLIT, ion mobility (TIMS + DTIMS), DIA, and GC-MS / electron ionization.
- The `agilent-qtof` file is a **chromatogram-only** dMRM acquisition (0 spectra, 138 chromatograms);
  `agilent-6490-triplequad` and `sciex-qtrap-6500` carry **SRM/MRM chromatograms**.
- **Directory-name caveats (kept to preserve the StackIT S3 layout):** two slugs disagree with the
  verified in-file model. `agilent-qtof` is an Agilent **6490 triple quad (QqQ)**, *not* a Q-TOF
  (in-file `instrument model="TandemQuadrupole"`, three quadrupole analyzers). `waters-xevo-g2s-qtof`
  is a Waters Xevo **G2-XS** QTof, *not* G2-S (the in-file Waters model field is empty; G2-XS comes
  from the MetaboLights MTBLS1129 record). See `docs/CORPUS.md` → Directory-name caveats.
- **Known gap:** no public mzML preserves **Waters TWIMS / Cyclic** ion mobility (vendor RAW only) —
  see `docs/CORPUS.md` for details.
- A committed tiny smoke-test fixture also lives at `tests/fixtures/mzml/tiny.pwiz.1.1.mzML`.

Full provenance + direct URLs: [`docs/CORPUS.md`](../../docs/CORPUS.md).
