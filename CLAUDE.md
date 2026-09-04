# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is the GitHub profile README repository (`anmolp1/anmolp1`). Its README renders on the user's GitHub profile page and is written for a consulting-client audience: it argues the "AI over BI" thesis (AI agents layered on the semantic/analytics stack, above dashboards) and features Keystone (mldeep.io/keystone), agentdx (PyPI), and executive command-center engagements. There is no application code, build system, linter, or test suite — the "product" is `README.md` plus the generated SVG assets in `dist/` that it embeds via absolute `github.com/anmolp1/anmolp1/raw/main/dist/...` URLs.

## Architecture

Every visual asset ships in dark + light variants selected with `<picture>`/`prefers-color-scheme` in the README. Shared palette: ink `#E6EDF3`/`#1F2328`, muted `#8B949E`/`#57606A`, amber accent `#E8963A`/`#B45309` (dark/light respectively).

- `scripts/generate_header.py` — the header wordmark (`dist/header-{dark,light}.svg`): name, the "AI *over* BI" mark (serif-italic accent on "over"), and the founder line. Text is converted to vector paths with `fontTools` because GitHub blocks external fonts inside README SVGs; requires `pip install fonttools` and the vendored OFL-licensed IBM Plex fonts in `scripts/fonts/`. Run manually after copy changes: `python3 scripts/generate_header.py`.
- `scripts/generate_lang_chart.py` — stdlib-only; fetches language bytes across all repos from the GitHub API (needs `GH_TOKEN`, e.g. `GH_TOKEN=$(gh auth token)`) and renders `dist/lang-chart-{dark,light}.svg`. Bar fills keep GitHub's per-language colors; only the chrome follows the shared palette.
- `.github/workflows/update-lang-chart.yml` — weekly (Sunday midnight UTC), regenerates and commits both chart variants.

Generated SVGs in `dist/` are committed — after regenerating locally, the change must be committed and pushed for the profile to update.

## Gotchas

- The repo lives on an external exFAT-style volume; macOS creates `._*` AppleDouble files everywhere. They are gitignored — never commit or try to clean them up as part of a change.
- The old terminal-themed README (matrix-green prompt SVGs, pixel-art header, contribution snake + its 15-minute workflow) was retired in 2026-09; don't reintroduce those patterns. The "Update snake files" commits dominating older history are from the deleted snake workflow.
- The anonymized "Selected work" lines in the README are client-engagement claims the user vets personally — never edit or extend them without explicit confirmation.
