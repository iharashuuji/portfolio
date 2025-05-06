from django.shortcuts import render
from .models import List, Item
from datetime import date
from django.utils.timezone import now
from .form import ItemFormSet
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404



def show(request):
    today = now().date()
    list = List.objects.filter(date=today).order_by('-created_at').first()

    if not list:  # 今日のリストが存在しない場合、新たに作成
        list, created = List.objects.get_or_create(date=today)

    tasks = list.items.all()

    if request.method == 'POST':
        task_text = request.POST.get('new_task', '').strip()
        proposal_text = request.POST.get('new_proposal', '').strip()
            
        if task_text:
            Item.objects.create(list=list, task=task_text, proposal=proposal_text)
            tasks = list.items.all()

    return render(request, 'proposals/show.html', {'list': list, 'tasks': tasks})


def delete(request, item_id):
  item = get_object_or_404(Item, id=item_id)
  if request.method == 'POST':
    item.delete()
  return redirect('proposals:show')