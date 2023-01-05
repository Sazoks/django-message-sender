from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MessageSenderConfig(AppConfig):
    """Конфигурация приложения"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.message_sender'
    verbose_name = _('Отправщик сообщений во внешние системы')

    def ready(self) -> None:
        """Метод срабатывает при полной инициализации приложения"""
        
        from . import (
            sender_registry,
            strategy_registry,
        )
        from .models import (
            SenderInfo,
            SendStrategyInfo,
        )
        from .services.core import (
            ModuleSynchronizer,
            DataGatewaysDBInitializer,
        )

        # Синхронизируем информацию о зарегистрированных отправщиках и стратегиях в БД,
        module_synchronizer = ModuleSynchronizer()
        module_synchronizer.synchronize(SenderInfo, sender_registry.get_sender_classes())
        module_synchronizer.synchronize(SendStrategyInfo, strategy_registry.get_strategy_classes())

        # Создаем дефолтные шлюзы данных из настроек.
        DataGatewaysDBInitializer().init()
