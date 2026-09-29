# Reproducible experiment recipes

Detection Threshold Lab generates labeled synthetic timing data so threshold behavior can be inspected without network access.

## Baseline

```bash
detection-lab simulate --seed 7 --groups 20 --samples 12 --output demo.csv
detection-lab evaluate demo.csv --thresholds 0.05,0.1,0.2,0.3,0.5 --output report.json
```

## More observations per entity pair

```bash
detection-lab simulate --seed 7 --groups 20 --samples 30 --output long-window.csv
detection-lab evaluate long-window.csv --thresholds 0.05,0.1,0.15,0.2,0.3 --output long-window-report.json
```

## More entity pairs

```bash
detection-lab simulate --seed 11 --groups 100 --samples 12 --output larger.csv
detection-lab evaluate larger.csv --thresholds 0.05,0.1,0.2,0.3,0.5 --output larger-report.json
```

Do not compare these synthetic outputs as if they were measurements of a production network. Their purpose is to test the evaluation pipeline and make threshold trade-offs visible.
