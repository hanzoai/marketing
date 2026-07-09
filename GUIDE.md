# The Guide™ 2.0 — AI-Native GTM Handbook

**INTERNAL.** The Guide™ is the handbook for customer happiness across sales,
marketing, and support. Version 1 (CTO-provided, preserved verbatim at the end of
this repo's history) was written for the Facebook/Google/Mailchimp era. This is
the same discipline, **modernized for the age of AI and mapped onto the
Hanzo-native stack** — because we run our GTM on the product we sell.

Two changes define 2.0:
1. **AI engineers + agents run the loop.** The daily assess→create→optimize→report
   cycle is executed by agents over MCP against connected accounts, supervised by
   AI engineers. Humans set strategy and guardrails; agents do the reps.
2. **One owned stack, not ten SaaS logins.** Every function below runs on a Hanzo
   plane (see `stack.md`). Third-party consoles are the *fallback* until our plane
   for that function is `[LIVE]`.

Status legend: `[LIVE]` · `[LANDING]` · `[ROADMAP]`.

---

## 1. Setup Corporation → Setup Org

*v1:* incorporate + EIN, bank, finance, team, G-Suite, password manager, Slack,
analytics/adwords access.

*2.0:* incorporate + EIN + bank still happen in the real world. Everything digital
is a **Hanzo org** on hanzo.id with a KMS vault — one identity, one secrets store,
one audit trail.

| v1 tool | Hanzo-native | Status |
|---|---|---|
| G-Suite / SSO | hanzo.id (IAM) | `[LIVE]` |
| Password manager | KMS (all secrets, all channel keys) | `[LIVE]` |
| Slack | hanzo chat / team | `[LIVE]` |
| Analytics + AdWords access | Insights + ads connected-accounts | `[LIVE]` / `[ROADMAP]` |
| Google Drive | team files / hanzo.space | `[LIVE]` / `[ROADMAP]` |

Rule: **no channel API key in an env file.** Meta/Google/TikTok/X tokens live in
KMS, surfaced to `ads`/`social` via the connected-account layer.

## 2. Infrastructure → Data-Driven Org, By Default

*v1:* connect Facebook Business, Mailchimp, GitHub, Drive, DNS to Cloudflare;
thesis → test → validated learning.

*2.0:* the data-driven org is the *default state*, because instrumentation is
built into the platform, not bolted on. Thesis → **instrument in Insights** →
validated learning. DNS/hosting per the platform rules (ingress + static, never
nginx/caddy; Cloudflare at the edge is fine for DNS).

- **Validated learning engine:** Insights (events, funnels, flags, A/B) `[LIVE]`
  + funnel wiring `[LANDING]`.
- **Connections:** social (28+ ch) `[LIVE]`, ads connected-accounts `[ROADMAP]`,
  GitHub/GitLab for the OSS rail `[ROADMAP]`.
- **Knowledge/data slurp:** team (ops/CRM) `[LIVE]` + hanzo.space (biz KB /
  graph-cards on Base + zapdb/dgraph) `[ROADMAP]`.

## 3. Research & Plan

*v1:* market research, personas, branding + messaging, narrative engine, feedback.

*2.0:* same discipline, AI-accelerated. Agents synthesize competitor teardowns and
persona research; humans own the narrative.

- **Market/competitor research:** agent-run (deep-research), stored in
  team/hanzo.space; competitor channel/pricing/social teardowns on a schedule.
- **Personas:** 2–3 buyer personas + journeys (top/mid/bottom funnel), kept in the
  KB, referenced by every campaign + landing page.
- **Branding + messaging:** `hanzoai/brand` (white-label by domain) `[LIVE]` +
  messaging doc (`ads/` here is the draft copy bank).
- **Narrative engine:** the one-binary / node-viral / oss-pay / price-shock spine
  (see `ads/`). One narrative, many surfaces.

## 4. Setup Accounts → Connected-Account Registry

*v1:* Facebook Business Manager, Google Analytics, AdWords MCC, Bing, TikTok,
Reddit, Warpcast, WhatsApp, Telegram, SMS, AdEspresso.

*2.0:* **one connection registry** (KMS-backed, OAuth) shared by `social`
(organic) and `ads` (paid), operated over the **Hanzo Ads MCP** — so agents post,
boost, and report across every channel through one tool surface.

| v1 channel | 2.0 plane | Status |
|---|---|---|
| Facebook/Instagram/TikTok/Reddit/X organic | `hanzoai/social` (28+ ch) | `[LIVE]` |
| Facebook/Google/TikTok paid | `hanzoai/ads` + connected-accounts + MCP | `[ROADMAP]` |
| Analytics | `hanzoai/insights` | `[LIVE]` / wiring `[LANDING]` |
| Email/SMS/WhatsApp/Telegram | `hanzoai/notify` + `auto` connectors | `[LIVE]` |
| AdEspresso (creative testing) | `hanzoai/studio` (gen) + `ads` (rotation) | `[LIVE]` / `[ROADMAP]` |
| Native exchange/SSP/DSP | `hanzoai/ads` + adnexustech | `[ROADMAP]` |

MCP note: fold in `pipeboard-co/meta-ads-mcp` and `amekala/ads-mcp` as reference
implementations; ship **one Hanzo Ads MCP** against our connected accounts (never
external MCPs as runtime deps — registry/secrets/branding rules).

## 5. Paid Audience + Campaign Structure

*v1:* the Facebook RETARGETING / PROSPECTING / LOOKALIKE / LOCAL / ENGAGEMENT /
LIKE structure, and the AdWords Search/Display/Video split.

*2.0:* **the structure is timeless; the operator changes.** The same audience
architecture, executed by the `ads` control plane + MCP agent, delivered to
Meta/Google/TikTok *and* our own exchange.

- **Retargeting** (highest ROI): custom audiences from the waitlist list, site
  visitors, cart/checkout abandons, engagers. Our warm list is the crown jewel
  (see `analysis/channels.md`).
- **Prospecting:** 3–6 interest/persona test audiences, known users excluded.
- **Lookalike:** 1% + 5% of purchasers / cart-abandoners / leads / engagers.
- **Local/geo, engagement→conversion progression, budget reallocation** — run by
  the agent on the daily loop.
- **Attribution:** Insights + unique promo codes per channel/sponsor.
- **Owned inventory:** the adnexustech exchange lets us run our own supply — a
  showcase and a Phase-3 B2B product.

## 6. Analytics — Insights, not GA

*v1:* link AdWords, enhanced ecommerce, referral exclusion, goals (Signup/Sale/
Add-to-cart), remarketing audiences, tag every page.

*2.0:* **`hanzoai/insights`** replaces GA4 wholesale — self-hosted, full data
ownership, event-native, with flags + session recording + A/B built in.

- **Goals → events:** `activation` (signup→plan), `purchase` (Sale), cart events.
  Canonical schema in `analysis/waitlist-phase.md`.
- **Enhanced ecommerce → commerce events:** billing engine emits subscription /
  promo / churn events straight to Insights.
- **Remarketing audiences:** cohorts (3/7/30/90/365d, signup, cart, customers)
  built in Insights, pushed to the `ads` connected-accounts for retargeting.
- **Referral exclusion / cross-domain:** handled at the analytics client
  (`cloud/clients/analytics`) `[LIVE]`.

## 7. Paid Search/Display/Video — the ads control plane

*v1:* AdWords campaign structure, import Analytics conversions, US-first, brand vs.
generic, Search/Display/Video splits.

*2.0:* same taxonomy, run through `hanzoai/ads` `[ROADMAP]`. Insights conversions
(activation→Lead, purchase→Sale) import automatically (owned pipeline, no manual
export). Brand keywords in their own campaigns; audience splits at the campaign
level; the agent mines search terms nightly and prunes.

## 8. Email — Notify, not Mailchimp/Mandrill

*v1:* enable transactional, verify sending domain, DKIM + SPF in Cloudflare.

*2.0:* **`hanzoai/notify`** `[LIVE lib]` for transactional + drip across
email/SMS/push/chat; DKIM+SPF at the sending domain; sequences orchestrated by
`hanzoai/auto`. Campaign UI `[LANDING]`. Lifecycle drips (engage/delight/sell/
retain), abandoned-cart, order-confirmation, win-back — all as `auto` workflows.

## 9. Creatives & Documents

*v1:* creative guidelines, new-creative process, landing URL, messaging doc, ad
text, embed analytics, optimize.ly landing review.

*2.0:* **creative is generated, versioned, and A/B'd by the platform.**

- **Generation:** `hanzoai/studio` (visual AI engine) — image/video ad creative on
  demand, on brand (`hanzoai/brand`).
- **Copy bank:** `ads/` in this repo (draft) → approved copy in the KB.
- **Landing A/B + heatmaps:** Insights (A/B + session recording) replaces
  optimize.ly + Hotjar.
- **Every page has a CTA, no dead ends** (Guide law, preserved).

## 10. Marketing Automation — Auto

*v1:* design funnels; email sequences that train users, nudge to goal, stage-
appropriate emails, post-purchase follow-ups, LTV maximization.

*2.0:* **`hanzoai/auto`** `[LIVE]` is the funnel engine — durable workflows on
Base + tasks, with the connector library (facebook-leads, google, linkedin,
heymarket-sms, sheets…) already built. Funnels are workflows; drips are triggers;
LTV maximization is a set of lifecycle automations. Agents author and tune them.

## 11. Daily Process — the agent loop

*v1:* ASSESS (referrals, ad efficiency, social monitoring, keywords, cost,
trends) → CREATE (new ads, inbound) → OPTIMIZE (boost, budgets, kill losers, new
campaigns, experiments) → REPORT (daily report, Slack outliers).

*2.0:* **this is the AI engineer's supervised agent loop**, run daily over MCP:

1. **ASSESS** — agent pulls Insights (CAC/LTV, funnel, cohorts), social analytics,
   spend, search terms, trends. Flags outliers.
2. **CREATE** — agent drafts new ad variants (`studio` creative + `ads/` copy
   patterns), inbound (blog/landing/CTA).
3. **OPTIMIZE** — agent reallocates budget, **kills poor performers**, launches
   expanded-audience experiments — on Meta/Google/TikTok/own-exchange via the Ads
   MCP. Human approves spend-moving actions above a threshold.
4. **REPORT** — daily account report to team; Slack/chat alerts on outlier
   referrals, trends, adjustments via `notify`.

The human sets guardrails (budget caps, kill thresholds, brand rules); the agent
does the reps. This is "AI engineers responsible for setup, management, and
optimization" (Guide v1) made operational.

## 12. User Studies

*v1:* execution > secrecy; always ask for feedback.

*2.0:* unchanged as philosophy. Continuous survey of current/churned/warm users
(via notify + in-product), live UX feedback + session recording (Insights), top-5
LTV interviews. Feedback lands in the KB (hanzo.space), tagged, queryable by
agents.

## 13. Marketing Strategies — the tactic library, mapped

The v1 Guide's ~150 tactics across **Business/Market Insight, Conversion
Optimization, Lead Gen/Traffic, Lead Nurturing, Search Optimization, Social Proof
& Trust, Viral Coefficient** remain the canonical tactic library. 2.0 doesn't
delete any — it assigns each an owner (agent vs. human) and a plane:

| Category | Primary plane(s) | Agent-run? |
|---|---|---|
| Business/Market Insight (personas, CLV/CAC, competitor teardowns, cohort analysis, north-star KPIs) | Insights + team/space (KB) | Mostly agent (synthesis); human owns KPIs |
| Conversion Optimization (A/B landing/payment/newsletter, heatmaps, hyper-targeted pages, on-site capture) | Insights (A/B + session) + studio (variants) | Agent-run, human-approved |
| Lead Gen/Traffic (forums, YouTube sponsorships, lead-magnet tools, Quora, SEO content, FB groups, influencers, PPC) | social + ads + studio + auto | Mixed; relationship tactics stay human |
| Lead Nurturing (retargeting, case studies, drips, webinars, win-back, upsell/cross-sell, private groups) | notify + auto + social + ads | Agent-run sequences |
| Search Optimization (keyword research, pillar pages, backlinks, repurposing, directory profiles) | content + Insights + agent research | Mostly agent |
| Social Proof & Trust (press list, testimonials, trust icons, case studies, PR) | brand + team (CRM) + site | Human-led, agent-assisted |
| Viral Coefficient (ambassador program, gamified loyalty, UGC incentives, share triggers, double-sided referral) | **waitlist + commerce credits** | **Built: this is Phase 0/1** |

The **Viral Coefficient** category is the one we've already *built* into product:
the double-sided referral, gamified points/leaderboard, and share triggers are the
waitlist engine (`[LIVE]`) + referral credits (`[LANDING]`). The rest of the
library is the backlog the daily agent loop works through.

## What changed from v1 → 2.0 (summary)

- **Operator:** human marketer → AI engineer + agent over MCP.
- **Analytics:** GA4 → Insights (owned, event-native, flags + session + A/B).
- **Email:** Mailchimp/Mandrill → notify + auto.
- **Ads:** Facebook/Google managers + AdEspresso → social (organic) + ads
  (paid, MCP-driven) + adnexustech (owned exchange) + studio (creative).
- **CRM/ops/KB:** Drive + spreadsheets → team (CRM/ops) + hanzo.space (KB/graph).
- **Secrets:** password manager → KMS.
- **Identity:** G-Suite → hanzo.id.
- **Unchanged:** the discipline. Data-driven, validated learning, every-page-a-CTA,
  kill poor performers, ask for feedback, execution over secrecy. The Guide's laws
  hold; only the tools got better — and now we own them.
