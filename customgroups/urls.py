from django.urls import path

from .views import GroupsListView, GroupsDetailView, GroupsCreateView, GroupsUpdateView, GroupsDeleteView


app_name = 'customgroups'

urlpatterns = [
    path('list/', GroupsListView.as_view(), name='list'),
    path('details/<int:pk>', GroupsDetailView.as_view(), name='details'),
    path('create/', GroupsCreateView.as_view(), name='create'),
    path('update/<int:pk>', GroupsUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', GroupsDeleteView.as_view(), name='delete'),

]