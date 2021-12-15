from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import Select, SelectDateWidget

from datetime import datetime

now = datetime.today()

class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['email'].label = 'Email Address'
        self.fields['username'].label = 'Username'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['gender'].label = 'Gender'
        self.fields['date_of_birth'].label = 'Date of Birth'

    gender_choices = (
            ('M', 'Male'),
            ('F', 'Female'),
        )
    
    date_of_birth = forms.DateField(widget=SelectDateWidget(years=range(1950,now.year),attrs={
        'type': 'date',
        'class': 'form-select'
    }))
    gender = forms.CharField(widget=Select(choices=gender_choices, attrs={
        'class': 'form-select'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your first name',
        'autofocus': ''
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your last name'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your username'
    }))    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your email address'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Re-enter password'
    }))
    is_superuser = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={
        'placeholder': 'is_superuser'
    }))

    class Meta:
        model=User
        fields = ['first_name', 'last_name','gender','date_of_birth','username','email','password1','password2', 'is_superuser']

class UpdateUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Email Address'
        self.fields['username'].label = 'Username'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'

    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your first name',
    }))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your last name'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your username'
    }))    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type your email address'
    }))
    is_superuser = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'placeholder': 'is_superuser',
        'class': 'form-check-input',
    }))


    class Meta:
        model=User
        fields = ['first_name', 'last_name','username','email','is_superuser']
