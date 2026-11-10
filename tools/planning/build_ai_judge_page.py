"""Build the ai-judge review page from its hand-written body and the planning package.

proposals/ai-judge/review-page/index.html is generated (same pattern as the declared-laws page): the head and the style come from the open-attempt
page (one look for both plan pages), the body from body.html beside it, and the package and maps sections from
build_open_attempt_page's section builders pointed at this plan's package, so they cannot drift from the files.

  python3 tools/planning/build_ai_judge_page.py
"""
import json

import build_open_attempt_page as oa

PAGE = oa.REPO / "proposals" / "ai-judge" / "review-page"
SOURCE = oa.REPO / "proposals" / "open-attempt" / "review-page" / "index.html"


def context_section() -> str:
    """The system context and container views, drawn from the Mermaid blocks of docs/model/ODD.md section 3, so the
    page shows the diagrams the package lists rather than only linking to them."""
    odd = (oa.REPO / "docs" / "model" / "ODD.md").read_text(encoding="utf-8")
    boundary = odd[odd.index("## 3. Boundary"):odd.index("\n## 4.")]
    blocks = [b.split("```", 1)[0].strip() for b in boundary.split("```mermaid")[1:]]
    pre = "\n".join(f'<pre class="mermaid">{oa.e(b)}</pre>' for b in blocks)
    return f'''<!-- context:start -->
<h2 id="context">Where World Substrate sits, and what is inside it</h2>
<p class="lede">The system context (who and what talks to World Substrate) and its containers (the parts inside), drawn from <a href="{oa.BLOB}docs/model/ODD.md">ODD.md</a> section 3. The judge adds no container: it runs inside the run loop as Concordia's game master component, reaches the model only through llm_client, and its rulings go through the same compiler and Engine as every other rule.</p>
<style>.mermaid{{background:var(--panel,#fff);border:1px solid var(--line,#ddd);border-radius:12px;padding:12px;margin:0 0 12px;overflow-x:auto;max-width:100%}}</style>
{pre}
<script src="../../planning-package/review-page/mermaid.min.js"></script>
<script>(function(){{if(!window.mermaid)return;var dark=window.matchMedia&&window.matchMedia("(prefers-color-scheme: dark)").matches;mermaid.initialize({{startOnLoad:false,theme:dark?"dark":"neutral",securityLevel:"strict"}});mermaid.run({{querySelector:"pre.mermaid"}});}})();</script>
<!-- context:end -->
'''


def main() -> None:
    oa.PAGE, oa.PACKAGE = PAGE, "docs/planning/ai-judge/planning-package.json"
    src = SOURCE.read_text(encoding="utf-8")
    style = src[src.index("<style>"):src.index("</style>") + len("</style>")]
    viewer = src[src.index('<script src="../../planning-package/review-page/graph-viewer.js">'):src.index("</body>")]
    text = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<title>AI Judge Plan</title>\n" + style + "\n</head>\n<body>\n"
            + (PAGE / "body.html").read_text(encoding="utf-8") + viewer + "</body>\n</html>\n")
    domain = oa._json("docs/model/domain.graph.json")
    qmap = oa._json("docs/model/open-questions.graph.json")
    text = oa._replace(text, "maps", oa.maps_section(domain, qmap))
    text = oa._replace(text, "context", context_section())
    text = oa._replace(text, "types", oa.types_section())
    package, n_checks, n_open, n_resolved = oa.package_section()
    text = oa._replace(text, "package", package)
    (PAGE / "index.html").write_text(text, encoding="utf-8")
    print(f"ai-judge page: {n_checks} checks, {n_open} open and {n_resolved} resolved questions, "
          f"domain map {len(domain['nodes'])} nodes, questions map {len(qmap['nodes'])} nodes")


if __name__ == "__main__":
    main()
