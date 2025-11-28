import unittest
import sys
import os
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from commands import get_weather_by_city, get_weather_by_coords


class TestCommands(unittest.TestCase):
    """Тесты для командного модуля"""
    
    @patch('commands.get_coordinates')
    @patch('commands.get_cached_weather')
    @patch('commands.get_current_weather')
    @patch('commands.set_cached_weather')
    def test_get_weather_by_city_from_cache(self, mock_set, mock_weather, mock_cache, mock_coords):
        mock_coords.return_value = {'latitude': 55.7558, 'longitude': 37.6173}
        mock_cache.return_value = {'temperature': 25.5}
        
        result = get_weather_by_city('Moscow')
        
        weather, from_cache, city, lat, lon = result
        self.assertEqual(weather, {'temperature': 25.5})
        self.assertTrue(from_cache)
        self.assertEqual(city, 'Moscow')
        self.assertEqual(lat, 55.7558)
        self.assertEqual(lon, 37.6173)
        mock_weather.assert_not_called()
        mock_set.assert_not_called()

    @patch('commands.get_coordinates')
    @patch('commands.get_cached_weather')
    @patch('commands.get_current_weather')
    @patch('commands.set_cached_weather')
    def test_get_weather_by_city_from_api(self, mock_set, mock_weather, mock_cache, mock_coords):
        mock_coords.return_value = {'latitude': 55.7558, 'longitude': 37.6173}
        mock_cache.return_value = None
        mock_weather.return_value = {'temperature': 26.0}
        
        result = get_weather_by_city('Moscow')
        
        weather, from_cache, city, lat, lon = result
        self.assertEqual(weather, {'temperature': 26.0})
        self.assertFalse(from_cache)
        mock_set.assert_called_once_with('city', 'Moscow', 55.7558, 37.6173, 26.0)

    @patch('commands.get_coordinates')
    def test_get_weather_by_city_not_found(self, mock_coords):
        mock_coords.return_value = None
        
        with self.assertRaises(ValueError) as context:
            get_weather_by_city('Unknown')
        
        self.assertEqual(str(context.exception), "Город 'Unknown' не найден")

    @patch('commands.get_city_by_coords')
    @patch('commands.get_cached_weather')
    @patch('commands.get_current_weather')
    @patch('commands.set_cached_weather')
    def test_get_weather_by_coords_from_cache(self, mock_set, mock_weather, mock_cache, mock_city):
        mock_city.return_value = 'Москва'
        mock_cache.return_value = {'temperature': 25.5}
        
        result = get_weather_by_coords(55.7558, 37.6173)
        
        weather, from_cache, city, lat, lon = result
        self.assertTrue(from_cache)
        mock_weather.assert_not_called()
        mock_set.assert_not_called()


if __name__ == '__main__':
    unittest.main()