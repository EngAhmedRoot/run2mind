from django.urls import path

from .views import LoginView, LogoutView, PatientsignupView


app_name = 'login'

urlpatterns = [
    path('', LoginView.as_view(), name='default'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(),name='logout'),

    path('patientsignup/', PatientsignupView.as_view(),name='patientsignup'),

]