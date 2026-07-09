# Analysis — Channel Plan (Phase 1)

**INTERNAL.** Channel-by-channel plan for paid + launch. **We have no spend data
yet.** Every CPM/CAC/conversion number below is an **ESTIMATE-TO-VALIDATE** — a
starting hypothesis and a range to test, not a result. The value of this doc is
the *framework* for how we'll learn per channel, not the numbers. When Insights
has real attribution, we replace estimates with measured values and this doc
becomes a scoreboard.

## How we judge every channel (one rubric)

For each channel we measure, in Insights + commerce:
- **CAC** = channel spend / net-new paid users attributed.
- **LTV:CAC** — scale only channels ≥ 3:1 (target-to-validate); kill < 1.5:1.
- **Payback period** — months of margin to recover CAC.
- **Promo redemption + month-2 retention** by channel — the tourist filter.
- **Assisted vs. last-touch** — don't over-credit the closer or the opener.

Ranges below are labelled **[EST]**. Sources for the ranges are public
benchmarks for dev/B2B SaaS, not Hanzo data. Treat as priors to update.

---

## X / Twitter — dev audience

**Role:** the one-binary story's native home; founder-led organic + paid
amplification of proof (0.245MB/tenant, 1B/20-nodes).

- **[EST] CPM:** $6–$12 (dev/tech targeting).
- **[EST] CTR:** 0.5–1.5% on strong dev creative.
- **[EST] CAC (paid):** $40–$120 to a $49 Pro — *tight*; this channel likely wins
  on **organic + retargeting**, not cold paid prospecting.
- **Plan:** organic founder threads (free) → retarget engagers + waitlist list
  with the $4.90 promo. Cold paid only after retargeting proves out.
- **Runs on:** `hanzoai/social` (organic 28-ch) `[LIVE]` + social paid module
  `[LANDING]` + `hanzoai/ads` `[ROADMAP]` for automation.
- **Kill signal:** cold-prospecting CAC > 1-month Pro with no retention lift →
  drop cold, keep retargeting only.

## Hacker News — launch (organic)

**Role:** credibility + a spike of exactly the right audience. Not a paid channel.

- **Cost:** $0 (organic). Cost is *reputational* — HN punishes marketing spin;
  reward is enormous if the Show HN is technically honest.
- **[EST] outcome:** front-page Show HN → thousands of high-intent devs in a day;
  unpredictable, not repeatable, not a plan you can budget on.
- **Plan:** one well-timed **Show HN** on the one-binary + measured claims; founder
  answers every comment (Guide: AMA energy). No promo hard-sell in the post; link
  to a clean landing.
- **Runs on:** landing page + Insights attribution (utm `hn`).
- **Kill signal:** n/a (organic, one-shot). Don't fake it; a detected astroturf
  attempt on HN is net-negative.

## Product Hunt — coordinated launch

**Role:** launch-day concentration; the waitlist is the upvote/hunter army.

- **Cost:** $0 direct; cost = coordination + the waitlist goodwill you spend
  mobilizing it.
- **[EST] outcome:** #1-3 of the day → a few thousand signups + backlinks +
  newsletter pickup. Quality lower than HN, volume decent.
- **Plan:** mobilize the waitlist (email via `notify`) to hunt/upvote at launch;
  offer the launch promo to PH traffic; assets from `hanzoai/studio`.
- **Runs on:** notify (list mobilization) + landing (utm `ph`) + commerce promo.
- **Kill signal:** if PH-sourced users show far worse promo retention than
  waitlist/HN, don't repeat the mobilization spend (goodwill is finite).

## Dev-YouTube — sponsorships

**Role:** buyer-intent, high-trust; mid-roll in AI/infra channels (Guide:
"sponsored links in buyer-intent YouTube videos").

- **[EST] CPM (sponsorship):** $15–$50 effective (varies wildly by channel size
  + integration depth).
- **[EST] CAC:** $60–$200 — high variance; the *right* mid-size channel with a
  dev audience can beat this, a mismatched big channel burns.
- **Plan:** start with **1–2 mid-size, on-topic channels** (AI infra, self-hosting,
  Go). Unique promo code per sponsor for clean attribution. Scale only proven ones.
- **Runs on:** per-sponsor commerce promo code (attribution) + Insights.
- **Kill signal:** a sponsor's code CAC > 3× blended → don't renew; reallocate.

## Retargeting — the warm list (highest ROI)

**Role:** the best audience we have — the waitlist email list + site visitors.
This is where the $4.90 promo does its heaviest lifting.

- **[EST] CAC:** **lowest of all channels** — retargeting warm intent typically
  fractions of cold CAC. This is the channel to lean on hardest at launch.
- **Plan:** email the waitlist (via `notify`, ranked-first promo allocation) +
  retarget site visitors on X/Meta with the promo countdown. Sequenced drip
  (`hanzoai/auto`), not a single blast (test cadence — H4 in `waitlist-phase.md`).
- **Runs on:** notify (email) `[LIVE lib]` + social paid retargeting `[LANDING]`
  + commerce promo + Insights attribution.
- **Kill signal:** rare — if even warm-list retargeting can't clear LTV:CAC, the
  *offer/product-fit* is the problem, not the channel. That's a Phase-0-back signal.

---

## Channel sequencing (Phase 1)

1. **Warm-list retargeting first** (lowest CAC, uses the asset we already built in
   Phase 0). Prove the promo converts + retains here.
2. **Organic HN + PH launch** (free, high-quality) around the same window.
3. **X retargeting → X cold** only after retargeting proves out.
4. **YouTube sponsorships**, 1–2 channels, unique codes, scale winners.
5. **Cold paid prospecting last**, and only on channels with a proven retargeting
   base to lookalike from.

Budget rule (from `GTM.md`): start small per channel, **kill < 1.5:1 LTV:CAC
weekly**, scale only ≥ 3:1. No channel gets a defended budget.

## The honest caveat

All numbers here are **priors, not data.** The framework — CAC/LTV rubric,
per-channel unique-code attribution, retention-not-redemption KPI, kill/scale
thresholds — is what's real. The moment Insights + commerce attribution is wired,
this doc's estimates get replaced by measured values, channel by channel. Until
then, no one quotes these ranges as fact, internally or externally.
