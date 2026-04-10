from datetime import datetime, timezone
from pathlib import Path

project = "DKubeX 2.0 Documentation"
author = "DKube"
doc_version = "v0.2"
build_date = datetime.now(timezone.utc).strftime("%d.%m.%Y")

def version_key(version: str):
    return tuple(int(part) for part in version.lstrip("vV").split("."))


repo_root = Path(__file__).resolve().parent.parent
discovered_versions = []
for directory in repo_root.glob("docs-v*"):
    if directory.is_dir():
        discovered_versions.append(directory.name.replace("docs-", "", 1))

documentation_versions = [
    {"version": version}
    for version in sorted(discovered_versions, key=version_key)
]

if not documentation_versions:
    documentation_versions = [{"version": doc_version}]


def version_url(version: str, latest: str):
    if version == latest:
        return "../../docs-latest/html/index.html"
    return f"../../docs-{version}/html/index.html"


latest_version = max((item["version"] for item in documentation_versions), key=version_key)
current_version_url = next(
    (
        version_url(item["version"], latest_version)
        for item in documentation_versions
        if item["version"] == doc_version
    ),
    "../../docs-v0.2/html/index.html",
)

version_links = []
for item in documentation_versions:
    version = item["version"]
    if version == doc_version:
        continue

    version_links.append(
        {
            "title": f"{version} | Latest" if version == latest_version else version,
            "url": version_url(version, latest_version),
            "summary": "Latest stable release" if version == latest_version else "Previous release",
            "resource": True,
        }
    )

copyright = (
    f"&copy; 2026, dkube.io. All rights reserved. Last updated on: {build_date}. Documentation version: {doc_version}"
)

extensions = [
    "myst_parser",
    "sphinx.ext.githubpages",
    "sphinx_copybutton",
]

myst_enable_extensions = [
    "substitution",
]

myst_substitutions = {
    "doc_version": doc_version,
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "shibuya"
html_title = project
html_static_path = ["_static"]
html_logo = "_static/DKube_Icon_512x512.svg"
html_theme_options = {
    "logo_target": "index.html",
    "github_url": "https://github.com/deepro713/product-docs-test/",
    "youtube_url": "https://www.youtube.com/@DKube_OC",
    "nav_links": [
        {
            "title": (
                f"Version: {doc_version} | Latest"
                if doc_version == latest_version
                else f"Version: {doc_version}"
            ),
            "url": current_version_url,
            "resource": True,
            "children": version_links,
        },
    ],
}
html_css_files = ["custom.css"]
html_js_files = ["version-badge.js", "footer-dkube-link.js"]
html_baseurl = "https://docs-test.dkube.io/"
html_favicon = "_static/DKube_Icon_512x512.svg"