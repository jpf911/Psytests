from django import forms

from administration.models import AdminScheduledConsultation


class SearchForm(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search the username of the user',
    }))

class ScheduleDateForm(forms.ModelForm):

    scheduled_date = forms.DateTimeField(required=True, widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local',
        'class': 'form-control'
    })) 

    class Meta:
        model = AdminScheduledConsultation
        fields = ['scheduled_date']