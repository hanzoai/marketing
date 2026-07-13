# Discounts & Promotions

The launch promo, specified against the **real plans** so finance can model it and
engineering can enforce it. One promo is live at launch; this doc is the single
source of truth for its rules.

## Plans (list price)

| Plan | Price / month | Billing unit |
|---|---|---|
| Developer | **$0** (free) | per user |
| Pro | **$49** | per user |
| Max | **$200** | per user |
| Team | **$199** | per seat |

Prices are the current published plans. If they change, update this table and
re-run the revenue math below — do not let this doc drift from the pricing page.

---

## Launch promo — "First 1,000"

> **90% off your first month.** First 1,000 paying users. Pro, Max, or Team.

### Eligibility

- **Who:** any org converting a Developer/waitlist account to a **paid** plan
  (Pro, Max, or Team) for the first time.
- **When:** from launch until **either** 1,000 redemptions **or** the promo end
  date, whichever comes first. The counter is hard — redemption 1,001 is
  declined automatically.
- **What it covers:** exactly the **first paid month**. Month 2 renews at list
  price. This is disclosed at checkout — no silent snap-back.
- **Free plan excluded:** Developer is already $0; there is nothing to discount.

### Discount by plan

| Plan | List | User pays month 1 | Discount value |
|---|---|---|---|
| Pro | $49 | **$4.90** | $44.10 |
| Max | $200 | **$20.00** | $180.00 |
| Team (per seat) | $199 | **$19.90 / seat** | $179.10 / seat |

For Team, the 90% applies to seats **purchased during the promo window**, capped
(see abuse guards) so a single org can't absorb a large share of the promo pool.

### Stacking rules

**One monetary discount at a time. Promos never stack.** Exactly one way to price
a first month.

- **Promo + referral points:** allowed — they are different currencies. Points
  move you up the access queue (see `GTM.md`); the promo discounts your bill.
  They never combine into a larger *monetary* discount.
- **Promo + another promo/coupon:** not allowed. The system applies the single
  best-for-the-user discount and rejects the rest.
- **Promo + annual/committed pricing:** not allowed in the same term. The user
  picks the promo (month 1) *or* committed pricing, not both.
- **Promo + Enterprise:** not applicable. Enterprise is contracted separately.

---

## Abuse guards

The promo and the points ledger share one adversary: someone spinning up fake
identities to farm value. Guards are enforced at redemption/award time, server-side.

- **One redemption per verified org.** Verification = confirmed email on a
  non-disposable domain **plus** a valid payment method. Disposable-domain and
  duplicate-card signals block the second redemption.
- **Payment instrument fingerprint.** The same card/instrument can redeem once.
  This is the hard stop against multi-account farming.
- **Team seat cap.** A single org's promo covers at most a fixed seat count
  (default **10** seats) at the promo rate; seats beyond that bill at list. This
  caps worst-case exposure per org.
- **Referral points fire on activation, not signup.** A referred account earns
  its referrer 10 points only after the referred org performs a real first
  action (`/v1/tracker` activation event). Dead invites earn nothing.
- **Share dedup.** Share points (2) are deduped per destination per account;
  re-clicking your own link does not compound.
- **Node points require sustained heartbeat.** The 25-point node award needs a
  minimum uptime window, not a single ping. A node that connects and vanishes
  earns nothing.
- **Velocity + anomaly review.** Redemption and point-award rates are monitored
  in `/v1/analytics`; anomalous spikes (many redemptions from one ASN/device
  cluster) are held for review, not auto-granted.

All guards are enforced in the promo/points service, never trusted from the
client.

---

## Revenue-impact math

The promo forgoes revenue for **one month only** — the acquisition cost is
bounded and known up front. All figures below are **illustrative scenarios**
built from list prices, not forecasts. Actuals land in `analysis/` once the
promo cohort exists.

**Per-redemption forgone revenue (month 1):** the "discount value" column above —
$44.10 (Pro), $180 (Max), $179.10 (Team seat).

**Worst / mixed / best case for a full 1,000-redemption pool** (single-seat
assumption for Team to bound it; seat cap makes true Team exposure lower):

| Scenario (plan mix) | Month-1 forgone revenue | Notes |
|---|---|---|
| All Pro (1,000 × $44.10) | **$44,100** | Cheapest to run; likely the bulk of the mix |
| Mixed (700 Pro / 200 Team / 100 Max) | **$95,190** | 700×44.10 + 200×179.10 + 100×180 |
| All Max (1,000 × $180) | **$180,000** | Absolute ceiling on month-1 exposure |

**Reading it as CAC.** Month-1 forgone revenue ÷ promo users = effective
discount-driven CAC:

- All-Pro: **$44.10 / user**
- Mixed: **$95.19 / user**
- All-Max: **$180.00 / user**

This is only worth it if promo users **stay**. Break-even in gross-margin months
after month 1:

- A Pro user who stays month 2 already returns $49 at list — the $44.10 discount
  is recovered inside the second paid month if they retain.
- The promo is **profitable iff** promo-cohort retention clears the Phase 1 exit
  gate in `GTM.md` (month-2 retention ≥ 60% TARGET). Below the kill line
  (< 30% month-2 retention) the promo is buying churn and must pause.

**What we will actually measure** (in `analysis/`, not assumed here):
- Realized plan mix of the 1,000 redemptions.
- Promo-cohort month-2 / month-3 retention vs. non-promo cohort.
- Blended CAC including the discount, compared to measured LTV.
- Net revenue effect = list revenue retained from surviving promo users −
  month-1 forgone revenue.
