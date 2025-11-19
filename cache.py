import psycopg2
from datetime import datetime

DB_PARAMS = {
    'dbname': 'weather',
    'user': 'postgres',
    'password': '1234',
    'host': 'localhost',
    'port': 5432,
}

TABLE_NAME = 'weather_cache'


def get_connection():
    return psycopg2.connect(**DB_PARAMS)


def get_cached_weather(request_type: str, city: str, latitude: float, longitude: float):
    sql = f'''
    SELECT temperature, requested_at 
    FROM {TABLE_NAME} 
    WHERE request_type = %s AND city = %s AND latitude = %s AND longitude = %s
    ORDER BY requested_at DESC LIMIT 1;
    '''
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (request_type, city, latitude, longitude))
            row = cur.fetchone()
            if row:
                temperature, requested_at = row
                return {'temperature': temperature, 'requested_at': requested_at}
    return None


def set_cached_weather(request_type: str, city: str, latitude: float, longitude: float, temperature: float):
    sql = f'''
    INSERT INTO {TABLE_NAME} 
    (request_type, city, latitude, longitude, temperature, requested_at)
    VALUES (%s, %s, %s, %s, %s, %s);
    '''
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (request_type, city, latitude, longitude, temperature, datetime.now()))
        conn.commit()
