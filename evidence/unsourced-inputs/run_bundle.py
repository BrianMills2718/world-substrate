"""Generate one world bundle for description.txt with the repo checkout given as argv[1]; write bundle + not_modeled to argv[2]."""
import json, sys, uuid
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo)); sys.path.insert(0, str(repo / "src"))
from scripts.generate_world_bundle import generate_world_bundle
trace = "model-more/bundle/" + uuid.uuid4().hex
text = (Path(__file__).parent / (sys.argv[3] if len(sys.argv) > 3 else "description.txt")).read_text().strip()
bundle, not_modeled, result = generate_world_bundle(text, trace_id=trace, world_kind="ongoing")
Path(sys.argv[2]).write_text(json.dumps({"trace_id": trace, "cost": getattr(result, "cost", None),
                                          "not_modeled": not_modeled, "bundle": bundle}, indent=2) + "\n")
print(trace, getattr(result, "cost", None), not_modeled)
