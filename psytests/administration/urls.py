from django.urls import path
from .views import Home, UnapprovedUsers, UserDetailUpdate, UserManagement, approve_user


app_name='administration'

urlpatterns=[
    path('', Home.as_view(), name='home'),
    path('user-management/', UserManagement.as_view(), name='user-management'),
    path('user-management/<int:pk>/update', UserDetailUpdate.as_view(), name='user-detail-update'),
    path('unapproved-users/', UnapprovedUsers.as_view(), name='unapproved-users'),
    path('approve-user/', approve_user, name='approve-user'),
]