"""Model abstraction + registry. Swap models without touching the app."""
import os, time, glob
from config import MIN_CONFIDENCE

INSUFFICIENT = "Insufficient visual evidence"

class Detector:
    name, version, scope = "none", "n/a", "none"
    def available(self): return False
    def detect(self, img): return []

class YoloDetector(Detector):
    def __init__(self, weights, name, scope):
        self.weights, self.name, self.scope, self._m = weights, name, scope, None
        self.version = os.path.basename(weights)
    def available(self):
        try: import ultralytics  # noqa
        except ImportError: return False
        return os.path.exists(self.weights) or self.name == "yolo-baseline"
    def detect(self, img):
        from ultralytics import YOLO
        self._m = self._m or YOLO(self.weights)
        r = self._m(img, verbose=False)[0]
        return [{"label": self._m.names[int(b.cls)], "confidence": float(b.conf),
                 "bbox": [float(v) for v in b.xyxy[0]]} for b in r.boxes]

def get_detector(baseline_weights="yolov8s.pt"):
    """Custom Karachi model (models/custom/*.pt) > COCO baseline (vehicles/people/etc., selectable
    size) > unavailable. baseline_weights lets the UI offer a slower-but-more-accurate COCO variant
    (e.g. yolov8s.pt) as an explicit opt-in — still a general-purpose model, not hazard-trained."""
    for w in sorted(glob.glob("models/custom/*.pt")):
        d = YoloDetector(w, "yolo-custom", "hazards")
        if d.available(): return d
    d = YoloDetector(baseline_weights, "yolo-baseline", "general COCO objects only (people/vehicles/etc.) - no hazard classes")
    return d if d.available() else Detector()

def class_names(det):
    """The real class list this detector's weights were trained on, read from the loaded model
    itself (not hard-coded) — empty if no model is loaded."""
    if not isinstance(det, YoloDetector) or not det.available():
        return []
    from ultralytics import YOLO
    det._m = det._m or YOLO(det.weights)
    return sorted(det._m.names.values())

def benchmark(det, n=None, size=(640, 640)):
    """Measures real wall-clock inference latency for n runs on THIS machine, using a synthetic
    random-noise image. This times raw inference speed only — a noise image says nothing about
    detection accuracy, so never report this benchmark as an accuracy measurement."""
    import numpy as np
    n = n or __import__("config").BENCHMARK_RUNS
    if not det.available():
        return None
    img = (np.random.rand(size[1], size[0], 3) * 255).astype("uint8")
    det.detect(img)  # warm-up run, excluded from timing (model/weights loading cost)
    times = []
    for _ in range(n):
        t0 = time.time(); det.detect(img); times.append((time.time() - t0) * 1000)
    times.sort()
    mean_ms = sum(times) / n
    return {"n_runs": n, "mean_ms": round(mean_ms, 1), "median_ms": round(times[n // 2], 1),
            "min_ms": round(times[0], 1), "max_ms": round(times[-1], 1),
            "fps": round(1000 / mean_ms, 1) if mean_ms else None}

def run(det, img):
    t = time.time(); h, w = img.shape[:2]
    dets = [d for d in det.detect(img) if d["confidence"] >= MIN_CONFIDENCE] if det.available() else []
    return {"model": det.name, "version": det.version, "scope": det.scope,
            "input_resolution": f"{w}x{h}", "inference_ms": round((time.time()-t)*1000, 1),
            "detections": dets, "status": "ok" if dets else INSUFFICIENT,
            "mode": "CUSTOM" if det.name == "yolo-custom" else "DEMO/BASELINE - performance limited"}
