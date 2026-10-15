#!/usr/bin/env bash
# Assemble the native-run replay pages from world-substrate's committed run evidence.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
repo=$(cd "$here/../../.." && pwd)
src="$repo/spikes/any-scenario-2026-10/evidence/waltzman-spec/run2/run"
root="$here/dist/world-substrate-runs"
rm -rf "$here/dist"
mkdir -p "$root/waltzman-native"
cp "$here/index.html" "$root/index.html"
cp "$src/frames.html" "$root/waltzman-native/index.html"
cp "$src"/frame-*.png "$root/waltzman-native/"
printf '/world-substrate-runs/*\n  Cache-Control: public, max-age=0, must-revalidate\n' > "$here/dist/_headers"
for f in index.html waltzman-native/index.html; do test -s "$root/$f"; done
echo "native-run pages ready: $(find "$here/dist" -type f | wc -l) files"
