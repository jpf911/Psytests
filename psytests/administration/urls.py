from django.urls import path

from .views import (
    Home,
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
    HistorySchedules,
    MissedSchedules,
    ResetSchedule,
    UpcomingSchedules,
    UserDetailUpdate,
    UserManagement,
    UserResults,
    UserSchedules,
    approve_user
)


app_name='administration'

urlpatterns=[
    path('', Home.as_view(), name='home'),
    path('user-management/', UserManagement.as_view(), name='user-management'),
    path('user-management/<int:pk>/update', UserDetailUpdate.as_view(), name='user-detail-update'),
    path('user-results/', UserResults.as_view(), name='user-results'),
    path('user-results/<user>/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('schedules/', UserSchedules.as_view(), name='schedules'),
    path('schedules/missed/', MissedSchedules.as_view(), name='missed-schedules'),
    path('schedules/upcoming/', UpcomingSchedules.as_view(), name='upcoming-schedules'),
    path('schedules/history/', HistorySchedules.as_view(), name='history-schedules'),
    path('schedules/<int:pk>/reset-schedule/', ResetSchedule.as_view(), name='reset-schedule'),
    path('approve-user/', approve_user, name='approve-user'),
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