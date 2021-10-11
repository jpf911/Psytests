from django.db import models
from django.contrib.auth.models import User

class RIASEC_Test(models.Model):
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
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    reality = models.IntegerField()
    investigative = models.IntegerField()
    artistic = models.IntegerField()
    social = models.IntegerField()
    enterprising = models.IntegerField ()
    conventional = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

