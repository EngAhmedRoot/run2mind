from collections import defaultdict
from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib import messages 
from .forms import GrouppermissionsForm

class GrouppermissionsListView(PermissionRequiredMixin, ListView):
    permission_required = 'auth.view_group'
    model = Group
    context_object_name = 'groups'
    template_name = 'customgrouppermissions/grouppermissions_list.html'


class GrouppermissionsDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'auth.view_group'
    model = Group
    form_class = GrouppermissionsForm
    template_name = 'customgrouppermissions/grouppermissions_details.html' 
    context_object_name = 'group'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        permissions = Permission.objects.all()
        
        grouped_permissions = defaultdict(lambda: {
            'add': [],
            'change': [],
            'delete': [],
            'view': []
        })


        for permission in permissions:
            model = permission.content_type.model
            if permission.codename.startswith('add_'):
                grouped_permissions[model]['add'].append(permission)
            elif permission.codename.startswith('change_'):
                grouped_permissions[model]['change'].append(permission)
            elif permission.codename.startswith('delete_'):
                grouped_permissions[model]['delete'].append(permission)
            elif permission.codename.startswith('view_'):
                grouped_permissions[model]['view'].append(permission)


        context['grouped_permissions'] = dict(grouped_permissions)
        
        context['group_permissions'] = self.object.permissions.all()          

        return context


class GrouppermissionsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'auth.change_group'
    model = Group
    form_class = GrouppermissionsForm
    template_name = 'customgrouppermissions/grouppermissions_create.html' 
    success_url = reverse_lazy('customgrouppermissions:list')

    def form_valid(self, form):
        group_name = form.cleaned_data['name'] 
        if Group.objects.exclude(pk=self.object.pk).filter(name=group_name).exists():
            messages.error(self.request, f'A group with the name "{group_name}" already exists.')
            return self.form_invalid(form)

        try:
            form.instance.clean()
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        permissions = Permission.objects.all()
        
        grouped_permissions = defaultdict(lambda: {
            'add': [],
            'change': [],
            'delete': [],
            'view': []
        })

        for permission in permissions:
            model = permission.content_type.model
            if permission.codename.startswith('add_'):
                grouped_permissions[model]['add'].append(permission)
            elif permission.codename.startswith('change_'):
                grouped_permissions[model]['change'].append(permission)
            elif permission.codename.startswith('delete_'):
                grouped_permissions[model]['delete'].append(permission)
            elif permission.codename.startswith('view_'):
                grouped_permissions[model]['view'].append(permission)

        context['grouped_permissions'] = dict(grouped_permissions)
        
        print("Grouped Permissions:")
        for model, perms in grouped_permissions.items():
            print(f"Model: {model}, Permissions: {perms}")

        return context


