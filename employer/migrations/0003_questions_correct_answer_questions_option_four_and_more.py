# Generated by Django 4.2.3 on 2023-10-16 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0002_alter_job_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='correct_answer',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='option_four',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='questions',
            name='option_one',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='option_three',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='questions',
            name='option_two',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='Answers',
        ),
    ]
