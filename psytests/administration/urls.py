from django.urls import path
from .views import HistorySchedules, Home, MissedSchedules, ResetSchedule, UpcomingSchedules, UserDetailUpdate, UserManagement, UserResults, UserSchedules, approve_user


app_name='administration'

urlpatterns=[
    path('', Home.as_view(), name='home'),
    path('user-management/', UserManagement.as_view(), name='user-management'),
    path('user-management/<int:pk>/update', UserDetailUpdate.as_view(), name='user-detail-update'),
    path('user-results/', UserResults.as_view(), name='user-results'),
    path('schedules/', UserSchedules.as_view(), name='schedules'),
    path('schedules/missed/', MissedSchedules.as_view(), name='missed-schedules'),
    path('schedules/upcoming/', UpcomingSchedules.as_view(), name='upcoming-schedules'),
    path('schedules/history/', HistorySchedules.as_view(), name='history-schedules'),
    path('schedules/<int:pk>/reset-schedule/', ResetSchedule.as_view(), name='reset-schedule'),
    path('approve-user/', approve_user, name='approve-user'),
]