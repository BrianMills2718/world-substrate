"""How a script names a file it just wrote or checked.

Every evidence script accepts `--output` and printed
`path.relative_to(REPO)`, which raises `ValueError` on any path outside the
repository -- including an ordinary relative one, because `--output foo.json`
resolves against the working directory rather than the repo root. The failure
lands *after* the file is written, so the run succeeds, the evidence is on
disk, and the script exits non-zero with a traceback that looks like the work
failed. That happened twice: once in the authoring experiment, where it was
fixed in place, and once in the policy runner, where the same call had been
left alone and produced a confusing failure on a completed 16-turn model run.

Ten scripts share the pattern, so this is the one definition of it.
"""

from __future__ import annotations

import os
from pathlib import Path


def display_path(path: Path | str, root: Path) -> str:
    """A short, human-readable name for `path`, relative to `root` when it can be.

    Never raises. A path outside `root` is shown absolute rather than as a
    chain of `../` segments, which is what it means and is shorter to read.
    """
    resolved = Path(path).resolve()
    relative = os.path.relpath(resolved, Path(root).resolve())
    return str(resolved) if relative.startswith("..") else relative
