from django.shortcuts import render
from django.http import HttpResponse
from .models import Log
from .forms import LogForm
from .forms import LogDateForm
import pandas as pd
import os
from django.conf import settings
import joblib
from datetime import timedelta
from suggestions.models import TodoList, TodoItem
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from datetime import date
from django.db.models import Q
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import matplotlib.pyplot as plt
import io
import urllib, base64
from proposals.models import List, Item




# Create your views here.
# This is a controller in Rails

def top(request):
    if request.method == 'POST':
        form = LogDateForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['date']

            # その日付のログがすでにあるかチェック
            log = Log.objects.filter(user=request.user, date=selected_date).first()

            if log:
                # ログがすでに存在する場合、そのログフォームに遷移
                return redirect('logs:log_form_edit', log_id=log.id)
            else:
                # ログがない場合、新規作成フォームに遷移
                return redirect('logs:log_form_create', date=selected_date)
    else:
        form = LogDateForm()

    return render(request, 'logs/top.html', {'form': form, 'date':date})

def index(request): 
    yesterday = now().date() - timedelta(days=1)
    today = now().date()
    
    today_list, created = TodoList.objects.get_or_create(date=today)
    yesterday_log = Log.objects.filter(date=yesterday).first()


    suggestions = TodoList.objects.filter(date=yesterday).first()
    # suggestions_today = today_list.items.all() if today_list else []
    logs = Log.objects.all()
    last_log = logs.last()
    prediction = request.session.pop('prediction', None)
        # 安全に float 変換（None 対応込み）
        #   list = get_object_or_404(TodoList, id=list_id)
        #   tasks = list.items.all()
    try:
        if prediction is not None:
            prediction = float(prediction)  # ← 修正済み：ここで str を float に変換
            prediction = int(prediction * 100)
        else:
            prediction=None
    except ValueError:
        prediction = None
        
        
    ###########
# 変数task_textを初期化
    task_text = None

# TodoListの取得
    list = TodoList.objects.filter(date=today).order_by('-date').first()    
    if list is not None:
        tasks = list.items.all()
    else:
        tasks = []

    yesterday_list = TodoList.objects.filter(date=yesterday).order_by('-date').first()
    if yesterday_list is not None:
        yesterday_item = yesterday_list.items.all()
    else:
        yesterday_item = []


    if request.method == 'POST':
    # POSTデータからタスクテキストを取得
        task_text = request.POST.get('new_task', '').strip()
    
    # task_textが空でない場合にタスクを作成
    if task_text:
        TodoItem.objects.create(list=list, task=task_text)
        tasks = list.items.all()  # 更新されたタスクリストを取得
    ############
    
    
    # 可視化
    x = Log.objects.filter(will_forget=1).count()
    y = Log.objects.filter(will_forget=0).count()
    plt.bar(['Will Forget', 'Will Not Forget'], [x, y])
    # バッファに保存
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()
    # base64にエンコードしてテンプレートに渡す
    graph = base64.b64encode(image_png).decode('utf-8')
    ###
    
    mokuhyou = List.objects.filter(date=today).first()
    if mokuhyou is not None: 
       mokuhyou_items = mokuhyou.items.all()
    else:
        mokuhyou_items = []
    
    
    return render(request, 'logs/index.html',{
        'logs': logs,
        'prediction': prediction,
        'last_log':last_log,
        'tasks': tasks,
        'yesterday_item':yesterday_item,
        'today_list':today_list,
        'suggestions': suggestions,
        'graph': graph,
        'mokuhyou_items':mokuhyou_items,
    })

# logは、回答を受信し、送信する関数
def log(request):
    if request.method == 'POST':
        log = Log() # 入力用のインスタンス
        # 今日の状況
        log.new_item_today = request.POST.get('新しいものをもったか？') == 'True'
        log.schedule_changed_today = request.POST.get('いつもとスケジュールが異なったか？') == 'True'
        log.emotion_state_today = request.POST.get('どのような感情だったか？')
        # 明日の予定
        log.routine_destination_tomorrow = request.POST.get('明日はいつもの場所に行くか') == 'True'
        log.special_event_tomorrow = request.POST.get('明日特別な予定があるか') == 'True'
        log.extra_items_needed_tomorrow = request.POST.get('明日は追加の持ち物があるか') == 'True'
        log.time_difference_tomorrow = request.POST.get('明日はいつもと違う時間に出発するか') == 'True'
        log.save()
        return render(request, 'logs/log_form_create.html', {'log': log})
    return render(request, 'logs/index.html')
  
from django.utils.timezone import now

def log_form(request, log_id=None):
    if log_id:
        return redirect('logs:log_form_edit', log_id=log_id)

    log = None

    if request.method == 'POST':
        # 今日の日付に対応する Log があるか確認（なければ作る）
        log, created = Log.objects.get_or_create(date=now().date())

        form = LogForm(request.POST, instance=log)

        if form.is_valid():
            data = form.cleaned_data

            # will_forget は後で追加するので一旦 None
            log.will_forget = None

            # 感情のワンホットエンコード
            emotion_onehot = [
                1 if data['emotion_state_today'] == 'busy' else 0,
                1 if data['emotion_state_today'] == 'calm' else 0,
                1 if data['emotion_state_today'] == 'late' else 0,
            ]

            # モデル予測用特徴量
            features = [
                int(data['time_difference_tomorrow']),
                int(data['extra_items_needed_tomorrow']),
                int(data['routine_destination_tomorrow']),
                int(data['new_item_today']),
                int(data['schedule_changed_today']),
                *emotion_onehot,
                int(data['special_event_tomorrow']),
            ]

            model_path = os.path.join(settings.BASE_DIR, 'model.pkl')
            model = joblib.load(model_path)
            prediction = model.predict_proba([features])[0][1]
            request.session['prediction'] = str(prediction)

            # 保存
            log.save()
            return redirect('logs:index')
    else:
        # GET のときも今日の Log を使う
        log, _ = Log.objects.get_or_create(date=now().date())
        form = LogForm(instance=log)

    return render(request, 'logs/log_form.html', {'form': form, 'log': log})

 
 # 既存のFORMの編集用
def log_form_edit(request, log_id):
  # 既存のものを見つける。
  log = get_object_or_404(Log, id=log_id)
  if request.method == 'POST':
    form = LogForm(request.POST, instance=log)
    if form.is_valid():
      form.save()
      return redirect('logs:index')
  else:
    form = LogForm(instance=log) 
  return render(request, 'logs/log_form_edit.html', {'log':log, 'form': form})

def confirm_label(request, log_id):
    log = Log.objects.get(id=log_id)
    prediction = request.session.pop('prediction', None)
    # 安全に float 変換（None 対応込み）
    try:
        prediction = float(prediction) if prediction is not None else None
    except ValueError:
        prediction = None
    return render(request, 'logs/index.html', {
        'log': log,
        'prediction': prediction,
    })