from django.db.models.aggregates import Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms import fields
from django.forms.models import modelformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum

from accounts.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView, FormView
from .forms import ReadinessFormSet, WorkoutExerciseSetForm, WorkoutForm, WorkoutExerciseForm, ExerciseForm, ReadinessAnswerForm
from .models import MuscleGroup, Exercise, ReadinessAnswer, ReadinessQuestion, Workout, WorkoutExercise, WorkoutExerciseSet, Readiness
from .mixins import UserWorkoutExerciseSetMixin, UserWorkoutMixin, UserWorkoutExerciseMixin
from django.forms.formsets import INITIAL_FORM_COUNT, formset_factory


def home(request):
    context = {}
    return render(request, 'home.html', context)

class ReadinessCreateView(CreateView):
    model         = ReadinessAnswer
    fields        = ['readiness_question','rating']
    template_name = 'routines/workout_readiness/_form.html'
    try:
        initial_data = [{'readiness_question':q} for q in ReadinessQuestion.objects.all()]
    except: 
        initial_data = []

    def post(self, request, *args, **kwargs):
        formset = ReadinessFormSet(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, formset):
        readiness = Readiness.objects.create(user=self.request.user)
        workout = Workout.objects.create(user=self.request.user, readiness=readiness)
        for idx, form in enumerate(formset):
            cd = form.cleaned_data
            readiness_question = self.initial_data[idx]['readiness_question']
            rating = cd.get('rating')
            readiness_answer = ReadinessAnswer(
                readiness=readiness,
                readiness_question=readiness_question,
                rating=rating
            )
            readiness_answer.save()
        return HttpResponseRedirect(
            reverse_lazy(
                'routines:workout_exercise_list', 
                kwargs={'pk':workout.id})
            )

    def get_context_data(self, **kwargs):
        """Render initial form"""
        context = super().get_context_data(**kwargs)
        context['formset'] = ReadinessFormSet(initial=self.initial_data)
        return context


class WorkoutListView(LoginRequiredMixin, ListView):
    model         = Workout
    ordering      = ['-date', '-id']
    template_name = 'routines/workout/_list.html'
    extra_context = {'title':'My Workouts'}

    def get_queryset(self):
        """only get user's workouts"""
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        """Need to check if user has an active workout"""
        context = super().get_context_data(**kwargs)
        context['active_wo'] = self.request.user.has_active_workout()
        return context


class WorkoutCreateView(LoginRequiredMixin, CreateView):
    model         = Workout
    form_class    = WorkoutForm
    template_name = 'routines/workout/_form.html'
    extra_context = {'title':'Create Workout'}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('routines:workout_list')


class WorkoutUpdateView(LoginRequiredMixin, UserWorkoutMixin, UpdateView):
    model           = Workout
    form_class      = WorkoutForm
    template_name   = 'routines/workout/_form.html'
    extra_context   = {'title':'Update Workout'}
    success_url     = reverse_lazy('routines:workout_list')


class WorkoutDeleteView(LoginRequiredMixin, UserWorkoutMixin, DeleteView):
    model       = Workout
    success_url = reverse_lazy('routines:workout_list')


class WorkoutExerciseListView(LoginRequiredMixin, UserWorkoutMixin, ListView):
    model         = WorkoutExercise
    template_name = 'routines/workout_exercise/_list.html'
    extra_context = {'title':'Workout Items'}

    def post(self, request, *args, **kwargs):
        w = Workout.objects.get(pk=self.kwargs['pk'])
        w.end_workout()
        return HttpResponseRedirect(
            reverse_lazy(
                'routines:workout_exercise_list', 
                kwargs={'pk':w.id})
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        w = Workout.objects.get(pk=self.kwargs['pk'])
        context['object'] = w
        context['object_list'] = WorkoutExercise.objects.filter(workout_id=w.id)
        context['workout_readiness'] = w.readiness.percentage()
        return context


class WorkoutExerciseDetailView(LoginRequiredMixin, UserWorkoutExerciseMixin, DetailView):
    model = WorkoutExercise
    template_name = 'routines/workout_exercise/_detail.html'


def load_exercises(request):
    """
    For AJAX request to allow dependent dropdown
    MuscleGroup --> Exercise
    """
    muscle_group_id = request.GET.get('muscle_group')
    exercises = Exercise.objects.filter(muscle_group_id=muscle_group_id).order_by('name')
    return render(request, 'routines/workout_exercise/partials/exercises_dropdown.html', {'exercises': exercises})
    

class WorkoutExerciseCreateView(LoginRequiredMixin, UserWorkoutMixin, CreateView):
    model         = WorkoutExercise
    form_class    = WorkoutExerciseForm
    template_name = 'routines/workout_exercise/_form.html'
    extra_context = {'title':'Add Exercise'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Workout.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.workout = Workout.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('routines:workout_exercise_detail', args=(self.object.id,))


class WorkoutExerciseUpdateView(LoginRequiredMixin, UserWorkoutExerciseMixin, UpdateView):
    model         = WorkoutExercise
    form_class    = WorkoutExerciseForm
    template_name = 'routines/workout_exercise/_form.html'
    extra_context = {'title':'Edit Exercise'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        we = WorkoutExercise.objects.get(pk=self.kwargs['pk'])
        context['object'] = we.workout
        context['workout_exercise'] = we
        return context

    def get_success_url(self):
        return reverse('routines:workout_exercise_detail', args=(self.object.id,))


class WorkoutExerciseDeleteView(LoginRequiredMixin, UserWorkoutExerciseMixin, DeleteView):
    model = WorkoutExercise
    def get_success_url(self):
        wi = WorkoutExercise.objects.get(pk=self.kwargs['pk'])
        pk = wi.workout_id
        return reverse_lazy('routines:workout_exercise_list', kwargs={'pk':pk})
        

class WorkoutExerciseSetListView(LoginRequiredMixin, UserWorkoutExerciseMixin, ListView):
    model         = WorkoutExerciseSet
    template_name = 'routines/workout_exercise_set/_list.html'
    extra_context = {'title':'Workout Exercise Sets'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        we = WorkoutExercise.objects.get(pk=self.kwargs['pk'])
        context['object'] = we
        context['object_list'] = WorkoutExerciseSet.objects.filter(workout_exercise_id=we.id)
        return context


class WorkoutExerciseSetDetailView(LoginRequiredMixin, UserWorkoutExerciseSetMixin, DetailView):
    model = WorkoutExerciseSet
    template_name = 'routines/workout_exercise_set/_detail.html'


class WorkoutExerciseSetCreateView(LoginRequiredMixin, UserWorkoutExerciseMixin, CreateView):
    model         = WorkoutExerciseSet
    form_class    = WorkoutExerciseSetForm
    template_name = 'routines/workout_exercise_set/_form.html'
    extra_context = {'title':'Add Set'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        we = WorkoutExercise.objects.get(pk=self.kwargs['pk'])
        context['object'] = we
        return context

    def form_valid(self, form):
        form.instance.workout_exercise = WorkoutExercise.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('routines:wo_ex_set_detail', args=(self.object.id,))


class WorkoutExerciseSetUpdateView(LoginRequiredMixin, UserWorkoutExerciseSetMixin, UpdateView):
    model         = WorkoutExerciseSet
    form_class    = WorkoutExerciseSetForm
    template_name = 'routines/workout_exercise_set/_form.html'
    extra_context = {'title':'Update Set'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wes = WorkoutExerciseSet.objects.get(pk=self.kwargs['pk'])
        context['object'] = wes.workout_exercise
        context['workout_exercise_set'] = wes
        return context

    def get_success_url(self):
        return reverse('routines:wo_ex_set_detail', args=(self.object.id,))


class WorkoutExerciseSetDeleteView(LoginRequiredMixin, UserWorkoutExerciseSetMixin, DeleteView):
    model = WorkoutExerciseSet
    def get_success_url(self):
        wes = WorkoutExerciseSet.objects.get(pk=self.kwargs['pk'])
        pk = wes.workout_exercise_id
        return reverse_lazy('routines:wo_ex_set_list', kwargs={'pk':pk})


def test_view(request):
    if request.method == "POST":
        print("this is a post request")
        return JsonResponse({'Json':'Response'})
    context = {}
    return render(request, 'test.html', context)