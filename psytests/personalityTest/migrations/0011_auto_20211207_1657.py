# Generated by Django 3.2.7 on 2021-12-07 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalityTest', '0010_questionnaire_key'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questionnaire',
            options={'ordering': ('-id',)},
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='key',
            field=models.CharField(blank=True, choices=[('1', 'Positive'), ('0', 'Negative')], max_length=10, null=True),
        ),
    ]
