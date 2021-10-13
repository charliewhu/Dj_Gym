from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import WorkoutForm, WorkoutItemForm, ExerciseForm
from .models import MuscleGroup, Exercise, Workout, WorkoutItem


def home(request):
    return render(request, 'home.html')


class WorkoutListView(ListView):
    model         = Workout
    ordering      = ['-date']
    extra_context = {'title':'My Workouts'}


class WorkoutCreateView(CreateView):
    model         = Workout
    form_class    = WorkoutForm
    extra_context = {'title':'Create Workout'}

    def get_success_url(self):
        return reverse('routines:workout_list')


class WorkoutUpdateView(UpdateView):
    model           = Workout
    form_class      = WorkoutForm
    extra_context   = {'title':'Update Workout'}

    def get_success_url(self):
        return reverse('routines:workout_list')


class WorkoutItemListView(ListView):
    model         = WorkoutItem
    extra_context = {'title':'Workout Items'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        w = Workout.objects.get(pk=self.kwargs['pk'])
        context['object'] = w
        context['object_list'] = WorkoutItem.objects.filter(workout_id=w.id)
        return context


class WorkoutItemCreateView(CreateView):
    model         = WorkoutItem
    form_class    = WorkoutItemForm
    extra_context = {'title':'Add Items To Workout'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        w = Workout.objects.get(pk=self.kwargs['pk'])
        context['object'] = w
        return context

    def form_valid(self, form):
        form.instance.workout = Workout.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('routines:workout_item_list', kwargs={'pk':pk})


class WorkoutItemUpdateView(UpdateView):
    model      = WorkoutItem
    form_class = WorkoutItemForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('routines:workout_item_list', kwargs={'pk':pk})

    
class ExerciseListView(ListView):
    queryset = MuscleGroup.objects.all().prefetch_related('exercise_set').order_by('name')


class ExerciseCreateView(CreateView):
    model         = Exercise
    form_class    = ExerciseForm
    extra_context = {'title':'Add Items To Workout'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        e = MuscleGroup.objects.get(id=self.kwargs['pk'])
        context['object'] = e
        return context

    def form_valid(self, form):
        form.instance.muscle_group = MuscleGroup.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('routines:exercise_list')