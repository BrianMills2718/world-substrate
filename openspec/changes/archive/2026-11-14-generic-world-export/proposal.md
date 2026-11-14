## Why

The first live build with a Builder-proposed layout (a clinic, 2026-11-14, share hn4jUQnwJH5g) crashed the room-map replay: the exporter only knew the pump's four action kinds ("check-in" raised a KeyError). Found by checking the live share link, as the plan required.

## What Changes

- Any action kind shows (its name plus the people, places or doors it names, with a neutral icon); a move only walks when its destination is a laid-out room.
- A door whose world has no open-door action is drawn open from the step someone first walks through it.
