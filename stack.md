# The GTM Command Stack

Every marketing function runs on a Hanzo-native plane. One tool per job,
composable, SSO through hanzo.id, secrets in KMS, data in Base. No SaaS
sprawl — we dogfood our own platform as the marketing stack, which is itself
a proof point ("we run our GTM on the product we sell").

Status legend: `[LIVE]` built & running · `[LANDING]` being built now ·
`[ROADMAP]` specced, not started.

## The planes

| Plane | Hanzo repo / surface | Replaces (industry) | Status | Notes |
|---|---|---|---|---|
| **Waitlist / Phase-0 engine** | `hanzoai/waitlist` + `base/plugins/waitlist` | Prefinery, viral-loops.com | `[LIVE]` | React widget + framework-free custom element; Base plugin backend (2 collections, `/v1/waitlist/{join,status,export}`); Turnstile-gated; points/referral/share/leaderboard/activity/invite; neighborhood-view benchmarked to 10M entries. |
| **Social command dash** | `hanzoai/social` (social.hanzo.ai) | Buffer, Hootsuite, Sprout | `[LIVE]` | Agentic scheduling — schedule, publish, analyze across **28+ channels**. SSO via hanzo.id. AGPL. → this is the "main dash" for organic social. |
| **Paid social ads** | `hanzoai/social` (ads module) | Meta/TikTok/Reddit ad managers | `[LANDING]` | Extend Social with paid-campaign create/boost/optimize on the same 28-channel connector base. |
| **Ad automation + exchange** | `hanzoai/ads` (**ads.hanzo.ai**) + `adnexustech` (SSP/DSP) | AdEspresso + a native exchange | `[ROADMAP]` | New repo, domain **ads.hanzo.ai**. `hanzoai/ads` = the paid-ads control plane (budgets, audiences, retargeting, LLA, kill-poor-performers loop). `github.com/adnexustech` merges in as the **native ad exchange + SSP + DSP** underneath → full-stack owned demand+supply. Dashboard also embeddable in **console.hanzo.ai**. See "Ads architecture" below. |
| **Marketing automation / funnels / connectors** | `hanzoai/auto` (auto.hanzo.ai) | Zapier, n8n, Make | `[LIVE]` | Native Go workflow engine on Base + `hanzoai/tasks`. Large connector library already includes `facebook-leads`, `facebook-pages`, `google-my-business`, `linkedin`, `heymarket-sms`, `google-sheets/forms/ads`-adjacent. → funnels, drip triggers, lead routing. |
| **Email / SMS / transactional + drip** | `hanzoai/notify` | Mailchimp, Mandrill, Customer.io | `[LIVE]` lib / `[LANDING]` campaign UI | Go notification library, multi-channel (email/SMS/push/chat). DKIM+SPF handled at the sending-domain. Drip/lifecycle sequences orchestrated via `auto`. |
| **Product analytics / measurement plane** | `hanzoai/insights` | GA4, Mixpanel, PostHog, Hotjar | `[LIVE]` product / `[LANDING]` funnel wiring | Event analytics, funnels, feature flags, session recording, A/B tests, cohorts. Cloud already ships an analytics client (`cloud/clients/analytics`). Gap = wiring the waitlist→activation funnel events (see `analysis/waitlist-phase.md`). |
| **Payments / subscriptions / promo codes** | `hanzoai/commerce` | Stripe Billing, Chargebee | `[LIVE]` engine / `[LANDING]` capped-promo | Billing engine: tiers (`pro` etc.), monthly/yearly plans (prices in cents), proration, trials, coupon processors in checkout. Gap = the capped-at-1000 promo-code redemption flow (see `discounts.md`). |
| **Creative production** | `hanzoai/studio` | Canva + AdEspresso creative gen | `[LIVE]` | Visual AI engine — generate image/video ad creative programmatically; feeds the ad + social planes. |
| **Brand kit / messaging** | `hanzoai/brand` | brand-guidelines doc | `[LIVE]` | White-label by domain (hanzo.ai / lux.network / zoo.ngo). Messaging guidelines, logos, visual identity. |
| **CRM + ops + team** | `hanzoai/team` (Huly-based) | HubSpot CRM + Linear + Notion-lite | `[LIVE]` | Project management, CRM, HRM, ATS, Chat, collaborative docs (yjs/CRDT). **This is Huly, not AppFlowy.** Covers leads/pipeline/tasks/docs. Gap = a Notion/AppFlowy-style *graph-card knowledge base* (see "Biz knowledge & data lake"). |
| **Identity / SSO** | `hanzoai/iam` (hanzo.id) | Auth0, WorkOS | `[LIVE]` | Every plane authenticates here; org from JWT `owner`. |
| **Secrets** | `hanzoai/kms` | Vault, Doppler | `[LIVE]` | All channel API keys (Meta, Google, TikTok, X, Twilio) live here — never in env files or the repo. |
| **Biz knowledge & data lake** | `hanzo.space` on `hanzoai/base` | Notion + Obsidian + a warehouse | `[ROADMAP]` | The "slurp all biz/ops data" destination. Base backend (SQLite per replica) with a graph layer (**zapdb** or **dgraph**) for knowledge graph-cards. Explicitly **not Obsidian.** See below. |
| **OSS attribution / authors 25%** | GitLab + per-compute attribution | — | `[ROADMAP]` | Phase-3 economics rail; not a marketing surface yet. |
| **x402 marketplace** | agents/tools marketplace | — | `[ROADMAP]` | Phase-3 sustained motion. |

## Ads architecture (`hanzoai/ads` + adnexustech)

Domain: **ads.hanzo.ai** (the ads plane's own surface); the campaign dashboard
is also **embeddable in console.hanzo.ai** so it sits alongside the rest of the
operator/admin cockpit. One backend, two entry points (standalone + console tab).

Decision: **build `hanzoai/ads` as the ad-ops control plane and merge
`github.com/adnexustech` as the exchange/SSP/DSP engine underneath.** This
gives Hanzo a full-stack, owned native-ads system rather than renting
AdEspresso + third-party exchanges.

```
                 hanzoai/ads (control plane)  [ROADMAP]
   budgets · audiences (retargeting/LLA/prospecting) · creative rotation
   optimize-for-purchase · kill-poor-performers loop · daily report
        │                                   │
        ▼                                   ▼
  external channels                  adnexustech (owned)  [ROADMAP: merge]
  (Meta/Google/TikTok/Reddit         ┌─────────────────────────────┐
   via hanzoai/social + auto)        │  DSP  →  Ad Exchange  →  SSP │
                                     └─────────────────────────────┘
                                        our own demand + supply side
```

- **Control plane (`hanzoai/ads`)** drives the Guide's Facebook/Google
  playbook mechanically: custom audiences, saved audiences, lookalikes
  (1%/5%), geo, engagement→conversion campaign progression, budget
  reallocation, experiment cycling.
- **adnexustech merge** = the native exchange + SSP + DSP. Showcase value:
  Hanzo owns both sides of the auction for its own inventory and can offer
  the stack to portfolio/B2B customers (Phase 3). Positioned as "full-featured
  stacked native ads exchange."
- Creative comes from `hanzoai/studio`; channel delivery for social rides
  `hanzoai/social`; all spend/conversion events land in `hanzoai/insights`.

### `hanzoai/ads` scope — full backend + MCP + connected accounts (required)

`hanzoai/ads` is not just a UI; it must ship three layers so agents (and the AI
engineers from The Guide™) can operate real ad spend:

1. **Full backend** `[ROADMAP]` — the control plane above + adnexustech
   exchange/SSP/DSP, on the Hanzo-native stack (Base storage, IAM SSO, KMS
   secrets, tasks for durable campaign jobs).
2. **Connected-account layer** `[ROADMAP]` — OAuth + token storage (in **KMS**,
   never env) for **Meta / Google / TikTok / Reddit / X** ad accounts and the
   28+ social accounts (shared with `hanzoai/social`). One connection registry,
   used by both organic (social) and paid (ads).
3. **MCP server** `[ROADMAP]` — so Claude/agents drive campaigns over MCP:
   create/pause campaigns, adjust budgets, pull spend/insights, rotate creative,
   run the kill-poor-performers loop — on *connected* accounts. Fold in prior
   art as reference implementations to absorb, not depend on:
   - `github.com/pipeboard-co/meta-ads-mcp` — Meta (Facebook/Instagram) Ads MCP.
   - `github.com/amekala/ads-mcp` — Ads MCP (Amazon/marketplace ads).
   - `github.com/foxgeeek/adskills` — ad-operations skill set / agent skills for
     campaign tasks; mine for the *skill* surface (the discrete actions an agent
     performs), map onto Hanzo agent-skills + the Ads MCP tool surface.
   Target: **one Hanzo Ads MCP** exposing every connected channel through a single
   tool surface, so an agent manages Meta + Google + TikTok + our own exchange the
   same way. This is the "AI engineer runs the ads" mechanic from The Guide™,
   made literal.

Do not adopt the external MCPs as runtime deps (registry/branding/secrets rules).
Study them, then implement the Hanzo Ads MCP against our connected-account layer +
KMS. One MCP, one connection registry, one control plane.

Sequencing: this is **Phase 1+ infrastructure**. Phase 0 needs none of it —
Phase 0 is organic (waitlist + social). Do not block the waitlist launch on ads.

## Biz knowledge & data lake — team vs. space

The question was whether AppFlowy is "mostly integrated in hanzo.team." It is
**not**. `hanzo.team` is **Huly-based** — project management, CRM, HRM, ATS,
Chat, and collaborative rich-text docs (CRDT via yjs). It already owns:
files, tasks, CRM pipeline, and team docs. What it does **not** have is a
Notion/AppFlowy-style *graph-card knowledge base* (linked database cards,
backlinks, graph view).

Recommendation (one way, no Obsidian):

1. **Ops/CRM/tasks/pipeline → `hanzoai/team`** `[LIVE]`. This is the system of
   record for GTM operations (leads, deals, campaigns-as-projects, the daily
   process). Do not duplicate it.
2. **Biz notes / markdown / knowledge graph-cards / data slurp → `hanzo.space`**
   `[ROADMAP]`. Stand it up on `hanzoai/base` (SQLite embedded per replica for
   fast local dev; source of truth) with a graph layer — **zapdb** (Hanzo-native)
   preferred, **dgraph** as the alternative — for graph-cards and backlinks.
   `space` is where all the biz/ops/marketing markdown and databases get
   "slurped up" and made queryable for the AI engineers and agents.
3. **Do not adopt AppFlowy or Obsidian.** If a Notion-like card/DB surface is
   needed, build it as a `space` view on Base, not a third-party app. One way
   to do everything.

Storage policy holds: Base/SQLite by default for local dev; PostgreSQL only
for production multi-instance; the graph layer (zapdb/dgraph) sits on top for
relationships. Chain/commerce remain their own sources of truth; `space`
indexes and links, it does not own transactional data.

## Prior art to absorb (references, not runtime deps)

Study these, extract the useful surface, implement natively on the Hanzo stack.
**Never adopt as runtime dependencies** — registry/secrets/branding rules
(ghcr.io/hanzoai/*, KMS, white-label). One MCP, one connection registry, one
control plane.

| Reference | What to mine | Target Hanzo plane |
|---|---|---|
| `github.com/adnexustech` | native ad **exchange + SSP + DSP** engine | `hanzoai/ads` (merge) `[ROADMAP]` |
| `github.com/pipeboard-co/meta-ads-mcp` | Meta Ads MCP tool surface | Hanzo Ads MCP `[ROADMAP]` |
| `github.com/amekala/ads-mcp` | Ads MCP (marketplace ads) tool surface | Hanzo Ads MCP `[ROADMAP]` |
| `github.com/foxgeeek/adskills` | ad-ops **agent skills** (discrete campaign actions) | Hanzo agent-skills + Ads MCP `[ROADMAP]` |
| `github.com/aialvi/autopost` | social **auto-posting** scheduling patterns | `hanzoai/social` (already `[LIVE]`; mine for gaps) |
| `github.com/EngAmi/meta-ads-growth-os` (**MIT**) | Meta Ads **growth dashboard** — MIT means we can absorb code directly, not just study | `hanzoai/ads` dashboard → **ads.hanzo.ai** + embed in **console.hanzo.ai** `[ROADMAP]` |
| AppFlowy (`AppFlowy-IO/AppFlowy`) | Notion-style graph-cards/DB UX — **considered, NOT adopted** | build as a `hanzo.space` view on Base instead `[ROADMAP]` |

License note: **meta-ads-growth-os is MIT** — license-compatible to fold code
directly into `hanzoai/ads` (unlike AGPL `hanzoai/social`, which is our own repo
anyway). It is the fastest path to a live ads dashboard: rebrand (white-label,
never show source branding), wire to our connected-account layer + KMS, ship at
ads.hanzo.ai and as a console.hanzo.ai tab. Still not a runtime dependency — we
vendor/fork the code into `hanzoai/ads`, we do not `import` their package.

Decision record: **AppFlowy and Obsidian are both rejected** as adopted tools.
Team (Huly) owns CRM/ops/tasks/docs; hanzo.space (Base + zapdb/dgraph) owns the
knowledge graph-cards + biz data-lake. External MCP/skill repos are reference
implementations to absorb into a single Hanzo Ads MCP + agent-skills surface.
