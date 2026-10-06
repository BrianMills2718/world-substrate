#!/usr/bin/env bash
# Assemble the World Builder pages from world-substrate's own sources.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
repo=$(cd "$here/../../.." && pwd)
dest="$here/dist/world-builder"
rm -rf "$here/dist"
mkdir -p "$dest/play" "$dest/build"
cp "$repo/scripts/world_builder_home.html" "$dest/index.html"
cp "$repo/evidence/renders/world-replay-studio-v0.html" "$dest/play/index.html"
cp "$repo/evidence/renders/world-builder-v0.html" "$dest/build/index.html"
printf '/world-builder/*\n  Cache-Control: public, max-age=0, must-revalidate\n' > "$here/dist/_headers"
for f in index.html play/index.html build/index.html; do test -s "$dest/$f"; done
echo "world-builder pages ready: $(find "$here/dist" -type f | wc -l) files"
