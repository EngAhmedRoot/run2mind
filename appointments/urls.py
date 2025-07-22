from django.urls import path
from . import views

from .views import AppointmentsListView, AppointmentsDetailView, AppointmentsAddView, AppointmentsChangeView, AppointmentsDeleteView, get_doctor_schedules, update_patient_order,  check_last_visit


app_name = 'appointments'

urlpatterns = [
    path('list/', AppointmentsListView.as_view(), name='list'),
    path('detail/<int:pk>', AppointmentsDetailView.as_view(), name='detail'),
    path('add/<int:expert_id>/', AppointmentsAddView.as_view(), name='add'),
    path('change/<int:pk>', AppointmentsChangeView.as_view(), name='change'),
    path('delete/<int:pk>', AppointmentsDeleteView.as_view(), name='delete'),

    # AJAX URLs 
    path('get-doctor-schedules/<int:doctor_id>/', views.get_doctor_schedules, name='get_doctor_schedules'),
    path('update-patient-order/', views.update_patient_order, name='update_patient_order'),
    path('check-last-visit/', check_last_visit, name='check_last_visit'),
]