from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import JobDescription
from .serializers import JobDescriptionSerializer

from ai_services.job_analysis import (
    build_job_analysis_prompt,
    build_job_learning_prompt,
)

from ai_services.openai_service import generate_career_analysis

from careers.models import UserSkill


class JobDescriptionCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobDescriptionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JobDescriptionAnalysisView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):

        job = JobDescription.objects.get(
            id=job_id,
            user=request.user
        )

        # -----------------------------
        # STEP 1: Ask Gemini to extract skills
        # -----------------------------

        prompt = build_job_analysis_prompt(
            job.description
        )

        ai_response = generate_career_analysis(
            prompt
        )

        # -----------------------------
        # STEP 2: Convert AI response
        # into structured skill data
        # -----------------------------

        job_skills = []

        for line in ai_response.splitlines():

            line = line.strip()

            if not line or "|" not in line:
                continue

            parts = [
                part.strip()
                for part in line.split("|")
            ]

            if len(parts) != 3:
                continue

            skill_name = parts[0]
            category = parts[1]

            try:
                importance = int(parts[2])
            except ValueError:
                continue

            if importance < 1:
                importance = 1

            if importance > 5:
                importance = 5

            job_skills.append({
                "name": skill_name,
                "category": category,
                "importance": importance,
            })

        # -----------------------------
        # STEP 3: Get user's skills
        # -----------------------------

        user_skills = {
            user_skill.skill.name.lower(): user_skill.proficiency
            for user_skill in UserSkill.objects.filter(
                user=request.user
            ).select_related("skill")
        }

        # -----------------------------
        # STEP 4: Compare skills
        # -----------------------------

        comparison = []

        for item in job_skills:

            current = user_skills.get(
                item["name"].lower(),
                0
            )

            required = item["importance"]

            gap = max(
                required - current,
                0
            )

            if current == 0:
                status = "Missing"
                priority = "High"

            elif gap > 0:
                status = "Needs Improvement"

                if gap >= 3:
                    priority = "High"
                elif gap == 2:
                    priority = "Medium"
                else:
                    priority = "Low"

            else:
                status = "Good"
                priority = "None"

            comparison.append({
                "skill": item["name"],
                "category": item["category"],
                "required": required,
                "current": current,
                "gap": gap,
                "status": status,
                "priority": priority,
            })

        # -----------------------------
        # STEP 5: Ask Gemini for
        # personalized learning plan
        # -----------------------------

        learning_prompt = build_job_learning_prompt(
            comparison
        )

        learning_plan = generate_career_analysis(
            learning_prompt
        )

        # -----------------------------
        # STEP 6: Return final response
        # -----------------------------

        return Response({
            "job_id": job.id,
            "job_title": job.title,
            "company": job.company,
            "required_skills": job_skills,
            "skill_comparison": comparison,
            "learning_plan": learning_plan,
        })