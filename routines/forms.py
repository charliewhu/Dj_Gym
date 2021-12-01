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
        fields = ['muscle_group', 'exercise', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['muscle_group'].queryset = self.fields['muscle_group'].queryset.order_by('name')
        self.fields['exercise'].queryset = Exercise.objects.none()

        if 'muscle_group' in self.data:
            try:
                muscle_group_id = int(self.data.get('muscle_group'))
                self.fields['exercise'].queryset = Exercise.objects.filter(muscle_group_id=muscle_group_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Exercise queryset
        elif self.instance.pk:
            self.fields['exercise'].queryset = Exercise.objects.filter(muscle_group=self.instance.muscle_group).order_by('name')


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

