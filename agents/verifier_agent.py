"""Verifier / Critic Agent — checks solution correctness and triggers HITL."""
import json
import re
from groq import Groq
from utils.config import GROQ_API_KEY, HITL_CONFIDENCE_THRESHOLD

client = Groq(api_key=GROQ_API_KEY)


VERIFIER_PROMPT = """You are a Math Verifier Agent. Your job is to critically check a proposed solution.

Problem:
{problem_text}

Topic: {topic}

Proposed Solution:
{solution_json}

Your job:
1. Verify the final answer is mathematically correct
2. Check for domain/range violations (e.g., log of negative number)
3. Check unit consistency and boundary conditions
4. Check if any step has a logical leap or error
5. Check edge cases: what if variables are 0 or negative?
6. Assign a confidence score (0.0 to 1.0)

Return ONLY a valid JSON:
{{
  "is_correct": true,
  "confidence": 0.95,
  "verified_answer": "confirmed or corrected answer",
  "issues_found": [],
  "corrections": [],
  "edge_cases_checked": ["list of edge cases considered"],
  "domain_check": "passed|failed|not_applicable",
  "hitl_recommended": false,
  "hitl_reason": "why human review is recommended (empty if not needed)"
}}

Rules:
- Set hitl_recommended: true if confidence < {threshold}
- Set hitl_recommended: true if is_correct is false
- Be critical but fair — don't reject correct solutions
"""


def run_verifier_agent(parsed_problem: dict, solution: dict) -> dict:
    """
    Verify the solution and decide if HITL is needed.
    Returns verification dict.
    """
    trace = {"agent": "Verifier Agent", "steps": []}

    try:
        prompt = VERIFIER_PROMPT.format(
            problem_text=parsed_problem.get("problem_text", ""),
            topic=parsed_problem.get("topic", "math"),
            solution_json=json.dumps(solution, indent=2),
            threshold=HITL_CONFIDENCE_THRESHOLD,
        )

        trace["steps"].append("🔎 Verifying solution correctness")
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        raw_response = response.choices[0].message.content.strip()

        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON in verifier response")

        verification = json.loads(json_match.group())

        # Safety check: always recommend HITL if confidence below threshold
        if verification.get("confidence", 1.0) < HITL_CONFIDENCE_THRESHOLD:
            verification["hitl_recommended"] = True
            if not verification.get("hitl_reason"):
                verification["hitl_reason"] = (
                    f"Confidence ({verification['confidence']:.0%}) below threshold "
                    f"({HITL_CONFIDENCE_THRESHOLD:.0%})"
                )

        trace["steps"].append(f"✅ Correct: {verification.get('is_correct')}")
        trace["steps"].append(f"📊 Confidence: {verification.get('confidence', 0):.0%}")
        if verification.get("hitl_recommended"):
            trace["steps"].append(f"⚠️ HITL recommended: {verification.get('hitl_reason', '')}")
        trace["output"] = verification
        trace["success"] = True

        return {"result": verification, "trace": trace}

    except Exception as e:
        fallback = {
            "is_correct": None,
            "confidence": 0.5,
            "verified_answer": solution.get("final_answer", "N/A"),
            "issues_found": [f"Verifier error: {str(e)}"],
            "corrections": [],
            "edge_cases_checked": [],
            "domain_check": "not_applicable",
            "hitl_recommended": True,
            "hitl_reason": f"Verifier encountered an error: {str(e)}",
        }
        trace["steps"].append(f"❌ Verifier error: {str(e)}")
        trace["success"] = False
        return {"result": fallback, "trace": trace}
