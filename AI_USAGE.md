# AI usage

## Tools I used, and for what

I used ChatGPT to understand the project requirements, develop and review implementation logic, debug errors, and clarify the behavior of the retrieval components. I used VS Code and PowerShell to write and run the code, `uv` to manage the Python environment, and `pytest` to test the implementation. I also used a local Python evaluation script to measure Recall@3 for BM25, Dense, and Hybrid retrieval.

## Where AI-written chunking or BM25 code broke one of the spec's rules

The AI-assisted chunking implementation initially had two issues. First, it used `start_offset` and `end_offset` instead of the required `start` and `end` fields defined in `types.py`. Pytest exposed this through a `TypeError`. Second, an earlier version had a loop that failed to make progress, causing execution to get stuck. I corrected these issues and reran the tests.

For BM25, I reviewed the implementation and corrected issues during development, but I did not identify a confirmed BM25 formula violation of the specification.

## My recall@3 table (from EVAL.md) and why hybrid did or did not win

| Retriever                    | recall@3       | queries missed |

|------------------------------|----------------|-----------------|
| BM25 only                    | 0.8333 (10/12) | q03, q12        |
| Dense only (HashingEmbedder) | 0.8333 (10/12) | q03, q12        |
| Hybrid (RRF)                 | 0.8333 (10/12) | q03, q12        |

Hybrid retrieval did not outperform BM25 or Dense retrieval because all three achieved the same Recall@3 of 83.33% and missed the same two queries.
