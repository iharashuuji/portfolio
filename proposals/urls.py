from django.contrib import admin
from django.urls import path, include
from proposals import views

app_name = 'proposals'
urlpatterns = [
  # path('', views.top, name='top'),
  # path('index/', views.index, name='index'),
  path('show/',views.show, name='show'),
  path('delete/<int:item_id>/', views.delete, name='delete'),

  
]