# Generated by Django 4.2.3 on 2023-10-15 20:37

from django.db import migrations, models
import employer.utility


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='deadline',
            field=models.DateField(default=employer.utility.default_deadline),
        ),
    ]
