from django.urls import path
from .views import (
    StatPage,
    UsersResults,
    UserDetailView,
    registerPage,
    loginPage,
    logoutUser,
)

app_name='accounts'
urlpatterns = [
    path('stats/', StatPage.as_view(), name='stats'),
    path('results/', UsersResults.as_view(), name='results'),
    path('results/<user>/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/',logoutUser,name='logout'),
]
