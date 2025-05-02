from django import forms
from .models import TodoList, TodoItem
from django.forms import inlineformset_factory
from .models import TodoList, TodoItem

TodoItemFormSet = inlineformset_factory(
    TodoList,
    TodoItem,
    fields=('task',),
    extra=1
)


# class ListForm(forms.ModelForm):
#     class Meta:
#         model = TodoItem # LISTから変更済み
#         fields = [
#             'task'
#         ]
#         widgets = {
#             'task': forms.TextInput(attrs={'placeholder': '忘れ物1'}),
#         }
        
class TodoListCreateForm(forms.ModelForm):
    class Meta:
        model = TodoList
        # title = forms.CharField(label='リスト名', max_length=100)
        # fields = ['title'] 
        exclude = ['log', 'date']
        tasks = forms.CharField(label='タスク（改行区切り）', widget=forms.Textarea)

