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

The project is built around a simple research principle:

> **A system should clearly distinguish what it knows, what it estimates, what it has measured, and what it does not yet know.**

Rather than presenting a black-box "AI risk score", Karachi Pulse keeps detection confidence, evidence confidence, and infrastructure risk as separate quantities and exposes the reasoning behind the final risk assessment.

The system is designed as a foundation for future real-world data collection — not as a claim that Karachi's infrastructure can already be reliably detected or predicted by this prototype.

---

## Research Question

Can low-cost smartphone imagery, combined with environmental, temporal, traffic, weather, and geospatial information, help identify, verify, prioritize, and analyze urban infrastructure risks while maintaining an explicit and auditable account of uncertainty?

The prototype investigates the complete pipeline:

**Detection → Tracking → Evidence Fusion → Geospatial Reasoning → Risk Scoring → Evaluation**

---

## Why Karachi?

Karachi faces recurring infrastructure and environmental challenges including open manholes, road damage, waterlogging, traffic congestion, and inconsistent infrastructure monitoring.

In December 2025, *Dawn* reported that **23 people, including 8 children, had died in Karachi during that year after falling into open manholes and uncovered sewers**.

That documented local problem motivated this project.

Karachi Pulse is therefore not built around a hypothetical "AI for cities" use case. It is an attempt to explore whether a low-cost technical layer could eventually complement existing infrastructure-monitoring processes.

**Important:** Karachi Pulse is not intended to replace municipal inspection, emergency services, engineers, or official infrastructure databases.

---

# What the System Does

## 1. Computer Vision

The computer-vision layer provides a model-agnostic detection pipeline.

Current capabilities include:

- Image preprocessing
- Video frame processing
- YOLO-based object detection
- Swappable detector/model registry
- IoU-based temporal tracking
- Detection filtering
- Confidence handling
- Frame-level to incident-level aggregation

### Important limitation

The current baseline detector is a general-purpose **COCO model**.

It can detect common classes such as:

- Person
- Car
- Bus
- Truck
- Motorcycle

It is **not a Karachi hazard detector**.

There is currently no trained pothole, open-manhole, waterlogging, or road-damage model in the repository.

A hazard-specific model requires a properly collected, consented, geotagged, and manually labelled dataset.

---

## 2. Transparent Risk Engine

Karachi Pulse does not use a single opaque AI-generated risk number.

The risk engine combines explicitly defined factors such as:

- Hazard severity
- Traffic exposure
- Recurrence
- Environmental context
- Multi-source confirmation

Weights and thresholds are kept in the `config/` layer rather than scattered throughout the application.

Each calculated risk score can be accompanied by its contributing factors so that a user can understand:

**Why did this incident receive this score?**

The scoring system is therefore intended to be:

- Auditable
- Adjustable
- Reproducible
- Interpretable

It should not be interpreted as an official safety rating.

---

## 3. Evidence Fusion

Karachi Pulse deliberately separates three concepts:

### AI confidence

How confident the detection model is that an object belongs to a detected class.

### Evidence confidence

How strong the available supporting observations are.

### Risk score

How important or hazardous an incident appears according to the configured scoring model.

These quantities are **not interchangeable**.

The evidence-fusion layer uses a noisy-OR style aggregation approach so that independent sources can contribute differently from repeated observations originating from the same source.

For example:

> Five frames from the same video should not automatically be treated as five independent confirmations.

This distinction is important when attempting to prevent duplicated observations from artificially inflating confidence.

---

# 4. Geospatial Intelligence

The geospatial layer provides:

- Coordinate validation
- Haversine-distance calculations
- Spatial clustering
- Duplicate incident merging
- Geographic filtering
- Interactive risk visualization

Multiple observations located close to one another can be grouped as the same physical incident rather than being treated as completely independent hazards.

This is particularly important for video-derived observations, where the same physical road condition may appear across many consecutive frames.

---

# 5. Traffic & Flood Labs

The project contains experimental analytical modules for:

### Traffic

Uploaded footage can be processed to estimate vehicle density and traffic-related exposure.

### Flood / Waterlogging

Rainfall scenarios can be used to explore potential waterlogging risk.

These modules are explicitly treated as **experimental analytical estimates**.

They are not:

- Official traffic measurements
- Official flood forecasts
- Emergency warnings
- Municipal predictions

---

# 6. Evaluation Framework

The evaluation layer is designed to produce measurable results once labelled data is available.

Current evaluation infrastructure includes:

- Precision
- Recall
- F1 score
- IoU-based matching
- Error analysis
- Per-condition evaluation
- MAE / RMSE for applicable numerical predictions

The system can analyse performance under conditions such as:

- Rain
- Low light
- Motion blur
- Occlusion
- Other user-defined environmental conditions

The goal is to make weaknesses measurable instead of hiding them behind a single accuracy number.

---

# 7. Dataset Tooling

The repository includes tools for preparing a future real-world dataset.

Available functionality includes:

- Image validation
- Corrupted-image detection
- Perceptual-hash duplicate detection
- Dataset statistics
- Geographic train/validation/test splitting

### Why geographic splitting?

Randomly splitting neighbouring frames can cause severe data leakage.

For example, if 20 consecutive frames from the same street are randomly distributed across training and testing sets, a model may effectively see almost the same scene in both.

Karachi Pulse therefore supports **geographic splitting** to reduce this form of leakage.

---

# 8. Current Data Status

This distinction is fundamental to the project.

| Component | Status |
|---|---|
| Detection pipeline | **Implemented** |
| IoU-based tracking | **Implemented** |
| Geospatial clustering | **Implemented** |
| Risk engine | **Implemented** |
| Evidence confidence | **Implemented** |
| SQLite persistence | **Implemented** |
| Dataset validation tools | **Implemented** |
| Duplicate detection | **Implemented** |
| Geographic dataset splitting | **Implemented** |
| Evaluation framework | **Implemented** |
| Experiment tracking | **Implemented** |
| Recurring-hotspot analysis | **Implemented as a documented recurrence rule** |
| Traffic analysis | **Experimental** |
| Flood/waterlogging analysis | **Experimental** |
| Hazard-specific trained model | **Not trained** |
| Real Karachi hazard dataset | **Not yet collected** |
| Real-world incident map | **Not available** |
| Official municipal data integration | **Not available** |
| mAP evaluation | **Not implemented** |
| Confusion matrix | **Not implemented** |

---

# Synthetic Data Policy

The prototype currently uses synthetic demonstration data where real Karachi observations are unavailable.

Synthetic incidents are explicitly labelled:

> **SYNTHETIC DEMONSTRATION DATA**

They are not presented as real observations.

This distinction exists specifically to prevent a demonstration dataset from being mistaken for a real Karachi infrastructure dataset.

---

# Honesty Statement

Karachi Pulse intentionally follows a strict rule:

> **If the system cannot measure something, it should say so.**

Metrics that cannot currently be computed are displayed as:

**NOT EVALUATED**

rather than being replaced with invented numbers.

The repository does **not** claim:

- 94% accuracy
- Real-world pothole detection accuracy
- Government validation
- Municipal deployment
- Academic validation
- Real Karachi hazard coverage
- Production-ready emergency prediction

The current project demonstrates the **engineering and evaluation framework**, not a finished city-scale AI monitoring system.

---

# Project Architecture

```text
karachi-pulse/
│
├── app.py
│
├── app_ui/
│   ├── Design system
│   └── Reusable UI components
│
├── computer_vision/
│   ├── Preprocessing
│   ├── Detection registry
│   └── IoU-based tracking
│
├── config/
│   └── Tunable weights and thresholds
│
├── data/
│   └── Raw / processed / demonstration data
│
├── database/
│   ├── SQLite schema
│   └── Persistence helpers
│
├── docs/
│   ├── methodology.md
│   └── research_report.md
│
├── evaluation/
│   ├── Precision / Recall / F1
│   ├── IoU matching
│   ├── Error analysis
│   └── Numerical evaluation
│
├── experiments/
│   └── Experiment tracking
│
├── geospatial/
│   ├── Haversine calculations
│   ├── Clustering
│   └── Coordinate validation
│
├── models/
│   └── Model registry / custom weights
│
├── prediction/
│   └── Recurring-hotspot analysis
│
├── risk_engine/
│   ├── Risk scoring
│   ├── Evidence confidence
│   └── Traffic density
│
├── scripts/
│   ├── Synthetic data generation
│   └── Dataset tooling
│
├── tests/
│   └── Unit tests
│
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── yolov8s.pt