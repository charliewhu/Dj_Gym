from django import forms
from .models import RoutineItem


class RoutineItemCreateForm(forms.ModelForm):
    class Meta:
        model = RoutineItem
        #fields = '__all__'
        fields = ['routine_day', 'muscle_group', 'exercise',]


class RoutineItemUpdateForm(RoutineItemCreateForm):

    class Meta(RoutineItemCreateForm.Meta):
        # show all the fields!
        fields = '__all__'
        #fields = ['sets', 'reps', 'weight', 'rir',]
    