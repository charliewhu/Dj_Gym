from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView
from .forms import RoutineItemCreateForm, RoutineItemUpdateForm
from .models import Routine, RoutineItem


class RoutineItemListView(ListView):
    model = RoutineItem


class RoutineItemCreateView(CreateView):
    model = RoutineItem
    form_class = RoutineItemCreateForm

    def get_success_url(self):
        return reverse('routines:routine_list')


class RoutineItemUpdateView(UpdateView):
    model = RoutineItem
    form_class = RoutineItemUpdateForm

    def get_success_url(self):
        return reverse('routines:routine_list')