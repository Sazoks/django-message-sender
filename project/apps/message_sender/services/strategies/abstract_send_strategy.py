from abc import (
    ABC,
    abstractmethod,
)

from ..interfaces import (
    ISendable,
    IModuleInformative,
)
from ..message_dao.base_message_dao import BaseMessageDAO
from ..reporters.base_send_reporter import BaseSendReporter
from ..reporters.default_send_reporter import DefaultSendReporter


class AbstractSendStrategy(ISendable, IModuleInformative, ABC):
    """
    Класс абстрактной стратегии отправки сообщения.
    """

    default_send_reporter_class = DefaultSendReporter

    def __init__(
        self, 
        senders: list[ISendable],
        send_reporter: BaseSendReporter | None = None,
    ) -> None:
        """
        Инициализатор класса.

        :param senders: Список отправителей данных.
        """

        self.__senders = senders
        self.__send_reporter = send_reporter or self.default_send_reporter_class()

    def get_senders(self) -> list[ISendable]:
        """Получение списка объектов отправителей"""

        return self.__senders

    def get_send_reporter(self) -> BaseSendReporter:
        """Получение объекта репортера об ошибках"""

        return self.__send_reporter

    @abstractmethod
    def send(self, message_dao: BaseMessageDAO) -> None:
        """
        Отправка сообщения согласно стратегии.

        :param message_dao: Объект для доступа к данным.
        """
        raise NotImplementedError()
