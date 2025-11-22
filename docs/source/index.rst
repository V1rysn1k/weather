.. Weather app documentation master file, created by
   sphinx-quickstart on Sat Nov 22 13:25:29 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Документация Weather App
========================

Weather App - это приложение для получения данных о погоде 
по названию города или географическим координатам с использованием кэширования.

Основные возможности
--------------------

* **Получение погоды по названию города** - автоматическое определение координат
* **Получение погоды по координатам** - автоматическое определение города
* **Кэширование запросов** в PostgreSQL для уменьшения нагрузки на API
* **Автоматическое определение типа запроса** - город или координаты
* **Поддержка русского языка** для городов и интерфейса

Быстрый старт
-------------

.. code-block:: bash

   # Запуск приложения
   python main.py

   # Примеры использования:
   > Москва
   > 55.7558 37.6173
   > Санкт-Петербург
   > exit

Структура проекта
-----------------

.. code-block:: text

   weather_app/
   ├── api.py          # Модуль для работы с API погоды
   ├── cache.py        # Модуль кэширования в PostgreSQL
   ├── commands.py     # Основные команды приложения
   ├── main.py         # Главный модуль приложения
   └── docs/           # Документация

.. toctree::
   :maxdepth: 2
   :caption: Содержание:
   :hidden:

   modules
   api
   cache
   commands
   main

Индексы и таблицы
=================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`