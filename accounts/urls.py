from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.log_in, name='log_in'),
    path('logout/', views.log_out, name='log_out'),
    path('signup/', views.sign_in, name='sign_in'),
]
