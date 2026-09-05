# UI Polish: token-aligned rounded tables, unified radii, chat bubbles

## Summary

While using the Kilo Code VS Code extension daily, I polished several chat UI
areas and then aligned everything with the
[kilo-design](https://github.com/Kilo-Org/kilo-design) token system
(`tokens.json` v0.2.0) before proposing this upstream.

Highlights:

- **Markdown tables**: outer `1px` border, rounded corners on all four sides
  (`radius.lg = 10px`), header tint, zebra rows, horizontal scroll preserved.
  Implemented with a `markdown-table-wrapper` div injected in `decorate()` so
  the scroll container owns the radius.
- **Unified radii**: user bubbles, code blocks, images, question options,
  prompt input, buttons, tags, list rows — all mapped to the token scale
  (`sm 4 / md 8 / lg 10 / xl 14`).
- **Model selector**: wider popover (`radius.xl`), full model names (wrap
  instead of ellipsis), search input rounding, OpenChamber-style selection.
- **Chat bubbles**: user messages get an interactive-color tint
  (`color-mix(var(--text-interactive-base) 16%)`); assistant replies get a
  neutral `surface-raised` bubble; copy/feedback icons sit outside the card.
- **Agent Manager sidebar**: 8px rows; the row of the project containing the
  active session gets the same interactive tint (`:has()` selector).

## Token compliance

Audited against `tokens.json` v0.2.0:

| Used | Token | Status |
|---|---|---|
| 10px | `radius.lg` | ✅ |
| 8px | `radius.md` | ✅ |
| 14px | `radius.xl` | ✅ |
| 4px | `radius.sm` | ✅ |
| Interactive blue | `color-mix(var(--text-interactive-base))` via host map | ✅ |
| Surfaces/borders | `var(--surface-raised-base)`, `var(--border-weak-base)` | ✅ |

All hard-coded rgba/hex values were replaced with theme variables +
`color-mix` so light/high-contrast themes inherit correctly.

## Evidence

Before/after screenshots available on request — happy to attach them here.

## Questions for maintainers

1. Is `radius.lg (10px)` the intended token for chat cards/bubbles, or should
   these use `radius.md (8px)`?
2. Is a wrapper div around `<table>` acceptable for the scroll+radius combo,
   or would you prefer pure-CSS (`display: block` table has alignment
   tradeoffs we hit during testing)?
3. Should the user-message tint use `--text-interactive-base` or a dedicated
   semantic token?

Happy to split this into focused PRs (tables / radii / model selector /
bubbles) against `packages/ui` and `packages/kilo-ui` once the direction is
confirmed. Local hot-patch prototype: https://github.com/Mayanktaker/kilo-ui-polish
