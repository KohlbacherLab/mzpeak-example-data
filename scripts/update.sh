#!/usr/bin/env bash
# ════════════════════════════════════════════════════════════════════════════════════════════════
#  update.sh — ONE command to add or refresh datasets.
#
#  To add data:   copy  data/TEMPLATE.yaml  to  data/<tile>/<id>/<id>.yaml , edit it, then run:
#      scripts/update.sh
#
#  It runs the whole pipeline for the selected datasets:
#      1. download   files          -> data/<tile>/<id>/        (idempotent)
#      2. convert    raw -> mzPeak   -> <unit>.mzpeak           (idempotent; skips if no converter)
#      3. upload     to the bucket   -> s3://$BUCKET/<tile>/<id>/
#      4. catalogs   rebuilt FROM the YAML descriptors          (data/<tile>/_catalog.md)
#      5. publish    the website     -> build-corpus-site.sh
#
#  Usage:
#      scripts/update.sh                                   # all datasets
#      scripts/update.sh data/<tile>/<id>/<id>.yaml ...    # just these
#      scripts/update.sh --id PXD000155
#  Flags:  --no-convert  --no-upload  --no-publish  --dry-run(implies --no-upload --no-publish)
#  Env:    ENDPOINT, BUCKET=v09, AWS_PROFILE=stackit, MZPEAK_CONVERT=/path/to/mzpeak-convert
# ════════════════════════════════════════════════════════════════════════════════════════════════
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$ROOT"
EP="${ENDPOINT:-https://object.storage.eu01.onstackit.cloud}"; B="${BUCKET:-v09}"
PROFILE="${AWS_PROFILE:-stackit}"
say(){ printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*"; }

CONVERT=1; UPLOAD=1; PUBLISH=1; DRY=0; SEL=()
for a in "$@"; do case "$a" in
  --no-convert) CONVERT=0 ;; --no-upload) UPLOAD=0 ;; --no-publish) PUBLISH=0 ;;
  --dry-run)    DRY=1; UPLOAD=0; PUBLISH=0 ;;
  --id)         SEL+=("$a") ;;          # passed through to the resolver
  *)            SEL+=("$a") ;;
esac; done
[ "${#SEL[@]}" -eq 0 ] && SEL=(--all)

# resolve the selector once: descriptor path + tile + id per dataset
PATHS=(); TILES=(); IDS=()
while IFS=$'\t' read -r p t i; do
  [ -n "$p" ] && { PATHS+=("$p"); TILES+=("$t"); IDS+=("$i"); }
done < <(python3 scripts/corpus_lib.py "${SEL[@]}")
[ "${#PATHS[@]}" -gt 0 ] || { echo "no datasets matched" >&2; exit 1; }
say "selected ${#PATHS[@]} dataset(s)"

say "1/5 download"; python3 scripts/fetch-dataset.py "${PATHS[@]}" || say "  some downloads failed (see above)"

if [ "$CONVERT" = 1 ]; then say "2/5 convert"; python3 scripts/convert-dataset.py "${PATHS[@]}" || say "  some conversions failed"; fi

if [ "$UPLOAD" = 1 ]; then
  say "3/5 upload -> s3://$B"
  for k in "${!IDS[@]}"; do
    d="data/${TILES[$k]}/${IDS[$k]}"
    # only upload data (raw + .mzpeak), never the descriptor or extract markers
    if find "$d" -type f ! -name '*.yaml' ! -name '*.yml' ! -name '*.json' ! -name '*.extracted' | grep -q .; then
      aws --profile "$PROFILE" --endpoint-url "$EP" s3 cp "$d" "s3://$B/${TILES[$k]}/${IDS[$k]}" \
        --recursive --exclude '*.yaml' --exclude '*.yml' --exclude '*.json' --exclude '*.extracted' \
        --only-show-errors && say "  uploaded ${IDS[$k]}" || say "  UPLOAD FAIL ${IDS[$k]}"
    fi
  done
else say "3/5 upload skipped"; fi

say "4/5 rebuild catalogs from YAML"; python3 scripts/build-catalogs.py

if [ "$PUBLISH" = 1 ]; then say "5/5 publish site"; bash scripts/build-corpus-site.sh
elif [ "$DRY" = 1 ]; then say "5/5 publish (dry-run)"; bash scripts/build-corpus-site.sh --dry-run
else say "5/5 publish skipped"; fi
say "=== update complete ==="
