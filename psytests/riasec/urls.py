from django.urls import path,include
from . import views

app_name='riasec'
urlpatterns = [
    path('test/', views.testPage, name='test'),
]
