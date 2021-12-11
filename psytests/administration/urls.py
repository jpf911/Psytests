from django.urls import path
from .views import Home
from . import views

app_name='administration'

urlpatterns=[
    path('',Home.as_view(),name='home'),
]