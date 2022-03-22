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

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(
        source = 'exercise'
    )

    class Meta:
        model = WorkoutExercise
        fields = [
            'id',
            'workout',
            'exercise',
            'name',
            'is_set_adjust',
        ]


class WorkoutSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = [
            'id',
            'user',
            'readiness',
            'date',
            'split_day',
            'is_active',
            'is_exercise_generate',
            'exercises',
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