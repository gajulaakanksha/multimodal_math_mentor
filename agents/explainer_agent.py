"""Explainer / Tutor Agent — produces clear, student-friendly step-by-step explanation."""
import json
import re
from groq import Groq
from utils.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


EXPLAINER_PROMPT = """You are a friendly Math Tutor Agent for JEE students. Your job is to explain a math solution clearly and engagingly.

Problem:
{problem_text}

Topic: {topic}

Verified Solution:
{solution_json}

Verification Notes:
{verification_notes}

Instructions:
1. Write a CLEAR, student-friendly explanation of how to solve this problem
2. Break it into numbered steps that are easy to follow
3. Explain WHY each step is done (not just what to do)
4. Mention the key formula or concept used at each step
5. Highlight any common mistakes students might make here
6. Add a concise summary at the end
7. Use simple language — imagine explaining to a 17-year-old student

Return ONLY a valid JSON object:
{{
  "title": "brief title for this explanation",
  "introduction": "1-2 sentences setting up the problem context",
  "steps": [
    {{
      "step_number": 1,
      "title": "Step title",
      "explanation": "What we do and WHY",
      "formula_used": "formula or concept applied (empty string if none)",
      "result": "result of this step"
    }}
  ],
  "final_answer": "the final answer stated clearly",
  "common_mistakes": ["mistake 1 to avoid", "mistake 2 to avoid"],
  "key_takeaway": "1-2 sentence summary of the most important lesson",
  "difficulty_level": "easy|medium|hard",
  "topics_covered": ["topic1", "topic2"]
}}
"""


def run_explainer_agent(parsed_problem: dict, solution: dict, verification: dict) -> dict:
    """
    Generate student-friendly step-by-step explanation.
    Returns explanation dict.
    """
    trace = {"agent": "Explainer Agent", "steps": []}

    try:
        # Use verified answer if available and different from solver
        verified_answer = verification.get("verified_answer", solution.get("final_answer", ""))
        if verified_answer and verified_answer != solution.get("final_answer"):
            solution_to_explain = {**solution, "final_answer": verified_answer}
        else:
            solution_to_explain = solution

        verification_notes = (
            f"Confidence: {verification.get('confidence', 'N/A')}\n"
            f"Issues found: {', '.join(verification.get('issues_found', [])) or 'None'}\n"
            f"Edge cases: {', '.join(verification.get('edge_cases_checked', [])) or 'None checked'}"
        )

        prompt = EXPLAINER_PROMPT.format(
            problem_text=parsed_problem.get("problem_text", ""),
            topic=parsed_problem.get("topic", "math"),
            solution_json=json.dumps(solution_to_explain, indent=2),
            verification_notes=verification_notes,
        )

        trace["steps"].append("📝 Generating student-friendly explanation")
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        raw_response = response.choices[0].message.content.strip()

        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON in explainer response")

        explanation = json.loads(json_match.group())
        num_steps = len(explanation.get("steps", []))
        trace["steps"].append(f"✅ Generated explanation with {num_steps} steps")
        trace["steps"].append(f"🎯 Key takeaway captured")
        trace["output"] = explanation
        trace["success"] = True

        return {"result": explanation, "trace": trace}

    except Exception as e:
        fallback = {
            "title": "Solution Explanation",
            "introduction": "Let's solve this problem step by step.",
            "steps": [
                {
                    "step_number": 1,
                    "title": "Direct Solution",
                    "explanation": str(solution.get("solution_steps", ["Solution computed"])),
                    "formula_used": "",
                    "result": solution.get("final_answer", "N/A"),
                }
            ],
            "final_answer": solution.get("final_answer", "N/A"),
            "common_mistakes": [],
            "key_takeaway": "Review the solution steps carefully.",
            "difficulty_level": "medium",
            "topics_covered": [parsed_problem.get("topic", "math")],
        }
        trace["steps"].append(f"❌ Explainer error: {str(e)}")
        trace["success"] = False
        return {"result": fallback, "trace": trace}
