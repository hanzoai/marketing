# Analysis

Where **measured** results live. Targets belong in `GTM.md`; the numbers that
replace them belong here.

## Rules

- **Measured or labeled.** Every figure in an analysis is pulled from
  `/v1/analytics` (which reads `/v1/tracker` capture) or is explicitly labeled an
  estimate with its assumption. No invented numbers.
- **Cite the source.** Each metric names the query/goal it came from so anyone
  can reproduce it.
- **One analysis per wave/campaign/phase.** Copy `what-worked-template.md`,
  fill it, name it by what it covers, e.g. `phase-1-first-1000-promo.md` or
  `2026-q3-cold-meta.md`.
- **A phase's next spend does not open until its analysis is filled** with
  measured numbers (see `GTM.md` → Instrumentation contract).

## Files

- `what-worked-template.md` — the what-worked analysis (cohort, channel, CAC/LTV).
- Filled analyses land alongside it, one per wave/campaign/phase.
