from django import forms
from .models import Log

class LogForm(forms.ModelForm):
    emotion_state_today = forms.CharField(
    required=False,
    widget=forms.Select(choices=[
            ('calm', 'いつも通り'),
            ('busy', 'いつもより疲れた'),
            ('late', 'とても疲れた'),
      ])
    )
    class Meta:
        model = Log
        fields = [
            'new_item_today',
            'schedule_changed_today',
            'emotion_state_today',
            'routine_destination_tomorrow',
            'special_event_tomorrow',
            'extra_items_needed_tomorrow',
            'time_difference_tomorrow',
            'will_forget'
        ]
        widgets = {
            'emotion_state_today': forms.Select(choices=[
                ('calm', 'いつも通り'),
                ('busy', 'いつもより疲れた'),
                ('late', 'とても疲れた')
            ]),
            # Checkbox 用に明示
            'new_item_today': forms.CheckboxInput(),
            'schedule_changed_today': forms.CheckboxInput(),
            'routine_destination_tomorrow': forms.CheckboxInput(),
            'special_event_tomorrow': forms.CheckboxInput(),
            'extra_items_needed_tomorrow': forms.CheckboxInput(),
            'time_difference_tomorrow': forms.CheckboxInput(),
        }


class LogDateForm(forms.Form):
    date = forms.DateField(
        label='日付',
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
        error_messages={
            'invalid': '正しい日付を入力してください。',
            'required': '日付は必須です。',
        }
    )