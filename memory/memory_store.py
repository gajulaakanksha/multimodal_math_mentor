"""Memory Store — SQLite-backed persistent memory with similarity search."""
import sqlite3
import json
import os
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from utils.config import MEMORY_DB_PATH


def _get_connection():
    conn = sqlite3.connect(MEMORY_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    """Create tables if they don't exist."""
    conn = _get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT NOT NULL,
            input_mode TEXT DEFAULT 'text',
            parsed_json TEXT,
            retrieved_context TEXT,
            solution_json TEXT,
            answer TEXT,
            explanation_json TEXT,
            verifier_score REAL DEFAULT 0.5,
            verifier_correct INTEGER DEFAULT NULL,
            user_feedback TEXT DEFAULT NULL,
            user_comment TEXT DEFAULT NULL,
            timestamp REAL NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ocr_corrections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_ocr TEXT NOT NULL,
            corrected_text TEXT NOT NULL,
            timestamp REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_problem(
    input_text: str,
    input_mode: str,
    parsed_json: dict,
    retrieved_context: list,
    solution_json: dict,
    explanation_json: dict,
    verifier_score: float,
) -> int:
    """Save a solved problem to memory. Returns the inserted ID."""
    initialize_db()
    conn = _get_connection()
    cursor = conn.execute(
        """INSERT INTO problems
           (input_text, input_mode, parsed_json, retrieved_context, solution_json,
            answer, explanation_json, verifier_score, timestamp)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            input_text,
            input_mode,
            json.dumps(parsed_json),
            json.dumps(retrieved_context),
            json.dumps(solution_json),
            solution_json.get("final_answer", ""),
            json.dumps(explanation_json),
            verifier_score,
            time.time(),
        ),
    )
    conn.commit()
    problem_id = cursor.lastrowid
    conn.close()
    return problem_id


def save_feedback(problem_id: int, feedback: str, comment: str = ""):
    """Save user feedback for a problem (✅ correct / ❌ incorrect)."""
    initialize_db()
    conn = _get_connection()
    is_correct = 1 if feedback == "correct" else 0
    conn.execute(
        "UPDATE problems SET user_feedback=?, user_comment=?, verifier_correct=? WHERE id=?",
        (feedback, comment, is_correct, problem_id),
    )
    conn.commit()
    conn.close()


def save_ocr_correction(raw_ocr: str, corrected_text: str):
    """Save an OCR correction for future learning."""
    initialize_db()
    conn = _get_connection()
    conn.execute(
        "INSERT INTO ocr_corrections (raw_ocr, corrected_text, timestamp) VALUES (?, ?, ?)",
        (raw_ocr, corrected_text, time.time()),
    )
    conn.commit()
    conn.close()


def find_similar_problems(query: str, top_k: int = 3) -> list[dict]:
    """Find similar past problems using TF-IDF cosine similarity."""
    initialize_db()
    conn = _get_connection()
    rows = conn.execute(
        "SELECT id, input_text, answer, parsed_json, solution_json, verifier_score FROM problems ORDER BY timestamp DESC LIMIT 100"
    ).fetchall()
    conn.close()

    if not rows:
        return []

    texts = [row["input_text"] for row in rows]
    all_texts = [query] + texts

    try:
        vectorizer = TfidfVectorizer(stop_words="english", max_features=500)
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.15:  # minimum similarity threshold
                row = rows[idx]
                results.append({
                    "id": row["id"],
                    "input_text": row["input_text"],
                    "answer": row["answer"],
                    "verifier_score": row["verifier_score"],
                    "similarity": float(similarities[idx]),
                    "parsed_json": json.loads(row["parsed_json"] or "{}"),
                    "solution_json": json.loads(row["solution_json"] or "{}"),
                })
        return results
    except Exception:
        return []


def get_all_problems(limit: int = 50) -> list[dict]:
    """Retrieve recent problems for review/display."""
    initialize_db()
    conn = _get_connection()
    rows = conn.execute(
        "SELECT * FROM problems ORDER BY timestamp DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_ocr_corrections() -> list[dict]:
    """Get all stored OCR corrections."""
    initialize_db()
    conn = _get_connection()
    rows = conn.execute(
        "SELECT raw_ocr, corrected_text FROM ocr_corrections ORDER BY timestamp DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# Initialize on import
initialize_db()
