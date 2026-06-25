# Vendor RAW corpus: Agilent + SciEX TOF

Real vendor RAW files (NOT converted mzML) for testing the `mzpeak-convert` native
Agilent and SciEX readers, plus the `--via-msconvert` fallback path.

All datasets are public proteomics submissions in the PRIDE archive (EBI). PRIDE
public data is freely available for reuse without restriction (the de-facto
"free, open access" terms of the ProteomeXchange/PRIDE repository; no explicit
per-dataset license file is attached). Cite the originating dataset DOI when used.

Downloaded with `curl -C -` (resume-capable) from the PRIDE HTTPS mirror
(`https://ftp.pride.ebi.ac.uk/...`). Sizes below were verified against the PRIDE
archive REST API (`https://www.ebi.ac.uk/pride/ws/archive/v2/`).

---

## Agilent — `agilent/PXD041315/`

- **Repository / accession:** PRIDE `PXD041315`
- **URL:** https://www.ebi.ac.uk/pride/archive/projects/PXD041315
- **DOI:** 10.6019/PXD041315
- **Vendor / instrument:** Agilent **6545 Q-TOF LC/MS**
- **Experiment:** Shotgun proteomics (*Caenorhabditis elegans*, *Cronobacter
  sakazakii* infection study)
- **Availability / license:** Public PRIDE submission (free reuse). Submission
  type PARTIAL; published 2023-10-13.

### What was downloaded
The raw data is published as per-run ZIP archives, each containing several
Agilent `.d` folders. The smallest archive, `LMV_CS_24_h.zip` (1,229,162,875 B
≈ 1.20 GB), was downloaded and verified (`unzip -t`: no errors), then extracted.
It contained three complete `.d` folders. **One representative folder was kept**;
the ZIP and the two redundant `.d` folders were deleted to keep the corpus lean.

Kept on disk:

```
agilent/PXD041315/LMVCS24HC.d/          (620 MB)
  AcqData/
    MSScan.bin      (3,906,932 B)   <- scan index
    MSProfile.bin   (570,744,189 B) <- profile spectra
    MSPeak.bin      (36,301,064 B)  <- centroided peaks
    MSScan.xsd, MSTS.xml, MSActualDefs.xml, MSPeriodicActuals.bin
    AcqMethod.xml, Contents.xml, DefaultMassCal.xml, Devices.xml ...
    ALS1.cd/.cg, DAD1.cd/.cg/.sd/.sp, QuatPump1.cd/.cg, TCC1.cd/.cg
    sample_info.xml, Worklist.xml
    "Proteomic Method NEW .m/" (acquisition method subfolder)
```

This is a genuine, complete Agilent `.d` with a populated `AcqData/` (non-empty
`MSScan.bin` / `MSProfile.bin` / `MSPeak.bin`) — suitable for the native Agilent
reader and the `--via-msconvert` path.

> Note: the other ZIPs in PXD041315 (e.g. `LMV_OP_48_h.zip`, ~1.1–1.2 GB each)
> are equivalent additional `.d` runs if more Agilent samples are wanted, all
> under the 3 GB per-file cap.

---

## SciEX — `sciex/PXD078909/`

- **Repository / accession:** PRIDE `PXD078909`
- **URL:** https://www.ebi.ac.uk/pride/archive/projects/PXD078909
- **DOI:** 10.6019/PXD078909
- **Vendor / instrument:** SCIEX **TripleTOF 5600** (Analyst `.wiff`)
- **Experiment:** SWATH-MS (zebrafish quantitative proteomics)
- **Availability / license:** Public PRIDE submission (free reuse). Submission
  type COMPLETE; published 2026-05-27.

### What was downloaded
A SCIEX acquisition is a `.wiff` (header/index) **plus** a sibling `.wiff.scan`
(the spectra); both are required. The smallest SWATH run pair was selected:

```
sciex/PXD078909/SW_F2_2-2.wiff        15,368,192 B  (≈ 14.66 MB)
sciex/PXD078909/SW_F2_2-2.wiff.scan  346,961,212 B  (≈ 330.9 MB)
```

Verified real vendor files:
- `SW_F2_2-2.wiff` magic bytes `D0 CF 11 E0 A1 B1 1A E1` = OLE2/Compound Document,
  `file` reports "Name of Creating Application: Analyst", SCIEX metadata.
- `.wiff.scan` present alongside as required, 346.96 MB binary (matches API size).

Suitable for the native SciEX reader and the `--via-msconvert` path.

---

## Coverage summary

| Vendor  | Accession | Instrument        | Files kept                         | Size on disk |
|---------|-----------|-------------------|------------------------------------|--------------|
| Agilent | PXD041315 | 6545 Q-TOF LC/MS  | `LMVCS24HC.d/` (full `.d` folder)  | 620 MB       |
| SciEX   | PXD078909 | TripleTOF 5600    | `SW_F2_2-2.wiff` + `.wiff.scan`    | 352 MB       |

Total corpus: ~0.97 GB (well within the ~5 GB budget; every file under the 3 GB cap).

### Notes / things not obtained
- **Agilent ion-mobility (6560 / IM-QTOF):** not included. A focused PRIDE search
  for "Agilent 6560" returned no public proteomics datasets with downloadable raw
  `.d`. The 6545 Q-TOF set above covers the standard (non-IM) Agilent path. A
  6560 IMS `.d` would be a good future addition if a small one surfaces.
- **SciEX ZenoTOF 7600 / `.wiff2`:** not included. The smallest confirmed SciEX
  raw set found was the TripleTOF 5600 `.wiff`/`.wiff.scan` above. `.wiff2`
  (ZenoTOF) datasets seen were either larger or not clearly small/public; left
  for a future targeted pull.
- Several other Agilent QTOF PRIDE projects (e.g. PXD057033, PXD050140, PXD059147)
  were rejected for size: their raw ZIPs are 1.4–8.5 GB single files, exceeding
  the 3 GB per-file cap or the total budget.
- PXD026412 (6520A QTOF) lists flattened `AcqData` files at the top level but the
  MS `.bin` data files are 0 bytes there (real data is only inside a 51 GB ZIP) —
  not usable, skipped.
