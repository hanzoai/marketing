# What worked — <WAVE / CAMPAIGN / PHASE NAME>

> Copy this file, fill every `<...>`, and delete this line. Every number must be
> pulled from `/v1/analytics` (cite the goal/query) or labeled an estimate with
> its assumption. No invented numbers.

- **Period:** `<start>` → `<end>`
- **Scope:** `<which phase / campaign / access wave>`
- **Spend:** `$<total>` (`<breakdown by channel>`)
- **Source of truth:** `/v1/analytics` goals: `<list the goal ids used>`

---

## 1. Funnel

Pull each stage from the analytics goal named in the header.

| Stage | Count | Rate vs. prior | Goal / query |
|---|---|---|---|
| Visitors | `<n>` | — | `<query>` |
| Signups | `<n>` | `<%>` | `signup` |
| Activated | `<n>` | `<%>` | `activate` |
| Added payment | `<n>` | `<%>` | `add_payment` |
| Purchased | `<n>` | `<%>` | `purchase` |

**Read:** `<where is the biggest leak, in one sentence>`

---

## 2. Cohort retention

Cohort by signup week (or by wave). Retention = still-active at week N.

| Cohort | Size | W1 | W2 | W4 | W8 |
|---|---|---|---|---|---|
| `<cohort>` | `<n>` | `<%>` | `<%>` | `<%>` | `<%>` |

Compare promo vs. non-promo cohorts where relevant (see `discounts.md`).

**Read:** `<is retention above/below the GTM target and kill line?>`

---

## 3. Channel attribution

One row per channel. CAC = channel spend ÷ channel conversions (name which goal).

| Channel | Spend | Signups | Purchases | CAC (per purchase) | Notes |
|---|---|---|---|---|---|
| `<channel>` | `$<x>` | `<n>` | `<n>` | `$<x>` | `<x>` |

**Read:** `<which channel to scale, which to cut>`

---

## 4. CAC / LTV

State the assumptions before the numbers — LTV depends on a retention/margin
assumption that must be explicit.

- **Assumptions:** gross margin `<%>`; churn / expected lifetime `<n months>`
  (source: `<cohort table above / measured>`).
- **Blended CAC:** `$<x>` (total spend ÷ new paying orgs).
- **LTV:** `$<x>` (`<formula, e.g. ARPU × margin × lifetime>`).
- **LTV:CAC:** `<x>:<y>`.

**Read against `GTM.md`:** `<does this clear the phase exit gate? breach the kill line?>`

---

## 5. Experiments

From Insights (feature flags), one row per test called this period.

| Test | Variants | Winner | Goal lift | Sample | Decision |
|---|---|---|---|---|---|
| `<test>` | `<A/B>` | `<A/B>` | `<%>` | `<n>` | keep / kill |

---

## 6. Decision

- **Keep doing:** `<...>`
- **Stop doing:** `<...>`
- **Next test:** `<one hypothesis, with the metric it moves>`
- **Phase gate:** `<met exit gate / hit kill criterion / continue>` (cite `GTM.md`)
