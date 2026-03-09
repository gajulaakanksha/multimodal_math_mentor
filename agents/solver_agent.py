"""Solver Agent — solves the problem using RAG context + SymPy tools."""
import json
import re
from groq import Groq
from utils.config import GROQ_API_KEY
from rag.retriever import retrieve, format_context
from utils.math_tools import compute_with_tool

client = Groq(api_key=GROQ_API_KEY)


SOLVER_PROMPT = """You are a Math Solver Agent specializing in JEE-level mathematics.

Problem:
{problem_text}

Topic: {topic}
Solving Strategy: {strategy}
Tools Used: {tool_results}

Relevant Knowledge Base Context:
{rag_context}

Similar Past Problems (from memory):
{memory_context}

Instructions:
1. Use the knowledge base context and past problems to inform your solution
2. Show your complete working step by step
3. Use the tool results (if any) to verify numerical answers
4. State any domain restrictions
5. Be precise — give exact answers (fractions, not decimals) when possible

Return ONLY a valid JSON object:
{{
  "final_answer": "the exact numerical or symbolic answer",
  "solution_steps": [
    "Step 1: ...",
    "Step 2: ...",
    "Step N: ..."
  ],
  "key_formulas_used": ["formula 1", "formula 2"],
  "tool_verification": "what the math tool confirmed (or 'N/A')",
  "answer_confidence": 0.9,
  "domain_restrictions": "any restrictions on variables or domain",
  "alternative_approach": "brief mention of another valid method if applicable"
}}
"""


def run_solver_agent(parsed_problem: dict, routing: dict, memory_results: list) -> dict:
    """
    Solve the problem using RAG, SymPy tools, and Gemini.
    Returns solution dict.
    """
    trace = {"agent": "Solver Agent", "steps": [], "retrieved_chunks": []}

    # Step 1: RAG retrieval
    rag_query = routing.get("rag_query", parsed_problem.get("problem_text", ""))
    trace["steps"].append(f"🔍 Retrieving context for: '{rag_query[:80]}...'")
    retrieved = retrieve(rag_query)
    trace["retrieved_chunks"] = retrieved
    rag_context = format_context(retrieved)

    # Step 2: Try SymPy tools
    tool_results = {}
    tools_to_use = routing.get("tools_to_use", [])
    problem_text = parsed_problem.get("problem_text", "")

    for tool in tools_to_use:
        if tool == "sympy_solver":
            trace["steps"].append("🔧 Running SymPy equation solver")
            # Try to extract equation from problem text
            eq_match = re.search(r'([^=\n]+=[^=\n]+)', problem_text)
            if eq_match:
                result = compute_with_tool("solve", {"equation": eq_match.group(), "variable": "x"})
                tool_results["equation_solver"] = result
        elif tool == "sympy_diff":
            trace["steps"].append("🔧 Running SymPy differentiation")
            # Extract expression to differentiate
            diff_match = re.search(r'differentiat\w+ (.+)', problem_text, re.IGNORECASE)
            if diff_match:
                result = compute_with_tool("differentiate", {"expression": diff_match.group(1)})
                tool_results["differentiation"] = result
        elif tool == "sympy_limit":
            trace["steps"].append("🔧 Running SymPy limit computation")
        elif tool == "sympy_evaluate":
            trace["steps"].append("🔧 Running SymPy numerical evaluation")

    # Step 3: Format memory context
    memory_context = "No similar problems found in memory."
    if memory_results:
        mem_lines = ["Found similar previously solved problems:"]
        for i, mem in enumerate(memory_results[:2]):
            mem_lines.append(f"\nPrevious Problem {i+1}: {mem.get('input_text', '')[:150]}")
            mem_lines.append(f"Previous Answer: {mem.get('answer', 'N/A')}")
        memory_context = "\n".join(mem_lines)
        trace["steps"].append(f"📚 Found {len(memory_results)} similar problem(s) in memory")

    # Step 4: Call Groq to solve
    trace["steps"].append("🤖 Calling Groq to solve with context")
    try:
        prompt = SOLVER_PROMPT.format(
            problem_text=problem_text,
            topic=parsed_problem.get("topic", "math"),
            strategy=routing.get("solving_strategy", ""),
            tool_results=json.dumps(tool_results, indent=2) if tool_results else "None",
            rag_context=rag_context,
            memory_context=memory_context,
        )

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        raw_response = response.choices[0].message.content.strip()

        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON in solver response")

        solution = json.loads(json_match.group())
        trace["steps"].append(f"✅ Final answer: {solution.get('final_answer', 'N/A')}")
        trace["steps"].append(f"📊 Solver confidence: {solution.get('answer_confidence', 'N/A')}")
        trace["output"] = solution
        trace["success"] = True

        return {"result": solution, "trace": trace, "retrieved_chunks": retrieved}

    except Exception as e:
        fallback = {
            "final_answer": "Could not compute answer",
            "solution_steps": [f"Error during solving: {str(e)}"],
            "key_formulas_used": [],
            "tool_verification": "N/A",
            "answer_confidence": 0.1,
            "domain_restrictions": "",
            "alternative_approach": "",
        }
        trace["steps"].append(f"❌ Solver error: {str(e)}")
        trace["success"] = False
        return {"result": fallback, "trace": trace, "retrieved_chunks": retrieved}
