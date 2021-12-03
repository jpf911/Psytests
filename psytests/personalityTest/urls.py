from django.urls import path
from .views import (
    DeleteRecord,
    PersonalityTestHomeView,
    TestView,
    QuestionsListView,
    QuestionsDetailView,
    QuestionsCreateView,
    QuestionsEditView,
    DeleteQuestions,
)


app_name = 'personalityTest'
urlpatterns = [
    path('', PersonalityTestHomeView.as_view(), name='home'),
    path('test/', TestView.as_view(), name='test'),
    path('delete/<username>/<str:pk>/', DeleteRecord.as_view(), name='delete'),
    path('questions/',QuestionsListView.as_view(),name='questions' ),
    path('questions/create/',QuestionsCreateView.as_view(),name='questions_add' ),
    path('questions/<slug:slug>/edit',QuestionsEditView.as_view(),name='questions_edit' ),
    path('questions/<slug:slug>/',QuestionsDetailView.as_view(),name='questions_detail' ),
    path('questions/<slug:slug>/delete', DeleteQuestions.as_view(), name='questions_delete'),
]


