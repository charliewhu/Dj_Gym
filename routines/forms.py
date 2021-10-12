from django import forms
from .models import Workout, WorkoutItem


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = '__all__'


class WorkoutItemForm(forms.ModelForm):
    class Meta:
        model = WorkoutItem
        fields = ['exercise', 'sets', 'reps', 'weight', 'rir',]
        #fields = '__all__'
        #fields = ['muscle_group', 'exercise',]


class WorkoutItemUpdateForm(WorkoutItemForm):
    class Meta(WorkoutItemForm.Meta):
        fields = '__all__'
        #fields = ['sets', 'reps', 'weight', 'rir',]
    