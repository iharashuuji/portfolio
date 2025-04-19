from django.shortcuts import render
from django.http import HttpResponse
from .models import Log
from .forms import LogForm
import pandas as pd
import os
from django.conf import settings
import joblib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect




# Create your views here.
# This is a controller in Rails

def top(request):
  return render(request, 'logs/top.html')

def index(request): 
    logs = Log.objects.all()
    last_log = logs.last() 
    prediction = request.session.pop('prediction', None)
    return render(request, 'logs/index.html',{
        'logs': logs,
        'prediction': prediction,
        'last_log':last_log,
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
        if log.will_forget is None:
            return redirect('logs:confirm_label', log_id=log.id)
        
        return render(request, 'logs/log_form.html', {'log': log})
    return render(request, 'logs/index.html')
  

def log_form(request):
    if request.method == 'POST':
        print(request.POST)
        form = LogForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            emotion_onehot = [
        1 if data['emotion_state_today'] == 'busy' else 0,
        1 if data['emotion_state_today'] == 'calm' else 0,
        1 if data['emotion_state_today'] == 'late' else 0,
        ]

            features = [
        int(data['time_difference_tomorrow']),
        int(data['extra_items_needed_tomorrow']),
        int(data['routine_destination_tomorrow']),
        int(data['new_item_today']),
        int(data['schedule_changed_today']),
        *emotion_onehot,
        int(data['special_event_tomorrow']),
            ]

            print("予測用特徴量:", features)
            
            feature_names = [
            'time_difference_tomorrow',
            'extra_items_needed_tomorrow',
            'routine_destination_tomorrow',
            'new_item_today',
            'schedule_changed_today',
            'emotion_state_today_busy',
            'emotion_state_today_calm',
            'emotion_state_today_late',
            'special_event_tomorrow'
            ]

            df = pd.DataFrame([features], columns=feature_names)




            # 🔽 モデル読み込みと予測
            model_path = os.path.join(settings.BASE_DIR, 'model.pkl')
            model = joblib.load(model_path)
            prediction = model.predict_proba([features])[0][1]

            # 🔽 予測値をセッションに保存
            request.session['prediction'] = str(prediction)

            # 予測結果をJSONで返す（文字列に変換している）
            return redirect('logs:index')  # 予測結果を文字列に変換
        else:
            print("保存に失敗")
            print(form.errors)
    else:
        form = LogForm()
        print("GETリクエスト：フォームを表示")
    return render(request, 'logs/log_form.html', {'form': form})



def confirm_label(request, log_id):
    log = Log.objects.get(id=log_id)
    if request.method == 'POST':
        log.will_forget = request.POST.get('忘れ物をしたか？') == 'True'
        log.save()
        return redirect('logs:index')
    return render(request, 'logs/confirm_label.html', {'log': log})
  
  
