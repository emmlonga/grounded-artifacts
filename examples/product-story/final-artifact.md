<!--
FREEZE HEADER (not rendered)
Public example: the final output of a workflow run on a synthetic test fixture (no real person or company).
Mode product-story · profile plain · budget 2 pages · writer: writing-v2 (frozen) · audits: Integrity and Audience, two rounds.
For publication, the fictional setting was generalized ("a retail bank"). See README.md in this folder.
-->
# Building an automatic savings feature

## The opportunity, and why then

In 2023, at a retail bank, our customers kept balances in their current account but moved their savings to other banks. Deposits per customer were flat for three quarters. Why then: instant-payment rails made moving money out effortless, so balances were leaving faster each month. I was the PM for the automatic savings feature that followed. I recommended what to leave out of the launch, and I designed the pilot with our data analyst. Compared with the rest of the base, customers in the pilot showed a clear lift in 90-day retention and growth in deposits per active user (directional).

Our research team had surfaced the need in exit interviews and a customer survey: people wanted to set money aside without opening a separate investment product. Competitors required a separate account; we could do it inside the current account.

## Vision, strategy and the trade-offs

Our head of product set the vision: savings that happen without a decision each time, through round-ups and a "safe to spend" balance. A "safe to spend" balance is the part of the balance not set aside. The link to the bank's strategy ran through the problem: stopping deposits leaving.

The first trade-off was mine, over the rewards tier: a bonus yield above a balance threshold. I recommended launching without it rather than with it, to aim to ship in one quarter. The steering committee approved it.

The second came from our engineering lead, who proposed using our payments partner's ledger instead of building our own. I agreed, and I owned the dependency risk in the roadmap.

## How the team built it, and my role

Five engineers, a designer and a data analyst made up the core team, with me as PM. I wrote the PRD and ran weekly prioritization.

With the data analyst, I designed a six-week pilot with 5% of customers before full launch, and we ran it. Pilot customers, the 5% who received the feature, were assigned at random.

## Stakeholders and the setback

The CFO worried that savings would cannibalize a fee-earning product. I agreed to report weekly on that product's balances during the pilot. Legal and compliance were consulted weekly.

The setback came in week 3, when a rounding bug double-counted round-ups for a subset of pilot customers. I paused the pilot for four days, we fixed the bug, and I wrote to the affected customers.

## Outcome, learnings and what I would do differently

Pilot customers showed a clear lift in 90-day retention compared with the rest of the base (directional; the exact figure is unavailable). That comparison covered the 90 days after the pilot started. During the pilot, deposits per active user also grew for pilot customers compared with the rest of the base (directional). The retention and deposit results describe pilot customers only. Separately, the fee-earning product the CFO worried about did not lose balances (directional).

Looking back, I would measure dependency risk earlier: our payments partner's ledger limited what we could change later. I would also define the success metric before the pilot, not during it.

With this story, I ask the panel to probe the trade-offs and the pilot in the deep dive.
