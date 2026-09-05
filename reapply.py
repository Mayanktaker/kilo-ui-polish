# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Re-apply Kilo Code chat UI patches after every extension update.
# Usage: python3 reapply.py   (idempotent, safe to run twice)
import glob
import os
import shutil

CSS_FILES = ["agent-manager.css", "webview.css", "marketplace.css", "documents.css"]
JS_DECORATE = {
    # 7.5.9 names first, then 7.5.14 — script tries each in order
    "webview.js": [
        'function wUr(e,t){let n=Array.from(e.querySelectorAll("pre"));for(let r of n)yUr(r,t);vUr(e)}',
        'function $Ur(e,t){let n=Array.from(e.querySelectorAll("pre"));for(let r of n)PUr(r,t);NUr(e)}',
    ],
    "agent-manager.js": [
        'function Xna(e,t){let n=Array.from(e.querySelectorAll("pre"));for(let r of n)Yna(r,t);Jna(e)}',
        'function Qra(e,t){let n=Array.from(e.querySelectorAll("pre"));for(let r of n)Rra(r,t);Fra(e)}',
    ],
}
JS_WRAP_TPL = "try{{for(let tbl of Array.from(e.querySelectorAll(\"table\"))){{if(tbl.closest(\"[data-component=markdown-table-wrapper]\"))continue;let w=document.createElement(\"div\");w.setAttribute(\"data-component\",\"markdown-table-wrapper\");tbl.parentNode&&tbl.parentNode.replaceChild(w,tbl);w.appendChild(tbl)}}}}catch(o){{}}/*{mark}*/"

BLOCKS = [
    ("KILO-TABLE-FIX-V1", """[data-component=markdown] table{width:100%;display:block;overflow:auto;margin:16px 0;font-size:var(--font-size-base);border:1px solid var(--border-weak-base);border-radius:10px;border-collapse:separate;border-spacing:0;padding:0;background:var(--surface-base)}
[data-component=markdown] thead,[data-component=markdown] tbody{display:table;width:100%;border-collapse:separate;border-spacing:0;margin:0}
[data-component=markdown] tr{display:table-row;width:100%}
[data-component=markdown] th,[data-component=markdown] td{display:table-cell;padding:10px 12px;text-align:start;vertical-align:top;border:0;border-bottom:1px solid var(--border-weaker-base);border-right:1px solid var(--border-weaker-base);min-width:120px;white-space:normal;overflow-wrap:break-word}
[data-component=markdown] th:last-child,[data-component=markdown] td:last-child{border-right:0}
[data-component=markdown] thead tr:last-child th{border-bottom:1px solid var(--border-weak-base)}
[data-component=markdown] tbody tr:last-child td{border-bottom:0}
[data-component=markdown] th{background:var(--surface-raised-base,var(--surface-base));color:var(--text-strong);font-weight:var(--font-weight-medium);white-space:nowrap}
[data-component=markdown] tbody tr:hover td{background:color-mix(in srgb,var(--surface-base) 96%,var(--text-strong) 4%)}
[data-component=markdown] thead tr:first-child th:first-child{border-top-left-radius:10px}
[data-component=markdown] thead tr:first-child th:last-child{border-top-right-radius:10px}
[data-component=markdown] tbody tr:last-child td:first-child{border-bottom-left-radius:10px}
[data-component=markdown] tbody tr:last-child td:last-child{border-bottom-right-radius:10px}
[data-component=markdown-table-wrapper]{margin:16px 0;border:1px solid var(--border-weak-base);border-radius:10px;overflow:auto;max-width:100%;background:var(--surface-base)}
[data-component=markdown-table-wrapper] table{border:0;border-radius:0;margin:0;display:table;overflow:visible;width:100%}
[data-component=markdown-table-wrapper] thead,[data-component=markdown-table-wrapper] tbody{display:table-row-group;width:auto}
[data-component=markdown-table-wrapper] tr{display:table-row}"""),
    ("KILO-ROUND2-V1", """[data-slot=user-message-text]{border-radius:10px}
[data-component=markdown] .shiki{border-radius:10px}
[data-component=markdown] img{border-radius:10px}
[data-slot=question-option]{border-radius:10px}
[data-component=prompt-input-form],.prompt-input-container{border-radius:10px}
[data-component=chat-input] [data-slot=input-wrapper],[data-component=textarea][data-variant=chat] [data-slot=input-wrapper]{border-radius:10px}"""),
    ("KILO-ROUND3-V1", """[data-component=question-dock]{background-color:var(--surface-raised-base,var(--surface-base));border:1px solid var(--border-weak-base);border-radius:12px;box-shadow:var(--shadow-md,0 4px 12px rgba(0,0,0,.18));padding:4px 4px 8px}
[data-slot=question-option]{transition:border-color .15s ease,background-color .15s ease,box-shadow .15s ease}
[data-slot=question-option]:hover{border-color:var(--border-focus,var(--text-interactive-base));background-color:var(--surface-raised-stronger-non-alpha);box-shadow:var(--shadow-sm,0 1px 4px rgba(0,0,0,.15))}
[data-slot=question-option][data-selected=true],[data-slot=question-option][aria-checked=true]{border-color:var(--text-interactive-base);box-shadow:0 0 0 1px var(--text-interactive-base)}"""),
    ("KILO-ROUND4-V1", """[data-slot=question-options] [data-slot=question-option]:nth-child(even){background-color:var(--surface-base)}
[data-slot=question-options] [data-slot=question-option]:hover{background-color:var(--surface-raised-stronger-non-alpha);border-color:var(--border-focus,var(--text-interactive-base))}
[data-component=task-tool-card]{border-radius:10px;transition:border-color .15s ease}
[data-component=task-tool-card]:hover{border-color:var(--border-focus,var(--text-interactive-base))}
[data-component=markdown] tbody tr:nth-child(even) td{background:color-mix(in srgb,var(--surface-base) 97%,var(--text-strong) 3%)}"""),
    ("KILO-ROUND5-V1", """[data-slot=question-options]{gap:0;border:1px solid var(--border-weak-base);border-radius:10px;overflow:hidden;background:var(--surface-base);padding:0}
[data-slot=question-options] [data-slot=question-option]{border:0;border-radius:0;box-shadow:none;border-bottom:1px solid var(--border-weaker-base);background-color:transparent}
[data-slot=question-options] [data-slot=question-option]:last-child{border-bottom:0}
[data-slot=question-options] [data-slot=question-option]:nth-child(even){background-color:color-mix(in srgb,var(--surface-base) 95%,var(--text-strong) 5%)}
[data-slot=question-options] [data-slot=question-option]:hover{background-color:var(--surface-raised-stronger-non-alpha);border-color:var(--border-weaker-base)}
[data-component=button]{border-radius:10px}
[data-component=tag],[data-component=badge]{border-radius:10px}"""),
    ("KILO-ROUND6-V1", """[data-slot=question-options]{border:0;border-radius:0;background:transparent;overflow:visible}"""),
    ("KILO-ROUND7-V1", """[data-component=model-selector-popover]{border-radius:12px;overflow:hidden;box-shadow:0 8px 28px rgba(0,0,0,.35)}
.model-selector-search{border-radius:10px}
.model-selector-list{padding:6px}
.model-selector-item{border-radius:8px}
.model-selector-item-select-btn{border-radius:8px}
.model-selector-star{border-radius:6px}"""),
    ("KILO-ROUND8-V1", """[data-component=popover-content]{border-radius:12px}
[data-component=model-selector-popover]{border-radius:14px}
[data-component=model-selector-popover] [data-component=list] [data-slot=list-scroll]{padding:6px}
[data-component=model-selector-popover] [data-component=list] [data-slot=list-item]{border-radius:8px}
[data-component=model-selector-popover] [data-component=list] [data-slot=list-item][data-active=true]{border-radius:8px}
[data-component=model-selector-popover] [data-component=list] [data-slot=list-item][data-selected=true]{border-radius:8px}"""),
    ("KILO-ROUND9-V1", """.model-selector-item.active{outline:none;border:0;box-shadow:none}"""),
    ("KILO-ROUND10-V1", """[data-component=markdown] thead th{background:color-mix(in srgb,var(--surface-base) 88%,var(--text-strong) 12%);font-weight:600;letter-spacing:.02em}
[data-component=markdown] thead tr:last-child th{border-bottom:2px solid var(--border-strong-base,var(--border-weak-base))}"""),
    ("KILO-ROUND11-V1", """[data-component=model-selector-popover]{background-color:color-mix(in srgb,var(--background-stronger) 82%,#000 18%);border:1px solid rgba(140,140,140,.28);box-shadow:0 12px 32px rgba(0,0,0,.5)}
.model-selector-search{background:color-mix(in srgb,#000 30%,var(--vscode-input-background));border:1px solid rgba(140,140,140,.22)}
.model-selector-group-label{text-transform:uppercase;letter-spacing:.07em}
.model-selector-item.active{background:linear-gradient(90deg,#2f6fed,#3b82f6);color:#fff}
.model-selector-item.active .model-selector-item-name,.model-selector-item.active .model-selector-item-name-main,.model-selector-item.active .model-selector-item-provider-tag{color:#fff;opacity:1}
[data-component=model-selector-popover] [data-component=list] [data-slot=list-item][data-active=true]{background:linear-gradient(90deg,#2f6fed,#3b82f6);color:#fff}"""),
    ("KILO-ROUND12-V1", """[data-component=question-dock]{padding:0;overflow:hidden}
[data-slot=question-dock-header]{background:color-mix(in srgb,var(--surface-base) 78%,#000 22%);border-bottom:1px solid var(--border-weak-base);padding:10px 12px 8px}
[data-slot=question-options]{background:var(--surface-base);border:1px solid var(--border-weaker-base);border-radius:10px;margin:8px;overflow:hidden}"""),
    # KILO-ROUND13-V1 REVERTED (bottom bar: no visible effect, risk at submit) — do not re-add
    ("KILO-ROUND14-V1", """[data-slot=question-options] [data-slot=question-option]{border-bottom:0}
[data-slot=question-options] [data-slot=question-option]:nth-child(even){background-color:transparent}"""),
    # KILO-ROUND15-V1 REVERTED (bottom bar v2: no visible effect) — do not re-add
    ("KILO-ROUND16-V1", """.session-actions-row>[data-component=tooltip-trigger]>[data-component=button]{border-radius:10px}"""),
    ("KILO-ROUND17-V1", """[data-component=model-selector-popover]{width:336px}
.model-selector-item-name,.model-selector-item-name-main{white-space:normal;overflow:visible;text-overflow:clip}
[data-component=card]{border-radius:10px}
[data-slot=settings-nav-item]{border-radius:8px}
[data-component=pricing-badge],.am-branch-badge{border-radius:8px}"""),
    ("KILO-ROUND18-V1", """[data-slot=list-item]{border-radius:8px}
[data-slot=list-item][data-active=true],[data-slot=list-item][data-selected=true]{border-radius:8px}"""),
    ("KILO-ROUND19-V1", """.model-selector-trigger-label{white-space:normal;overflow:visible;text-overflow:clip;text-align:end}"""),
    ("KILO-ROUND20-V1", """.model-selector-item{background-color:color-mix(in srgb,var(--surface-raised-base) 50%,transparent);border:1px solid rgba(140,140,140,.12)}
.model-selector-item:hover,.model-selector-item.selected{background-color:var(--surface-interactive-hover,var(--vscode-list-hoverBackground));border-color:rgba(140,140,140,.25)}"""),
    ("KILO-ROUND21-V1", """button:has(>.model-selector-trigger-label){background-color:color-mix(in srgb,var(--surface-raised-base) 55%,transparent);border:1px solid rgba(140,140,140,.14);border-radius:8px;padding:4px 8px}
button:has(>.model-selector-trigger-label):hover{border-color:rgba(140,140,140,.3)}"""),
    ("KILO-ROUND22-V1", """.model-selector-item{background-color:transparent;border:0;border-radius:0}
.model-selector-item:hover,.model-selector-item.selected{background:var(--surface-interactive-hover,var(--vscode-list-hoverBackground));border-color:transparent}
button:has(.model-selector-trigger-label),[role=button]:has(.model-selector-trigger-label){background-color:var(--vscode-input-background);border:1px solid var(--vscode-input-border,rgba(140,140,140,.35));border-radius:8px;padding:4px 8px}
button:has(.model-selector-trigger-label):hover,[role=button]:has(.model-selector-trigger-label):hover{border-color:var(--vscode-focusBorder,var(--text-interactive-base))}"""),
    ("KILO-ROUND23-V1", """button[data-component=button]:has(.model-selector-trigger-label){background-color:var(--vscode-input-background);border:1px solid var(--vscode-input-border,rgba(140,140,140,.35));border-radius:8px;padding:4px 8px}
button[data-component=button]:has(.model-selector-trigger-label):hover{border-color:var(--vscode-focusBorder,var(--text-interactive-base))}
.model-selector-item:hover,.model-selector-item.selected{border-radius:8px}"""),
    ("KILO-ROUND24-V1", """.session-actions-row>[data-component=tooltip-trigger]>[data-component=button]{border-radius:10px;background-color:color-mix(in srgb,var(--surface-raised-base) 45%,transparent);border:1px solid transparent}
.session-actions-row>[data-component=tooltip-trigger]>[data-component=button]:hover:not(:disabled){background-color:color-mix(in srgb,var(--surface-interactive-hover,var(--vscode-list-hoverBackground)) 70%,var(--text-strong) 8%);border-color:rgba(140,140,140,.3)}"""),
    ("KILO-ROUND25-V1", """[data-component=tool-trigger][data-clickable=true]{background-color:color-mix(in srgb,var(--surface-raised-base) 45%,transparent);border:1px solid transparent;border-radius:10px;padding:4px 8px}
[data-component=collapsible]{border-radius:10px}"""),
    ("KILO-ROUND26-V1", """[data-slot=user-message-text]{background-color:color-mix(in srgb,var(--text-interactive-base) 14%,transparent);border-color:color-mix(in srgb,var(--text-interactive-base) 35%,transparent)}"""),
    ("KILO-ROUND27-V1", """[data-component=user-message] [data-slot=user-message-text]{background-color:rgba(3,76,255,.16)!important;border:1px solid rgba(3,76,255,.45)!important}"""),
    ("KILO-ROUND28-V1", """[data-component=user-message] [data-slot=user-message-text]{border:1px solid rgba(3,76,255,.28)!important}
[data-component=text-part]{background-color:rgba(255,255,255,.045);border:1px solid rgba(140,140,140,.14);border-radius:10px;padding:8px 12px;margin-top:8px}"""),
    ("KILO-ROUND29-V1", """[data-component=text-part]{background:transparent;border:0;padding:0}
[data-slot=text-part-body]{background-color:rgba(255,255,255,.045);border:1px solid rgba(140,140,140,.14);border-radius:10px;padding:8px 12px;margin-top:8px}
[data-slot=assistant-copy-wrapper]{margin-top:4px;padding:0 2px}
[data-component=reasoning-part]{background-color:rgba(255,255,255,.045);border:1px solid rgba(140,140,140,.14);border-radius:10px;padding:8px 12px;margin-top:8px}
[data-component=collapsible]{background-color:rgba(255,255,255,.045);border:1px solid rgba(140,140,140,.14);border-radius:10px}
[data-component=tool-trigger][data-clickable=true]{background:transparent;border:0;padding:4px 8px}"""),
    ("KILO-ROUND30-V1", """[data-component=reasoning-part]{background:transparent;border:0;padding:0;margin-top:0}
[data-component=collapsible]{background:transparent;border:0}
[data-component=tool-trigger][data-clickable=true]{background-color:color-mix(in srgb,var(--surface-raised-base) 45%,transparent);border:1px solid transparent;border-radius:10px;padding:4px 8px}
.am-local-item,.am-worktree-item,.am-project-item .am-sidebar-header,.am-project-item>.am-sidebar-header{border-radius:8px}
.am-project-item>.am-sidebar-header{padding:4px 6px}
.am-project-item:has(.am-local-item-active)>.am-sidebar-header{background-color:rgba(3,76,255,.16);border:1px solid rgba(3,76,255,.28)}
.am-worktree-item-active,.am-local-item-active{background-color:rgba(3,76,255,.16)!important;border:1px solid rgba(3,76,255,.28)!important}"""),
    # KILO-TOKENS-V1: token-compliant pass (kilo-design tokens.json v0.2.0).
    # Off-scale 12px/6px -> scale (xl/sm); raw rgba colors -> vars + color-mix.
    # This block supersedes earlier hard-coded colors for PR-readiness.
    ("KILO-TOKENS-V1", """[data-component=question-dock]{border-radius:var(--radius-xl,14px)}
[data-component=model-selector-popover]{border-radius:var(--radius-xl,14px)}
.model-selector-star{border-radius:var(--radius-sm,4px)}
.model-selector-item.active{background:linear-gradient(90deg,var(--text-interactive-base),color-mix(in srgb,var(--text-interactive-base) 82%,#fff 18%));color:var(--text-on-interactive-base,var(--text-strong))}
.model-selector-item.active .model-selector-item-name,.model-selector-item.active .model-selector-item-name-main,.model-selector-item.active .model-selector-item-name-provider{color:var(--text-on-interactive-base,var(--text-strong));opacity:1}
[data-component=model-selector-popover] [data-component=list] [data-slot=list-item][data-active=true]{background:linear-gradient(90deg,var(--text-interactive-base),color-mix(in srgb,var(--text-interactive-base) 82%,#fff 18%));color:var(--text-on-interactive-base,var(--text-strong))}
[data-component=user-message] [data-slot=user-message-text]{background-color:color-mix(in srgb,var(--text-interactive-base) 16%,transparent)!important;border:1px solid color-mix(in srgb,var(--text-interactive-base) 28%,transparent)!important}
[data-slot=text-part-body]{background-color:var(--surface-raised-base);border:1px solid var(--border-weak-base)}
[data-slot=assistant-copy-wrapper]{margin-top:var(--spacing-1,4px);padding:0 2px}
[data-component=reasoning-part]{background:transparent;border:0;padding:0;margin-top:0}
[data-component=collapsible]{background:transparent;border:0}
[data-component=tool-trigger][data-clickable=true]{background-color:color-mix(in srgb,var(--surface-raised-base) 45%,transparent);border:1px solid transparent;border-radius:var(--radius-lg,10px);padding:var(--spacing-1,4px) var(--spacing-2,8px)}
.am-local-item,.am-worktree-item,.am-project-item>.am-sidebar-header{border-radius:var(--radius-md,8px)}
.am-project-item>.am-sidebar-header{padding:var(--spacing-1,4px) var(--spacing-1_5,6px)}
.am-project-item:has(.am-local-item-active)>.am-sidebar-header{background-color:color-mix(in srgb,var(--text-interactive-base) 16%,transparent);border:1px solid color-mix(in srgb,var(--text-interactive-base) 28%,transparent)}
.am-worktree-item-active,.am-local-item-active{background-color:color-mix(in srgb,var(--text-interactive-base) 16%,transparent)!important;border:1px solid color-mix(in srgb,var(--text-interactive-base) 28%,transparent)!important}
.session-actions-row>[data-component=tooltip-trigger]>[data-component=button]{border-radius:var(--radius-lg,10px);background-color:color-mix(in srgb,var(--surface-raised-base) 45%,transparent);border:1px solid transparent}
.session-actions-row>[data-component=tooltip-trigger]>[data-component=button]:hover:not(:disabled){background-color:color-mix(in srgb,var(--surface-interactive-hover,var(--vscode-list-hoverBackground)) 70%,var(--text-strong) 8%);border-color:var(--border-strong-base,var(--border-weak-base))}
[data-slot=question-options] [data-slot=question-option]{border-bottom:0}
[data-slot=question-options] [data-slot=question-option]:nth-child(even){background-color:transparent}
.model-selector-item:hover,.model-selector-item.selected{border-radius:var(--radius-md,8px)}
button[data-component=button]:has(.model-selector-trigger-label){background-color:var(--vscode-input-background);border:1px solid var(--vscode-input-border,rgba(127,127,127,.35));border-radius:var(--radius-md,8px);padding:var(--spacing-1,4px) var(--spacing-2,8px)}
button[data-component=button]:has(.model-selector-trigger-label):hover{border-color:var(--vscode-focusBorder,var(--text-interactive-base))}
.model-selector-trigger-label{white-space:normal;overflow:visible;text-overflow:clip;text-align:end}
.model-selector-item{background-color:transparent;border:0;border-radius:0}
[data-component=markdown] thead th{background:color-mix(in srgb,var(--surface-base) 88%,var(--text-strong) 12%);font-weight:600;letter-spacing:.02em}
[data-component=markdown] thead tr:last-child th{border-bottom:2px solid var(--border-strong-base,var(--border-weak-base))}"""),
    ("KILO-ROUND31-V1", """[data-slot=text-part-body]{background:transparent;border:0;padding:0;margin-top:0}
[data-component=todos]{border-radius:var(--radius-lg,10px)}"""),
    ("KILO-ROUND32-V1", """.session-actions-row>[data-component=tooltip-trigger]>[data-component=button]{border-radius:10px}"""),
]


def ver_key(p):
    import re
    m = re.search(r"kilo-code-([\d.]+)", p)
    return tuple(int(x) for x in m.group(1).split(".")) if m else ()


def find_dist():
    hits = sorted(glob.glob(os.path.expanduser("~/.vscode/extensions/kilocode.kilo-code-*/dist")), key=ver_key)
    if not hits:
        raise SystemExit("Kilo extension dist not found")
    print("dist:", hits[-1])
    return hits[-1]


def main():
    dist = find_dist()
    for name in CSS_FILES:
        p = os.path.join(dist, name)
        bak = p + ".before-ui-patch.bak"
        if not os.path.exists(bak):
            shutil.copy2(p, bak)
            print("backup", os.path.basename(bak))
        cur = open(p, errors="ignore").read()
        changed = False
        for mark, css in BLOCKS:
            if mark not in cur:
                cur += "\n/* %s */\n%s\n" % (mark, css)
                changed = True
                print(name, mark, "applied")
        if changed:
            open(p, "w", errors="ignore").write(cur)
        else:
            print(name, "already fully patched")
    for js_name, olds in JS_DECORATE.items():
        p = os.path.join(dist, js_name)
        if not os.path.exists(p):
            print(js_name, "missing, skip")
            continue
        bak = p + ".before-ui-patch.bak"
        if not os.path.exists(bak):
            shutil.copy2(p, bak)
            print("backup", os.path.basename(bak))
        cur = open(p, errors="ignore").read()
        if "markdown-table-wrapper" in cur:
            print(js_name, "wrapper already present")
            continue
        old = next((o for o in olds if o in cur), None)
        if not old:
            print(js_name, "WARN: decorate signature changed, manual check needed")
            continue
        new_fn = old[:-1] + ";" + JS_WRAP_TPL.format(mark="KILO-JS-WRAP-V1") + "}"
        open(p, "w", errors="ignore").write(cur.replace(old, new_fn, 1))
        print(js_name, "wrapper injected")
    print("DONE. VS Code me Developer: Reload Window karo.")


if __name__ == "__main__":
    main()
