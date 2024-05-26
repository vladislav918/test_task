from django.views.generic import ListView, UpdateView, FormView, DetailView
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import MemoryForm
from .models import Coordinates, Memory


def index(request):
    return render(request, 'places_remember/index.html')


class MemoryListView(LoginRequiredMixin, ListView):
    model = Memory
    template_name = 'places_remember/memory_list.html'

    def get_queryset(self):
        memory = Memory.objects.filter(author=self.request.user).order_by('-id')
        return memory


class MemoryAddView(LoginRequiredMixin, FormView):
    template_name = 'places_remember/map.html'
    form_class = MemoryForm
    success_url = reverse_lazy('memory_list')

    def form_valid(self, form):
        memory = Memory()
        memory.author = self.request.user
        memory.title = form.cleaned_data['title']
        memory.comment = form.cleaned_data['comment']

        coord = Coordinates()
        coord.lat = form.cleaned_data['latitude']
        coord.lng = form.cleaned_data['longitude']
        coord.save()

        memory.coordinates = coord
        memory.save()
        return super().form_valid(form)


class MemoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Memory
    form_class = MemoryForm
    template_name = 'places_remember/memory_update_form.html'
    success_url = reverse_lazy('memory_list')

    def form_valid(self, form):
        memory = self.get_object()

        memory.title = form.cleaned_data['title']
        memory.comment = form.cleaned_data['comment']

        if form.cleaned_data['latitude'] and form.cleaned_data['longitude']:
            coord = memory.coordinates

            coord.lat = form.cleaned_data['latitude']
            coord.lng = form.cleaned_data['longitude']
            coord.save()

        memory.save()

        return redirect(self.success_url)


class MemoryDetailView(LoginRequiredMixin, DetailView):
    model = Memory


def logout(request):
    auth_logout(request)
    return redirect('home')
