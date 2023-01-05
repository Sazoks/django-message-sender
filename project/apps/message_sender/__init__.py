from .services import senders
from .services import registry
from .services import strategies


# Регистрация встроенных отправщиков и стратегий.
sender_registry = registry.SenderRegistry()
sender_registry.register(senders.EmailSender)
sender_registry.register(senders.TelegramSender)


# Регистрация встроенных стратегий отправки.
strategy_registry = registry.StrategyRegistry()
strategy_registry.register(strategies.AllSystemsSendStrategy)
strategy_registry.register(strategies.FirstSuccessSystemSendStrategy)
