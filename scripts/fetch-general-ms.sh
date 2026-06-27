#!/usr/bin/env bash
# Download the resolved General MS demonstrator raws into data/general-ms/<accession>/ and verify
# byte counts against manifest/general-ms-files.tsv. Idempotent (curl -C - resume; skips complete files).
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$ROOT"
MAN="$ROOT/manifest/general-ms-files.tsv"; OUT="$ROOT/data/general-ms"
say(){ printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*"; }
ok=0; fail=0; mism=0
# portable local file size (BSD stat / GNU stat / wc fallback)
fsize(){ [ -f "$1" ] && { stat -f%z "$1" 2>/dev/null || stat -c%s "$1" 2>/dev/null || wc -c <"$1" | tr -d ' '; } || echo 0; }
# remote size via HEAD (works for http(s) and ftp); empty if the server doesn't report it
rsize(){ curl -fsSLI "$1" 2>/dev/null | awk 'tolower($1)=="content-length:"{v=$2} END{gsub(/\r/,"",v); print v+0}'; }

while IFS=$'\t' read -r acc repo vendor unit exp urls; do
  [ "${acc#\#}" != "$acc" ] && continue; [ "$acc" = "accession" ] && continue; [ -z "$acc" ] && continue
  dest="$OUT/$acc"; mkdir -p "$dest"
  say "$acc ($repo, $vendor) — $unit  exp=$(awk "BEGIN{printf \"%.1f\",$exp/1e6}")MB"
  IFS=';' read -ra parts <<< "$urls"
  for u in ${parts[@]+"${parts[@]}"}; do
    f="$dest/$(basename "${u%%\?*}")"
    rem="$(rsize "$u")"
    # idempotent skip when the server reports a size (http(s)); ftp:// rarely does, so we also handle
    # the "already complete" curl exit codes below.
    if [ -n "$rem" ] && [ "$rem" -gt 0 ] && [ "$(fsize "$f")" = "$rem" ]; then say "  have $(basename "$f")"; continue; fi
    rc=0; curl -fL --retry 4 --retry-delay 5 -C - -o "$f" "$u" || rc=$?
    case "$rc" in
      0) ;;
      # 33 = server doesn't support resume; 36 = bad resume offset — both mean a complete local file
      # being asked to resume from EOF (the ftp:// "already downloaded" case). Treat as done if nonempty.
      33|36) [ -s "$f" ] && say "  have (resume refused ⇒ complete) $(basename "$f")" || { say "  FAIL $(basename "$f")"; fail=$((fail+1)); } ;;
      *) say "  FAIL $(basename "$f") (curl $rc)"; fail=$((fail+1)) ;;
    esac
  done
  # verify: sum local bytes of the unit's parts vs expected (when known)
  got=$(for u in ${parts[@]+"${parts[@]}"}; do fsize "$dest/$(basename "${u%%\?*}")"; done | awk '{s+=$1} END{print s+0}')
  if [ "$exp" -gt 0 ] 2>/dev/null && [ "$got" -ne "$exp" ]; then say "  SIZE MISMATCH got=$got exp=$exp"; mism=$((mism+1))
  else say "  ok ($got bytes)"; ok=$((ok+1)); fi
done < "$MAN"
say "DONE  ok=$ok size-mismatch=$mism part-fail=$fail"
