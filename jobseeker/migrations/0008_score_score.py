# Generated by Django 4.2.3 on 2023-10-25 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobseeker', '0007_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
