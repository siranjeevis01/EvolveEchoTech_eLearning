# Generated by Django 5.1.2 on 2024-10-21 18:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_enrollment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='myapp.course'),
        ),
    ]
