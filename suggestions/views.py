from django.shortcuts import render
from .models import List
from .forms import ListForm
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404


# Create your views here.

# 必要要件：忘れ物の確率が５０％を超えた際に、
# 忘れ物に関して記述を行っておライその記述されたものを通知で知らせるようにする。
# なので必要なカラムに関しては、入力してもらったデータをモデルに送信を行う為のカラム
def list(request):
  if request.method == 'POST':
    list = List()
    forget_item_1 = request.POST.get('forget_item_1')
    list.save()
    return render(request, 'suggestions/list.html') 
  
def list_form(request):
  if request.method == 'POST':
    form = ListForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      list = List()
      list.must_item_1 = data['must_item_1']
      list.save()
      return redirect('suggestions:show', list_id=list.id)
    else:
      form = ListForm()
  return render(request, 'suggestions/list_form.html', {'form': form})


def show(request, list_id):
  list = get_object_or_404(List, id=list_id)
  return render(request, 'suggestions/show.html', {'list': list})

