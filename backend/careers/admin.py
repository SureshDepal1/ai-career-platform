from django.contrib import admin
from .models import Career, Skill, CareerSkill


admin.site.register(Career)
admin.site.register(Skill)
admin.site.register(CareerSkill)