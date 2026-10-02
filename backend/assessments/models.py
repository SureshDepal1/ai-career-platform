from django.contrib.auth.models import User
from django.db import models

from careers.models import Career, Skill


class AssessmentQuestion(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='assessment_questions')
    question = models.TextField()
    options = models.JSONField(default=list)
    correct_option = models.PositiveSmallIntegerField()
    explanation = models.TextField(blank=True)

    def __str__(self):
        return f'{self.skill.name}: {self.question[:60]}'


class AssessmentAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessment_attempts')
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    questions = models.JSONField(default=list)
    answers = models.JSONField(default=list)
    total_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    score_percentage = models.PositiveIntegerField(default=0)
    weak_areas = models.JSONField(default=list)
    recommended_skills = models.JSONField(default=list)
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-completed_at']


class InterviewSession(models.Model):
    DIFFICULTIES = [('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')]
    STATUS_CHOICES = [('active', 'Active'), ('completed', 'Completed')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interview_sessions')
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTIES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    overall_score = models.PositiveIntegerField(default=0)
    technical_score = models.PositiveIntegerField(default=0)
    communication_feedback = models.TextField(blank=True)
    weak_skills = models.JSONField(default=list)
    preparation_topics = models.JSONField(default=list)
    next_steps = models.JSONField(default=list)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']


class InterviewTurn(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='turns')
    question_number = models.PositiveIntegerField()
    question = models.TextField()
    answer = models.TextField(blank=True)
    score = models.PositiveIntegerField(default=0)
    strengths = models.JSONField(default=list)
    weaknesses = models.JSONField(default=list)
    suggestions = models.JSONField(default=list)
    better_answer = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['question_number']
