from django.shortcuts import render
from django.http import HttpResponse
from .models import Log
from .forms import LogForm


# Create your views here.
# This is a controller in Rails

def top(request):
  return render(request, 'logs/top.html')

def index(request):
    name = "John Doe" # ローカル変数
    return render(request, 'logs/index.html', {
        'name': name, # ローカル変数をテンプレートに渡す。
    })

# logは、回答を受信し、送信する関数
def log(request):
    if request.method == 'POST':
        log = Log() # 入力用のインスタンス
        log.name = request.POST.get('name')
        log.usage_date = request.POST.get('usage_date')
        log.usage_time = request.POST.get('usage_time')
        log.usage_place = request.POST.get('usage_place')
        log.frequency = request.POST.get('frequency')
        log.last_used_date = request.POST.get('last_used_date')
        log.importance = request.POST.get('importance')
        log.recovery_difficulty = request.POST.get('recovery_difficulty')
        log.size = request.POST.get('size')
        log.weight = request.POST.get('weight')
        log.visibility = request.POST.get('visibility') == 'True' 
        log.forget_count = request.POST.get('forget_count')
        log.time_prone = request.POST.get('time_prone')
        log.emotion_state = request.POST.get('emotion_state')
        log.save()
        return render(request, 'logs/log.html', {'log': log})
    return render(request, 'logs/index.html')
  
def log_form(request):
  if request.method == 'POST':
    form = LogForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponse("ログが保存されました。")
  else:
    form = LogForm()
  return render(request, 'logs/log_form.html', {'form': form})

def log_list(request):
  logs = Log.objects.all()
  return render(request, 'logs/log_list.html', {'logs': logs})
  
def trained(request):
  logs = Log.objects.all()
  context = {
    'logs': logs
  }
  return render(request, 'trained.html', context)
