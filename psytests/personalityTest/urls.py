from django.urls import path

import personalityTest

from .views import PersonalityTestHomeView

urlpatterns = [
    path('', PersonalityTestHomeView.as_view(), name='personalityTest-home')
]


