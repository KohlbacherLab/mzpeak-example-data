# Removed datasets

Datasets that were removed from the corpus, with the reason. Removing a dataset means: its
descriptor is deleted from `data/<tile>/<id>/`, its data is purged from `s3://v09/<tile>/<id>/`,
and it is dropped from the tile on the next `build-corpus-site.sh` rebuild.

## sdrf-examples/*/mzml — orphaned SDRF demonstrator archives (removed 2026-07-28)

**Reason: no source, unreadable format.** Twelve `.mzpeak` files (~4.8 GB) under
`sdrf-examples/{PXD009909,PXD011799,PXD014145,PXD020187}/mzml/` had no local source and could not be
rebuilt. Their own provenance records why:

```
software           : 0.4.5
conversion options : /private/tmp/.../scratchpad/sdrf-reconvert/70JG_01.mzML
                     -o data/sdrf-examples/PXD009909/mzml/70JG_01.mzpeak --sdrf ...
```

They were produced by converter **v0.4.5** from mzML staged in a **scratch directory that has since
been cleaned**, and the dataset descriptors declare only the `.sdrf.tsv` — the mzML was never a
corpus file. So no raw unit maps to them: they are output without input. Being pre-0.7.0 packed
archives they are also unreadable by the current converter, so they no longer served the SDRF tile.

The descriptors and `.sdrf.tsv` files are **kept**. To restore the demonstrators, re-download the
runs from PRIDE for each accession and convert with `--sdrf <accession>.sdrf.tsv`.

## ims-examples/bruker-timstof-MSV000101607 — duplicate archive (removed 2026-07-28)

**Reason: superseded duplicate.** `Blank(1) Try_Slot1-1_1_8270.mzpeak` (280 MB) sat at the tile root
while the same acquisition also had an archive inside `Blank_Try.d/`. The outer one dated from when
the harness addressed the wrapper directory as the unit; discovery now descends into wrapper `.d`
directories, so the output moved beside the real acquisition. The surviving archive was verified
complete against the TDF (41,175 spectra = `Frames` row count) before the old one was deleted; the
old one was pre-0.7.0 packed and unreadable by the current converter.

## general-ms/MSV000084273 — Bruker micrOTOF II (removed 2026-08-12)

**Reason: incomplete upstream deposit — `analysis.baf_xtr` is missing.** The single unit
`DK-100119 BD_1079-C_Hil_RB2_01_12082.d` (533 MB) carries `analysis.baf` but not the
`analysis.baf_xtr` index that Bruker's `baf2sql` requires to build its SQLite cache. Both readers on
the Windows box fail on it for the same underlying reason:

```
native   : baf2sql_get_sqlite_cache_filename_v2 failed: boost::filesystem::file_size:
           Das System kann die angegebene Datei nicht finden: "...\analysis.baf_xtr"
msconvert: msconvert failed (exit 1)
```

The file is not merely missing locally: the dataset's own descriptor listed all nine files MassIVE
publishes for this acquisition, and `analysis.baf_xtr` is not among them — so re-downloading cannot
fix it. This is the same class as the `MTBLS432` vendor-library gap and the truncated imzML `.ibd`:
no mzPeak can be produced, so the dataset is removed rather than kept as a permanently
unconvertible entry.

Bruker BAF coverage in the corpus is unaffected — `general-ms/bruker-impact-ii-qtof/` still provides
a BAF demonstrator. Source URLs, if this is ever worth retrying with a complete deposit:
`https://massive.ucsd.edu/ProteoSAFe/DownloadResultFile?forceDownload=true&file=f.MSV000084273/raw/DK-100119%20BD_1079-C_Hil_RB2_01_12082.d/…`

## general-ms/MTBLS432 — Shimadzu LCMS (removed 2026-07-28)

**Reason: unsupported `.lcd` variant.** `6-wk_HZ_CC_male_37_74__30min_pos-neg_100.lcd`
(7,389,184 bytes, intact) is rejected independently by **both** readers on the Windows box:

```
native  : resolving glue export Open: Unknown error code: 0x8000211D
msconvert: [ShimadzuReader::ctor] LoadData error: E_UNSUPPORTEDFILE
```

ProteoWizard's own `ShimadzuReader` reporting `E_UNSUPPORTEDFILE` is the decisive part — the
installed LabSolutions runtime does not recognise this `.lcd` variant, so the failure is a
vendor-library coverage gap rather than anything in the converter. No mzPeak can be produced from
it, so the dataset is removed rather than kept as a permanently unconvertible entry. If a newer
LabSolutions runtime is ever installed on the box, this one is worth re-testing.

**Retested 2026-08-20 at mzpeak-convert 0.7.8 — removal upheld.** The `native` line above was a
MISDIAGNOSIS: `0x8000211D` was `AmbiguousMatchException` from an overloaded export in our own glue,
which hit *every* `.lcd` regardless of content, so the native lane had never actually reached this
file. That bug is fixed in v0.7.8 and the native lane is now verified working on other Shimadzu data
(LCMS-9030, 2,101 spectra, m/z matching msconvert). Re-downloaded from MetaboLights
(7,389,184 bytes, byte-identical to the size recorded above) and retested:

```
native   : LoadData error: E_UNSUPPORTEDFILE
msconvert: [ShimadzuReader::ctor] LoadData error: E_UNSUPPORTEDFILE
```

Both lanes call the same vendor `LoadData`, and both reject it. Two further `.lcd` files from the
same study (`..._1_63__30min_pos-neg_26.lcd`, `..._3_64__30min_pos-neg_76.lcd`) fail identically, so
this is a study-wide format variant the installed LabSolutions runtime cannot read, not one bad file.
The `.lcd` files are still published under `FILES/` (the study's file API omits that subtree), so the
data is re-fetchable if a newer runtime ever lands. Note the study also ships ANDI-MS `.CDF` siblings
per run, which this converter does not read.

## general-ms/PXD000155 — Thermo LTQ Velos (removed 2026-07-01)

**Reason: inconvertible `.raw`.** The single file `20100625_mAbBBA1b_JAA_51.raw`
(16,809,984 bytes; valid Finnigan header; size matches PRIDE's record, so not a truncated download)
cannot be opened by ThermoFisher's `RawFileReader`:

```
error: converting … as a Raw File!
ThermoFisher.CommonCore.RawFileReader.Facade.RandomAccessRawFileLoader.InitialDeviceLists()  -> exit 1
```

Both the native reader **and** the ProteoWizard/msconvert path (which uses the same RawFileReader)
fail identically, so the file itself is the problem — an old/edge-case 2010 LTQ Velos `.raw` that the
modern reader rejects. No mzPeak can be produced from it, so the dataset was removed rather than kept
as an unconvertible raw-only entry.

## tof-grid-examples/PXD041903 — Agilent Q-TOF (removed 2026-07-13)

**Reason: centroid-only at source.** `20190423_Alex7.d` has no profile data (`MSProfile.bin`
absent / zero-length), so msconvert can only emit **centroid**. The TOF-Grid tile exists for the
integer flight-time **profile** grid, which a centroid-only run cannot provide — no profile mzPeak
can be produced for its purpose. Removed rather than kept as a centroid-only raw entry that doesn't
serve the grid-encoding evaluation.

## tof-grid-examples/PXD059765 — Agilent Q-TOF (removed 2026-07-13)

**Reason: centroid-only at source.** Same as PXD041903 — `CON1_2.d` is centroid-only (no profile
`MSProfile.bin`), so it yields only a centroid mzML/mzPeak and cannot serve the profile flight-time
grid the TOF-Grid tile targets. Removed rather than kept as a centroid-only raw entry.

## tof-grid-examples/PXD059108 — Bruker microTOF-Q BAF (removed 2026-07-13)

**Reason: inconvertible on the hosted CI (out-of-memory / disk).** `lysate_000008.d.zip` is a
**3.87 GB BAF** whose profile mzML deterministically **OOMs / disk-fills the hosted GitHub Actions
runner** while msconvert writes it (confirmed 2×). It cannot be converted within the hosted-runner
limits, so no mzPeak could be produced; removed rather than kept as a raw-only entry.

## general-ms/PXD044023 — Bruker amaZon ETD (removed 2026-07-14)

**Reason: inconvertible — both native and msconvert fail.** `37090_B9-2_20140710003.d` (Bruker
amaZon ETD ion trap, ~80 MB `.d.zip`) cannot be read by the native Bruker BAF reader (`libbaf2sql_c`
returns exit 1) **nor** by ProteoWizard/msconvert (also exit 1, no mzML written) — both attempts run
on the Windows box (converter 0.4.9), including the automatic native→msconvert fallback. The amaZon
is an older ion-trap instrument whose `.d` payload is not a BAF variant either reader accepts, so no
mzPeak can be produced. By contrast the Bruker **impact HD** BAF (PXD076861) reads natively fine — so
this is specific to the amaZon/ion-trap format, not Bruker BAF in general. Removed rather than kept as
an unconvertible raw-only entry. (Re-evaluate if the box converter is upgraded past 0.4.9 — newer
native BAF readers may support it.)

## ims-examples/bruker-timstof-pro — duplicate id, duplicate deposit (removed 2026-08-12)

**Reason: same `id` as general-ms/bruker-timstof-pro, and the same source deposit.** Two datasets
carried the id `bruker-timstof-pro`, one in `general-ms` and one in `ims-examples`. Ids key the data
path, the bucket prefix and the catalog entry, so a duplicate id is a structural fault, not a
cosmetic one. Both cited MassIVE **MSV000101607** (*ZooMS analysis of Phasianidae remains from the
Namjeon shell midden* — timsTOF Pro paleoproteomics) and both declared the same URL
(`f.MSV000101607/peak/SBA415.mzML`), yet held different archives: `SBA415.mzpeak` (742 MB) here
versus `SBA415(1) Try_Slot1-2_1_8271.mzpeak` (2.15 GB) in general-ms.

The general-ms entry is kept as the Bruker timsTOF vendor-coverage demonstrator. The ion-mobility
tile loses nothing: it still holds four richer TIMS studies (PXD059079 single-cell DIA, PXD076703
FLAG co-IP, PXD078573 cross-linking, PXD079300 extracellular vesicles) plus FAIMS, cyclic-IMS,
TWIMS and DTIMS examples.

## ims-examples/bruker-timstof-MSV000101607 — blank run (removed 2026-08-12)

**Reason: it is a blank.** The archive was built from `Blank_Try.d/Blank(1) Try_Slot1-1_1_8270.d` —
an instrument blank with no sample, from the same MSV000101607 deposit as the entry above. It was
verified complete (41,175 spectra = TDF frames) but a blank demonstrates nothing about ion mobility
that a real acquisition does not demonstrate better, and it was the third entry drawn from one
deposit. Removed in favour of the four sample-bearing TIMS studies in the tile.

## general-ms/sciex-zenotof-7600 — same acquisition as tof-grid-examples/MSV000095995 (removed 2026-08-12)

**Reason: the same run in two tiles.** Both entries published
`20240826_RNAseB_Reduced_50ngul_1ul_MRM_03` from MassIVE **MSV000095995** (*Establishing a Top-Down
Proteomics Platform on a Time-of-Flight Instrument with Electron-Activated Dissociation*), so one
acquisition was counted twice in the corpus statistics and the compression figures.

The TOF-Grid copy is kept: that tile exists for the integer flight-time grid, and this run is its
ZenoTOF reference where the native SCIEX reader recovers the uniform-*m/z* lattice. SCIEX remains
covered in general-ms by `sciex-qtrap-6500` and `sciex-tripletof-6600`.

## general-ms/agilent-6560-dtims-imqtof — duplicate id, same run as the ims copy (removed 2026-08-12)

**Reason: identical dataset in two tiles.** `general-ms` and `ims-examples` both carried the id
`agilent-6560-dtims-imqtof` publishing the same file (`CEMS_10ppm.mzML` from Zenodo 18481720, a
CE-MS standard mix) and byte-identical 326,308-byte archives — a duplicate id and a double count in
the corpus statistics.

The ion-mobility copy is kept: the Agilent 6560 is a **drift-tube** IM-QTOF and this is the tile's
only DTIMS reference. Agilent stays covered in general-ms by `agilent-qtof`,
`agilent-6490-triplequad`, `agilent-8890-gc-ei` and MTBLS11742.

## general-ms/* — undescribed bucket orphans (purged 2026-08-12)

**Reason: data in the bucket with no descriptor.** The corpus is descriptor-driven — the site, the
catalogs and `ratios.tsv` are all generated from the bucket, so any prefix without a matching
`data/<tile>/<id>/<id>.yaml` renders as a dataset row with no description and inflates the corpus
statistics. Four such prefixes were purged (23.4 GB):

* `MSV000084273` (0.56 GB) and `MTBLS432` (0.01 GB) — both retired earlier (see entries above), but
  only the descriptors were deleted; the bucket prefixes were left behind and kept appearing.
* `thermo-orbitrap-astral-PXD049028` (22.4 GB: 22.1 GB `.raw` + 235 MB `.mzML`) — an Astral DIA run
  of HAP1 cells uploaded during the compression-benchmark work and never described. The corpus keeps
  its described Astral example, `thermo-orbitrap-astral` (MassIVE MSV000100943, Coon-lab plasma DIA).
* `thermo-qexactive-plus-PXD077619` (0.48 GB) — never described, no tracked descriptor in git.

Retiring a dataset means deleting the descriptor **and** purging `s3://v09/<tile>/<id>/`; doing only
the first leaves exactly this kind of ghost row.
