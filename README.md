# Hanzo Marketing / GTM

**INTERNAL ONLY. NEVER PUBLIC.** This repo is the go-to-market war-chest:
strategy, promo mechanics, channel plans, ad concepts, and the modernized
growth handbook. Nothing here is published — not the plan, not the numbers,
not the ad copy — without **explicit written approval from the CTO.**

Private GitHub repo: `hanzoai/marketing` (created `--private`). Do not fork
to a public remote. Do not paste contents into public issues, Discord, or
tweets. Ad copy here is *draft*; only measured claims ship (see the honesty
rule below).

## The honesty rule

Every claim we publish must be true and, ideally, measured. This repo tags
each referenced system with its real status:

- `[LIVE]` — built and running in production.
- `[LANDING]` — being built now; partially wired; do not depend on for a hard date.
- `[ROADMAP]` — specced, not started.

Numbers we are allowed to use in public copy (measured, from the papers):
`0.245 MB/tenant`, `1B users / 20 nodes`, `28+ social channels`. Everything
else (CAC, CPM, K-factor targets) is an **estimate-to-validate**, labelled as
such, and never printed as if it were data.

## Repo map

| Path | What |
|---|---|
| `GTM.md` | **The spine.** Phased plan (0 waitlist → 1 paid → 2 nodes → 3 OSS flywheel), metrics, kill-criteria, dependency flags. |
| `discounts.md` | Promo playbook: 90%-first-month-first-1000, referral credits, node credits, annual, Techstars, edu/OSS. |
| `stack.md` | **The GTM command stack** — every marketing plane mapped to a Hanzo repo with honest status. |
| `GUIDE.md` | The Guide™ 2.0 — the classic startup-marketing handbook, modernized for the AI age and mapped onto the Hanzo-native stack. |
| `CHECKLIST.md` | Ordered, human-readable business/GTM checklist (setup → infra → research → channels → automation → daily loop). |
| `checklist.yaml` | The same checklist, machine-readable (owner, status, tool, phase) — the source we drive from ops. |
| `analysis/waitlist-phase.md` | What drives the waitlist/email phase — hypotheses + the exact events to instrument in Insights. |
| `analysis/channels.md` | Channel-by-channel plan (X, HN, PH, YouTube, retargeting) with CPM/CAC ranges flagged ESTIMATE. |
| `ads/` | Draft ad copy + creative concepts (text only), by campaign. |

## Who owns this

CTO owns the strategy. AI Engineers (per The Guide™) own setup, management,
and optimization of the campaigns. Nothing ships without the honesty rule
satisfied and CTO sign-off.
