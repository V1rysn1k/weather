"""
Модуль команд для получения погодных данных.

Этот модуль содержит функции для получения данных о погоде
по названию города или координатам, с использованием кэширования.
"""
from .api import get_coordinates, get_city_by_coords, get_current_weather
from .cache import get_cached_weather, set_cached_weather


def get_weather_by_city(city: str):
    """Получает данные о погоде по названию города.
    
    Args:
        city (str): Название города.
    
    Returns:
        tuple: Кортеж содержащий:
            - dict: Данные о погоде
            - bool: Флаг использования кэша
            - str: Название города
            - float: Широта
            - float: Долгота
    
    Raises:
        ValueError: Если город не найден или произошла ошибка при получении погоды.
    """
    coords = get_coordinates(city)
    if not coords:
        raise ValueError(f"Город '{city}' не найден")

    latitude = coords["latitude"]
    longitude = coords["longitude"]

    cached = get_cached_weather("city", city, latitude, longitude)
    if cached:
        return cached, True, city, latitude, longitude

    weather = get_current_weather(latitude, longitude)
    if weather is None:
        raise ValueError("Ошибка получения данных о погоде")

    temperature = weather["temperature"]

    set_cached_weather("city", city, latitude, longitude, temperature)

    return {"temperature": temperature}, False, city, latitude, longitude


def get_weather_by_coords(lat: float, lon: float):
    """Получает данные о погоде по географическим координатам.
    
    Args:
        lat (float): Широта.
        lon (float): Долгота.
    
    Returns:
        tuple: Кортеж содержащий:
            - dict: Данные о погоде
            - bool: Флаг использования кэша
            - str: Название города
            - float: Широта
            - float: Долгота
    
    Raises:
        ValueError: Если произошла ошибка при получении погоды.
    """
    city = get_city_by_coords(lat, lon)
    if city is None:
        city = "Неизвестно"

    cached = get_cached_weather("coords", city, lat, lon)
    if cached:
        return cached, True, city, lat, lon

    weather = get_current_weather(lat, lon)
    if weather is None:
        raise ValueError("Ошибка получения данных о погоде")

    temperature = weather["temperature"]

    set_cached_weather("coords", city, lat, lon, temperature)

    return {"temperature": temperature}, False, city, lat, lon
