# SDVM Walkthrough Demo Design v0.1

**Status:** Design only — not implemented  
**Repository:** [`ijamhour/SDVM-Action-Preview`](https://github.com/ijamhour/SDVM-Action-Preview) (public)  
**Scope lock:** Defines a narrative walkthrough demo artifact. Does **not** implement the demo, publish Marketplace, publish the draft release, or add private engine code.

## Purpose

Design a new **SDVM Walkthrough Demo** — *From Workflow Friction to Pilot Readiness* — that explains the SDVM concept more convincingly than the current friendly sample report.

The walkthrough should help non-technical and semi-technical readers understand **why SDVM matters** before they encounter evidence validation or screening output. It must remain public-safe: no scoring internals, no pilot-grade claims, no private engine exposure.

## Why the current friendly report is not enough

The current [`friendly_sample_report.html`](friendly_sample_report.html) is **accurate and public-safe**, but it reads like a **technical screening report**. It starts too late in the story — at evidence validation — and does not demonstrate why SDVM exists.

| Current artifact | Role today | Limitation |
|------------------|------------|------------|
| `friendly_sample_report.md` / `.html` / `.json` | Output illustration | Assumes the reader already cares about JSONL shape and sufficiency |
| Action Preview CLI/Action | Executable screening | Technical entry point; not a narrative demo |

**Repositioning decision:** The friendly sample report should remain in the repo but be labeled **Evidence Screening Sample** — a supporting output illustration, not the main SDVM demo.

**Design position:** The current friendly sample report is a useful output illustration, but it is **not** the main SDVM demo. The new SDVM Walkthrough Demo should explain the operational problem first: recurring AI workflows can degrade through coordination friction, context loss, repeated handoffs, weak checkpoints, and rework. The Action Preview then appears as the public-safe first step for determining whether the workflow leaves enough evidence for controlled SDVM analysis.

## Demo role in the public repository

The public repository will have **three complementary demo layers**:

| Layer | Artifact | Role |
|-------|----------|------|
| **1. SDVM Walkthrough Demo** (new, primary) | `sdvm_walkthrough_demo.md` / `.html` | Narrative — operational problem → evidence readiness → pilot path |
| **2. Action Preview** (executable) | CLI / GitHub Action | Technical screening — JSONL validation, sufficiency, PRE/POST/DELTA shape |
| **3. Evidence Screening Sample** (existing, supporting) | `friendly_sample_report.*` | Output illustration — how screening results can be communicated |

The walkthrough is the **front door** for selective sharing. The friendly sample report is a **supporting exhibit** linked from section 6 of the walkthrough.

## Target audiences

| Audience | What they should take away |
|----------|----------------------------|
| **Technical reviewer** | The repo has a real executable public-safe screening layer (Action Preview), and the walkthrough correctly scopes what it does and does not do. |
| **Potential pilot sponsor** | The repo helps decide whether a workflow has enough evidence for a controlled SDVM pilot — not whether SDVM has already diagnosed the workflow. |
| **Executive / non-technical reader** | SDVM is about making **workflow coordination degradation observable**, not making generic claims about AI quality or answer correctness. |

## Core narrative

The walkthrough follows this arc:

1. **A recurring AI-assisted workflow exists** — multiple runs, agents, tools, human reviewers.
2. **The final answer may still look acceptable**, but the process starts showing friction.
3. **Friction appears in coordination** — handoffs, context loss, repeated corrections, unclear checkpoints, rework.
4. **SDVM asks** whether the workflow leaves evidence that makes this degradation observable.
5. **The public Action Preview checks** whether evidence is structured enough for screening.
6. **The friendly sample report shows** how screening can be communicated (Evidence Screening Sample).
7. **Full SDVM analysis remains private and controlled** — not demonstrated in this public repo.
8. **The next step** is an authorized pilot trace package.

### Suggested opening copy

> In AI-assisted workflows, the problem often does not appear as a single wrong answer. It appears as coordination friction: repeated handoffs, unclear checkpoints, rework, context loss, and fragile transitions between agents, tools, or human reviewers. SDVM starts by asking whether the workflow leaves enough operational evidence to make that degradation observable.

### Public-safe bridge

> The public SDVM Action Preview does not run the full SDVM engine. It checks whether workflow evidence has enough structure to support screening and a later controlled pilot conversation.

## Recommended walkthrough flow

User-facing sections (in order):

| # | Section | Content focus |
|---|---------|---------------|
| 1 | **The workflow** | Synthetic recurring AI-assisted workflow (e.g., support triage, code review assist, research synthesis) |
| 2 | **The symptom** | Final output acceptable; process shows friction (rework, handoff delays, context gaps) |
| 3 | **Why ordinary output review misses the issue** | Answer quality ≠ coordination health; degradation is operational, not a single failure |
| 4 | **What evidence SDVM needs** | Canonical JSONL fields, run boundaries, actor/event trace — qualitative description only |
| 5 | **What the public Action Preview can check** | Structure, sufficiency, PRE/POST/DELTA shape — link to CLI/Action |
| 6 | **What the friendly sample report communicates** | Evidence Screening Sample — link to `friendly_sample_report.html` |
| 7 | **What full SDVM would examine in a controlled pilot** | High-level only: coordination patterns, degradation signals, intervention context — **no methodology** |
| 8 | **Why this matters** | Observable degradation enables informed pilot decisions, not blind deployment |
| 9 | **Next step: pilot readiness** | Authorized pilot trace package; link to https://sdvm.tech/pilot/intake/ |

## Proposed demo artifacts

**Implement later** (not in this design PR):

```text
docs/demo/sdvm_walkthrough_demo.md
docs/demo/sdvm_walkthrough_demo.html
```

**Optional:**

```text
docs/demo/assets/sdvm_walkthrough_demo_screenshot.png
```

**Retain and reposition** (supporting artifacts):

```text
docs/demo/friendly_sample_report.md
docs/demo/friendly_sample_report.json
docs/demo/friendly_sample_report.html   → label as "Evidence Screening Sample"
```

**Update in implementation PR:**

- `docs/demo/README.md` — walkthrough as primary demo; friendly sample as supporting
- Root `README.md` — link to walkthrough as main demo entry point

## What the demo may show

Allowed qualitative concepts (no numeric scores):

- Coordination friction
- Handoff ambiguity
- Context loss
- Checkpoint weakness
- Rework
- Evidence readiness
- PRE/POST/DELTA shape (present / partial / absent)
- Pilot readiness (categorical, not scored)

Allowed visual patterns (HTML):

- Timeline or step diagram of a synthetic workflow (static, no live data)
- Qualitative status labels (e.g., “friction observed”, “evidence partial”)
- Side-by-side: “output looks fine” vs “process shows friction”

## What the demo must not imply

Forbidden or restricted:

- SDVM score or S/D/V/M numeric values
- Diagnostic heatmaps or scored visualizations
- Thresholds, weights, normalization, calibration
- Statistical confidence or confidence intervals
- Playbook recommendation or intervention prescription
- Claims of measured improvement or guaranteed remediation
- Customer, sponsor, or real production trace data
- That the walkthrough is generated by the private SDVM engine
- Pilot-grade analysis or Gate 3 / commercial-ready status
- GitHub Marketplace publication or hosted SaaS product

## Relationship to Action Preview

| Action Preview | Walkthrough demo |
|----------------|------------------|
| Executable (CLI / GitHub Action) | Static narrative (Markdown / HTML) |
| Validates JSONL, emits screening report | Explains *why* validation matters |
| Produces `validation.json`, `preview_report.*` | Links to Evidence Screening Sample as exhibit |
| Answers: “Is evidence shape sufficient for screening?” | Answers: “Why does evidence shape matter for SDVM?” |

The walkthrough should include a **concrete call-to-action** to run Action Preview on `examples/synthetic/` fixtures, then compare output with the friendly sample report.

## Relationship to full SDVM

The walkthrough may describe **what full SDVM would investigate** in a controlled pilot, but only at a high level:

- Whether coordination degradation is observable across runs
- Whether PRE/POST comparison could support intervention assessment
- Whether evidence supports categorical next-step discussion

It must **not** reveal the actual scoring model, measured-variable catalog, thresholds, statistical methodology, calibration, or playbook logic. Those remain in the private `ijamhour/SDVM` repository and authorized pilot work only.

| Surface | Location | Walkthrough may say |
|---------|----------|---------------------|
| Action Preview | This public repo | “Checks evidence structure for screening” |
| Evidence Screening Sample | This public repo | “Illustrates screening communication” |
| Full SDVM | Private repo | “Examines coordination degradation in controlled pilots” — no internals |

## Suggested copy

**Problem framing:**

> In AI-assisted workflows, the problem often does not appear as a single wrong answer. It appears as coordination friction: repeated handoffs, unclear checkpoints, rework, context loss, and fragile transitions between agents, tools, or human reviewers. SDVM starts by asking whether the workflow leaves enough operational evidence to make that degradation observable.

**Public-safe bridge:**

> The public SDVM Action Preview does not run the full SDVM engine. It checks whether workflow evidence has enough structure to support screening and a later controlled pilot conversation.

**Screening sample repositioning:**

> The Evidence Screening Sample (`friendly_sample_report.html`) shows how public-safe screening results can be communicated. It is a supporting illustration — not the main SDVM story.

**Pilot close:**

> Full SDVM analysis remains in authorized controlled pilot work. The next step for interested teams is to prepare an authorized pilot trace package via https://sdvm.tech/pilot/intake/

**Limitations block (required on walkthrough artifacts):**

> This walkthrough is synthetic and presentation-oriented. It does not represent full SDVM pilot-grade analysis and does not include scoring internals, statistical methodology, thresholds, weights, calibration, or playbook logic.

## Risks

| Risk | Mitigation |
|------|------------|
| Walkthrough over-claims SDVM capabilities | High-level “what full SDVM would examine” only; explicit private-scope boundary |
| Walkthrough confused with live engine output | Static artifact; prominent synthetic notice; separate from CLI artifacts |
| Friendly sample report still treated as main demo | Reposition as Evidence Screening Sample; walkthrough links to it in section 6 only |
| Executive reader infers “SDVM fixes workflows” | Emphasize observability and pilot readiness, not remediation |
| Technical reviewer dismisses narrative as marketing | Link every narrative section to executable Action Preview + synthetic fixtures |
| Copy drift toward scoring language | Forbidden concept list; copy guardrails block |

## Recommendation

**Proceed to implement a static Markdown + HTML SDVM Walkthrough Demo**, using the existing friendly sample report as a supporting output illustration (Evidence Screening Sample).

Implementation sequence:

1. **First implementation PR:** `sdvm_walkthrough_demo.md` + update `docs/demo/README.md` to position walkthrough as primary demo.
2. **Follow-up PR:** `sdvm_walkthrough_demo.html` — static narrative layout with section flow above; inline CSS only; no external JS/tracking.
3. **Optional:** screenshot asset; reposition friendly sample titles to “Evidence Screening Sample” in HTML/Markdown headers.

Do **not** wire walkthrough generation into CLI or Action runtime.

## Non-goals

- Implement the walkthrough in this design PR
- Remove or replace `friendly_sample_report.*` (reposition only)
- Publish GitHub Marketplace listing
- Publish draft release `sdvm-action-preview-public-v0.1`
- Create or move tags
- Add private engine code or imports from `sdvm/`, `sdvm_playbooks/`, `sdvm_baseline/`
- Expose scoring internals, statistical methodology, thresholds, weights, normalization, calibration, or playbook logic
- Show SDVM scores or S/D/V/M numeric values
- Imply Gate 3 complete or commercial-ready status
- Use customer, sponsor, or real production trace data
