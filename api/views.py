from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import viewsets
from api.serializers import ExerciseSerializer, ReadinessQuestionSerializer, WorkoutExerciseSerializer, WorkoutExerciseSetSerializer, WorkoutSerializer
from exercises.models import Exercise
from routines.models import ReadinessQuestion, Workout, WorkoutExercise, WorkoutExerciseSet



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
def workouts(request):
    """
    List all ReadinessQuestions
    Or create a new Readiness instance with associated ReadinessQuestions
    """
    if request.method == 'GET':
        workouts = Workout.objects.all()
        serializer = WorkoutSerializer(workouts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        pass


@api_view(['GET', 'POST'])
def workout_exercises(request, pk):
    """
    List all Exercises for a Workout (pk)
    Or create a new WorkoutExercise instance for given Workout (pk)
    """
    if request.method == 'GET':
        workout_exercises = WorkoutExercise.objects.filter(workout_id=pk)
        serializer = WorkoutExerciseSerializer(workout_exercises, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WorkoutExerciseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', 'DELETE'])
def workoutexercise_detail(request, pk):
    """
    Update or Delete WorkoutExercise (pk)
    """
    try:
        workout_exercise = WorkoutExercise.objects.get(id=pk)
    except WorkoutExercise.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = WorkoutExerciseSerializer(workout_exercise, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        workout_exercise.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def workoutexercise_sets(request, pk):
    """
    List all Sets for a WorkoutExercise (pk)
    Or create a new WorkoutExerciseSet instance for a given WorkoutExercise (pk)
    """
    if request.method == 'GET':
        workout_exercise_sets = WorkoutExerciseSet.objects.filter(workoutexercise_id=pk)
        serializer = WorkoutExerciseSetSerializer(workout_exercise_sets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WorkoutExerciseSetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT', 'PATCH', 'DELETE'])
def workoutexerciseset_detail(request, pk):
    """
    Update or Delete WorkoutExerciseSet (pk)
    """
    try:
        workout_exercise_set = WorkoutExerciseSet.objects.get(id=pk)
    except WorkoutExerciseSet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = WorkoutExerciseSetSerializer(workout_exercise_set, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        workout_exercise_set.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def exercises(request):
    """
    List all Exercises
    Or Create new Exercise
    """
    if request.method == 'GET':
        exercise = Exercise.objects.all()
        serializer = ExerciseSerializer(exercise, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WorkoutExerciseSetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def exercise_detail(request, pk):
    """
    Get Exercise (pk) 
    Or Update/Delete
    """
    pass


@api_view(['GET', 'PUT', 'PATCH'])
def user_detail(request, pk):
    """
    Get User details (pk)
    Or Update
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