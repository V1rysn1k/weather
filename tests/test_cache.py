import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cache import get_connection, get_cached_weather, set_cached_weather


class TestCache(unittest.TestCase):
    """Тесты для модуля кэширования"""
    
    @patch('cache.psycopg2.connect')
    def test_get_connection(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        conn = get_connection()
        
        mock_connect.assert_called_once_with(
            dbname='weather',
            user='postgres',
            password='1234',
            host='localhost',
            port=5432
        )
        self.assertEqual(conn, mock_conn)

    @patch('cache.get_connection')
    def test_get_cached_weather_exists(self, mock_get_conn):
        # Создаем моки для цепочки контекстных менеджеров
        mock_conn_context = MagicMock()
        mock_conn = MagicMock()
        mock_cursor_context = MagicMock()
        mock_cursor = MagicMock()
        
        # Настраиваем цепочку вызовов
        mock_get_conn.return_value = mock_conn_context
        mock_conn_context.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor_context
        mock_cursor_context.__enter__.return_value = mock_cursor
        
        # Настраиваем возвращаемые данные
        mock_cursor.fetchone.return_value = (25.5, datetime(2023, 10, 1, 12, 0, 0))

        result = get_cached_weather('city', 'Moscow', 55.7558, 37.6173)

        expected = {
            'temperature': 25.5,
            'requested_at': datetime(2023, 10, 1, 12, 0, 0)
        }
        self.assertEqual(result, expected)
        mock_cursor.execute.assert_called_once()

    @patch('cache.get_connection')
    def test_get_cached_weather_not_exists(self, mock_get_conn):
        # Создаем моки для цепочки контекстных менеджеров
        mock_conn_context = MagicMock()
        mock_conn = MagicMock()
        mock_cursor_context = MagicMock()
        mock_cursor = MagicMock()
        
        # Настраиваем цепочку вызовов
        mock_get_conn.return_value = mock_conn_context
        mock_conn_context.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor_context
        mock_cursor_context.__enter__.return_value = mock_cursor
        
        # Настраиваем возвращаемые данные (нет в кэше)
        mock_cursor.fetchone.return_value = None

        result = get_cached_weather('city', 'Unknown', 0, 0)

        self.assertIsNone(result)

    @patch('cache.get_connection')
    def test_set_cached_weather(self, mock_get_conn):
        # Создаем моки для цепочки контекстных менеджеров
        mock_conn_context = MagicMock()
        mock_conn = MagicMock()
        mock_cursor_context = MagicMock()
        mock_cursor = MagicMock()
        
        # Настраиваем цепочку вызовов
        mock_get_conn.return_value = mock_conn_context
        mock_conn_context.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor_context
        mock_cursor_context.__enter__.return_value = mock_cursor

        set_cached_weather('city', 'Moscow', 55.7558, 37.6173, 25.5)

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()