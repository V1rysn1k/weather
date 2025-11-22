Модуль api
==========

.. automodule:: api
   :members:
   :undoc-members:
   :show-inheritance:
   :caption: Содержание:

Класс WeatherAPI
----------------

.. autoclass:: api.WeatherAPI
   :members:
   :undoc-members:

   **Атрибуты класса:**

   .. autoattribute:: api.WeatherAPI.BASE_GEO_URL
   
   .. autoattribute:: api.WeatherAPI.BASE_FORECAST_URL

   **Методы:**

   .. automethod:: api.WeatherAPI.get_coordinates

   .. automethod:: api.WeatherAPI.get_city_by_coords

   .. automethod:: api.WeatherAPI.get_current_weather

Методы класса
-------------

.. autofunction:: api.WeatherAPI.get_coordinates

   **Аргументы:**
   
   * **city_name** (str) - Название города для поиска координат
   
   **Возвращает:**
   
   * dict or None - Словарь с координатами города или None при ошибке
   
   **Пример:**
   
   .. code-block:: python
   
      api = WeatherAPI()
      coords = api.get_coordinates("Москва")
      if coords:
          lat = coords["latitude"]  # 55.7558
          lon = coords["longitude"] # 37.6173

.. autofunction:: api.WeatherAPI.get_city_by_coords

   **Аргументы:**
   
   * **latitude** (float) - Географическая широта
   * **longitude** (float) - Географическая долгота
   
   **Возвращает:**
   
   * str or None - Название города или None при ошибке
   
   **Пример:**
   
   .. code-block:: python
   
      api = WeatherAPI()
      city = api.get_city_by_coords(55.7558, 37.6173)
      print(city)  # "Москва"

.. autofunction:: api.WeatherAPI.get_current_weather

   **Аргументы:**
   
   * **latitude** (float) - Географическая широта
   * **longitude** (float) - Географическая долгота
   
   **Возвращает:**
   
   * dict or None - Словарь с данными о погоде или None при ошибке
   
   **Пример:**
   
   .. code-block:: python
   
      api = WeatherAPI()
      weather = api.get_current_weather(55.7558, 37.6173)
      if weather:
          temp = weather["temperature"]  # 15.5

Пример использования
--------------------

.. code-block:: python

   from api import WeatherAPI
   
   # Создание экземпляра API
   weather_api = WeatherAPI()
   
   # Получение координат города
   coordinates = weather_api.get_coordinates("Москва")
   if coordinates:
       latitude = coordinates["latitude"]
       longitude = coordinates["longitude"]
       print(f"Координаты Москвы: {latitude}, {longitude}")
   
   # Получение погоды по координатам
   weather_data = weather_api.get_current_weather(55.7558, 37.6173)
   if weather_data:
       temperature = weather_data["temperature"]
       print(f"Температура: {temperature}°C")
   
   # Получение города по координатам
   city_name = weather_api.get_city_by_coords(59.9343, 30.3351)
   print(f"Город по координатам: {city_name}")  # Санкт-Петербург