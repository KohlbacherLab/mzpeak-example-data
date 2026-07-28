# Removed datasets

Datasets that were removed from the corpus, with the reason. Removing a dataset means: its
descriptor is deleted from `data/<tile>/<id>/`, its data is purged from `s3://v09/<tile>/<id>/`,
and it is dropped from the tile on the next `build-corpus-site.sh` rebuild.

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
