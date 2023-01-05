from ..senders.abstract_sender import AbstractSender


class BaseSendReporter:
    """
    Базовый класс для генерации отчета о работе 
    отправителей сообщений.
    """

    def __init__(self) -> None:
        """Инициализатор класса"""

        self.__errors: list[tuple[AbstractSender, Exception]] = []
        self.__success_senders: list[AbstractSender] = []

    def add_error(self, sender: AbstractSender, error: Exception) -> None:
        """
        Добавление ошибки отправителя в отчет.

        :param sender: Объект отправителя.
        :param error: Ошибка, которая возникла во время отправки.
        """
        
        self.__errors.append((sender, error))

    def get_errors(self) -> list[tuple[AbstractSender, Exception]]:
        """Получение списка ошибок"""
        
        return self.__errors

    def add_success_sender(self, sender: AbstractSender) -> None:
        """
        Добавление отправителя в список успешных.

        :param sender: Объект отправителя.
        """

        self.__success_senders.append(sender)
    
    def get_success_senders(self) -> list[AbstractSender]:
        """Получение списка успешно отработанных отправителей"""

        return self.__success_senders

    def clear(self) -> None:
        """Очистка отчета"""
        
        self.__errors.clear()
        self.__success_senders.clear()
