from abc import (
    ABC,
    abstractmethod,
)

from ..message_dao.base_message_dao import BaseMessageDAO


class ISendable(ABC):
    """
    Интерфейс отправляемого объекта.
    """

    @abstractmethod
    def send(self, message_dao: BaseMessageDAO) -> None:
        raise NotImplementedError()
