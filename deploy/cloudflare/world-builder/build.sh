#!/usr/bin/env bash
# Assemble the World Builder pages from world-substrate's own sources.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
repo=$(cd "$here/../../.." && pwd)
dest="$here/dist/world-builder"
rm -rf "$here/dist"
mkdir -p "$dest/room-map/assets-cc0" "$dest/play" "$dest/build" "$dest/design/attempt-from-belief"
cp "$repo/scripts/world_builder_home.html" "$dest/index.html"
# The room-map viewer: our own code, the generated map and CC0 tiles only. Never Smallville's art or maps.
cp "$repo/viewer/smallville/index.html" "$repo/viewer/smallville/viewer.js" "$repo/viewer/smallville/replay-public.json" "$dest/room-map/"
cp "$repo/viewer/smallville/assets-cc0/tinydungeon.png" "$repo/viewer/smallville/assets-cc0/TinyDungeon-License.txt" "$dest/room-map/assets-cc0/"
cp "$repo/scripts/vendor/graph-viewer.js" "$dest/graph-viewer.js"
cp "$repo/evidence/renders/world-replay-studio-v0.html" "$dest/play/index.html"
cp "$repo/evidence/renders/world-builder-v0.html" "$dest/build/index.html"
cp "$repo/docs/plans/attempt-from-belief/index.html" "$dest/design/attempt-from-belief/index.html"
printf '/world-builder/*\n  Cache-Control: public, max-age=0, must-revalidate\n' > "$here/dist/_headers"
for f in index.html graph-viewer.js play/index.html build/index.html design/attempt-from-belief/index.html room-map/index.html room-map/viewer.js room-map/assets-cc0/tinydungeon.png; do test -s "$dest/$f"; done
echo "world-builder pages ready: $(find "$here/dist" -type f | wc -l) files"
