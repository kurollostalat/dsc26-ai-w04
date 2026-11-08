# AI Usage and Development Reflection

## 1. Tools Used

The following tools were used during development:

| Tool | Purpose |
|---|---|
| ChatGPT | Understanding requirements, discussing implementation logic, reviewing code, and debugging issues. |
| VS Code | Writing and editing Python files. |
| PowerShell | Running commands and managing the project locally. |
| Python | Implementing and testing retrieval components. |
| uv | Managing the Python environment and running project commands. |
| pytest | Running the project's automated tests. |
| Git and GitHub | Tracking changes, committing updates, and pushing the project repository. |

A local Python evaluation script was also used to compare BM25, Dense, and Hybrid retrieval using Recall@3.

## 2. How AI Was Used

ChatGPT was used as a development assistant throughout the project.

Its main contributions included:

- Helping interpret the project requirements and technical specifications.
- Discussing the implementation of Arabic normalization and tokenization.
- Reviewing the chunking strategy and its boundary conditions.
- Explaining BM25 scoring and Reciprocal Rank Fusion.
- Helping investigate errors and understand test failures.
- Reviewing evaluation results and improving technical documentation.

AI-generated suggestions were not treated as automatically correct. The implementation was tested locally, and issues identified during development were corrected before continuing.

## 3. Chunking Issues and Lessons Learned

The AI-assisted chunking implementation initially had two issues.

### Issue 1: Incorrect Offset Field Names

An earlier implementation used `start_offset` and `end_offset` instead of the required `start` and `end` fields defined in `types.py`.

This caused a `TypeError` during testing.

**Correction:** The implementation was updated to use the required field names.

**Lesson learned:** Implementation details must follow the project's existing data structures and type definitions rather than relying on assumed field names.

### Issue 2: Loop That Failed to Make Progress

An earlier version of the chunking logic contained a loop that failed to advance correctly, causing execution to get stuck.

**Correction:** The loop logic was reviewed and corrected to ensure that processing makes progress.

**Lesson learned:** Chunking algorithms must handle edge cases carefully and guarantee that every iteration advances toward completion.

## 4. BM25 Implementation and Verification

ChatGPT was used to discuss the BM25 implementation and understand its scoring components, including:

- Term frequency (TF).
- Inverse document frequency (IDF).
- Document length normalization.
- Final relevance scoring.

The implementation was reviewed against the project specification.

I also performed local checks comparing BM25 scores against an independently calculated reference formula using multiple parameter configurations.

These checks passed.

I did not identify a confirmed BM25 formula violation during development. Therefore, I am not claiming that a specific BM25 formula bug was found and fixed.

**Lesson learned:** Understanding the mathematical formula and independently checking its output are important steps when implementing a retrieval algorithm.

## 5. Evaluation Findings

The evaluation compared BM25, Dense retrieval using `HashingEmbedder`, and Hybrid retrieval using RRF.

| Retriever | Recall@3 | Successful Queries | Queries Missed |
|---|---:|---:|---|
| BM25 only | 0.8333 (10/12) | 10 | q03, q12 |
| Dense only (HashingEmbedder) | 0.8333 (10/12) | 10 | q03, q12 |
| Hybrid (RRF) | 0.8333 (10/12) | 10 | q03, q12 |

All three approaches achieved the same Recall@3 of 83.33%.

Hybrid retrieval did not outperform BM25 or Dense retrieval on this dataset because all three approaches retrieved relevant results for the same 10 queries and missed the same two queries.

The missed queries were:

- q03: Tenant termination notice period.
- q12: Governing law and competent court.

This finding helped identify precise legal provisions as an area that could benefit from further retrieval improvements.

## 6. What I Learned

Working on this project helped me understand several practical concepts:

1. **Specification-driven development:** Small differences in field names and expected behavior can cause implementation failures.
2. **Chunking trade-offs:** Chunk size, overlap, and boundary selection affect how document content is retrieved.
3. **Sparse retrieval:** BM25 provides a structured keyword-based approach to ranking documents.
4. **Dense retrieval:** Semantic retrieval provides a different retrieval signal from keyword matching.
5. **Hybrid retrieval:** Combining retrieval methods does not automatically guarantee better results.
6. **Testing and validation:** Passing a basic test suite is useful, but additional edge-case and reference-based tests provide stronger confidence.
7. **Evaluation:** Retrieval improvements should be supported by measurable results rather than assumptions.

## 7. Limitations and Responsible AI Use

AI assistance was useful for understanding requirements, reviewing implementation decisions, and debugging.

However, AI-generated suggestions can contain incorrect assumptions or implementation errors.

For this reason:

- The project requirements and existing type definitions were used as the reference.
- Code was executed and tested locally.
- Errors identified during development were reviewed and corrected.
- Evaluation results were based on the local evaluation script rather than assumed AI-generated results.
- No claim was made that Hybrid retrieval was better when the measured results showed otherwise.

The final implementation and evaluation should be judged by the actual code, tests, and measured results.

## 8. Final Reflection

This project demonstrated that implementing a retrieval system involves more than writing individual algorithms.

It requires understanding specifications, handling edge cases, validating mathematical logic, testing retrieval behavior, and documenting the results honestly.

One important takeaway was that combining multiple retrieval methods does not necessarily improve performance. The evaluation results showed the importance of measuring each approach under the same conditions before deciding whether a change is beneficial.
