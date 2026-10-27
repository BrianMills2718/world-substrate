"""Write rules for the bundle in argv[2] with the repo checkout argv[1]; save to argv[3]."""
import json, sys, uuid
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo)); sys.path.insert(0, str(repo / "src"))
from scripts.generate_causal_model import generate_causal_model
bundle = json.loads(Path(sys.argv[2]).read_text())["bundle"]
trace = "model-more/rules/" + uuid.uuid4().hex
causal, result = generate_causal_model(bundle, trace_id=trace, world_kind="ongoing")
Path(sys.argv[3]).write_text(json.dumps({"trace_id": trace, "cost": getattr(result, "cost", None), "causal_model": causal}, indent=2) + "\n")
print(trace, getattr(result, "cost", None))
