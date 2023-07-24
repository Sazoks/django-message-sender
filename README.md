# django-message-sender
Проект представляет собой батарейку для Django, которая дает возможность динамически из админ. панели Django настраивать шлюзы данных для отправки сообщений во внешние сервисы.

## Суть проекта
Идея проекта пришла разработчику спонтанно, т.к. на одном из мест работ часто были кейсы, когда нужно было разрабатывать сервисы для отправки сообщений в сторонние сервис по типу Битрикс24, amoCRM, Telegram, email и другие.
Разработчик данного проекта решил зайти немного дальше и добавить возможность конфигурирования логики отправки сообщений из админ. панели Django. При этом можно выстраивать бесконечные древовидные структуры из отправщиков. 
Конечно, на практике, такая логика почти что бесполезна, т.к. трудно представить кейс, где, к примеру, сначала нужно отправить данные в telegram, затем в email, а затем в один из сервисов: amoCRM и Битрикс24, например.

## Схема работы
Ниже представлен пример схемы работы данной батарейки.

![django-message-sender jpg](https://github.com/Sazoks/django-message-sender/assets/46415966/93315c9a-1a56-4378-b875-f271bb4d56e9)

Это и есть конфигурация отправки. Все, что требуется от разработчика, зарегистрировать свои классы отправщиков и стратегий в специальных реестрах, информация о которых затем при запуске проекта будет сохранена в БД.

Такие конфигурации можно радеактировать как угодно прямо из админки.

## Шлюзы данных
Шлюз данных - это класс, который привязан к конкретной конфигурации отправки. Когда разработчик зарегестировал свои отправщики и стратегии и настроил конфигурацию в админке, он привязывает ее к шлюзу данных, который затем в 
нужном месте может загружать из БД со всей конфигурацией и отправлять данные по заранее заготовленной схеме.

Также можно заранее настраивать конфигурации отправки в настройках проекта. Пример ниже.
```python
MESSAGE_SENDER = {
    'INIT_FILE_NAME': 'message_sender',
    'SENDER_CONFIGS': (
        {
            'name': 'KanalservisTelegramGroupsSender_config_1',
            'description': 'Какое-то описание конфигурации',
            'sender_name': 'KanalservisTelegramGroupsSender',
            'params': {
                'bot_token': TELEGRAM_BOT_TOKEN,
                'main_group_id': TELEGRAM_GROUP_ID,
                'duty_group_id': TELEGRAM_DUTY_ID,
                'duty_start_time': '22:00:00',
                'duty_end_time': '07:00:00',
            },
        },
    ),
    'STRATEGY_CONFIGS': (
        {
            'name': 'AllSystemsSendStrategy_config_1',
            'strategy_name': 'AllSystemsSendStrategy',
            'senders': (
                {
                    'serial_number': 1,
                    'enabled': True,
                    'sender_config': 'KanalservisTelegramGroupsSender_config_1',
                },
            ),
        },
    ),
    'DATA_GATEWAYS': (
        {
            'name': 'Telegram Groups',
            'description': 'Шлюз отправки данных в телеграм-группы в зависимости от времени.',
            'strategy_config': 'AllSystemsSendStrategy_config_1',
        },
    ),
}
```

Пример использования шлюза данных.
```python
@shared_task
def send_data(data: dict[str, Any]) -> None:
    data_gateway = DataGateway.objects.get(pk='data_gateway_name')
    message_builder = DefaultMessageBuilder(
        subject_template='app/subject_template.txt',
        body_template='app/body_template.txt',
    )
    sender = data_gateway.get_sender(message_builder)

    message = DefaultMessageDAO(
        data={
            'message_data': {
                'data_1': 'some_data_1',
                ...,
            },
            'other_data': ...,
        },
        body_data_key='message_data',
    )
    sender.send(message)
```

## Вместо послесловия
Проект разрабатывался на голом энтузиазме 4 дня. Вскоре, после начала проекта, разработчик понял, что практического смысла это не имело, но задумка получилась интересной :)
В проекте очень много кода за запашком, который следовало бы отрефакторить, однако, как я уже сказал, практического смысла проект не имеет, поэтому разработчик его забросил.
