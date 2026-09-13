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