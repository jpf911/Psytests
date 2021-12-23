from django.urls import path
from .views import (
    PersonalityTestHomeView,
    ResultView,
    TestView,
)


app_name = 'personalityTest'
urlpatterns = [
    path('', PersonalityTestHomeView.as_view(), name='home'),
    path('test/', TestView.as_view(), name='test'),
    path('result/', ResultView.as_view(), name='result'),
]


