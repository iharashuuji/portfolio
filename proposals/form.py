from django import forms
from .models import List, Item
from django.forms import inlineformset_factory

ItemFormSet = inlineformset_factory(
    List,
    Item,
    fields=('task','proposal'),
    extra=1
)

        
class TodoListCreateForm(forms.ModelForm):
    class Meta:
        model = List
        # title = forms.CharField(label='リスト名', max_length=100)
        # fields = ['title'] 
        exclude = ['log', 'date']
        tasks = forms.CharField(label='タスク（改行区切り）', widget=forms.Textarea)

