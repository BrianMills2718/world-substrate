"""Rebuild a World Builder world from the AI answers a live build used, with no AI calls (tests/AGENTS.md, #215).

The saved answers (spec, actions, rules) go through the real pipeline (people_world.prepare_people_world and
write_people_rules) behind a stand-in llm_client, so today's compiled rules, merges and checks apply to them.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def _stand_in(responses: dict[str, str]) -> ModuleType:
    module = ModuleType("llm_client")

    def call_llm_structured(model, messages, schema, *, task, **_):
        return schema.model_validate_json(responses[task]), SimpleNamespace(cost=0.0, model="replay")

    def call_llm(model, messages, *, task="world-substrate-mechanic-authoring", **_):
        return SimpleNamespace(content=responses[task], cost=0.0, model="replay")

    module.call_llm_structured = call_llm_structured
    module.call_llm = call_llm
    module.safe_json_loads = json.loads
    module.OpenRouterRoutePolicyV1 = lambda **kw: SimpleNamespace(**kw)
    return module


def replay(fixture: str | Path) -> dict[str, Any]:
    """The finished world (people_world.assemble_people_world's result) rebuilt from a saved build."""
    sys.path.insert(0, str(ROOT))
    from scripts import people_world

    saved = json.loads(Path(fixture).read_text())
    with patch.dict(sys.modules, {"llm_client": _stand_in(saved["responses"])}):
        prepared = people_world.prepare_people_world(saved["description"], trace_id="replay", max_budget=0.0,
                                                     progress=lambda *a, **k: None)
        return people_world.write_people_rules(prepared, trace_id="replay", max_budget=0.0,
                                               progress=lambda *a, **k: None)
