from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import (
    JobDescription,
    JobAnalysis,
)

from .serializers import (
    JobDescriptionSerializer,
    JobAnalysisSerializer,
)

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
        serializer.save(
            user=self.request.user
        )


class JobDescriptionListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = JobDescriptionSerializer

    def get_queryset(self):
        return JobDescription.objects.filter(
            user=self.request.user
        ).order_by('-created_at')


class JobDescriptionAnalysisView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = JobAnalysisSerializer

    def get(self, request, job_id):

        job = JobDescription.objects.filter(
            id=job_id,
            user=request.user
        ).first()

        if not job:
            raise NotFound(
                "Job description not found."
            )

        existing_analysis = JobAnalysis.objects.filter(
            job=job
        ).first()

        if existing_analysis:

            serializer = self.get_serializer(
                existing_analysis
            )

            return Response({
                "message": "Saved analysis found.",
                "analysis": serializer.data
            })

        prompt = build_job_analysis_prompt(
            job.description
        )

        ai_response = generate_career_analysis(
            prompt
        )

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

            importance = max(
                1,
                min(importance, 5)
            )

            job_skills.append({
                "name": skill_name,
                "category": category,
                "importance": importance,
            })

        user_skills = {
            user_skill.skill.name.lower(): user_skill.proficiency
            for user_skill in UserSkill.objects.filter(
                user=request.user
            ).select_related("skill")
        }

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

        learning_prompt = build_job_learning_prompt(
            comparison
        )

        learning_plan = generate_career_analysis(
            learning_prompt
        )

        analysis = JobAnalysis.objects.create(
            job=job,
            required_skills=job_skills,
            skill_comparison=comparison,
            learning_plan=learning_plan
        )

        serializer = self.get_serializer(
            analysis
        )

        return Response({
            "message": "AI job analysis created and saved.",
            "analysis": serializer.data
        })


class SavedJobAnalysisView(generics.RetrieveAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = JobAnalysisSerializer

    def get_queryset(self):

        return JobAnalysis.objects.filter(
            job__user=self.request.user
        )