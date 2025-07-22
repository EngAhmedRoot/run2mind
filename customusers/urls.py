from django.urls import path

from .views import CustomusersListView, CustomusersDetailView,  CustomusersChangeView, ChangePasswordView, UserGroupMessageView, UserprofileDetailView


app_name = 'customusers'

urlpatterns = [
    path('list/', CustomusersListView.as_view(), name='list'),
    path('detail/<int:pk>', CustomusersDetailView.as_view(), name='detail'),
    path('change/<int:pk>', CustomusersChangeView.as_view(), name='change'),
    path('changepassword/<int:pk>', ChangePasswordView.as_view(), name='changepassword'),

    path('get_user_group_message/', UserGroupMessageView.as_view(), name='get_user_group_message'),
    path('userprofile/<int:pk>', UserprofileDetailView.as_view(), name='userprofile'),

]