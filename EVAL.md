# Retrieval evaluation

Setup: all 8 contracts in `data/contracts/`, `chunk_text(..., max_chars=500, overlap=50)`, `HashingEmbedder()`, the 12 queries in `data/queries.jsonl`. A hit is relevant when its span overlaps one of the query's `relevant` ranges in the same document.

| Retriever                    | recall@3       | queries missed |

|------------------------------|----------------|-----------------|
| BM25 only                    | 0.8333 (10/12) | q03, q12        |
| Dense only (HashingEmbedder) | 0.8333 (10/12) | q03, q12        |
| Hybrid (RRF)                 | 0.8333 (10/12) | q03, q12        |

All three retrievers achieved the same recall@3 of 83.33%, so hybrid retrieval did not improve the results in this evaluation. Both missed queries require retrieving specific legal provisions: the tenant's termination notice period (q03) and the governing law and competent court (q12). I would next experiment with a real embedding model, contextual chunk headers, and a re-ranker to improve retrieval of these specific clauses, then compare their recall@3 results.
