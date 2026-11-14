"""Durable private worlds and immutable round-boundary checkpoint ancestry."""
from __future__ import annotations

import json
import sqlite3
import uuid
import zlib
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


class CatalogError(Exception):
    status = 422


class CatalogConflict(CatalogError):
    status = 409


class CatalogUnavailable(CatalogError):
    pass


class CatalogNotFound(CatalogError):
    status = 404


def _now():
    return datetime.now(timezone.utc).isoformat()


def _pack(value):
    return zlib.compress(json.dumps(value, separators=(",", ":")).encode())


def _unpack(value):
    return json.loads(zlib.decompress(value))


class WorldCatalog:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._db() as db:
            db.executescript("""
            CREATE TABLE IF NOT EXISTS catalog_worlds (
              id TEXT PRIMARY KEY, title TEXT NOT NULL, description TEXT NOT NULL,
              created TEXT NOT NULL, updated TEXT NOT NULL, fingerprint TEXT NOT NULL,
              build_trace_id TEXT UNIQUE, definition BLOB NOT NULL);
            CREATE TABLE IF NOT EXISTS catalog_runs (
              id TEXT PRIMARY KEY, world_id TEXT NOT NULL REFERENCES catalog_worlds(id),
              name TEXT NOT NULL, parent_run_id TEXT REFERENCES catalog_runs(id),
              fork_checkpoint_id TEXT, created TEXT NOT NULL, updated TEXT NOT NULL,
              checkpoint_id TEXT, legacy_share_id TEXT UNIQUE, legacy_record BLOB);
            CREATE TABLE IF NOT EXISTS catalog_checkpoints (
              id TEXT PRIMARY KEY, run_id TEXT NOT NULL REFERENCES catalog_runs(id),
              parent_checkpoint_id TEXT REFERENCES catalog_checkpoints(id),
              round INTEGER NOT NULL, created TEXT NOT NULL, body BLOB NOT NULL);
            CREATE TABLE IF NOT EXISTS catalog_imports (trace_id TEXT PRIMARY KEY,
              run_id TEXT NOT NULL REFERENCES catalog_runs(id));
            CREATE TABLE IF NOT EXISTS catalog_finishes (run_id TEXT PRIMARY KEY REFERENCES catalog_runs(id),
              recorded TEXT NOT NULL, response BLOB NOT NULL);
            """)

    @contextmanager
    def _db(self):
        db = sqlite3.connect(self.path, timeout=30)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        try:
            with db:
                yield db
        finally:
            db.close()

    def _world(self, db, wid):
        row = db.execute("SELECT *, (SELECT COUNT(*) FROM catalog_runs WHERE world_id=catalog_worlds.id) run_count FROM catalog_worlds WHERE id=?", (wid,)).fetchone()
        if row is None:
            raise CatalogNotFound("world not found")
        out = dict(row)
        out["definition"] = _unpack(out["definition"])
        return out

    def save_world(self, definition, fingerprint, build_trace_id=None):
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            if build_trace_id:
                old = db.execute("SELECT id FROM catalog_worlds WHERE build_trace_id=?", (build_trace_id,)).fetchone()
                if old:
                    return self._world(db, old[0])
            wid, now = uuid.uuid4().hex, _now()
            description = str(definition.get("description") or "")
            world = (definition.get("bundle") or {}).get("world") or {}
            title = str(world.get("label") or world.get("name") or description or "Untitled world")[:160]
            db.execute("INSERT INTO catalog_worlds VALUES (?,?,?,?,?,?,?,?)", (wid, title, description, now, now, fingerprint, build_trace_id, _pack(definition)))
            return self._world(db, wid)

    def worlds(self):
        with self._db() as db:
            return [{k: v for k, v in self._world(db, row[0]).items() if k not in {"definition", "build_trace_id"}}
                    for row in db.execute("SELECT id FROM catalog_worlds ORDER BY updated DESC")]

    def _runrow(self, db, rid):
        row = db.execute("SELECT * FROM catalog_runs WHERE id=?", (rid,)).fetchone()
        if row is None:
            raise CatalogNotFound("run not found")
        return dict(row)

    def _chain(self, db, checkpoint_id):
        chain, seen = [], set()
        while checkpoint_id:
            if checkpoint_id in seen:
                raise CatalogConflict("invalid checkpoint ancestry")
            seen.add(checkpoint_id)
            row = db.execute("SELECT * FROM catalog_checkpoints WHERE id=?", (checkpoint_id,)).fetchone()
            if row is None:
                raise CatalogNotFound("checkpoint not found")
            cp = dict(row)
            cp.update(_unpack(cp.pop("body")))
            chain.append(cp)
            checkpoint_id = cp["parent_checkpoint_id"]
        return list(reversed(chain))

    def _eligibility(self, world, cp):
        if cp is None:
            return True, None
        response = cp["response"]
        if response.get("_catalog_replay_only_reason"):
            return False, response["_catalog_replay_only_reason"]
        if not isinstance((response.get("trace") or {}).get("final_snapshot"), dict) or not isinstance(response.get("approval"), dict):
            return False, "This recording has no complete continuation snapshot and approval."
        if (world["definition"].get("bundle") or {}).get("actor_information"):
            state = response.get("actor_state")
            if not isinstance(state, dict) or set(state) != {"resident_memory", "recent", "briefs", "underway", "turn_offset"}:
                return False, "This recording has no complete saved actor cognition; replay remains available."
        stopped = (response.get("summary") or {}).get("stopped")
        # round_cap ends one HTTP segment, not the logical world run.
        if isinstance(stopped, dict) and stopped.get("reason") in {"quiet_rounds", "round_limit", "budget"}:
            why = stopped.get("why")
            return False, (why or "The saved run stop setting was reached.") + " A branch preserves this stop setting; choose an earlier checkpoint or New run."
        if (response.get("summary") or {}).get("active_at_end") is False:
            return False, "This world has no active moves at this saved round."
        return True, None

    def _detail(self, db, row):
        world = self._world(db, row["world_id"])
        chain = self._chain(db, row["checkpoint_id"])
        legacy = _unpack(row["legacy_record"]) if row["legacy_record"] else None
        can, reason = self._eligibility(world, chain[-1] if chain else None)
        if legacy is not None:
            can, reason = False, "Recovered recording: no authenticated continuation checkpoint was retained."
        finish = db.execute("SELECT response FROM catalog_finishes WHERE run_id=?", (row["id"],)).fetchone()
        if finish:
            can, reason = False, "This run has finished under its saved rules and stop conditions."
        summary = {k: row[k] for k in ("id", "world_id", "name", "parent_run_id", "fork_checkpoint_id", "created", "updated", "checkpoint_id")}
        summary.update(latest_round=chain[-1]["round"] if chain else max((r.get("turn", 0) for r in (legacy or {}).get("rounds", [])), default=0),
                       can_continue=can, reason=reason, status="ready" if can else "replay_only")
        if finish:
            summary.update(status="finished", finish_summary=_unpack(finish[0]).get("summary"))
        record = legacy or {"schema": "world-builder-share/v1", "created": row["created"], "world": world["definition"], "rounds": [], "actor_inputs": {}, "runs": [], "world_fingerprint": world["fingerprint"]}
        checkpoints = []
        for cp in chain:
            response, trace = cp["response"], cp["response"].get("trace") or {}
            record["rounds"].extend(trace.get("transcript") or [])
            for actor, inputs in (trace.get("actor_inputs") or {}).items():
                record["actor_inputs"].setdefault(actor, []).extend(inputs)
            record["actor_information_mode"] = trace.get("actor_information_mode", "legacy-unrestricted")
            record["runs"].append({"trace_id": response.get("trace_id"), "policy": cp["request"].get("policy"), **(response.get("summary") or {})})
            eligible, why = self._eligibility(world, cp)
            checkpoints.append({"id": cp["id"], "round": cp["round"], "can_branch": eligible, "reason": why})
        record.update(catalog_world_id=row["world_id"], catalog_run_id=row["id"], checkpoint_id=row["checkpoint_id"], event_namespace=row["id"])
        return {"ok": True, "run": summary, "record": record, "checkpoints": checkpoints}

    def world(self, wid):
        with self._db() as db:
            world = self._world(db, wid)
            runs = [self._detail(db, dict(r))["run"] for r in db.execute("SELECT * FROM catalog_runs WHERE world_id=? ORDER BY updated DESC", (wid,))]
            return {"ok": True, "world": world, "runs": runs}

    def run(self, wid, rid):
        with self._db() as db:
            row = self._runrow(db, rid)
            if row["world_id"] != wid:
                raise CatalogNotFound("run not found in this world")
            return self._detail(db, row)

    def run_by_id(self, rid):
        with self._db() as db:
            return self._detail(db, self._runrow(db, rid))

    def create_run(self, wid, name=None, parent_run_id=None, checkpoint_id=None):
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            world = self._world(db, wid)
            if bool(parent_run_id) != bool(checkpoint_id):
                raise CatalogConflict("a branch requires both parent_run_id and checkpoint_id")
            if parent_run_id:
                parent = self._runrow(db, parent_run_id)
                if parent["world_id"] != wid:
                    raise CatalogConflict("parent belongs to a different world")
                cp = next((c for c in self._chain(db, parent["checkpoint_id"]) if c["id"] == checkpoint_id), None)
                if cp is None:
                    raise CatalogConflict("checkpoint is not in the parent's history")
                can, reason = self._eligibility(world, cp)
                if not can:
                    raise CatalogUnavailable(reason)
            rid, now = uuid.uuid4().hex, _now()
            db.execute("INSERT INTO catalog_runs VALUES (?,?,?,?,?,?,?,?,NULL,NULL)", (rid, wid, str(name or ("Branch" if parent_run_id else "Run"))[:160], parent_run_id, checkpoint_id, now, now, checkpoint_id))
            db.execute("UPDATE catalog_worlds SET updated=? WHERE id=?", (now, wid))
            return self._detail(db, self._runrow(db, rid))

    def resume(self, rid, expected_checkpoint_id=...):
        with self._db() as db:
            row = self._runrow(db, rid)
            if expected_checkpoint_id is not ... and row["checkpoint_id"] != expected_checkpoint_id:
                raise CatalogConflict("this run advanced; reload its latest checkpoint")
            detail = self._detail(db, row)
            if not detail["run"]["can_continue"]:
                raise CatalogUnavailable(detail["run"]["reason"])
            chain = self._chain(db, row["checkpoint_id"])
            cp = chain[-1] if chain else None
            return {"world": self._world(db, row["world_id"]), "run": detail["run"], "checkpoint": cp,
                    "request": cp["request"] if cp else {}, "response": cp["response"] if cp else {}}

    def append(self, rid, expected_checkpoint_id, request, response):
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            row = self._runrow(db, rid)
            if row["checkpoint_id"] != expected_checkpoint_id or row["legacy_record"]:
                raise CatalogConflict("this run advanced; reload its latest checkpoint")
            chain = self._chain(db, row["checkpoint_id"])
            previous = chain[-1]["round"] if chain else 0
            rounds = (response.get("trace") or {}).get("transcript") or []
            summary = response.get("summary") or {}
            if not rounds and summary.get("last_turn") == previous and (summary.get("terminal_reached") is True or summary.get("stopped")):
                db.execute("INSERT OR REPLACE INTO catalog_finishes VALUES (?,?,?)", (rid, _now(), _pack(response)))
                return {"id": expected_checkpoint_id, "round": previous, "finished": True}
            if not rounds or [r.get("turn") for r in rounds] != list(range(previous + 1, previous + len(rounds) + 1)):
                raise CatalogConflict("run result does not continue this exact round boundary")
            last = rounds[-1]["turn"]
            if (response.get("summary") or {}).get("last_turn") != last:
                raise CatalogConflict("result summary and checkpoint round disagree")
            cid, now = uuid.uuid4().hex, _now()
            stored = dict(response)
            stored.pop("replay_html", None)
            db.execute("INSERT INTO catalog_checkpoints VALUES (?,?,?,?,?,?)", (cid, rid, expected_checkpoint_id, last, now, _pack({"request": request, "response": stored})))
            db.execute("UPDATE catalog_runs SET checkpoint_id=?,updated=? WHERE id=?", (cid, now, rid))
            db.execute("UPDATE catalog_worlds SET updated=? WHERE id=?", (now, row["world_id"]))
            return {"id": cid, "round": last}

    def import_share(self, wid, share_id, record):
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            self._world(db, wid)
            old = db.execute("SELECT * FROM catalog_runs WHERE legacy_share_id=?", (share_id,)).fetchone()
            if old:
                return self._detail(db, dict(old))
            rid, now = uuid.uuid4().hex, _now()
            db.execute("INSERT INTO catalog_runs VALUES (?,?,?,NULL,NULL,?,?,NULL,?,?)", (rid, wid, "Recovered recording", now, now, share_id, _pack(record)))
            return self._detail(db, self._runrow(db, rid))

    def import_initial_run(self, wid, trace_id, request, response):
        """Only callers with an explicit fresh-start record may use this import."""
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            self._world(db, wid)
            old = db.execute("SELECT run_id FROM catalog_imports WHERE trace_id=?", (trace_id,)).fetchone()
            if old:
                return self._detail(db, self._runrow(db, old[0]))
            rounds = (response.get("trace") or {}).get("transcript") or []
            if not rounds or [r.get("turn") for r in rounds] != list(range(1, len(rounds) + 1)):
                raise CatalogConflict("recovered segment must explicitly begin at round one")
            if (response.get("summary") or {}).get("last_turn") != len(rounds):
                raise CatalogConflict("recovered segment summary disagrees with its rounds")
            rid, cid, now = uuid.uuid4().hex, uuid.uuid4().hex, _now()
            db.execute("INSERT INTO catalog_runs VALUES (?,?,?,NULL,NULL,?,?,?,NULL,NULL)", (rid, wid, "Recovered first segment", now, now, cid))
            db.execute("INSERT INTO catalog_checkpoints VALUES (?,?,NULL,?,?,?)", (cid, rid, len(rounds), now, _pack({"request": request, "response": response})))
            db.execute("INSERT INTO catalog_imports VALUES (?,?)", (trace_id, rid))
            return self._detail(db, self._runrow(db, rid))
