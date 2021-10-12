from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from .forms import WorkoutForm, WorkoutItemForm, WorkoutItemUpdateForm
from .models import Workout, WorkoutItem


def home(request):
    return render(request, 'home.html')


class WorkoutListView(ListView):
    model         = Workout
    template_name = 'routines/_list.html'
    extra_context = {'title':'Workout List'}


class WorkoutCreateView(CreateView):
    form_class = WorkoutForm
    template_name = 'routines/_form.html'
    extra_context = {'title':'Create Workout'}

    def get_success_url(self):
        return reverse('routines:workout_list')


class WorkoutUpdateView(UpdateView):
    model = Workout
    form_class = WorkoutForm
    template_name = 'routines/_form.html'
    extra_context = {'title':'Update Workout'}
    def get_success_url(self):
        return reverse('routines:workout_list')


class WorkoutItemListView(ListView):
    model = WorkoutItem
    template_name = 'routines/_list.html'
    extra_context = {'title':'Workout Items'}


class WorkoutItemCreateView(CreateView):
    model = WorkoutItem
    form_class = WorkoutItemForm
    template_name = 'routines/_form.html'
    extra_context = {'title':'Add Items To Workout'}

    def form_valid(self, form):
        form.instance.workout = Workout.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('routines:workout_list')


class WorkoutItemUpdateView(UpdateView):
    model = WorkoutItem
    form_class = WorkoutItemUpdateForm

    def get_success_url(self):
        return reverse('routines:workout_list')