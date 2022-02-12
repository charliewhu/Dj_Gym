from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from .forms import ReadinessFormSet, WorkoutExerciseSetForm, WorkoutForm, WorkoutExerciseForm
from .models import Exercise, ReadinessAnswer, ReadinessQuestion, Workout, WorkoutExercise, WorkoutExerciseSet, Readiness
from .mixins import UserWorkoutExerciseSetMixin, UserWorkoutMixin, UserWorkoutExerciseMixin



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
        """
        When form is submitted:
        1. create a Readiness object for today
        2. create a Workout for that Readiness object
        3. create ReadinessAnswers for that Readiness object
        (using the initial_data and answers from the form the User submitted)
        """
        readiness = Readiness.objects.create(user=self.request.user)
        
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
        workout = Workout.objects.get(readiness=readiness)
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


def end_workout_view(request, pk):
    """
    POST to this view to end the workout with id=pk
    """
    workout = Workout.objects.get(id=pk)
    user = request.user
    if request.POST and workout.user==user:
        workout.end_workout()
        return HttpResponseRedirect(reverse_lazy('routines:workout_list'))
    return HttpResponseRedirect(reverse_lazy('routines:workout_list'))


class WorkoutExerciseListView(LoginRequiredMixin, UserWorkoutMixin, ListView):
    model         = WorkoutExercise
    template_name = 'routines/workout_exercise/_list.html'
    extra_context = {'title':'Workout Items'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        w = Workout.objects.get(pk=self.kwargs['pk'])
        context['object'] = w
        context['object_list'] = w.exercises.all()
        context['workout_readiness'] = w.readiness.percentage()
        return context


class WorkoutExerciseDetailView(LoginRequiredMixin, UserWorkoutExerciseMixin, DetailView):
    model = WorkoutExercise
    template_name = 'routines/workout_exercise/_detail.html'


# def load_exercises(request):
#     """
#     For AJAX request to allow dependent dropdown
#     MuscleGroup --> Exercise
#     """
#     muscle_group_id = request.GET.get('muscle_group')
#     exercises = Exercise.objects.filter(muscle_group_id=muscle_group_id).order_by('name')
#     return render(request, 'routines/workout_exercise/partials/exercises_dropdown.html', {'exercises': exercises})
    

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
    extra_context = {
        'title':'Workout Exercise Sets'
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        we = WorkoutExercise.objects.get(pk=self.kwargs['pk'])
        context['object'] = we
        context['object_list'] = we.sets.all()
        # one_rm = UserRM.one_rm_manager.latest_one_rm(user=self.request.user, exercise=we.exercise)
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

    mean   = ReadinessAnswer.manager.mean(request.user)
    stddev = ReadinessAnswer.manager.stddev(request.user)

    context = {
        'mean': mean,
        'stddev': stddev,
        }
    return render(request, 'test.html', context)