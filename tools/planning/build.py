"""Build the planning package model files from domain_src.py and questions_src.py: docs/model/domain.graph.json,
docs/model/DOMAIN.md, docs/planning/open-questions.json and docs/model/open-questions.graph.json.

  python3 tools/planning/build.py
"""
import json, sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from domain_src import KINDS, NODES, EDGES
from questions_src import Q
R = str(__import__('pathlib').Path(__file__).resolve().parents[2]) + '/'
ids = {n[0] for n in NODES}
kinds = {k: {"label": l, "color": c, **({"dashed": True} if d else {}), "explain": e} for k, (l, c, d, e) in KINDS.items()}
g = {"schema": "typed-graph/v1", "kinds": kinds,
     "nodes": [{"id": i, "label": l, "kind": k, "explain": f"{d} Code: {c}."} for i, l, k, d, s, c in NODES],
     "edges": [{"id": f"e{n}", "source": a, "target": b, "label": lab} for n, (a, b, lab) in enumerate(EDGES)],
     "layout": {"direction": "DOWN"}}
for a, b, _ in EDGES: assert a in ids and b in ids, (a, b)
json.dump(g, open(R + 'docs/model/domain.graph.json', 'w'), indent=1, ensure_ascii=False)
for q in Q:
    for t in q['touches']: assert t in ids, (q['id'], t)
json.dump({"schema_version": "1.0", "record_type": "open_questions", "questions": Q}, open(R + 'docs/planning/open-questions.json', 'w'), indent=1, ensure_ascii=False)
# open-questions map
qk = {"AgentQuestion": {"label": "Checking can settle it", "color": "#3b6fa8", "explain": "An open question an agent can settle by reading, running or testing."},
      "BrianQuestion": {"label": "Brian's call", "color": "#d9822b", "explain": "A product or priority question; it carries a recommendation and a default."},
      "Concept": {"label": "Concept", "color": "#7a8491", "explain": "A domain-model concept; open the Domain model tab for its definition."}}
open_q = [q for q in Q if q['status'] == 'open' and q['touches']]
used = sorted({t for q in open_q for t in q['touches']})
byid = {n[0]: n for n in NODES}
qm = {"schema": "typed-graph/v1", "kinds": qk,
      "nodes": [{"id": q['id'], "label": f"{q['id']}: {q['short']}", "kind": "BrianQuestion" if q['owner'] == 'brian' else "AgentQuestion",
                 "explain": f"Blocks: {q['blocks']}."} for q in open_q]
             + [{"id": t, "label": byid[t][1], "kind": "Concept", **({"dashed": True} if byid[t][2] == 'Theory' else {}), "explain": byid[t][3]} for t in used],
      "edges": [{"id": f"{q['id']}-{t}", "source": q['id'], "target": t, "label": "bears on"} for q in open_q for t in q['touches']],
      "layout": {"direction": "RIGHT"}}
json.dump(qm, open(R + 'docs/model/open-questions.graph.json', 'w'), indent=1, ensure_ascii=False)
# glossary
lines = ["---", "description: Domain model of World Substrate: the ideas it is about, which are fixed code and which an AI writes per world.", "---", "",
 "# World Substrate domain model", "",
 "The graph is [domain.graph.json](domain.graph.json) (Representation Router `typed-graph/v1`). This page is its glossary.",
 "The model's main job is to keep two levels apart: **the substrate** (code every world runs through) and **one world** (what an AI writes for a described world, or the hand-written Waltzman reference). A problem is a substrate problem when the concept it lives in is one of the first two kinds below.", ""]
for k, (l, c, d, e) in KINDS.items():
    lines += [f"## {l}", "", e, "", "| Concept | Definition | Defined in | Code |", "| --- | --- | --- | --- |"]
    for i, lab, kk, de, s, co in NODES:
        if kk == k: lines.append(f"| **{lab}** (`{i}`) | {de} | `{s}` | `{co}` |")
    lines.append("")
lines += ["## Where the sources disagree", "",
 "1. **Decision 008 versus the live build.** Decision 008 says worlds are built in an agent harness that drafts, checks and edits; the live service builds with fixed calls and a rules retry and does not import `scripts/world_harness.py` (open question Q14).",
 "2. **The wiki's 'Concepts and terminology' versus this model.** The wiki (`docs/wiki/README.md`) defines engine-level terms only; people, concerns, support, tasks and residents are defined here and in ODD section 11, not there.",
 ""]
open(R + 'docs/model/DOMAIN.md', 'w').write("\n".join(lines))
print("nodes", len(g['nodes']), "edges", len(g['edges']), "questions", len(Q), "open", sum(q['status']=='open' for q in Q), "map nodes", len(qm['nodes']))
