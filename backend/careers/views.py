from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ai_services.skill_gap import build_skill_gap_prompt
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
    UserSkillSerializer,
)


class CareerListView(generics.ListAPIView):
    queryset = Career.objects.all().prefetch_related(
        'careerskill_set__skill'
    )
    serializer_class = CareerSerializer


class CareerDetailView(generics.RetrieveAPIView):
    queryset = Career.objects.all().prefetch_related(
        'careerskill_set__skill'
    )
    serializer_class = CareerSerializer


class SkillGapView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SkillGapSerializer

    def get(self, request, career_id):
        career = get_object_or_404(Career, id=career_id)

        required_skills = CareerSkill.objects.filter(
            career=career
        ).select_related('skill')

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

        return Response({
            "career": career.title,
            "skill_gaps": skill_gap_data,
        })


class CareerAIAnalysisView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, career_id):
        career = get_object_or_404(Career, id=career_id)
        required_skills = CareerSkill.objects.filter(
            career=career
        ).select_related('skill')
        user_skills = {
            item.skill_id: item.proficiency
            for item in UserSkill.objects.filter(user=request.user)
        }
        skill_gaps = []
        for required in required_skills:
            current = user_skills.get(required.skill_id, 0)
            gap = max(required.importance - current, 0)
            skill_gaps.append({
                'skill': {
                    'name': required.skill.name,
                    'category': required.skill.category,
                },
                'required_importance': required.importance,
                'current_proficiency': current,
                'gap': gap,
                'status': (
                    'Missing' if current == 0 else
                    'Needs Improvement' if gap else 'Good'
                ),
            })
        try:
            analysis = generate_career_analysis(
                build_skill_gap_prompt(request.user, career, skill_gaps)
            )
        except Exception:
            return Response(
                {'detail': 'AI career advice is temporarily unavailable.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        if not analysis:
            return Response(
                {'detail': 'AI career advice returned no usable content.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        return Response({'career': career.title, 'ai_analysis': analysis})


class UserSkillListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSkillSerializer

    def get_queryset(self):
        return UserSkill.objects.filter(
            user=self.request.user
        ).select_related('skill')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserSkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSkillSerializer

    def get_queryset(self):
        return UserSkill.objects.filter(
            user=self.request.user
        ).select_related('skill')


class RoadmapView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoadmapSerializer

    def get_object(self):
        return get_object_or_404(
            Roadmap.objects.prefetch_related('resources__skill'),
            career_id=self.kwargs["career_id"],
        )

    def retrieve(self, request, *args, **kwargs):
        roadmap = self.get_object()
        user_skills = {
            item.skill_id: item.proficiency
            for item in UserSkill.objects.filter(user=request.user)
        }
        resources = []
        for resource in roadmap.resources.all().order_by('phase', 'id'):
            required = CareerSkill.objects.filter(
                career=roadmap.career,
                skill=resource.skill,
            ).values_list('importance', flat=True).first() or 1
            current = user_skills.get(resource.skill_id, 0)
            status = (
                'Completed' if current >= required else
                'In Progress' if current > 0 else
                'Not Started'
            )
            item = LearningResourceSerializer(resource).data
            item.update({
                'priority': required,
                'status': status,
                'current_proficiency': current,
                'required_proficiency': required,
            })
            resources.append(item)
        data = RoadmapSerializer(roadmap).data
        data['resources'] = resources
        return Response(data)


class RecommendationView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LearningResourceSerializer

    def get(self, request, career_id):
        career = get_object_or_404(Career, id=career_id)

        required_skills = CareerSkill.objects.filter(
            career=career
        ).select_related('skill')

        user_skills = {
            user_skill.skill_id: user_skill.proficiency
            for user_skill in UserSkill.objects.filter(
                user=request.user
            )
        }

        skill_ids = []

        for required in required_skills:
            current = user_skills.get(
                required.skill_id,
                0
            )

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


class ReadinessScoreView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, career_id):
        career = get_object_or_404(Career, id=career_id)

        required_skills = CareerSkill.objects.filter(
            career=career
        ).select_related('skill')

        user_skills = {
            user_skill.skill_id: user_skill.proficiency
            for user_skill in UserSkill.objects.filter(
                user=request.user
            )
        }

        total_required = 0
        total_current = 0

        skill_scores = []

        for required in required_skills:
            current = user_skills.get(
                required.skill_id,
                0
            )

            total_required += required.importance

            total_current += min(
                current,
                required.importance
            )

            percentage = round(
                (
                    min(
                        current,
                        required.importance
                    )
                    / required.importance
                ) * 100
            )

            skill_scores.append({
                "skill": required.skill.name,
                "required": required.importance,
                "current": current,
                "percentage": percentage,
            })

        if total_required > 0:
            readiness_score = round(
                (total_current / total_required) * 100
            )
        else:
            readiness_score = 0

        return Response({
            "career": career.title,
            "readiness_score": readiness_score,
            "skill_scores": skill_scores,
        })