from django.apps import AppConfig

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    verbose_name = "Головний застосунок"

    def ready(self):
        import main.signals  # Подключаем сигналы
