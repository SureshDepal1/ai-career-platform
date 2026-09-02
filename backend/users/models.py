from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    career_goal = models.CharField(max_length=200, blank=True)
    education = models.CharField(max_length=200, blank=True)
    experience = models.TextField(blank=True)
    current_skills = models.TextField(blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username