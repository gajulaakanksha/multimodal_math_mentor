"""OCR handler using EasyOCR with confidence scoring."""
import numpy as np
from PIL import Image
import io
import os


def get_ocr_reader():
    """Lazy-load EasyOCR reader (downloads model on first run)."""
    import easyocr
    from utils.config import OCR_LANGUAGES
    return easyocr.Reader(OCR_LANGUAGES, gpu=False)


_reader = None


def extract_text_from_image(image_bytes: bytes) -> dict:
    """
    Extract text from image bytes using EasyOCR.
    Returns:
        {
            "text": str,           # Full extracted text
            "confidence": float,   # Average confidence (0-1)
            "low_confidence": bool,# True if confidence < 0.60
            "word_results": list   # Per-word results
        }
    """
    global _reader
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_array = np.array(img)

        if _reader is None:
            _reader = get_ocr_reader()

        results = _reader.readtext(img_array)

        if not results:
            return {
                "text": "",
                "confidence": 0.0,
                "low_confidence": True,
                "word_results": [],
                "error": None,
            }

        words = []
        confidences = []
        for bbox, text, conf in results:
            words.append(text)
            confidences.append(conf)

        avg_confidence = float(np.mean(confidences)) if confidences else 0.0
        full_text = " ".join(words)

        # Apply math-specific post-processing
        full_text = postprocess_math_ocr(full_text)

        return {
            "text": full_text,
            "confidence": round(avg_confidence, 3),
            "low_confidence": avg_confidence < 0.60,
            "word_results": [
                {"text": r[1], "confidence": round(r[2], 3)} for r in results
            ],
            "error": None,
        }

    except Exception as e:
        return {
            "text": "",
            "confidence": 0.0,
            "low_confidence": True,
            "word_results": [],
            "error": str(e),
        }


def postprocess_math_ocr(text: str) -> str:
    """Fix common OCR mistakes in math text."""
    import re
    replacements = {
        r"\bl\b": "1",   # lowercase l misread as one
        r"\bO\b": "0",   # letter O as zero (context-dependent)
        r"×": "*",
        r"÷": "/",
        r"−": "-",
        r"≤": "<=",
        r"≥": ">=",
        r"²": "^2",
        r"³": "^3",
        r"√": "sqrt",
        r"∫": "integral",
        r"∑": "sum",
        r"π": "pi",
        r"∞": "inf",
    }
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)
    return text.strip()
