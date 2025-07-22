from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from datetime import date
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .forms import PatientsForm
from .models import Patients


# Create your views here.

class PatientsListView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
    permission_required = 'patients.view_patients'
    model = Patients
    context_object_name = 'patients'
    template_name = 'patients/patients_list.html'

    def get_queryset(self):
        user = self.request.user

        # تحديد القيم الأساسية بناءً على نوع المستخدم
        if user.is_superuser or user.is_staff:
            queryset = Patients.objects.all()
        elif user.user_type == 'admin':
            queryset = Patients.objects.all()
        elif user.user_type == 'expert':
            queryset = Patients.objects.all()
        elif user.user_type == 'patient':
            queryset = Patients.objects.none()
        else:
            queryset = Patients.objects.none()


        # إضافة الفلاتر الأخرى

        name_filter = self.request.GET.get('name', '')
        if name_filter:
            queryset = queryset.filter(name__icontains=name_filter)

        phone_filter = self.request.GET.get('phone', '')
        if phone_filter:
            queryset = queryset.filter(phone__icontains=phone_filter)

        gender_filter = self.request.GET.getlist('gender', [])
        if gender_filter:
            queryset = queryset.filter(gender__in=gender_filter)

        # فلترة الأسعار
        min_age = self.request.GET.get('min_age', None)
        max_age = self.request.GET.get('max_age', None)
        if min_age and max_age:
            today = date.today()
            min_birthdate = today.replace(year=today.year - int(min_age))
            max_birthdate = today.replace(year=today.year - int(max_age) - 1, month=today.month, day=today.day)
            queryset = queryset.filter(birthdate__range=(max_birthdate, min_birthdate))

        queryset = queryset.distinct().order_by('id')  # لضمان أن النتائج متميزة (عدم تكرار النتائج)
        return queryset


    def render_to_response(self, context, **response_kwargs):
        request = self.request
        page = request.GET.get('page', 1)
    
        queryset = self.get_queryset()
    
        paginate_by = 4  
    
        paginator = Paginator(queryset, paginate_by)
        page_obj = paginator.get_page(page)
    
        context['patients'] = page_obj 
        context['page_obj'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
    
        current_page = page_obj.number
        total_pages = paginator.num_pages
    
        start_page = max(current_page - 1, 1)
        end_page = min(current_page + 1, total_pages)
    
        context['page_range'] = range(start_page, end_page + 1)
    
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string(
                'patients/_patients_list_partial.html',
                context,
                request=request
            )
            return JsonResponse({'html': html})
    
        return super().render_to_response(context, **response_kwargs)
    








class PatientsDetailView(PermissionRequiredMixin, SuccessMessageMixin, DetailView):
    permission_required = 'patients.view_patients'
    model = Patients
    template_name = 'patients/patients_detail.html'

    def get_queryset(self):
        user = self.request.user

        # تحديد القيم الأساسية بناءً على نوع المستخدم
        if user.is_superuser or user.is_staff:
            queryset = Patients.objects.all()
        elif user.user_type == 'admin':
            queryset = Patients.objects.all()
        elif user.user_type == 'expert':
            queryset = Patients.objects.all()
        elif user.user_type == 'patient':
            queryset = Patients.objects.none()
        else:
            queryset = Patients.objects.none()

        return queryset





class PatientsChangeView(PermissionRequiredMixin, UpdateView):
    permission_required = 'patients.change_patients'
    model = Patients
    form_class = PatientsForm
    template_name = 'patients/patients_add.html'
    success_url = reverse_lazy('patients:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  
        return kwargs

    def get_queryset(self):
        user = self.request.user       
        if user.is_superuser or user.is_staff:
            return Patients.objects.all()
        elif user.user_type == 'admin':
            return Patients.objects.all()
        elif user.user_type == 'doctor':
            return Patients.objects.filter(user__is_active=True)
        elif user.user_type == 'patient':
            return Patients.objects.filter(user=user, user__is_active=True)
        else:
            return Patients.objects.none()

    def form_valid(self, form):    
        patient = form.save(commit=False)  
        patient.user = form.cleaned_data['user']  
        patient.updated_by = self.request.user
        patient.save()   
   
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error, extra_tags='error')
        return super().form_invalid(form)


