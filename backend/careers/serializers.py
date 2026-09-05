from rest_framework import serializers
from .models import Career, Skill, CareerSkill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category']


class CareerSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = CareerSkill
        fields = ['id', 'skill', 'importance']


class CareerSerializer(serializers.ModelSerializer):
    required_skills = serializers.SerializerMethodField()

    class Meta:
        model = Career
        fields = ['id', 'title', 'description', 'required_skills']

    def get_required_skills(self, obj):
        career_skills = CareerSkill.objects.filter(career=obj)

        return CareerSkillSerializer(
            career_skills,
            many=True
        ).data


class SkillGapSerializer(serializers.Serializer):
    skill = SkillSerializer()
    required_importance = serializers.IntegerField()
    current_proficiency = serializers.IntegerField()
    gap = serializers.IntegerField()
    status = serializers.CharField()