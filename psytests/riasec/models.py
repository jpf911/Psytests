from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _ #used for changing name in admin

class RIASEC_Test(models.Model):
    class Meta:
        verbose_name = _('RIASEC Test')
        verbose_name_plural = _('RIASEC Tests')

    category_choices =[
        ('R','Reality'),
        ('I','Investigative'),
        ('A','Artistic'),
        ('S','Social'),
        ('E','Enterprising'),
        ('C','Conventional'),
    ]
    question=models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, choices=category_choices)

    def __str__(self):
        return str(self.question)

class Riasec_result (models.Model):
    class Meta:
        verbose_name = _('RIASEC Result')
        verbose_name_plural = _('RIASEC Results')

    user=models.ForeignKey(User, null=True,on_delete=models.CASCADE)
    reality = models.FloatField(default=0)
    investigative = models.FloatField(default=0)
    artistic = models.FloatField(default=0)
    social = models.FloatField(default=0)
    enterprising = models.FloatField (default=0)
    conventional = models.FloatField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    
