from django.urls import path

from .views import PatientsListView, PatientsDetailView, PatientsChangeView

app_name = 'patients'

urlpatterns = [
    path('list/', PatientsListView.as_view(), name='list'),
    path('detail/<int:pk>', PatientsDetailView.as_view(), name='detail'),
    path('change/<int:pk>', PatientsChangeView.as_view(), name='change'),

 
]