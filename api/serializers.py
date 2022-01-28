from rest_framework import serializers
from routines.models import WorkoutExercise, WorkoutExerciseSet


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExercise
        fields = [
            'workout',
            'muscle_group',
            'exercise',
            'is_set_adjust',
        ]

class WorkoutExerciseSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExerciseSet
        fields = [
            'workout_exercise',
            'reps',
            'weight',
            'rir',
        ]