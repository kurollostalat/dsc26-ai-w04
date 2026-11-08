"""Reciprocal rank fusion and the hybrid retriever. You write this file."""
from __future__ import annotations

from bayyina.bm25 import BM25Index
from bayyina.types import Chunk, Embedder, Hit, Reranker


def rrf(rankings: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    """Ranks start at 1; score = sum of 1 / (k + rank); by score descending, then ID ascending."""
    scores = {}
    for ranking in rankings:
        for rank, chunk_id in enumerate(ranking, start=1):
            scores[chunk_id] = scores.get(chunk_id, 0) + 1 / (k + rank)

    results = sorted(
        scores.items(),
        key=lambda item: (-item[1], item[0])
    )

    return results

class HybridRetriever:
    def __init__(self, chunks: list[Chunk], embedder: Embedder, *, k1: float = 1.5,
                 b: float = 0.75, reranker: Reranker | None = None):
        self.chunks=chunks
        self.embedder=embedder
        self.k1=k1
        self.b=b
        self.reranker=reranker
        self.bm25 = BM25Index(k1=k1, b=b)
        self.bm25.add(chunks)
        self.embeddings = embedder.embed([chunk.text for chunk in chunks])
    def search(self, query: str, top_k: int = 5, candidates: int = 50) -> list[Hit]:
        if not self.chunks or not query.strip() or top_k <= 0 or candidates <= 0:
          return []
        query_embedding = self.embedder.embed([query])
        dense_scores =self.embeddings @ query_embedding[0]
        dense_order= sorted(range(len(self.chunks)),key=lambda i : (-float(dense_scores[i]), self.chunks[i].chunk_id))
        dense_ranking = [
    self.chunks[i].chunk_id
    for i in dense_order[:candidates]
]
        bm25_results = self.bm25.search(query, top_k=candidates)

        bm25_ranking = [chunk_id for chunk_id, _ in bm25_results]

        fused_results = rrf([bm25_ranking, dense_ranking])[:candidates]
        chunks_by_id = {chunk.chunk_id: chunk for chunk in self.chunks}

        hits = [
            Hit(
                chunk_id=chunk_id,
                doc_id=chunks_by_id[chunk_id].doc_id,
                start=chunks_by_id[chunk_id].start,
                end=chunks_by_id[chunk_id].end,
                text=chunks_by_id[chunk_id].text,
                score=score
            )
            for chunk_id, score in fused_results
        ]
        if self.reranker is not None and hits:
          rerank_scores = self.reranker(query, hits)

          hits = [
                Hit(
                    chunk_id=hit.chunk_id,
                    doc_id=hit.doc_id,
                    start=hit.start,
                    end=hit.end,
                    text=hit.text,
                    score=float(score)
                )
           for hit, score in zip(hits, rerank_scores)
        ]

        hits.sort(key=lambda hit: (-hit.score, hit.chunk_id))
        return hits[:top_k]
"""Searches the chunks for the query, returning a list of Hits."""
