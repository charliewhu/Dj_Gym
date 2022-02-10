from django import forms
from django.forms import widgets
from .models import Exercise, Workout, WorkoutExercise, WorkoutExerciseSet, Readiness, ReadinessQuestion, ReadinessAnswer


class ReadinessAnswerForm(forms.ModelForm):
    class Meta:
        model  = ReadinessAnswer
        fields = ['readiness_question','rating']

ReadinessFormSet = forms.formset_factory(ReadinessAnswerForm, extra=0)


class WorkoutForm(forms.ModelForm):
    class Meta:
        model   = Workout
        fields  = []
        widgets = {
            'date': widgets.DateInput(attrs={'type': 'date'})
        }


class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model  = WorkoutExercise
        fields = ['exercise', 'is_set_adjust', ]


class WorkoutExerciseSetForm(forms.ModelForm):
    class Meta:
        model  = WorkoutExerciseSet
        fields = ['weight', 'reps', 'rir']

    weight = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    reps   = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    rir    = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))


class ExerciseForm(forms.ModelForm):
    class Meta:
        model  = Exercise
        fields = ['name']

