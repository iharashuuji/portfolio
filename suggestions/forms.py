from djangpo import forms
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