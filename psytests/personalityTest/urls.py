from django.urls import path
from .views import (
    DeleteRecord,
    PersonalityTestHomeView,
    TestView,
    QuestionsListView,
    RQuestionsDetailView,
    RQuestionsCreateView,
    RQuestionsEditView,
    RDeleteQuestions,
    PQuestionsDetailView,
    PQuestionsCreateView,
    PQuestionsEditView,
    PDeleteQuestions,
)


app_name = 'personalityTest'
urlpatterns = [
    path('', PersonalityTestHomeView.as_view(), name='home'),
    path('test/', TestView.as_view(), name='test'),
    path('delete/<username>/<str:pk>/', DeleteRecord.as_view(), name='delete'),
    path('questions/',QuestionsListView.as_view(),name='questions' ),
    path('questions/create/riasec/', RQuestionsCreateView.as_view(), name='rquestions_add'),
    path('questions/create/personality/', PQuestionsCreateView.as_view(), name='pquestions_add'),
    path('questions/<slug:slug>/riasec/edit', RQuestionsEditView.as_view(), name='rquestions_edit'),
    path('questions/<slug:slug>/personality/edit', PQuestionsEditView.as_view(), name='pquestions_edit'),
    path('questions/<slug:slug>/riasec/', RQuestionsDetailView.as_view(), name='rquestions_detail'),
    path('questions/<slug:slug>/personality/', PQuestionsDetailView.as_view(), name='pquestions_detail'),
    path('questions/<slug:slug>/riasec/delete', RDeleteQuestions.as_view(), name='rquestions_delete'),
    path('questions/<slug:slug>/personality/delete', PDeleteQuestions.as_view(), name='pquestions_delete'),
]


