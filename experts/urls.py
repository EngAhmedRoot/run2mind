from django.urls import path

from .views import (ExpertsListView, ExpertsDetailView, ExpertsChangeView)


app_name = 'experts'

urlpatterns = [
    path('list/', ExpertsListView.as_view(), name='list'),
    path('detail/<int:pk>', ExpertsDetailView.as_view(), name='detail'),
    path('change/<int:pk>', ExpertsChangeView.as_view(), name='change'),

]