from django.urls import path
from . import views

app_name='accounts'
urlpatterns = [
    path('stats/', views.StatPage.as_view(), name='stats'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser,name='logout'),
]
