# Contributing

Changes should preserve the project's main purpose: making detection-threshold trade-offs measurable and reproducible.

## Required for metric or simulator changes

- deterministic tests where practical;
- at least one multi-seed replicate check;
- documentation of changed assumptions;
- no claim that synthetic results represent production-network performance.

## Local checks

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
detection-lab replicate --seeds 1,2,3,4,5 --output replicate-report.json
```

Prefer adding interpretable metrics over introducing an opaque scoring rule.
