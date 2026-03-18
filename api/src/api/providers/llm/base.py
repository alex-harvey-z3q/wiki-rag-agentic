from __future__ import annotations

from typing import Protocol


class LLMProvider(Protocol):
    def answer_with_evidence(self, question: str, evidence_items: list[dict]) -> str: ...
