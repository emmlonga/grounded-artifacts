# Grounding (excerpt): automatic savings feature

**Mode:** product-story · **Sources:** S1 `source-input.md` (agent-assisted planning document, not owner-reviewed) and OA, the owner's answers to the readiness questions (`what-the-workflow-changed.md`, §1) · **Line references** (`S1 l.n`) point to `source-input.md`.

Sections 4–9 of the grounding, as the draft received them. Sections 1–3 (sources, audience anchor, criteria mapping) and 10 (decisions for owner) are omitted. This run predates the story-frame layer: its claim classes, including MUST COMMUNICATE, were assigned in the grounding itself. Today that happens in pass B, against the story frame.

## 4. Claim classes

| ID | Class | Claim | Source |
|---|---|---|---|
| C1 | MUST COMMUNICATE | Customers kept balances in their current account but moved savings to other banks; deposits per customer were flat for three quarters. | S1 l.7 |
| C2 | MUST COMMUNICATE | Why then: instant-payment rails made moving money out effortless, so balances were leaving faster each month. | S1 l.13 |
| C3 | MUST INCLUDE | The research team surfaced the need in exit interviews and a customer survey: people wanted to set money aside without opening a separate investment product; competitors required a separate account, we could do it inside the current account. | OA Q1; S1 l.11–12 |
| C4 | MUST INCLUDE | The head of product set the vision: savings that happen without a decision each time, through round-ups and a "safe to spend" balance. | OA Q1; S1 l.16 |
| C5 | MUST INCLUDE | I recommended launching without the rewards tier (bonus yield above a balance threshold) to aim to ship in one quarter; the steering committee approved it. | OA Q2; S1 l.18 |
| C6 | MUST INCLUDE | The engineering lead proposed using our payments partner's ledger instead of building our own; I agreed and owned the dependency risk in the roadmap. | OA Q2; S1 l.20 |
| C7 | MUST INCLUDE | Core team: 5 engineers, 1 designer, 1 data analyst and me as PM. I wrote the PRD, ran weekly prioritization and designed the pilot with the data analyst. | S1 l.23–24; OA Q1 |
| C8 | MUST INCLUDE | We ran a six-week pilot with 5% of customers, assigned at random by customer ID, before full launch. | S1 l.25; OA Q3 |
| C9 | MUST INCLUDE | Setback: in week 3 a rounding bug double-counted round-ups for a subset of pilot customers; I paused the pilot for four days, we fixed it, and I wrote to affected customers. | S1 l.26 |
| C10 | MUST INCLUDE | The CFO worried savings would cannibalize a fee-earning product; I agreed to report weekly on that product's balances during the pilot. | S1 l.30; OA Q1 |
| C11 | MAY SAY | Legal and compliance were consulted weekly. | S1 l.23 |
| C12 | MUST INCLUDE | Measured against the rest of the base over the 90 days after the pilot started, pilot customers showed a clear lift in 90-day retention (directional; exact figure unavailable). | S1 l.34; OA Q3 |
| C13 | MUST INCLUDE | Deposits per active user grew for pilot customers versus the rest of the base during the pilot; the fee product did not lose balances. | S1 l.35; OA Q3 |
| C14 | MUST INCLUDE | Learning: measure dependency risk earlier; the partner ledger limited what we could change later. | S1 l.39 |
| C15 | MUST INCLUDE | Do differently: define the success metric before the pilot, not during it. | S1 l.40 |
| C16 | MUST PRESERVE | Problem-finding belongs to the research team and the vision to the head of product; the author's own actions are C5, C7, C10, agreeing to C6, and in C9 the pause and the customer letter; running the pilot (C8) and the fix (C9) stay "we". "We" is not upgraded to "I". | OA Q1 |
| C17 | MUST PRESERVE | Outcomes are directional, pilot vs rest of base, and are not attributed beyond the feature's users. | OA Q3; brief guardrail |
| C18 | MUST PRESERVE | "One quarter" is an aim; whether it was met is unknown. | OA Q6 |
| C19 | MUST NOT SAY | Any retention or outcome figure (e.g. "35%"). Alternative: C12 directional wording. | OA Q3 |
| C20 | MUST NOT SAY | Company-wide impact or contribution to company growth. Alternative: C12–C13, scoped to pilot customers. | Brief guardrail; S1 l.36 [inferred] |
| C21 | MUST NOT SAY | "Primary bank" as the strategic goal. Alternative: link to strategy through C1–C2 (stopping deposits leaving). | OA Q4 |
| C22 | MUST NOT SAY | Marketing was involved or legal and marketing were "aligned throughout". Alternative: C11. | OA Q5 |
| C23 | MUST NOT SAY | "I found the problem" / "my vision". Alternative: C3, C4 with the author's build role. | OA Q1 |
| C24 | MUST NOT SAY | That the launch shipped in one quarter, or that trade-off reasons were argued at the time. Alternative: "to aim to ship in one quarter"; state decisions and reasons without timing claims. | OA Q6 |
| C25 | MUST NOT SAY | The pilot as a "holdout". Alternative: 5% received the feature; comparison is with the rest of the base. | OA Q3 (supersedes S1 l.49) |
| C26 | MUST NOT SAY | Whether retention was of customers or of balances. Alternative: "90-day retention" unqualified. | OA Q3 |

## 5. Constants

| ID | Value | Accepted renderings | Stale renderings | Source |
|---|---|---|---|---|
| K1 | Flat deposits duration | three quarters | | S1 l.7 |
| K2 | Pilot share of customers | 5% of customers | 5% holdout | S1 l.25; OA Q3 |
| K3 | Pilot length | six weeks; 6 weeks; six-week | | S1 l.25 |
| K4 | Bug timing | week 3 | | S1 l.26 |
| K5 | Pause length | four days | | S1 l.26 |
| K6 | Core team | 5 engineers, 1 designer, 1 data analyst; five engineers, a designer and a data analyst | | S1 l.23 |
| K7 | Delivery aim | aim to ship in one quarter; to ship in one quarter (as an aim) | shipped in one quarter | S1 l.18; OA Q6 |
| K8 | Retention window | 90-day retention; 90 days after the pilot started | 35% | S1 l.34; OA Q3 |
| K9 | Year | 2023 | | S1 l.6 |

<!-- CONFIDENTIAL:START anonymization map. Never paste this block into an external model. -->
### Anonymization map

Owner-supplied instructions only. `scripts/check_names.py` fails on any variant in the Real column.

| ID | Real (never in artifact) | Anonymized rendering | Owner instruction |
|---|---|---|---|
| N1 | Example Bank | a retail bank | Do not name the bank |
| N2 | Project Kestrel; Kestrel | an automatic savings feature | Do not name the code name |
| N3 | ExamplePay | our payments partner | Do not name the partner |
| N4 | 1.2M; 1.2 million | directional scale only | customer count not absolute |
| N5 | 400 customers | a customer survey | survey size not absolute |
| N6 | 2,000 customers; 2000 | a subset of pilot customers | affected count not absolute |
<!-- CONFIDENTIAL:END -->

## 6. Terminology

| Internal term | Audience term | Forbidden phrasing | Note |
|---|---|---|---|
| round-ups | round-ups (S1 term; mechanism not described in sources) | | do not describe the mechanism beyond S1 |
| safe to spend | "safe to spend" balance: the part of the balance not set aside | | defines, no outcome |
| pilot group | pilot customers: the 5% who received the feature | holdout; control group | OA Q3 |
| outcome | directional result versus the rest of the base | drove company growth; primary bank; 35% | C19–C21 |
| fee product | a fee-earning product (S1 term; not named in sources) | naming or describing the product beyond S1 | the reason for CFO reporting is C10 |
| alignment | named person and action | drove alignment; stakeholder buy-in; leveraged; data-driven | mode writing rule 4 |

## 7. Open items

| ID | Open item | What is known | Resolved where | How the artifact treats it |
|---|---|---|---|---|
| O1 | Exact retention and deposit figures | Directional lift only; dashboards inaccessible | Not resolvable | Stated as directional (C12–C13) |
| O2 | Retention of customers or balances | Unknown | Not resolvable | "90-day retention" unqualified (C26) |
| O3 | Whether the one-quarter aim was met | Unknown | Deep dive, if owner recalls | Stated as aim (C18) |
| O4 | Reason for choosing the partner ledger | Proposed by engineering lead; author owned the risk | Deep dive | Decision stated without reason beyond "instead of building our own" |
| O5 | Whether trade-off reasons were given at the time | Unknown | Not resolvable | No timing claim (C24) |
| O6 | How setbacks were communicated to stakeholders beyond customers | Not in sources | Deep dive | Stated only as customer letter and CFO reporting |
| O7 | Share of customers affected by the bug | Absolute only, confidential | Not resolvable | "a subset of pilot customers" |
| O8 | S1 owner review status | Not given; fallback accepted | Owner | Unmarked lines not used beyond OA |

## 8. Reserve

| ID | Content | Why it is out | Use | Source |
|---|---|---|---|---|
| R1 | Rewards tier design that was cut | Not needed beyond the trade-off; detail for probing | Deep dive | S1 l.50 |
| R2 | Pilot randomization detail (by customer ID) | Detail for probing | Deep dive | OA Q3 |
| R3 | Alternatives considered for each trade-off | Not in sources | Reserve question | Readiness |

## 9. Editorial rules

1. Open with the problem and preview the directional outcome in one sentence.
2. Follow the five-element order of the mode.
3. First person only for C5, C7, C10, agreeing to C6, and in C9 the pause and the customer letter; "we" for running the pilot (C8) and the fix (C9); team or head of product for C3–C4.
4. Every outcome sentence carries "compared with the rest of the base" or an equivalent and a directional label.
5. Use anonymized renderings only; no absolute customer counts.

