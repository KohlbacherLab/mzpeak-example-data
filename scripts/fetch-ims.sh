#!/usr/bin/env bash
# Download the ion-mobility example raws listed in manifest/ims-files.tsv into the working-corpus
# ims-examples tile, verifying byte counts. Idempotent (curl -C - resume). One raw file per study.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAN="$ROOT/manifest/ims-files.tsv"
OUT="${IMS_OUT:-$ROOT/data/ims-examples}"
say(){ printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*"; }
fsize(){ [ -f "$1" ] && { stat -f%z "$1" 2>/dev/null || stat -c%s "$1" 2>/dev/null; } || echo 0; }
ok=0; fail=0; mism=0
while IFS=$'\t' read -r acc repo vendor imt exp url; do
  [ "${acc#\#}" != "$acc" ] && continue; [ "$acc" = "accession" ] && continue; [ -z "$acc" ] && continue
  dest="$OUT/$acc"; mkdir -p "$dest"
  # filename: MassIVE DownloadResultFile carries it in the file= param; else basename of the URL path
  case "$url" in
    *DownloadResultFile*file=*) name="$(basename "${url##*file=}")"; name="${name%%&*}" ;;
    *) name="$(basename "${url%%\?*}")" ;;
  esac
  f="$dest/$name"
  enc="${url// /%20}"   # URL-encode spaces (MassIVE filenames)
  say "$acc ($vendor / $imt) -> $name  exp=$(awk "BEGIN{printf \"%.0f\",$exp/1e6}")MB"
  if [ "$(fsize "$f")" = "$exp" ]; then say "  have (complete)"; ok=$((ok+1)); continue; fi
  rc=0; curl -fL --retry 5 --retry-delay 5 -C - -o "$f" "$enc" || rc=$?
  case "$rc" in
    0) ;;
    33|36) [ -s "$f" ] || { say "  FAIL (curl $rc, empty)"; fail=$((fail+1)); continue; } ;;
    *) say "  FAIL $name (curl $rc)"; fail=$((fail+1)); continue ;;
  esac
  got=$(fsize "$f")
  if [ "$exp" -gt 0 ] 2>/dev/null && [ "$got" -ne "$exp" ]; then say "  SIZE MISMATCH got=$got exp=$exp"; mism=$((mism+1))
  else say "  ok ($got bytes)"; ok=$((ok+1)); fi
done < "$MAN"
say "DONE  ok=$ok size-mismatch=$mism fail=$fail  (into $OUT)"
