from django import forms
from .models import ToDo

class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'content', 'priority', 'due_date']
        widgets = {
            'due_date' : forms.DateTimeInput(attrs={'type' : 'datetime-local'}),
            'content' : forms.Textarea(attrs={'rows' : 4}),
        }
        labels = {
            'title': 'Task Title',
            'content': 'Content',
            'priority': 'Priority Level',
            'due_date': 'Due Date',
        }