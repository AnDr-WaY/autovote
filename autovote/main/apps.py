from django.apps import AppConfig
import threading
import os

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'


    def ready(self):
        if "runserver" in os.environ.get("DJANGO_COMMAND", ""):
            from .task_manager import start_task_loop
            thread = threading.Thread(target=start_task_loop, daemon=True)
            thread.start()