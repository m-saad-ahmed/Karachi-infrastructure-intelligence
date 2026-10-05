import sqlite3, os
SCHEMA = """
CREATE TABLE IF NOT EXISTS locations(id INTEGER PRIMARY KEY, lat REAL, lon REAL, area TEXT, road_segment TEXT);
CREATE TABLE IF NOT EXISTS models(id INTEGER PRIMARY KEY, name TEXT, version TEXT, scope TEXT);
CREATE TABLE IF NOT EXISTS incidents(id INTEGER PRIMARY KEY, code TEXT UNIQUE, type TEXT, lat REAL, lon REAL,
  first_seen TEXT, last_seen TEXT, n_observations INTEGER, evidence_confidence REAL, is_synthetic INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS observations(id INTEGER PRIMARY KEY, incident_id INTEGER REFERENCES incidents(id),
  source_id TEXT, timestamp TEXT, lat REAL, lon REAL, evidence_type TEXT, model TEXT, model_version TEXT,
  confidence REAL, is_synthetic INTEGER NOT NULL, processing_version TEXT);
CREATE TABLE IF NOT EXISTS detections(id INTEGER PRIMARY KEY, observation_id INTEGER REFERENCES observations(id),
  label TEXT, confidence REAL, bbox TEXT);
CREATE TABLE IF NOT EXISTS weather(id INTEGER PRIMARY KEY, timestamp TEXT, lat REAL, lon REAL, rain_mm REAL, source TEXT);
CREATE TABLE IF NOT EXISTS risk_scores(id INTEGER PRIMARY KEY, incident_id INTEGER REFERENCES incidents(id),
  score REAL, level TEXT, details TEXT, computed_at TEXT);
CREATE TABLE IF NOT EXISTS experiments(id INTEGER PRIMARY KEY, name TEXT, date TEXT, model TEXT, dataset_version TEXT, params TEXT, metrics TEXT, notes TEXT);
CREATE INDEX IF NOT EXISTS ix_inc_type ON incidents(type);
CREATE INDEX IF NOT EXISTS ix_inc_loc ON incidents(lat, lon);
CREATE INDEX IF NOT EXISTS ix_obs_inc ON observations(incident_id);
CREATE INDEX IF NOT EXISTS ix_obs_ts ON observations(timestamp);
"""
def connect(path):
    d = os.path.dirname(path)
    if d: os.makedirs(d, exist_ok=True)
    c = sqlite3.connect(path, check_same_thread=False); c.executescript(SCHEMA); return c


def insert_observation(conn, source_id, lat, lon, evidence_type, model, model_version,
                        confidence, is_synthetic, processing_version):
    """Persists one real (or synthetic, if explicitly flagged) observation. Returns its row id."""
    import datetime
    cur = conn.execute(
        "INSERT INTO observations(source_id,timestamp,lat,lon,evidence_type,model,model_version,"
        "confidence,is_synthetic,processing_version) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (source_id, datetime.datetime.now().isoformat(), lat, lon, evidence_type, model,
         model_version, confidence, int(is_synthetic), processing_version))
    conn.commit()
    return cur.lastrowid


def insert_detection(conn, observation_id, label, confidence, bbox):
    import json as _json
    conn.execute("INSERT INTO detections(observation_id,label,confidence,bbox) VALUES (?,?,?,?)",
                 (observation_id, label, confidence, _json.dumps(bbox)))
    conn.commit()


def fetch_observations(conn):
    import pandas as pd
    return pd.read_sql_query("SELECT * FROM observations ORDER BY timestamp DESC", conn)


def fetch_detections(conn):
    import pandas as pd
    return pd.read_sql_query("SELECT * FROM detections ORDER BY id DESC", conn)
