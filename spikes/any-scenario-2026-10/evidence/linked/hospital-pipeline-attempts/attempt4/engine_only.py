"""Attempt 4 check with no model calls: advance the generated hospital world (final model = causal.r2.json) for
60 ticks from a set start state, and record every Engine event. The rules are unchanged; only the start state is
set, because the generated world starts with no patients and has no arrival rule left after repair 2.

Run from a world-substrate checkout with its environment: uv run python <this file>
"""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
sys.path[:0] = [str(REPO), str(REPO / "src")]
from scripts.run_authored_world import build_engine  # noqa: E402
from world_substrate.mechanisms.time import ClockAdvanceProcess  # noqa: E402

# 5 critically ill admitted flu patients in beds; no one on a ventilator. With 1 or 3 ventilated patients the
# generated ventilator-failure rule runs first each tick, lowers ventilators_in_use without unhooking a patient,
# and the death rule's own check (ventilators_in_use >= patients_on_ventilators) then never holds.
START = {("flu-patients", "patient_group", "care_status"): "admitted",
         ("flu-patients", "patient_group", "number_of_patients"): 5,
         ("flu-patients", "patient_group", "illness_severity"): 1,
         ("hospital", "hospital_capacity", "occupied_beds"): 5,
         ("hospital", "hospital_capacity", "available_beds"): 35}

bundle = json.loads((HERE / "bundle.json").read_text())
for e in bundle["entities"]:
    for (eid, comp, field), v in START.items():
        if e["id"] == eid:
            e["components"][comp][field] = v
engine, _, _ = build_engine(bundle, json.loads((HERE / "causal.r2.json").read_text()))
engine.registry.register_process(ClockAdvanceProcess())
events = [e for _ in range(60) for e in engine.advance(1)["events"]]
(HERE / "engine_only_start_set_events.jsonl").write_text("".join(json.dumps(e) + "\n" for e in events))
print(Counter(e["rule_id"] for e in events))
