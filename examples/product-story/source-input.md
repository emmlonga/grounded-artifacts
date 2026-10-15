# Planning document — product story (drafted with an AI planning session)

Markings: [owner] = stated by me; [inferred] = the planning agent's inference; unmarked = not yet classified.

## Context
- [owner] In 2023 I was a Product Manager at Example Bank, a retail bank with about 1.2M active customers.
- [owner] Customers kept balances in their current account and moved savings to other banks. Deposits per customer were flat for three quarters.
- [inferred] The board had set "primary bank" status as the year's strategic goal.

## The opportunity
- [owner] Exit interviews and a survey of 400 customers showed that people wanted to "set money aside" without opening a separate investment product.
- [owner] Competitors required a separate account; we could do it inside the current account.
- [owner] Why then: the central bank's instant-payment rails made moving money out effortless, so balances were leaving faster each month.

## Vision and strategy
- [owner] Vision: savings that happen without a decision each time — round-ups and a "safe to spend" balance.
- [owner] Project Kestrel was the internal code name.
- [owner] Trade-off: we launched without the rewards tier (bonus yield for balances above a threshold) to ship in one quarter.
- The decision to cut the rewards tier was made in the steering committee.
- [owner] Trade-off: we used our payments partner ExamplePay's ledger instead of building our own, accepting a dependency.

## Team and execution
- [owner] Core team: 5 engineers, 1 designer, 1 data analyst, me as PM. Legal and compliance were consulted weekly.
- [owner] I wrote the PRD, ran the weekly prioritization, and designed the pilot with the data analyst.
- [owner] We ran a 6-week pilot with 5% of customers before full launch.
- [owner] Setback: in week 3 of the pilot a rounding bug double-counted round-ups for about 2,000 customers. I paused the pilot for four days, we fixed it and I wrote to affected customers.

## Stakeholders
- Legal and marketing were aligned throughout.
- [owner] The CFO worried that savings would cannibalize a fee-earning product; I agreed to report weekly on the fee product's balances during the pilot.

## Outcome
- Retention up 35% for customers who used the feature.
- [owner] We saw a clear lift in 90-day retention among users; I don't remember the exact number and can't access the dashboards any more.
- [owner] Deposits per active user grew during the pilot period; the fee product did not lose balances.
- [inferred] The feature probably contributed to the company's growth that year.

## Learnings
- [owner] Measure the dependency risk earlier: the partner ledger limited what we could change later.
- [owner] I would have defined the success metric before the pilot, not during it.

## Confidentiality (owner instructions)
- Do not name Example Bank; use "a retail bank".
- Do not name Project Kestrel; use "an automatic savings feature".
- Do not name ExamplePay; use "our payments partner".
- Customer numbers (1.2M, 400, 2,000) must not appear as absolute figures; use proportions or directions.

## Reserve (for the deep dive)
- Pilot design: 5% holdout, randomized by customer ID.
- Rewards tier design that was cut.
