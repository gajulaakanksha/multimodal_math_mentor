"""Intent Router Agent — classifies problem and decides workflow routing."""
import json
import re
from groq import Groq
from utils.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


ROUTER_PROMPT = """You are an Intent Router Agent for a Math Mentor system.

Given a structured math problem, you must decide the optimal solving strategy.

Problem:
{problem_json}

Available tools:
- "sympy_solver": for symbolic algebra, solving equations, finding roots
- "sympy_diff": for differentiation problems
- "sympy_integrate": for integration problems
- "sympy_limit": for limit problems
- "sympy_evaluate": for numerical evaluation
- "rag_only": when only looking up formulas/applying templates
- "llm_only": for word problems, logic-based, or when symbolic tools won't help

Return ONLY a valid JSON object:
{{
  "problem_type": "equation|optimization|limit|derivative|integral|probability|combinatorics|matrix|proof|word_problem|other",
  "difficulty": "easy|medium|hard",
  "tools_to_use": ["list", "of", "tools"],
  "rag_query": "optimized search query to find relevant knowledge base chunks",
  "solving_strategy": "brief description of how to approach this problem",
  "expected_answer_type": "numeric|symbolic|fraction|proof|multiple_choice",
  "solution_notes": "any domain restrictions or special cases to watch for"
}}
"""


def run_router_agent(parsed_problem: dict) -> dict:
    """
    Route the parsed problem to the right tools and strategy.
    Returns routing plan dict.
    """
    trace = {"agent": "Intent Router Agent", "steps": []}

    try:
        problem_json = json.dumps(parsed_problem, indent=2)
        prompt = ROUTER_PROMPT.format(problem_json=problem_json)

        trace["steps"].append(f"Routing problem of type: {parsed_problem.get('topic', 'unknown')}")
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        raw_response = response.choices[0].message.content.strip()

        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON in router response")

        routing = json.loads(json_match.group())
        trace["steps"].append(f"Problem type: {routing.get('problem_type')}")
        trace["steps"].append(f"Tools: {routing.get('tools_to_use')}")
        trace["steps"].append(f"Strategy: {routing.get('solving_strategy', '')[:100]}")
        trace["output"] = routing
        trace["success"] = True

        return {"result": routing, "trace": trace}

    except Exception as e:
        fallback = {
            "problem_type": parsed_problem.get("topic", "other"),
            "difficulty": "medium",
            "tools_to_use": ["rag_only"],
            "rag_query": parsed_problem.get("problem_text", ""),
            "solving_strategy": "Use knowledge base to find relevant formulas and solve step-by-step",
            "expected_answer_type": "numeric",
            "solution_notes": "",
        }
        trace["steps"].append(f"Routing error: {str(e)} — using fallback")
        trace["success"] = False
        return {"result": fallback, "trace": trace}
