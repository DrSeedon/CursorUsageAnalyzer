"""Утилиты для работы с файлами."""

import sys
import io
import glob
import os
import shutil


def find_csv_file():
    """Находит CSV файл с данными об использовании в папке csv_data."""
    csv_files = glob.glob('csv_data/team-usage-events-*.csv')
    if not csv_files:
        raise FileNotFoundError("CSV файл не найден! Поместите файл team-usage-events-*.csv в папку csv_data/")
    
    csv_files.sort()
    return csv_files[0]


def clear_directory(directory_path):
    """Удаляет все файлы и подпапки в указанной директории."""
    if not os.path.exists(directory_path):
        return
        
    print(f"🧹 Очистка папки {directory_path}...")
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


def setup_output_encoding():
    """Настраивает кодировку вывода для Windows."""
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

