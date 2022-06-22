from django.db.models import Q

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework import viewsets
from api.serializers import ExerciseSerializer, ForceSerializer, MechanicSerializer, PurposeSerializer, ReadinessAnswerSerializer, ReadinessQuestionSerializer, ReadinessSerializer, TierSerializer, WorkoutExerciseSerializer, WorkoutExerciseSetSerializer, WorkoutSerializer
from exercises.models import Exercise, Force, Mechanic, Purpose, Tier
from routines.models import Readiness, ReadinessQuestion, Workout, WorkoutExercise, WorkoutExerciseSet


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def check_token(request):
    """
    Returns 200 if user IsAuthenticated
    Returns 401 if user is not authenticated
    """
    if request.method == 'GET':
        return Response(status=status.HTTP_200_OK)


class ReadinessViewSet(viewsets.ModelViewSet):
    serializer_class = ReadinessSerializer
    queryset = Readiness.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET', 'POST'])
def readiness_answer(request):
    """
    List all ReadinessQuestions
    Or create new ReadinessAnswer instances for associated Readiness/ReadinessQuestions
    """
    if request.method == 'GET':
        readiness_questions = ReadinessQuestion.objects.all()
        serializer = ReadinessQuestionSerializer(
            readiness_questions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # TODO
        serializer = ReadinessAnswerSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer
    queryset = Workout.objects.all().prefetch_related('exercises').order_by("-date")


class WorkoutExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutExerciseSerializer
    queryset = WorkoutExercise.objects.all()


class WorkoutExerciseSetViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutExerciseSetSerializer
    queryset = WorkoutExerciseSet.objects.all()

    # def get_queryset(self):
    #     #TODO - should be model manager
    #     user = self.request.user
    #     return WorkoutExerciseSet.objects.filter(user=user)


@api_view(['POST'])
def generate_next_set(request, pk):
    if request.method == 'POST':
        set = WorkoutExerciseSet.objects.get(id=pk)
        next_set = set.generate_next_set()
        serializer = WorkoutExerciseSetSerializer(set)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        user = self.request.user
        # TODO - should be model manager
        return Exercise.objects.filter(user=user).order_by('name')


class MechanicViewSet(viewsets.ModelViewSet):
    serializer_class = MechanicSerializer
    queryset = Mechanic.objects.all()


class ForceViewSet(viewsets.ModelViewSet):
    serializer_class = ForceSerializer
    queryset = Force.objects.all()


class PurposeViewSet(viewsets.ModelViewSet):
    serializer_class = PurposeSerializer
    queryset = Purpose.objects.all()


class TierViewSet(viewsets.ModelViewSet):
    serializer_class = TierSerializer
    queryset = Tier.objects.all()
