from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from .forms import TodoListCreateForm, TodoItemFormSet
from .models import TodoList, TodoItem
from datetime import date
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from logs.models import Log
from .models import get_today_log


# Create your views here.

# 必要要件：忘れ物の確率が５０％を超えた際に、
# 忘れ物に関して記述を行っておライその記述されたものを通知で知らせるようにする。
# なので必要なカラムに関しては、入力してもらったデータをモデルに送信を行う為のカラム
def list(request):
  if request.method == 'POST':
    list = TodoList()  # LISTから変更済み
    forget_item_1 = request.POST.get('forget_item_1')
    list.save()
    return render(request, 'suggestions/list.html') 

# def list_form(request):
#     today = date.today() #+ timedelta(days=1)
#     yesterday = date.today() - timedelta(days=1)
#     log = get_today_log()
#     try:
#         today_list = TodoList.objects.filter(date=today).order_by('-created_at').first()
#     except TodoList.DoesNotExist:
#         today_list = None   
#     try:
#         yesterday_list = TodoList.objects.get(date=yesterday)
#     except TodoList.DoesNotExist:
#         yesterday_list = None   
#     tasks = today_list.items.all() if today_list else []
#     tasks_yesterday = yesterday_list.items.all() if yesterday_list else []
#     task_formset = None

#     # ListFormの処理
#     if request.method == 'POST' :
#       if today_list:
#         today_list.save()
#         return redirect('suggestions:show', list_id=today_list.id)
#       else:
#         form = TodoListCreateForm(request.POST)
#         if form.is_valid() :
#         # まずリスト（親）を保存
#           today_list = form.save(commit=False)
#           today_list.log = log  # logは自動でセット
#           today_list.date = today  # 日付も手動でセット
#           today_list.save()
#           task_formset = TodoItemFormSet(request.POST, instance=today_list)
#         # 次にタスク（子）たちを保存
          
#           if task_formset.is_valid():
#             task_formset.save()
#             return redirect('suggestions:show', list_id=today_list.id)
#           else:
#             dummy_list = TodoList()
#             task_formset = TodoItemFormSet(request.POST, instance=dummy_list)

#     else:
#         form = TodoListCreateForm()
#         dummy_list = TodoList()
#         task_formset = TodoItemFormSet(instance=dummy_list)



#     return render(request, 'suggestions/list_form.html', {
#         'form': form,
#         'tasks': tasks,
#         'today_list': today_list,
#         'task_formset' : task_formset,
#         'tasks_yesterday': tasks_yesterday,
#     })

def show(request, list_id):
  today = now().date()
  list = TodoList.objects.filter(date=today).order_by('-created_at').first()
  if not list:  # 今日のリストが存在しない場合、新たに作成
    list = TodoList.objects.create(date=today)
  tasks = list.items.all()
  if request.method == 'POST':
    task_text = request.POST.get('new_task','').strip() #昨日のTASKをいったん全て取得
    if task_text:
      #if task_text: # ここで、タスクがあるかを確認。ただ確認する意味はない。
      TodoItem.objects.create(list=list, task=task_text) #
      tasks = list.items.all()
  return render(request, 'suggestions/show.html', {'list': list, 'tasks': tasks})



def today_todo(request):
  yesterday = date.today() - timedelta(days=1)
  today_list, created = TodoList.objects.get_or_create(date=yesterday)
  tasks = today_list.items.all()
  if request.method   == 'POST':
    task_text = request.POST.get('task','').strip()
    if task_text:
      TodoItem.objects.create(list=today_list, task=task_text)
      return redirect('suggestions:list_form', list_id=today_list.id)
  return render(request, 'suggestions/list_form.html', 
                {'tasks': tasks,
                 'today_list': today_list,
                 'is_new': created}) 
  
  
def delete(request, item_id):
  item = get_object_or_404(TodoItem, id=item_id)
  if request.method == 'POST':
    item.delete()
  return redirect('logs:index')