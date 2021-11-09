from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Exercise, MuscleGroup
from .forms import ExerciseForm


# Create your views here.
class ExerciseListView(LoginRequiredMixin, ListView):
    queryset = MuscleGroup.objects.all().prefetch_related('exercise_set').order_by('name')
    template_name = 'exercises/_list.html'
    extra_context = {'title':'Exercises'}


class ExerciseCreateView(LoginRequiredMixin, CreateView):
    model         = Exercise
    form_class    = ExerciseForm
    template_name = 'exercises/_form.html'
    extra_context = {'title':'Add Items To Workout'}
    success_url   = reverse_lazy('exercises:exercise_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)