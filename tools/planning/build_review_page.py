"""Build the planning-package review page's data file from the package itself.

Reads the manifest, the open-questions ledger, the domain graph, the open-questions map, the
context diagrams in docs/model/ODD.md, the disagreements in docs/model/DOMAIN.md and
the next plan, and writes proposals/planning-package/review-page/data.js. The page (index.html next
to it) only renders that data, so the page cannot say anything the package files do not.

  python3 tools/planning/build_review_page.py
"""
import json
import pathlib
import re

REPO = pathlib.Path(__file__).resolve().parents[2]
PAGE = REPO / "proposals" / "planning-package" / "review-page"


def _read(rel: str) -> str:
    return (REPO / rel).read_text(encoding="utf-8")


def _section(markdown: str, heading: str) -> str:
    start = markdown.index(heading)
    rest = markdown[start + len(heading):]
    nxt = re.search(r"^## ", rest, flags=re.M)
    return rest[: nxt.start()] if nxt else rest


def main() -> None:
    manifest = json.loads(_read("docs/planning/planning-package.json"))
    parts = manifest["parts"]
    ledger = json.loads(_read(parts["open_questions"]["path"]))
    domain = json.loads(_read(parts["domain_model"]["path"]))
    qmap = json.loads(_read("docs/model/open-questions.graph.json"))
    architecture = _read("docs/model/ODD.md")
    diagrams = re.findall(r"```mermaid\n(.*?)```", architecture, flags=re.S)
    disagreements = [re.sub(r"\s+", " ", item).strip() for item in
                     re.split(r"^\d+\. ", _section(_read(parts["domain_model"]["glossary"]),
                                                   "## Where the sources disagree"), flags=re.M)[1:]]
    revision = manifest["subject_revision"][:7]
    data = {
        "manifest": manifest,
        "questions": ledger["questions"],
        "domain": domain,
        "question_map": qmap,
        "context_diagrams": diagrams,
        "disagreements": disagreements,
        "next_plan": _read(parts["plan"]["path"]),
        "built_from": revision,
    }
    PAGE.mkdir(parents=True, exist_ok=True)
    (PAGE / "data.js").write_text("window.PAGE_DATA = " + json.dumps(data, ensure_ascii=False, indent=1)
                                  + ";\n", encoding="utf-8")
    print(f"questions={len(ledger['questions'])} concepts={len(domain['nodes'])} "
          f"context_diagrams={len(diagrams)} disagreements={len(disagreements)} built_from={revision}")


if __name__ == "__main__":
    main()
