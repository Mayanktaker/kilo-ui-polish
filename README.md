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
- Tested with Kilo Code 7.5.9 → 7.5.14 on Linux (dark theme).

## License

[MIT](LICENSE) — © [Mayanktaker Computers & Web Development](https://mayanktaker.com)
