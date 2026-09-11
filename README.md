# Travel Handbook Skill

A portable agent skill for converting travel-plan Markdown into a polished, static, responsive six-tab travel handbook HTML.

## Agent entrypoints

| Environment | Read first |
| --- | --- |
| Codex | `SKILL.md` |
| Claude Code | `CLAUDE.md` |
| WorkBuddy and other coding agents | `AGENTS.md` |

All entrypoints lead to one canonical ruleset in `SKILL.md` and `references/`, so the requirements do not drift between agents.

## Repository contents

- `SKILL.md` — canonical workflow and requirements
- `AGENTS.md` — portable instructions for agents supporting `AGENTS.md`
- `CLAUDE.md` — Claude Code entrypoint
- `references/` — detailed implementation and validation requirements
- `assets/` — six-tab HTML starter template
- `scripts/audit_handbook.py` — structural audit

## Use in another agent

Clone or download this repository, then point the agent at the repository root and ask it to read its relevant entrypoint before creating a handbook. The agent must read every required reference in the stated order.

The skill asks for tool capabilities, not a specific vendor: any compatible agent can substitute its own image-generation, browser-validation, and local file tools. It must preserve the required six tabs, local-only checklist/photo behavior, and validation process.

## Validation

From the repository root:

```powershell
python scripts/audit_handbook.py <absolute-path-to-output.html>
```

This checks structural markers only. Verify actual venue identity, phone numbers, official ticket links, route order, and responsive behavior separately before delivery.

## GitHub upload

Upload the entire folder, including hidden files if you add any later. Do not upload generated handbooks, customer itineraries, API keys, browser profiles, or personal order/ID screenshots.
