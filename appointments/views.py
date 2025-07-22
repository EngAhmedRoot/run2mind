from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.urls import reverse_lazy

from .forms import AppointmentsForm
from .models import Appointments
from patients.models import Patients
from expertsessions.models import Expertsessions

# Create your views here.
class AppointmentsListView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
    permission_required = 'appointments.view_appointments'
    model = Appointments
    context_object_name = 'appointments'
    template_name = 'appointments/appointments_list.html'

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            queryset = Patients.objects.all()
        elif user.user_type == 'admin':
            queryset = Patients.objects.all()
        elif user.user_type == 'expert':
            queryset = Patients.objects.all()
        elif user.user_type == 'patient':
            queryset = Patients.objects.all()
        else:
            queryset = Patients.objects.none()

        return queryset




class AppointmentsDetailView(PermissionRequiredMixin, SuccessMessageMixin, DetailView):
    permission_required = 'appointments.view_appointments'
    model = Appointments
    template_name = 'appointments/appointments_detail.html'

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
            queryset = Patients.objects.all()
        else:
            queryset = Patients.objects.none()

        return queryset



class AppointmentsAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'appointments.add_appointments'
    model = Appointments
    form_class = AppointmentsForm
    template_name = 'appointments/appointments_add.html'
    success_url = reverse_lazy('appointments:list')

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            queryset = Patients.objects.all()
        elif user.user_type == 'admin':
            queryset = Patients.objects.all()
        elif user.user_type == 'expert':
            queryset = Patients.objects.filter(expert__user=user)  # المرضى المرتبطين بالخبير
        elif user.user_type == 'patient':
            queryset = Patients.objects.filter(user=user)  # المريض الحالي فقط
        else:
            queryset = Patients.objects.none()

        return queryset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # تمرير المستخدم للفورم
        kwargs['expert_id'] = self.kwargs.get('expert_id')  # تمرير expert_id للفورم
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expert_id = self.kwargs.get('expert_id')  # الحصول على expert_id من الرابط
    
        if expert_id:
            expertsessions = Expertsessions.objects.filter(expert_id=expert_id)
        
            # افترض أن كل جلسة لديها سعر واحد فقط
            if expertsessions.exists():
                context['session_price'] = expertsessions.first().session_price
            else:
                context['session_price'] = None

            # جمع sessionduration و availabletimes
            session_durations = set()
            available_times = set()
            languages = set()

            for session in expertsessions:
                session_durations.update(session.sessionduration.all())
                available_times.update(session.availabletimes.all())
                languages.update(session.languages.all())


            context['session_durations'] = session_durations
            context['available_times'] = available_times
            context['languages'] = languages
        else:
            context['session_durations'] = []
            context['available_times'] = []
            context['languages'] = []
            context['session_price'] = None

        return context

    def form_valid(self, form):
        appointment = form.save(commit=False)
        appointment.created_by = self.request.user
        appointment.updated_by = self.request.user

        # ضبط السعر إذا لم يتم إدخاله
        if not appointment.price:
            appointment.price = appointment.expertsession.session_price

        appointment.save()

        messages.success(self.request, _('The appointment has been successfully created!'), extra_tags='success')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error, extra_tags='error')
        return super().form_invalid(form)




class AppointmentsChangeView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'appointments.change_appointments'
    model = Appointments
    form_class = AppointmentsForm
    template_name = 'appointments/appointments_add.html'
    success_url = reverse_lazy('appointments:list')


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
            queryset = Patients.objects.all()
        else:
            queryset = Patients.objects.none()

        return queryset

    #get current user
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        appointment = form.save(commit=False)
    
        appointment.patient_order_in_day = Appointments.objects.filter(
            doctor=form.cleaned_data['doctor'],
            appointment_date=form.cleaned_data['appointment_date'],
            doctorschedule=form.cleaned_data['doctorschedule']
        ).count() + 1  # patient_order_in_day + 1
    
        appointment.updated_by = self.request.user

        appointment.save()

        # Check the current language
        if self.request.LANGUAGE_CODE == 'ar':
            message = "تم تحديث الميعاد بنجاح" #then 'en'
        else:
            message = "Appointment Updated Successfully"

        messages.warning(self.request, message, extra_tags='changed')

        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error, extra_tags='error')
        return super().form_invalid(form)



class AppointmentsDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'appointments.delete_appointments'
    model = Appointments
    template_name = 'appointments/appointments_delete.html'
    success_url = reverse_lazy('appointments:list')


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
            queryset = Patients.objects.all()
        else:
            queryset = Patients.objects.none()

        return queryset

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        delete_type = request.POST.get('delete_type')

        if delete_type == 'delete':
            # Check the current language
            if self.request.LANGUAGE_CODE == 'ar':
                message = "تم حذف الميعاد بنجاح"  #then 'en'
            else:
                message = "Appointment Deleted Successfully"

            messages.success(request, _(message), extra_tags='deleted')
            return super().delete(request, *args, **kwargs)

        elif delete_type == 'deactive':
            self.object.is_confirmed = 'unconfirmed'
            self.object.updated_by = request.user
            self.object.save()

            # Check the current language
            if self.request.LANGUAGE_CODE == 'ar':
                message = "تم تعطيل الميعاد بنجاح"  #then 'en'
            else:
                message = "Appointment Deactived Successfully"

            messages.warning(request, _(message), extra_tags='deactived')
            return redirect(self.success_url)
        else:
            messages.error(request, _('Invalid action.'))
            return redirect(self.success_url)



def get_doctor_schedules(request, doctor_id):
    days_of_week_order = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    doctorschedules = Doctorschedules.objects.filter(doctor_id=doctor_id, is_deleted=False)

    def format_time(time):
        return time.strftime('%H:%M')

    day_choices_dict = dict(Doctorschedules.DAY_CHOICES)

    data = []
    
    for doctorschedule in doctorschedules:
        day_name = day_choices_dict.get(doctorschedule.day_of_week, None)
        if day_name:
            data.append({
                'id': doctorschedule.id,
                'day_of_week': doctorschedule.day_of_week,  
                'day_of_week_name': day_name, 
                'doctorschedule': f"{day_name}: {format_time(doctorschedule.start_time)} - {format_time(doctorschedule.end_time)}",
                'max_patients': doctorschedule.max_patients,
                'max_exception_patients': doctorschedule.max_exception_patients
            })
    
    data.sort(key=lambda x: days_of_week_order.index(x['day_of_week_name']))
    
    return JsonResponse(data, safe=False)


def update_patient_order(request):
    appointment_date = request.GET.get('date')
    doctorschedule_id = request.GET.get('doctorschedule_id')

    if appointment_date and doctorschedule_id:
        try:
            count = Appointments.objects.filter(
                appointment_date=appointment_date,
                doctorschedule_id=doctorschedule_id
            ).count()
        except Exception as e:
            print(f"Error fetching patient order: {e}")
            count = 0

        return JsonResponse({'patient_order_in_day': count + 1})

    return JsonResponse({'patient_order_in_day': 1})


def check_last_visit(request):
    patient_id = request.GET.get('patient_id')
    doctor_id = request.GET.get('doctor_id')
    appointment_date_str = request.GET.get('appointment_date')

    if patient_id and doctor_id and appointment_date_str:
        try:
            appointment_date = timezone.make_aware(
                timezone.datetime.strptime(appointment_date_str, '%Y-%m-%d'),
                timezone.get_current_timezone()
            )

            last_appointment = Appointments.objects.filter(
                patient_id=patient_id,
                doctor_id=doctor_id,
                visitcost__visit_type="Examination",
                is_confirmed='confirmed',
                appointment_date__lte=appointment_date.date()  
            ).order_by('-appointment_date').select_related('visitcost').first()



            if last_appointment is not None:
                visitcost_type = last_appointment.visitcost.visit_type  # الحصول على نوع الزيارة
                print(visitcost_type)
            else:
                print("no")  # إذا لم يتم العثور على زيارة


            if last_appointment:
                last_appointment_date = last_appointment.appointment_date  # الحصول على تاريخ الموعد
                last_appointment_datetime = timezone.make_aware(
                    timezone.datetime.combine(last_appointment_date, timezone.datetime.min.time()),
                    timezone.get_current_timezone()
                )

                if (appointment_date - last_appointment_datetime).days <= 30:
                    return JsonResponse({'follow_up_needed': True})

            else:
                print("no")

        except Exception as e:
            print(f"Error: {e}") 
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'follow_up_needed': False})
