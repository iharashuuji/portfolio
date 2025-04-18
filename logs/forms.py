from django import forms
from .models import Log

class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = [
            'forgotten_item_place',
            'importance','recovery_difficulty','frequency',
            'size','weight','visibility','forget_count',
            'time_prone','emotion_state',
        ]


