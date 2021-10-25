from django.urls import path
from .views import Home
from . import views

app_name='riasec'
urlpatterns = [
    path('test/', views.testPage, name='test'),
    path('home/', Home.as_view(), name='home'),
    path('test/evaluate/', views.evaluate, name='test_evaluate')
]
