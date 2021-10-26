from django.contrib import admin
from django.apps import apps
from . import models


class ExerciseAdmin(admin.TabularInline):
    model = models.Exercise

class MuscleGroupAdmin(admin.ModelAdmin):
   inlines = [ExerciseAdmin,]

admin.site.register(models.MuscleGroup, MuscleGroupAdmin)
admin.site.register(models.Exercise)
admin.site.register(models.Workout)
admin.site.register(models.WorkoutExercise)
admin.site.register(models.WorkoutExerciseSet)
admin.site.register(models.ReadinessQuestion)
admin.site.register(models.WorkoutReadiness)







