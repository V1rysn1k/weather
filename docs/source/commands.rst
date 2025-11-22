Модуль commands
===============

.. automodule:: commands
   :members:
   :undoc-members:
   :show-inheritance:
   :caption: Содержание:

Функции модуля
--------------

.. autofunction:: commands.get_weather_by_city

   Получает данные о погоде по названию города.
   
   **Аргументы:**
   
   * **city** (str) - Название города
   
   **Возвращает:**
   
   * tuple - Кортеж с результатом:
     
     .. code-block:: python
     
        (
            {"temperature": 15.5},  # Данные о погоде
            True,                    # Флаг использования кэша
            "Москва",               # Название города
            55.7558,                # Широта
            37.6173                 # Долгота
        )
   
   **Исключения:**
   
   * **ValueError** - Если город не найден или ошибка получения погоды
   
   **Алгоритм работы:**
   
   1. Геокодирование города в координаты
   2. Проверка наличия данных в кэше
   3. Если нет в кэше - запрос к API погоды
   4. Сохранение результата в кэш
   5. Возврат результата

.. autofunction:: commands.get_weather_by_coords

   Получает данные о погоде по географическим координатам.
   
   **Аргументы:**
   
   * **lat** (float) - Географическая широта
   * **lon** (float) - Географическая долгота
   
   **Возвращает:**
   
   * tuple - Кортеж с результатом (аналогично get_weather_by_city)
   
   **Исключения:**
   
   * **ValueError** - Если ошибка получения погоды
   
   **Алгоритм работы:**
   
   1. Обратное геокодирование координат в город
   2. Проверка наличия данных в кэше
   3. Если нет в кэше - запрос к API погоды
   4. Сохранение результата в кэш
   5. Возврат результата

Пример использования
--------------------

.. code-block:: python

   from commands import get_weather_by_city, get_weather_by_coords
   
   # Пример 1: Получение погоды по городу
   try:
       weather_data, from_cache, city, lat, lon = get_weather_by_city("Москва")
       
       source = "кэша" if from_cache else "API"
       temp = weather_data["temperature"]
       
       print(f"Город: {city}")
       print(f"Координаты: {lat}, {lon}")
       print(f"Температура: {temp}°C (из {source})")
       
   except ValueError as e:
       print(f"Ошибка: {e}")
   
   # Пример 2: Получение погоды по координатам
   try:
       weather_data, from_cache, city, lat, lon = get_weather_by_coords(59.9343, 30.3351)
       
       if from_cache:
           print("Данные получены из кэша")
       else:
           print("Данные получены из API")
           
       print(f"Температура в {city}: {weather_data['temperature']}°C")
       
   except ValueError as e:
       print(f"Ошибка: {e}")

Интеграция с системой
---------------------

Функции модуля commands интегрируются с:

* :mod:`api` - для геокодирования и получения погоды
* :mod:`cache` - для кэширования результатов
* :mod:`main` - для пользовательского интерфейса