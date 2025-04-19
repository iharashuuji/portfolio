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
    prediction = request.session.get('prediction', None)
    return render(request, 'logs/index.html', { #ローカル変数をテンプレートに渡す。
        'logs': logs,
        'prediction': prediction,
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
        form = LogForm(request.POST)
        if form.is_valid():
            form.save()

            # 🔽 予測用の特徴量を取得
            features = [
                int(request.POST.get('time_difference_tomorrow', 'False') == 'True'),
                int(request.POST.get('extra_items_needed_tomorrow', 'False') == 'True'),
                int(request.POST.get('routine_destination_tomorrow', 'False') == 'True'),
                int(request.POST.get('new_item_today', 'False') == 'True'),
                int(request.POST.get('schedule_changed_today', 'False') == 'True'),
                int(request.POST.get('emotion_state_today_busy', 'False') == 'True'),
                int(request.POST.get('emotion_state_today_calm', 'False') == 'True'),
                int(request.POST.get('emotion_state_today_late', 'False') == 'True'),
                int(request.POST.get('special_event_tomorrow', 'False') == 'True'),
            ]

            # 🔽 モデル読み込みと予測
            model_path = os.path.join(settings.BASE_DIR, 'model.pkl')
            model = joblib.load(model_path)
            prediction = model.predict([features])[0]

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
  
  
