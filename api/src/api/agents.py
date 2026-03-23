from __future__ import annotations

from .llm import invoke_claude
from .retrieval import retrieve


def _format_evidence(evidence: list[dict]) -> str:
    if not evidence:
        return "No retrieved evidence."
    parts = []
    for i, item in enumerate(evidence, start=1):
        parts.append(
            f"[{i}] {item['page']} — {item['section']}\n"
            f"URL: {item['url']}\n"
            f"Excerpt: {item['excerpt']}"
        )
    return "\n\n".join(parts)


def plan_task(question: str, evidence: list[dict]) -> str:
    system_prompt = (
        "You are Planner, a software planning agent. Produce a concise, structured "
        "implementation plan for a small Python application. Use the retrieved "
        "evidence for domain rules and behaviour. Be deterministic. Do not write code."
    )
    user_prompt = (
        f"Task: {question}\n\n"
        f"Retrieved evidence:\n{_format_evidence(evidence)}\n\n"
        "Return these sections only:\n"
        "1. Files\n"
        "2. Data structures\n"
        "3. Game rules and flow\n"
        "4. Test strategy\n"
        "Keep it compact and implementation-ready. Prefer evidence-grounded rules."
    )
    return invoke_claude(system_prompt, user_prompt, max_tokens=900, temperature=0.0)


def implement_task(question: str, evidence: list[dict], plan: str) -> str:
    system_prompt = (
        "You are Implementer, a Python coding agent. Generate a complete, runnable, "
        "terminal-based Python application using standard library only unless the "
        "task explicitly requires otherwise. Use the retrieved evidence only for "
        "gameplay rules and conventions. Output only code files using the exact "
        "separator format === filename ===."
    )
    user_prompt = (
        f"Task: {question}\n\n"
        f"Retrieved evidence:\n{_format_evidence(evidence)}\n\n"
        f"Plan:\n{plan}\n\n"
        "Generate the full application now. Requirements:\n"
        "- Python only\n"
        "- standard library preferred\n"
        "- playable in the terminal\n"
        "- configurable board width, height, and mine count\n"
        "- reveal cells\n"
        "- flag and unflag cells\n"
        "- recursive reveal for empty areas\n"
        "- win/loss detection\n"
        "- text board rendering\n"
        "- restartable game loop\n"
        "- modular, readable, compact\n"
        "- include basic tests for core game logic\n\n"
        "Use the evidence to keep gameplay behaviour aligned with Minesweeper rules, "
        "but choose reasonable Python structure yourself.\n\n"
        "Output multiple files in one plain-text response using separators like:\n"
        "=== main.py ===\n"
        "...\n"
        "=== game.py ===\n"
        "...\n"
        "=== test_game.py ==="
    )
    return invoke_claude(system_prompt, user_prompt, max_tokens=4500, temperature=0.0)


def review_code(question: str, evidence: list[dict], code: str) -> str:
    system_prompt = (
        "You are Reviewer, a software review agent. Review generated Python code for "
        "correctness and completeness. Check it against the retrieved evidence where "
        "that evidence describes gameplay rules. Be specific, concise, and deterministic."
    )
    user_prompt = (
        f"Task: {question}\n\n"
        f"Retrieved evidence:\n{_format_evidence(evidence)}\n\n"
        "Review the generated application. Focus on:\n"
        "- correctness\n"
        "- game logic\n"
        "- mismatches with retrieved gameplay evidence\n"
        "- edge cases\n"
        "- structure and readability\n"
        "- test coverage\n\n"
        "Return short bullet points only.\n\n"
        f"Code:\n{code}"
    )
    return invoke_claude(system_prompt, user_prompt, max_tokens=1000, temperature=0.0)


def run_workflow(question: str) -> dict[str, object]:
    evidence = retrieve(question)
    plan = plan_task(question, evidence)
    code = implement_task(question, evidence, plan)
    review = review_code(question, evidence, code)
    return {
        "evidence": evidence,
        "plan": plan,
        "code": code,
        "review": review,
    }
