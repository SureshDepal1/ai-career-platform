from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ai_services.skill_gap import (
    build_skill_gap_prompt,
    build_learning_roadmap_prompt,
)
from ai_services.openai_service import generate_career_analysis

from .models import (
    Career,
    CareerSkill,
    UserSkill,
    Roadmap,
    LearningResource,
)

from .serializers import (
    CareerSerializer,
    SkillGapSerializer,
    RoadmapSerializer,
    LearningResourceSerializer,
)


class CareerListView(generics.ListAPIView):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer


class CareerDetailView(generics.RetrieveAPIView):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer


class SkillGapView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SkillGapSerializer

    def get(self, request, career_id):
        career = Career.objects.get(id=career_id)

        required_skills = CareerSkill.objects.filter(
            career=career
        )

        user_skills = {
            user_skill.skill_id: user_skill.proficiency
            for user_skill in UserSkill.objects.filter(
                user=request.user
            )
        }

        results = []

        for required in required_skills:
            current = user_skills.get(required.skill_id, 0)
            gap = max(required.importance - current, 0)

            if current == 0:
                status = "Missing"
            elif gap > 0:
                status = "Needs Improvement"
            else:
                status = "Good"

            results.append({
                "skill": required.skill,
                "required_importance": required.importance,
                "current_proficiency": current,
                "gap": gap,
                "status": status,
            })

        serializer = self.get_serializer(
            results,
            many=True
        )

        skill_gap_data = serializer.data

        # Build AI skill-gap analysis prompt
        skill_gap_prompt = build_skill_gap_prompt(
            request.user,
            career,
            skill_gap_data
        )

        # Build AI personalized learning roadmap prompt
        roadmap_prompt = build_learning_roadmap_prompt(
            request.user,
            career,
            skill_gap_data
        )

        # Generate AI career analysis
        ai_analysis = generate_career_analysis(
            skill_gap_prompt
        )

        # Generate AI personalized learning roadmap
        learning_roadmap = generate_career_analysis(
            roadmap_prompt
        )

        return Response({
            "career": career.title,
            "skill_gaps": skill_gap_data,
            "ai_analysis": ai_analysis,
            "learning_roadmap": learning_roadmap,
        })


class RoadmapView(generics.RetrieveAPIView):
    serializer_class = RoadmapSerializer

    def get_object(self):
        career_id = self.kwargs['career_id']

        return Roadmap.objects.filter(
            career_id=career_id
        ).first()


class RecommendationView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LearningResourceSerializer

    def get(self, request, career_id):
        career = Career.objects.get(id=career_id)

        required_skills = CareerSkill.objects.filter(
            career=career
        )

        user_skills = {
            user_skill.skill_id: user_skill.proficiency
            for user_skill in UserSkill.objects.filter(
                user=request.user
            )
        }

        skill_ids = []

        for required in required_skills:
            current = user_skills.get(required.skill_id, 0)

            if current < required.importance:
                skill_ids.append(required.skill_id)

        resources = LearningResource.objects.filter(
            roadmap__career=career,
            skill_id__in=skill_ids
        )

        serializer = self.get_serializer(
            resources,
            many=True
        )

        return Response({
            "career": career.title,
            "recommended_resources": serializer.data
        })