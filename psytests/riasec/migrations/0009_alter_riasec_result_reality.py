# Generated by Django 3.2.7 on 2021-10-25 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riasec', '0008_alter_riasec_result_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riasec_result',
            name='reality',
            field=models.FloatField(null=True),
        ),
    ]