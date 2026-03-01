from __future__ import annotations

import logging

from fastapi import FastAPI, HTTPException

from . import config
from .db import connect, fetch_evidence
from .llm import answer_with_evidence, embed_text
from .models import AskRequest, AskResponse, EvidenceItem

logger = logging.getLogger("wiki_rag_api")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="wiki-rag API")


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="question is required")

    try:
        q_emb = embed_text(question)
    except Exception as e:  # noqa: BLE001
        logger.exception("Embedding failed")
        raise HTTPException(status_code=500, detail=f"embedding failed: {e}")

    try:
        conn = connect()
    except Exception as e:  # noqa: BLE001
        logger.exception("DB connection failed")
        raise HTTPException(status_code=500, detail=f"db connect failed: {e}")

    try:
        rows = fetch_evidence(conn, q_emb, config.TOP_K)
    except Exception as e:  # noqa: BLE001
        logger.exception("DB query failed")
        raise HTTPException(status_code=500, detail=f"db query failed: {e}")
    finally:
        try:
            conn.close()
        except Exception:  # noqa: BLE001
            pass

    if not rows:
        raise HTTPException(status_code=404, detail="no evidence found")

    evidence: list[EvidenceItem] = []
    evidence_payload: list[dict] = []

    for r in rows:
        excerpt = (r.text or "").strip()
        if len(excerpt) > config.MAX_EVIDENCE_CHARS:
            excerpt = excerpt[: config.MAX_EVIDENCE_CHARS].rstrip() + "…"

        item = EvidenceItem(
            page=r.page_title,
            section=r.section_title,
            url=r.url,
            revision_id=r.revision_id,
            excerpt=excerpt,
        )
        evidence.append(item)
        evidence_payload.append(item.model_dump())

    try:
        answer = answer_with_evidence(question, evidence_payload)
    except Exception as e:  # noqa: BLE001
        logger.exception("LLM answer failed")
        raise HTTPException(status_code=500, detail=f"llm failed: {e}")

    return AskResponse(answer=answer, evidence=evidence)
