from django.contrib import admin
from django.urls import path
from . import views
from .views import sign_up,log_in,log_out,reset_pass,check_pass,login_employee

urlpatterns = [
    path('sign_up',sign_up ,name='sign_up'),
    path('log_in',log_in ,name='log_in'),
    path('log_out', log_out,name='log_out'),
    path('reset_pass', reset_pass,name='reset_pass'),
    path('check_pass', check_pass,name='check_pass'),
    path('login_employee', login_employee,name='login_employee'),
    #path('', ,name=''),
    #path('', ,name=''),
    #path('', ,name=''),
    #path('', ,name=''),
    #path('', ,name=''),
    #path('', ,name=''),
    #path('', ,name=''),


]
