#!/usr/bin/env bash
# sync-s3.sh — publish the rebuilt corpus and refresh the browsable site.
#   1) idempotent `aws s3 sync` of each publishable tile's *.mzpeak to s3://v09
#   2) rebuild index.html (+ subpages) from the LIVE bucket listing and deploy it
#      (delegated to push-index-stackit.sh, which re-lists the bucket each run)
#
#   bash scripts/sync-s3.sh              # sync + rebuild + deploy
#   bash scripts/sync-s3.sh --dry-run    # plan only, transfer/deploy nothing
#
# Env (defaults): ENDPOINT, BUCKET=v09, AWS_PROFILE=stackit.
# Only the four published tiles are uploaded; vendor-raw/benchmark tiles stay local.
set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

EP="${ENDPOINT:-https://object.storage.eu01.onstackit.cloud}"
B="${BUCKET:-v09}"
PROFILE="${AWS_PROFILE:-stackit}"
DRYRUN="${DRYRUN:-0}"; [ "${1:-}" = "--dry-run" ] && DRYRUN=1
AWS=(aws --profile "$PROFILE" --endpoint-url "$EP")
TILES=(imzml-examples general-ms pwiz-examples sdrf-examples)
say(){ echo "[$(date +%H:%M:%S)] $*"; }

command -v aws >/dev/null || { echo "ERROR: aws CLI not found (brew install awscli)" >&2; exit 1; }

dry=(); [ "$DRYRUN" = 1 ] && dry=(--dryrun)
for t in "${TILES[@]}"; do
  [ -d "data/$t" ] || { say "skip $t (not built locally)"; continue; }
  say "sync $t -> s3://$B/$t  (only *.mzpeak, idempotent)"
  "${AWS[@]}" s3 sync "data/$t" "s3://$B/$t" \
    --exclude '*' --include '*.mzpeak' ${dry[@]+"${dry[@]}"} --only-show-errors \
    && say "  $t synced" || { say "  $t sync FAILED"; exit 1; }
done

say "rebuild + deploy index.html from the live bucket"
DRYRUN="$DRYRUN" bash scripts/push-index-stackit.sh
