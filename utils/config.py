"""Configuration loader for Math Mentor."""
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
OCR_LANGUAGES = os.getenv("OCR_LANGUAGES", "en").split(",")
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "5"))
HITL_CONFIDENCE_THRESHOLD = float(os.getenv("HITL_CONFIDENCE_THRESHOLD", "0.75"))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
KB_DIR = os.path.join(BASE_DIR, "rag", "knowledge_base")
FAISS_INDEX_DIR = os.path.join(DATA_DIR, "faiss_index")
MEMORY_DB_PATH = os.path.join(DATA_DIR, "memory.db")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FAISS_INDEX_DIR, exist_ok=True)
