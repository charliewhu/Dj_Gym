from rest_framework import serializers
from exercises.models import Exercise
from routines.models import ReadinessQuestion, Readiness, Workout, WorkoutExercise, WorkoutExerciseSet


class ReadinessQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadinessQuestion
        fields = [
            'id',
            'name',
        ]


class WorkoutSerializer(serializers.ModelSerializer):
    exercises = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = [
            'user',
            'readiness',
            'date',
            'split_day',
            'is_active',
            'is_exercise_generate',
            'exercises',
        ]

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExercise
        fields = [
            'id',
            'workout',
            'exercise',
            'is_set_adjust',
        ]


class WorkoutExerciseSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExerciseSet
        fields = [
            'id',
            'workout_exercise',
            'weight',
            'reps',
            'rir',
        ]


class ExerciseSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Exercise
        fields = [
            'name',
            'user',
            'mechanic',
            'force',
            'purpose',
            'tier',
            'progression_type',
            'min_reps',
            'max_reps',
            'is_active',
            'is_unilateral',
        ]