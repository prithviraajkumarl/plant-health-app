"""Database management and SQLite repository for PlantHealthApp."""

import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path

from app.backend.config import DB_PATH, DB_DIR
from app.backend.seed_data import DISEASE_KNOWLEDGE_BASE, get_disease_info


def get_db_connection() -> sqlite3.Connection:
    """Create a SQLite connection with row factory enabled."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize database tables and seed diseases knowledge base."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Analyses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                image_path TEXT NOT NULL,
                thumbnail_path TEXT,
                plant TEXT NOT NULL,
                predicted_class TEXT NOT NULL,
                confidence REAL NOT NULL,
                is_simulated INTEGER DEFAULT 0,
                source TEXT DEFAULT 'upload',
                notes TEXT
            );
        """)

        # Diseases table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS diseases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_label TEXT UNIQUE NOT NULL,
                plant TEXT NOT NULL,
                display_name TEXT NOT NULL,
                is_healthy INTEGER DEFAULT 0,
                description TEXT NOT NULL,
                cause TEXT NOT NULL,
                treatment TEXT NOT NULL,
                prevention TEXT NOT NULL
            );
        """)

        # Indexes for fast lookup
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analyses_timestamp ON analyses(timestamp DESC);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_diseases_class ON diseases(class_label);")

        conn.commit()

        # Seed diseases table if not already populated
        cursor.execute("SELECT COUNT(*) FROM diseases;")
        count = cursor.fetchone()[0]

        if count < len(DISEASE_KNOWLEDGE_BASE):
            for label, info in DISEASE_KNOWLEDGE_BASE.items():
                cursor.execute("""
                    INSERT INTO diseases (class_label, plant, display_name, is_healthy, description, cause, treatment, prevention)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(class_label) DO UPDATE SET
                        plant=excluded.plant,
                        display_name=excluded.display_name,
                        is_healthy=excluded.is_healthy,
                        description=excluded.description,
                        cause=excluded.cause,
                        treatment=excluded.treatment,
                        prevention=excluded.prevention;
                """, (
                    label,
                    info["plant"],
                    info["display_name"],
                    1 if info["is_healthy"] else 0,
                    info["description"],
                    info["cause"],
                    info["treatment"],
                    info["prevention"]
                ))
            conn.commit()


def save_analysis(
    image_path: str,
    thumbnail_path: str,
    plant: str,
    predicted_class: str,
    confidence: float,
    is_simulated: bool = False,
    source: str = "upload",
    notes: Optional[str] = None
) -> int:
    """Save an analysis record and return its new ID."""
    timestamp = datetime.now().isoformat()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO analyses (timestamp, image_path, thumbnail_path, plant, predicted_class, confidence, is_simulated, source, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            image_path,
            thumbnail_path,
            plant,
            predicted_class,
            confidence,
            1 if is_simulated else 0,
            source,
            notes
        ))
        conn.commit()
        return cursor.lastrowid


def get_all_analyses(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """Retrieve list of analyses ordered by newest first."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, timestamp, image_path, thumbnail_path, plant, predicted_class, confidence, is_simulated, source, notes
            FROM analyses
            ORDER BY id DESC
            LIMIT ? OFFSET ?
        """, (limit, offset))
        return [dict(row) for row in cursor.fetchall()]


def get_analysis_by_id(analysis_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve single analysis by ID."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM analyses WHERE id = ?", (analysis_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def delete_analysis_by_id(analysis_id: int) -> Optional[Dict[str, Any]]:
    """Delete single analysis and return its metadata for file cleanup."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM analyses WHERE id = ?", (analysis_id,))
        row = cursor.fetchone()
        if row:
            record = dict(row)
            cursor.execute("DELETE FROM analyses WHERE id = ?", (analysis_id,))
            conn.commit()
            return record
        return None


def delete_all_analyses_history() -> List[Dict[str, Any]]:
    """Delete all analyses and return records for file cleanup."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM analyses")
        records = [dict(r) for r in cursor.fetchall()]
        cursor.execute("DELETE FROM analyses")
        conn.commit()
        return records


def get_disease_record(class_label: str) -> Dict[str, Any]:
    """Retrieve disease record from database or fallback to seed dict."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM diseases WHERE class_label = ?", (class_label,))
        row = cursor.fetchone()
        if row:
            d = dict(row)
            d["is_healthy"] = bool(d["is_healthy"])
            return d
    return get_disease_info(class_label)


def get_all_diseases_records() -> List[Dict[str, Any]]:
    """Retrieve all disease records."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM diseases ORDER BY plant, display_name")
        rows = cursor.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["is_healthy"] = bool(d["is_healthy"])
            result.append(d)
        return result
