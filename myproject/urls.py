"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),  # accountsアプリ
    # ユーザーが未認証の場合はサインアップにリダイレクト
    path('', lambda request: redirect('accounts:sign_in') if not request.user.is_authenticated else redirect('logs:index')),
    path('', include('logs.urls', namespace='logs')),
    path('suggestions/', include('suggestions.urls', namespace='suggestions')),
    path('proposals/', include('proposals.urls', namespace='proposals')),
]
