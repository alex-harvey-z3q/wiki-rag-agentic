from __future__ import annotations

from openai import OpenAI

from ... import config


class OpenAILLMProvider:
    def __init__(self) -> None:
        if not config.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        self._client = OpenAI(api_key=config.OPENAI_API_KEY)

    def answer_with_evidence(self, question: str, evidence_items: list[dict]) -> str:
        system = (
            "You are a careful assistant answering questions using ONLY the provided evidence excerpts from Wikipedia. "
            "If the evidence is insufficient, say you don't know and suggest what page or section would be needed. "
            "Always include citations like [1], [2] corresponding to the evidence list."
        )

        evidence_block = "\n\n".join(
            f"[{i+1}] {e['page']} — {e['section']}\nURL: {e['url']}\nExcerpt: {e['excerpt']}"
            for i, e in enumerate(evidence_items)
        )

        user = f"Question: {question}\n\nEvidence:\n{evidence_block}"

        resp = self._client.chat.completions.create(
            model=config.OPENAI_CHAT_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=config.TEMPERATURE,
        )
        return resp.choices[0].message.content or ""
