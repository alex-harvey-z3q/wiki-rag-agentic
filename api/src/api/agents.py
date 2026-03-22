from __future__ import annotations

from .llm import invoke_claude


def plan_task(question: str) -> str:
    system_prompt = (
        "You are Planner, a software planning agent. Produce a concise, structured "
        "implementation plan for a small Python application. Be deterministic. "
        "Do not write code."
    )
    user_prompt = (
        f"Task: {question}\n\n"
        "Return these sections only:\n"
        "1. Files\n"
        "2. Data structures\n"
        "3. Game rules and flow\n"
        "4. Test strategy\n"
        "Keep it compact and implementation-ready."
    )
    return invoke_claude(system_prompt, user_prompt, max_tokens=700, temperature=0.0)



def implement_task(question: str, plan: str) -> str:
    system_prompt = (
        "You are Implementer, a Python coding agent. Generate a complete, runnable, "
        "terminal-based Python application using standard library only unless the "
        "task explicitly requires otherwise. Output only code files using the exact "
        "separator format === filename ===."
    )
    user_prompt = (
        f"Task: {question}\n\n"
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
        "Output multiple files in one plain-text response using separators like:\n"
        "=== main.py ===\n"
        "...\n"
        "=== game.py ===\n"
        "...\n"
        "=== test_game.py ==="
    )
    return invoke_claude(system_prompt, user_prompt, max_tokens=4000, temperature=0.0)



def review_code(question: str, code: str) -> str:
    system_prompt = (
        "You are Reviewer, a software review agent. Review generated Python code for "
        "correctness and completeness. Be specific, concise, and deterministic."
    )
    user_prompt = (
        f"Task: {question}\n\n"
        "Review the generated application. Focus on:\n"
        "- correctness\n"
        "- game logic\n"
        "- edge cases\n"
        "- structure and readability\n"
        "- test coverage\n\n"
        "Return short bullet points only.\n\n"
        f"Code:\n{code}"
    )
    return invoke_claude(system_prompt, user_prompt, max_tokens=900, temperature=0.0)



def run_workflow(question: str) -> dict[str, str]:
    plan = plan_task(question)
    code = implement_task(question, plan)
    review = review_code(question, code)
    return {"plan": plan, "code": code, "review": review}
