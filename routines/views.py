from django.http import HttpResponse, HttpResponseRedirect
from django.forms import fields
from django.forms.models import modelformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test


from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView, FormView
from .forms import WRFormSet, WorkoutExerciseSetForm, WorkoutForm, WorkoutExerciseForm, ExerciseForm, WorkoutReadinessForm
from .models import MuscleGroup, Exercise, ReadinessQuestion, Workout, WorkoutExercise, WorkoutExerciseSet, WorkoutReadiness
from .mixins import UserWorkoutMixin, UserWorkoutExerciseMixin
from django.forms.formsets import INITIAL_FORM_COUNT, formset_factory


def home(request):
    return render(request, 'home.html')


class ExerciseListView(LoginRequiredMixin, ListView):
    queryset = MuscleGroup.objects.all().prefetch_related('exercise_set').order_by('name')
    template_name = 'routines/exercise/_list.html'
    extra_context = {'title':'Exercises'}


class ExerciseCreateView(LoginRequiredMixin, CreateView):
    model         = Exercise
    form_class    = ExerciseForm
    template_name = 'routines/exercise/_form.html'
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
    template_name = 'routines/workout/_list.html'
    extra_context = {'title':'My Workouts'}

    def get_queryset(self):
        """only get user's workouts"""
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


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

    def get_success_url(self):
        return reverse('routines:workout_list')


class WorkoutDeleteView(LoginRequiredMixin, UserWorkoutMixin, DeleteView):
    model = Workout
    def get_success_url(self):
        return reverse_lazy('routines:workout_list')


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
        return context


class WorkoutExerciseDetailView(DetailView):
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
    

def load_exercises2(request):
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
        w = Workout.objects.get(pk=self.kwargs['pk'])
        context['object'] = w
        return context

    def form_valid(self, form):
        form.instance.workout = Workout.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('routines:workout_exercise_detail', args=(self.object.id,))


class WorkoutExerciseUpdateView(LoginRequiredMixin, UpdateView):
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
        

class WorkoutExerciseSetListView(ListView):
    model         = WorkoutExerciseSet
    template_name = 'routines/workout_exercise_set/_list.html'
    extra_context = {'title':'Workout Exercise Sets'}
    #extra_context = {'title':'Workout Items'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        we = WorkoutExercise.objects.get(pk=self.kwargs['pk'])
        context['object'] = we
        context['object_list'] = WorkoutExerciseSet.objects.filter(workout_exercise_id=we.id)
        return context


class WorkoutExerciseSetDetailView(DetailView):
    model = WorkoutExerciseSet
    template_name = 'routines/workout_exercise_set/_detail.html'


class WorkoutExerciseSetCreateView(CreateView):
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
        pk = self.kwargs['pk']
        return reverse('routines:wo_ex_set_detail', args=(self.object.id,))


class WorkoutExerciseSetUpdateView(UpdateView):
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


class WorkoutExerciseSetDeleteView(DeleteView):
    model = WorkoutExerciseSet
    def get_success_url(self):
        wes = WorkoutExerciseSet.objects.get(pk=self.kwargs['pk'])
        pk = wes.workout_exercise_id
        return reverse_lazy('routines:wo_ex_set_list', kwargs={'pk':pk})


class WorkoutReadinessCreateView(CreateView):
    model         = WorkoutReadiness
    fields        = ['readiness_question','rating']
    template_name = 'routines/workout_readiness/_form.html'
    initial_data = [{'readiness_question':q} for q in ReadinessQuestion.objects.all()]

    def post(self, request, *args, **kwargs):
        formset = WRFormSet(request.POST)
        if formset.is_valid():            
            return self.form_valid(formset)
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, formset):
        workout = Workout.objects.create(user=self.request.user)
        for idx, form in enumerate(formset):
            cd = form.cleaned_data
            readiness_question = self.initial_data[idx]['readiness_question']
            rating = cd.get('rating')
            w_readiness = WorkoutReadiness(
                workout=workout,
                readiness_question=readiness_question,
                rating=rating
            )
            w_readiness.save()
        return HttpResponseRedirect(
            reverse_lazy(
                'routines:workout_exercise_list', 
                kwargs={'pk':workout.id})
            )

    def get_context_data(self, **kwargs):
        """Render initial form"""
        context = super().get_context_data(**kwargs)
        context['formset'] = WRFormSet(
            initial =self.initial_data
        )
        return context

