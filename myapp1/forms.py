from django import forms
from .models import Task, Comments, Order, ComicsMangas, Categories, Publisher, Genres
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    birth_date = forms.DateField(label='Fecha de nacimiento', widget=forms.DateInput(attrs={'type': 'date'}))
    full_name = forms.CharField(max_length=150, label='Full Name')

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'password1', 'password2', 'birth_date']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.full_name = self.cleaned_data["full_name"]
        user.birth_date = self.cleaned_data["birth_date"]
        if commit:
            user.save()
        return user
    
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