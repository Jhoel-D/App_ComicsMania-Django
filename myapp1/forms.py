from django import forms
from .models import Task, Comments

class TaskForm (forms.ModelForm):
    class Meta:
        model = Task
        fields =  ['title', 'descripction', 'important']
        widgets ={
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a title'}),
            'descripction': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a description'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input text-center'}),
        }
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['review_comment']