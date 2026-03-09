"""Parser Agent — cleans raw input and structures it into a math problem JSON."""
import json
import re
from groq import Groq
from utils.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


PARSER_PROMPT = """You are a Math Parser Agent. Your job is to analyze raw text (which may come from OCR, speech-to-text, or typed input) and convert it into a structured math problem.

Raw input: {raw_input}

Instructions:
1. Clean up any OCR/ASR artifacts (garbled text, symbols, repeated chars)
2. Identify the core math question
3. Determine the topic: one of [algebra, probability, calculus, linear_algebra, trigonometry, combinatorics, other]
4. Extract variables and any constraints mentioned
5. Determine if clarification is needed (e.g., input is too ambiguous, incomplete, or garbled beyond recovery)

Return ONLY a valid JSON object with this exact structure:
{{
  "problem_text": "clean, complete math problem statement",
  "topic": "algebra|probability|calculus|linear_algebra|trigonometry|combinatorics|other",
  "variables": ["list", "of", "variables"],
  "constraints": ["list of constraints or conditions, e.g., x > 0"],
  "given_values": {{"key": "value pairs of known quantities"}},
  "question_goal": "what the problem is asking to find or prove",
  "needs_clarification": false,
  "clarification_reason": "reason why clarification is needed, or empty string if not needed",
  "confidence": 0.95
}}

Rules:
- If the input is mostly garbled and unrecoverable, set needs_clarification to true
- confidence reflects how sure you are about the parsing (0.0 to 1.0)
- Do NOT add any text before or after the JSON
"""


def run_parser_agent(raw_input: str) -> dict:
    """
    Parse raw input text into a structured math problem.
    Returns the parsed problem dict.
    """
    trace = {"agent": "Parser Agent", "input": raw_input[:200], "steps": []}

    try:
        prompt = PARSER_PROMPT.format(raw_input=raw_input)
        
        trace["steps"].append("Calling Groq to parse and structure problem")
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        raw_response = response.choices[0].message.content.strip()

        # Extract JSON from response (handle markdown code blocks)
        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON found in parser response")

        parsed = json.loads(json_match.group())
        trace["steps"].append(f"Parsed topic: {parsed.get('topic', 'unknown')}")
        trace["steps"].append(f"Needs clarification: {parsed.get('needs_clarification', False)}")
        trace["output"] = parsed
        trace["success"] = True

        return {"result": parsed, "trace": trace}

    except Exception as e:
        fallback = {
            "problem_text": raw_input,
            "topic": "other",
            "variables": [],
            "constraints": [],
            "given_values": {},
            "question_goal": "Solve the given problem",
            "needs_clarification": True,
            "clarification_reason": f"Parser error: {str(e)}",
            "confidence": 0.3,
        }
        trace["steps"].append(f"Error: {str(e)} — using fallback")
        trace["success"] = False
        return {"result": fallback, "trace": trace}
