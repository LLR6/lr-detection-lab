# Engineering Decisions

## D1 — Keep the detector simple

The project intentionally uses interval CV so that threshold behavior is easy to inspect. The lab is about evaluation mechanics, not claiming a state-of-the-art beacon detector.

## D2 — Never hide threshold trade-offs

Reports expose confusion counts and multiple metrics rather than selecting a single preferred threshold.

## D3 — Repeat synthetic experiments

Multi-seed replicate reports reduce dependence on one lucky random sample.

## D4 — Keep production claims separate

Synthetic stability is useful for validating the pipeline, but it is not evidence of real-network accuracy.
