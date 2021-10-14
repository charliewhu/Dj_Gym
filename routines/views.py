from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin


from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import WorkoutForm, WorkoutItemForm, ExerciseForm
from .models import MuscleGroup, Exercise, Workout, WorkoutItem


def home(request):
    return render(request, 'home.html')


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


class WorkoutUpdateView(LoginRequiredMixin, UpdateView):
    model           = Workout
    form_class      = WorkoutForm
    extra_context   = {'title':'Update Workout'}

    def get_success_url(self):
        return reverse('routines:workout_list')


def workout_delete(request, pk):
    workout = Workout.objects.get(id=pk)
    workout.delete()
    return redirect('routines:workout_list')


class WorkoutItemListView(LoginRequiredMixin, ListView):
    model         = WorkoutItem
    extra_context = {'title':'Workout Items'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        w = Workout.objects.get(pk=self.kwargs['pk'])
        context['object'] = w
        context['object_list'] = WorkoutItem.objects.filter(workout_id=w.id)
        return context


def mg_list(request, pk):
    object_list = MuscleGroup.objects.all()
    context = {
        'object_list':object_list,
        'pk':pk,
    }
    return render(request, 'routines/workoutitemcreate_form.html', context)


def load_exercises(request):
    muscle_group_id = request.GET.get('muscle_group')
    exercises = Exercise.objects.filter(muscle_group_id=muscle_group_id).order_by('name')
    print(muscle_group_id)
    return render(request, 'routines/partials/exercises_dropdown.html', {'exercises': exercises})


class WorkoutItemCreateView(LoginRequiredMixin, CreateView):
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


# class WorkoutItemCreateView(LoginRequiredMixin, CreateView):
#     model         = WorkoutItem
#     form_class    = WorkoutItemForm
#     template_name = 'routines/partials/workoutitem_form.html'
#     extra_context = {'title':'Add Items To Workout'}

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         w = Workout.objects.get(pk=self.kwargs['pk'])
#         context['object'] = w
#         return context

#     def get_form_kwargs(self, *args, **kwargs):
#         kwargs = super(WorkoutItemCreateView, self).get_form_kwargs()
#         mg = self.request.GET.get('mg','')
#         kwargs.update({'muscle_group':mg})
#         return kwargs

#     def form_valid(self, form):
#         form.instance.workout = Workout.objects.get(pk=self.kwargs['pk'])
#         return super().form_valid(form)

#     def get_success_url(self):
#         pk = self.kwargs['pk']
#         return reverse_lazy('routines:workout_item_list', kwargs={'pk':pk})


class WorkoutItemUpdateView(LoginRequiredMixin, UpdateView):
    model      = WorkoutItem
    form_class = WorkoutItemForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('routines:workout_item_list', kwargs={'pk':pk})


def workout_item_delete(request, pk):
    workout = Workout.objects.get(id=pk)
    workout.delete()
    return redirect('routines:workout_list')

    
class ExerciseListView(LoginRequiredMixin, ListView):
    queryset = MuscleGroup.objects.all().prefetch_related('exercise_set').order_by('name')
    template_name = 'routines/exercise_list.html'


class ExerciseCreateView(LoginRequiredMixin, CreateView):
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