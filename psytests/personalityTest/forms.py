from django import forms
from .models import Questionnaire
from riasec.models import RIASEC_Test


class AddRQuestionsForm(forms.ModelForm):

    class Meta:
        model = RIASEC_Test
        fields=('question','category')

        category_choices = [
            ('R', 'Realistic'),
            ('I', 'Investigative'),
            ('A', 'Artistic'),
            ('S', 'Social'),
            ('E', 'Enterprising'),
            ('C', 'Conventional'),
        ]
        widgets={
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'},choices=category_choices),
        }


class AddPQuestionsForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ('question', 'category')

        category_choices = [
            ('EXT', 'Extroversion'),
            ('EST', 'Neurotic'),
            ('AGR', 'Agreeable'),
            ('CSN', 'Conscientious'),
            ('OPN', 'Openness'),
        ]

        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}, choices=category_choices),
        }
