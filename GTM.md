# Go-to-Market

The plan for taking Hanzo from public signup to a self-reinforcing network. Four
phases. Each phase has an **entry gate** (what must be true to start it), an
**exit gate** (what must be true to move on), and a **kill criterion** (what
tells us to stop and rethink instead of pouring more money in).

## Ground rules

- **Every number below is a TARGET** unless it links to a measured source.
  Targets are hypotheses, not promises. They get replaced by measured values in
  `analysis/` once the data exists.
- **One funnel, one source of truth.** All signup, activation, and referral
  events land in `/v1/tracker`; all cohort and channel reads come from
  `/v1/analytics`. No spreadsheet becomes a second source of truth.
- **A phase does not "end."** Its spend and attention wind down as the next
  phase's engine takes over. Points, referral, and the waitlist persist across
  all four phases.

## Product surface (what access means)

| Surface | URL | Phase 0 status |
|---|---|---|
| Marketing site + signup | `hanzo.ai` | **Public, free** |
| Docs | `docs.hanzo.ai` | Public |
| Console | `app.hanzo.ai` / `/console` | **Waitlisted** |
| Chat | `/chat` | **Waitlisted** |
| Cloud app / API | `api.hanzo.ai` | **Waitlisted** |
| Studio | `studio.hanzo.ai` | Waitlisted |
| Node | `hanzod` | Public download; running it earns access |

"On the waitlist" means the account exists and is free to create; the gated
surfaces are unlocked by position, by points, or by running a node.

---

## The points ledger (spans all phases)

Points do one job: **move a waitlisted account up the access queue.** They are
not currency and are not redeemable for cash.

| Action | Points | Verified by |
|---|---|---|
| Referral (referred account activates) | **10** | `/v1/tracker` activation event tied to a referral code |
| Share (unique outbound share click) | **2** | `/v1/tracker` share event, deduped per destination |
| Social follow | **15** | OAuth-confirmed follow (X, GitHub) |
| Run `hanzod` (per qualifying node) | **25** | Node heartbeat to the coordinator, min uptime window |

Anti-gaming rules live in `discounts.md` (shared abuse-guard section); the
referral point only fires on **activation**, never on signup, so a wall of dead
invites earns nothing.

---

## Phase 0 — Waitlist and email

**Goal:** build a real, engaged email list and a ranked access queue before
spending a dollar on ads.

**Entry gate**
- Public signup live on `hanzo.ai`, writing to `/v1/tracker`.
- Points ledger deployed; referral codes issued at signup.
- Transactional + sequence email wired (see `GUIDE.md` → Email).

**What we do**
- Drive signups through owned channels: OSS repos, docs, Discord, founder
  social, the `hanzod` download page.
- Every signup gets a referral code and a visible queue position.
- Weekly access waves: unlock the top of the queue (position + points) into
  console/chat/app in controlled batches so we can watch activation and load.

**Exit gate (all TARGETs)**
- ≥ 10,000 signups.
- ≥ 30% of signups complete at least one point-earning action (referral, share,
  follow, or node).
- Email sequence open rate ≥ 35% and click rate ≥ 5% (measured, not assumed).
- Activation rate of unlocked users ≥ 40% (unlocked → first real console/chat/API action).

**Kill criterion**
- Organic signups stall below **500/week for 3 consecutive weeks** with no
  channel showing a path to more, **or** activation of unlocked users stays
  below **20%**. Below 20% activation, paid acquisition in Phase 1 would pour
  users into a leaky bucket — stop and fix activation first.

---

## Phase 1 — Paid acquisition + launch promo

**Goal:** buy growth profitably now that the funnel converts, and convert the
warm waitlist into paying users with a time-boxed offer.

**Entry gate**
- Phase 0 exit gate met (funnel proven to convert organically).
- Analytics goals defined in `/v1/analytics` for signup → activation → paid.
- Promo implemented and abuse-guarded per `discounts.md`.

**What we do**
- **Promo:** *90% off the first month for the first 1,000 paying users.* Applies
  to the first paid month of Pro ($49), Max ($200), or Team ($199). One
  redemption per verified org. Full spec, stacking rules, and revenue math in
  `discounts.md`.
- **Paid channels:** FB/Meta and Google campaigns structured per `GUIDE.md`
  (campaign hierarchy, retargeting, lookalikes). Retarget waitlist and site
  visitors first — cheapest, warmest audience.
- Landing-page and offer A/B tests via native feature flags (`GUIDE.md` → Insights).

**Exit gate (all TARGETs)**
- Blended CAC < 12-month gross margin per user (unit economics positive). CAC and
  LTV are computed in `analysis/`, not asserted here.
- ≥ 1,000 paying orgs (promo cohort filled) with month-2 retention ≥ 60%.
- At least one paid channel with a repeatable CAC:LTV ≤ 1:3.

**Kill criterion**
- Blended CAC exceeds 12-month gross margin for **4 consecutive weeks** after
  creative/audience iteration, **or** promo-cohort month-2 retention < 30%
  (the offer is buying churners, not customers). Pause paid spend; the offer or
  the product, not the ad account, is the problem.

---

## Phase 2 — Viral node expansion

**Goal:** turn users into infrastructure. Running `hanzod` earns access and
points, which grows both capacity and the queue at once.

**Entry gate**
- `hanzod` packaged for one-command install; heartbeat + node-points verified.
- Coordinator can measure node contribution (uptime, served work).
- Phase 1 shows positive unit economics (we are scaling something that works).

**What we do**
- Promote node-running as the fastest path off the waitlist (25 points/node).
- Publish honest node economics: what a node contributes, what access it unlocks.
- Instrument the loop: node count, node retention, share of served work handled
  by community nodes.

**Exit gate (all TARGETs)**
- ≥ 1,000 active community nodes with 30-day node retention ≥ 50%.
- Community nodes serve ≥ 20% of eligible workload (measured share).
- Node-driven signups become a top-3 acquisition channel by volume.

**Kill criterion**
- 30-day node retention < 20% (people run it once for points, then quit), **or**
  community-served workload stays < 5% after packaging and docs are solid. If
  nodes don't stay up, they aren't infrastructure — treat node-points as a pure
  acquisition cost and re-scope.

---

## Phase 3 — OSS flywheel

**Goal:** make it economically rational to build in the open on Hanzo. Authors of
open-source models/tools that run on the network earn a **25% compute share**.

**Entry gate**
- Metering attributes compute to a specific OSS artifact (model/tool).
- Payout rail live and auditable (per compute-share accounting).
- Phases 1–2 stable: paying base + node capacity to serve OSS demand.

**What we do**
- Publish the 25% compute-share program with transparent, auditable accounting.
- Recruit model/tool authors; feature their work in Studio and the catalog.
- Measure the loop: OSS artifacts published → compute they drive → payouts →
  new artifacts.

**Exit gate (all TARGETs)**
- ≥ 50 OSS authors receiving non-trivial monthly compute-share payouts.
- OSS-attributed compute is a growing share of total, quarter over quarter.
- Author-published artifacts drive measurable new signups (attributed in `/v1/tracker`).

**Kill criterion**
- After two full payout quarters, OSS-attributed compute < 5% of total and flat,
  **or** author retention (published again within 90 days) < 15%. The revenue
  share isn't changing author behavior — revisit the split or the developer
  experience before scaling payouts.

---

## Instrumentation contract

Every phase reads from the same two APIs. If an event isn't in `/v1/tracker`, it
didn't happen for GTM purposes.

- **Capture:** `/v1/tracker` — signup, activation, share, referral-activation,
  node-heartbeat, purchase, promo-redemption.
- **Read:** `/v1/analytics` — funnels, cohort retention, channel attribution,
  goal conversion.
- **Experiment:** native feature flags (Insights) — landing pages, offers,
  onboarding variants.

The what-worked review after each wave/campaign uses the templates in
`analysis/`. Do not start a new phase's spend without the prior phase's
`analysis/` filled in with **measured** numbers.
