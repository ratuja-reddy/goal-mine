from django import forms
from .models import Goal, HabitLog

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name']

class HabitLogForm(forms.ModelForm):
    class Meta:
        model = HabitLog
        fields = ['goal', 'date', 'achieved']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }