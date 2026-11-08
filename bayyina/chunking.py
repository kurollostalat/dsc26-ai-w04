"""Offset-preserving chunker. You write this file. See README.md for the seven rules."""
from __future__ import annotations

from bayyina.types import Chunk


def chunk_text(doc_id: str, text: str, max_chars: int = 500, overlap: int = 50) -> list[Chunk]:

            if max_chars <= 0 or overlap < 0 or overlap >= max_chars:
                raise ValueError("max_chars must be > 0 and 0 <= overlap < max_chars")

            if not text.strip():
                return []

            chunks = []
            start = 0

            while start < len(text):

                remaining_length = len(text) - start

                # Case 1: Remaining text fits in one chunk
                if remaining_length <= max_chars:

                    original_chunk = text[start:]
                    chunk_content = original_chunk.strip()

                    if chunk_content:
                        removed_chars = (
                            len(original_chunk) - len(original_chunk.lstrip())
                        )

                        start_offset = start + removed_chars
                        end_offset = start_offset + len(chunk_content)

                        chunk = Chunk(
                            chunk_id=f"{doc_id}#{len(chunks)}",
                            doc_id=doc_id,
                            text=chunk_content,
                            start=start_offset,
                            end=end_offset
                        )

                        chunks.append(chunk)

                    break

                # Case 2: Remaining text is longer than max_chars
                window = text[start:start + max_chars]
                min_cut = max_chars // 2

                paragraph_cuts = []
                sentence_cuts = []
                whitespace_cuts = []

                for index, char in enumerate(window):

                    cut = index + 1

                    # Paragraph boundary
                    if window[index:index + 2] == "\n\n":
                        paragraph_cut = index + 2

                        if min_cut <= paragraph_cut <= max_chars:
                            paragraph_cuts.append(paragraph_cut)

                    # Sentence boundary
                    if char in [".", "!", "?", "؟", "۔", "\n"]:
                        if min_cut <= cut <= max_chars:
                            sentence_cuts.append(cut)

                    # Whitespace boundary
                    if char.isspace():
                        if min_cut <= cut <= max_chars:
                            whitespace_cuts.append(cut)

                # Choose the best cut according to priority
                if paragraph_cuts:
                    best_cut = max(paragraph_cuts)

                elif sentence_cuts:
                    best_cut = max(sentence_cuts)

                elif whitespace_cuts:
                    best_cut = max(whitespace_cuts)

                else:
                    best_cut = max_chars

                # Create chunk content
                original_chunk = text[start:start + best_cut]
                chunk_content = original_chunk.strip()

                if not chunk_content:
                    start += best_cut
                    continue

                removed_chars = (
                    len(original_chunk) - len(original_chunk.lstrip())
                )

                start_offset = start + removed_chars
                end_offset = start_offset + len(chunk_content)

                chunk = Chunk(
                    doc_id=doc_id,
                    chunk_id=f"{doc_id}#{len(chunks)}",
                    start=start_offset,
                    end=end_offset,
                    text=chunk_content
                )

                chunks.append(chunk)

                # Determine whether the chunk ended in the middle of a word
                ended_mid_word = (
                    end_offset < len(text)
                    and not text[end_offset - 1].isspace()
                    and not text[end_offset].isspace()
                )

                if ended_mid_word:
                    next_start = max(
                        start_offset + 1,
                        end_offset - overlap
                    )

                else:
                    next_start = end_offset

                    while next_start < len(text) and text[next_start].isspace():
                        next_start += 1

                start = next_start

            return chunks
"""Split `text` into chunks whose offsets point into the ORIGINAL text.

    ValueError unless max_chars > 0 and 0 <= overlap < max_chars.
    """
