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



