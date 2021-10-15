from django.contrib import admin
from .models import Riasec_result,RIASEC_Test
# Register your models here.

class ResultAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'reality', 'investigative', 'artistic', 'social', 'enterprising', 'conventional']
    list_filter = ['user']

admin.site.register(Riasec_result, ResultAdmin)
admin.site.register(RIASEC_Test)