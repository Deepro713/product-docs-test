project = "Test Documentation"
author = "DKube"
copyright = "2026, DKube"

extensions = [
    "myst_parser",
    "sphinx.ext.githubpages",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "shibuya"
html_title = "Test Documentation"
html_static_path = ["_static"]
html_baseurl = "https://docs-test.dkube.io/"