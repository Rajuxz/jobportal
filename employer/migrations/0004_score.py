# Generated by Django 4.2.3 on 2023-10-25 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0003_questions_correct_answer_questions_option_four_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
