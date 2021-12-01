from django.contrib import admin
from django.apps import apps
from . import models


admin.site.register(models.Workout)
admin.site.register(models.WorkoutExercise)
admin.site.register(models.WorkoutExerciseSet)
admin.site.register(models.ReadinessQuestion)
admin.site.register(models.Readiness)
admin.site.register(models.ReadinessAnswer)







