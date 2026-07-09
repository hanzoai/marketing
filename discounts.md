# Promo & Discount Playbook

**INTERNAL ONLY.** Every promo specced against the real plans and the real
`hanzoai/commerce` billing engine (prices in cents; coupon processors in
checkout `[LIVE]`; capped-redemption flow `[LANDING]`). Every promo carries a
cap, a fraud guard, and an expected CAC impact. No promo ships without
server-enforced limits — a discount you can't cap is a discount you can't afford.

Plan reference: Developer **$0** · Pro **$49** · Max **$200** · Team **$199**.

Anti-fraud primitives available from the waitlist/referral systems (reuse, do
not reinvent):
- **Turnstile** gate on claim (already on waitlist join).
- **Disposable-email blocklist** (already in `base/plugins/waitlist` + mock-api).
- **hanzo.id identity** — one identity, one redemption; org from JWT `owner`.
- **Payment-method fingerprint** (commerce) — one card family, one first-month promo.
- **Referral conversion = server-side only** (points credited on the referred
  join event, never client-asserted).

---

## 1. Launch promo — 90% off first month, first 1,000 users

**The flagship.** Early-bird scarcity engineered to be shared.

| Plan | List | First month (90% off) |
|---|---|---|
| Pro | $49 | **$4.90** ← hero |
| Max | $200 | **$20.00** |
| Team | $199 | **$19.90** |

**Mechanics**
- Coupon in `hanzoai/commerce`: `percent_off = 90`, `duration = first_month_only`,
  auto-reverts to list at month 2.
- **Cap = 1,000 redemptions**, enforced by an **atomic server-side counter** in
  commerce (not a client check, not a config guess). When the counter hits 1,000
  the code is dead — no race, no overshoot.
- **Live countdown on the site**: "N of 1,000 claimed," read from the redemption
  counter. Scarcity is the mechanic; the number must be truthful and live.
- **Waitlist-first allocation**: offer the 1,000 to the waitlist by rank order
  (referrers first) before opening remainder to paid channels. Makes waitlist
  position pay off and rewards the K-factor drivers.

**Fraud guard**
- One redemption per hanzo.id identity **and** per payment-method fingerprint.
- Turnstile at claim; disposable-email domains excluded (reuse waitlist blocklist).
- First-month only + card required up front → filters tourists better than a free
  trial; a real card at $4.90 is a stronger intent signal than $0.

**Expected CAC impact** (ESTIMATE-TO-VALIDATE)
- Effective first-month discount cost = $44.10 (Pro) × up to 1,000 = **≤ $44,100
  max exposure** — a hard, known ceiling. That is the entire promo budget, capped.
- The bet: month-2 retention on a $4.90-acquired, card-on-file Pro user beats a
  free-trial cohort. **Success = promo month-2 retention ≥ organic free→paid
  retention.** If it doesn't clear that, tighten to waitlist-only (kill-criterion
  in `GTM.md`).

---

## 2. Referral credits (double-sided)

Extends the Phase-0 waitlist referral into paid credits post-launch.

**Mechanics**
- Waitlist phase: referral (converted) = **10 points** `[LIVE]`.
- Post-launch: **points → account credits** `[LANDING]`. Proposed: referrer and
  referred each get a credit on the referred's first paid month (double-sided,
  the Guide's "gamified double-sided referral system"). Propose **$20 credit each**
  on referred's first Pro payment (to validate against margin).
- Credits spend on usage (Pro/Max metered), never cash-out (avoids money-transmission).

**Cap**
- Per-referrer monthly credit cap (e.g. 10 successful referrals/mo) to bound
  exposure and deter farming.

**Fraud guard**
- Credit issues **only on the referred user's first successful paid charge**
  (server-side event), not on signup — kills self-referral and fake-signup farms.
- Same identity + payment-fingerprint dedupe as the launch promo.

**Expected CAC impact** (ESTIMATE-TO-VALIDATE)
- CAC = credits issued (both sides) / net-new paid referred users. Only "spent"
  when a real paying customer arrives → structurally CAC-efficient vs. paid ads.

---

## 3. Node-operator credits

The Phase-2 bridge: reward operators who expand our compute.

**Mechanics**
- Waitlist: run-a-node = **25 points** (jump the line) `[LIVE config]`.
- Post-launch: node points → credits `[LANDING]`; then **x402 / wallet earnings
  for compute contributed** `[ROADMAP]` (the durable rail — earnings, not just
  discounts).
- GPU / TEE-CC nodes earn a premium multiplier (premium supply tier).

**Cap**
- Credits/earnings capped at the **measured value of capacity contributed** —
  never pay out more than the node saved us in cloud cost. This is the economic
  guard-rail (Phase-2 kill-criterion).

**Fraud guard**
- Requires hanzod → identity **node-proof** `[LANDING]` (real, attested capacity),
  not self-report. Until node-proof lands, treat node points as self-attested and
  **rate-limited**, credits withheld.
- Quality/SLO gate: a node that fails latency/uptime earns nothing.

**Expected CAC impact** (ESTIMATE-TO-VALIDATE)
- This is negative-CAC by design: the "cost" (credits/earnings) is paid in the
  currency of capacity the operator *gave* us. Every retained operator = CAC we
  didn't pay + capex we didn't spend.

---

## 4. Annual-plan discount

Standard prepay discount to pull LTV forward and cut churn.

**Mechanics**
- Annual = **~2 months free** (pay for 10, get 12) — i.e. Pro annual ≈ **$490/yr**
  vs. $588 monthly. Commerce already supports yearly plans (proration, trials).
- Offered at checkout and as a lifecycle upsell (Guide: "transactional email
  CTAs, upsell").

**Cap** — none needed; it's a pricing tier, not a scarcity promo.

**Fraud guard** — standard billing; refund/proration rules on downgrade.

**Expected impact** (ESTIMATE-TO-VALIDATE)
- Improves cash-flow + reduces monthly churn surface. Stackable with the launch
  promo? **No** — launch promo is first-month-only monthly; annual is a separate
  path. Don't stack 90%-off with annual (margin hole).

---

## 5. Techstars-portfolio deal

Hanzo AI is Techstars '17 — leverage the network for high-quality B2B logos and
Phase-3 recursive-org referrals.

**Options (propose; CTO picks one)**
- **Option A — Free Pro for 1 year** for verified Techstars-portfolio companies.
  Simple, generous, high goodwill. Cost = foregone Pro revenue on a cohort that
  likely wasn't going to pay list yet; upside = logos, case studies, referrals.
- **Option B — Free Max for 6 months, then 50% off for 6.** Higher-touch tier,
  shorter runway, softer landing to paid.
- **Option C — $0 platform + revenue-share** — they build on Hanzo free, we take
  the recursive-org referral cut when *their* users arrive (Phase-3 aligned). Best
  strategic fit with the flywheel; needs the recursive-org rail `[ROADMAP]`.

**Recommendation:** **Option A now** (simple, ships on existing commerce coupon),
migrate the cohort to **Option C** when the recursive-org rail lands.

**Cap** — verified portfolio list only; per-company one deal.

**Fraud guard** — manual verification against Techstars portfolio + domain check.

**Expected impact** — not a CAC play; a **logo + referral-seed** play. Measure by
referred-orgs and case studies produced, not direct revenue.

---

## 6. Edu / OSS-maintainer free tiers

Feeds Phase-3: OSS maintainers are the authors who'll earn the 25% share; students
are the next cohort of builders.

**Mechanics**
- **OSS maintainers**: free Pro (or Max) for maintainers of qualifying public
  repos (stars/activity threshold). Ties directly to the "your code earns 25%"
  narrative — give them the tools free, they bring projects + users.
- **Edu**: free Pro with a verified `.edu` / student credential.

**Cap** — qualification-gated (repo threshold / edu verification), annual renewal.

**Fraud guard**
- OSS: verify repo ownership (GitHub/GitLab OAuth) + activity threshold, not
  self-claim.
- Edu: SheerID-style verification or `.edu` + active-enrollment check. Disposable
  domains excluded.

**Expected impact** — pipeline, not revenue. Measure by conversion of edu/OSS free
users into paid *or* into node-operators/authors (the flywheel roles).

---

## Global rules

1. **Every promo is server-capped.** No client-trusted limits. Ever.
2. **Card-on-file beats free** for intent — the $4.90 promo requires a card;
   prefer discounted-paid over free-trial where retention matters.
3. **Never stack scarcity promos** (90%-off + annual + referral credit on the same
   charge = margin hole). One promo per charge.
4. **Reuse the anti-fraud stack** (Turnstile, disposable-email blocklist, identity
   + payment-fingerprint dedupe, server-side conversion events). Do not build new
   fraud logic per promo.
5. **Measure retention, not redemption.** A redeemed code that churns in month 2
   is a loss. Every promo's real KPI is the retained cohort (see `GTM.md`
   kill-criteria).
