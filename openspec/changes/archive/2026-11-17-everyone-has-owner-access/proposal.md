## Why

Brian, 2026-11-17: "we can turn off owner access i.e. everyone ahs the same access", then chose "A everyone gets owner level" over private per-browser libraries or no saving. His builds ran as a visitor and were not saved.

## What Changes

- With `WORLD_BUILDER_OPEN_ACCESS=1` on the server, every request is the owner: no password, one shared library, one shared owner daily allowance ($5/day for everyone), per-visitor rate limits skipped. Off by default; `=0` or removing it restores the password. `/health` says `open_access`.
- The page hides Owner access and the not-saved notice when open access is on, and shows the library to everyone.
- Supersedes the goal boundary "owner library stays owner-only" on his word.
