# Roadmap

## Current foundation

- Seeded synthetic beacon / benign traffic
- Interval-CV feature extraction
- Threshold sweep
- Precision / Recall / FPR / Specificity / F1
- Balanced Accuracy / Youden's J
- Pareto frontier
- Multi-seed replicate stability reports

## Next

- bootstrap confidence intervals;
- configurable benign timing distributions;
- class-imbalance experiments;
- threshold selection under explicit FP/FN costs;
- CSV export for plotting outside the tool.

## Later

- multiple simple periodicity features;
- train/test time splits;
- calibration-drift experiments;
- comparison with simple spectral baselines.

## Non-goals

- publishing synthetic metrics as production-network accuracy;
- auto-selecting one universal “best” threshold.
