Модуль cache
============

.. automodule:: cache
   :members:
   :undoc-members:
   :show-inheritance:
   :caption: Содержание:

Конфигурация базы данных
------------------------

.. py:data:: cache.DB_PARAMS

   Параметры подключения к PostgreSQL:
   
   .. code-block:: python
   
      DB_PARAMS = {
          'dbname': 'weather',
          'user': 'postgres', 
          'password': '1234',
          'host': 'localhost',
          'port': 5432,
      }

.. py:data:: cache.TABLE_NAME

   Имя таблицы для кэширования: ``weather_cache``

Функции модуля
--------------

.. autofunction:: cache.get_connection

   Создает и возвращает соединение с базой данных PostgreSQL.
   
   **Возвращает:**
   
   * psycopg2.connection - Объект соединения с БД

.. autofunction:: cache.get_cached_weather

   Ищет закэшированные данные о погоде в базе данных.
   
   **Аргументы:**
   
   * **request_type** (str) - Тип запроса: ``'city'`` или ``'coords'``
   * **city** (str) - Название города
   * **latitude** (float) - Географическая широта
   * **longitude** (float) - Географическая долгота
   
   **Возвращает:**
   
   * dict or None - Словарь с температурой и временем запроса или None
   
   **Структура возвращаемых данных:**
   
   .. code-block:: python
   
      {
          'temperature': 15.5,
          'requested_at': datetime(2024, 1, 15, 10, 30, 0)
      }

.. autofunction:: cache.set_cached_weather

   Сохраняет данные о погоде в кэш базы данных.
   
   **Аргументы:**
   
   * **request_type** (str) - Тип запроса: ``'city'`` или ``'coords'``
   * **city** (str) - Название города
   * **latitude** (float) - Географическая широта
   * **longitude** (float) - Географическая долгота
   * **temperature** (float) - Температура для сохранения

Пример использования
--------------------

.. code-block:: python

   from cache import get_cached_weather, set_cached_weather
   
   # Проверка наличия закэшированных данных
   cached_data = get_cached_weather("city", "Москва", 55.7558, 37.6173)
   
   if cached_data:
       print(f"Температура из кэша: {cached_data['temperature']}°C")
       print(f"Запрос был сделан: {cached_data['requested_at']}")
   else:
       # Если данных нет в кэше, получаем их и сохраняем
       temperature = 25.5  # Получено из API
       set_cached_weather("city", "Москва", 55.7558, 37.6173, temperature)
       print("Данные сохранены в кэш")

Настройка базы данных
---------------------

Перед использованием создайте базу данных и таблицу:

.. code-block:: sql

   -- Создание базы данных
   CREATE DATABASE weather;
   
   -- Создание таблицы для кэша
   CREATE TABLE weather_cache (
       id SERIAL PRIMARY KEY,
       request_type VARCHAR(10) NOT NULL,
       city VARCHAR(100) NOT NULL,
       latitude FLOAT NOT NULL,
       longitude FLOAT NOT NULL,
       temperature FLOAT NOT NULL,
       requested_at TIMESTAMP NOT NULL
   );
   
   -- Создание индекса для быстрого поиска
   CREATE INDEX idx_weather_cache_search 
   ON weather_cache (request_type, city, latitude, longitude);