from django.db import models


class Career(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class CareerSkill(models.Model):
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    importance = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.career.title} - {self.skill.name}"


class UserSkill(models.Model):
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE
    )
    proficiency = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.skill.name}"