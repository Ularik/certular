from django.apps import AppConfig


class MessagesAppsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messages_app'
    verbose_name = 'Приложение "Сообщения"'

    def ready(self):
        import messages_app.signals  # Импортируем файл с сигналами