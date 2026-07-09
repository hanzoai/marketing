# Hanzo Go-To-Market — The Master Plan

**INTERNAL ONLY.** The CTO's phased motion from cold start to self-sustaining
flywheel: **Phase 0 waitlist → Phase 1 paid + launch promo → Phase 2 viral node
expansion → Phase 3 OSS flywheel.** Each phase has success metrics, explicit
kill-criteria (the metric whose failure means *pause and fix, do not spend*),
and an honest dependency list against the real systems (see `stack.md` for the
built/landing/roadmap map).

The through-line: **users become infrastructure become research become more
users.** People join a waitlist, pay for Pro, run a node that expands our
compute, that compute powers OSS whose authors earn a cut, whose projects bring
their own users. The GTM is the ignition sequence for that loop.

Status legend: `[LIVE]` · `[LANDING]` · `[ROADMAP]`.

---

## The product truths we sell (measured only)

- **One binary.** "Your AI cloud. One binary. Run it anywhere." — the whole
  cloud is a single Go binary (Base + goja embedding).
- **0.245 MB per tenant.** Multi-tenancy is nearly free — measured, from the
  papers. This is what makes "1B users / 20 nodes" real.
- **1B users / 20 nodes.** The scaling claim, measured, usable in public copy.
- **28+ social channels** from one dash (`hanzoai/social`).
- Everything else (K-factor, CAC, CPM, conversion %) is a **target or
  estimate**, never stated as achieved data until Insights measures it.

Pricing we market against (canonical):

| Plan | Price | Notes |
|---|---|---|
| Developer | **$0** | Free tier; the top of the funnel. |
| Pro | **$49/mo** | The consumer/individual paid tier; promo hero. |
| Max | **$200/mo** | Power users. |
| Team | **$199/mo** | Team tier (seat basis — *flag: confirm per-seat vs. flat in commerce*). |

Billing engine stores prices in cents (`pro` = 4900). All promo math below is
computed against these.

---

## Phase 0 — Waitlist zone (NOW)

**Goal:** prove organic pull before we spend a dollar. Build the email list,
the referral graph, and the node-operator top-of-funnel. Measure everything.

**What's live:** public + free signup, Turnstile-protected, on the viral
waitlist engine (`hanzoai/waitlist` + `base/plugins/waitlist`) `[LIVE]`. Viral
points are config-driven (server is source of truth); the canonical weights:

| Action | Points | Purpose |
|---|---|---|
| Referral (converted — invited friend joins) | **10** | The K-factor driver. |
| Share (X/LinkedIn/copy-link click) | **2** | Cheap, high-frequency loop. |
| Social follow (@hanzoai) | **15** | Convert waitlist → owned audience. |
| Run a hanzod node | **25** | The signature hook: "run a node, jump the line." |

Leaderboard, live activity feed, invite-friends, and the **neighborhood-view**
(benchmarked to 10M entries) are built. Position visualization + "N people
ahead of you, skip the line" is the core drama.

### Drivers
1. **Share loops** — every status page has a share CTA (+2) and a referral link
   (`?ref=`). Placement is a testable variable (see `analysis/waitlist-phase.md`).
2. **Referral links** — double-sided: referrer gets 10 on conversion; invited
   friend lands higher than a cold signup. This is the growth engine.
3. **Run-a-node hook** — 25 points, the biggest single jump, seeds Phase 2. Even
   at Phase 0 this quietly recruits the operators who become our compute.

### Success metrics
- **Signups/day** (trend, not vanity total).
- **Referral K-factor** = (invites sent per user) × (invite→join conversion).
  K ≥ 1 = self-sustaining organic growth. **Target to validate: K ≥ 0.5 by end
  of Phase 0**, trending up.
- **Share rate** = shares / active waitlist user.
- **Waitlist → activation conversion** — % who become Developer (free) or paid
  accounts when access opens. This is the number that justifies Phase 1 spend.
- **Node-signup rate** — % choosing the run-a-node action (Phase 2 leading
  indicator).

### Measurement plane
Insights `[LIVE]` product; funnel wiring `[LANDING]`. Admin cockpit
(`hanzoai/operator`) `[LANDING]` is the read surface. Exact events to
instrument: `analysis/waitlist-phase.md`.

### Kill-criteria (pause, do not advance)
- **K-factor < 0.2 and flat after the list crosses ~2k** → the loop is broken;
  fix share/referral placement and points weighting before ANY paid spend.
  Paid on a leaky bucket burns cash.
- **Share→join conversion < 2%** → the share creative/landing is wrong; fix copy
  (`ads/`) and the invited-friend landing before scaling shares.
- **Instrumentation not emitting** → we are flying blind; **hard block** on
  Phase 1. No spend without measurement.

### Dependencies (honest)
- `[LIVE]` waitlist engine, points, referral, share, leaderboard, neighborhood-view.
- `[LIVE]` social dash for the follow-loop and organic drivers.
- `[LANDING]` Insights funnel instrumentation — **the gating dependency for
  advancing.**
- `[LANDING]` admin/operator cockpit as the metrics read surface.
- `[LANDING]` run-hanzod → waitlist verification (points config supports the 25pt
  action; the node-proof wiring is landing — until then, treat node points as
  self-attested and rate-limited).

---

## Phase 1 — Paid advertising + launch promo

**Goal:** pour fuel on a fire that's already burning. Paid channels open **only
after Phase 0 proves organic pull** (K-factor trending up, activation
conversion measured). Launch with a scarcity promo engineered to be shared.

### The launch promo — 90% off first month, first 1,000 users

Spec against real plans (billing engine, cents):

| Plan | List | 90% off first month | Shareable line |
|---|---|---|---|
| Pro | $49 | **$4.90** | "$4.90 first month" — the hero number |
| Max | $200 | **$20.00** | "$20 first month" |
| Team | $199 | **$19.90** | "$19.90 first month" |

**$4.90 first month Pro** is the campaign spearhead — an absurd, screenshot-able
number. Mechanics:
- Promo code(s) via `hanzoai/commerce` coupon system `[LIVE engine]` /
  capped-redemption flow `[LANDING]`.
- **Hard cap: 1,000 redemptions**, enforced server-side (atomic counter in
  commerce; not client-trusted). First-month only; month 2 reverts to list.
- **Countdown surfaces on the site**: "X of 1,000 claimed" — live scarcity.
  Pulls from the commerce redemption counter.
- **Waitlist gets first dibs**: the 1,000 codes are offered to the waitlist by
  rank order first (reward the referrers), remainder to paid channels. This ties
  Phase 1 back into Phase 0 and makes the waitlist position *mean something*.
- Anti-fraud: one redemption per verified identity (hanzo.id) + payment-method
  fingerprint; Turnstile at claim; excludes disposable-email domains (already in
  the waitlist blocklist). See `discounts.md`.

### Channels
Retarget the warm list first, then prospect. Full plan + estimated ranges in
`analysis/channels.md` (all CPM/CAC marked ESTIMATE-TO-VALIDATE — no spend data
yet).
- **X/Twitter dev audience** — where the one-binary story lands; founder-led +
  paid amplification.
- **Hacker News launch** — Show HN, the one-binary + 0.245MB/tenant + 1B/20-nodes
  proof. Organic; timed, not paid.
- **Product Hunt** — coordinated launch-day; waitlist becomes the upvote army.
- **Dev-YouTube sponsorships** — mid-roll in buyer-intent AI/infra channels (per
  The Guide™: sponsored links in high-intent videos).
- **Retargeting the waitlist email list** — the highest-ROI audience; drives promo
  redemption. Runs on `hanzoai/notify` (email) + `hanzoai/ads` `[ROADMAP]` /
  `hanzoai/social` paid `[LANDING]` for social retargeting.

### Success metrics
- **CAC by channel** (blended and per-channel) vs. **LTV** — the gate on scaling
  any channel. Scale only channels where LTV:CAC clears the threshold (target
  ≥ 3:1, to validate).
- **Promo redemption rate + velocity** (how fast the 1,000 go) — the scarcity
  signal.
- **Promo → month-2 retention** — the number that says the promo bought customers,
  not tourists. **This is the real success metric of Phase 1.**
- **Payback period** by channel.

### Kill-criteria
- **LTV:CAC < 1.5:1 on a channel** → kill that channel (Guide daily process:
  "kill poor performers"). Reallocate, don't defend.
- **Promo month-2 retention < baseline free→paid retention** → the promo is
  buying churners; stop widening it, tighten targeting to warm/waitlist only.
- **Blended CAC > 1-month Pro price with no retention lift** → we're renting
  logos; pause paid, return to organic + fix activation.

### Dependencies (honest)
- `[LIVE]` commerce billing engine + coupon processors.
- `[LANDING]` **capped-at-1000 promo redemption + live countdown** — the gating
  build for the launch promo. Until it's atomic and server-enforced, do not run
  the scarcity campaign (a miscounted cap is a public embarrassment + margin leak).
- `[LIVE]` notify for email retargeting; `[LANDING]` campaign UI on top.
- `[ROADMAP]` `hanzoai/ads` control plane for paid-channel automation — Phase 1
  can launch with manual channel management (Meta/Google/X consoles) and
  `hanzoai/social` paid `[LANDING]`; `ads` automation makes it scale.
- `[LANDING]` Insights spend/conversion attribution — must be wired before scaling.

---

## Phase 2 — Viral node expansion (the compute flywheel)

**Goal:** turn users into infrastructure. The waitlist and promo brought people;
now the "run a node, jump the line" hook converts a slice of them into **hanzod
node operators who expand OUR cloud + GPU capacity.** Users become the supply side.

### The mechanic
1. Waitlist fills via social + referral (Phase 0/1).
2. The 25-point run-a-node action `[LIVE config]` / node-proof `[LANDING]` is the
   entry: run hanzod, jump the line — a real reward for real capacity.
3. Points → credits `[LANDING]`: node points convert to platform credits
   (spend on Pro/Max usage). The first economic bridge.
4. x402 / wallet earnings `[ROADMAP]`: operators earn for compute *contributed* —
   per-agent / per-project wallets, x402 settlement. This is the durable
   incentive that outlives the waitlist gimmick.

### Node tiers
- **CPU/edge nodes** — the broad base; expand cloud capacity, jump-the-line +
  credits.
- **GPU node operators = the premium tier** — TEE/CC-capable (confidential
  compute) nodes command premium earnings; they run the paid inference. Marketing
  angle: "your GPU earns while you sleep; confidential by hardware."

### Success metrics
- **Nodes online / net-new nodes per week** — the capacity growth rate.
- **Compute contributed** (GPU-hours, requests served) vs. **our cloud cost
  avoided** — the flywheel's unit economics. Every operator node is CAC we didn't
  pay + capex we didn't spend.
- **Operator retention** (nodes still online at 30/90d) — churn of supply.
- **% of platform inference served by operator nodes** — the flywheel's share of
  total load.

### Kill-criteria
- **Operator 30-day retention < 40%** (to validate) → the incentive doesn't hold;
  fix credits/earnings economics before promoting node-running harder.
- **Operator-served inference quality/latency SLO breach** → pause growth of the
  operator-served pool; a bad node hurts the paid product. Quality gate before
  scale.
- **Credit/earning payout > value of capacity contributed** → the economics are
  upside-down; re-price before scaling (don't subsidize into a hole).

### Dependencies (honest)
- `[LIVE config]` 25-pt run-a-node waitlist action.
- `[LANDING]` hanzod → identity node-proof (so points/credits are earned, not
  claimed).
- `[LANDING]` points → credits bridge.
- `[ROADMAP]` x402 / wallet earnings rail (per-agent/project wallets, settlement).
- `[ROADMAP]` TEE/CC GPU-node premium tier + operator quality/SLO monitoring.
- **Honest flag:** Phase 2's *economics* (credits, earnings) are the least-built
  part of the plan. Phase 2 can start on jump-the-line alone (live), but the
  durable version waits on the economics rail.

---

## Phase 3 — The OSS flywheel

**Goal:** the expanded compute powers OSS research; OSS authors earn the **25%
compute share**; their projects bring their users; portfolio + B2B companies
build on Hanzo and refer more companies. Self-sustaining, no paid spend required
to grow.

### The loop
1. Phase-2 compute (operator + our cloud) powers **OSS research + models**.
2. **OSS devs earn 25%** of the compute their code powers — clients *and* authors,
   via per-compute attribution `[ROADMAP]` (GitLab + attribution being completed).
   Marketing hook: **"Your code earns 25% of the compute it powers."**
3. Those OSS projects bring **their own users** onto Hanzo (the project runs on
   our cloud; users follow).
4. **Techstars-portfolio + B2B onboarding** via the recursive-org substrate:
   companies build THEIR products on Hanzo, become orgs, refer more companies;
   **multi-level referral cuts** `[ROADMAP]` reward the chain.
5. Sustained motion: **x402 marketplace** (agents/tools) `[ROADMAP]` +
   **enterprise EE tier** (hanzo-private) `[LIVE license-gate]`.

### Success metrics
- **OSS-project → user acquisition** (users arriving via an OSS project on Hanzo).
- **Author-share paid out** vs. **compute revenue generated** — the 25% must be a
  growth lever, not a cost center; measured as revenue-per-dollar-shared.
- **B2B orgs onboarded + their referred orgs** (multi-level depth) — the recursive
  motion's reach.
- **Marketplace GMV** (x402 agent/tool transactions) once live.
- **Net revenue retention** on the EE tier.

### Kill-criteria
- **Author-share cost > incremental revenue it drives** → the 25% isn't paying
  for itself; adjust attribution/rate before widening.
- **Multi-level referral fraud rate > threshold** → the recursive cuts are being
  gamed; tighten attribution (per-compute, not per-signup) before scaling.
- **Marketplace take-rate can't cover trust/safety cost** → gate marketplace
  growth on quality, not volume.

### Dependencies (honest)
- `[ROADMAP]` authors 25% compute-share (GitLab + per-compute attribution) — the
  central Phase-3 mechanic; being completed.
- `[ROADMAP]` recursive-org substrate + multi-level referral cuts.
- `[ROADMAP]` x402 marketplace.
- `[LIVE]` EE tier license-gate (hanzo-private) — the one Phase-3 monetization
  rail already built.
- **Honest flag:** Phase 3 is the most visionary and least-built. It is the
  *destination*, not a near-term revenue plan. Do not put Phase-3 numbers in any
  investor/public material as committed.

---

## Budget & sequencing logic

**Spend follows proof, never precedes it.** The sequencing is a ratchet: each
phase unlocks the next only when its success metric clears the bar, and each
phase's kill-criterion can send us back.

| Phase | Spend posture | Unlocks next when… |
|---|---|---|
| 0 Waitlist | **~$0 paid** (organic + product). Cost = eng time on instrumentation. | K-factor trending ≥ 0.5 AND activation conversion measured AND instrumentation emitting. |
| 1 Paid + promo | **Metered, per-channel, kill-fast.** Start small; scale only LTV:CAC ≥ 3:1 channels. | ≥ 1 channel proven profitable AND promo month-2 retention ≥ baseline. |
| 2 Nodes | **Incentive budget** (credits/earnings), gated on operator retention. | Operator 30d retention ≥ 40% AND operator-served inference within SLO. |
| 3 OSS flywheel | **Revenue-share budget** (the 25%), self-funding by design. | Author-share revenue-positive AND recursive referral fraud in check. |

Rules:
- **No Phase-1 dollar until Phase-0 instrumentation emits.** Measurement is the
  gate, stated three times because it's the one most tempting to skip.
- **Cap the promo hard at 1,000** — server-enforced. A public "first 1,000" that
  quietly becomes 3,000 destroys the scarcity mechanic and trust.
- **Kill poor performers weekly** (Guide daily process). Defended budgets are
  dead budgets.
- **Honest dependency gating:** if a phase depends on a `[ROADMAP]` system for its
  *durable* form, the phase may *start* on its `[LIVE]` subset but must not be
  marketed as complete. Flagged per phase above.

## Dependency summary (built vs. landing vs. roadmap)

| System | Status | Blocks phase |
|---|---|---|
| Waitlist engine + points + referral + neighborhood-view | `[LIVE]` | 0 (unblocked) |
| Social dash (28+ ch) | `[LIVE]` | 0/1 organic + retargeting |
| Insights product | `[LIVE]` | — |
| Insights waitlist-funnel instrumentation | `[LANDING]` | **0→1 gate** |
| Admin/operator cockpit (metrics read) | `[LANDING]` | 0/1 visibility |
| Commerce billing engine + coupons | `[LIVE]` | 1 |
| Capped-1000 promo redemption + countdown | `[LANDING]` | **1 launch promo gate** |
| Notify (email/SMS lib) | `[LIVE]` | 1/2 drips |
| Notify campaign UI | `[LANDING]` | 1 ease-of-use |
| hanzoai/ads control plane + adnexus SSP/DSP | `[ROADMAP]` | 1 scale (not launch) |
| Social paid-ads module | `[LANDING]` | 1 social retargeting |
| run-hanzod node-proof | `[LANDING]` | 2 (jump-the-line live) |
| Points→credits bridge | `[LANDING]` | 2 economics |
| x402 / wallet earnings | `[ROADMAP]` | 2 durable / 3 marketplace |
| TEE/CC GPU premium tier | `[ROADMAP]` | 2 premium |
| Authors 25% compute-share (GitLab attribution) | `[ROADMAP]` | **3 core** |
| Recursive-org + multi-level referral | `[ROADMAP]` | 3 |
| EE tier license-gate (hanzo-private) | `[LIVE]` | 3 monetization |
| hanzo.space biz data lake (Base + zapdb/dgraph) | `[ROADMAP]` | ops/measurement support |

See `stack.md` for the full plane-by-plane map and `GUIDE.md` for the tactical
handbook mapped onto these systems.
