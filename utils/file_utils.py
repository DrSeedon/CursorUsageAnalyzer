"""Утилиты для работы с файлами."""

import sys
import io
import glob


def find_csv_file():
    """Находит CSV файл с данными об использовании в папке csv_data."""
    csv_files = glob.glob('csv_data/team-usage-events-*.csv')
    if not csv_files:
        raise FileNotFoundError("CSV файл не найден! Поместите файл team-usage-events-*.csv в папку csv_data/")
    
    csv_files.sort()
    return csv_files[0]


def setup_output_encoding():
    """Настраивает кодировку вывода для Windows."""
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

