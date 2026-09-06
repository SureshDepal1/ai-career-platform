def build_skill_gap_prompt(user, career, skill_gaps):
    prompt = f"""
You are an AI career advisor.

Analyze the following student's career goal and skill gaps.

Target Career:
{career.title}

Student:
{user.username}

Skill Gaps:
"""

    for item in skill_gaps:
        prompt += f"""
- {item['skill']['name']}
  Required Level: {item['required_importance']}
  Current Level: {item['current_proficiency']}
  Gap: {item['gap']}
  Status: {item['status']}
"""

    prompt += """
Based on this information:

1. Explain the student's biggest skill gaps.
2. Identify which skills should be learned first.
3. Suggest a practical learning order.
4. Give advice for becoming job-ready.

Keep the response practical and easy to understand.
"""

    return prompt