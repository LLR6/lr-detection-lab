# Change Risk Policy

Low risk: docs, examples, additive output fields.

Medium risk: new metrics, new synthetic generator controls, new replicate summaries.

High risk: metric definition changes, label semantics, feature extraction, synthetic distribution changes, Pareto logic, threshold interpretation.

High-risk changes must preserve old experiment comparability or clearly version the schema and document why results before/after are not directly comparable.
