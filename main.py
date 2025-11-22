import sys
from .commands import get_weather_by_city, get_weather_by_coords


def is_coordinates(items):
    if len(items) != 2:
        return False
    try:
        float(items[0])
        float(items[1])
        return True
    except ValueError:
        return False


def process_query(query):
    query_parts = query.strip().split()
    if not query_parts:
        return None

    if is_coordinates(query_parts):
        lat, lon = float(query_parts[0]), float(query_parts[1])
        return get_weather_by_coords(lat, lon)
    else:
        city = ' '.join(query_parts)
        return get_weather_by_city(city)


def main():
    print("Запущено приложение погоды.")
    print("Введите город либо координаты (широта и долгота). Для выхода введите 'exit' или пустую строку.")
    
    while True:
        user_input = input("> ").strip()
        if user_input.lower() in ('exit', 'выход', ''):
            print("Выход из программы.")
            break
        try:
            result = process_query(user_input)
            if result is None:
                continue
            weather, from_cache, city, lat, lon = result
            source = "кэша" if from_cache else "API"
            temp = weather["temperature"]
            print(f"Город: {city}")
            print(f"Координаты: широта {lat}, долгота {lon}")
            print(f"Температура: {temp} °C")
        except Exception as e:
            print(f"Ошибка: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
