from fastapi import FastAPI
from .retrieval import retrieve
from .llm import answer_with_evidence

app = FastAPI()

@app.get("/query")
def query(q: str):
    ctx = retrieve(q)
    answer = answer_with_evidence(q, ctx)
    return {"answer": answer}
