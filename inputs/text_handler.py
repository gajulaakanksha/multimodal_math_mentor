"""Text input handler with basic sanitization."""
import re


def clean_text_input(text: str) -> dict:
    """
    Clean and validate a typed math question.
    Returns:
        {
            "text": str,
            "confidence": float,  # always 1.0 for typed input
            "low_confidence": bool,
            "error": None | str
        }
    """
    if not text or not text.strip():
        return {
            "text": "",
            "confidence": 0.0,
            "low_confidence": True,
            "error": "Empty input.",
        }

    cleaned = text.strip()
    cleaned = re.sub(r"\s+", " ", cleaned)  # normalize whitespace

    return {
        "text": cleaned,
        "confidence": 1.0,
        "low_confidence": False,
        "error": None,
    }
