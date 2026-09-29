# Benchmarks

## Single-dataset threshold sweep

```bash
detection-lab simulate --seed 7 --groups 20 --samples 12 --output demo.csv
detection-lab evaluate demo.csv --thresholds 0.05,0.1,0.2,0.3,0.5 --output report.json
```

Outputs confusion-matrix counts, derived metrics and a Recall–FPR Pareto frontier.

## Multi-seed replicate

```bash
detection-lab replicate \
  --seeds 1,2,3,4,5 \
  --groups 20 \
  --samples 12 \
  --thresholds 0.05,0.1,0.2,0.3,0.5 \
  --output replicate-report.json
```

For each threshold, the report stores mean, population standard deviation, min and max across runs.

## Interpretation boundary

Synthetic repeatability is useful for validating the experiment pipeline. It is not evidence of production-network accuracy.
