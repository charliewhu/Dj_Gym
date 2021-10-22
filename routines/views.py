from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test


from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from .forms import WorkoutForm, WorkoutExerciseForm, ExerciseForm
from .models import MuscleGroup, Exercise, Workout, WorkoutExercise, WorkoutExerciseSet
from .mixins import UserWorkoutMixin, UserWorkoutExerciseMixin


def home(request):
    return render(request, 'home.html')


class ExerciseListView(LoginRequiredMixin, ListView):
    queryset = MuscleGroup.objects.all().prefetch_related('exercise_set').order_by('name')
    template_name = 'routines/exercise_list.html'
    extra_context = {'title':'Exercises'}


class ExerciseCreateView(LoginRequiredMixin, CreateView):
    model         = Exercise
    form_class    = ExerciseForm
    extra_context = {'title':'Add Items To Workout'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mg = MuscleGroup.objects.get(id=self.kwargs['pk'])
        context['object'] = mg
        return context

    def form_valid(self, form):
        form.instance.muscle_group = MuscleGroup.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('routines:exercise_list')


class WorkoutListView(LoginRequiredMixin, ListView):
    model         = Workout
    ordering      = ['-date', '-id']
    extra_context = {'title':'My Workouts'}

    def get_queryset(self):
        """only get user's workouts"""
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


class WorkoutCreateView(LoginRequiredMixin, CreateView):
    model         = Workout
    form_class    = WorkoutForm
    extra_context = {'title':'Create Workout'}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('routines:workout_list')


class WorkoutUpdateView(LoginRequiredMixin, UserWorkoutMixin, UpdateView):
    model           = Workout
    form_class      = WorkoutForm
    extra_context   = {'title':'Update Workout'}

    def get_success_url(self):
        return reverse('routines:workout_list')


class WorkoutDeleteView(LoginRequiredMixin, UserWorkoutMixin, DeleteView):
    model = Workout
    def get_success_url(self):
        return reverse_lazy('routines:workout_list')


class WorkoutExerciseListView(LoginRequiredMixin, UserWorkoutMixin, ListView):
    model         = WorkoutExercise
    extra_context = {'title':'Workout Items'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        w = Workout.objects.get(pk=self.kwargs['pk'])
        context['object'] = w
        context['object_list'] = WorkoutExercise.objects.filter(workout_id=w.id)
        return context


def load_exercises(request):
    """
    For AJAX request to allow dependent dropdown
    MuscleGroup --> Exercise
    """
    muscle_group_id = request.GET.get('muscle_group')
    exercises = Exercise.objects.filter(muscle_group_id=muscle_group_id).order_by('name')
    return render(request, 'routines/partials/exercises_dropdown.html', {'exercises': exercises})


class WorkoutExerciseCreateView(LoginRequiredMixin, UserWorkoutMixin, CreateView):
    model         = WorkoutExercise
    form_class    = WorkoutExerciseForm
    extra_context = {'title':'Add Exercise'}

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
        return reverse_lazy('routines:workout_exercise_list', kwargs={'pk':pk})


class WorkoutExerciseUpdateView(LoginRequiredMixin, UserWorkoutExerciseMixin, UpdateView):
    model      = WorkoutExercise
    form_class = WorkoutExerciseForm
    extra_context = {'title':'Edit Exercise'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wi = WorkoutExercise.objects.get(pk=self.kwargs['pk'])
        context['object'] = wi.workout
        return context

    def get_success_url(self):
        wi = WorkoutExercise.objects.get(pk=self.kwargs['pk'])
        pk = wi.workout_id
        return reverse_lazy('routines:workout_exercise_list', kwargs={'pk':pk})


class WorkoutExerciseDeleteView(LoginRequiredMixin, UserWorkoutExerciseMixin, DeleteView):
    model = WorkoutExercise
    def get_success_url(self):
        wi = WorkoutExercise.objects.get(pk=self.kwargs['pk'])
        pk = wi.workout_id
        return reverse_lazy('routines:workout_exercise_list', kwargs={'pk':pk})
        

class WorkoutExerciseSetListView(ListView):
    model = WorkoutExerciseSet


class WorkoutExerciseSetCreateView(CreateView):
    model = WorkoutExerciseSet


class WorkoutExerciseSetUpdateView(UpdateView):
    model = WorkoutExerciseSet


class WorkoutExerciseSetDeleteView(DeleteView):
    model = WorkoutExerciseSet

