from django.contrib import admin
from .models import Questionnaire, Result,Cluster

# Register your models here.
admin.site.register(Questionnaire)
admin.site.register(Result)
admin.site.register(Cluster)