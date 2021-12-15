from django.urls import path
from .views import (
    Home,
    UnapprovedUsers,
    UserDetailUpdate,
    UserManagement,
    approve_user,
    UsersResults,
    UserDetailView,
    RQuestionsTemplateView,
    PQuestionsTemplateView,
    RQuestionsDetailView,
    PQuestionsDetailView,
    RQuestionsCreateView,
    PQuestionsCreateView,
    RQuestionsEditView,
    PQuestionsEditView,
    RDeleteQuestions,
    PDeleteQuestions,
)


app_name='administration'

urlpatterns=[
    path('', Home.as_view(), name='home'),
    path('user-management/', UserManagement.as_view(), name='user-management'),
    path('user-management/<int:pk>/update', UserDetailUpdate.as_view(), name='user-detail-update'),
    path('unapproved-users/', UnapprovedUsers.as_view(), name='unapproved-users'),
    path('approve-user/', approve_user, name='approve-user'),
    path('results/', UsersResults.as_view(), name='results'),
    path('results/<user>/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('rquestions/', RQuestionsTemplateView.as_view(), name='rquestions'),
    path('pquestions/', PQuestionsTemplateView.as_view(), name='pquestions'),
    path('rquestions/create/riasec/', RQuestionsCreateView.as_view(), name='rquestions_add'),
    path('pquestions/create/personality/', PQuestionsCreateView.as_view(), name='pquestions_add'),
    path('rquestions/<slug:slug>/riasec/edit', RQuestionsEditView.as_view(), name='rquestions_edit'),
    path('pquestions/<slug:slug>/personality/edit', PQuestionsEditView.as_view(), name='pquestions_edit'),
    path('rquestions/<slug:slug>/riasec/', RQuestionsDetailView.as_view(), name='rquestions_detail'),
    path('pquestions/<slug:slug>/personality/', PQuestionsDetailView.as_view(), name='pquestions_detail'),
    path('rquestions/<slug:slug>/riasec/delete', RDeleteQuestions.as_view(), name='rquestions_delete'),
    path('pquestions/<slug:slug>/personality/delete', PDeleteQuestions.as_view(), name='pquestions_delete'),
]