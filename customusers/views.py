from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth import update_session_auth_hash

from django.http import JsonResponse
from django.views import View

from django.utils import timezone

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.urls import reverse


from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import CustomusersChangeForm,  ChangePasswordForm  
from .models import Customusers  


from experts.models import Experts  
from patients.models import Patients


class UserprofileDetailView(PermissionRequiredMixin, SuccessMessageMixin, DetailView):
    model = Customusers
    permission_required = 'customusers.view_customusers'
    template_name = 'customusers/userprofile_detail.html'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = self.request.user
        context['customuser'] = user
        
        profile = Experts.objects.filter(user=user).first() or \
                  Patients.objects.filter(user=user).first() 
            

        if profile:
            context['profile'] = profile
            context['edit_profile_url'] = reverse(f'{profile._meta.app_label}:change', kwargs={'pk': profile.id})


            if isinstance(profile, Experts):
                context['edit_user_details_url'] = reverse('experts:change', kwargs={'pk': profile.id})
            elif isinstance(profile, Patients):
                context['edit_user_details_url'] = reverse('patients:change', kwargs={'pk': profile.id})


        context['edit_user_url'] = reverse('customusers:change', kwargs={'pk': user.id})

        return context


class CustomusersListView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
    permission_required = 'usersmanagement.view_customusers'
    model = Customusers
    context_object_name = 'users'
    template_name = 'customusers/customusers_list.html'    

    def get_queryset(self):
        user = self.request.user
        
        if user.is_superuser or user.is_staff:
            return Customusers.objects.filter(is_superuser=False, is_staff=False)        
        elif user.user_type == 'admin':
            return Customusers.objects.all()
        elif user.user_type == 'doctor':
            return Customusers.objects.filter(doctor__user=user, doctor__user__is_active=True)
        elif user.user_type == 'patient':
            return Customusers.objects.filter(patient__user=user, patient__user__is_active=True)
        else:
            return Doctorschedules.objects.none()


class CustomusersDetailView(PermissionRequiredMixin, SuccessMessageMixin, DetailView):
    permission_required = 'customusers.view_customuser'
    model = Customusers
    template_name = 'customusers/customusers_detail.html' 

    def has_permission(self):
        user = self.request.user
        # السماح لمجموعات معينة
        if user.is_superuser or user.user_type in ['admin', 'expert', 'patient']:
            return True
        return super().has_permission()

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Customusers.objects.filter(is_superuser=False, is_staff=False)
        elif user.user_type in ['admin', 'expert', 'patient']:
            return Customusers.objects.all()
        else:
            return Customusers.objects.none()



class CustomusersChangeView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'customusers.change_customusers'
    model = Customusers
    form_class = CustomusersChangeForm
    template_name = 'customusers/customusers_change.html'  

    def get_success_url(self):
        # طباعة معرف المستخدم لتأكيد الوجهة
        print(f"Redirecting to user profile page with pk: {self.object.pk}")
        return reverse('customusers:userprofile', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        user = self.request.user
        print(f"Current user: {user.username}, user_type: {user.user_type}")

        if user.is_superuser or user.is_staff:
            queryset = Customusers.objects.filter(is_superuser=False, is_staff=False)
            print(f"Queryset for superuser/staff: {queryset}")
            return queryset
        elif user.user_type in ['admin', 'expert', 'patient']:
            queryset = Customusers.objects.all()
            print(f"Queryset for {user.user_type}: {queryset}")
            return queryset
        else:
            print("No queryset available for this user.")
            return Customusers.objects.none()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # طباعة بيانات المستخدم التي يتم تمريرها للنموذج
        print(f"Form kwargs: {kwargs}")
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        customuser = form.save(commit=False)  
        customuser.updated_by = self.request.user
        customuser.save()
        # طباعة بيانات المستخدم بعد الحفظ
        print(f"User updated successfully: {customuser}")
        messages.success(self.request, 'تم تحديث المستخدم بنجاح.', extra_tags='success')
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form validation failed with errors:")
        for field, errors in form.errors.items():
            for error in errors:
                # طباعة الأخطاء في الفورم
                print(f"Field: {field}, Error: {error}")
                messages.error(self.request, error, extra_tags='error')
        return super().form_invalid(form)

    def assign_user_to_group(self, customuser, user_type):
        user_type_to_group = {
            'admin': 'Admin-Group',
            'expert': 'Expert-Group',
            'patient': 'Patient-Group',
            'user': 'User-Group',
        }
        group_name = user_type_to_group.get(user_type)
        print(f"Assigning user {customuser.username} to group {group_name}")

        if group_name:
            try:
                type_group = Group.objects.get(name=group_name)
                customuser.groups.add(type_group)
                print(f"User {customuser.username} added to group {group_name}")
            except Group.DoesNotExist:
                print(f"Group {group_name} does not exist.")
                raise forms.ValidationError(_('The specified group does not exist.'))




class ChangePasswordView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'customusers.change_customusers'
    model = Customusers
    form_class = ChangePasswordForm
    template_name = 'customusers/change_password.html'  

    def get_success_url(self):
        # طباعة معرف المستخدم لتأكيد الوجهة
        print(f"Redirecting to user profile page with pk: {self.object.pk}")
        return reverse('customusers:userprofile', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        user = self.request.user
        print(f"Current user: {user.username}, user_type: {user.user_type}")
        print(f"User: {user}, is_superuser: {user.is_superuser}")
        print(f"Has permission 'customusers.add_customusers': {user.has_perm('customusers.add_customusers')}")
        print(f"User permissions: {user.get_all_permissions()}")

        if user.is_superuser or user.is_staff:
            queryset = Customusers.objects.filter(is_superuser=False, is_staff=False)
            print(f"Queryset for superuser/staff: {queryset}")
            return queryset
        elif user.user_type in ['admin', 'expert', 'patient']:
            queryset = Customusers.objects.all()
            print(f"Queryset for {user.user_type}: {queryset}")
            return queryset
        else:
            print("No queryset available for this user.")
            return Customusers.objects.none()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # طباعة بيانات المستخدم التي يتم تمريرها للنموذج
        print(f"Form kwargs: {kwargs}")
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        customuser = form.save(commit=False)  
        customuser.updated_by = self.request.user
        customuser.save()
        # طباعة بيانات المستخدم بعد الحفظ
        print(f"User updated successfully: {customuser}")
        messages.success(self.request, 'تم تحديث المستخدم بنجاح.', extra_tags='success')
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form validation failed with errors:")
        for field, errors in form.errors.items():
            for error in errors:
                # طباعة الأخطاء في الفورم
                print(f"Field: {field}, Error: {error}")
                messages.error(self.request, error, extra_tags='error')
        return super().form_invalid(form)





class UserGroupMessageView(View):
    def get(self, request, *args, **kwargs):
        user_type = request.GET.get('user_type')
        user_type_to_message = {
            'admin': 'User in Admin-Group',
            'expert': 'User in Expert-Group',
            'patient': 'User in Patient-Group',
        }

        message = user_type_to_message.get(user_type, '')
        return JsonResponse({'message': message})
