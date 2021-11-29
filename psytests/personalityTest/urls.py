from django.urls import path
from .views import DeleteRecord, PersonalityTestHomeView, TestView


app_name = 'personalityTest'
urlpatterns = [
    path('', PersonalityTestHomeView.as_view(), name='home'),
    path('test/', TestView.as_view(), name='test'),
    path('delete/<username>/<str:pk>/', DeleteRecord.as_view(), name='delete')
]


