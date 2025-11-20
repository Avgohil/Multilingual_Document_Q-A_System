"""Document chunking and vector retrieval helpers.

This module provides utilities to split long texts into overlapping word
chunks, build a FAISS vector store from SentenceTransformer embeddings,
and retrieve the top-k most relevant chunks for a query.

All functions are lightweight helpers intended for use by other modules
in the project (no CLI or main runner included).
"""

from typing import List, Tuple

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def split_into_chunks(text: str, chunk_size: int = 300, overlap: int = 50) -> List[str]:
    """Fast & optimized text chunking."""
    
    if not text:
        return []

    words = text.split()
    n = len(words)

    if n <= chunk_size:
        return [" ".join(words)]

    chunks = []
    step = chunk_size - overlap  # faster sliding window

    for i in range(0, n, step):
        chunk = words[i : i + chunk_size]
        chunks.append(" ".join(chunk))

    return chunks



def build_vector_store(chunks: List[str]) -> Tuple[faiss.IndexFlatL2, np.ndarray]:
    """Compute embeddings for chunks and build a FAISS L2 index.

    Args:
        chunks: List of text chunks to embed.

    Returns:
        A tuple of (faiss_index, embeddings_array) where `embeddings_array`
        is a NumPy array of shape (n_chunks, dim) with dtype float32 and
        rows L2-normalized.

    Raises:
        ValueError: If `chunks` is empty.
    """
    if not chunks:
        raise ValueError("`chunks` must be a non-empty list of texts")

    try:
        embeddings = EMBED_MODEL.encode(chunks, show_progress_bar=False, convert_to_numpy=True)


        # Ensure dtype float32
        embeddings = embeddings.astype("float32")

        # L2-normalize embeddings so cosine similarity can be computed via L2
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        # Avoid division by zero
        norms[norms == 0.0] = 1.0
        embeddings = embeddings / norms

        # Create FAISS index for L2 distances
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)

        # Add vectors to the index
        index.add(embeddings)

        return index, embeddings
    except Exception as exc:
        # Surface minimal information while avoiding hard failures
        raise RuntimeError(f"Failed to build vector store: {exc}") from exc


def retrieve_top_chunks(
    query: str,
    index: faiss.IndexFlatL2,
    embeddings: np.ndarray,
    chunks: List[str],
    top_k: int = 5,
) -> List[Tuple[str, float]]:
    """Retrieve top-k most relevant chunks for `query`.

    The function embeds the query using the same SentenceTransformer
    model (`all-MiniLM-L6-v2`), L2-normalizes the query embedding, then
    performs an L2 search in FAISS. Because embeddings are normalized,
    L2 distance can be converted into cosine similarity.

    Args:
        query: Query string to search for.
        index: FAISS index built over normalized embeddings.
        embeddings: Numpy array of chunk embeddings (normalized).
        chunks: Original list of chunk strings (same order as embeddings).
        top_k: Number of top results to return (default 5).

    Returns:
        A list of tuples `(chunk_text, similarity_score)` sorted by
        descending similarity (highest relevance first). Similarity is
        cosine similarity in range [-1, 1].
    """
    if not query:
        return []

    if index is None or embeddings is None or not len(chunks):
        return []

    try:
        # Load same model used for chunk embeddings
        q_emb = EMBED_MODEL.encode([query], convert_to_numpy=True)
        q_emb = q_emb.astype("float32")
        q_norm = np.linalg.norm(q_emb, axis=1, keepdims=True)
        q_norm[q_norm == 0.0] = 1.0
        q_emb = q_emb / q_norm

        # Search the index (FAISS expects shape (n_queries, dim))
        distances, indices = index.search(q_emb, top_k)

        results: List[Tuple[str, float]] = []
        # distances are squared L2 distances between normalized vectors
        # For unit vectors: dist^2 = 2 - 2 * cos_sim => cos_sim = 1 - dist^2 / 2
        for dist, idx in zip(distances[0], indices[0]):
            if idx < 0 or idx >= len(chunks):
                continue
            # convert squared L2 distance to cosine similarity
            # dist returned by IndexFlatL2 is the squared L2? FAISS returns L2
            # distances (not squared) depending on index; in practice for
            # IndexFlatL2 it returns squared L2 distances. We'll be robust
            # and clamp the resulting similarity.
            d = float(dist)
            # Protect against small numerical issues
            cos_sim = 1.0 - (d / 2.0)
            cos_sim = max(-1.0, min(1.0, cos_sim))
            results.append((chunks[int(idx)], float(cos_sim)))

        # Sort results by similarity descending
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    except Exception:
        # On any error, return empty list rather than raising
        return []
