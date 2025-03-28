# Generated by Django 5.1.7 on 2025-03-28 12:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskstatistic',
            old_name='execution_time',
            new_name='start_time',
        ),
        migrations.AddField(
            model_name='taskstatistic',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.loliaccount'),
        ),
        migrations.AddField(
            model_name='taskstatistic',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='taskstatistic',
            name='error_message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='taskstatistic',
            name='status',
            field=models.CharField(choices=[('SUCCESS', 'Успех'), ('FAILED', 'Ошибка'), ('PENDING', 'Ожидание')], default='PENDING', max_length=20),
        ),
        migrations.AlterField(
            model_name='taskstatistic',
            name='task_name',
            field=models.CharField(default='Сбор ежедневного бонуса Loliland', max_length=255),
        ),
    ]
