from django.urls import path
from .views import (
    StatPage,
    registerPage,
    loginPage,
    logoutUser,
)

app_name='accounts'
urlpatterns = [
    path('stats/', StatPage.as_view(), name='stats'),
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/',logoutUser,name='logout'),
]
