# Generated by Django 3.2.7 on 2021-12-12 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalityTest', '0012_alter_questionnaire_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]