# Generated by Django 3.1.1 on 2020-09-24 17:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classrooms', '0009_auto_20200924_1912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='name',
        ),
        migrations.AddField(
            model_name='teacher',
            name='teacher',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
