from django.contrib import admin
from django.urls import path, include
from suggestions import views
from suggestions import forms

app_name = 'suggestions'
urlpatterns = [
  path('list_form/', views.list_form, name='list_form'),
  path('show/<int:list_id>', views.show, name='show'),

]