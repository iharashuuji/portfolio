from django.shortcuts import render
from .models import List

# Create your views here.

# 必要要件：忘れ物の確率が５０％を超えた際に、
# 忘れ物に関して記述を行っておライその記述されたものを通知で知らせるようにする。
# なので必要なカラムに関しては、入力してもらったデータをモデルに送信を行う為のカラム
def post_list(request):
  if request.method == 'POST':
    list = List()
    forget_item_1 = request.POST.get('forget_item_1')
    list.save()
    return render(request, 'suggestions/list.html') 
  
def post_list_form(request):
  if request.method == 'POST':
    form = ListForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      list = List()
      list.must_item_1 = data['must_item_1']
      list.save()
      return render(request, 'suggestions/list.html')
  return render(request, 'suggestions/list_form.html')