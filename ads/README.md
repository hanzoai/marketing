# Ads

Concept briefs for paid creative. A brief is the spec a designer/copywriter (or
Studio workflow) builds from, and the record of what claim each ad makes.

## The honesty rule (non-negotiable)

Every claim in every ad is **measured-and-sourced** or **clearly a target**.

- No invented benchmarks ("10x faster") unless measured, sourced, and current.
- No fake or borrowed logos, testimonials, or social proof.
- No implied capability the product doesn't ship today.
- Promo claims must match `discounts.md` exactly (offer, eligibility, expiry).

A brief that can't fill the **Claims** table with real or clearly-labeled-target
lines doesn't ship.

## Workflow

1. Copy `brief-template.md`, name it by concept, e.g. `own-your-node.md`.
2. Fill it. The **Claims** table is mandatory and must pass the honesty rule.
3. Produce assets in Studio (`studio.hanzo.ai`).
4. Ship variants behind Insights flags; judge on `/v1/analytics` goals
   (see `GUIDE.md`).
5. Record outcomes in `analysis/`.

## Files

- `brief-template.md` — the concept brief template.
- `own-your-node.md` — example brief (viral node expansion, Phase 2).
- `first-1000.md` — example brief (launch promo, Phase 1).
