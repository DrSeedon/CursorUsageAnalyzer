"""Анализатор CSV файлов с данными использования."""

import csv
from collections import defaultdict
from datetime import datetime, timedelta
from tqdm import tqdm
from .cost_calculator import CostCalculator


class CSVAnalyzer:
    """Класс для анализа CSV данных об использовании Cursor."""
    
    def __init__(self, csv_file, period='all'):
        """
        Инициализирует анализатор.
        
        Args:
            csv_file: Путь к CSV файлу
            period: 'all', 'month', 'week', 'day'
        """
        self.csv_file = csv_file
        self.period = period
        self.period_start = self._get_period_start()
        self.models = defaultdict(lambda: {
            'included_requests': 0, 'on_demand_requests': 0,
            'included_cost': 0.0, 'on_demand_cost': 0.0,
            'input_tokens': 0, 'output_tokens': 0,
            'cache_read': 0, 'cache_write': 0,
            'errors': 0
        })
        self.daily_usage = defaultdict(lambda: defaultdict(int))
        self.hourly_usage = defaultdict(int)
        self.request_costs_by_model = defaultdict(list)  # Для box plot
    
    def _get_period_start(self):
        """Возвращает начальную дату фильтрации."""
        now = datetime.now()
        if self.period == 'day':
            return now - timedelta(days=1)
        elif self.period == 'week':
            return now - timedelta(days=7)
        elif self.period == 'month':
            return now - timedelta(days=30)
        return None  # 'all' - без фильтра
        
    def analyze(self):
        """Анализирует CSV файл и собирает статистику."""
        print("\n📊 Анализирую CSV файл...")
        
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            lines = sum(1 for _ in f) - 1
        
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in tqdm(reader, total=lines, desc="Обработка данных", unit="строк"):
                self._process_row(row)
        
        return {
            'models': dict(self.models),
            'daily_usage': dict(self.daily_usage),
            'hourly_usage': dict(self.hourly_usage),
            'request_costs_by_model': dict(self.request_costs_by_model)
        }
    
    def _process_row(self, row):
        """Обрабатывает одну строку CSV."""
        try:
            model = row['Model']
            kind = row['Kind']
            
            # Парсим дату с UTC+7 смещением
            date_obj = datetime.fromisoformat(row['Date'].replace('Z', '+00:00'))
            date_utc7 = date_obj + timedelta(hours=7)
            date_utc7_naive = date_utc7.replace(tzinfo=None)
            
            # Фильтруем по периоду
            if self.period_start and date_utc7_naive < self.period_start:
                return
            
            date_str = date_utc7_naive.strftime('%Y-%m-%d')
            hour = date_utc7_naive.hour
            
            # Парсим токены
            input_tokens = int(row.get('Input (w/ Cache Write)', 0) or 0)
            output_tokens = int(row.get('Output Tokens', 0) or 0)
            cache_read = int(row.get('Cache Read', 0) or 0)
            
            input_no_cache = int(row.get('Input (w/o Cache Write)', 0) or 0)
            cache_write = max(0, input_tokens - input_no_cache)
            
            # Считаем стоимость
            cost = CostCalculator.calculate_cost(
                model, input_no_cache, output_tokens, cache_read, cache_write
            )
            
            # Обновляем статистику
            if kind == 'Included':
                self.models[model]['included_requests'] += 1
                self.models[model]['included_cost'] += cost
                self.request_costs_by_model[model].append(cost)
            elif kind == 'On-Demand':
                self.models[model]['on_demand_requests'] += 1
                self.models[model]['on_demand_cost'] += cost
                self.request_costs_by_model[model].append(cost)
            elif kind == 'Rate Limited':
                self.models[model]['errors'] += 1
            
            # Обновляем токены
            self.models[model]['input_tokens'] += input_tokens
            self.models[model]['output_tokens'] += output_tokens
            self.models[model]['cache_read'] += cache_read
            self.models[model]['cache_write'] += cache_write
            
            # Дневная и почасовая статистика (только для Included/On-Demand)
            if kind in ['Included', 'On-Demand']:
                self.daily_usage[date_str][model] += 1
                self.hourly_usage[hour] += 1
                
        except (KeyError, ValueError) as e:
            # Пропускаем проблемные строки
            pass
    
    def get_total_cost(self):
        """Возвращает общую стоимость использования."""
        return sum(
            m['included_cost'] + m['on_demand_cost'] 
            for m in self.models.values()
        )
    
    def get_total_requests(self):
        """Возвращает общее количество запросов."""
        return sum(
            m['included_requests'] + m['on_demand_requests'] 
            for m in self.models.values()
        )

