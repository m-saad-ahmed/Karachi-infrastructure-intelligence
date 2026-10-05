"""All tunable parameters live here (no weights hard-coded elsewhere)."""
import os
DB_PATH = os.getenv("KP_DB_PATH", "data/karachi_pulse.db")
PROCESSING_VERSION = "0.1.0"
KARACHI_BBOX = (24.70, 66.80, 25.60, 67.60)  # lat_min, lon_min, lat_max, lon_max
MAX_IMAGE_MB, MAX_VIDEO_MB, MAX_FILES, MAX_VIDEO_SECONDS = 10, 100, 10, 60
DUP_RADIUS_M = 25.0
MIN_CONFIDENCE = 0.35
RISK_WEIGHTS = {"severity": 0.35, "exposure": 0.20, "recurrence": 0.15,
                "environment": 0.15, "confirmation": 0.15}
RISK_LEVELS = [(85, "Critical"), (60, "High"), (30, "Moderate"), (0, "Low")]
BASE_SEVERITY = {"pothole": 0.7, "road_damage": 0.6, "waterlogging": 0.65, "garbage": 0.45,
                 "open_drain": 0.8, "sign_damage": 0.4, "streetlight": 0.35, "hazard": 0.5}
RAIN_SENSITIVE = {"waterlogging": 1.0, "open_drain": 0.8, "garbage": 0.5, "pothole": 0.4}
VEHICLE_CLASSES = {"car", "truck", "bus", "motorcycle", "bicycle", "train"}
# Vehicles-per-analyzed-frame bands — experimental and NOT calibrated against real traffic counts.
TRAFFIC_DENSITY_THRESHOLDS = {"Low": (0, 4), "Moderate": (5, 10), "High": (11, 20), "Severe": (21, float("inf"))}
BENCHMARK_RUNS = 10
ROAD_HEALTH_WEIGHTS = {"surface": 0.30, "drainage": 0.20, "cleanliness": 0.15, "lighting": 0.10,
                       "traffic_exposure": 0.10, "recurrence": 0.10, "safety_evidence": 0.05}
