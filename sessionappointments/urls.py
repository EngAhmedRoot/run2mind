from django.urls import path

from .views import (SessionappointmentsListView, SessionappointmentsDetailView)


app_name = 'sessionappointments'

urlpatterns = [
    path('list/', SessionappointmentsListView.as_view(), name='list'),
    path('detail/<int:pk>', SessionappointmentsDetailView.as_view(), name='detail'),


]