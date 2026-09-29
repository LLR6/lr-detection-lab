# Compatibility

## Runtime

- Python: **3.10+**
- CI target: **3.10 / 3.11 / 3.12**
- CLI: `detection-lab`

## Data contract

CSV input requires:

- `timestamp`
- `source`
- `destination`
- `label`

Labels are currently limited to `beacon` and `benign`.

## Report schemas

- threshold evaluation: `lr-detection-lab/v2`
- multi-seed replicate: `lr-detection-lab-replicate/v1`

Adding metrics is backward-compatible; redefining an existing metric is not.
