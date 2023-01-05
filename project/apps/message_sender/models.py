from django.db import models
from django.utils.translation import gettext_lazy as _


class ModuleInfo(models.Model):
    """Модель для хранения данных о модуле Python"""

    name = models.CharField(
        max_length=120,
        primary_key=True,
        verbose_name=_('Название'),
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Описание'),
    )
    module_path = models.CharField(
        max_length=512,
        unique=True,
        verbose_name=_('Модуль'),
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f'{self._meta.verbose_name}: {self.name}'


class SenderInfo(ModuleInfo):
    """Модель отправщика"""

    class Meta:
        verbose_name = _('Отправщик данных')
        verbose_name_plural = _('Отправщики данных')


class SendStrategyInfo(ModuleInfo):
    """Модель стратегии отправки"""

    class Meta:
        verbose_name = _('Стратегия отправки')
        verbose_name_plural = _('Стратегии отправки')


class DataGateway(models.Model):
    """Модель шлюза данных"""

    name = models.CharField(
        max_length=120,
        unique=True,
        verbose_name=_('Название шлюза'),
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Описание'),
    )
    enabled = models.BooleanField(
        default=True,
        verbose_name=_('Активен'),
    )
    send_strategy = models.ForeignKey(
        to=SendStrategyInfo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='data_gateways',
        related_query_name='data_gateway',
        verbose_name=_('Стратегия отправки'),
    )

    class Meta:
        verbose_name = _('Шлюз данных')
        verbose_name_plural = _('Шлюзы данных')

    def __str__(self) -> str:
        return f'{self._meta.verbose_name}: {self.name}'


class SenderGatewayRelation(models.Model):
    """Модель, привязывающая к шлюзу данных какого-то отправщика"""

    serial_number = models.PositiveSmallIntegerField(
        verbose_name=_('Порядковый номер'),
    )
    enabled = models.BooleanField(
        default=True,
        verbose_name=_('Активен'),
    )    
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Описание'),
    )
    sender = models.ForeignKey(
        to=SenderInfo,
        on_delete=models.SET_NULL,
        null=True,
        related_name='gateway_relations',
        related_query_name='gateway_relation',
        verbose_name=_('Отправщик данных'),
    )
    data_gateway = models.ForeignKey(
        to=DataGateway,
        on_delete=models.CASCADE,
        related_name='sender_relations',
        related_query_name='sender_relation',
        verbose_name=_('Шлюз данных'),
    )

    class Meta:
        verbose_name = _('Связь с отправщиком')
        verbose_name_plural = _('Связи с отправщиками')
        unique_together = ('serial_number', 'data_gateway')
        ordering = ('serial_number', )

    def __str__(self) -> str:
        return f'{self.data_gateway.name}#{self.sender}'
