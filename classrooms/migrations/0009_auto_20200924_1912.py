# Generated by Django 3.1.1 on 2020-09-24 17:12

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classrooms', '0008_auto_20200923_1956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='email',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='phone',
        ),
        migrations.AlterField(
            model_name='classroom',
            name='classroom_opens',
            field=models.DateField(default=datetime.date(2020, 9, 24), verbose_name='When do you want the classroom to become available to students?'),
        ),
        migrations.RemoveField(
            model_name='classroom',
            name='teacher',
        ),
        migrations.AddField(
            model_name='classroom',
            name='teacher',
            field=models.ManyToManyField(to='classrooms.Teacher'),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_name',
            field=models.CharField(default='some company', max_length=200, unique=True),
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='name',
        ),
        migrations.AddField(
            model_name='teacher',
            name='name',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
