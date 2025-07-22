from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.exceptions import ValidationError

from .forms import CustomusergroupForm  
from customusers.models import Customusers  


class CustomusergroupListView(PermissionRequiredMixin, ListView):
    permission_required = 'usersmanagement.view_customusergroup'
    model = Customusers
    context_object_name = 'users'
    template_name = 'customusergroup/customusergroup_list.html'    

    def get_queryset(self):
        return Customusers.objects.filter(is_superuser=False, is_staff=False)


class CustomusergroupDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'customusergroup.view_customusergroup'
    model = Customusers
    template_name = 'customusergroup/customusergroup_detail.html' 



class CustomusergroupUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'customusergroup.change_customusergroup'
    model = Customusers
    form_class = CustomusergroupForm
    template_name = 'customusergroup/customusergroup_update.html'  
    success_url = reverse_lazy('customusergroup:list')

    def form_valid(self, form):
        print(form.cleaned_data) 
        user = form.save(commit=False)

        group = form.cleaned_data.get('group')

        if group:
            user.groups.clear()
            user.groups.add(group)

        user.save()

        return super().form_valid(form)


