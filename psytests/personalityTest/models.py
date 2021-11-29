from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Questionnaire(models.Model):

    category_choices =[
        ('EXT','Extroversion'),
        ('EST','Neurotic'),
        ('AGR','Agreeable'),
        ('CSN','Conscientious'),
        ('OPN','Openness'),
    ]
    question=models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, choices=category_choices)

    def __str__(self):
        return str(self.question)

class Result(models.Model):
    user=models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    extroversion = models.FloatField(default=0)
    neurotic = models.FloatField(default=0)
    agreeable = models.FloatField(default=0)
    conscientious = models.FloatField(default=0)
    openness = models.FloatField (default=0)
    prediction = models.IntegerField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

class Cluster(models.Model):
    cluster = models.CharField(max_length=10)
    extroversion = models.FloatField(default=0)
    neurotic = models.FloatField(default=0)
    agreeable = models.FloatField(default=0)
    conscientious = models.FloatField(default=0)
    openness = models.FloatField (default=0)

    def __str__(self):
        return self.cluster