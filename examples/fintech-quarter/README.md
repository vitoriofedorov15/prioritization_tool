# Which onboarding improvements should ship next?

An educational decision case for a fictional fintech product team. **All options, ratings and effort estimates are synthetic.** This case has no company affiliation and makes no claims about real customer or financial outcomes.

## Decision

The team has **12 effort points** for the next quarter. It is considering 12 improvements to onboarding and early payments. Product cares about activation, Operations about workload, and Risk about controls. The goal is to agree a shortlist and understand whether a change in stakeholder influence changes the decision.

**Recommendation:** choose **Verification status tracker (3 points), Document precheck (4) and Manual review triage (5)**, using all 12 points. Tracker and precheck occupy the first two baseline positions and remain in the top three when Risk influence increases. Manual review triage is fourth in the baseline, second in the risk-first scenario and first in the TOPSIS reference. This makes it a reasonable third item when the team values a shortlist that remains useful across the scenarios.

The strict baseline top three would instead include Payment error messages (2 points) and use 9 points. That is a reasonable alternative if delivery speed and the baseline stakeholder agreement dominate; it leaves 3 points of capacity. The recommended 12-point portfolio deliberately trades that quicker item for review triage. This is a documented human choice informed by rankings, not the output of a budget optimization algorithm.

## Inputs and assumptions

[`options.csv`](options.csv) holds the original invented judgments:

- Conversion benefit, operations benefit and risk reduction: ordinal scores from 1 to 10; higher is better.
- Effort: invented delivery points; lower is better.
- Delivery ease: `11 − effort`, so all TOPSIS criteria have benefit direction.

The two methods use the same named options but different representations:

| Input | Meaning |
|---|---|
| [`moscow.csv`](moscow.csv) | 108 rows: 12 alternatives × 3 criteria × 3 stakeholders |
| [`baseline-weights.csv`](baseline-weights.csv) | Product 0.45, Operations 0.35, Risk 0.20 |
| [`risk-first-weights.csv`](risk-first-weights.csv) | Product 0.20, Operations 0.20, Risk 0.60 |
| [`topsis.csv`](topsis.csv) | Four benefit criteria; each alternative's row weight is 1 |

For MoSCoW, each stakeholder assesses three equally represented criteria: **Role value** (that role's corresponding benefit score), **Delivery ease**, and **Shared benefit** (the mean of the three benefit scores). Scores are converted to the category scale by `round(0.3 × rating, 1)` and encoded as a mixture of adjacent categories: W=0, C=1, S=2, M=3. For example, 2.7 becomes `70% M, 30% S`. Feasibility and shared benefit judgments are common across roles; role-value judgments differ. This is an illustrative elicitation model, rather than real survey evidence.

The Russian CSV headers are intentional: they match the existing parsers. Option and criterion names remain English. The application weights stakeholders, not criteria, in MoSCoW; the sensitivity scenario changes **Risk stakeholder influence**.

## Actual results

| Alternative | Baseline rank | Risk-first rank | TOPSIS rank |
|---|---:|---:|---:|
| Verification status tracker | 1 | 3 | 3 |
| Document precheck | 2 | 1 | 2 |
| Payment error messages | 3 | 5 | 5 |
| Manual review triage | 4 | 2 | 1 |
| Duplicate payment guard | 7 | 4 | 4 |
| Sanctions review queue | 11 | 7 (tied score) | 6 |

[Full score table](ranking.md) · [Machine-readable results](results.json)

Increasing Risk influence promotes review triage and duplicate payment protection. Tracker and precheck remain in the top three in all runs. Sanctions review rises, but does not enter the leading shortlist because its conversion benefit and delivery ease are lower in the synthetic inputs. Risk-first scores for sanctions review and support routing tie at 85.6; their display order follows input order.

Compare **ranks**, rather than interpreting a MoSCoW score of 100 as better performance than a TOPSIS score of 78.2. The methods use different normalizations. The case does not run the other algorithm families: Kano needs satisfaction responses, while fuzzy methods need their own elicitation formats; inventing those responses would create a separate assessment.

## Reproduce

Follow the [root quick start](../../README.md#quick-start). On the home page click **Run fintech demo →**. It submits the checked-in files through `/api/upload` and `/api/analyze/{method}` and opens a populated dashboard.

Alternatively, from the root with backend development dependencies installed:

```bash
python examples/fintech-quarter/run_demo.py
```

The script uses an empty Gemini key, checks that all three calculations return 12 options, verifies that AI is unavailable, and regenerates `results.json` and `ranking.md`.

For manual upload, choose MoSCoW, upload `moscow.csv` as Requirements and `baseline-weights.csv` as Weights. Run a second MoSCoW analysis with `risk-first-weights.csv`, then a TOPSIS analysis with `topsis.csv`. The one-click demo gives these runs distinct scenario labels.

Ratings do not estimate ROI or guarantee outcomes. Before a real delivery decision, collect actual evidence, validate effort and dependencies, and agree any mandatory controls with the relevant owners.
