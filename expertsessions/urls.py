from django.urls import path

from .views import (ExpertsessionsListView,  ExpertsessionsDetailView)


app_name = 'expertsessions'

urlpatterns = [
    path('list/', ExpertsessionsListView.as_view(), name='list'),
    path('detail/<int:pk>', ExpertsessionsDetailView.as_view(), name='detail'),

]