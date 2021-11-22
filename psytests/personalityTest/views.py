from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class PersonalityTestHomeView(TemplateView):
    template_name = 'personalityTest/home.html'