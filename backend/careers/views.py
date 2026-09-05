from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Career, CareerSkill, UserSkill
from .serializers import CareerSerializer, SkillGapSerializer


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

        serializer = self.get_serializer(results, many=True)

        return Response({
            "career": career.title,
            "skill_gaps": serializer.data
        })
        