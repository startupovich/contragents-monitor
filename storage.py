import sqlite3, json
from typing import Dict, Tuple, List
from pathlib import Path
import pandas as pd
from datetime import datetime
from config import DB_PATH, CSV_LOG_DIR

def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS snapshot (inn TEXT PRIMARY KEY, payload TEXT, dt TEXT)"
    )
    return conn

def load_previous(inn: str) -> Dict:
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT payload FROM snapshot WHERE inn=?", (inn,))
    row = cur.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return {}

def save_current(inn: str, payload: Dict):
    conn = _connect()
    conn.execute(
        "REPLACE INTO snapshot (inn, payload, dt) VALUES (?,?,?)",
        (inn, json.dumps(payload, ensure_ascii=False), datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()

def diff(old: Dict, new: Dict) -> List[Tuple[str, object, object]]:
    changes = []
    keys = set(old) | set(new)
    for k in keys:
        if old.get(k) != new.get(k):
            changes.append((k, old.get(k), new.get(k)))
    return changes

def log_csv(rows: List[dict]):
    if not rows:
        return
    df = pd.DataFrame(rows)
    fname = CSV_LOG_DIR / f"diff_{datetime.now():%Y-%m-%d}.csv"
    df.to_csv(fname, index=False, encoding="utf-8-sig")
    return fname