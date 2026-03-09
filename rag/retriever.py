"""RAG Retriever — top-k semantic search over the FAISS index."""
import numpy as np
from rag.embedder import embed_texts, load_index
from utils.config import RAG_TOP_K


_index = None
_metadata = None


def get_index():
    """Lazy-load FAISS index."""
    global _index, _metadata
    if _index is None:
        _index, _metadata = load_index()
    return _index, _metadata


def retrieve(query: str, top_k: int = None) -> list[dict]:
    """
    Retrieve top-k relevant chunks for a query.
    Returns list of:
        {
            "text": str,
            "source": str,
            "score": float,   # cosine similarity
            "rank": int,
        }
    """
    top_k = top_k or RAG_TOP_K
    index, metadata = get_index()

    query_embedding = embed_texts([query]).astype(np.float32)
    scores, indices = index.search(query_embedding, top_k)

    results = []
    for rank, (score, idx) in enumerate(zip(scores[0], indices[0])):
        if idx < 0 or idx >= len(metadata):
            continue
        meta = metadata[idx]
        results.append({
            "text": meta["text"],
            "source": meta["source"],
            "score": float(score),
            "rank": rank + 1,
        })

    return results


def format_context(retrieved_chunks: list[dict]) -> str:
    """Format retrieved chunks into a prompt-ready context string."""
    if not retrieved_chunks:
        return "No relevant context found in knowledge base."

    lines = ["=== Retrieved Knowledge Base Context ===\n"]
    for chunk in retrieved_chunks:
        lines.append(f"--- Source: {chunk['source']} (Relevance: {chunk['score']:.2f}) ---")
        lines.append(chunk["text"])
        lines.append("")
    return "\n".join(lines)
