from django.contrib import admin
from .models import LoliAccount, TaskStatistic # Импортируем модели

admin.site.register(LoliAccount) # Регистрируем модель LoliAccount
admin.site.register(TaskStatistic) # Регистрируем модель TaskStatistic