from rest_framework import serializers
from .models import (
    Career,
    Skill,
    CareerSkill,
    Roadmap,
    LearningResource,
    UserSkill,
)


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category']


class UserSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_id = serializers.PrimaryKeyRelatedField(
        source='skill',
        queryset=Skill.objects.all(),
        write_only=True,
    )

    class Meta:
        model = UserSkill
        fields = ['id', 'skill', 'skill_id', 'proficiency']
        read_only_fields = ['id', 'skill']

    def validate_proficiency(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError(
                'Proficiency must be between 1 and 5.'
            )
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        skill = attrs.get('skill', getattr(self.instance, 'skill', None))
        if skill and UserSkill.objects.filter(
            user=user,
            skill=skill,
        ).exclude(pk=getattr(self.instance, 'pk', None)).exists():
            raise serializers.ValidationError(
                {'skill_id': 'You already have this skill.'}
            )
        return attrs


class CareerSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = CareerSkill
        fields = ['id', 'skill', 'importance']


class CareerSerializer(serializers.ModelSerializer):
    required_skills = serializers.SerializerMethodField()

    class Meta:
        model = Career
        fields = ['id', 'title', 'category', 'description', 'required_skills']

    def get_required_skills(self, obj):
        career_skills = obj.careerskill_set.all()

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


class LearningResourceSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = LearningResource
        fields = [
            'id',
            'skill',
            'title',
            'description',
            'resource_type',
            'url',
            'learning_objectives',
            'practice_project',
            'expected_outcome',
            'phase',
        ]


class RoadmapSerializer(serializers.ModelSerializer):
    resources = LearningResourceSerializer(many=True, read_only=True)

    class Meta:
        model = Roadmap
        fields = [
            'id',
            'career',
            'title',
            'description',
            'resources',
        ]