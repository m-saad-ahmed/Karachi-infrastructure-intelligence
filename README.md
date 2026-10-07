# Karachi Pulse — Low-Cost AI Urban Risk Intelligence

> **An independent research prototype exploring AI-assisted infrastructure risk intelligence for Karachi.**
>
> *Not an official municipal system, safety rating, government service, or production-ready hazard detection system.*

**Author:** Muhammad Saad
**Interface Version:** 1.0.0
**License:** MIT

---

## Overview

**Karachi Pulse** is a research prototype exploring whether low-cost smartphone imagery, computer vision, geospatial reasoning, environmental context, traffic information, and transparent risk scoring can be combined into an auditable urban-risk monitoring pipeline for a resource-constrained megacity.

The project is built around one principle:

> **A system should clearly distinguish what it knows, what it estimates, what it has measured, and what it does not yet know.**

Rather than presenting a black-box "AI risk score," Karachi Pulse keeps detection confidence, evidence confidence, and infrastructure risk as separate quantities, and exposes the reasoning behind every risk assessment.

The system is a foundation for future real-world data collection — not a claim that Karachi's infrastructure can already be reliably detected or predicted by this prototype.

---

## Research Question

Can low-cost smartphone imagery, combined with environmental, temporal, traffic, weather, and geospatial information, help identify, verify, prioritize, and analyze urban infrastructure risks while maintaining an explicit, auditable account of uncertainty?

The prototype investigates the full pipeline:

**Detection → Tracking → Evidence Fusion → Geospatial Reasoning → Risk Scoring → Evaluation**

Full write-up (sourced motivation, related work, methodology, limitations): `docs/research_report.md`.

---

## Why Karachi?

In December 2025, *Dawn* reported that **23 people, including 8 children, had died in Karachi that year after falling into open manholes and uncovered sewers** — a recurring, documented problem, not a hypothetical one.

Karachi Pulse is an attempt to explore whether a low-cost technical layer could eventually *complement* existing infrastructure-monitoring processes. It is **not** intended to replace municipal inspection, emergency services, engineers, or official infrastructure databases.

---

## What the System Does

### 1. Computer Vision
Model-agnostic detection pipeline: image preprocessing, video frame sampling, YOLO-based object detection, a swappable detector registry (nano/small baseline or a custom model), IoU-based temporal tracking, confidence filtering, and frame-to-incident aggregation.

**Limitation:** the baseline detector is a general-purpose COCO model (person, car, bus, truck, motorcycle). It is **not a Karachi hazard detector** — no pothole, open-manhole, waterlogging, or road-damage model exists in this repository yet. That requires a properly collected, consented, geotagged, labelled dataset.

### 2. Transparent Risk Engine
No single opaque AI-generated number. The risk engine combines explicitly weighted factors — severity, traffic exposure, recurrence, environmental context, multi-source confirmation — all configured in `config/`, not hard-coded inline. Every score ships with its contributing factors, so "why did this get this score?" always has an answer. Auditable, adjustable, reproducible — and explicitly **not** an official safety rating.

### 3. Evidence Fusion
Three deliberately separate concepts: **AI confidence** (how sure the model is about a detection), **evidence confidence** (how strong the supporting observations are), and **risk score** (how hazardous the configured model considers the incident). A noisy-OR aggregation means five frames from one video are not treated as five independent confirmations — only independent sources inflate evidence confidence.

### 4. Geospatial Intelligence
Coordinate validation, haversine-distance clustering, duplicate-incident merging, geographic filtering, and interactive risk maps. Nearby observations of the same physical hazard are grouped into one incident rather than counted separately.

### 5. Traffic & Flood Labs
Vehicle-density estimation from uploaded footage, and rainfall-scenario waterlogging risk modeling. Both explicitly labelled **experimental analytical estimates** — not official traffic measurements, flood forecasts, or municipal predictions.

### 6. Evaluation Framework
Precision/Recall/F1, IoU-based matching, MAE/RMSE, and a **condition-wise error-analysis tool**: upload labelled images tagged with conditions (rain, low light, blur, occlusion, etc.) and get a real, separately-measured score per condition — so weaknesses are measurable, not hidden behind one accuracy number.

### 7. Dataset Tooling
Corrupted-image validation, perceptual-hash duplicate detection, dataset statistics, and **geographic** (not random) train/val/test splitting — preventing leakage when nearby frames of the same street would otherwise land in both the training and test sets.

---

## Current Data Status

| Component | Status |
|---|---|
| Detection pipeline | **Implemented** |
| IoU-based tracking | **Implemented** |
| Geospatial clustering | **Implemented** |
| Risk engine | **Implemented** |
| Evidence confidence | **Implemented** |
| SQLite persistence (real uploads) | **Implemented** |
| Dataset validation / duplicate detection | **Implemented** |
| Geographic dataset splitting | **Implemented** |
| Evaluation framework + error analysis | **Implemented** |
| Experiment tracking | **Implemented** |
| Recurring-hotspot analysis | **Implemented** — a documented recurrence rule, not a trained forecaster |
| Traffic analysis | **Experimental** |
| Flood/waterlogging analysis | **Experimental** |
| Hazard-specific trained model | **Not trained** |
| Real Karachi hazard dataset | **Not yet collected** |
| mAP / confusion matrix | **Not implemented** |

---

## Synthetic Data Policy

Where real Karachi observations are unavailable, the prototype uses synthetic demonstration data, always explicitly labelled **SYNTHETIC DEMONSTRATION DATA** — never presented as real.

## Honesty Statement

> **If the system cannot measure something, it says so.**

Metrics that cannot currently be computed display **NOT EVALUATED**, never an invented number. This repository does not claim 94%-style accuracy, real-world pothole detection accuracy, government validation, municipal deployment, academic validation, real Karachi hazard coverage, or production-ready emergency prediction. It demonstrates an **engineering and evaluation framework** — not a finished city-scale AI monitoring system.

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install ultralytics          # optional — enables the COCO baseline detector
python -m pytest -q              # 31 tests should pass
streamlit run app.py
```

> First run with `ultralytics` installed downloads the baseline weights (`yolov8s.pt`, ~22MB) into the project root automatically. This file is machine-generated and already excluded via `.gitignore` — never commit it.

## Project Structure

```text
karachi-pulse/
│
├── app.py                        Streamlit application (12 pages)
├── requirements.txt
├── README.md
├── LICENSE
├── .env.example
├── .gitignore
│
├── app_ui/                       Design system + reusable UI components
│   ├── theme.py                  Color tokens, typography, global CSS
│   └── components.py             Cards, gauges, dossiers, detection rendering
│
├── computer_vision/
│   ├── preprocessing.py          Validation, decode, face blur, frame sampling
│   ├── detection.py              Model registry (baseline/custom), benchmarking
│   └── tracking.py               IoU-based temporal tracking
│
├── config/
│   └── __init__.py               All tunable weights/thresholds — nothing hard-coded inline
│
├── risk_engine/
│   ├── scoring.py                Risk scoring, evidence confidence, road health
│   └── traffic.py                Vehicle density categorization
│
├── geospatial/
│   └── clustering.py             Haversine clustering, coordinate validation
│
├── database/
│   └── db.py                     SQLite schema + real read/write helpers
│
├── evaluation/
│   └── metrics.py                Precision/Recall/F1, IoU matching, condition-wise error analysis
│
├── prediction/
│   └── hotspots.py                Recurring-hotspot flagging (recurrence rule)
│
├── experiments/
│   └── tracker.py                Real experiment logger (log.json created on first use)
│
├── scripts/
│   ├── generate_demo_data.py     Synthetic demonstration dataset generator
│   └── dataset_tools.py          Validation, duplicate detection, geographic split, stats
│
├── models/
│   └── custom/                   Empty — drop a trained .pt here to auto-override the baseline
│
├── data/
│   ├── raw/                      Real images go here (git-ignored)
│   ├── annotations/              Ground-truth labels for a real dataset
│   └── demo/                     Synthetic demonstration CSV
│
├── docs/
│   ├── methodology.md            Technical methodology + limitations
│   └── research_report.md        Full research write-up with verified citations
│
└── tests/
    └── test_core.py              31 unit tests covering every module above
```

## Using the Dataset Tools

```python
from scripts.dataset_tools import dataset_summary, validate_images, detect_duplicates, geographic_split
dataset_summary("data/raw")           # image count, corrupted count, resolution spread
validate_images("data/raw")           # which files fail to decode
detect_duplicates("data/raw")         # near-duplicate pairs via perceptual hashing
geographic_split(records)             # train/val/test by location, not randomly — avoids leakage
```

## Logging an Experiment

```python
from experiments.tracker import log_experiment, list_experiments
log_experiment("baseline-v1", model="yolov8s.pt", dataset_version="v0", params={"conf": 0.35}, metrics={"f1": 0.0})
list_experiments()
```

## Evaluating a Real Model

1. Fine-tune a YOLO model on real, geotagged Karachi hazard images (not included — see `docs/research_report.md` §8, §18).
2. Place the weights at `models/custom/your_model.pt` — the app auto-detects and prioritizes it over the baseline, no code changes needed.
3. In **Model Lab**, upload labelled test images plus a ground-truth JSON (template provided in-app) for real, live-computed Precision/Recall/F1 — and tag images with conditions (`rain`, `low_light`, `blur`, `occlusion`, etc.) for a real per-condition error-analysis breakdown.

## License

MIT — see `LICENSE`.