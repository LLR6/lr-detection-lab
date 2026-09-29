# Known Failure Modes

- A single seed produces unusually easy or hard synthetic data.
  - Detection: multi-seed replicate variance.
  - Response: inspect mean and spread, not one run.
- Class imbalance makes one metric look deceptively strong.
  - Detection: compare Precision, Recall, FPR, Specificity and Balanced Accuracy.
- Threshold comparison changes because generator semantics changed.
  - Detection: CHANGELOG / schema change.
  - Response: do not compare old and new reports directly.
- Small event windows make CV unstable.
  - Detection: low sample count.
  - Response: increase samples or min-events.
- Pareto frontier is misread as an automatic recommendation.
  - Response: choose using explicit operational costs.
