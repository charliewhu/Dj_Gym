from rest_framework import serializers
from routines.models import WorkoutExerciseSet

class WorkoutExerciseSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExerciseSet
        fields = [
            'workout_exercise',
            'reps',
            'weight',
            'rir',
        ]