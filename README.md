# kilo-ui-polish

A hot-patch that brings a polished, cohesive look to the [Kilo Code](https://github.com/Kilo-Org/kilocode) VS Code extension — properly rounded markdown tables, a consistent corner-radius scale, an OpenChamber-style model picker, and cleaner chat bubbles.

> **Why this exists:** every Kilo Code update overwrites the extension bundle in
> `~/.vscode/extensions/kilocode.kilo-code-*/dist/`, wiping any manual edits.
> This repo ships a single idempotent script that re-applies the full patch set
> after every update — one command, ten seconds.

## Features

| Area | What you get |
|---|---|
| **Markdown tables** | Full border box with rounded corners on all four sides, tinted header with a `2px` rule, zebra rows, row hover, horizontal scroll that never breaks column alignment |
| **Chat messages** | User messages in a blue-tinted bubble that stands out during long sessions; assistant replies stay clean; copy/feedback icons moved outside the card |
| **Question prompts** | Two-tone card — dark header band, separate answers list with clean hover states |
| **Model picker** | Wider popover with full model names (no truncation), rounded search and rows, prominent select-style triggers, OpenChamber-inspired selection |
| **Agent Manager sidebar** | 10px project/session/worktree rows, blue highlight on the active project and session |
| **Global consistency** | Buttons, tags, badges, tool cards, and list items unified on a 4 / 8 / 10 / 14px radius scale |

All values are aligned with the
[Kilo design system](https://github.com/Kilo-Org/kilo-design) (`tokens.json`
v0.2.0) — colors flow through theme variables and `color-mix()` so light and
high-contrast themes inherit correctly.

## Quick start

```bash
python3 reapply.py
```

Then in VS Code: **Developer: Reload Window**.

The script:

- auto-detects the newest installed Kilo version (semver sort),
- backs up each file once (`*.before-ui-patch.bak`),
- is **idempotent** — re-running only applies missing blocks,
- covers `agent-manager.css`, `webview.css`, `marketplace.css`,
  `documents.css`, plus table-wrapper injection in `webview.js` and
  `agent-manager.js`.

## Rollback

Every patched file keeps a one-time backup next to the original:

```bash
cp ~/.vscode/extensions/kilocode.kilo-code-*/dist/agent-manager.css.before-ui-patch.bak \
   ~/.vscode/extensions/kilocode.kilo-code-*/dist/agent-manager.css
```

## Patch log

<details>
<summary>Full change log (click to expand)</summary>

| Patch | Files | Change |
|---|---|---|
| TABLE-FIX-V1 | 3 CSS + 2 JS | Markdown tables: bordered box, `10px` radius, header tint, wrapper div for scroll-safe corners |
| ROUND2-V1 | CSS | 10px unification: user bubble, code blocks, images, question options, inputs |
| ROUND3-V1 | CSS | Question dock card: raised background, border, shadow |
| ROUND4-V1 | CSS | Option hover states, tool cards, table zebra rows |
| ROUND5-V1 | CSS | Options as joined rows; buttons, tags, badges 10px |
| ROUND6-V1 | CSS | Removed outer options border (dividers kept) |
| ROUND7-V1 | CSS | Model selector: popover, search, rows, select button rounding |
| ROUND8-V1 | CSS | Popover shell + inner list rows (incl. active/selected) |
| ROUND9-V1 | CSS | Removed outline on active model row |
| ROUND10-V1 | CSS | Premium table header: tint, semibold, `2px` rule |
| ROUND11-V1 | CSS | Dark popover + gradient selection (OpenChamber vibe) |
| ROUND12-V1 | CSS | Two-tone question card |
| ROUND13-V1 | — | Reverted (no visual effect) |
| ROUND14-V1 | CSS | Plain answers list, hover only |
| ROUND15-V1 | — | Reverted (no visual effect) |
| ROUND16-V1 | CSS | Session row hover 10px |
| ROUND17-V1 | 4 CSS | Full model names, cards 10px, badges 8px |
| ROUND18-V1 | 4 CSS | Global list rows 8px |
| ROUND19-V1 | 4 CSS | Trigger values wrap fully (no ellipsis) |
| ROUND20–21 | 4 CSS | Superseded by ROUND22 |
| ROUND22-V1 | 4 CSS | Flat rows, prominent select-style triggers |
| ROUND23-V1 | 4 CSS | Trigger specificity fix, hover radius |
| ROUND24-V1 | 4 CSS | Session chips: default background + hover |
| ROUND25-V1 | 4 CSS | Timeline rows as chips, collapsible 10px |
| ROUND26–27 | 4 CSS | User bubble interactive tint |
| ROUND28–29 | 4 CSS | Assistant bubble + icons outside card |
| ROUND30–36 | 4 CSS | Reasoning revert, sidebar rows 10px, host-var fixes, sidebar + task-header inset shade, rounded progress bar and usage pill |
| ROUND37-V1 | 4 CSS + 2 JS | Chip icons (mode ⚙️ / thinking 🧠 / provider emoji) via observer |
| ROUND38-V1 | 4 CSS + 2 JS | Monochrome per-mode list icons, compact 320px mode list |
| ROUND39-V1 | 4 CSS + 2 JS | Mode list hard cap 300px, monochrome provider icons on model rows |
| ROUND40-V1 | 4 CSS | Modern tab bar: inset shade, rounded tabs, stronger active |
| ROUND41-V1 | 4 CSS | Tag-agnostic settings trigger rounding (`:has`) — later superseded |
| ROUND42-V1 | 4 CSS | Settings Radix select triggers: 8px + bg + blue expand border (true model picker fix) |
| ROUND43-V1 | — | Reverted (2026-09-07 hang: sidebar restyle + ACTIVE-MARKER-V3 loop) |
| ROUND44-V1 | — | Reverted (2026-09-07 hang: sidebar restyle) |
| ROUND45-V1 | — | Reverted (2026-09-07 hang: `kilo-live` relied on V3 JS loop) |
| ROUND46-V1 | 4 CSS | CSS-only active pill: `:has(.am-local-item-active)` tint + `::after` "active" pill on non-idle `[data-activity]` project — zero JS |
| ROUND47-V1 | 4 CSS | CSS-only chat icons: `::before` emoji on mode/thinking/model rows + hint-selector buttons (`nth-child` positional) — React-safe, no DOM moves |
| ROUND48-V1 | 4 CSS | Agent-list left-align (column kept) + global radius pass: popover/select `14px`, mode/thinking/model/list rows `8px` base — fixes native `2px`/`0` overrides |
| ROUND49-V1 | 4 CSS | Compact agent rows: icon+name one line (`row+wrap`), desc second line indented with ellipsis — supersedes ROUND48 stacking |
| ROUND50-V1 | 4 CSS | Global rows `8px` → `10px` (`radius-lg`): mode/thinking/model/select/list rows — restores earlier feel, popover stays `14px` |
| ROUND51-V1 | 4 CSS | Hint-icon wrapper fix (parent-`nth-child`, all-gear bug), settings triggers + hint buttons `10px`, hover radius keep, desc full-wrap on hover |
| ROUND52-V1 | 4 CSS | Literal radius (theme `--radius-lg=4px` bypass): rows/triggers fixed `10px`, popover `14px` — supersedes token fallbacks |
| ROUND53-V1 | 4 CSS | Kilo Settings dropdowns (`popover-trigger` in `settings-row-input`) fixed `10px` — select-trigger rule never matched settings |
| ROUND54-V1 | 4 CSS | Agent Manager rows/tabs literal `10px` (token override `4px` fix) — radius-only, hang-safe, ROUND43-45 stay reverted |
| ROUND55-V1 | 4 CSS | Chat hint hover match: wrapper + hover/expanded/focus states literal `10px` with `background-clip` — halo shape same as resting |
| TOKENS-V1 | 4 CSS | Token-compliance pass (kilo-design `tokens.json` v0.2.0) |

</details>

## Notes and limits

- This is a **local hot-patch of build output**, not a source-level fix. An
  upstream contribution would target `packages/ui` and `packages/kilo-ui` in
  the main repository — see [`ISSUE-DRAFT.md`](ISSUE-DRAFT.md) for the draft.
- New Kilo releases rename minified JS functions (7.5.9: `wUr`/`Xna`,
  7.5.14: `$Ur`/`Qra` — both covered). If the script prints
  `WARN: decorate signature changed`, the new `decorate` function must be
  located and added to `JS_DECORATE` in `reapply.py`.
- Tested with Kilo Code 7.5.9 → 7.5.15 on Linux (dark theme).
- **2026-09-07 hang rule:** all `MutationObserver` JS is disabled
  (`ENABLE_JS_PATCH=False` in `reapply.py`) — the V3 active-marker loop
  froze the Agent Manager webview. Icons and the active pill are CSS-only
  (ROUND46/47). Any future observer must follow `SAFE_OBSERVE_TPL`
  (rAF throttle + `disconnect()` while mutating + `attributeFilter`).

## License

[MIT](LICENSE) — © [Mayanktaker Computers & Web Development](https://mayanktaker.com)
