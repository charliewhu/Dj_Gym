from dataclasses import fields
from rest_framework import serializers
from accounts.models import User
from exercises.models import Exercise
from routines.models import ReadinessAnswer, ReadinessQuestion, Readiness, Workout, WorkoutExercise, WorkoutExerciseSet


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', ]


class ReadinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Readiness
        fields = [
            'id',
            'user',
            'date_created',
            'workout'
        ]

        def get_workout(self, instance):
            instance.get_workout() 


class ReadinessQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadinessQuestion
        fields = [
            'id',
            'name',
        ]


class ReadinessAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadinessAnswer
        fields = [
            'readiness',
            'readiness_question',
            'rating'
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
    class Meta:
        model = WorkoutExercise
        fields = [
            'id',
            'workout',
            'exercise',
            'name',
            'is_set_adjust',
        ]
    name = serializers.StringRelatedField(source = 'exercise')


class WorkoutSerializer(serializers.ModelSerializer):
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
            'exertion_load',
            'exercises',
        ]
    exercises = WorkoutExerciseSerializer(many=True, read_only=True)
    split_day = serializers.StringRelatedField()
    split_day = serializers.StringRelatedField()

    def get_exertion_load(self, instance):
        return instance.exertion_load()


class ExerciseSerializer(serializers.ModelSerializer):
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
    user = serializers.StringRelatedField()