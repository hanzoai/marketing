# GTM Checklist

**INTERNAL ONLY.** The ordered business/GTM checklist, human-readable mirror of
`checklist.yaml` (the machine-readable source ops drives from). Follows The
Guide™ flow: setup → infra → research → accounts → instrumentation → automation →
phased launch → daily loop.

Status: **[x] done** · **[~] landing** (in progress) · **[r] roadmap** (specced,
not started) · **[ ] todo** (real-world action, no code dependency).

## Setup Org
- [ ] Incorporate + EIN + company bank account — *cto, external*
- [ ] Finance plan (bootstrap / angel / F&F) — *cto*
- [ ] Build the GTM team (AI engineers own campaigns) — *cto, team*
- [x] Org + SSO on hanzo.id — *iam*
- [x] KMS vault; all channel keys in KMS, never env — *kms*
- [x] Team chat / collaboration — *team*

## Infrastructure / Data-Driven Org
- [x] DNS at edge (Cloudflare) + platform ingress/static (never nginx) — *ingress*
- [x] Insights product (events/flags/session/A-B/cohorts) — *insights*
- [~] Wire Phase-0 funnel events into Insights (canonical schema) — *insights*
- [~] Admin/operator cockpit as metrics read + alert surface — *operator*
- [r] Biz KB / data-lake (graph-cards) on Base + zapdb/dgraph — *hanzo.space*
- [x] CRM/ops/pipeline system of record — *team (Huly)*

## Research & Plan
- [ ] 2-3 buyer personas + journeys (top/mid/bottom funnel) — *space*
- [ ] Competitor teardowns (pricing/channels/social), scheduled — *space*
- [x] Brand + messaging guidelines (white-label by domain) — *brand*
- [x] Narrative spine (one-binary / node / oss-pay / price-shock) — *ads/*
- [ ] North-star + leading/lagging KPIs defined — *insights*

## Setup Accounts / Connected-Account Registry
- [x] Social command dash (schedule/publish/analyze, 28+ ch) — *social*
- [~] Paid social ads module on the 28-ch base — *social*
- [r] Connected-account registry (OAuth + KMS): Meta/Google/TikTok/X/Reddit — *ads*
- [r] hanzoai/ads full backend (control plane + adnexustech SSP/DSP/exchange) — *ads*
- [r] Hanzo Ads MCP over connected accounts (absorb meta-ads-mcp / ads-mcp / adskills) — *ads*
- [~] Email/SMS/WhatsApp/Telegram sending domains (DKIM+SPF) — *notify*

## Measurement Plane
- [~] Canonical Phase-0 events emitting (join/share/invite/referral/node/activation) — *insights*
- [~] K-factor + share-rate + activation derived metrics + dashboards — *insights*
- [r] Spend/conversion attribution (unique promo codes per channel) — *insights*
- [r] Daily account report + Slack/chat outlier alerts — *notify*

## Marketing Automation / Funnels
- [x] Workflow engine + connector library (funnels/drips/lead-routing) — *auto*
- [~] Lifecycle drips (welcome/climb/access + engage/delight/sell/retain) — *auto*
- [r] Abandoned-cart + order-confirmation + win-back sequences — *auto*

## Phase 0 — Waitlist Launch
- [x] Waitlist engine live (Turnstile, points, referral, leaderboard, neighborhood-view) — *waitlist*
- [x] Points config (referral 10 / share 2 / follow 15 / node 25) — *waitlist*
- [~] run-hanzod → identity node-proof (attested points) — *waitlist*
- [ ] A/B share-loop placement (H1) — *insights*
- [ ] A/B points weighting (H2) — *waitlist*
- [ ] **GATE:** K-factor trending ≥ 0.5 + activation measured + events emitting — *cto*

## Phase 1 — Paid + Launch Promo
- [x] Commerce billing engine (tiers/plans/proration/trials/coupons) — *commerce*
- [~] 90%-off-first-month promo, server-enforced cap = 1000, atomic counter — *commerce*
- [~] Live "N of 1000 claimed" countdown (from redemption counter) — *commerce*
- [r] Waitlist-first promo allocation by rank order — *commerce*
- [~] Warm-list retargeting (email + social) with promo — *notify*
- [ ] HN Show HN + Product Hunt coordinated launch — *cto*
- [r] 1-2 dev-YouTube sponsorships (unique codes) — *ads*
- [ ] **GATE:** ≥ 1 channel LTV:CAC ≥ 3 + promo month-2 retention ≥ baseline — *cto*

## Phase 2 — Viral Node Expansion
- [~] hanzod node-proof (attested capacity) — *cloud*
- [~] Points → credits bridge — *commerce*
- [r] x402 / wallet earnings for compute contributed — *x402*
- [r] TEE/CC GPU premium node tier + SLO monitoring — *cloud*
- [ ] **GATE:** operator 30d retention ≥ 40% + operator-served inference within SLO — *cto*

## Phase 3 — OSS Flywheel
- [r] Authors 25% compute-share (GitLab + per-compute attribution) — *gitlab*
- [r] Recursive-org substrate + multi-level referral cuts — *iam*
- [r] x402 marketplace (agents/tools) — *x402*
- [x] Enterprise EE tier (hanzo-private) license-gate — *licensing*
- [ ] Techstars-portfolio deal (Option A: free Pro 1yr) — *commerce*
- [ ] Edu + OSS-maintainer free tiers (verified) — *commerce*

## Daily Agent Loop (ongoing)
- [r] **ASSESS** — CAC/LTV, funnel, cohorts, social, spend, search terms, trends — *insights*
- [r] **CREATE** — new ad variants (studio) + inbound (blog/landing/CTA) — *studio*
- [r] **OPTIMIZE** — reallocate budget, kill poor performers, run experiments — *ads*
- [r] **REPORT** — daily report + Slack/chat outlier alerts — *notify*
- [r] User studies — continuous survey + session recording + LTV interviews — *insights*

---

**The three gates that govern everything:**
1. **Phase 0→1:** no paid dollar until Insights emits + K-factor healthy.
2. **Phase 1→2:** no node-incentive budget until a channel is profitable + promo retains.
3. **Phase 2→3:** no flywheel scale until operator retention + inference SLO hold.

Skipping a gate is the one way this plan fails. Don't skip a gate.
