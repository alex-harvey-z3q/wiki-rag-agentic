from __future__ import annotations

from openai import OpenAI

from . import config


def embed_text(text: str) -> list[float]:
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    resp = client.embeddings.create(model=config.EMBED_MODEL, input=text)
    return list(resp.data[0].embedding)


def answer_with_evidence(question: str, evidence_items: list[dict]) -> str:
    client = OpenAI(api_key=config.OPENAI_API_KEY)

    system = (
        "You are a careful assistant answering questions using ONLY the provided evidence excerpts from Wikipedia. "
        "If the evidence is insufficient, say you don't know and suggest what page/section would be needed. "
        "Always include citations like [1], [2] corresponding to the evidence list."
    )

    evidence_block = "\n\n".join(
        f"[{i+1}] {e['page']} — {e['section']}\nURL: {e['url']}\nExcerpt: {e['excerpt']}"
        for i, e in enumerate(evidence_items)
    )

    user = f"Question: {question}\n\nEvidence:\n{evidence_block}"

    resp = client.chat.completions.create(
        model=config.CHAT_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.2,
    )

    return resp.choices[0].message.content or ""
