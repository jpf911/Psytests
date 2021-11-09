from django.urls import path
from .views import DeleteRecord, Home
from . import views

app_name='riasec'
urlpatterns = [
    path('test/', views.testPage, name='test'),
    path('home/', Home.as_view(), name='home'),
    path('test/evaluate/', views.evaluate, name='test_evaluate'),
    path('delete/<username>/<str:pk>', DeleteRecord.as_view(), name='delete_record')
]
