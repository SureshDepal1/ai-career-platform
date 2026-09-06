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


def build_learning_roadmap_prompt(user, career, skill_gaps):
    prompt = f"""
You are an AI learning roadmap advisor.

Create a personalized learning roadmap for a student who wants to become:

Target Career:
{career.title}

Student:
{user.username}

Current Skill Gaps:
"""

    for item in skill_gaps:
        if item['gap'] > 0:
            prompt += f"""
- {item['skill']['name']}
  Required Level: {item['required_importance']}
  Current Level: {item['current_proficiency']}
  Gap: {item['gap']}
  Status: {item['status']}
"""

    prompt += """
Create a practical learning roadmap based on the student's missing skills.

Requirements:

1. Decide which skill should be learned first.
2. Arrange the skills in a logical learning order.
3. Divide the roadmap into phases.
4. Explain what the student should learn in each phase.
5. Suggest practical projects for each phase.
6. Mention when the student should start applying for jobs.
7. Keep the roadmap realistic and beginner-friendly.

Give the roadmap in a clear format with:

- Phase
- Skills to Learn
- What to Study
- Practice Projects
- Expected Outcome

Do not include skills that the student already has at a good level
unless they are needed as prerequisites.

Keep the response practical, structured, and easy to understand.
"""

    return prompt