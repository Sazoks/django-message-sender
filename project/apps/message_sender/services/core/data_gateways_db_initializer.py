from typing import (
    Any,
    Type,
    Iterable,
)
from django.conf import settings

from ...models import (
    DataGateway,
    SenderGatewayRelation,
)
from ..senders import AbstractSender
from ..module_import import lazy_class_import
from ..strategies import AbstractSendStrategy


class DataGatewaysDBInitializer:
    """
    Класс для инициализации шлюзов данных в БД в Django-проекте.

    Берет из настроек Django-проекта информацию о шлюзах данных и 
    инициализирует их в БД.
    """

    def init(self) -> None:
        """Синхронизация конфигурации шлюзов данных с БД"""

        # Создаем в БД шлюзы данных, которых еще нет.
        data_gateways_configs = self.__get_gateways_configs()
        for data_gateway_config in data_gateways_configs:
            # Если в БД существует конфигурация для указанного шлюза, пропускаем текущую конфигруацию.
            if DataGateway.objects.filter(name=data_gateway_config['name']).exists():
                continue

            # Прикрепляем к шлюзу данных стратегию.
            send_strategy: Type[AbstractSendStrategy] = lazy_class_import(data_gateway_config['strategy'])
            data_gateway = DataGateway.objects.create(
                name=data_gateway_config['name'],
                description=data_gateway_config['description'],
                enabled=data_gateway_config['enabled'],
                send_strategy_id=send_strategy.get_name(),
            )

            # Связываем шлюз данных с отправщиками.
            related_senders: list[SenderGatewayRelation] = []
            for i, sender_module_path in enumerate(data_gateway_config['senders']):
                sender: Type[AbstractSender] = lazy_class_import(sender_module_path)
                related_senders.append(
                    SenderGatewayRelation(
                        serial_number=i,
                        sender_id=sender.get_name(),
                        data_gateway=data_gateway,
                    )
                )
            SenderGatewayRelation.objects.bulk_create(related_senders)

    def __get_gateways_configs(self) -> Iterable[dict[str, Any]]:
        """Получение списка конфигураций шлюзов данных"""

        if (
            hasattr(settings, 'MESSAGE_SENDER') and 
            settings.MESSAGE_SENDER.get('DATA_GATEWAYS') is not None
        ):
            return settings.MESSAGE_SENDER['DATA_GATEWAYS']
        else:
            return []
