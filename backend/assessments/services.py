import json
import re

from ai_services.openai_service import generate_career_analysis


def _parse_json(text):
    cleaned = text.strip()
    cleaned = re.sub(r'^```(?:json)?\s*|\s*```$', '', cleaned, flags=re.IGNORECASE)
    return json.loads(cleaned)


def generate_interview_question(career, difficulty, question_number):
    prompt = f"""
You are a professional technical interviewer. Generate one {difficulty} interview question
for a candidate targeting the career "{career.title}". This is question {question_number} of a
multi-question interview. Return only valid JSON with this shape:
{{"question": "string"}}
"""
    result = _parse_json(generate_career_analysis(prompt))
    question = result.get('question')
    if not question:
        raise ValueError('AI returned an empty interview question.')
    return question


def evaluate_interview_answer(career, difficulty, question, answer):
    prompt = f"""
Evaluate this candidate answer for a {difficulty} interview for "{career.title}".
Question: {question}
Answer: {answer}
Return only valid JSON with this exact shape:
{{
  "score": 0,
  "strengths": ["string"],
  "weaknesses": ["string"],
  "suggestions": ["string"],
  "better_answer": "string",
  "communication_feedback": "string",
  "technical_topics": ["string"]
}}
Score must be an integer from 0 to 100.
"""
    result = _parse_json(generate_career_analysis(prompt))
    result['score'] = max(0, min(int(result.get('score', 0)), 100))
    return result
