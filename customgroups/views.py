from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib import messages 
from .forms import GroupsForm  

class GroupsListView(PermissionRequiredMixin, ListView):
    permission_required = 'auth.view_group'
    model = Group
    context_object_name = 'groups'
    template_name = 'customgroups/groups_list.html'


class GroupsDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'auth.view_group' 
    model = Group
    context_object_name = 'group' 
    template_name = 'customgroups/groups_detail.html'


class GroupsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'auth.add_group'
    model = Group
    form_class = GroupsForm  
    template_name = 'customgroups/groups_create.html'
    success_url = reverse_lazy('customgroups:list')

    def form_valid(self, form):
        group_name = form.cleaned_data['name']
        
        if Group.objects.filter(name=group_name).exists():
            messages.error(self.request, f'A group with the name "{group_name}" already exists.')  
            return self.form_invalid(form) 

        return super().form_valid(form)


class GroupsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'auth.change_group'
    model = Group
    form_class = GroupsForm
    template_name = 'customgroups/groups_create.html' 
    success_url = reverse_lazy('customgroups:list')

    def form_valid(self, form):
        if Group.objects.exclude(pk=self.object.pk).filter(name=group_name).exists():
            messages.error(self.request, f'A group with the name "{group_name}" already exists.')  
            return self.form_invalid(form) 

        try:
            form.instance.clean()
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

        return super().form_valid(form)


class GroupsDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'auth.delete_group'
    model = Group
    template_name = 'customgroups/groups_delete.html'
    success_url = reverse_lazy('customgroups:list')
