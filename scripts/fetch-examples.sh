#!/usr/bin/env bash
# fetch-examples.sh — unified downloader for the OPEN-FORMAT example tiles:
#   mzML-examples · imzml-examples · sdrf-examples · pwiz-examples
# (The vendor-RAW tiles are driven from manifest/datasets.tsv by build_data.sh.)
#
# Idempotent: files already present (non-empty) are skipped. Curated URLs are verified against the
# PRIDE / MetaboLights / Zenodo / GitHub / object-store sources. Requires: bash, curl, unzip;
# pwiz-examples additionally needs python3 (UTF-8-safe URL encoding of the file list).
#
#   bash scripts/fetch-examples.sh                 # all four tiles
#   bash scripts/fetch-examples.sh mzML-examples   # one tile
#
# Exits non-zero if any download failed (count reported at the end).
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
M=https://massive.ucsd.edu/ProteoSAFe/DownloadResultFile     # NOTE: no HTTP range/resume
MIRROR=https://object.storage.eu01.onstackit.cloud/v09       # public-read object store (pwiz source)
FAILS=0

# dl <url> <dest> [--no-resume]   — skip if present; resume by default (off for MassIVE).
dl() {
  local url="$1" dest="$2" resume="-C -"
  [ "${3:-}" = "--no-resume" ] && resume=""
  if [ -s "$dest" ]; then echo "  exists: $dest"; return 0; fi
  echo "  fetch : $dest"
  mkdir -p "$(dirname "$dest")"
  # shellcheck disable=SC2086
  if curl -fL --retry 3 --retry-delay 5 $resume -o "$dest" "$url"; then return 0; fi
  echo "  FAIL  : $dest" >&2; rm -f "$dest"; FAILS=$((FAILS+1)); return 1
}

# ── mzML-examples — one .mzML per instrument (non-imaging sweep) ─────────────────────────────────
fetch_mzml() {
  local B="$ROOT/data/mzML-examples"; mkdir -p "$B"; cd "$B"
  echo "== mzML-examples =="
  dl "https://zenodo.org/api/records/18502866/files/MRM-standmix-5.mzML/content"                          "agilent-qtof/MRM-standmix-5.mzML"
  dl "https://ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/MTBLS520/FILES/neg_01_Fistax_1-A,2_01_5715.mzML" "bruker-microtof-q2/neg_01_Fistax_1-A,2_01_5715.mzML"
  dl "https://ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/MTBLS1129/FILES/QC01.mzML"          "waters-xevo-g2s-qtof/QC01.mzML"
  dl "https://zenodo.org/api/records/17549994/files/160920_SM-AKTWT_509.mzML/content"                     "thermo-qexactive-plus/160920_SM-AKTWT_509.mzML"
  dl "https://zenodo.org/api/records/17416537/files/12_80.mzML/content"                                   "sciex-tripletof-6600/12_80.mzML"
  dl "https://ftp.pride.ebi.ac.uk/pride/data/archive/2012/03/PXD000001/TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzML" "thermo-ltq-orbitrap-velos/TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzML"
  dl "https://ftp.pride.ebi.ac.uk/pride/data/archive/2018/05/PXD008952/01_CPTAC_TMTS1-NCI7_P_JHUZ_20170509_LUMOS.mzML" "thermo-fusion-lumos/01_CPTAC_TMTS1-NCI7_P_JHUZ_20170509_LUMOS.mzML"
  dl "$M?file=f.MSV000101607/peak/SBA415.mzML&forceDownload=true"                                         "bruker-timstof-pro/SBA415.mzML" --no-resume
  dl "$M?file=f.MSV000100943/ccms_peak/RAW/20240912_WFB_exp01_magnet_5_0.mzML&forceDownload=true"         "thermo-orbitrap-astral/20240912_WFB_exp01_magnet_5_0.mzML" --no-resume
  # extended coverage (new vendors / analyzers / modalities; all small)
  dl "https://ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/MTBLS13204/FILES/DERIVED_FILES/Blind_P1_pos_012.mzML" "shimadzu-lcms-9030-qtof/Blind_P1_pos_012.mzML"
  dl "https://ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/MTBLS11550/FILES/DERIVED_FILES/GC/EFWS-1.mzML"  "agilent-8890-gc-ei/EFWS-1.mzML"
  dl "https://ftp.pride.ebi.ac.uk/pride/data/archive/2024/01/PXD041762/REC-2349_P2_F1.mzML"               "agilent-6490-triplequad/REC-2349_P2_F1.mzML"
  dl "https://ftp.pride.ebi.ac.uk/pride/data/archive/2026/02/PXD066465/Drug_substance_3_scheduled_MRM.mzML" "sciex-qtrap-6500/Drug_substance_3_scheduled_MRM.mzML"
  dl "https://zenodo.org/api/records/18481720/files/CEMS_10ppm.mzML/content"                              "agilent-6560-dtims-imqtof/CEMS_10ppm.mzML"
  dl "https://ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/MTBLS3512/FILES/mtab_BIOS_CRAM1620_1_072617_34.mzML" "thermo-ltq-ft-ultra-fticr/mtab_BIOS_CRAM1620_1_072617_34.mzML"
  dl "https://ftp.pride.ebi.ac.uk/pride/data/archive/2025/10/PXD059878/2013_30_Amrutha_050713_1.mzML"     "thermo-ltq-xl-iontrap/2013_30_Amrutha_050713_1.mzML"
  dl "https://ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/MTBLS12824/FILES/21P0055_Tissue_Georges_NEG_N_01_17471.mzML" "bruker-impact-ii-qtof/21P0055_Tissue_Georges_NEG_N_01_17471.mzML"
  dl "$M?file=f.MSV000095995/ccms_peak/20240826_RNAseB_Reduced_50ngul_1ul_MRM_03.mzML&forceDownload=true" "sciex-zenotof-7600/20240826_RNAseB_Reduced_50ngul_1ul_MRM_03.mzML" --no-resume
}

# ── imzml-examples — imzML(+ibd) + optical TIFF + Zenodo collections ─────────────────────────────
fetch_imzml() {
  local B="$ROOT/data/imzml-examples"; mkdir -p "$B"; cd "$B"
  echo "== imzml-examples =="
  # 1) ms-imaging.org Example 1 (mirror: github.com/beny/imzml) — tiny 3x3 pairs
  local G=https://raw.githubusercontent.com/beny/imzml/master/data
  dl "$G/Example_Continuous.imzML" "example1-continuous/Example_Continuous.imzML"
  dl "$G/Example_Continuous.ibd"   "example1-continuous/Example_Continuous.ibd"
  dl "$G/Example_Processed.imzML"  "example1-processed/Example_Processed.imzML"
  dl "$G/Example_Processed.ibd"    "example1-processed/Example_Processed.ibd"
  # 2) PRIDE PXD001283 — HR2MSI mouse urinary bladder (imzML + ibd + optical TIFF + results)
  local PXD=PXD001283-HR2MSI-urinary-bladder; mkdir -p "$PXD"
  local P=https://ftp.pride.ebi.ac.uk/pride/data/archive/2014/11/PXD001283
  dl "$P/HR2MSImouseurinarybladderS096.imzML"            "$PXD/HR2MSImouseurinarybladderS096.imzML"
  dl "$P/HR2MSImouseurinarybladderS096-opticalimage.tif" "$PXD/HR2MSImouseurinarybladderS096-opticalimage.tif"
  dl "$P/HR2MSImouseurinarybladderS096-results.csv"      "$PXD/HR2MSImouseurinarybladderS096-results.csv"
  # .ibd is 777 MiB: reuse data/HR2MSImouseurinarybladderS096.ibd if present (hardlink, no extra disk)
  if [ -s "$ROOT/data/HR2MSImouseurinarybladderS096.ibd" ] && \
     ln -f "$ROOT/data/HR2MSImouseurinarybladderS096.ibd" "$PXD/HR2MSImouseurinarybladderS096.ibd" 2>/dev/null; then
    echo "  link  : $PXD/HR2MSImouseurinarybladderS096.ibd (hardlink from data/)"
  else
    dl "$P/HR2MSImouseurinarybladderS096.ibd" "$PXD/HR2MSImouseurinarybladderS096.ibd"
  fi
  # 3) Zenodo 10084132 — modality collections (extract one dir each)
  local d z
  for d in "zenodo-DESI:imzML_DESI.zip" "zenodo-LA-ESI:imzML_LA-ESI.zip" \
           "zenodo-AP-SMALDI:imzML_AP_SMALDI.zip" "zenodo-LTP:imzML_LTP.zip"; do
    local dir="${d%%:*}" zip="${d#*:}"; mkdir -p "$dir"
    if find "$dir" -iname '*.imzML' 2>/dev/null | grep -q .; then echo "  exists: $dir (extracted)"; continue; fi
    echo "  fetch : $dir/$zip"
    if curl -fL --retry 3 -o "$dir/$zip" "https://zenodo.org/api/records/10084132/files/$zip/content"; then
      ( cd "$dir" && unzip -o -q "$zip" && rm -f "$zip" )
    else echo "  FAIL  : $dir/$zip" >&2; rm -f "$dir/$zip"; FAILS=$((FAILS+1)); fi
  done
  # 4) Zenodo 18187395 — GBM MALDI phenomics (per-section zip; smallest by default)
  local GBM=zenodo-18187395-GBM-multimodal sec
  for sec in ${GBM_SECTIONS:-24_Test_P15_r2}; do
    local dest="$GBM/$sec"
    if find "$dest" -iname '*.imzML' 2>/dev/null | grep -q .; then echo "  exists: $dest (extracted)"; continue; fi
    mkdir -p "$dest"; echo "  fetch : $dest ($sec.zip)"
    if curl -fL --retry 3 -o "$dest/$sec.zip" "https://zenodo.org/api/records/18187395/files/$sec.zip/content"; then
      ( cd "$dest" && unzip -o -q "$sec.zip" && rm -f "$sec.zip" )
    else echo "  FAIL  : $dest/$sec.zip" >&2; rm -f "$dest/$sec.zip"; FAILS=$((FAILS+1)); fi
  done
}

# ── sdrf-examples — SDRF/ISA study-design files ──────────────────────────────────────────────────
fetch_sdrf() {
  local B="$ROOT/data/sdrf-examples"; mkdir -p "$B"; cd "$B"
  echo "== sdrf-examples =="
  dl "https://raw.githubusercontent.com/bigbio/proteomics-sample-metadata/master/annotated-projects/MTBLS1129/MTBLS1129.sdrf.tsv" "MTBLS1129/MTBLS1129.sdrf.tsv"
  dl "https://raw.githubusercontent.com/bigbio/sdrf-annotated-datasets/main/datasets/PXD011799/PXD011799.sdrf.tsv"                 "PXD011799/PXD011799.sdrf.tsv"
}

# ── pwiz-examples — ProteoWizard vendor-reader test mzML ─────────────────────────────────────────
# Canonical upstream is the ProteoWizard test corpus (Reader_*_Test.data, in the pwiz source tree,
# not individually URL-addressable). We fetch the same files from the project's public-read object
# store via manifest/pwiz-files.txt; python3 percent-encodes the (UTF-8, spaces, commas) paths.
fetch_pwiz() {
  local B="$ROOT/data/pwiz-examples" list="$ROOT/manifest/pwiz-files.txt"
  echo "== pwiz-examples =="
  [ -f "$list" ] || { echo "  missing $list" >&2; FAILS=$((FAILS+1)); return 1; }
  command -v python3 >/dev/null || { echo "  python3 required to fetch pwiz-examples" >&2; FAILS=$((FAILS+1)); return 1; }
  mkdir -p "$B"
  local url dest
  while IFS=$'\t' read -r url dest; do
    [ -n "$url" ] || continue
    if [ -s "$dest" ]; then continue; fi
    mkdir -p "$(dirname "$dest")"
    if curl -fL --retry 3 --retry-delay 5 -o "$dest" "$url"; then echo "  ok   : ${dest#"$B/"}"
    else echo "  FAIL : ${dest#"$B/"}" >&2; rm -f "$dest"; FAILS=$((FAILS+1)); fi
  done < <(python3 - "$list" "$MIRROR/pwiz-examples" "$B" <<'PY'
import sys, urllib.parse
listf, base_url, base = sys.argv[1:4]
for line in open(listf):
    p = line.strip()
    if not p or p.startswith('#'): continue
    enc = '/'.join(urllib.parse.quote(seg) for seg in p.split('/'))
    print(f"{base_url}/{enc}\t{base}/{p}")
PY
  )
}

# ── dispatch ─────────────────────────────────────────────────────────────────────────────────────
case "${1:-all}" in
  mzML-examples)  fetch_mzml ;;
  imzml-examples) fetch_imzml ;;
  sdrf-examples)  fetch_sdrf ;;
  pwiz-examples)  fetch_pwiz ;;
  all)            fetch_mzml; fetch_imzml; fetch_sdrf; fetch_pwiz ;;
  *) echo "usage: fetch-examples.sh [mzML-examples|imzml-examples|sdrf-examples|pwiz-examples|all]" >&2; exit 2 ;;
esac

echo
[ "$FAILS" -eq 0 ] && echo "fetch-examples: OK (no failures)" || echo "fetch-examples: $FAILS download(s) FAILED" >&2
[ "$FAILS" -eq 0 ]
