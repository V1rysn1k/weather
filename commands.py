from .api import WeatherAPI
from .cache import get_cached_weather, set_cached_weather


def get_weather_by_city(city: str):
    api = WeatherAPI()
    coords = api.get_coordinates(city)
    if not coords:
        raise ValueError(f"Город '{city}' не найден")

    latitude = coords["latitude"]
    longitude = coords["longitude"]

    cached = get_cached_weather("city", city, latitude, longitude)
    if cached:
        return cached, True, city, latitude, longitude

    weather = api.get_current_weather(latitude, longitude)
    if weather is None:
        raise ValueError("Ошибка получения данных о погоде")

    temperature = weather["temperature"]

    set_cached_weather("city", city, latitude, longitude, temperature)

    return {"temperature": temperature}, False, city, latitude, longitude


def get_weather_by_coords(lat: float, lon: float):
    api = WeatherAPI()
    city = api.get_city_by_coords(lat, lon)
    if city is None:
        city = "Неизвестно"

    cached = get_cached_weather("coords", city, lat, lon)
    if cached:
        return cached, True, city, lat, lon

    weather = api.get_current_weather(lat, lon)
    if weather is None:
        raise ValueError("Ошибка получения данных о погоде")

    temperature = weather["temperature"]

    set_cached_weather("coords", city, lat, lon, temperature)

    return {"temperature": temperature}, False, city, lat, lon
