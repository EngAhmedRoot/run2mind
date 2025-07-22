from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView




class SessionappointmentsListView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
    permission_required = 'sessionappointments.view_sessionappointments'
    template_name = 'sessionappointments/sessionappointments_list.html'
    context_object_name = 'sessionappointments'
    queryset = []  # ← هيرجع قائمة فاضية



class SessionappointmentsDetailView(PermissionRequiredMixin, SuccessMessageMixin, DetailView):
    permission_required = 'sessions.view_sessionappointments'
    template_name = 'sessionappointments/sessionappointments_detail.html'


