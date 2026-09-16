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