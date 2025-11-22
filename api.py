"""Модуль для работы с внешними API погоды и геокодирования.

Этот модуль предоставляет класс для взаимодействия с Open-Meteo API
для получения данных о погоде и геокодирования.
"""
import requests
from typing import Optional


BASE_GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
BASE_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

def get_coordinates(city_name: str) -> Optional[dict]:
    """Получает координаты по названию города.

    Args:
        city_name (str): Название города.
        
    Returns:
        dict or None: Словарь с координатами города или None при ошибке.
    """
    try:
        url = f"{BASE_GEO_URL}?name={city_name}&count=1&language=ru"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if "results" in data and data["results"]:
            return data["results"][0]
        return None
    except requests.RequestException as e:
        print(f"Ошибка при запросе координат: {e}")
        return None

def get_city_by_coords(latitude: float, longitude: float) -> Optional[str]:
    """Получает название города по координатам.
        
    Args:
        latitude (float): Широта.
        longitude (float): Долгота.
        
    Returns:
        str or None: Название города или None при ошибке.
    """
    try:
        url = (
            f"https://nominatim.openstreetmap.org/reverse?"
            f"format=json&lat={latitude}&lon={longitude}&accept-language=ru"
        )
        headers = {"User-Agent": "weather_app/1.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        address = data.get('address', {})
        for key in ['city', 'town', 'village', 'hamlet']:
            if key in address:
                return address[key]
        return data.get('display_name')
    except requests.RequestException as e:
        print(f"Ошибка при обратном геокодировании: {e}")
        return None

def get_current_weather(latitude: float, longitude: float) -> Optional[dict]:
    """Получает текущую погоду по координатам.
        
    Args:
        latitude (float): Широта.
        longitude (float): Долгота.
        
    Returns:
        dict or None: Словарь с данными о погоде или None при ошибке.
    """
    try:
        url = f"{BASE_FORECAST_URL}?latitude={latitude}&longitude={longitude}&current_weather=true"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if "current_weather" in data:
            return data["current_weather"]
        return None
    except requests.RequestException as e:
        print(f"Ошибка при запросе погоды: {e}")
        return None