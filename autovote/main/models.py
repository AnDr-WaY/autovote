from django.db import models
from django.utils import timezone

class LoliAccount(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    next_run_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.username} - run at {self.next_run_time.strftime('%Y-%m-%d %H:%M:%S')}"


class TaskStatistic(models.Model):
    STATUS_CHOICES = [
        ('SUCCESS', 'Успех'),
        ('FAILED', 'Ошибка'),
        ('PENDING', 'Ожидание'),
    ]

    account = models.ForeignKey(LoliAccount, on_delete=models.CASCADE, default=1)
    task_name = models.CharField(max_length=255, default='Сбор ежедневного бонуса Loliland') #  Более конкретное имя задачи
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True) #  Может быть пустым, если задача не завершилась
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    error_message = models.TextField(blank=True, null=True) #  Для хранения сообщений об ошибках

    def __str__(self):
        return f"Задача '{self.task_name}' для {self.account.username} - {self.status} - {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}"