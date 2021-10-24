from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db.models.fields import TextField
from django.forms.fields import ChoiceField
from django.forms.widgets import Select, SelectDateWidget, TextInput

class CreateUserForm(UserCreationForm):
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        )
    
    date_of_birth = forms.DateField(widget=SelectDateWidget(attrs={
        'type': 'date'
    }))
    gender = forms.CharField(widget=Select(choices=gender_choices))
    class Meta:
        model=User
        fields = ['first_name', 'last_name','gender','date_of_birth','username','email','password1','password2']
