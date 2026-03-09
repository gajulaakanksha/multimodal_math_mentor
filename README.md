# Multimodal Math Mentor AI

An end-to-end AI application that solves JEE-style math problems, explains solutions step-by-step, and learns from user feedback over time.


## Features

- **Multimodal Input**: Accepts text, images (EasyOCR), and audio (Whisper).
- **RAG Pipeline**: FAISS-backed retrieval covering Algebra, Calculus, Probability, etc.
- **5-Agent System**:
  - **Parser**: Cleans input → structured JSON
  - **Router**: Categorizes and plans approach
  - **Solver**: Solves using RAG + Python SymPy math tools
  - **Verifier**: Critically checks correctness and score
  - **Explainer**: Creates student-friendly markdown tutorials
- **Human-in-the-Loop (HITL)**: Automatically pauses execution if OCR confidence is low, input is ambiguous, or verifier confidence drops below threshold.
- **Memory & Learning**: Stores verified solutions in SQLite and uses TF-IDF similarity to reuse past knowledge.

---

## Setup & Run Instructions

### 1. Requirements
- Python 3.9+
- Provide your own Groq API key (Llama-3.1-8b-instant).

### 2. Installation
Clone the repo, then set up the virtual environment:

```bash
# Create and activate virtualenv
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
# source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Configuration
Copy the sample environment file and add your Groq API key:

```bash
cp .env.example .env
```
Open `.env` and replace `your_groq_api_key_here` with your actual key from [Groq Console](https://console.groq.com/keys).

### 4. Build Knowledge Base & Run

```bash
# Optional but recommended: Build the FAISS embedding index first
python -c "from rag.embedder import build_index; build_index()"

# Start the Streamlit app
streamlit run app.py
```

*Note: On your very first run involving an Image or Audio file, EasyOCR and Whisper will download their respective model weights (approx 150MB and 500MB). Subsequent runs will be fast.*

---

## Deployment

The app is entirely Streamlit-native and optimized for **Streamlit Cloud**:
1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy `app.py`
4. In Streamlit Cloud settings, add `GROQ_API_KEY` to the app Secrets.

## Project Structure

- `app.py`: Streamlit frontend UI
- `agents/`: The orchestration pipeline and 5 individual agents
- `inputs/`: Local OCR, ASR, and text parsing modules
- `rag/`: FAISS embedder, retriever, and the markdown knowledge base
- `memory/`: SQLite DB wrapper for problem storage and similarity search
- `utils/`: Config loaders and the Python SymPy calculator tool
