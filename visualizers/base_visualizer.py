"""Базовый класс для визуализаторов."""

import os
import matplotlib.pyplot as plt


class BaseVisualizer:
    """Базовый класс для всех визуализаторов."""
    
    _figure_counter = 0
    
    def __init__(self, output_dir='graphics'):
        """
        Инициализирует визуализатор.
        
        Args:
            output_dir: Директория для сохранения графиков
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Настройка matplotlib
        plt.ioff()
        plt.switch_backend('Agg')
        plt.style.use('dark_background')
    
    def save_figure(self, filename, dpi=300, use_tight_layout=True):
        """
        Сохраняет текущую фигуру с автоматической нумерацией.
        
        Args:
            filename: Имя файла без номера (например, 'models_overview.png')
            dpi: Разрешение изображения
            use_tight_layout: Использовать ли tight_layout
        """
        BaseVisualizer._figure_counter += 1
        numbered_filename = f"{BaseVisualizer._figure_counter:02d}_{filename}"
        filepath = os.path.join(self.output_dir, numbered_filename)
        if use_tight_layout:
            plt.tight_layout()
        plt.savefig(filepath, dpi=dpi, bbox_inches='tight')
        plt.close()
    
    def create_subplot_grid(self, rows, cols, figsize):
        """
        Создает сетку подграфиков.
        
        Args:
            rows: Количество строк
            cols: Количество столбцов
            figsize: Размер фигуры (ширина, высота)
            
        Returns:
            tuple: (fig, axes)
        """
        return plt.subplots(rows, cols, figsize=figsize)

