#!/usr/bin/env bash
# One command to ship the World Builder: local gate, backend to the VPS, pages to Cloudflare,
# then verify both are live at the deployed revision.
#
#   scripts/deploy_world_builder.sh [revision, default origin/main]
#
# Needs: ssh personal-vps; ~/.secrets/api_keys.env with CLOUDFLARE_API_KEY and CLOUDFLARE_EMAIL;
# a checkout of BrianMills2718/personal-vps at ~/code/personal-vps (for its deploy script).
# Pages are built from the same revision as the backend.
set -euo pipefail
REV=${1:-origin/main}
repo=$(cd "$(dirname "$0")/.." && pwd)
git -C "$repo" fetch -q origin
commit=$(git -C "$repo" rev-parse "$REV")
# A real checkout (some tests read git metadata), detached at the exact revision.
stage="$repo/worktrees/deploy-${commit:0:12}"
git -C "$repo" worktree add -q --detach "$stage" "$commit"
trap 'git -C "$repo" worktree remove "$stage" >/dev/null 2>&1 || true' EXIT
echo "== gate at ${commit:0:12}"
# Concordia is a runtime dependency (people-world residents, deploy/vps/Dockerfile pins the same version); without it
# the resident tests fail at import (2026-10-17, first deploy of #168).
CONCORDIA=gdm-concordia==2.4.0
# check_project runs the whole suite once, in parallel, and stamps the tree it passed on. A squash merge keeps the
# pull request's tree, so a tree that already passed is not run again (2026-10-26: the same tests ran three times
# per change). FORCE_GATE=1 reruns it anyway.
tree=$(git -C "$repo" rev-parse "$commit^{tree}")
stamp="$HOME/.cache/world-substrate/passed-trees/$tree"
if [[ -f "$stamp" && "${FORCE_GATE:-0}" != 1 ]]; then
  echo "check_project skipped: tree ${tree:0:12} passed at $(cat "$stamp")"
else
  log=$(mktemp)
  (cd "$stage" && PYTHONDONTWRITEBYTECODE=1 uv run -q --no-project --python 3.12 --with pydantic --with pytest --with pytest-xdist --with "$CONCORDIA" python scripts/check_project.py >"$log" 2>&1) \
    || { echo "check_project FAILED:" >&2; tail -25 "$log" >&2; exit 1; }
  grep -E "^Neutral runtime tests" "$log" || true
  echo "check_project ok"
fi
echo "== backend"
vps=$(mktemp -d)
git -C "$HOME/code/personal-vps" fetch -q origin
# deploy.sh also runs ../../host/prune-app-images.sh to drop old image tags on the VPS.
git -C "$HOME/code/personal-vps" archive origin/main apps/world-builder host/prune-app-images.sh | tar -C "$vps" -xf -
"$vps/apps/world-builder/deploy.sh" "$repo" "$commit"
rm -rf "$vps"
echo "== pages"
pages="$stage/deploy/cloudflare/world-builder"
(cd "$pages" && npm install --silent >/dev/null 2>&1 && ./build.sh)
set -a; . "$HOME/.secrets/api_keys.env"; set +a
export CLOUDFLARE_API_KEY CLOUDFLARE_EMAIL
wlog=$(mktemp)
(cd "$pages" && node_modules/.bin/wrangler deploy >"$wlog" 2>&1) \
  || { echo "pages deploy FAILED:" >&2; tail -25 "$wlog" >&2; exit 1; }
grep -E "Current Version" "$wlog" || tail -5 "$wlog"
echo "== verify"
want=$(sha256sum < "$pages/dist/world-builder/index.html" | cut -c1-16)
for _ in $(seq 1 20); do
  got=$(curl -s -m 20 "https://brianmills.dev/world-builder/?v=$RANDOM" | sha256sum | cut -c1-16)
  [[ "$got" == "$want" ]] && break
  sleep 3
done
[[ "$got" == "$want" ]] || { echo "live page does not match the deployed build" >&2; exit 3; }
echo "live page matches ${commit:0:12}; backend: $(curl -s -m 20 https://brianmills.dev/world-builder/api/health | python3 -c 'import json,sys; print(json.load(sys.stdin)["build_commit"][:12])')"
