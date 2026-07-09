# Analysis — Waitlist / Email Phase (Phase 0)

**INTERNAL.** What drives activity in the waitlist/email phase, as testable
hypotheses, and exactly how we measure each in **Insights** `[LIVE product]` /
funnel-instrumentation `[LANDING]`. This is the measurement plane for Phase 0.
Nothing here is a result — these are the questions and the instrumentation to
answer them.

## The Phase-0 funnel (what we instrument)

```
land → join (Turnstile) → status page → {share, invite, follow, run-node}
     → referred-friend lands → referred-friend joins → … → activation (access opens)
```

Every arrow is an event. K-factor and activation conversion fall out of the
event graph; if the events aren't emitting, Phase 0 has no evidence and Phase 1
is blocked (the gating dependency in `GTM.md`).

## Events to instrument (Insights)

Canonical event names — one namespace, one schema. Emit from the waitlist widget
+ Base plugin; land in Insights.

| Event | Props | Answers |
|---|---|---|
| `waitlist_view` | `ref?`, `variant`, `source` (utm) | Top-of-funnel volume, share-link landings. |
| `waitlist_join` | `ref?`, `source`, `email_domain_class` | Signups/day; referred vs. cold. |
| `waitlist_join_blocked` | `reason` (turnstile/disposable) | Fraud/abuse pressure; blocklist efficacy. |
| `waitlist_status_view` | `rank`, `points`, `neighbors_ahead` | Do people come back to check rank? |
| `waitlist_share_click` | `channel` (x/linkedin/copy), `placement` | Share-rate by channel & placement. |
| `waitlist_invite_sent` | `count` | Invites-sent — the K-factor numerator input. |
| `waitlist_referral_converted` | `referrer_code` | Invite→join conversion — the K-factor multiplier. |
| `waitlist_social_follow` | `network` | Follow-loop conversion (owned audience growth). |
| `waitlist_node_action` | `attested` (bool) | Run-a-node intent; Phase-2 leading indicator. |
| `waitlist_leaderboard_view` | `own_rank` | Does the leaderboard drive return + sharing? |
| `email_drip_sent` / `_open` / `_click` | `sequence`, `step` | Drip cadence performance. |
| `activation` | `plan` (developer/pro/…), `days_on_list` | Waitlist→activation conversion — the Phase-1 gate. |

Derived metrics (compute in Insights, surface in the operator cockpit):
- **K-factor** = mean(`invite_sent.count`) × (`referral_converted` / `invite_sent`).
- **Share rate** = `share_click` distinct users / active users.
- **Return rate** = repeat `status_view` / joiners.
- **Activation conversion** = `activation` / eligible joiners.

## Hypotheses to test (and how)

### H1 — Share-loop placement drives share rate
*Hypothesis:* share CTA on the **status page immediately after join** (peak
dopamine, "you're #N, skip ahead") out-shares a share CTA buried in a menu.
*Test:* A/B `placement` = `post_join_hero` vs. `status_footer` vs. `leaderboard_inline`.
*Measure:* `waitlist_share_click` rate by `placement`; downstream
`referral_converted` per placement (shares are worthless if they don't convert).
*Decision:* ship the placement with the best *converted-referral* rate, not the
best raw click rate.

### H2 — Points weighting changes behavior mix
*Hypothesis:* the 10/2/15/25 weights (referral/share/follow/node) steer effort.
Raising referral relative to share pushes users from cheap shares to high-value
invites.
*Test:* config-driven weights (server is source of truth — no redeploy). A/B two
weight vectors on new cohorts.
*Measure:* mix of `referral_converted` vs. `share_click` vs. `node_action` per
vector; net K-factor.
*Decision:* pick the vector that maximizes K-factor without cratering total
activity. **Guard:** don't over-weight node (25) before node-proof lands, or you
incentivize un-attested claims.

### H3 — Leaderboard visibility drives return + virality
*Hypothesis:* showing rank + "N neighbors ahead" (neighborhood-view, to 10M)
increases return visits and shares (competitive drive).
*Test:* leaderboard/neighborhood-view shown vs. hidden (or top-N only vs. full
neighborhood).
*Measure:* `leaderboard_view` → `status_view` return rate; shares per viewer.
*Decision:* keep the variant with higher return + share; watch for
discouragement (very-low-rank users churning — segment by `own_rank`).

### H4 — Email drip cadence drives activation, not fatigue
*Hypothesis:* a 3-touch drip (welcome / "climb the list" / "access opening")
beats both silence and a daily blast.
*Test:* cadence A (3 touches over launch window) vs. B (weekly) vs. C (control,
transactional only). Runs on `hanzoai/notify` + `hanzoai/auto` sequences.
*Measure:* `email_drip_open`/`click` by step; `activation` by cadence; unsub rate
as the fatigue guard.
*Decision:* max activation at acceptable unsub. **Cap** any cadence that pushes
unsub above threshold.

### H5 — The run-a-node hook recruits real operators, not just points-farmers
*Hypothesis:* framing "run a node, jump the line + earn later" converts a
meaningful slice into Phase-2 operators.
*Test:* node-action framing variants (line-jump only vs. line-jump + future
earnings copy).
*Measure:* `waitlist_node_action` rate; `attested=true` share once node-proof
lands; Phase-2 conversion of these users to online nodes.
*Decision:* the framing with the highest *attested-node* conversion, not raw
clicks.

### H6 — Referred friends activate better than cold signups
*Hypothesis:* referral is not just cheap growth — referred users retain/activate
better (warm intro).
*Test:* segment `activation` and later retention by `source` = referral vs. cold.
*Measure:* activation conversion + downstream paid-retention by source.
*Decision:* if referred >> cold, over-invest in the referral loop (weights,
placement) vs. paid — informs the Phase-0→1 spend gate.

## Reporting

- **Daily** (Guide daily process): signups/day, K-factor trend, share rate, top
  referrers, blocked-join rate. Surfaced in the operator cockpit `[LANDING]`;
  Slack outlier alerts via `notify`.
- **Weekly cohort**: join-week cohorts by source → return, share, activation.
- **The one chart that gates Phase 1**: K-factor trend + activation conversion.
  Until both are measured and healthy, no paid spend (stated in `GTM.md`).

## Honest instrumentation status

- `[LIVE]` widget/plugin emit the user actions (join/share/invite/referral) as
  product behavior.
- `[LANDING]` the Insights event pipeline wiring (canonical schema above) and the
  derived-metric dashboards. **This is the Phase-0→1 gating build.**
- `[LANDING]` operator cockpit as the read/alert surface.
- Do not report a metric we aren't actually emitting. If it's not in Insights,
  it's not a number — it's a guess.
