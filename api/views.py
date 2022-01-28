from django.shortcuts import render
from rest_framework import viewsets
from api.serializers import WorkoutExerciseSerializer, WorkoutExerciseSetSerializer
from routines.models import WorkoutExercise, WorkoutExerciseSet



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