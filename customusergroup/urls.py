from django.urls import path

from .views import CustomusergroupListView, CustomusergroupDetailView,  CustomusergroupUpdateView


app_name = 'customusergroup'

urlpatterns = [
    path('list/', CustomusergroupListView.as_view(), name='list'),
    path('details/<int:pk>', CustomusergroupDetailView.as_view(), name='details'),
    path('update/<int:pk>', CustomusergroupUpdateView.as_view(), name='update'),
]