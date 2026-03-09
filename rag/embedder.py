"""RAG Knowledge Base Embedder — chunks, embeds, and stores docs in FAISS."""
import os
import pickle
import re
import numpy as np

from utils.config import KB_DIR, FAISS_INDEX_DIR


def load_knowledge_base() -> list[dict]:
    """Load all .md and .txt files from the knowledge base directory."""
    docs = []
    for fname in os.listdir(KB_DIR):
        if fname.endswith((".md", ".txt")):
            fpath = os.path.join(KB_DIR, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            docs.append({
                "source": fname,
                "content": content,
            })
    return docs


def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> list[str]:
    """Split text into overlapping word-based chunks."""
    words = text.split()
    chunks = []
    step = chunk_size - overlap
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks


def get_embedding_model():
    """Lazy-load the sentence-transformers model."""
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")


_embed_model = None


def embed_texts(texts: list[str]) -> np.ndarray:
    """Embed a list of strings and return numpy array."""
    global _embed_model
    if _embed_model is None:
        _embed_model = get_embedding_model()
    embeddings = _embed_model.encode(texts, show_progress_bar=True, normalize_embeddings=True)
    return embeddings


def build_index(force_rebuild: bool = False) -> dict:
    """
    Build FAISS index from knowledge base docs.
    Saves index and metadata to FAISS_INDEX_DIR.
    Returns summary dict.
    """
    import faiss

    index_path = os.path.join(FAISS_INDEX_DIR, "index.faiss")
    meta_path = os.path.join(FAISS_INDEX_DIR, "metadata.pkl")

    if os.path.exists(index_path) and os.path.exists(meta_path) and not force_rebuild:
        return {"status": "exists", "message": "Index already exists. Use force_rebuild=True to rebuild."}

    print("Loading knowledge base documents...")
    docs = load_knowledge_base()
    if not docs:
        return {"status": "error", "message": f"No documents found in {KB_DIR}"}

    print(f"Found {len(docs)} documents. Chunking...")
    all_chunks = []
    all_metadata = []
    for doc in docs:
        chunks = chunk_text(doc["content"])
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_metadata.append({
                "source": doc["source"],
                "chunk_id": i,
                "text": chunk,
            })

    print(f"Created {len(all_chunks)} chunks. Embedding...")
    embeddings = embed_texts(all_chunks)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # Inner Product on normalized vecs = cosine similarity
    index.add(embeddings.astype(np.float32))

    faiss.write_index(index, index_path)
    with open(meta_path, "wb") as f:
        pickle.dump(all_metadata, f)

    print(f"FAISS index built with {len(all_chunks)} chunks from {len(docs)} documents.")
    return {
        "status": "built",
        "num_docs": len(docs),
        "num_chunks": len(all_chunks),
        "dim": dim,
    }


def load_index():
    """Load FAISS index and metadata from disk."""
    import faiss
    index_path = os.path.join(FAISS_INDEX_DIR, "index.faiss")
    meta_path = os.path.join(FAISS_INDEX_DIR, "metadata.pkl")

    if not os.path.exists(index_path) or not os.path.exists(meta_path):
        # Auto-build if missing
        build_index()

    index = faiss.read_index(index_path)
    with open(meta_path, "rb") as f:
        metadata = pickle.load(f)
    return index, metadata
