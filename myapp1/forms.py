from django import forms
from .models import Task, Comments, Order, ComicsMangas, Categories, Publisher, Genres

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
        

class FilterForm(forms.Form):
    category = forms.ModelMultipleChoiceField(
        queryset=Categories.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # O cualquier otro widget que prefieras
        required=False,
    )
    publisher = forms.ModelChoiceField(queryset=Publisher.objects.all(), required=False)
    genre = forms.ModelChoiceField(queryset=Genres.objects.all(), required=False)