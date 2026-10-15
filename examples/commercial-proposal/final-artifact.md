<!--
FREEZE HEADER (not rendered)
Public teaching example, derived from a real commercial-proposal run. Reconstructed for publication: the domain,
parties, figures and wording are generalized; bracketed values stand in for commercial constants that are not
published. See README.md in this folder.
-->
# Alignment proposal: an in-house document-to-calculation capability

*Scope, delivery approach and proposed investment*

**To:** [Client] · **From:** [Proposer]

Preliminary document for validating commercial direction. Final terms will be set in the definitive proposal and contract.

## 1. Decision summary

### A capability [Client] owns, which turns case documents into reviewed, traceable calculations within a defined scope

Today, to reach the amount owed in a case, a specialist reads the case documents, works out by hand which amounts, rates, rules and dates govern each component, gathers facts the documents do not contain, and prepares the calculation manually or with third-party tools.

**What we propose.** An application owned by [Client] that turns the relevant documents of a case into structured, reviewable parameters, each key parameter shown with the evidence behind it, and, for the cases the first version covers, into a calculation with a traceable calculation report.

**Expected result.** The specialist moves from interpreting everything from scratch to reviewing and confirming a prepared result. The process becomes traceable, and [Client] controls a workflow whose next improvements are prioritized by what real use shows. The operational gain will be measured in that use.

**Delivery.** A working pilot in about [A] weeks; the complete product for the initial scope in about [B] weeks; followed by about [C] months of rollout, stabilization, transfer and an evolution study.

**Investment.** [TOTAL] across three stages. Recurring third-party running costs are not included.

Before the definitive proposal, we would like to validate the six points in section 7: capability, scope, build and reuse, timing, investment and mandatory requirements.

## 2. The problem and what we will build

### From interpreting and calculating by hand to reviewing a prepared result

The hard part of the calculation is not finding numbers in the documents. It is giving each amount and each date its role: which amount actually governs among several plausible ones, which rule applies to each component, and from which event it runs. After that, the specialist still has to find facts the documents do not contain, such as the date of a later event, before preparing the calculation.

The application organizes this work in five steps:

1. **The specialist opens the case and uploads the relevant documents**, stating the type of each one and, where several documents could govern, which one does.
2. **The system prepares a structured interpretation** of the parameters, shows the evidence for the key parameters, and flags what is ambiguous or missing.
3. **The specialist reviews, corrects and confirms.** Nothing becomes final without that confirmation: the prepared interpretation is a draft to be validated.
4. **The specialist adds the facts the calculation needs**, by typing them, uploading a spreadsheet or attaching a supporting document.
5. **For covered cases, the product checks that the data is complete and consistent, runs the calculation with the confirmed rules and returns the result** with a calculation report showing the components, rules and versions used. Review history is kept, and a recalculation creates a new version without erasing the previous one.

| What goes in | What the product prepares | What the specialist receives |
|---|---|---|
| The relevant documents of the case, with the role of each, and the additional facts the calculation needs | A structured sheet of the case's parameters, with the evidence for the key ones and what is missing | For covered cases, the calculation with its report, and the review history |

## 3. Why an owned capability

### A solution of your own, without rebuilding what the market already does well

The investment goes into what is specific to [Client]'s operation. Mature components already on the market are integrated where they lower cost, risk and maintenance. Owning the solution means controlling the product and how it evolves, not owning every technical component it uses.

**What makes the capability yours**

- the project's specific application, which [Client] will own, subject to the definitive contract;
- the workflow in which specialists review, correct and confirm;
- the reviewed information of each case and its history;
- the evidence for the key parameters, and the traceability of every value and every calculation.

**What we can reuse**

- AI models available on the market;
- official reference tables and rates;
- a market calculation engine, where it proves the more reliable option after validation;
- standard cloud and corporate identity services.

The difference is between having access to a tool and controlling your own workflow, data and path of evolution: [Client] can adapt rules, workflows and integrations to its operation and, where the architecture allows, replace market components without losing the product layer and the data built up through use.

## 4. What the first version covers, and what it leaves out

### A first version that is complete for a defined scope

The product is designed for case documents with financial consequences. The first version does not aim to calculate every such case: it supports a defined set of calculation structures, illustrated below, which will be validated and frozen with [Client] in the first weeks of the project. One family of cases is the main reference today, because it offers the strongest basis for defining and validating those structures. Other case types can be supported once they are validated as compatible with the same structures.

| Examples within the initial scope | Examples outside the initial scope |
|---|---|
| Cases whose calculation follows one of the supported structures | Reading a complete case history to work out on its own which documents govern |
| Rules and rates applied component by component, each from its own start date | Cases whose obligation follows a materially different calculation model |
| Amounts owed by each party offset against each other | Reconciling two existing calculations that disagree |

When a case falls outside the covered scope, the product states the reason instead of producing an approximate calculation.

## 5. How we deliver, validate and price it

### Three stages in sequence, with a total investment of [TOTAL]

**~Week [A]: working pilot of interpretation and review.** A small group of trained specialists uploads documents, reviews the interpretation the system prepared and confirms the data.

**~Week [B]: complete product for the initial scope.** For covered cases the workflow runs from the documents to the calculation and its report, with functional acceptance by [Client].

**Then, about [C] months: rollout, stabilization, transfer and evolution study.** Use widens in a controlled way; defects found within the accepted scope are corrected; the product is transferred to an environment under [Client]'s control; and a performance study on real cases measures where the product reduces work, where it still needs manual intervention, which case types it completes and which situations block the calculation most often. The study guides the next improvements.

**How stages 1 and 2 will be validated**

- **Working pilot.** Accepted when the pilot users can run the agreed workflow (upload documents, receive the structured interpretation, see the evidence, correct and confirm) without software defects that prevent normal use. The prepared interpretation is not required to be free of corrections.
- **Complete product.** Accepted when, for the calculation types in scope, the full workflow runs from the reviewed information to the calculation and its traceable report, and out-of-scope cases or cases without enough information are correctly flagged.

Detailed acceptance criteria will be set in the definitive proposal, before the project starts.

| Stage | Result | Timing | Investment |
|---|---|---|---|
| 1. Working pilot of interpretation and review | Interpretation and review in use by the pilot group | ~Week [A] | [PRICE-1] |
| 2. Complete product for the initial scope | Full workflow to the calculation, with functional acceptance | ~Week [B] | [PRICE-2] |
| 3. Rollout, stabilization, transfer and evolution study | Wider use, corrective stabilization, transfer to the environment [Client] provides, performance study | ~[C] months after stage 2 | [PRICE-3] |
| **Total** | | | **[TOTAL]** |

Payment: [payment terms per stage].

The investment of [TOTAL] covers the three stages and the use of third-party services during development, testing and the pilot, the pilot up to reasonable use; exceptional consumption is borne by [Client], with prior approval. Recurring third-party costs of running the product, such as cloud, AI model usage and any external calculation service, are not included: after the transfer they are contracted and paid by [Client] or whoever it designates, and they will be sized to the selected architecture and the real volume of use.

Timing is approximate and depends on [Client]'s contributions, listed in the next section.

## 6. Conditions and responsibilities

**Main conditions**

- **Rollout (stage 3).** Includes up to [N] hours per month, scheduled and not cumulative unless agreed, for support activities not related to defects. Fixes for reproducible defects within the accepted scope do not use that allowance and remain [Proposer]'s responsibility during stage 3. New features are not included.
- **Design premises.** Specialists select and upload the documents. With [Client]'s systems, the only planned integration is corporate sign-in; the first version does not connect to document-management or case-management systems. Interpretation will use an enterprise AI service from the market, not a self-hosted model.
- **Confidentiality and security.** Real documents will be processed only in configurations [Client] has approved in advance for confidentiality, retention, access and data handling.
- **Transfer.** [Client] defines the final environment in the first weeks of the project, and the infrastructure transfer may complete during rollout. After the transfer, infrastructure and operation are the responsibility of [Client] or whoever it designates; indefinite hosting or operation by [Proposer] is not included.
- **After stage 3.** Further improvements are a separate scope, prioritized by the performance study. Ongoing maintenance and support are not part of this engagement and are a separate topic.

**What we will need from you**

- a business owner to answer questions and validate scope decisions;
- representative cases and calculations for validation;
- pilot users, participation in training, and timely feedback on acceptance;
- support from your IT team to enable corporate access;
- approval of how confidential documents may be processed and stored;
- a decision on the final environment and on who will operate it.

## 7. What we would like to align before moving forward

1. **Capability.** Is this the capability [Client] wants to bring in-house?
2. **Scope.** Does the initial scope cover the cases you want to prioritize?
3. **Build and reuse.** Does it make sense to concentrate the investment on what is specific to [Client] and reuse market components?
4. **Timing.** Does the sequence (~week [A], ~week [B], then about [C] months of rollout) meet your expectations?
5. **Investment.** Is [TOTAL] within an acceptable order of magnitude for [Client]?
6. **Mandatory requirements.** Given the design premises in section 6, is there an integration, security requirement, way of operating or other mandatory requirement that would materially change this design?

With these points aligned, we will prepare the definitive proposal, including acceptance criteria, responsibilities, and commercial and contractual terms. We suggest a short conversation to go through them together.
