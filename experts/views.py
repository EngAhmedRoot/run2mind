from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .forms import ExpertsForm
from .models import Experts


# Create your views here.
class ExpertsListView(PermissionRequiredMixin,  SuccessMessageMixin, ListView):
    permission_required = 'experts.view_experts'
    model = Experts
    context_object_name = 'experts'
    template_name = 'experts/experts_list.html'

    def get_queryset(self):
        user = self.request.user
        
        if user.is_superuser or user.is_staff:
            return Experts.objects.all()
        elif user.user_type == 'admin':
            return Experts.objects.all()
        elif user.user_type == 'expert':
            return Experts.objects.filter(user=user, user__is_active=True)
        elif user.user_type == 'patient':
            return Experts.objects.filter(user__is_active=True)
        else:
            return Experts.objects.none()


class ExpertsDetailView(PermissionRequiredMixin, SuccessMessageMixin, DetailView):
    permission_required = 'experts.view_experts'
    model = Experts
    template_name = 'experts/experts_detail.html'


    def get_queryset(self):
        user = self.request.user
        
        if user.is_superuser or user.is_staff:
            return Experts.objects.all()
        elif user.user_type == 'admin':
            return Experts.objects.all()
        elif user.user_type == 'expert':
            return Experts.objects.filter(user=user, user__is_active=True)
        elif user.user_type == 'patient':
            return Experts.objects.filter(user__is_active=True)
        else:
            return Experts.objects.none()




class ExpertsChangeView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'experts.change_experts'
    model = Experts
    form_class = ExpertsForm
    template_name = 'experts/experts_add.html'
    success_url = reverse_lazy('experts:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  
        return kwargs

    def get_queryset(self):
        user = self.request.user       
        if user.is_superuser or user.is_staff:
            return Doctors.objects.all()
        elif user.user_type == 'admin':
            return Doctors.objects.all()
        elif user.user_type == 'expert':
            return Doctors.objects.filter(user=user, user__is_active=True)
        else:
            return Doctors.objects.none()

    #get current user
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        print("Form is valid. Attempting to update the doctor.")        
        doctor = form.save(commit=False)  
        doctor.user = form.cleaned_data['user']  
        doctor.updated_by = self.request.user
        doctor.save()   
   
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error, extra_tags='error')
        return super().form_invalid(form)



