from django import forms
from .models import List

class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = [
            'must_item_1',
            # 'must_item_2',
            # 'must_item_3',
            # 'must_item_4',
            # 'must_item_5',
            # 'must_item_6'
        ]
        widgets = {
            'must_item_1': forms.TextInput(attrs={'placeholder': '忘れ物1'}),

        }
        
class TodoListCreateForm(forms.Form):
  title = forms.CharField(label='リスト名', max_length=100)
  tasks = forms.CharField(label='タスク（改行区切り）', widget=forms.Textarea)