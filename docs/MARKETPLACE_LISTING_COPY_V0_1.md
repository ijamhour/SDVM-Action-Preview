# SDVM GitHub Action — Marketplace Listing Copy (draft v0.1)

**Status:** Draft copy only — **not published**  
**Scope:** Preparatory listing language for a future public distribution repository. Does **not** publish to GitHub Marketplace.

## Listing name candidates

| Candidate | Notes |
|-----------|--------|
| **SDVM Action Preview** | Matches public distribution repo name; clear preview scope |
| SDVM Workflow Evidence Screening | Emphasizes validation/screening, not full diagnosis |
| SDVM Coordination Health Preview | Shorter; preview-only framing |

**Recommended (draft):** **SDVM Action Preview** — aligns with public-safe slice package name and avoids implying full engine or pilot-grade analysis.

## Short description

GitHub Marketplace short descriptions are concise (~80 characters). Three draft options:

1. `Public-safe workflow evidence screening for recurring AI workflows.` (63 chars)
2. `Validate JSONL evidence shape and generate a limited preview report.` (62 chars)
3. `Preview: evidence validation and screening for agentic workflows.` (58 chars)

**Recommended (draft):** option 1.

## Long description

**Draft — copy for future Marketplace listing (not final):**

SDVM Action Preview is a **public-safe GitHub Action** that validates canonical JSONL evidence structure, checks whether PRE/POST/DELTA comparison is plausible, and generates a **limited preview report** over synthetic or user-provided evidence.

The Action runs on your GitHub Actions runner. It produces screening-oriented artifacts (`preview_report.md`, `preview_report.json`, `validation.json`) suitable for **pilot screening** and workflow readiness assessment.

This package is designed for **developer and enterprise preview** use: evidence shape validation, synthetic examples, and controlled pilot preparation. It is **not** pilot-grade SDVM analysis, **not** a hosted SaaS product, and does **not** replace your observability stack.

The **full SDVM diagnostic engine**, scoring internals, statistical methodology, playbooks, and calibration logic remain **private** and are used only in controlled pilot work.

SDVM Action Preview does **not** perform autonomous tuning, causal diagnosis, automatic remediation, or guaranteed workflow improvement. Next-step guidance is categorical (e.g., refine capture, candidate for pilot screening) — not full playbook recommendations.

For privacy, processing stays on the runner you control. The Action does not send telemetry to SDVM, does not call external services, and does not use the GitHub API to comment on pull requests or write to your repository.

This listing copy describes a **preview** public-safe slice. Artifact semantics may evolve; see repository docs for current limits before production claims.

## Who it is for

- AI platform teams evaluating workflow evidence shape before pilot screening  
- Agentic workflow developers integrating **preview** validation into CI  
- Enterprise AI reviewers assessing data-handling posture for preview Actions  
- Observability / AIOps teams checking PRE/POST/DELTA evidence structure  
- Teams preparing controlled pilots with long-running AI workflows  

## What it does today (public-safe slice)

- Runs inside **GitHub Actions** on the customer's runner  
- Accepts runner-local **canonical JSONL** (`evidence_path`) or bundled **synthetic** examples  
- **Validates** evidence structure (required fields: `run_id`, `ts`, `actor`, `event_type`)  
- Emits qualitative **sufficiency** (`sufficient` / `partial` / `insufficient`) — preview heuristics only  
- Detects **PRE/POST/DELTA shape** (yes/no/partial) without SDVM delta scoring  
- Generates a **limited preview report** (markdown + JSON) with limitations and next-step category  
- Writes **job summary** markdown (and appends to `$GITHUB_STEP_SUMMARY` when present)  
- Supports modes: **`validate-only`**, **`preview-report`**, **`synthetic`**  

## What it does not do

- Does **not** run the full private SDVM engine  
- Does **not** expose SDVM scoring internals, measured-variable catalog, or S/D/V/M diagnostic scoring  
- Does **not** apply statistical methodology, weights, thresholds, or normalization logic  
- Does **not** emit playbook recommendations or calibration logic  
- Does **not** provide pilot-grade SDVM analysis  
- No autonomous tuning or auto-applied changes  
- No causal diagnosis or proof of root cause  
- No automatic remediation  
- No policy enforcement or merge blocking by default  
- No PR comments or GitHub API writes  
- No external telemetry or SDVM-hosted data ingestion  
- No SaaS dashboard or UI  
- No billing or paid SKU in this preview phase  
- No GitHub Marketplace publication claim (publication on hold)  

## Basic usage draft

**Draft workflow** — uses public-safe Action input names from staged `action.yml`. Pins preview tag `sdvm-action-preview-v0.2` (historical pointer unchanged).

```yaml
name: SDVM Action Preview

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  sdvm:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Run SDVM Action Preview
        uses: ijamhour/SDVM-Action-Preview@sdvm-action-preview-v0.2
        with:
          mode: preview-report
          evidence_path: examples/synthetic/healthy/canonical.jsonl
          out_dir: sdvm_preview_artifacts
          write_job_summary: "true"
```

**Notes:**

- `sdvm-action-preview-v0.2` → commit `2f32e94` (immutable when published).  
- `sdvm-action-preview-v0.1` → commit `1afc731` (historical, preserved).  
- Public distribution repository **not created yet** — slug is a candidate (`SDVM-Action-Preview`).  
- For local development after public repo creation, use `uses: ./` at repository root.  
- This listing copy draft is **not** a Marketplace publication.  

## Inputs and outputs

### Inputs (public-safe `action.yml`)

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `evidence_path` | Yes* | — | Canonical JSONL file or directory on runner |
| `mode` | No | `preview-report` | `validate-only` \| `preview-report` \| `synthetic` |
| `run_label` | No | — | Optional report label |
| `out_dir` | No | `sdvm_preview_artifacts` | Output directory |
| `synthetic_example` | No | `healthy` | When `mode=synthetic` |
| `write_job_summary` | No | `true` | Write `job_summary.md` + step summary |

*Not required when `mode=synthetic`.

### Step outputs

| Output | Description |
|--------|-------------|
| `preview_report_path` | Path to `preview_report.md` |
| `validation_path` | Path to `validation.json` |
| `artifacts_dir` | Output directory root |
| `preview_mode` | Mode executed |

### Artifacts (under `out_dir`)

- `preview_report.md`  
- `preview_report.json`  
- `validation.json`  
- `job_summary.md` (when enabled)  

## Security and data handling summary

- Runs in the **user-controlled** GitHub Actions environment.  
- **No telemetry** and **no** SDVM-operated data collection.  
- **No** GitHub API calls, PR comments, or repository writes from the Action.  
- Users should avoid secrets, tokens, and unnecessary PII in canonical JSONL.  
- Do **not** post private production traces, customer data, or sponsor materials in public issues.  
- Artifact retention follows GitHub, repository, and organization settings.  

Full detail: [`SECURITY.md`](../../SECURITY.md).

## Preview limitations

- **Public-safe preview slice** — not full SDVM engine or pilot-grade analysis.  
- Sufficiency and PRE/POST/DELTA signals are **preview heuristics** — not SDVM scoring.  
- Artifact and summary copy may change before public repo publication.  
- Support via GitHub Issues — **best-effort, no SLA**.  
- **Marketplace publication remains on hold.**  

## Support and feedback

Use repository issue templates (`.github/ISSUE_TEMPLATE/`):

- **GitHub Action bug report** — Action failures or missing artifacts  
- **Documentation feedback** — incorrect or missing docs  
- **Report quality feedback** — preview report clarity (not full engine report quality)  
- **Adapter request** — future observability sources (no implementation commitment)  
- **Product preview feedback** — general adoption experience  

## Marketplace readiness note

This draft **does not** mean the Action is ready for Marketplace publication.

Readiness is tracked in [`MARKETPLACE_READINESS_CHECKLIST_V0_1.md`](MARKETPLACE_READINESS_CHECKLIST_V0_1.md). Publication still depends on:

- public-safe copy and screenshot alignment (see repository docs for public-safe slice posture);  
- trimmed staging exposure re-review;  
- explicit operator approval for public repo creation and Marketplace submission;  
- coherent public README / examples in `SDVM-Action-Preview` staging package.  

**Marketplace publication:** not done. On hold.

## Explicit non-claims (public-safe slice)

- does not run the full private SDVM engine;  
- does not expose SDVM scoring internals;  
- does not provide automatic remediation;  
- does not guarantee workflow improvement;  
- does not replace observability tools;  
- does not collect telemetry by default;  
- does not send traces to an SDVM backend;  
- does not claim Gate 3 complete or commercial-ready status.  

## Non-goals (this front)

- Marketplace publication, billing, GitHub App  
- Tag creation or movement  
- Private full-engine runtime changes  
- Reintroducing `sdvm/`, `sdvm_playbooks/`, or `sdvm_baseline/` into public staging  

## Related documentation

| Doc | Role |
|-----|------|
| `MARKETPLACE_COPY_PUBLIC_SAFE_SLICE_REVIEW_V0_1.md` | Copy alignment review for public-safe slice |
| `PUBLIC_SAFE_ACTION_SLICE_IMPLEMENTATION_V0_1.md` | Reduced slice implementation record |
| `MARKETPLACE_READINESS_CHECKLIST_V0_1.md` | Readiness matrix |
| `REPO_PRODUCT_SURFACE_V0_1.md` | Official product surfaces |
