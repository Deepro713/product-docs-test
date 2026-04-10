# Product Documentation System

<p align="right">
  <a href="#developer-cheatsheet">
    <img alt="Developer Cheatsheet" src="https://img.shields.io/badge/Developer-Cheatsheet-0A66C2?style=for-the-badge" />
  </a>
</p>

This repository is a multi-version documentation system built with Sphinx.

It is designed to:
- Build every documentation version from folders named `docs-v*`.
- Publish each version to its own output path.
- Always publish the newest version again as `docs-latest`.
- Keep local build output in `site/` for preview while preventing accidental commits.

## What This System Does

1. Versioned docs sources
- Each version is a folder at repo root, for example:
  - `docs-v0.1`
  - `docs-v0.2`
  - `docs-v0.3`

2. Shared config with per-version uniqueness
- Shared configuration logic lives in `conf_main.py`.
- Each version still has its own `conf.py` that only sets its own `doc_version` through the shared builder.
- This keeps behavior consistent while preserving version identity.

3. Latest alias behavior
- The highest semantic version (for example `v0.3`) is treated as latest.
- Navigation labels it as `Latest`.
- Build output includes both:
  - `site/docs-vX.Y/html`
  - `site/docs-latest/html`

4. CI publishing
- GitHub Actions builds docs and force-pushes generated site contents to the `site-files` branch.
- Intended flow: merge your PR to `main`, then CI updates `site-files`.

## Project Layout

- `.github/workflows/build.yml`: CI build and publish workflow.
- `conf_main.py`: shared Sphinx configuration generator.
- `docs-v*/conf.py`: thin wrappers that set `doc_version`.
- `docs-v*/index.md`, `docs-v*/test.md`: versioned docs content.
- `site/`: local generated output (ignored by Git).
- `requirements.txt`: Python package dependencies.

## Prerequisites

- Python 3.11+ recommended.
- Install dependencies from `requirements.txt`.

## Quick Start (Local)

1. Create and activate a virtual environment (example):

```bash
python3 -m venv .venv-docs
source .venv-docs/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2. Build all versions plus `docs-latest`:

```bash
find site -mindepth 1 -maxdepth 1 -exec rm -rf {} + && for DOC_DIR in $(ls -d docs-v* | sort -V); do python -m sphinx -b html -W --keep-going "$DOC_DIR" "site/$DOC_DIR/html"; done && LATEST_DOC_DIR=$(ls -d docs-v* | sort -V | tail -n1) && python -m sphinx -b html -W --keep-going "$LATEST_DOC_DIR" site/docs-latest/html
```

3. Open output files directly from:
- `site/docs-v0.1/html/index.html`
- `site/docs-v0.2/html/index.html`
- `site/docs-v0.3/html/index.html`
- `site/docs-latest/html/index.html`

## Why `mindepth` and `maxdepth` Are Used

The cleanup command starts with:

```bash
find site -mindepth 1 -maxdepth 1 -exec rm -rf {} +
```

- `-mindepth 1`: do not delete the `site` folder itself.
- `-maxdepth 1`: target only direct children under `site`.
- Each direct child is removed recursively via `rm -rf`, so nested generated files are fully cleaned.

This is a safe and controlled way to clean build output.

## Adding a New Documentation Version

Suppose you want to add `v0.4`.

1. Copy an existing version folder:

```bash
cp -R docs-v0.3 docs-v0.4
```

2. Update only one line in `docs-v0.4/conf.py`:
- `doc_version="v0.4"`

3. Edit content files under `docs-v0.4/`.

4. Re-run the full build command.

Result:
- `site/docs-v0.4/html` is created.
- `site/docs-latest/html` is automatically refreshed from `v0.4`.
- Version switcher includes `v0.4` and marks it as latest.

## How Version Discovery Works

`conf_main.py` discovers all source folders that match `docs-v*` at repo root, sorts them semantically, and computes:
- current version
- latest version
- version dropdown links

To keep discovery reliable:
- Keep version folders at repo root.
- Use consistent semantic naming like `docs-v0.4`, `docs-v1.0`.

## CI Workflow Summary

Workflow file: `.github/workflows/build.yml`

On push to `main` (for docs and workflow changes):
1. Install dependencies.
2. Build every `docs-v*` folder to `site/docs-v*/html`.
3. Build highest version again to `site/docs-latest/html`.
4. Add `CNAME`.
5. Publish generated content to `site-files` branch.

## Git Ignore Policy

Ignored locally:
- `site/` (generated output)
- `.venv-docs/` (local environment)

This keeps source branch clean while still letting you inspect local HTML output.

## Troubleshooting

1. `sphinx-build: command not found`
- Activate your virtual environment.
- Or use `python -m sphinx ...` instead of `sphinx-build ...`.

2. Latest version not what you expect
- Check folder naming and semantic order (`docs-v0.9` < `docs-v1.0`).

3. New version not appearing in switcher
- Ensure folder matches `docs-v*` and exists at repo root.
- Rebuild after creating/updating the version folder.

## Maintenance Tips

- Keep shared logic in `conf_main.py`.
- Keep each version `conf.py` minimal.
- Add real content progressively while preserving placeholder pages for smoke tests.
- Run local build before pushing changes to verify all versions and `docs-latest`.

## Developer Cheatsheet

Setup:

```bash
python3 -m venv .venv-docs && source .venv-docs/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
```

Build all versions + latest:

```bash
find site -mindepth 1 -maxdepth 1 -exec rm -rf {} + && for DOC_DIR in $(ls -d docs-v* | sort -V); do python -m sphinx -b html -W --keep-going "$DOC_DIR" "site/$DOC_DIR/html"; done && LATEST_DOC_DIR=$(ls -d docs-v* | sort -V | tail -n1) && python -m sphinx -b html -W --keep-going "$LATEST_DOC_DIR" site/docs-latest/html
```

Add new version (example v0.4 from v0.3):

```bash
cp -R docs-v0.3 docs-v0.4 && sed -i '' 's/doc_version="v0.3"/doc_version="v0.4"/' docs-v0.4/conf.py
```

Publish readiness check (before push to main):

```bash
test -f .github/workflows/build.yml && git check-ignore -v site/placeholder .venv-docs/placeholder && git status --short
```
