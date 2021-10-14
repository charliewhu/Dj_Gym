from django import forms
from django.forms import widgets
from .models import Workout, WorkoutItem, Exercise


class WorkoutForm(forms.ModelForm):
    class Meta:
        model   = Workout
        fields  = ['name', 'date']
        widgets = {
            'date': widgets.DateInput(attrs={'type': 'date'})
        }


class WorkoutItemForm(forms.ModelForm):
    class Meta:
        model  = WorkoutItem
        fields = ['exercise', 'sets', 'reps', 'weight', 'rir',]


class ExerciseForm(forms.ModelForm):
    class Meta:
        model  = Exercise
        fields = ['name']

