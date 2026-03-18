from __future__ import annotations

from llama_index.core.llms import ChatMessage
from llama_index.llms.bedrock_converse import BedrockConverse

from ... import config


class BedrockClaudeProvider:
    def __init__(self) -> None:
        kwargs: dict = {
            "model": config.BEDROCK_CHAT_MODEL_ID,
            "region_name": config.AWS_REGION,
            "temperature": config.TEMPERATURE,
        }
        if config.AWS_PROFILE:
            kwargs["profile_name"] = config.AWS_PROFILE
        self._llm = BedrockConverse(**kwargs)

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

        resp = self._llm.chat(
            [
                ChatMessage(role="system", content=system),
                ChatMessage(role="user", content=user),
            ]
        )
        return resp.message.content if resp.message and resp.message.content else ""
