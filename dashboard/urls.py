from django.urls import path

from .views import DashboardListView


app_name = 'dashboard'

urlpatterns = [
    path('list/', DashboardListView.as_view(), name='list'),


]