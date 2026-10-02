def build_job_analysis_prompt(job_description):
    prompt = f"""
You are an AI job description analyzer.

Analyze the following job description:

JOB DESCRIPTION:
{job_description}

Extract the technical and professional skills required for this job.

For each skill, provide:
- Skill name
- Category
- Importance from 1 to 5

Importance:
5 = Essential
4 = Very Important
3 = Important
2 = Useful
1 = Nice to have

Return ONLY the skills in this format:

Skill | Category | Importance

Example:
Python | Programming | 5
SQL | Database | 4
Machine Learning | AI/ML | 5
Git | Tools | 3

Do not include explanations.
Do not include markdown.
Only return the skill list.
"""

    return prompt


def build_job_learning_prompt(skill_comparison):
    prompt = """
You are an AI career learning advisor.

A student's skills were compared with the requirements of a job.

SKILL COMPARISON:
"""

    for item in skill_comparison:
        prompt += f"""
Skill: {item['skill']}
Category: {item['category']}
Required Level: {item['required']}
Current Level: {item['current']}
Gap: {item['gap']}
Status: {item['status']}
"""

    prompt += """
Based on this comparison, create a personalized learning plan.

Focus mainly on skills with:
- Missing status
- Needs Improvement status

For each skill provide:

Skill:
Priority:
Why Learn It:
What To Learn:
Practice Project:

Priority must be:
High
Medium
Low

Also provide:
1. Which skill should be learned first.
2. A logical learning order.
3. When the student can start applying for jobs.

Keep the advice practical and beginner-friendly.
Do not recommend skills that already have a Good status unless they are necessary as prerequisites.
"""

    return prompt


def normalize_skill_name(name):
    return ' '.join(name.casefold().strip().split())


def parse_job_skills(text):
    """Parse Gemini's pipe format while tolerating common formatting noise."""
    skills = []
    seen = set()
    for raw_line in (text or '').splitlines():
        line = raw_line.strip().strip('`*_- ')
        if not line or '|' not in line:
            continue
        parts = [part.strip().strip('`*') for part in line.split('|')]
        if len(parts) != 3:
            continue
        name, category, raw_importance = parts
        if not name or not category:
            continue
        try:
            importance = int(raw_importance)
        except (TypeError, ValueError):
            continue
        key = normalize_skill_name(name)
        if not key or key in seen:
            continue
        seen.add(key)
        skills.append({
            'name': name,
            'category': category,
            'importance': max(1, min(importance, 5)),
        })
    return skills