from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

def sign_in(request):
    if request.method == 'POST':
      username = request.POST.get('username')
      passward = request.POST.get('passward')
      if User.objects.filter(username=username).exists():
        messages.error(request,'このユーザーはすでに存在します')
        return redirect('accounts:sign_in')
      else:
        user = User.objects.create_user(username=username, password=passward)
        login(request, user)
        return redirect('logs:index')
    return render(request, 'accounts/sign_in.html')
  
def log_out(request):
    logout(request)
    return render(request, 'accouts/log_in.html')
    
  
  
def log_in(request):
    if request.method == 'POST':
      usernmae = request.POST.get('username')
      passward = request.POST.get('passward')
      user = authenticate(request, username=usernmae, password=passward)
      if user is not None:
        login(request, user)
        return redirect('logs:index')
      else:
        messages.error(request, 'ユーザー名 or パスワードの誤り')
        return redirect('accoutns:log_in')
      
    return render(request, 'accounts/log_in.html')