from django import forms
from .models import Log

class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = [
            'name','usage_date','usage_time',
            'usage_place','frequency','last_used_date',
            'importance','recovery_difficulty',
            'size','weight','visibility','forget_count',
            'time_prone','emotion_state','reminder_set',
        ]
        widgets = {
            'usage_date': forms.DateInput(attrs={'type': 'date'}),
            'last_used_date': forms.DateInput(attrs={'type': 'date'}),
            'usage_time': forms.TimeInput(attrs={'type': 'time'}),
        }
