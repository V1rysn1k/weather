import unittest
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from commands import get_weather_by_city, get_weather_by_coords


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""
    
    @patch('commands.get_coordinates')
    @patch('commands.get_cached_weather')
    @patch('commands.get_current_weather')
    @patch('commands.set_cached_weather')
    def test_full_flow_city(self, mock_set, mock_weather, mock_cache, mock_coords):
        mock_coords.return_value = {'latitude': 55.7558, 'longitude': 37.6173}
        mock_cache.return_value = None
        mock_weather.return_value = {'temperature': 25.5}
        
        result = get_weather_by_city('Moscow')
        
        self.assertEqual(result[0], {'temperature': 25.5})
        self.assertFalse(result[1])
        mock_set.assert_called_once()

    @patch('commands.get_city_by_coords')
    @patch('commands.get_cached_weather')
    @patch('commands.get_current_weather')
    @patch('commands.set_cached_weather')
    def test_full_flow_coords(self, mock_set, mock_weather, mock_cache, mock_city):
        mock_city.return_value = 'Москва'
        mock_cache.return_value = None
        mock_weather.return_value = {'temperature': 25.5}
        
        result = get_weather_by_coords(55.7558, 37.6173)
        
        self.assertEqual(result[0], {'temperature': 25.5})
        self.assertFalse(result[1])
        mock_set.assert_called_once()


if __name__ == '__main__':
    unittest.main()