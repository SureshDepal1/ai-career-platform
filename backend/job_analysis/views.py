from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import JobDescription
from .serializers import JobDescriptionSerializer

from ai_services.job_analysis import build_job_analysis_prompt
from ai_services.openai_service import generate_career_analysis

from careers.models import Skill, UserSkill


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

        prompt = build_job_analysis_prompt(
            job.description
        )

        ai_response = generate_career_analysis(
            prompt
        )

        return Response({
            "job_id": job.id,
            "job_title": job.title,
            "company": job.company,
            "ai_analysis": ai_response
        })