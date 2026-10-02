from rest_framework import serializers

from .models import AssessmentAttempt, AssessmentQuestion, InterviewSession, InterviewTurn


class AssessmentQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentQuestion
        fields = ['id', 'question', 'options']


class AssessmentAttemptSerializer(serializers.ModelSerializer):
    career_title = serializers.CharField(source='career.title', read_only=True)
    skill_name = serializers.CharField(source='skill.name', read_only=True)

    class Meta:
        model = AssessmentAttempt
        fields = [
            'id', 'career', 'career_title', 'skill', 'skill_name',
            'total_questions', 'correct_answers', 'score_percentage',
            'weak_areas', 'recommended_skills', 'completed_at',
        ]


class InterviewTurnSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewTurn
        fields = [
            'question_number', 'question', 'answer', 'score',
            'strengths', 'weaknesses', 'suggestions', 'better_answer',
        ]


class InterviewSessionSerializer(serializers.ModelSerializer):
    career_title = serializers.CharField(source='career.title', read_only=True)
    turns = InterviewTurnSerializer(many=True, read_only=True)

    class Meta:
        model = InterviewSession
        fields = [
            'id', 'career', 'career_title', 'difficulty', 'status',
            'overall_score', 'technical_score', 'communication_feedback',
            'weak_skills', 'preparation_topics', 'next_steps',
            'started_at', 'completed_at', 'turns',
        ]
