from django.shortcuts import render
from .models import List
from .forms import ListForm
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from .forms import TodoListCreateForm
from .models import TodoList, TodoItem
from datetime import date
from django.contrib.auth.decorators import login_required


# Create your views here.

# 必要要件：忘れ物の確率が５０％を超えた際に、
# 忘れ物に関して記述を行っておライその記述されたものを通知で知らせるようにする。
# なので必要なカラムに関しては、入力してもらったデータをモデルに送信を行う為のカラム
@login_required
def list(request):
  if request.method == 'POST':
    list = List()
    forget_item_1 = request.POST.get('forget_item_1')
    list.save()
    return render(request, 'suggestions/list.html') 
@login_required
def list_form(request):
    today = date.today()
    today_list, created = TodoList.objects.get_or_create(date=today)
    tasks = today_list.items.all()

    # ListFormの処理
    if request.method == 'POST' and 'submit_list' in request.POST:
        form = ListForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            list_obj = List()
            list_obj.must_item_1 = data['must_item_1']
            list_obj.save()
            return redirect('suggestions:show', list_id=list_obj.id)
    else:
        form = ListForm()

    # Todo追加処理
    if request.method == 'POST' and 'submit_task' in request.POST:
        task_text = request.POST.get('task', '').strip()
        if task_text:
            TodoItem.objects.create(list=today_list, task=task_text)
            return redirect('suggestions:list_form')  # 自分にリダイレクト

    return render(request, 'suggestions/list_form.html', {
        'form': form,
        'tasks': tasks,
        'today_list': today_list,
        'is_new': created
    })

@login_required
def show(request, list_id):
  list = get_object_or_404(List, id=list_id)
  return render(request, 'suggestions/show.html', {'list': list})


#　TO ｄOをリスト作成
def create_todo_list(request):
    if request.method == 'POST':
        form = TodoListCreateForm(request.POST)
        if form.is_valid():
            # TodoListを作成
            todo_list = TodoList.objects.create(title=form.cleaned_data['title'])
            
            # タスクを改行で分割して登録
            tasks_text = form.cleaned_data['tasks']
            task_lines = tasks_text.strip().split('\n')
            for line in task_lines:
                if line.strip():
                    TodoItem.objects.create(list=todo_list, task=line.strip())
            
            # 作成完了後、リスト表示ページにリダイレクト
            return redirect('logs:index')
    else:
        form = TodoListCreateForm()

    return render(request, 'suggestions/list_form.html', {'form': form})

def today_todo(request):
  today = date.today()
  today_list, created = TodoList.objects.get_or_create(date=today)
  tasks = today_list.items.all()
  if request == 'POST':
    task_text = request.POST.get('task','').strip()
    if task_text:
      TodoItem.objects.create(list=today_list, task=task_text)
      return redirect('suggestions:list_form', list_id=today_list.id)
  return render(request, 'suggestions/list_form.html', 
                {'tasks': tasks,
                 'today_list': today_list,
                 'is_new': created}) 