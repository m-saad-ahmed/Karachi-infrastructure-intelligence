**Pipeline.** Image: decode -> optional face blur -> detector -> confidence filter -> incidents. Video: frame sampling -> detection -> IoU tracking -> one incident per track.

**Three separate quantities.** AI confidence (detector output), evidence confidence (noisy-OR over *independent* sources; repeated frames from one source do not inflate it), and risk score (weighted, configurable factors in `config/__init__.py`).

**Risk** = weighted severity + traffic exposure + recurrence + rainfall context + confirmation. Missing inputs use a neutral value and are reported as uncertainty.

**Limitations.** No custom Karachi model or real dataset is included; baseline COCO YOLO detects vehicles only, so hazard classes return "Insufficient visual evidence". Demo data is synthetic. Risk weights are expert-set, unvalidated. Face blur is best-effort; license plates are not reliably anonymized. No flood, accident or traffic-flow prediction is claimed.

**Traffic Lab** runs the active COCO detector on an uploaded image or clip and counts objects in `config.VEHICLE_CLASSES`. Density bands (`config.TRAFFIC_DENSITY_THRESHOLDS`) are configured, not calibrated against measured traffic — treat them as an experimental estimate. Peak-period and road-segment comparisons need traffic data gathered across many sessions, which a single upload cannot provide.

**Model Lab** now runs a real, measured inference-latency benchmark on a synthetic image (speed only — not an accuracy test), and can compute real precision/recall/F1 if you upload your own labelled images plus a matching ground-truth JSON (see the in-app template). mAP, confusion matrix and class-level error analysis still require a larger labelled set than a quick upload provides.

**Dataset tooling** (`scripts/dataset_tools.py`) is real and unit-tested: corrupted-image validation, perceptual-hash near-duplicate detection, and both random and geographic train/val/test splitting (geographic split keeps nearby observations of the same physical location in the same split, preventing leakage). It operates on whatever is in `data/raw/` and reports an honest empty result until real images are added.

**Recurring hotspots** (`prediction/hotspots.py`) is a documented recurrence rule (3+ observations flags a location as recurring), not a trained forecasting model — it returns "unavailable" rather than guessing when there's too little history.

**Experiment tracking** (`experiments/tracker.py`) is a real, functional JSON-backed logger — empty until an experiment is actually logged.

**Database persistence**: every image/video analyzed in AI Analysis Lab is now saved as a real (non-synthetic) observation to the local SQLite database (`database/db.py`), browsable and exportable from the new Data Explorer page.

**Error analysis** (`evaluation/metrics.py::evaluate_with_conditions`) extends the live evaluation tool: if uploaded ground truth tags each image with condition labels (rain, low_light, blur, occlusion, unusual_angle, night, heavy_traffic — or custom tags), Model Lab computes a real, separately-measured F1/precision/recall for every condition, not just one averaged overall score. An image tagged with multiple conditions counts in every bucket it's tagged with. The plain (untagged) ground-truth format remains fully supported, bucketed as "unspecified." This closes the last item from the original functional spec that could be built without real field data — everything beyond this point (a trained hazard model, real Karachi observations) requires actual data collection, not further engineering.
