## Why

Brian, 2026-11-14: "i approve c then b then a" (A: embed the viewer in the workspace as an owner-only scene), after viewing the viewer ("yes looks good"). The viewer uses Smallville's art, which is private-use only, so it cannot be served from the public site or the VPS.

## What Changes

- `scripts/open_scene_viewer.py` runs on the owner's machine: it reads a saved run from the service with the owner password (or from a run-log file), exports it with the world's own layout, and serves the static viewer on localhost.
- Nothing about Smallville's art or map data is deployed. Public scenes still need a free-to-use tileset (open).
