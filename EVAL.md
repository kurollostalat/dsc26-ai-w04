# Retrieval Evaluation

**Setup:** All 8 contracts in `data/contracts/`, using `chunk_text(..., max_chars=500, overlap=50)`, `HashingEmbedder()`, and the 12 queries in `data/queries.jsonl`.

A hit is considered relevant when its span overlaps a relevant range for the same document.

| Retriever | Recall@3 | Queries missed |
|---|---:|---|
| BM25 only | 0.8333 (10/12) | q03, q12 |
| Dense only (HashingEmbedder) | 0.8333 (10/12) | q03, q12 |
| Hybrid (RRF) | 0.8333 (10/12) | q03, q12 |

All three retrievers achieved the same Recall@3 of 83.33%. Therefore, hybrid retrieval did not improve retrieval performance on this evaluation dataset.

Both missed queries require retrieving specific legal provisions: the tenant's termination notice period (q03), and the governing law and competent court (q12).

The identical results do not establish that hybrid retrieval is ineffective in general; they only show that it provided no measurable improvement on this particular evaluation set.

As next steps, I would experiment with a stronger embedding model, contextual chunk headers, and a reranker, then evaluate whether these changes improve Recall@3.