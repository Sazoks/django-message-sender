from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models


class SenderGatewayRelationInline(admin.StackedInline):
    """Встроенная модель для админки связи шлюза данных и отправщиков"""

    model = models.SenderGatewayRelation
    extra = 0


# TODO: Запретить добавление и удаление из админки.
@admin.register(models.DataGateway)
class DataGatewayAdmin(admin.ModelAdmin):
    """Администрирование шлюзов данных"""

    list_display = ('name', 'enabled')
    list_display_links = ('name', )
    inlines = (
        SenderGatewayRelationInline,
    )


# TODO: Запретить добавление, удаление и редактирование из админки.
@admin.register(models.SenderInfo)
class SenderInfoAdmin(admin.ModelAdmin):
    """Администрирование отправщиков данных"""

    list_display = ('name', )
    list_display_links = ('name', )


# TODO: Запретить добавление, удаление и редактирование из админки.
@admin.register(models.SendStrategyInfo)
class SendStrategyInfoAdmin(admin.ModelAdmin):
    """Администрирование стратегий отправки"""

    list_display = ('name', )
    list_display_links = ('name', )
