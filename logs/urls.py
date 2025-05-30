from django.contrib import admin
from django.urls import path, include
from logs import views
from logs import forms

app_name = 'logs'
urlpatterns = [
  path('', views.top, name='top'),
  path('index/', views.index, name='index'),
  # path('log_form/<int:log_id>/', views.confirm_label, name='confirm_label'),
  path('log/', views.log, name='log'),
  path('log_form/', views.log_form, name='log_form'),
  path('log_form/edit/<int:log_id>', views.log_form_edit, name='log_form_edit'),
  
]


