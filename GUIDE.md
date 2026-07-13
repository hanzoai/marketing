# The Guide&trade; 2.0

The classic direct-response agency playbook — campaign structure, retargeting,
lookalikes, analytics goals, offer testing, and a daily operating rhythm —
rebuilt on Hanzo tooling. Where the old Guide said "open Google Analytics" or
"build a Facebook custom audience," this one says which Hanzo product and route
does the same job.

> **Source note.** The original `the-guide.md` was not reachable at
> `spark:/tmp/the-guide.md` when this was written, so this is a clean rebuild
> from the playbook structure, not a paste. Any performance figure here is a
> **published-benchmark reference or a TARGET**, clearly labeled — never a
> Hanzo-measured result. Measured results live in `analysis/`.

## How to use this

The Guide is a loop, not a checklist you finish once:

```
  measure ─▶ hypothesize ─▶ ship a variant ─▶ measure ─▶ keep or kill
     ▲                                                        │
     └────────────────────────────────────────────────────────┘
```

Everything below feeds that loop. The machine-readable version a founder org
works through step by step is `checklist.yaml` / `CHECKLIST.md`.

---

## 0. Foundations — you cannot optimize what you don't capture

Before a single ad runs, tracking is live. This is the non-negotiable base.

| Job (old playbook) | Hanzo tool | Route |
|---|---|---|
| Analytics / pageviews / funnels | Analytics | `/v1/analytics` |
| Event & conversion capture | Tracker | `/v1/tracker` |
| A/B tests & rollouts | Insights (feature flags) | Insights |
| Content production | Studio | `studio.hanzo.ai` |

**Rule:** one capture layer. Every meaningful action — pageview, signup, add
payment, activate, purchase, share, referral-activation — is a `/v1/tracker`
event with a stable name. If it isn't tracked, it doesn't exist for
optimization. Do not add a second analytics SDK; there is one funnel.

### Analytics goals

Define goals in `/v1/analytics` **before** driving traffic. A goal is a named
conversion with a value. Minimum set for launch:

1. `signup` — account created (value: list-derived, e.g. expected LTV proxy).
2. `activate` — first real product action (console/chat/API call).
3. `add_payment` — payment method attached.
4. `purchase` — first paid month (attach plan + promo flag).
5. `refer_activated` — a referred account activated (ties to points).

Every campaign, email, and landing test is judged against these goals — not
against clicks, not against impressions. Clicks are diagnostics; goals are truth.

---

## 1. Insights — the testing engine (feature flags + analytics)

Insights is where hypotheses become experiments. Native feature flags gate a
variant to a percentage of traffic; `/v1/analytics` reads which variant won
against the goals above.

**Pattern for every test:**
1. Write the hypothesis as one sentence with a metric: *"Headline B lifts
   `signup` conversion vs. A."*
2. Create a flag with variants (A control, B challenger). Split traffic.
3. Let it run to a **pre-declared** sample size / duration — no peeking-and-stopping.
4. Read the goal delta in `/v1/analytics`. Keep the winner, kill the loser,
   log it in `analysis/`.

**What to flag-test, in order of leverage:** offer > landing headline > hero
CTA > pricing presentation > onboarding first-run > email subject lines.
Test one thing at a time so the winner is attributable.

---

## 2. Landing pages & offers

The offer is the highest-leverage variable. Test it first, and test it with real
traffic, not opinions.

- **Offer tests** run behind Insights flags. The launch offer (90% off first
  month, see `discounts.md`) is itself a variant to measure against a no-discount
  and a trial control.
- **Landing structure** (the durable direct-response skeleton): promise headline
  → proof → what it is → offer → single primary CTA → risk reversal → FAQ. One
  page, one CTA, one goal event.
- **Build content in Studio** (`studio.hanzo.ai`) — node-graph workflows for
  copy variants, images, and video. Studio outputs feed the flagged variants.
- **Honesty gate:** every claim on a landing page must be real or labeled as a
  target. No invented benchmarks, no fake logos, no borrowed testimonials.
  A landing page that lies converts once and refunds twice.

---

## 3. Campaign structure — Meta (Facebook/Instagram)

The proven three-tier hierarchy. Keep the layers clean so budget and learning
attribute correctly.

```
Campaign        = objective        (e.g. Conversions → goal: signup/purchase)
  └ Ad Set      = audience + budget + placement
      └ Ad      = one creative + one hook
```

**Audience tiers (cold → warm → hot):**

| Tier | Audience | Source |
|---|---|---|
| Hot | Waitlist + site visitors + cart-abandoners | `/v1/tracker` events exported to the ad platform's custom-audience |
| Warm | Lookalikes of activated/paying users | Seed = paying-user list from `/v1/analytics`; platform builds the lookalike |
| Cold | Interest / broad prospecting | Platform targeting |

**Rules:**
- One conversion objective per campaign, mapped to one analytics goal.
- Separate cold, warm, and hot into different campaigns — never let retargeting
  spend hide inside a prospecting campaign's numbers.
- Start each ad set with 3–5 creatives, kill the losers fast, scale the winner.
- Feed the platform your **real** conversion events from `/v1/tracker` so its
  optimizer learns on truth, not proxy clicks.

---

## 4. Campaign structure — Google

Two intents, two motions. Don't blend them.

- **Search (high intent):** bid on terms where someone already wants what we do
  (e.g. "AI coding assistant", "hosted MCP", competitor terms where allowed).
  Tight ad groups: one theme → a few keywords → matching ad → matching landing
  page. Map conversions to the same `/v1/analytics` goals.
- **Performance/Display + YouTube (demand-gen):** creative-led, audience-targeted,
  including retargeting site visitors and lookalike-style similar audiences.

**Rule:** search captures existing demand; display/social *creates* it. Fund and
judge them separately — a search campaign and a prospecting display campaign have
different jobs and different acceptable CAC.

---

## 5. Retargeting + lookalikes

The cheapest conversions you will ever buy come from people who already touched
you. Retargeting is mandatory before scaling cold spend.

**Retargeting ladder** (built from `/v1/tracker` audiences):
1. Visited pricing, didn't sign up → offer clarity + the launch promo.
2. Signed up, didn't activate → onboarding nudge, "here's your first win."
3. Activated, didn't pay → the offer, risk reversal, proof.
4. Cart/checkout abandon → the exact plan they left, promo reminder.

**Lookalikes / similar audiences:**
- Seed only from **high-value, verified** events — activated or paying users
  pulled from `/v1/analytics`, never raw signups. Garbage seed, garbage
  lookalike.
- Rebuild seeds as the paying base grows; a lookalike is only as current as its
  seed.
- Suppress existing customers from prospecting audiences (don't pay to acquire
  who you already have).

---

## 6. Content — Studio

`studio.hanzo.ai` (node-graph visual workflows) is the content factory feeding
every channel above.

- **Ad creative:** hooks, image/video variants for Meta/Google/YouTube.
- **Landing assets:** hero imagery, explainer clips, comparison visuals.
- **Email assets:** header art, diagrams.
- **Organic/social:** repurpose one core asset into per-channel cuts.

Workflow: one core message → Studio fans it into channel-native variants →
variants ship behind Insights flags → `/v1/analytics` says which lives. Reuse the
winning angle everywhere; retire the rest.

---

## 7. Email campaigns

Owned audience, zero per-send auction cost — the highest-ROI channel we control.
Two motions:

**Transactional / lifecycle (triggered by `/v1/tracker` events):**
- Welcome + queue position (on `signup`).
- "You're unlocked" (on access-wave grant).
- Activation nudge (signed up, no `activate` after N days).
- Trial/promo ending (before month-1 promo snap-back — honest, no dark pattern).
- Win-back (paid, then churned).

**Sequence / nurture (the launch runway):**
- Waitlist nurture: what Hanzo is, proof, how to climb the queue (points),
  founder story. Cadence tuned to keep open rate ≥ 35% (TARGET) — if a send
  drops opens, cut frequency.

**Measured, not assumed:** open, click, and goal-conversion per email read from
`/v1/analytics`. Subject lines are Insights-flagged A/B tests. Kill any sequence
step that doesn't earn its send.

---

## 8. Social / paid social

Covered structurally under Meta (§3). Operating notes:

- Organic social seeds the audiences retargeting later harvests — post
  consistently on the calendar (§9), even pre-spend.
- Social-follow is a **15-point** waitlist action (see `GTM.md`) — every organic
  post can carry the "follow to climb the queue" ask.
- Creative is produced in Studio (§6); performance is judged on `/v1/analytics`
  goals, not vanity likes.

---

## 9. The calendar & daily process

Rhythm beats intensity. The old Guide's "daily process" on Hanzo tooling:

**Daily (15–30 min):**
- Open the `/v1/analytics` dashboard. Check yesterday's goals: signup, activate,
  purchase, CAC by channel.
- Scan ad spend vs. conversions. Pause any ad set breaching its CAC ceiling.
- Reply to the funnel: fix anything that broke overnight (dead link, failing
  event).

**Weekly:**
- Review each Insights experiment; call winners/losers at pre-declared sample.
- Refresh creative on fatigued ad sets (frequency up, CTR down).
- Publish the content calendar for the coming week (Studio assets queued).
- Fill in the `analysis/` weekly row with **measured** numbers.

**Per phase (from `GTM.md`):**
- Run the full what-worked analysis (cohort, channel, CAC/LTV) in `analysis/`
  before opening the next phase's spend.

**Content calendar** = one shared schedule of sends (email), posts (social), and
launches (offers/experiments), so channels reinforce instead of collide. A promo
push, its emails, its ads, and its organic posts land the same week by design.

---

## 10. Metrics that matter (and the ones that don't)

**Judge on:** cost per goal (signup/activate/purchase), activation rate, cohort
retention, CAC vs. LTV, referral-driven signups. These decide spend.

**Diagnose with (never optimize to):** clicks, CTR, CPM, impressions, likes.
They explain *why* a real metric moved; they are not the goal.

**The one honesty rule that governs all of it:** every number that leaves this
repo — in an ad, a landing page, a deck, an email — is either measured (and
sourced) or labeled a target. That is the difference between marketing and slop,
and it is the difference between a customer who stays and a refund.
