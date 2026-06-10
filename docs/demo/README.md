# SDVM Action Preview — Friendly Demo

This folder contains a **synthetic, public-safe friendly sample report** for the SDVM Action Preview. It is a **presentation layer**, not the full SDVM engine and not pilot-grade analysis.

## What is here

| File | Purpose |
|------|---------|
| [`friendly_sample_report.md`](friendly_sample_report.md) | Human-readable sample (Markdown) |
| [`friendly_sample_report.html`](friendly_sample_report.html) | Static browser-friendly sample (no external dependencies) |
| [`friendly_sample_report.json`](friendly_sample_report.json) | Structured mirror for integrators |
| [`FRIENDLY_DEMO_REPORT_DESIGN_V0_1.md`](FRIENDLY_DEMO_REPORT_DESIGN_V0_1.md) | Design record for this demo |

The HTML file is the primary visual artifact for sharing with non-technical readers. No screenshot PNG is included in this release.

## How this relates to Action Preview

| Layer | Location | Role |
|-------|----------|------|
| **Action Preview** | CLI / GitHub Action | Executable evidence screening — produces `validation.json`, `preview_report.json`, `preview_report.md` |
| **Friendly sample** | This folder | Static illustration of how screening results can be communicated |

Run the real preview against synthetic fixtures:

```bash
pip install -e .
python -m sdvm_action_preview.cli \
  --mode preview-report \
  --input examples/synthetic/healthy/canonical.jsonl \
  --output sdvm_preview_out
```

## Related documentation

- [`README.md`](../../README.md) — repository overview and quick start
- [`docs/ACTION_USAGE.md`](../ACTION_USAGE.md) — Action inputs, outputs, and usage patterns
- [`examples/synthetic/`](../../examples/synthetic/) — public-safe JSONL fixtures

## Pilot intake

For controlled pilot discussions, see **https://sdvm.tech/pilot/intake/**
