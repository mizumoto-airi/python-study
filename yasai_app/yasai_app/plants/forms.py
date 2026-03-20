from django import forms
from .models import Plant

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'season', 'sow_month', 'harvest_month', 'days_to_harvest', 'memo']
        labels = {
            'name': '野菜名',
            'season': '季節',
            'sow_month': '種まきの月',
            'harvest_month': '収穫の月',
            'days_to_harvest': '収穫までの日数',
            'memo': 'メモ',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'border-radius: 10px; border: 2px solid #4caf50;',
                'placeholder': '例：トマト',
            }),
            'season': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'border-radius: 10px; border: 2px solid #4caf50;',
                'placeholder': '例：夏',
            }),
            'sow_month': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'border-radius: 10px; border: 2px solid #4caf50;',
                'placeholder': '例：4',
            }),
            'harvest_month': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'border-radius: 10px; border: 2px solid #4caf50;',
                'placeholder': '例：7',
            }),
            'days_to_harvest': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'border-radius: 10px; border: 2px solid #4caf50;',
                'placeholder': '例：90',
            }),
            'memo': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'border-radius: 10px; border: 2px solid #4caf50;',
                'rows': 3,
                'placeholder': '自由にメモを書いてください',
            }),
        }