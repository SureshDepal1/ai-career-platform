from django.db import models
from django.contrib.auth.models import User


class JobDescription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    company = models.CharField(
        max_length=200,
        blank=True
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class JobAnalysis(models.Model):
    job = models.OneToOneField(
        JobDescription,
        on_delete=models.CASCADE,
        related_name="analysis"
    )

    required_skills = models.JSONField(
        default=list
    )

    skill_comparison = models.JSONField(
        default=list
    )

    learning_plan = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Analysis - {self.job.title}"