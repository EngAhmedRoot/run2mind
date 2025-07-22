from django.urls import path

from .views import GrouppermissionsListView, GrouppermissionsDetailView,  GrouppermissionsUpdateView


app_name = 'customgrouppermissions'

urlpatterns = [
    path('list/', GrouppermissionsListView.as_view(), name='list'),
    path('details/<int:pk>', GrouppermissionsDetailView.as_view(), name='details'),
    path('update/<int:pk>', GrouppermissionsUpdateView.as_view(), name='update'),

]