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
        fields = ['muscle_group', 'exercise', 'sets', 'reps', 'weight', 'rir',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['exercise'].queryset = Exercise.objects.none()

        if 'muscle_group' in self.data:
            try:
                muscle_group_id = int(self.data.get('muscle_group'))
                self.fields['exercise'].queryset = Exercise.objects.filter(muscle_group_id=muscle_group_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Exercise queryset
        elif self.instance.pk:
            self.fields['exercise'].queryset = Exercise.objects.filter(muscle_group=self.instance.muscle_group).order_by('name')


class ExerciseForm(forms.ModelForm):
    class Meta:
        model  = Exercise
        fields = ['name']

