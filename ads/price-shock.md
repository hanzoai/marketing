# Campaign — Price Shock ("$4.90 first month — first 1,000 only")

**Hook:** "$4.90 first month. First 1,000 only."
**Audience:** warm list (waitlist email), retargeting, launch traffic.
**Phase:** 1 (launch promo).
**True claims allowed:** Pro is $49; 90% off first month = $4.90; cap = first
1,000 (server-enforced); month 2 reverts to $49. **Every claim here is real
arithmetic + a real cap — this is the one campaign where the number IS the
message.**

## Variant A — short
> $4.90 first month. Hanzo Pro.
> 90% off — first 1,000 only. Then $49. The card's five bucks; the cloud's real.

## Variant B — social (scarcity)
> Hanzo Pro is $49/mo. For the first 1,000 people, the first month is **$4.90.**
> That's ninety percent off, one time, capped at a thousand, counting down live.
> When it's gone, it's gone. [N of 1,000 claimed]

## Variant C — retargeting the waitlist
> You're on the list. Here's your jump.
> Waitlist members get first claim on the $4.90 first month — 90% off Pro, before
> anyone else. 1,000 codes. Ranked by your spot. Claim yours.

*(Ties to the waitlist-first allocation in `discounts.md`.)*

## Variant D — the absurd-number angle
> A full AI cloud for the price of a coffee. First month, $4.90.
> Not a trial that nags you. Pro, actually on, for less than your latte.
> First 1,000. Then it's $49 like everyone else.

## Variant E — countdown / urgency (late-promo)
> Almost gone: [N of 1,000] claimed.
> $4.90 first month of Hanzo Pro disappears at 1,000. After that, $49. Last calls.

## Creative concept (assets via hanzoai/studio)
- Big, dumb, beautiful **"$4.90"** with a strikethrough **$49** — the whole ad.
- A live **"[N] / 1,000 claimed"** counter (real, from the commerce redemption
  counter) — scarcity you can watch.
- Coffee cup next to the price for scale ("less than this").

## Guardrails (non-negotiable)
- **The cap is real and server-enforced.** Never run "first 1,000" copy if the
  atomic redemption counter isn't live (`[LANDING]`). A "first 1,000" that
  silently becomes 5,000 is fraud and kills the mechanic.
- **The countdown number must be truthful and live** — read from commerce, never
  a hardcoded fake-scarcity number.
- **"Then $49" must be stated** — no dark-pattern surprise on month 2. The revert
  is disclosed in every long variant.

## Channel note
Highest ROI on **warm-list retargeting + waitlist email** (via `notify`). This is
the conversion campaign that the one-binary campaign sets up. Unique promo codes
per channel/sponsor for clean CAC attribution (see `analysis/channels.md`).
