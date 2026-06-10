# SDVM Walkthrough — From Workflow Friction to Pilot Readiness

**A synthetic, public-safe walkthrough of how SDVM starts from operational evidence.**

## Preview notice

This walkthrough is **synthetic** and **public-safe**. It explains the SDVM concept using a simplified scenario. It does **not** run the full SDVM engine and does **not** include scoring internals, statistical methodology, thresholds, weights, calibration, or playbook logic.

> In AI-assisted workflows, the problem often does not appear as a single wrong answer. It appears as coordination friction: repeated handoffs, unclear checkpoints, rework, context loss, and fragile transitions between agents, tools, or human reviewers. SDVM starts by asking whether the workflow leaves enough operational evidence to make that degradation observable.

The public SDVM Action Preview does not run the full SDVM engine. It checks whether workflow evidence has enough structure to support screening and a later controlled pilot conversation.

---

## 1. The workflow

**Synthetic scenario:** A team uses an AI-assisted workflow to produce recurring technical review reports. Each run passes through drafting, tool-assisted evidence gathering, review, correction, and final decision.

| Stage | Actor roles (synthetic) |
|-------|-------------------------|
| Draft | Agent drafts initial report |
| Gather | Tool retrieves reference material |
| Review | Human reviewer checks draft |
| Correct | Agent revises based on feedback |
| Decide | Human approves or rejects |

Runs repeat on a schedule. Evidence is captured as canonical JSONL events with `run_id`, `ts`, `actor`, `event_type`, and optional `stage` / `note` fields.

## 2. The symptom

The final report may still look **acceptable**, but the workflow begins to show friction:

- Same final output quality, but **more correction loops**
- Handoffs become **less clear** — unclear who owns the next step
- Reviewer asks the **same clarifying questions repeatedly**
- Tool outputs are **copied forward without context**
- Checkpoints happen **late or inconsistently**

This is **coordination friction** — not necessarily a wrong answer on any single run.

## 3. Why output review is not enough

Reviewing only the final report misses operational degradation:

| What output review sees | What it misses |
|-------------------------|----------------|
| Final text quality | Repeated handoffs and rework |
| Single-run success | Cross-run coordination patterns |
| Answer correctness | Context loss between agents and tools |
| Pass/fail on deliverable | Weak or late checkpoints |

SDVM focuses on whether the **process** leaves evidence that makes coordination degradation **observable** across runs.

## 4. The evidence SDVM needs

Public-safe canonical JSONL fields (no proprietary SDVM variables):

| Field | Public-safe meaning |
|-------|---------------------|
| `run_id` | Which workflow run produced the event |
| `ts` | When the event happened |
| `actor` | Human, agent, or tool role |
| `event_type` | Draft, handoff, review, correction, checkpoint, decision |
| `stage` | Where in the workflow the event occurred |
| `note` | Optional public-safe description |

SDVM asks: *Can we trace who did what, when, and at which stage — across comparable runs?*

## 5. What the public Action Preview can check

The public SDVM Action Preview (CLI / GitHub Action) checks:

- Whether JSONL is parseable
- Whether required fields are present (`run_id`, `ts`, `actor`, `event_type`)
- Whether evidence is **sufficient** / **partial** / **insufficient** for screening
- Whether PRE/POST/DELTA shape is plausible
- Whether a pilot conversation is justified

It does **not** check:

- Full SDVM coordination diagnosis
- Scoring, thresholds, weights, or calibration
- Statistical methodology or playbook logic
- Intervention recommendations

**Try it:**

```bash
pip install -e .
python -m sdvm_action_preview.cli \
  --mode preview-report \
  --input examples/synthetic/healthy/canonical.jsonl \
  --output sdvm_preview_out
```

Pin in GitHub Actions: `ijamhour/SDVM-Action-Preview@sdvm-action-preview-public-v0.1`

## 6. What the friendly sample report adds

The [**Evidence Screening Sample**](friendly_sample_report.html) (`friendly_sample_report.md`, `.json`, `.html`) is a **presentation layer** over public-safe screening. It shows how screening results can be communicated to sponsors and executives.

It is **not** the full SDVM diagnostic report and is **not** the main SDVM story — this walkthrough is.

## 7. What full SDVM would examine in a controlled pilot

In a controlled pilot, the **private SDVM engine** would examine — at a high level only:

- How coordination changes across comparable runs
- Where evidence suggests repeated friction (handoffs, rework, context gaps)
- Whether interventions improve or degrade workflow coordination

This walkthrough does **not** reveal how that analysis is scored, calibrated, or turned into recommendations. Full SDVM analysis remains in authorized controlled pilot work only.

## 8. Why this matters

Observable coordination degradation enables:

- Informed decisions about pilot readiness — not blind deployment
- Evidence-backed conversations with sponsors and operators
- A path from “output looks fine” to “process may be degrading”

SDVM is about **operational evidence** and **workflow coordination** readiness — not generic AI quality claims.

## 9. Next step: pilot readiness

If screening suggests the workflow may support a controlled pilot:

1. Prepare an **authorized pilot trace package** (de-identified, approved for pilot use)
2. Use the pilot intake template: **https://sdvm.tech/pilot/intake/**
3. Do **not** post private production traces, customer data, or sponsor materials in public GitHub issues

## How to use this walkthrough

| Audience | Suggested path |
|----------|----------------|
| **Executive / sponsor** | Read this walkthrough → open [HTML version](sdvm_walkthrough_demo.html) → skim [Evidence Screening Sample](friendly_sample_report.html) |
| **Technical reviewer** | Read sections 4–5 → run CLI on `examples/synthetic/` → compare with screening sample |
| **Pilot sponsor** | Sections 1–3 + 9 → pilot intake link |

## Limitations

- This walkthrough is synthetic and presentation-oriented
- Not pilot-grade SDVM analysis
- No SDVM scores, S/D/V/M variables, thresholds, weights, calibration, or playbook logic
- Marketplace publication remains **on hold**
- Full SDVM engine remains in the private repository

## Links

- [Walkthrough (HTML)](sdvm_walkthrough_demo.html)
- [Evidence Screening Sample](friendly_sample_report.html)
- [Repository README](../../README.md)
- [Action usage](../ACTION_USAGE.md)
- [Synthetic examples](../../examples/synthetic/)
