#!/usr/bin/env bash
# ════════════════════════════════════════════════════════════════════════════════════════════════
#  CANONICAL corpus-site builder — THE ONLY supported way to (re)generate and deploy the browsable
#  site to s3://v09: index.html, one page per tile, per-directory statistics, ratios.tsv, and the
#  per-category ratio figures.
#
#  The tiles are FIXED: each is defined by a `<tile>/_catalog.md` (frontmatter slug/title/icon/accent/
#  imaging/order + blurb + provenance + `## datasets`). This script + scripts/make-s3-index.py +
#  scripts/make-ratio-plots.py are a LOCKED pipeline. DO NOT modify any of them, or add tiles, without
#  EXPLICIT user instruction. (memory: mzpeak-tiles-fixed-by-catalog)
#
#  Usage:  bash scripts/build-corpus-site.sh [--dry-run]
#  Env:    ENDPOINT, BUCKET=v09, AWS_PROFILE=stackit, OUTDIR=out/site,
#          CATALOG_ROOT=$HOME/Claude/mzPeak/data   (where the <tile>/_catalog.md live)
# ════════════════════════════════════════════════════════════════════════════════════════════════
set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EP="${ENDPOINT:-https://object.storage.eu01.onstackit.cloud}"
B="${BUCKET:-v09}"
PROFILE="${AWS_PROFILE:-stackit}"
OUT="${OUTDIR:-out/site}"
CATALOG_ROOT="${CATALOG_ROOT:-$HOME/Claude/mzPeak/data}"; export CATALOG_ROOT
DRY=0; [ "${1:-}" = "--dry-run" ] && DRY=1
AWS=(aws --profile "$PROFILE" --endpoint-url "$EP")
say(){ echo "[$(date +%H:%M:%S)] $*"; }
command -v aws >/dev/null     || { echo "ERROR: aws CLI not found" >&2; exit 1; }
command -v python3 >/dev/null || { echo "ERROR: python3 not found" >&2; exit 1; }
mkdir -p out "$OUT"

# 0) the FIXED tiles = directories carrying a _catalog.md
TILES=(); for c in "$CATALOG_ROOT"/*/_catalog.md; do [ -f "$c" ] && TILES+=("$(basename "$(dirname "$c")")"); done
[ "${#TILES[@]}" -gt 0 ] || { echo "ERROR: no <tile>/_catalog.md under $CATALOG_ROOT" >&2; exit 1; }
VALID_SLUGS=(); for t in "${TILES[@]}"; do
  s="$(awk -F': *' '/^slug:/{print $2; exit}' "$CATALOG_ROOT/$t/_catalog.md")"; VALID_SLUGS+=("${s:-$t}")
done
say "fixed tiles (${#TILES[@]}): ${TILES[*]}"
say "slugs: ${VALID_SLUGS[*]}"

# 1) publish the _catalog.md markers (make-s3-index gates tiles on their S3 presence)
if [ "$DRY" = 0 ]; then
  for t in "${TILES[@]}"; do
    "${AWS[@]}" s3 cp "$CATALOG_ROOT/$t/_catalog.md" "s3://$B/$t/_catalog.md" \
      --content-type 'text/markdown; charset=utf-8' --only-show-errors && say "catalog -> $t/_catalog.md"
  done
fi

# 2) list the live bucket  ->  3) generate the site (index + per-tile pages + ratios.tsv + stats)
say "listing s3://$B"
"${AWS[@]}" s3api list-objects-v2 --bucket "$B" --output json > out/v09-listing.json \
  || { echo "ERROR: bucket list failed" >&2; exit 1; }
say "generating site -> $OUT  (CATALOG_ROOT=$CATALOG_ROOT)"
python3 scripts/make-s3-index.py "$OUT" < out/v09-listing.json
say "rendering per-category ratio figures"
python3 scripts/make-ratio-plots.py "$OUT" || say "WARN ratio plots skipped (matplotlib unavailable?)"

if [ "$DRY" = 1 ]; then say "DRY-RUN — generated in $OUT, nothing uploaded"; ls -1 "$OUT"; exit 0; fi

# 4) deploy site assets
shopt -s nullglob; rc=0
put(){ "${AWS[@]}" s3 cp "$1" "s3://$B/$2" --content-type "$3" --cache-control no-cache --only-show-errors \
        && say "put $2" || { say "FAIL $2"; rc=1; }; }
for f in "$OUT"/*.html; do put "$f" "$(basename "$f")" "text/html; charset=utf-8"; done
[ -f "$OUT/README.md" ] && put "$OUT/README.md" "README.md" "text/markdown; charset=utf-8"
for f in "$OUT"/*.png; do put "$f" "$(basename "$f")" "image/png"; done
for f in "$OUT"/*.sh;  do put "$f" "$(basename "$f")" "text/x-shellscript; charset=utf-8"; done

# 5) prune stale subpages/figures for tiles that no longer exist (allowlist = index + valid slugs)
keep="index"; for s in "${VALID_SLUGS[@]}"; do keep="$keep|$s"; done
while read -r key; do
  case "$key" in *.html) base="${key%.html}";; *-ratios.png) base="${key%-ratios.png}";; *) continue;; esac
  printf '%s\n' "$base" | grep -qE "^(${keep})$" || { "${AWS[@]}" s3 rm "s3://$B/$key" --only-show-errors && say "pruned stale $key"; }
done < <("${AWS[@]}" s3 ls "s3://$B/" 2>/dev/null | awk '{print $4}' | grep -E '\.html$|-ratios\.png$')

# 6) verify the landing page is served
read -r code ctype < <(curl -fsS -o /dev/null -w '%{http_code} %{content_type}\n' "$EP/$B/index.html" 2>/dev/null || echo "000 -")
say "live: $EP/$B/index.html  (HTTP $code, $ctype)"
[ "$rc" = 0 ] && say "=== DONE ===" || say "=== DONE (with upload errors) ==="
exit $rc
