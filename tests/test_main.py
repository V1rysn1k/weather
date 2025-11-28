import unittest
import sys
import os
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import is_coordinates, process_query


class TestMain(unittest.TestCase):
    """Тесты для основного модуля"""
    
    def test_is_coordinates_valid(self):
        self.assertTrue(is_coordinates(['55.7558', '37.6173']))
        self.assertTrue(is_coordinates(['-90.0', '180.0']))

    def test_is_coordinates_invalid(self):
        self.assertFalse(is_coordinates(['55.7558']))
        self.assertFalse(is_coordinates(['55.7558', '37.6173', 'extra']))
        self.assertFalse(is_coordinates(['not_number', '37.6173']))
        self.assertFalse(is_coordinates(['55.7558', 'not_number']))

    @patch('main.get_weather_by_city')
    def test_process_query_city(self, mock_weather_city):
        mock_weather_city.return_value = (
            {'temperature': 25.5}, False, 'Moscow', 55.7558, 37.6173
        )
        
        result = process_query('Moscow')
        
        mock_weather_city.assert_called_once_with('Moscow')
        expected = ({'temperature': 25.5}, False, 'Moscow', 55.7558, 37.6173)
        self.assertEqual(result, expected)

    @patch('main.get_weather_by_coords')
    def test_process_query_coords(self, mock_weather_coords):
        mock_weather_coords.return_value = (
            {'temperature': 25.5}, False, 'Moscow', 55.7558, 37.6173
        )
        
        result = process_query('55.7558 37.6173')
        
        mock_weather_coords.assert_called_once_with(55.7558, 37.6173)
        expected = ({'temperature': 25.5}, False, 'Moscow', 55.7558, 37.6173)
        self.assertEqual(result, expected)

    def test_process_query_empty(self):
        self.assertIsNone(process_query(''))
        self.assertIsNone(process_query('   '))


if __name__ == '__main__':
    unittest.main()