from django.contrib import admin
from .models import Career, Skill, CareerSkill, UserSkill, Roadmap, LearningResource


admin.site.register(Career)
admin.site.register(Skill)
admin.site.register(CareerSkill)
admin.site.register(UserSkill)
admin.site.register(Roadmap)
admin.site.register(LearningResource)