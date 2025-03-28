import time
import logging
from .models import LoliAccount, TaskStatistic
from .tasks import run_loliland_bonus_script
from django.utils import timezone
from datetime import timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def start_task_loop():
    logger.info("Фоновый процесс запущен")
    while True:
        check_and_run_tasks()
        time.sleep(5)  # Пауза между проверками

def check_and_run_tasks():
    logger.info("Проверяем задачи...")
    try:
        accounts_to_collect = LoliAccount.objects.filter(next_run_time__lte=timezone.now())
        if accounts_to_collect.exists():
            logger.info(f"Найдено {accounts_to_collect.count()} аккаунтов для сбора бонусов.")
            for account in accounts_to_collect:
                
                if TaskStatistic.objects.filter(account=account, end_time__isnull=True).exists():
                    logger.info(f"Задача для аккаунта {account.username} уже выполняется, пропускаем.")
                    continue  # Пропускаем аккаунт, если задача уже выполняется
                
                task_statistic = TaskStatistic.objects.create(account=account, start_time=timezone.now()) # Создаем запись статистики перед запуском задачи
                logger.info(f"Запускаем задачу для аккаунта: {account.username}")
                try:
                    run_loliland_bonus_script(account.username, account.password) # Запускаем скрипт
                    account.next_run_time = timezone.now() + timedelta(days=1) # Следующий запуск через 24 часа
                    account.save()
                    task_statistic.end_time = timezone.now() # Обновляем время окончания
                    task_statistic.status = 'SUCCESS' # Устанавливаем статус "успех"
                    task_statistic.save() # Сохраняем статистику
                    logger.info(f"Задача для аккаунта {account.username} успешно выполнена. Следующий запуск: {account.next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")
                except Exception as e:
                    logger.error(f"Ошибка при выполнении задачи для аккаунта {account.username}: {e}") # Логируем ошибки для конкретного аккаунта
                    task_statistic.end_time = timezone.now() # Обновляем время окончания
                    task_statistic.status = 'FAILED' # Устанавливаем статус "ошибка"
                    task_statistic.error_message = str(e) # Записываем сообщение об ошибке
                    task_statistic.save() # Сохраняем статистику
        else:
            logger.info("Нет задач для выполнения на данный момент.")

    except Exception as e:
        logger.error(f"Глобальная ошибка при проверке и запуске задач: {e}") # Логируем глобальные ошибки