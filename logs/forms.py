from django import forms
from .models import Log

class LogForm(forms.ModelForm):
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
        ]
        widgets = {
            'emotion_state_today': forms.Select(choices=[
                ('calm', 'Calm'),
                ('busy', 'Busy'),
                ('late', 'Late')
            ]),
            # Checkbox 用に明示
            'new_item_today': forms.CheckboxInput(),
            'schedule_changed_today': forms.CheckboxInput(),
            'routine_destination_tomorrow': forms.CheckboxInput(),
            'special_event_tomorrow': forms.CheckboxInput(),
            'extra_items_needed_tomorrow': forms.CheckboxInput(),
            'time_difference_tomorrow': forms.CheckboxInput(),
        }


