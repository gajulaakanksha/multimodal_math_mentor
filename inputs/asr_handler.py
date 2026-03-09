"""ASR handler using OpenAI Whisper with math phrase normalization."""
import os
import re
import tempfile


def get_whisper_model():
    """Lazy-load Whisper model (downloads on first run)."""
    import whisper
    from utils.config import WHISPER_MODEL
    return whisper.load_model(WHISPER_MODEL)


_whisper_model = None


def transcribe_audio(audio_bytes: bytes, file_extension: str = "wav") -> dict:
    """
    Transcribe audio bytes using Whisper.
    Returns:
        {
            "text": str,
            "confidence": float,   # estimated from avg log-prob
            "low_confidence": bool,
            "language": str,
            "error": None | str
        }
    """
    global _whisper_model
    try:
        if _whisper_model is None:
            _whisper_model = get_whisper_model()

        # Write to temp file (Whisper needs a file path)
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        result = _whisper_model.transcribe(tmp_path, language="en", fp16=False)
        os.unlink(tmp_path)

        transcript = result.get("text", "").strip()
        segments = result.get("segments", [])

        # Estimate confidence from avg log probability
        if segments:
            avg_logprob = sum(s.get("avg_logprob", -1.0) for s in segments) / len(segments)
            # Convert log prob to ~confidence: logprob of 0 = perfect, -1 = poor
            confidence = max(0.0, min(1.0, (avg_logprob + 1.0)))
        else:
            confidence = 0.5

        transcript = normalize_math_speech(transcript)

        return {
            "text": transcript,
            "confidence": round(confidence, 3),
            "low_confidence": confidence < 0.60,
            "language": result.get("language", "en"),
            "error": None,
        }

    except Exception as e:
        return {
            "text": "",
            "confidence": 0.0,
            "low_confidence": True,
            "language": "unknown",
            "error": str(e),
        }


def normalize_math_speech(text: str) -> str:
    """Convert spoken math phrases to standard notation."""
    # Order matters — longer phrases first
    replacements = [
        (r"raised to the power of (\w+)", r"^\1"),
        (r"to the power of (\w+)", r"^\1"),
        (r"raised to (\w+)", r"^\1"),
        (r"square root of", "sqrt"),
        (r"cube root of", "cbrt"),
        (r"log base (\w+) of", r"log_\1"),
        (r"natural log of", "ln"),
        (r"log of", "log"),
        (r"sine of", "sin"),
        (r"cosine of", "cos"),
        (r"tangent of", "tan"),
        (r"integral of", "integral"),
        (r"derivative of", "d/dx"),
        (r"limit as (\w+) approaches", r"lim(\1->"),
        (r"infinity", "inf"),
        (r"pi", "pi"),
        (r"factorial", "!"),
        (r"choose", "C"),
        (r"over", "/"),
        (r"divided by", "/"),
        (r"multiplied by", "*"),
        (r"times", "*"),
        (r"plus", "+"),
        (r"minus", "-"),
        (r"equals", "="),
        (r"is equal to", "="),
        (r"greater than or equal to", ">="),
        (r"less than or equal to", "<="),
        (r"greater than", ">"),
        (r"less than", "<"),
    ]
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text.strip()
