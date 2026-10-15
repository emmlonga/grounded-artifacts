# Examples

Public teaching material that shows what the workflow does on a realistic problem.

The examples here are intentionally public-safe. Some are derived from real workflow runs, but they are reconstructed rather than copied: parties, figures, domain details and wording are generalized, and each example says so at the top. They are not the private source records of those runs. Grounding versions, audit files, adjudication history and source documents stay with the maintainer.

| Example | What it shows |
|---|---|
| [`commercial-proposal/`](commercial-proposal/README.md) | An alignment-stage proposal for an enterprise buyer: how the grounding settled where the sources pulled apart, what was kept out of the reader's way, a real audit round with its fixes, and the resulting proposal |
| [`product-story/`](product-story/README.md) | A synthetic two-page product story: a readiness check that blocks on unsupported claims, the ownership line written into the grounding, audits catching the same overstatement at three layers, and the final story |

For the smallest runnable material, see the synthetic pipeline fixture in `../scripts/selftest/`, used by `scripts/selftest.sh`. It describes a fictional logistics company and exercises the render path and the checks, but it does not model a real grounding.

A real run lives in its own project folder outside this repository. Nothing enters `examples/` automatically: each example is an explicit, reviewed extraction.
