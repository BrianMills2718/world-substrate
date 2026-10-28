import json,sys
from llm_client import call_llm_json_schema
x=[json.loads(l) for l in open(__import__('pathlib').Path(__file__).with_name('llm-calls.jsonl')) if '"id": 22108' in l][0]
r=json.loads(x['call_snapshot'])['request']
for mt in (400,4000):
    try:
        v,res=call_llm_json_schema(r['requested_model'],r['messages'],r['response_model_schema'],schema_name="world_substrate_attempt_reading",
            task="world-builder-attempt-interpreter",trace_id=f"s2p3-repro/{mt}",max_budget=0.05,max_tokens=mt,reasoning_effort="low")
        print(mt,'OK',json.dumps(v)[:300],getattr(res,'usage',None))
    except Exception as e: print(mt,'FAIL',type(e).__name__,str(e)[:200])
