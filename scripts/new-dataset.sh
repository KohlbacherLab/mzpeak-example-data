#!/usr/bin/env bash
# new-dataset.sh <tile> <id> — scaffold a dataset descriptor from data/TEMPLATE.yaml.
#
# Creates  data/<tile>/<id>/<id>.yaml  with id and tile already filled in. Then edit that file
# (title, description, file urls) and add it:
#     scripts/update.sh data/<tile>/<id>/<id>.yaml
#
# <tile> must be an existing tile (have a data/<tile>/_tile.yaml).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$ROOT"
[ $# -eq 2 ] || { echo "usage: scripts/new-dataset.sh <tile> <id>" >&2; exit 2; }
tile="$1"; id="$2"
[ -f "data/$tile/_tile.yaml" ] || { echo "unknown tile '$tile' (no data/$tile/_tile.yaml)" >&2; exit 1; }
dst="data/$tile/$id/$id.yaml"
[ -e "$dst" ] && { echo "$dst already exists" >&2; exit 1; }
mkdir -p "data/$tile/$id"
sed -e "s|^id: .*|id: $id|" -e "s|^tile: .*|tile: $tile|" data/TEMPLATE.yaml > "$dst"
echo "created $dst"
echo "next: edit it, then run   scripts/update.sh $dst"
