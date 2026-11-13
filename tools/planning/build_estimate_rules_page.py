"""Build the estimate-rules review page from its hand-written body and the planning package.

proposals/estimate-rules/review-page/index.html is generated (same pattern as the declared-laws page): the head and the style come from the open-attempt
page (one look for both plan pages), the body from body.html beside it, and the package and maps sections from
build_open_attempt_page's section builders pointed at this plan's package, so they cannot drift from the files.

  python3 tools/planning/build_estimate_rules_page.py
"""
import json

import build_open_attempt_page as oa

PAGE = oa.REPO / "proposals" / "estimate-rules" / "review-page"
SOURCE = oa.REPO / "proposals" / "open-attempt" / "review-page" / "index.html"


def main() -> None:
    oa.PAGE, oa.PACKAGE = PAGE, "docs/planning/estimate-rules/planning-package.json"
    # The active open-attempt page now uses its own document renderer. Preserve
    # this legacy page's scaffold while refreshing its governed package sections.
    src = (PAGE / "index.html").read_text(encoding="utf-8")
    style = src[src.index("<style>"):src.index("</style>") + len("</style>")]
    viewer = src[src.index('<script src="../../planning-package/review-page/graph-viewer.js">'):src.index("</body>")]
    text = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<title>Estimate Rules Plan</title>\n" + style + "\n</head>\n<body>\n"
            + (PAGE / "body.html").read_text(encoding="utf-8") + viewer + "</body>\n</html>\n")
    domain = oa._json("docs/model/domain.graph.json")
    qmap = oa._json("docs/model/open-questions.graph.json")
    text = oa._replace(text, "maps", oa.maps_section(domain, qmap))
    package, n_checks, n_open, n_resolved = oa.package_section()
    text = oa._replace(text, "package", package)
    (PAGE / "index.html").write_text(text, encoding="utf-8")
    print(f"estimate-rules page: {n_checks} checks, {n_open} open and {n_resolved} resolved questions, "
          f"domain map {len(domain['nodes'])} nodes, questions map {len(qmap['nodes'])} nodes")


if __name__ == "__main__":
    main()
