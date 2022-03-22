from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import viewsets
from api.serializers import ReadinessQuestionSerializer, WorkoutExerciseSerializer, WorkoutExerciseSetSerializer
from routines.models import ReadinessQuestion, WorkoutExercise, WorkoutExerciseSet



@api_view(['GET', 'POST'])
def readiness(request):
    """
    List all ReadinessQuestions
    Or create a new Readiness instance with associated ReadinessQuestions
    """
    if request.method == 'GET':
        readiness_questions = ReadinessQuestion.objects.all()
        serializer = ReadinessQuestionSerializer(readiness_questions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        pass
    

@api_view(['GET', 'POST'])
def workout_exercises(request, pk):
    """
    List all Exercises for a Workout (pk)
    Or create a new WorkoutExercise instance for given Workout (pk)
    """
    pass


@api_view(['PUT', 'PATCH', 'DELETE'])
def workoutexercise_detail(request, pk):
    """
    Update or Delete WorkoutExercise (pk)
    """
    pass


@api_view(['GET', 'POST'])
def workoutexercise_sets(request, pk):
    """
    List all Sets for a WorkoutExercise (pk)
    Or create a new WorkoutExerciseSet instance for a given WorkoutExercise (pk)
    """
    pass


@api_view(['PUT', 'PATCH', 'DELETE'])
def workoutexerciseset_detail(request, pk):
    """
    Update or Delete WorkoutExerciseSet (pk)
    """
    pass


@api_view(['GET', 'POST'])
def exercises(request):
    """
    List all Exercises
    """
    pass


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def exercise_detail(request, pk):
    """
    Get Exercise (pk) 
    Or Update/Delete
    """
    pass







class WorkoutExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutExerciseSerializer
    queryset = WorkoutExercise.objects.all()



class WorkoutExerciseSetViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutExerciseSetSerializer
    queryset = WorkoutExerciseSet.objects.all()

    # def get_queryset(self):
    #     print(self.request.user)
    #     user = self.request.user
    #     ##user doesnt have workout exercise sets!
    #     return WorkoutExerciseSet.objects.filter(user=user)