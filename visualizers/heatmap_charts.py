"""Визуализатор хитмапов."""

import csv
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime, timedelta
from tqdm import tqdm
from .base_visualizer import BaseVisualizer


class HeatmapChartsVisualizer(BaseVisualizer):
    """Класс для создания хитмапов активности и стоимости."""
    
    def __init__(self, csv_file, output_dir='graphics'):
        """
        Инициализирует визуализатор хитмапов.
        
        Args:
            csv_file: Путь к CSV файлу для чтения данных
            output_dir: Директория для сохранения графиков
        """
        super().__init__(output_dir)
        self.csv_file = csv_file
    
    @staticmethod
    def _format_value(value, decimals=1):
        """Форматирует число, показывая 0 без дробной части."""
        if value == 0:
            return "0"
        return f"{value:.{decimals}f}"
    
    def create_combined_requests_heatmap(self):
        """Создает объединенный хитмап: матрица в центре, суммы по краям."""
        weekday_hourly = defaultdict(lambda: defaultdict(int))
        
        print("  └─ Объединенный хитмап активности...")
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            lines = sum(1 for _ in f) - 1
        
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in tqdm(reader, total=lines, desc="     Обработка", unit="строк", leave=False):
                if row['Kind'] in ['Included', 'On-Demand']:
                    try:
                        date_obj = datetime.fromisoformat(row['Date'].replace('Z', '+00:00'))
                        date_utc7 = date_obj + timedelta(hours=7)
                        weekday = date_utc7.weekday()
                        hour = date_utc7.hour
                        weekday_hourly[weekday][hour] += 1
                    except:
                        pass
        
        weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = []
        
        for weekday in range(7):
            row = [weekday_hourly[weekday].get(hour, 0) for hour in range(24)]
            heatmap_data.append(row)
        
        heatmap_array = np.array(heatmap_data)
        hourly_totals = heatmap_array.sum(axis=0)
        weekday_totals = heatmap_array.sum(axis=1)
        
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(2, 2, height_ratios=[1, 4], width_ratios=[1, 8], 
                              hspace=0.05, wspace=0.05)
        
        ax_top = fig.add_subplot(gs[0, 1])
        ax_left = fig.add_subplot(gs[1, 0])
        ax_main = fig.add_subplot(gs[1, 1])
        
        hourly_matrix = hourly_totals.reshape(1, -1)
        sns.heatmap(hourly_matrix, annot=True, fmt='.0f', cmap='YlOrRd',
                    xticklabels=[], yticklabels=[], ax=ax_top, cbar=False)
        ax_top.set_title('Activity by Hour and Day', 
                        fontsize=16, fontweight='bold', pad=20)
        
        weekday_matrix = weekday_totals.reshape(-1, 1)
        sns.heatmap(weekday_matrix, annot=True, fmt='.0f', cmap='YlOrRd',
                    xticklabels=[], yticklabels=weekday_names, ax=ax_left, cbar=False)
        
        sns.heatmap(heatmap_array, annot=True, fmt='.0f', cmap='YlOrRd',
                    xticklabels=list(range(24)), yticklabels=[],
                    ax=ax_main, cbar=False)
        ax_main.set_xlabel('Hour of Day', fontsize=12)
        
        plt.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.05)
        self.save_figure('requests_heatmap.png', use_tight_layout=False)
    
    def create_combined_cost_heatmap(self):
        """Создает объединенный хитмап стоимости: матрица в центре, суммы по краям."""
        weekday_hourly_cost = defaultdict(lambda: defaultdict(float))
        
        print("  └─ Объединенный хитмап стоимости...")
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            lines = sum(1 for _ in f) - 1
        
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in tqdm(reader, total=lines, desc="     Обработка", unit="строк", leave=False):
                if row['Kind'] in ['Included', 'On-Demand']:
                    try:
                        date_obj = datetime.fromisoformat(row['Date'].replace('Z', '+00:00'))
                        date_utc7 = date_obj + timedelta(hours=7)
                        weekday = date_utc7.weekday()
                        hour = date_utc7.hour
                        cost_str = row['Cost']
                        cost = float(cost_str) if (cost_str and cost_str != 'NaN') else 0.0
                        weekday_hourly_cost[weekday][hour] += cost
                    except:
                        pass
        
        weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = []
        
        for weekday in range(7):
            row = [weekday_hourly_cost[weekday].get(hour, 0.0) for hour in range(24)]
            heatmap_data.append(row)
        
        heatmap_array = np.array(heatmap_data, dtype=float)
        hourly_totals = heatmap_array.sum(axis=0)
        weekday_totals = heatmap_array.sum(axis=1)
        
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(2, 2, height_ratios=[1, 4], width_ratios=[1, 8], 
                              hspace=0.05, wspace=0.05)
        
        ax_top = fig.add_subplot(gs[0, 1])
        ax_left = fig.add_subplot(gs[1, 0])
        ax_main = fig.add_subplot(gs[1, 1])
        
        hourly_matrix = hourly_totals.reshape(1, -1)
        hourly_labels = np.array([[self._format_value(c) for c in hourly_totals]])
        sns.heatmap(hourly_matrix, annot=hourly_labels, fmt='', cmap='YlOrRd',
                    xticklabels=[], yticklabels=[], ax=ax_top, cbar=False)
        ax_top.set_title('Cost by Hour and Day', 
                        fontsize=16, fontweight='bold', pad=20)
        
        weekday_matrix = weekday_totals.reshape(-1, 1)
        weekday_labels = np.array([[self._format_value(c)] for c in weekday_totals])
        sns.heatmap(weekday_matrix, annot=weekday_labels, fmt='', cmap='YlOrRd',
                    xticklabels=[], yticklabels=weekday_names, ax=ax_left, cbar=False)
        
        main_labels = np.array([[self._format_value(val) for val in row] for row in heatmap_data])
        sns.heatmap(heatmap_array, annot=main_labels, fmt='', cmap='YlOrRd',
                    xticklabels=list(range(24)), yticklabels=[],
                    ax=ax_main, cbar=False)
        ax_main.set_xlabel('Hour of Day', fontsize=12)
        
        plt.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.05)
        self.save_figure('cost_heatmap.png', use_tight_layout=False)
    
    def create_cost_per_request_heatmap(self):
        """Создает хитмап средней стоимости на запрос: стоимость / количество платных запросов."""
        weekday_hourly_cost = defaultdict(lambda: defaultdict(float))
        weekday_hourly_count = defaultdict(lambda: defaultdict(int))
        
        print("  └─ Хитмап средней стоимости запроса...")
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            lines = sum(1 for _ in f) - 1
        
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in tqdm(reader, total=lines, desc="     Обработка", unit="строк", leave=False):
                if row['Kind'] in ['Included', 'On-Demand']:
                    try:
                        cost_str = row['Cost']
                        cost = float(cost_str) if (cost_str and cost_str != 'NaN') else 0.0
                        
                        if cost > 0:
                            date_obj = datetime.fromisoformat(row['Date'].replace('Z', '+00:00'))
                            date_utc7 = date_obj + timedelta(hours=7)
                            weekday = date_utc7.weekday()
                            hour = date_utc7.hour
                            
                            weekday_hourly_cost[weekday][hour] += cost
                            weekday_hourly_count[weekday][hour] += 1
                    except:
                        pass
        
        weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = []
        
        for weekday in range(7):
            row = []
            for hour in range(24):
                total_cost = weekday_hourly_cost[weekday].get(hour, 0.0)
                total_count = weekday_hourly_count[weekday].get(hour, 0)
                avg_cost = (total_cost / total_count) if total_count > 0 else 0.0
                row.append(avg_cost)
            heatmap_data.append(row)
        
        heatmap_array = np.array(heatmap_data, dtype=float)
        
        hourly_avg = []
        for hour in range(24):
            hour_cost = sum(weekday_hourly_cost[wd].get(hour, 0.0) for wd in range(7))
            hour_count = sum(weekday_hourly_count[wd].get(hour, 0) for wd in range(7))
            hourly_avg.append((hour_cost / hour_count) if hour_count > 0 else 0.0)
        
        weekday_avg = []
        for weekday in range(7):
            day_cost = sum(weekday_hourly_cost[weekday].get(h, 0.0) for h in range(24))
            day_count = sum(weekday_hourly_count[weekday].get(h, 0) for h in range(24))
            weekday_avg.append((day_cost / day_count) if day_count > 0 else 0.0)
        
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(2, 2, height_ratios=[1, 4], width_ratios=[1, 8], 
                              hspace=0.05, wspace=0.05)
        
        ax_top = fig.add_subplot(gs[0, 1])
        ax_left = fig.add_subplot(gs[1, 0])
        ax_main = fig.add_subplot(gs[1, 1])
        
        hourly_matrix = np.array(hourly_avg).reshape(1, -1)
        hourly_labels = np.array([[f'{v:.3f}' if v > 0 else '0' for v in hourly_avg]])
        sns.heatmap(hourly_matrix, annot=hourly_labels, fmt='', cmap='YlOrRd',
                    xticklabels=[], yticklabels=[], ax=ax_top, cbar=False)
        ax_top.set_title('Average Cost Per Request ($) by Hour and Day', 
                        fontsize=16, fontweight='bold', pad=20)
        
        weekday_matrix = np.array(weekday_avg).reshape(-1, 1)
        weekday_labels = np.array([[f'{v:.3f}' if v > 0 else '0'] for v in weekday_avg])
        sns.heatmap(weekday_matrix, annot=weekday_labels, fmt='', cmap='YlOrRd',
                    xticklabels=[], yticklabels=weekday_names, ax=ax_left, cbar=False)
        
        main_labels = np.array([[f'{val:.3f}' if val > 0 else '0' for val in row] for row in heatmap_data])
        sns.heatmap(heatmap_array, annot=main_labels, fmt='', cmap='YlOrRd',
                    xticklabels=list(range(24)), yticklabels=[],
                    ax=ax_main, cbar=False)
        ax_main.set_xlabel('Hour of Day', fontsize=12)
        
        plt.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.05)
        self.save_figure('cost_per_request_heatmap.png', use_tight_layout=False)
