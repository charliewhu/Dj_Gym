from django import forms
from .models import Exercise


class ExerciseForm(forms.ModelForm):
    class Meta:
        model  = Exercise
        fields = [
            'name',
            'purpose',
            'tier',
            #'muscle_group',
            'mechanic',
            'force',
            ]