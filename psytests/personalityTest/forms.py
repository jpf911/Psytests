from django import forms
from .models import Questionnaire

class AddQuestionsForm(forms.ModelForm):

    class Meta:
        model = Questionnaire
        fields=('question','category')

        category_choices = [
            ('EXT', 'Extroversion'),
            ('EST', 'Neurotic'),
            ('AGR', 'Agreeable'),
            ('CSN', 'Conscientious'),
            ('OPN', 'Openness'),
        ]

        widgets={
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'},choices=category_choices),
        }