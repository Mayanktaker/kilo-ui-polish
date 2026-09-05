# © Mayanktaker Computers & Web Development | https://mayanktaker.com

# kilo-ui-polish — Kilo Code Chat UI Polish (hot-patch)

A set of CSS/JS hot-patches that polish the Kilo Code VS Code extension chat UI:
proper markdown tables with rounded corners, unified 10px radii, a two-tone
question card, an OpenChamber-style model picker, and more.

> Every Kilo Code update overwrites `~/.vscode/extensions/kilocode.kilo-code-*/dist/`.
> After an update, just re-run the script below.

## Quick start

```bash
python3 reapply.py
```

Then in VS Code: `Developer: Reload Window`.

The script:

- auto-detects the newest installed Kilo version (semver sort),
- backs each file up once (`*.before-ui-patch.bak`),
- is idempotent — re-running only applies missing blocks, wrapped tables included.

## What is patched

| Round | Files | Change |
|---|---|---|
| TABLE-FIX-V1 | 3 CSS + `webview.js`, `agent-manager.js` | Markdown tables: outer `1px` border, `10px` radius on all corners, header tint, last-row border cleanup, horizontal scroll kept; JS `decorate()` wraps each table in a `markdown-table-wrapper` div |
| ROUND2-V1 | CSS | 10px unification: user bubble, code blocks (shiki), markdown images, question options, prompt input, chat input wrapper |
| ROUND3-V1 | CSS | Question dock subtle card: raised background + border + `12px` radius + shadow; option hover + selected ring |
| ROUND4-V1 | CSS | Options alternate shade + hover; task tool cards 10px + hover; table zebra rows |
| ROUND5-V1 | CSS | Options as joined table-style rows (dividers + alt tint); buttons 10px; tags/badges 10px |
| ROUND6-V1 | CSS | Removed the outer options box border (dividers kept) |
| ROUND7-V1 | CSS | Model selector: popover `12px` + shadow, search 10px, rows 8px + padding, select button 8px, star 6px |
| ROUND8-V1 | CSS | Popover shell `14px` (+ generic popovers `12px`); inner list rows 8px incl. active/selected |
| ROUND9-V1 | CSS | Removed the outline/border on the active model row |
| ROUND10-V1 | CSS | Premium table header: deeper tint + semibold + `2px` bottom rule |
| ROUND11-V1 | CSS | OpenChamber vibe: dark popover + shadow, dark search, caps group labels, blue gradient selection |
| ROUND12-V1 | CSS | Two-tone question card: dark header band + separate answers box |
| ROUND13-V1 | — | ~~Bottom bar chips/icons/send~~ → **REVERTED** (no visible effect, submit-time risk) |
| ROUND14-V1 | CSS | Plain answers: dividers + alt tint removed, hover only |
| ROUND15-V1 | — | ~~Bottom bar v2~~ → **REVERTED** (no visible effect) |
| ROUND16-V1 | CSS | Session row (New/Fork/Move) hover 10px |
| ROUND17-V1 | 4 CSS (+documents) | Full model names (wider popover + wrapping), cards 10px, settings rail 8px, mini badges 8px |
| ROUND18-V1 | 4 CSS | Global list rows 8px (incl. settings nav) |
| ROUND19-V1 | 4 CSS | Trigger values wrap fully (ellipsis removed) |
| ROUND20-V1 | 4 CSS | Model rows resting background + border (superseded by ROUND22) |
| ROUND21-V1 | 4 CSS | Settings trigger resting background via `:has` (superseded by ROUND22/23) |
| ROUND22-V1 | 4 CSS | Flat rows again (boxes removed) + prominent select-like triggers |
| ROUND23-V1 | 4 CSS | Trigger specificity fix + hover radius on rows |
| ROUND24-V1 | 4 CSS | Session chips: default background + radius, deeper hover |
| ROUND25-V1 | 4 CSS | Timeline rows (Reasoning/Shell/Write) as chips, collapsible 10px |
| ROUND26-V1 | 4 CSS | User bubble link-blue tint (stands out from assistant in long sessions) |
| ROUND27-V1 | 4 CSS | Stronger solid tint + border on user bubble (bidi rule override) |
| ROUND28-V1 | 4 CSS | Assistant replies get neutral bubble; user border softened |

Covered bundles: `agent-manager.css`, `webview.css`, `marketplace.css`,
`documents.css` (settings/account pages).

## Rollback

Each file is backed up on first run next to the original:

```bash
cp ~/.vscode/extensions/kilocode.kilo-code-*/dist/agent-manager.css.before-ui-patch.bak \
   ~/.vscode/extensions/kilocode.kilo-code-*/dist/agent-manager.css
```

## Notes / limits

- This is a **local hot-patch of build output**, not a source fix. A proper
  upstream PR would target `packages/ui/src/components/markdown.css`,
  `markdown.tsx`, and the `kilo-ui` theme in `Kilo-Org/kilocode`.
- New Kilo versions rename minified JS functions (7.5.9: `wUr`/`Xna`,
  7.5.14: `$Ur`/`Qra` — both covered). If the script prints
  `WARN: decorate signature changed`, the new `decorate` function must be
  located and added to `JS_DECORATE` in `reapply.py`.
- Tested on Kilo Code 7.5.9 → 7.5.14 (Linux, dark theme).

## License

MIT — © Mayanktaker Computers & Web Development (https://mayanktaker.com)
