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

        read_only_fields = ['workout']

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
            'is_set_adjust',
            'name',
            'sets',
            'set_count',
            'avg_reps',
            'exertion_load',
        ]

        read_only_fields = [
            'name',
            'sets',
            'set_count',
            'avg_reps',
            'exertion_load',
        ]

    name = serializers.StringRelatedField(source='exercise')
    sets = WorkoutExerciseSetSerializer(many=True, read_only=True)

    def get_sets_count(self, instance):
        instance.set_count()

    def get_avg_reps(self, instance):
        instance.avg_reps_count()

    def get_exertion_load(self, instance):
        instance.exertion_load()


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = [
            'id',
            'user',
            'readiness',
            'date',
            'is_active',
            'is_exercise_generate',
            'split_day',
            'exertion_load',
            'exercises',
        ]

        read_only_fields = [
            'exercises',
            'split_day',
            'exertion_load',
        ]

    exercises = WorkoutExerciseSerializer(many=True, read_only=True)
    split_day = serializers.StringRelatedField()

    def get_exertion_load(self, instance):
        return instance.exertion_load()


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = [
            'id',
            'name',
            'user',
            'mechanic',
            'force',
            'purpose',
            'tier',
            'min_reps',
            'max_reps',
            'is_active',
            'is_unilateral',
        ]
    user = serializers.StringRelatedField()


class MechanicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = [
            'id',
            'name',
        ]


class ForceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = [
            'id',
            'name',
        ]


class PurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = [
            'id',
            'name',
        ]


class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = [
            'id',
            'name',
        ]
