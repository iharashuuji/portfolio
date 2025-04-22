from django.shortcuts import render
from django.http import HttpResponse
from .models import Log
from .forms import LogForm
from .forms import LogDateForm
import pandas as pd
import os
from django.conf import settings
import joblib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from datetime import date
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404






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

@login_required
def index(request): 
    today_log = Log.objects.get_or_create(date=now().date())[0]
    suggestions = today_log.suggestions.all()
    logs = Log.objects.all()
    last_log = logs.last()
    prediction = request.session.pop('prediction', None)
        # 安全に float 変換（None 対応込み）
    try:
        prediction = float(prediction) if prediction is not None else None
    except ValueError:
        prediction = None
    return render(request, 'logs/index.html',{
        'logs': logs,
        'prediction': prediction,
        'last_log':last_log,
        'suggestions': suggestions,
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

@login_required
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
@login_required
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