# AGENTS.md — Bayyina W4

## Project Context
- This repository implements Bayyina, a bilingual Arabic/English contract retrieval system.
- Read `README.md` before changing implementation behavior.
- Follow the exact specifications in `README.md`; do not replace them with assumptions.

## Environment
- Use Python 3.12 (`>=3.12,<3.13`).
- Use `uv` for environment and dependency management.
- Run tests with `uv run pytest`.
- Run `git diff --check` before committing changes.
- Do not modify dependencies in `pyproject.toml` or `uv.lock`.

## Protected Files and Data
- Do not edit `bayyina/types.py`; its definitions are provided by DSC.
- Do not edit `bayyina/embedder.py`; the grader restores the DSC version.
- Treat `data/contracts/` and `data/queries.jsonl` as provided evaluation inputs.
- Do not modify public tests to make an implementation pass.

## Implementation Rules
- Preserve exact source offsets when chunking and retrieving text.
- Follow the normalization mappings and tokenization rules in `README.md`.
- Implement BM25 using the specified formula and deterministic tie-breaking.
- Implement RRF and hybrid retrieval using the specified ranking rules.
- Keep citation offsets and quoted text tied to the original document.
- Do not add external search libraries such as `rank_bm25` or FAISS.
- Do not assume that a reranker or external embedding model is available.

## Models and Evaluation
- The provided offline embedding implementation is `HashingEmbedder(dim=512, n=3)`.
- No external embedding model or model version is specified as approved by this repository.
- `EVAL.md` documents the evaluation method and recorded Recall@3 results.
- No standalone evaluation script or evaluation run command currently exists in the repository.
- Do not invent evaluation commands or claim that documented results were freshly reproduced.
- Keep evaluation comparisons consistent with the documented dataset and chunking configuration.

## AI Agent Working Rules
- Inspect relevant files and existing interfaces before proposing code changes.
- Make the smallest change that satisfies the requirement.
- Do not silently change public interfaces, dependencies, or protected files.
- Explain assumptions and identify missing information instead of guessing.
- Run relevant tests after changes and report actual results.
- Never claim a test or evaluation passed unless it was actually executed.
- Review the final diff before suggesting a commit.
