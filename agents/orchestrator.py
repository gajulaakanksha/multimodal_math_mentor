"""Orchestrator — runs the complete multi-agent pipeline."""
from agents.parser_agent import run_parser_agent
from agents.router_agent import run_router_agent
from agents.solver_agent import run_solver_agent
from agents.verifier_agent import run_verifier_agent
from agents.explainer_agent import run_explainer_agent
from memory.memory_store import find_similar_problems, save_problem


def run_pipeline(raw_input: str, input_mode: str = "text") -> dict:
    """
    Run the complete 5-agent pipeline on raw input text.

    Returns a comprehensive result dict:
    {
        "parsed_problem": {...},
        "routing": {...},
        "solution": {...},
        "verification": {...},
        "explanation": {...},
        "retrieved_chunks": [...],
        "memory_results": [...],
        "agent_traces": [...],
        "hitl_needed": bool,
        "hitl_reason": str,
        "problem_id": int | None,
    }
    """
    result = {
        "parsed_problem": None,
        "routing": None,
        "solution": None,
        "verification": None,
        "explanation": None,
        "retrieved_chunks": [],
        "memory_results": [],
        "agent_traces": [],
        "hitl_needed": False,
        "hitl_reason": "",
        "problem_id": None,
        "error": None,
    }

    try:
        # ── Agent 1: Parser ──────────────────────────────────────────────────
        parser_out = run_parser_agent(raw_input)
        result["agent_traces"].append(parser_out["trace"])
        parsed_problem = parser_out["result"]
        result["parsed_problem"] = parsed_problem

        # HITL: Parser needs clarification
        if parsed_problem.get("needs_clarification"):
            result["hitl_needed"] = True
            result["hitl_reason"] = (
                parsed_problem.get("clarification_reason") or
                "Parser could not confidently interpret the problem"
            )
            return result  # Return early for HITL

        # ── Memory: Find similar past problems ───────────────────────────────
        memory_results = find_similar_problems(parsed_problem.get("problem_text", raw_input))
        result["memory_results"] = memory_results

        # ── Agent 2: Router ──────────────────────────────────────────────────
        router_out = run_router_agent(parsed_problem)
        result["agent_traces"].append(router_out["trace"])
        routing = router_out["result"]
        result["routing"] = routing

        # ── Agent 3: Solver ──────────────────────────────────────────────────
        solver_out = run_solver_agent(parsed_problem, routing, memory_results)
        result["agent_traces"].append(solver_out["trace"])
        solution = solver_out["result"]
        result["solution"] = solution
        result["retrieved_chunks"] = solver_out.get("retrieved_chunks", [])

        # ── Agent 4: Verifier ────────────────────────────────────────────────
        verifier_out = run_verifier_agent(parsed_problem, solution)
        result["agent_traces"].append(verifier_out["trace"])
        verification = verifier_out["result"]
        result["verification"] = verification

        # HITL: Verifier recommends review
        if verification.get("hitl_recommended"):
            result["hitl_needed"] = True
            result["hitl_reason"] = (
                verification.get("hitl_reason") or
                f"Verifier confidence: {verification.get('confidence', 0):.0%}"
            )

        # ── Agent 5: Explainer ───────────────────────────────────────────────
        explainer_out = run_explainer_agent(parsed_problem, solution, verification)
        result["agent_traces"].append(explainer_out["trace"])
        explanation = explainer_out["result"]
        result["explanation"] = explanation

        # ── Save to Memory ───────────────────────────────────────────────────
        problem_id = save_problem(
            input_text=raw_input,
            input_mode=input_mode,
            parsed_json=parsed_problem,
            retrieved_context=result["retrieved_chunks"],
            solution_json=solution,
            explanation_json=explanation,
            verifier_score=verification.get("confidence", 0.5),
        )
        result["problem_id"] = problem_id

    except Exception as e:
        result["error"] = str(e)
        result["hitl_needed"] = True
        result["hitl_reason"] = f"Pipeline error: {str(e)}"

    return result
