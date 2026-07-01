# Removed datasets

Datasets that were removed from the corpus, with the reason. Removing a dataset means: its
descriptor is deleted from `data/<tile>/<id>/`, its data is purged from `s3://v09/<tile>/<id>/`,
and it is dropped from the tile on the next `build-corpus-site.sh` rebuild.

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
