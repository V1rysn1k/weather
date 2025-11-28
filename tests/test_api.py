import unittest
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api import get_coordinates, get_city_by_coords, get_current_weather


class TestAPI(unittest.TestCase):
    """Тесты для API модуля"""
    
    @patch('api.requests.get')
    def test_get_coordinates_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            'results': [{
                'latitude': 55.7558,
                'longitude': 37.6173
            }]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_coordinates('Moscow')
        
        self.assertEqual(result, {'latitude': 55.7558, 'longitude': 37.6173})
        mock_get.assert_called_once_with(
            'https://geocoding-api.open-meteo.com/v1/search?name=Moscow&count=1&language=ru',
            timeout=10
        )

    @patch('api.requests.get')
    def test_get_coordinates_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'results': []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_coordinates('UnknownCity')
        
        self.assertIsNone(result)

    @patch('api.requests.get')
    def test_get_city_by_coords_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            'address': {'city': 'Москва'},
            'display_name': 'Москва, Россия'
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_city_by_coords(55.7558, 37.6173)
        
        self.assertEqual(result, 'Москва')

    @patch('api.requests.get')
    def test_get_current_weather_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            'current_weather': {'temperature': 25.5}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_current_weather(55.7558, 37.6173)
        
        self.assertEqual(result, {'temperature': 25.5})


if __name__ == '__main__':
    unittest.main()