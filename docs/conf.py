from datetime import datetime, timezone

project = "DKubeX 2.0 Documentation`"
author = "DKube"
doc_version = "v0.1"
build_date = datetime.now(timezone.utc).strftime("%d.%m.%Y")
copyright = (
    f"&copy; 2026, dkube.io. All rights reserved. Last updated on: {build_date}. Documentation version: {doc_version}"
)

extensions = [
    "myst_parser",
    "sphinx.ext.githubpages",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "shibuya"
html_title = project
html_static_path = ["_static"]
html_js_files = ["_static/dkube-link.js"]
html_baseurl = "https://docs-test.dkube.io/"
html_favicon = "_static/DKube_Icon_512x512.svg"