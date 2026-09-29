# Detection Threshold Lab Research Card

## Question

How stable are simple beacon-detection thresholds when synthetic timing data changes across random seeds and operating conditions?

## Hypotheses

1. A threshold that looks attractive under one seed may not remain attractive across repeated datasets.
2. Recall and false-positive rate should be examined jointly rather than collapsed into a single “best” score.
3. Multi-seed dispersion provides useful context beyond a single confusion matrix.

## Method

- Generate labeled synthetic interval data.
- Aggregate by source/destination entity pair.
- Compute coefficient of variation.
- Sweep thresholds.
- Repeat the entire generation/evaluation process across multiple seeds.
- Compare mean, population standard deviation, min and max for each metric.

## Metrics

- TP / FP / TN / FN
- Precision / Recall
- False-positive rate / Specificity
- F1
- Balanced Accuracy
- Youden's J
- Recall–FPR Pareto frontier
- Across-seed mean / population standard deviation / min / max

## Current evidence

The project currently shows how the same evaluation pipeline behaves over deterministic repeated synthetic datasets.

It does **not** demonstrate real-network beacon-detection performance.

## Threats to validity

- synthetic generator assumptions;
- simple CV-only detector;
- limited traffic regimes;
- equal-ish class construction;
- no production time split.

## Next experiment

Introduce multiple benign jitter families and controlled class imbalance, then compare how Pareto candidates move across seeds and workload regimes.
