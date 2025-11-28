import unittest
import sys
import os

# Добавляем текущую директорию в путь для импорта модулей
sys.path.append('.')

if __name__ == '__main__':
    # Находим все тесты в директории tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Возвращаем код выхода в зависимости от результата тестов
    sys.exit(0 if result.wasSuccessful() else 1)