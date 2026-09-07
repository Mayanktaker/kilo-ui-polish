# AGENTS.md — kilo-ui-patch

## Stack
- **Script:** Python 3 stdlib only (`glob`, `os`, `shutil`, `re`) — no deps, no package manager
- **Target:** Kilo Code VS Code extension `dist/` bundles (`agent-manager.css/js`, `webview.css/js`, `marketplace.css`, `documents.css`), tested 7.5.9 → 7.5.15 Linux dark theme
- **Runtime:** system `python3` + VS Code `Developer: Reload Window`
- **Public mirror:** `Mayanktaker/kilo-ui-polish` (local-only patch, never upstream to Kilo-Org)

## Conventions
- File header (all files): `© Mayanktaker Computers & Web Development | https://mayanktaker.com`
- **Idempotent:** `reapply.py` backs up once (`*.before-ui-patch.bak`), applies missing `KILO-*` marks only, safe to run twice
- **CSS-only preferred (2026-09-07 hang rule):** no `MutationObserver` JS — `ENABLE_JS_PATCH=False`; icons via `::before`, active pill via `:has()` + `[data-activity]` selectors (ROUND46/47)
- **JS guard (if ever re-enabled):** rAF throttle + `disconnect()` while mutating + `attributeFilter:['class']` mandatory — see `SAFE_OBSERVE_TPL`; never bare `attributes:true`, never remove+re-add own trigger nodes, never `while(firstChild)` move React nodes
- **Design tokens:** radius scale 4/8/10/14 (`--radius-sm/md/lg/xl`), colors via `color-mix()` + theme vars, sidebar/header `#17181d`, one live ACTIVE pill at a time
- **Literal radius (2026-09-07 token finding):** theme resolves `--radius-lg→4px`/`--md→2px`/`--xl→6px`, so `var()` fallbacks never apply — rows/triggers fixed `10px`, popover `14px` (ROUND52-55)
- **Selector facts:** Kilo Settings dropdowns are `[data-slot=popover-trigger]` not `select-trigger` (ROUND53); hint icons need parent-`nth-child` — `button:nth-child` matches every wrapper child (ROUND51)
- **Reverts on record:** ROUND13/15 (bottom bar, no effect), ROUND29 (reasoning plain), ROUND43-45 (AM sidebar + V3 loop hang) — do not re-add

## Docs
- `README.md` → features, quick start, patch log, rollback
- `ISSUE-DRAFT.md` → upstream issue draft (`packages/ui`, `packages/kilo-ui`)
- Parent `../../AGENTS.md` → Lolu UI design language (shared)
