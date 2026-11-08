"""Citation checks. You write this file."""
from __future__ import annotations

from bayyina.types import Hit


def verify_citation(quote: str, document: str, start: int, end: int) -> bool:
    """Returns True if the quote is found in document[start:end], else False."""
    if start < 0 or end > len(document) or start >= end:
        return False

    if not quote.strip():
        return False

    normalized_quote = " ".join(quote.split())
    normalized_document = " ".join(document[start:end].split())

    return normalized_quote in normalized_document

def format_citation(hit: Hit, max_quote: int = 160) -> str:
    """[doc_id:start-end] "quote" """
    quote=" ".join(hit.text.split())
    if len(quote) > max_quote:
        quote = quote[:max_quote].rstrip() + "..."
    return f"[{hit.doc_id}:{hit.start}-{hit.end}] \"{quote}\""
