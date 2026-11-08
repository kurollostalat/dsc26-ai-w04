"""BM25, written by hand. You write this file (no search libraries)."""
from __future__ import annotations
from bayyina.types import Chunk

import math
from collections import Counter
from .normalize import tokenize
class BM25Index:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.n=0
        self.avgdl=0
        self.term_freqs={}
        self.doc_lengths={}
        self.df={}

    def add(self, chunks: list[Chunk]) -> None:

        self.N = len(chunks)

        self.term_freqs = {}
        self.doc_lengths = {}
        self.df = {}

        for chunk in chunks:
            tokens = tokenize(chunk.text)

            self.term_freqs[chunk.chunk_id] = Counter(tokens)

            self.doc_lengths[chunk.chunk_id] = len(tokens)

            for term in set(tokens):
                self.df[term] = self.df.get(term, 0) + 1

        if self.N > 0:
            self.avgdl = sum(self.doc_lengths.values()) / self.N
        else:
            self.avgdl = 0

    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:

        if not query.strip() or not self.term_freqs or top_k <= 0:
            return []

        if self.avgdl == 0:
            return []

        query_tokens = tokenize(query)
        scores = {}

        for chunk_id in self.term_freqs:

            score = 0.0

            for term in set(query_tokens):

                df = self.df.get(term, 0)

                idf = math.log(
                    1 + (self.N - df + 0.5) / (df + 0.5)
                )

                tf = self.term_freqs[chunk_id].get(term, 0)
                dl = self.doc_lengths[chunk_id]

                numerator = tf * (self.k1 + 1)

                denominator = tf + self.k1 * (
                    1 - self.b + self.b * (dl / self.avgdl)
                )

                if tf > 0:
                    score += idf * (numerator / denominator)

            if score > 0:
                scores[chunk_id] = score

        results = sorted(
            scores.items(),
            key=lambda item: (-item[1], item[0])
        )

        return results[:top_k]
"""[(chunk_id, score), ...] with score > 0, by score descending then chunk ID ascending."""
