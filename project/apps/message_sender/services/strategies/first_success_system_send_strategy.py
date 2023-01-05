from .abstract_send_strategy import AbstractSendStrategy
from ..message_dao.base_message_dao import BaseMessageDAO


class FirstSuccessSystemSendStrategy(AbstractSendStrategy):
    """
    Стратегия отправки данных в первую успешную внешнюю систему.
    """

    def send(self, message_dao: BaseMessageDAO) -> None:
        """
        Отправка сообщения согласно стратегии.

        :param message_dao: Объект для доступа к данным.
        """

        send_reporter = self.get_send_reporter()
        senders = self.get_senders()

        # Пытаемся отправить данные в первый успешный вариант.
        for sender in senders:
            try:
                sender.send(message_dao)
            except Exception as e:
                # В случае ошибки отправки с помощью какого-либо отправителя 
                # добавляем этот отправитель и ошибку отправки в список ошибок.
                send_reporter.add_error(sender, e)
            else:
                send_reporter.add_success_sender(sender)
                break
