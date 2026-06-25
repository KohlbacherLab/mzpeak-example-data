#!/usr/bin/env bash
# build_data.sh — reconstruct the mzPeak example-data corpus from its public sources.
#
# For every tile: download the data from the originating repository (PRIDE / MassIVE /
# MetaboLights / Zenodo / ProteoWizard) and run mzPeakConverter (`mzpeak-convert`) to
# (re)generate the .mzpeak files. Idempotent — present downloads and existing .mzpeak
# outputs are skipped.
#
# Usage:
#   ./build_data.sh                       # all tiles
#   ./build_data.sh mzML-examples sdrf-examples
#   SKIP_CONVERT=1 ./build_data.sh        # download only
#   SKIP_FETCH=1   ./build_data.sh        # convert already-downloaded inputs only
#   MZPEAK_CONVERT=/path/to/mzpeak-convert ./build_data.sh   # use a prebuilt binary
#
# Vendor raw with no cross-platform reader (SCIEX/.wiff, Agilent/.d, Waters/.raw, Bruker-BAF)
# converts only on Windows/Linux with vendor libs, or anywhere via --via-msconvert (ProteoWizard).
# Where unsupported, the input is fetched and the conversion is reported SKIP, not failed.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT" || exit 1

# Tiles build_data.sh can reconstruct from public repos. raw-replacements (locally-derived
# subsets) and demo (seeded from the imzml-examples conversion) are documented but not auto-built.
ALL_TILES="mzML-examples imzml-examples sdrf-examples pwiz-examples raw-bench tof-grid-examples vendor-agilent-sciex vendor-waters vendor-bruker-baf"
TILES="${*:-$ALL_TILES}"
SKIP_FETCH="${SKIP_FETCH:-0}"
SKIP_CONVERT="${SKIP_CONVERT:-0}"
MANIFEST="$ROOT/manifest/datasets.tsv"
declare -i N_OK=0 N_SKIP=0 N_FAIL=0 N_MANUAL=0

say(){ printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*"; }
need(){ command -v "$1" >/dev/null || { echo "ERROR: '$1' not found on PATH" >&2; exit 1; }; }

need curl; need unzip

# ── locate or build mzpeak-convert ──────────────────────────────────────────────
BIN=""
ensure_converter(){
  [ "$SKIP_CONVERT" = 1 ] && return 0
  if [ -n "${MZPEAK_CONVERT:-}" ] && [ -x "${MZPEAK_CONVERT}" ]; then BIN="$MZPEAK_CONVERT"
  elif command -v mzpeak-convert >/dev/null; then BIN="$(command -v mzpeak-convert)"
  else
    local b="$ROOT/.build/mzPeakConverter/target/release/mzpeak-convert"
    if [ ! -x "$b" ]; then
      need git; need cargo
      say "building mzpeak-convert (clone + cargo build --release)…"
      [ -d "$ROOT/.build/mzPeakConverter" ] || \
        git clone --depth 1 https://github.com/okohlbacher/mzPeakConverter.git "$ROOT/.build/mzPeakConverter"
      ( cd "$ROOT/.build/mzPeakConverter" && cargo build --release ) || { echo "ERROR: converter build failed" >&2; exit 1; }
    fi
    BIN="$b"
  fi
  say "converter: $BIN"
}

# ── conversion ──────────────────────────────────────────────────────────────────
out_path(){ printf '%s' "$1" | sed -E 's/\.(mzML|mzML\.gz|imzML|raw|RAW|wiff|d|lcd)$/.mzpeak/'; }

convert_one(){  # <input> [flags…]
  [ "$SKIP_CONVERT" = 1 ] && return 0
  local in="$1"; shift
  [ -e "$in" ] || { say "  miss   $(basename "$in") (not downloaded)"; return 0; }
  local out; out="$(out_path "$in")"
  if [ -e "$out" ]; then say "  have   $(basename "$out")"; N_OK+=1; return 0; fi
  say "  convert $(basename "$in")"
  local flags=(); if [ "${1:-}" = "-" ]; then shift; else flags=("$@"); fi
  if "$BIN" "$in" -o "$out" --force ${flags[@]+"${flags[@]}"} >/dev/null 2>"$out.convlog"; then
    rm -f "$out.convlog"; say "    ok $(du -h "$out" | cut -f1)"; N_OK+=1
  else
    local rc=$?
    if [ "$rc" = 3 ]; then say "    SKIP unsupported on this platform (needs vendor reader / --via-msconvert)"; N_SKIP+=1
    else say "    FAIL rc=$rc — see $out.convlog"; N_FAIL+=1; fi
  fi
}

convert_glob(){  # <tile> <find-name-pattern>
  local tile="$1" pat="$2" f
  while IFS= read -r f; do convert_one "$f"; done < <(find "$ROOT/data/$tile" -type f -iname "$pat" 2>/dev/null | sort)
}

# ── per-repo fetch for the vendor-raw manifest ───────────────────────────────────
dl(){  # <url> <dest>   resume-capable; skip if present
  local url="$1" dest="$2"
  [ -s "$dest" ] && { say "  exists $(basename "$dest")"; return 0; }
  mkdir -p "$(dirname "$dest")"
  say "  fetch  $(basename "$dest")"
  curl -fL --retry 3 --retry-delay 5 -C - -o "$dest" "$url"
}

vendor_tile(){  # <tile>  — process all manifest rows whose 'tile' matches
  local want="$1"
  while IFS=$'\t' read -r tile dir accession repo files unpack cinput flags notes; do
    [ "${tile#\#}" != "$tile" ] && continue          # comment
    [ "$tile" = tile ] && continue                    # header
    # match the tile OR a "tile/subdir" row (e.g. vendor-agilent-sciex/sciex)
    case "$tile" in "$want"|"$want"/*) ;; *) continue ;; esac
    local dest="$ROOT/data/$tile/$dir"
    say "$tile/$dir  ($accession, $repo)"
    if [ "$SKIP_FETCH" != 1 ]; then
      if [ "$files" = "-" ]; then
        say "  MANUAL fetch $accession from $repo into data/$tile/$dir/ (see docs/CORPUS.md)"; N_MANUAL+=1
      else
        local u urls; IFS=';' read -ra urls <<< "$files"
        for u in "${urls[@]}"; do dl "$u" "$dest/$(basename "${u%%\?*}")"; done
        if [ "$unpack" = zip ]; then
          local z; for z in "$dest"/*.zip; do [ -e "$z" ] && ( cd "$dest" && unzip -o -q "$z" && rm -f "$z" ); done
        fi
      fi
    fi
    [ "$cinput" = "-" ] && continue
    convert_one "$dest/$cinput" "${flags:--}"
  done < "$MANIFEST"
}

# ── drivers ──────────────────────────────────────────────────────────────────────
run_fetch_script(){ [ "$SKIP_FETCH" = 1 ] && return 0; say "fetch $1"; bash "$ROOT/scripts/$2"; }

ensure_converter
for tile in $TILES; do
  echo "──────────────────────────────────────────────────────────────────────"
  say "TILE: $tile"
  case "$tile" in
    mzML-examples)   run_fetch_script "$tile" fetch-mzml-examples.sh;  convert_glob "$tile" '*.mzML' ;;
    imzml-examples)  run_fetch_script "$tile" fetch-imzml-examples.sh; convert_glob "$tile" '*.imzML' ;;
    sdrf-examples)   run_fetch_script "$tile" fetch-sdrf-examples.sh;  convert_glob "$tile" '*.mzML' ;;
    pwiz-examples)
      if [ -d "$ROOT/data/pwiz-examples" ] && find "$ROOT/data/pwiz-examples" -iname '*.mzML' -print -quit | grep -q .; then
        convert_glob "$tile" '*.mzML'
      else
        say "  pwiz-examples source = ProteoWizard test corpus — not auto-fetched."
        say "  Seed data/pwiz-examples/ from the ProteoWizard 'Reader_*_Test.data' fixtures, then re-run."
        N_MANUAL+=1
      fi ;;
    raw-bench|raw-replacements|tof-grid-examples|vendor-agilent-sciex|vendor-waters|vendor-bruker-baf)
      vendor_tile "$tile" ;;
    *) say "  unknown tile '$tile' — skipping" ;;
  esac
done

echo "══════════════════════════════════════════════════════════════════════"
say "DONE  ok=$N_OK  skip(platform)=$N_SKIP  fail=$N_FAIL  manual=$N_MANUAL"
[ "$N_FAIL" -eq 0 ]
