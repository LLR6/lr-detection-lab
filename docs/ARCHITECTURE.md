# Detection Threshold Lab Architecture

```text
seed(s)
  ↓
synthetic labeled timing data
  ↓
entity-pair interval features
  ↓
coefficient of variation (CV)
  ↓
threshold sweep
  ↓
confusion matrix + derived metrics
  ↓
Pareto frontier / multi-seed aggregate
```

## Design choices

The lab keeps the detector deliberately simple so the evaluation mechanics stay inspectable. CV is not presented as a complete beacon detector.

## Reproducibility controls

- explicit random seeds;
- deterministic generator for a fixed seed;
- JSON reports;
- repeated-seed aggregation;
- CI-published replicate artifacts.

## Non-goals

- claiming real-world detection accuracy from synthetic data;
- active network collection;
- traffic interception;
- automatic selection of a universally optimal threshold.
