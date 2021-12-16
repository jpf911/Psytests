from django import forms
<<<<<<< HEAD
<<<<<<< HEAD
from personalityTest.models import Questionnaire
from riasec.models import RIASEC_Test
from django.forms.widgets import SelectDateWidget
=======
>>>>>>> 86974052695f3dd791fa26a8d9dad54eeb78fb5b
=======
from personalityTest.models import Questionnaire
from riasec.models import RIASEC_Test
>>>>>>> cb0fb85cc6070eebef8de542ec403e8f4b9fbbeb

from administration.models import AdminScheduledConsultation


class SearchForm(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search username',
    }))


class AddRQuestionsForm(forms.ModelForm):
    class Meta:
        model = RIASEC_Test
        fields = ('question', 'category')

        category_choices = [
            ('R', 'Realistic'),
            ('I', 'Investigative'),
            ('A', 'Artistic'),
            ('S', 'Social'),
            ('E', 'Enterprising'),
            ('C', 'Conventional'),
        ]
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}, choices=category_choices),
        }


class AddPQuestionsForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ('question', 'category', 'key')

        category_choices = [
            ('EXT', 'Extroversion'),
            ('EST', 'Neurotic'),
            ('AGR', 'Agreeable'),
            ('CSN', 'Conscientious'),
            ('OPN', 'Openness'),
        ]

        key_choices = [
            ('1', 'Positive'),
            ('0', 'Negative')
        ]

        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}, choices=category_choices),
            'key': forms.Select(attrs={'class': 'form-control'}, choices=key_choices),
        }


class ScheduleDateForm(forms.ModelForm):
    scheduled_date = forms.DateTimeField(required=True, widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local',
        'class': 'form-control'
    }))

    class Meta:
        model = AdminScheduledConsultation
        fields = ['scheduled_date']
