# The Business Checklist

The founder GTM curriculum: the ordered steps an org completes to go from a blank
page to a fundraise, each mapped to the Hanzo product that does the job and a
checkable done-criterion.

This document is the human-readable rendering **and the schema documentation**
for [`checklist.yaml`](./checklist.yaml). The YAML is the machine-readable
contract consumed by the `/v1/guide` engine.

---

## Schema

`checklist.yaml` is the single source of truth. Its schema:

| Field | Type | Meaning |
|---|---|---|
| `schema_version` | int | Schema version. Bump only on a breaking change. Current: **1**. |
| `curriculum` | string (kebab-case) | Curriculum id. Current: `founder-gtm`. |
| `title` | string | Human title. |
| `description` | string | One-paragraph summary. |
| `stages[]` | ordered list | Top-level grouping, walked in order. |

Each **stage**:

| Field | Type | Meaning |
|---|---|---|
| `id` | string (kebab-case, unique) | Stable stage id. |
| `title` | string | Short label. |
| `steps[]` | ordered list | The stage's steps, walked in order. |

Each **step**:

| Field | Type | Meaning |
|---|---|---|
| `id` | string (kebab-case, **unique across the whole file**) | **Stable** id. The engine keys per-org progress on it. |
| `title` | string | Short imperative label. |
| `why` | string | Why the step matters. |
| `how_on_hanzo` | object `{ product, route }` | Which Hanzo product does the job, and its route. `route` is `""` when the step is off-product (e.g. a deck). |
| `done_criteria` | string | An observable, checkable completion condition. |
| `depends_on` | list of step ids | Prerequisite step ids (may be empty). Forms a DAG. |

### Contract rules (do not break)

1. **IDs are stable.** Progress is keyed by `id`. Renaming an id orphans every
   org's progress on that step. Add steps; never repurpose an id.
2. **IDs are kebab-case and globally unique** across all steps in the file.
3. **`depends_on` is a DAG** — every referenced id must exist and there are no
   cycles. (Both are checked in CI; see below.)
4. **`how_on_hanzo` has exactly two keys**, `product` and `route`.
5. **`schema_version` gates breaking changes.** Additive fields do not require a
   bump; renaming/removing fields or changing meaning does.

### Validation

The invariants above are machine-checked. From the repo root:

```bash
python3 tools/validate_checklist.py
```

It fails loudly on: invalid YAML, a non-kebab or duplicate id, a missing required
field, a `how_on_hanzo` with the wrong keys, an unresolved `depends_on`, or a
dependency cycle.

---

## The curriculum

Ten stages, 27 steps. Rendered from `checklist.yaml` — the YAML is authoritative
if this drifts.

### 1. Positioning
- **define-icp** — Define the ideal customer profile. *(Analytics · `/v1/analytics`)*
- **craft-positioning** — Write the one-sentence positioning. *(Studio · `studio.hanzo.ai`)*
- **define-offer** — Define the core offer. *(Studio · `studio.hanzo.ai`)*

### 2. Landing & signup
- **build-landing** — Build the landing page. *(Studio · `studio.hanzo.ai`)*
- **setup-signup** — Wire public free signup. *(IAM · `/iam`)*

### 3. Analytics foundation
- **install-tracker** — Install event capture. *(Tracker · `/v1/tracker`)*
- **define-analytics-goals** — Define analytics goals. *(Analytics · `/v1/analytics`)*
- **setup-insights** — Stand up the testing engine. *(Insights · feature flags)*

### 4. Waitlist & points
- **launch-waitlist** — Launch the gated waitlist. *(Console · `app.hanzo.ai`)*
- **setup-points-ledger** — Enable the points ledger. *(Tracker · `/v1/tracker`)*
- **run-access-waves** — Run controlled access waves. *(Analytics · `/v1/analytics`)*

### 5. Email
- **wire-transactional-email** — Wire lifecycle email. *(Tracker · `/v1/tracker`)*
- **build-nurture-sequence** — Build the waitlist nurture sequence. *(Studio · `studio.hanzo.ai`)*
- **test-email-subjects** — A/B test subject lines. *(Insights · feature flags)*

### 6. Paid acquisition
- **define-campaign-structure** — Define the campaign hierarchy. *(Analytics · `/v1/analytics`)*
- **launch-first-1000-promo** — Launch the First-1000 promo. *(Console · `app.hanzo.ai`)*
- **launch-cold-prospecting** — Launch cold prospecting. *(Analytics · `/v1/analytics`)*

### 7. Retargeting & lookalikes
- **export-conversion-events** — Export conversion events to ad platforms. *(Tracker · `/v1/tracker`)*
- **build-retargeting-audiences** — Build retargeting audiences. *(Tracker · `/v1/tracker`)*
- **build-lookalikes** — Build lookalike audiences. *(Analytics · `/v1/analytics`)*

### 8. Referral & node growth
- **launch-referral-program** — Launch the referral program. *(Tracker · `/v1/tracker`)*
- **amplify-node-running** — Promote node-running as the fast lane. *(hanzod)*

### 9. Content engine
- **setup-content-calendar** — Set up the content calendar. *(Studio · `studio.hanzo.ai`)*
- **produce-studio-content** — Produce channel content in Studio. *(Studio · `studio.hanzo.ai`)*

### 10. Fundraise
- **assemble-metrics-deck** — Assemble the metrics deck. *(Analytics · `/v1/analytics`)*
- **build-data-room** — Build the data room. *(Analytics · `/v1/analytics`)*
- **run-raise** — Run the raise. *(Analytics · `/v1/analytics`)*

---

## How this connects to the rest of the repo

- **`GTM.md`** — the phase strategy this curriculum operationalizes.
- **`GUIDE.md`** — the tactical how-to behind many steps (campaign structure,
  retargeting, testing).
- **`discounts.md`** — the promo enforced by `launch-first-1000-promo`.
- **`analysis/`** — where the measured results of each step's experiments land.
