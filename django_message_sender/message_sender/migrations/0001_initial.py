# Generated by Django 4.1.4 on 2023-01-13 13:01

import apps.message_sender.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SenderModule',
            fields=[
                ('name', models.CharField(max_length=120, primary_key=True, serialize=False, verbose_name='Название')),
                ('description', models.TextField(default='', verbose_name='Описание')),
                ('module_path', models.CharField(max_length=512, unique=True, verbose_name='Модуль')),
            ],
            options={
                'verbose_name': 'Отправщик данных',
                'verbose_name_plural': 'Отправщики данных',
            },
        ),
        migrations.CreateModel(
            name='StrategyModule',
            fields=[
                ('name', models.CharField(max_length=120, primary_key=True, serialize=False, verbose_name='Название')),
                ('description', models.TextField(default='', verbose_name='Описание')),
                ('module_path', models.CharField(max_length=512, unique=True, verbose_name='Модуль')),
            ],
            options={
                'verbose_name': 'Стратегия отправки',
                'verbose_name_plural': 'Стратегии отправки',
            },
        ),
        migrations.CreateModel(
            name='StrategyConfig',
            fields=[
                ('name', models.CharField(max_length=120, primary_key=True, serialize=False, verbose_name='Название')),
                ('description', models.TextField(default='', verbose_name='Описание')),
                ('init_params', models.JSONField(default=apps.message_sender.models.module_config_params_default, verbose_name='Параметры')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='strategy_configs', related_query_name='strategy_config', to='message_sender.strategymodule', verbose_name='Стратегия отправки')),
            ],
            options={
                'verbose_name': 'Конфигурация стратегии отправки',
                'verbose_name_plural': 'Конфигурации стратегий отправки',
            },
        ),
        migrations.CreateModel(
            name='SenderConfig',
            fields=[
                ('name', models.CharField(max_length=120, primary_key=True, serialize=False, verbose_name='Название')),
                ('description', models.TextField(default='', verbose_name='Описание')),
                ('init_params', models.JSONField(default=apps.message_sender.models.module_config_params_default, verbose_name='Параметры')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_configs', related_query_name='sender_config', to='message_sender.sendermodule', verbose_name='Отправщик')),
            ],
            options={
                'verbose_name': 'Конфигурация отправщика',
                'verbose_name_plural': 'Конфигурации отправщиков',
            },
        ),
        migrations.CreateModel(
            name='DataGateway',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True, verbose_name='Название шлюза')),
                ('description', models.TextField(default='', verbose_name='Описание')),
                ('send_strategy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='data_gateways', related_query_name='data_gateway', to='message_sender.strategyconfig', verbose_name='Стратегия отправки')),
            ],
            options={
                'verbose_name': 'Шлюз данных',
                'verbose_name_plural': 'Шлюзы данных',
            },
        ),
        migrations.CreateModel(
            name='StrategySenderRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.PositiveSmallIntegerField(verbose_name='Порядковый номер')),
                ('enabled', models.BooleanField(default=True, verbose_name='Активен')),
                ('parent_send_strategy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='senders', related_query_name='sender', to='message_sender.strategyconfig', verbose_name='Родителькая стратегия отправки')),
                ('send_strategy_config', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='strategy_relations', related_query_name='strategy_relation', to='message_sender.strategyconfig', verbose_name='Стратегия отправки данных')),
                ('sender_config', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender_relations', related_query_name='sender_relation', to='message_sender.senderconfig', verbose_name='Отправщик данных')),
            ],
            options={
                'verbose_name': 'Связь с отправщиком',
                'verbose_name_plural': 'Связи с отправщиками',
                'ordering': ('serial_number',),
                'unique_together': {('serial_number', 'parent_send_strategy')},
            },
        ),
    ]