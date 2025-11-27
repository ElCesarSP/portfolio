from django.contrib import admin
from .models import User, Skill, Project, Experiment

# Register your models here.
admin.site.register(User)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Experiment)
