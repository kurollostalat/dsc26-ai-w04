# Retrieval Evaluation

## 1. Evaluation Overview

The purpose of this evaluation is to compare three retrieval approaches:

- BM25: sparse keyword-based retrieval.
- Dense: semantic retrieval using `HashingEmbedder`.
- Hybrid: Reciprocal Rank Fusion (RRF), combining sparse and dense retrieval results.

The main evaluation metric is Recall@3. It measures whether the retriever returns a relevant result within its top three retrieved results.

## 2. Evaluation Setup

The evaluation was performed using:

- Documents: All 8 contracts in `data/contracts/`.
- Queries: The 12 queries in `data/queries.jsonl`.
- Chunking configuration: `max_chars=500`, `overlap=50`.
- Dense embedding implementation: `HashingEmbedder()`.
- Retrieval approaches: BM25, Dense, and Hybrid (RRF).

The same document collection and query set were used to compare all three approaches.

## 3. Relevance Criteria and Metric

A retrieved result is considered relevant when its text span overlaps a relevant range belonging to the same document.

Recall@3 is calculated as:

Recall@3 = Number of queries with at least one relevant result in the top 3 / Total number of queries

For this evaluation, there were 12 queries. Therefore, each successfully retrieved query contributes 1/12 to the final Recall@3.

## 4. Evaluation Results

| Retriever | Recall@3 | Successful Queries | Queries Missed |
|---|---:|---:|---|
| BM25 only | 0.8333 (10/12) | 10 | q03, q12 |
| Dense only (HashingEmbedder) | 0.8333 (10/12) | 10 | q03, q12 |
| Hybrid (RRF) | 0.8333 (10/12) | 10 | q03, q12 |

All three retrieval approaches achieved a Recall@3 of 83.33%.

## 5. Results Analysis

### BM25

BM25 successfully retrieved relevant results for 10 out of 12 queries. It provides keyword-based retrieval and performed well on this evaluation set.

### Dense Retrieval

Dense retrieval using `HashingEmbedder` also achieved 10 successful queries out of 12.

Its performance was identical to BM25 on the tested queries.

### Hybrid Retrieval

Hybrid retrieval using RRF achieved the same Recall@3 as both individual retrieval approaches.

Although it combines sparse and dense retrieval signals, it did not produce a measurable improvement on this particular evaluation dataset.

This result does not mean that hybrid retrieval is ineffective in general. It only indicates that no improvement was observed under the current dataset, configuration, and evaluation criteria.

## 6. Missed Queries Analysis

The three retrieval approaches missed the same two queries:

- **q03:** Related to the tenant's termination notice period.
- **q12:** Related to the governing law and competent court.

Both queries concern specific legal provisions.

Their failure suggests that retrieving precise legal information remains a challenge for the current retrieval configuration. However, the identical results alone are not sufficient to identify the exact technical cause of these failures.

Further inspection of the retrieved chunks and relevant document ranges would be needed to determine why these queries were missed.

## 7. Limitations

The evaluation has several limitations:

1. The dataset contains only 8 contracts and 12 queries.
2. Dense retrieval uses `HashingEmbedder`, which is the embedding implementation used in this experiment.
3. The results depend on the selected chunking configuration.
4. Recall@3 measures whether a relevant result appears in the top three, but does not measure the quality of the generated answer.
5. The evaluation does not establish how the approaches would perform on larger or different legal document collections.

Therefore, the results should be interpreted within the scope of this evaluation.

## 8. Potential Improvements and Future Experiments

The following experiments could help improve retrieval performance:

- Test a stronger semantic embedding model.
- Experiment with different chunk sizes and overlap values.
- Add contextual information to chunk headers.
- Evaluate a reranker to improve the ordering of retrieved candidates.
- Inspect the failed queries and their retrieved chunks to identify specific retrieval weaknesses.

Each experiment should be evaluated using the same Recall@3 methodology to make the results comparable.

## 9. Conclusion

BM25, Dense retrieval, and Hybrid retrieval all achieved a Recall@3 of 83.33% on the current evaluation dataset.

Hybrid retrieval did not outperform either individual approach in this experiment.

The results provide a baseline for future improvements, particularly in retrieving precise legal provisions.
