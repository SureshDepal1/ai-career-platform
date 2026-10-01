from rest_framework import serializers

from .models import (
    JobDescription,
    JobAnalysis,
)


class JobDescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobDescription

        fields = [
            'id',
            'title',
            'company',
            'description',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
        ]


class JobAnalysisSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobAnalysis

        fields = [
            'id',
            'job',
            'required_skills',
            'skill_comparison',
            'learning_plan',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'job',
            'created_at',
            'updated_at',
        ]