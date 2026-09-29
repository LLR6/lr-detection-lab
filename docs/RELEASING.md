# Releasing Detection Threshold Lab

## Checklist

1. CI green on supported Python versions.
2. Unit tests pass.
3. Multi-seed replicate report is generated.
4. Metric definitions and Pareto behavior remain documented.
5. Any synthetic generator change is called out explicitly.
6. Update `CHANGELOG.md`, `pyproject.toml` and `CITATION.cff`.
7. Review `docs/BENCHMARKS.md` and `docs/ROADMAP.md`.

Do not promote synthetic results as production-network accuracy in release notes.
