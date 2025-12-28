"""Визуализатор графиков активности."""

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from .base_visualizer import BaseVisualizer


class ActivityChartsVisualizer(BaseVisualizer):
    """Класс для создания графиков активности."""
    
    def create_daily_activity(self, daily_usage):
        """Создает график активности по дням (топ-5 моделей на одном графике)."""
        print("  ├─ Дневная активность...")
        all_days = sorted(daily_usage.keys())
        
        # Находим топ-5 моделей
        model_totals = defaultdict(float)
        for day_data in daily_usage.values():
            for model, count in day_data.items():
                model_totals[model] += count
        
        top_models = sorted(model_totals.items(), key=lambda x: x[1], reverse=True)[:5]
        
        bright_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        
        fig, ax = plt.subplots(figsize=(16, 8))
        
        for idx, (model, _) in enumerate(top_models):
            daily_requests = [daily_usage[day].get(model, 0) for day in all_days]
            ax.plot(all_days, daily_requests, marker='o', label=model, linewidth=3,
                    color=bright_colors[idx], markersize=6, alpha=0.9)
        
        ax.set_title('Daily Activity (Top 5 Models)', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Number of Requests', fontsize=12)
        ax.legend(fontsize=11, loc='upper left')
        ax.grid(True, alpha=0.4, linestyle='--', linewidth=0.8)
        ax.set_facecolor('#0a0a0a')
        plt.xticks(rotation=45, fontsize=10)
        
        self.save_figure('daily_activity.png')
    
    def create_daily_activity_separate(self, daily_usage):
        """Создает график активности по дням (каждая модель отдельно, вертикально)."""
        print("  ├─ Дневная активность (раздельно)...")
        all_days = sorted(daily_usage.keys())
        
        # Находим топ-5 моделей
        model_totals = defaultdict(float)
        for day_data in daily_usage.values():
            for model, count in day_data.items():
                model_totals[model] += count
        
        top_models = sorted(model_totals.items(), key=lambda x: x[1], reverse=True)[:5]
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        
        fig, axes = plt.subplots(5, 1, figsize=(16, 20))
        
        for idx, (model, _) in enumerate(top_models):
            ax = axes[idx]
            daily_requests = [daily_usage[day].get(model, 0) for day in all_days]
            
            ax.bar(all_days, daily_requests, color=colors[idx], alpha=0.8, edgecolor='white', linewidth=1)
            ax.set_title(f'{model}', fontsize=14, fontweight='bold')
            ax.set_ylabel('Requests', fontsize=11)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            
            # Показываем каждую ~10ю дату для компактности
            step = max(1, len(all_days) // 10)
            ax.set_xticks(range(0, len(all_days), step))
            ax.set_xticklabels([all_days[i] for i in range(0, len(all_days), step)], 
                              rotation=45, ha='right', fontsize=9)
        
        axes[-1].set_xlabel('Date', fontsize=12)
        
        plt.suptitle('Daily Activity by Model', 
                    fontsize=18, fontweight='bold', y=0.995)
        
        self.save_figure('daily_activity_separate.png')
    
    def create_plans_comparison(self, monthly_api_cost):
        """Создает график сравнения планов Cursor Individual."""
        print("  ├─ Сравнение планов...")
        cursor_plans = {
            'API': monthly_api_cost,
            'Pro\n$20+$20': 20 + max(0, monthly_api_cost - 20),
            'Pro+\n$60+$70': 60 + max(0, monthly_api_cost - 70),
            'Ultra\n$200+$400': 200 if monthly_api_cost <= 400 else 200 + (monthly_api_cost - 400)
        }
        
        plan_names = list(cursor_plans.keys())
        plan_costs = list(cursor_plans.values())
        colors_plans = ['red', 'lightblue', 'blue', 'darkblue']
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        bars = ax.bar(plan_names, plan_costs, color=colors_plans, alpha=0.7)
        
        ax.set_title('Сравнение планов Cursor Individual vs API', fontsize=16, fontweight='bold')
        ax.set_ylabel('Стоимость ($)')
        ax.axhline(y=monthly_api_cost, color='yellow', linestyle='--', linewidth=2, 
                   label=f'API стоимость: ${monthly_api_cost:.0f}')
        
        # Добавляем числа на бары
        for bar, cost in zip(bars, plan_costs):
            ax.annotate(f'${cost:.0f}',
                       xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                       xytext=(0, 3), textcoords="offset points",
                       ha='center', va='bottom', fontweight='bold')
        
        ax.legend()
        
        self.save_figure('09_plans_comparison.png')
    
    def create_breakeven_analysis(self, monthly_api_cost):
        """Создает график анализа точек безубыточности."""
        print("  └─ Анализ безубыточности...")
        usage_range = np.linspace(0, 500, 200)
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Прямые API
        ax.plot(usage_range, usage_range, 'r--', linewidth=2, label='Прямые API', alpha=0.8)
        
        # Планы Cursor
        plans = [
            ('Pro', 20, 20),
            ('Pro+', 60, 70),
            ('Ultra', 200, 400)
        ]
        
        plan_colors = ['lightblue', 'blue', 'darkblue']
        
        for i, (plan_name, monthly, included) in enumerate(plans):
            cursor_costs = []
            for usage in usage_range:
                if usage <= included:
                    cost = monthly
                else:
                    cost = monthly + (usage - included)
                cursor_costs.append(cost)
            
            ax.plot(usage_range, cursor_costs, color=plan_colors[i], linewidth=2,
                   label=f'Cursor {plan_name}', alpha=0.8)
        
        ax.axvline(x=monthly_api_cost, color='yellow', linestyle=':', linewidth=2,
                   label=f'Текущее использование\n${monthly_api_cost:.0f}/мес')
        
        ax.set_xlabel('Месячное использование API ($)')
        ax.set_ylabel('Общая стоимость ($)')
        ax.set_title('⚖️ Анализ точек безубыточности: Cursor Individual vs API', 
                    fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 500)
        ax.set_ylim(0, 600)
        
        self.save_figure('10_breakeven_analysis.png')
    
    def _get_top_models(self, timeframe_data, n=10):
        """Возвращает топ-N моделей по стоимости в конкретном временном промежутке."""
        model_totals = defaultdict(float)
        for data in timeframe_data.values():
            for model, cost in data.items():
                model_totals[model] += cost
        
        top_models = sorted(model_totals.items(), key=lambda x: x[1], reverse=True)[:n]
        return [m[0] for m in top_models]
    
    def _get_model_colors(self, model_names):
        """Возвращает словарь цветов для моделей (поддерживает до 10 цветов)."""
        colors = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
            '#F1C40F', '#9B59B6', '#E67E22', '#3498DB', '#2ECC71'
        ]
        return {model: colors[i % len(colors)] for i, model in enumerate(model_names)}
    
    def _is_night(self, timestamp_str):
        """Проверяет, является ли время ночным (22:00 - 06:00)."""
        try:
            # Формат может быть 'YYYY-MM-DD HH:00' или 'YYYY-MM-DD HH:MM'
            hour = int(timestamp_str.split(' ')[1].split(':')[0])
            return hour >= 22 or hour < 6
        except:
            return False

    def _is_weekend(self, timestamp_str):
        """Проверяет, является ли день выходным."""
        try:
            from datetime import datetime
            # Формат 'YYYY-MM-DD' или начинается с него
            date_str = timestamp_str.split(' ')[0]
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            return dt.weekday() >= 5  # 5=Saturday, 6=Sunday
        except:
            return False

    def _get_bar_color(self, timestamp_str, base_color, night_color='#2c3e50', weekend_color='#e67e22'):
        """Возвращает цвет для бара в зависимости от времени."""
        if self._is_weekend(timestamp_str):
            return weekend_color
        if self._is_night(timestamp_str):
            return night_color
        return base_color
    
    def create_cost_timeline_all_period(self, all_timestamps):
        """График 1: Весь период, 200 точек по X."""
        print("  ├─ График стоимости за весь период (200 точек)...")
        
        if not all_timestamps:
            print("     [!] Нет данных о временных метках")
            return
        
        # Группируем данные в 200 бакетов
        num_buckets = min(200, len(all_timestamps))
        bucket_size = max(1, len(all_timestamps) // num_buckets)
        
        buckets_cost = []
        buckets_labels = []
        
        for i in range(0, len(all_timestamps), bucket_size):
            bucket = all_timestamps[i:i+bucket_size]
            if bucket:
                total_cost = sum(item[2] for item in bucket)
                buckets_cost.append(total_cost)
                buckets_labels.append(bucket[0][0].strftime('%Y-%m-%d'))
        
        # Кумулятивная сумма
        cumulative = []
        total = 0
        for val in buckets_cost:
            total += val
            cumulative.append(total)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        
        # График 1: Кумулятивная стоимость
        ax1.fill_between(range(len(cumulative)), cumulative, alpha=0.3, color='#2ecc71')
        ax1.plot(range(len(cumulative)), cumulative, color='#2ecc71', linewidth=2.5, marker='o', markersize=3)
        ax1.set_title('Cumulative Cost - All Period (200 points)', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Total Cost ($)', fontsize=12)
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # Подписи
        for i in [0, len(cumulative)//4, len(cumulative)//2, 3*len(cumulative)//4, -1]:
            if i < len(cumulative):
                ax1.annotate(f'${cumulative[i]:.2f}', 
                           xy=(i, cumulative[i]), 
                           xytext=(5, 10), textcoords='offset points',
                           fontsize=9, fontweight='bold', color='#2ecc71')
        
        # X-axis labels
        step = max(1, len(buckets_labels) // 10)
        ax1.set_xticks(range(0, len(buckets_labels), step))
        ax1.set_xticklabels([buckets_labels[i] for i in range(0, len(buckets_labels), step)], 
                          rotation=45, ha='right', fontsize=9)
        
        # График 2: Стоимость по бакетам
        colors = ['#e74c3c' if v > np.mean(buckets_cost) else '#3498db' for v in buckets_cost]
        ax2.bar(range(len(buckets_cost)), buckets_cost, color=colors, alpha=0.8, edgecolor='white', linewidth=0.5)
        ax2.axhline(y=np.mean(buckets_cost), color='yellow', linestyle='--', linewidth=2, 
                   label=f'Average: ${np.mean(buckets_cost):.2f}')
        ax2.set_title('Cost Distribution', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Time Period', fontsize=12)
        ax2.set_ylabel('Cost ($)', fontsize=12)
        ax2.legend(fontsize=10)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        
        ax2.set_xticks(range(0, len(buckets_labels), step))
        ax2.set_xticklabels([buckets_labels[i] for i in range(0, len(buckets_labels), step)], 
                          rotation=45, ha='right', fontsize=9)
        
        plt.tight_layout()
        self.save_figure('cost_timeline_all_period.png')
    
    def create_cost_timeline_last_month(self, daily_cost_by_model):
        """График 2: Последний месяц, по дням (все дни)."""
        print("  ├─ График стоимости за последний месяц (по дням)...")
        
        from datetime import datetime, timedelta
        
        if not daily_cost_by_model:
            print("     [!] Нет данных")
            return
        
        # Генерируем список последних 30 дней без пропусков
        end_date = datetime.now() + timedelta(hours=7) # UTC+7
        all_days = [(end_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]
        
        daily_values = []
        bar_colors = []
        for day in all_days:
            total = sum(daily_cost_by_model.get(day, {}).values())
            daily_values.append(total)
            bar_colors.append(self._get_bar_color(day, '#3498db', weekend_color='#e67e22'))
        
        # Кумулятивная сумма
        cumulative = []
        total = 0
        for val in daily_values:
            total += val
            cumulative.append(total)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        
        # График 1: Кумулятивная стоимость
        ax1.fill_between(range(len(cumulative)), cumulative, alpha=0.3, color='#3498db')
        ax1.plot(range(len(cumulative)), cumulative, color='#3498db', linewidth=2.5, marker='o', markersize=4)
        ax1.set_title('Cumulative Cost - Last 30 Days', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Total Cost ($)', fontsize=12)
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # Подписи
        if len(cumulative) > 0:
            ax1.annotate(f'${cumulative[-1]:.2f}', 
                       xy=(len(cumulative)-1, cumulative[-1]), 
                       xytext=(5, 10), textcoords='offset points',
                       fontsize=10, fontweight='bold', color='#3498db')
        
        # X-axis labels
        step = 3
        ax1.set_xticks(range(0, len(all_days), step))
        ax1.set_xticklabels([all_days[i] for i in range(0, len(all_days), step)], 
                          rotation=45, ha='right', fontsize=9)
        
        # График 2: Дневная стоимость
        ax2.bar(range(len(daily_values)), daily_values, color=bar_colors, alpha=0.8, edgecolor='white', linewidth=0.5)
        if len(daily_values) > 0:
            ax2.axhline(y=np.mean(daily_values), color='yellow', linestyle='--', linewidth=2, 
                       label=f'Average: ${np.mean(daily_values):.2f}/day')
        ax2.set_title('Daily Cost (Orange = Weekend)', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_ylabel('Cost ($)', fontsize=12)
        ax2.legend(fontsize=10)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        
        ax2.set_xticks(range(0, len(all_days), step))
        ax2.set_xticklabels([all_days[i] for i in range(0, len(all_days), step)], 
                          rotation=45, ha='right', fontsize=9)
        
        plt.tight_layout()
        self.save_figure('cost_timeline_last_month.png')
    
    def create_cost_timeline_last_week(self, hourly_cost_full):
        """График 3: Последняя неделя, по часам (168 часов без пропусков)."""
        print("  ├─ График стоимости за последнюю неделю (по часам)...")
        
        from datetime import datetime, timedelta
        
        if not hourly_cost_full:
            print("     [!] Нет данных о почасовой стоимости")
            return
        
        # Генерируем 168 часов (7 дней) без пропусков
        end_time = datetime.now() + timedelta(hours=7) # UTC+7
        start_time = end_time - timedelta(days=7)
        all_hours = []
        for i in range(168):
            dt = start_time + timedelta(hours=i+1)
            all_hours.append(dt.strftime('%Y-%m-%d %H:00'))
        
        values = [hourly_cost_full.get(t, 0) for t in all_hours]
        bar_colors = [self._get_bar_color(t, '#e74c3c', night_color='#2c3e50', weekend_color='#e67e22') for t in all_hours]
        
        # Кумулятивная сумма
        cumulative = []
        total = 0
        for val in values:
            total += val
            cumulative.append(total)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        
        # График 1: Кумулятивная стоимость
        ax1.fill_between(range(len(cumulative)), cumulative, alpha=0.3, color='#e74c3c')
        ax1.plot(range(len(cumulative)), cumulative, color='#e74c3c', linewidth=2, markersize=2)
        ax1.set_title('Cumulative Cost - Last 7 Days (Hourly)', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Total Cost ($)', fontsize=12)
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # Разделители дней (00:00) и вертикальные линии
        for i, t in enumerate(all_hours):
            if ':00' in t and t.endswith(' 00:00'):
                dt = datetime.strptime(t, '%Y-%m-%d %H:00')
                day_name = dt.strftime('%A')
                ax1.axvline(x=i, color='white', linestyle=':', alpha=0.4)
                ax1.text(i, ax1.get_ylim()[1]*0.9, day_name, color='white', rotation=90, alpha=0.6, fontsize=8)
                ax2.axvline(x=i, color='white', linestyle=':', alpha=0.4)
        
        # Аннотация
        if len(cumulative) > 0:
            ax1.annotate(f'Total: ${cumulative[-1]:.2f}', 
                        xy=(len(cumulative)-1, cumulative[-1]), 
                        xytext=(-60, 10), textcoords='offset points',
                        fontsize=11, fontweight='bold', color='#e74c3c',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#e74c3c'))
        
        # X-axis labels
        step = 12
        ax1.set_xticks(range(0, len(all_hours), step))
        ax1.set_xticklabels([all_hours[i][-5:] if i % 24 != 0 else all_hours[i][5:10] for i in range(0, len(all_hours), step)], 
                          rotation=45, ha='right', fontsize=9)
        
        # График 2: Почасовая стоимость
        ax2.bar(range(len(values)), values, color=bar_colors, alpha=0.7, edgecolor='white', linewidth=0.1)
        if len(values) > 0:
            ax2.axhline(y=np.mean(values), color='yellow', linestyle='--', linewidth=2,
                       label=f'Average: ${np.mean(values):.2f}/hour')
        ax2.set_title('Hourly Cost (Grey=Night, Orange=Weekend)', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Time (UTC+7)', fontsize=12)
        ax2.set_ylabel('Cost ($)', fontsize=12)
        ax2.legend(fontsize=10)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        
        ax2.set_xticks(range(0, len(all_hours), step))
        ax2.set_xticklabels([all_hours[i][-5:] if i % 24 != 0 else all_hours[i][5:10] for i in range(0, len(all_hours), step)], 
                          rotation=45, ha='right', fontsize=9)
        
        plt.tight_layout()
        self.save_figure('cost_timeline_last_week.png')
    
    def create_cost_timeline_last_day(self, ten_min_cost):
        """График 4: Последний день, по 10 минут (144 интервала без пропусков)."""
        print("  └─ График стоимости за последний день (по 10 минут)...")
        
        from datetime import datetime, timedelta
        
        if not ten_min_cost:
            print("     [!] Нет данных о стоимости по 10-минутным интервалам")
            return
        
        # Генерируем 144 интервала по 10 минут
        end_time = datetime.now() + timedelta(hours=7) # UTC+7
        start_time = end_time - timedelta(days=1)
        all_intervals = []
        for i in range(144):
            dt = start_time + timedelta(minutes=(i+1)*10)
            key = dt.strftime('%Y-%m-%d %H:%M')
            bucket = key[:-1] + '0'
            all_intervals.append(bucket)
        
        values = [ten_min_cost.get(t, 0) for t in all_intervals]
        bar_colors = [self._get_bar_color(t, '#9b59b6', night_color='#2c3e50') for t in all_intervals]
        
        # Кумулятивная сумма
        cumulative = []
        total = 0
        for val in values:
            total += val
            cumulative.append(total)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        
        # График 1: Кумулятивная стоимость
        ax1.fill_between(range(len(cumulative)), cumulative, alpha=0.3, color='#9b59b6')
        ax1.plot(range(len(cumulative)), cumulative, color='#9b59b6', linewidth=2, markersize=2)
        ax1.set_title('Cumulative Cost - Last 24 Hours (10-min intervals)', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Total Cost ($)', fontsize=12)
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # Подписи
        if len(cumulative) > 0:
            ax1.annotate(f'${cumulative[-1]:.2f}', 
                       xy=(len(cumulative)-1, cumulative[-1]), 
                       xytext=(5, 10), textcoords='offset points',
                       fontsize=10, fontweight='bold', color='#9b59b6')
        
        # X-axis labels (каждый час = 6 интервалов)
        step = 6
        ax1.set_xticks(range(0, len(all_intervals), step))
        ax1.set_xticklabels([all_intervals[i][-5:] for i in range(0, len(all_intervals), step)], 
                          rotation=45, ha='right', fontsize=8)
        
        # График 2: Стоимость по интервалам
        ax2.bar(range(len(values)), values, color=bar_colors, alpha=0.7, edgecolor='white', linewidth=0.3)
        if len(values) > 0:
            ax2.axhline(y=np.mean(values), color='yellow', linestyle='--', linewidth=2, 
                       label=f'Average: ${np.mean(values):.4f}/10min')
        ax2.set_title('Cost Distribution (10-min intervals, Grey=Night)', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Time', fontsize=12)
        ax2.set_ylabel('Cost ($)', fontsize=12)
        ax2.legend(fontsize=10)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        
        ax2.set_xticks(range(0, len(all_intervals), step))
        ax2.set_xticklabels([all_intervals[i][-5:] for i in range(0, len(all_intervals), step)], 
                          rotation=45, ha='right', fontsize=8)
        
        plt.tight_layout()
        self.save_figure('cost_timeline_last_day.png')
    
    # ========== Графики по моделям ==========
    
    def create_cost_timeline_by_model_all_period(self, all_timestamps, models):
        """График 5: Весь период по моделям, 200 точек."""
        print("  ├─ График по моделям за весь период (200 точек)...")
        
        if not all_timestamps:
            print("     [!] Нет данных")
            return
        
        # Группируем данные в 200 бакетов
        num_buckets = min(200, len(all_timestamps))
        bucket_size = max(1, len(all_timestamps) // num_buckets)
        
        buckets_labels = []
        buckets_data = [] # List of dicts {model: cost}
        
        for i in range(0, len(all_timestamps), bucket_size):
            bucket = all_timestamps[i:i+bucket_size]
            if bucket:
                buckets_labels.append(bucket[0][0].strftime('%Y-%m-%d'))
                model_costs = defaultdict(float)
                for item in bucket:
                    model_costs[item[1]] += item[2]
                buckets_data.append(dict(model_costs))
        
        # Фильтруем данные для выбора топ моделей (используем индексы как ключи для _get_top_models)
        timeframe_data = {i: data for i, data in enumerate(buckets_data)}
        top_model_names = self._get_top_models(timeframe_data, n=10)
        model_colors = self._get_model_colors(top_model_names)
        
        # Собираем данные по моделям для бакетов
        buckets_by_model = {model: [data.get(model, 0) for data in buckets_data] for model in top_model_names}
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        
        # График 1: Stacked area
        ax1.set_title('Cumulative Cost - All Period (By Model, Stacked)', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Cumulative Cost ($)', fontsize=12)
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # Создаем накопительные данные
        cumulative_by_model = {}
        for model in top_model_names:
            cumulative = []
            total = 0
            for val in buckets_by_model[model]:
                total += val
                cumulative.append(total)
            cumulative_by_model[model] = cumulative
        
        # Stacked area
        x_range = range(len(buckets_labels))
        y_stack = np.zeros(len(buckets_labels))
        
        for model in reversed(top_model_names):
            y_values = np.array(cumulative_by_model[model])
            ax1.fill_between(x_range, y_stack, y_stack + y_values, 
                           alpha=0.7, color=model_colors[model], label=model)
            y_stack += y_values
        
        # X-axis labels
        step = max(1, len(buckets_labels) // 10)
        ax1.set_xticks(range(0, len(buckets_labels), step))
        ax1.set_xticklabels([buckets_labels[i] for i in range(0, len(buckets_labels), step)], 
                          rotation=45, ha='right', fontsize=9)
        ax1.legend(fontsize=9, loc='upper left', ncol=2)
        
        # График 2: Stacked bar chart
        ax2.set_title('Cost Distribution (Stacked by Model)', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Time Period', fontsize=12)
        ax2.set_ylabel('Cost ($)', fontsize=12)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        
        bottom = np.zeros(len(buckets_labels))
        for model in top_model_names:
            values = buckets_by_model[model]
            ax2.bar(range(len(values)), values, bottom=bottom, color=model_colors[model], 
                   alpha=0.8, edgecolor='white', linewidth=0.5, label=model)
            bottom += np.array(values)
        
        ax2.set_xticks(range(0, len(buckets_labels), step))
        ax2.set_xticklabels([buckets_labels[i] for i in range(0, len(buckets_labels), step)], 
                          rotation=45, ha='right', fontsize=9)
        ax2.legend(fontsize=9, loc='upper left', ncol=2)
        
        plt.tight_layout()
        self.save_figure('cost_timeline_by_model_all_period.png')
    
    def create_cost_timeline_by_model_last_month(self, daily_cost_by_model, models):
        """График 6: Последний месяц по моделям, по дням (все дни)."""
        print("  ├─ График по моделям за последний месяц...")
        
        from datetime import datetime, timedelta
        
        if not daily_cost_by_model:
            print("     [!] Нет данных")
            return
        
        # Генерируем список последних 30 дней без пропусков
        end_date = datetime.now() + timedelta(hours=7) # UTC+7
        all_days = [(end_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]
        
        # Фильтруем данные для выбора топ моделей
        filtered_data = {day: daily_cost_by_model.get(day, {}) for day in all_days}
        top_model_names = self._get_top_models(filtered_data, n=10)
        model_colors = self._get_model_colors(top_model_names)
        
        # Собираем данные по моделям
        model_daily_values = {}
        for model in top_model_names:
            model_daily_values[model] = [daily_cost_by_model.get(day, {}).get(model, 0) for day in all_days]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        
        # График 1: Stacked area
        ax1.set_title('Cumulative Cost - Last 30 Days (By Model, Stacked)', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Cumulative Cost ($)', fontsize=12)
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # Создаем накопительные данные
        cumulative_by_model = {}
        for model in top_model_names:
            cumulative = []
            total = 0
            for val in model_daily_values[model]:
                total += val
                cumulative.append(total)
            cumulative_by_model[model] = cumulative
        
        # Stacked area
        x_range = range(len(all_days))
        y_stack = np.zeros(len(all_days))
        
        for model in reversed(top_model_names):
            y_values = np.array(cumulative_by_model[model])
            ax1.fill_between(x_range, y_stack, y_stack + y_values, 
                           alpha=0.7, color=model_colors[model], label=model)
            y_stack += y_values
        
        # X-axis labels
        step = 3
        ax1.set_xticks(range(0, len(all_days), step))
        ax1.set_xticklabels([all_days[i] for i in range(0, len(all_days), step)], 
                          rotation=45, ha='right', fontsize=9)
        ax1.legend(fontsize=9, loc='upper left', ncol=2)
        
        # График 2: Stacked bar chart
        ax2.set_title('Daily Cost (Stacked by Model, Highlighting Weekends)', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_ylabel('Cost ($)', fontsize=12)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        
        bottom = np.zeros(len(all_days))
        for model in top_model_names:
            values = model_daily_values[model]
            ax2.bar(range(len(values)), values, bottom=bottom, color=model_colors[model], 
                   alpha=0.8, edgecolor='white', linewidth=0.5, label=model)
            bottom += np.array(values)
        
        # Подсветка выходных на фоне или границах? Удобнее просто добавить текст или вертикальные линии.
        # Пользователь просил цвет баров менять, но тут stacked bars. 
        # Можно добавить вертикальные затененные области.
        for i, day in enumerate(all_days):
            if self._is_weekend(day):
                ax2.axvspan(i-0.5, i+0.5, color='orange', alpha=0.1)
        
        ax2.set_xticks(range(0, len(all_days), step))
        ax2.set_xticklabels([all_days[i] for i in range(0, len(all_days), step)], 
                          rotation=45, ha='right', fontsize=9)
        ax2.legend(fontsize=9, loc='upper left', ncol=2)
        
        plt.tight_layout()
        self.save_figure('cost_timeline_by_model_last_month.png')
    
    def create_cost_timeline_by_model_last_week(self, hourly_cost_by_model_full, models):
        """График 7: Последняя неделя по моделям, по часам (168 часов без пропусков)."""
        print("  ├─ График по моделям за последнюю неделю...")
        
        from datetime import datetime, timedelta
        
        if not hourly_cost_by_model_full:
            print("     [!] Нет данных")
            return
        
        # Генерируем 168 часов (7 дней) без пропусков
        end_time = datetime.now() + timedelta(hours=7) # UTC+7
        start_time = end_time - timedelta(days=7)
        all_hours = []
        for i in range(168):
            dt = start_time + timedelta(hours=i+1)
            all_hours.append(dt.strftime('%Y-%m-%d %H:00'))
        
        # Фильтруем данные для выбора топ моделей
        filtered_data = {t: hourly_cost_by_model_full.get(t, {}) for t in all_hours}
        top_model_names = self._get_top_models(filtered_data, n=10)
        model_colors = self._get_model_colors(top_model_names)
        
        # Собираем данные по моделям
        model_hourly_values = {}
        for model in top_model_names:
            model_hourly_values[model] = [hourly_cost_by_model_full.get(t, {}).get(model, 0) for t in all_hours]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        
        # График 1: Stacked area
        ax1.set_title('Cumulative Cost - Last 7 Days (By Model, Stacked)', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Cumulative Cost ($)', fontsize=12)
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # Создаем накопительные данные
        cumulative_by_model = {}
        for model in top_model_names:
            cumulative = []
            total = 0
            for val in model_hourly_values[model]:
                total += val
                cumulative.append(total)
            cumulative_by_model[model] = cumulative
        
        # Stacked area
        x_range = range(len(all_hours))
        y_stack = np.zeros(len(all_hours))
        
        for model in reversed(top_model_names):
            y_values = np.array(cumulative_by_model[model])
            ax1.fill_between(x_range, y_stack, y_stack + y_values, 
                           alpha=0.7, color=model_colors[model], label=model)
            y_stack += y_values
        
        # Разделители дней (00:00) и вертикальные линии
        for i, t in enumerate(all_hours):
            if ':00' in t and t.endswith(' 00:00'):
                dt = datetime.strptime(t, '%Y-%m-%d %H:00')
                day_name = dt.strftime('%A')
                ax1.axvline(x=i, color='white', linestyle=':', alpha=0.4)
                ax1.text(i, ax1.get_ylim()[1]*0.9, day_name, color='white', rotation=90, alpha=0.6, fontsize=8)
                ax2.axvline(x=i, color='white', linestyle=':', alpha=0.4)
        
        # X-axis labels
        step = 12
        ax1.set_xticks(range(0, len(all_hours), step))
        ax1.set_xticklabels([all_hours[i][-5:] if i % 24 != 0 else all_hours[i][5:10] for i in range(0, len(all_hours), step)], 
                          rotation=45, ha='right', fontsize=9)
        ax1.legend(fontsize=9, loc='upper left', ncol=2)
        
        # График 2: Stacked bar chart
        ax2.set_title('Hourly Cost (Stacked by Model, Grey=Night, Orange=Weekend)', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Time (UTC+7)', fontsize=12)
        ax2.set_ylabel('Cost ($)', fontsize=12)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        
        bottom = np.zeros(len(all_hours))
        for model in top_model_names:
            values = model_hourly_values[model]
            ax2.bar(range(len(all_hours)), values, bottom=bottom, color=model_colors[model], 
                   alpha=0.8, edgecolor='none', linewidth=0, label=model)
            bottom += np.array(values)
        
        # Подсветка ночи и выходных
        for i, t in enumerate(all_hours):
            if self._is_night(t):
                ax2.axvspan(i-0.5, i+0.5, color='grey', alpha=0.1)
            if self._is_weekend(t):
                ax2.axvspan(i-0.5, i+0.5, color='orange', alpha=0.05)
        
        ax2.set_xticks(range(0, len(all_hours), step))
        ax2.set_xticklabels([all_hours[i][-5:] if i % 24 != 0 else all_hours[i][5:10] for i in range(0, len(all_hours), step)], 
                          rotation=45, ha='right', fontsize=9)
        ax2.legend(fontsize=9, loc='upper left', ncol=2)
        
        plt.tight_layout()
        self.save_figure('cost_timeline_by_model_last_week.png')
    
    def create_cost_timeline_by_model_last_day(self, ten_min_cost_by_model, models):
        """График 8: Последний день по моделям, по 10 минут (144 интервала без пропусков)."""
        print("  └─ График по моделям за последний день...")
        
        from datetime import datetime, timedelta
        
        if not ten_min_cost_by_model:
            print("     [!] Нет данных")
            return
        
        # Генерируем 144 интервала по 10 минут
        end_time = datetime.now() + timedelta(hours=7) # UTC+7
        start_time = end_time - timedelta(days=1)
        all_intervals = []
        for i in range(144):
            dt = start_time + timedelta(minutes=(i+1)*10)
            key = dt.strftime('%Y-%m-%d %H:%M')
            bucket = key[:-1] + '0'
            all_intervals.append(bucket)
        
        # Фильтруем данные для выбора топ моделей
        filtered_data = {t: ten_min_cost_by_model.get(t, {}) for t in all_intervals}
        top_model_names = self._get_top_models(filtered_data, n=10)
        model_colors = self._get_model_colors(top_model_names)
        
        # Собираем данные по моделям
        model_values = {}
        for model in top_model_names:
            model_values[model] = [ten_min_cost_by_model.get(t, {}).get(model, 0) for t in all_intervals]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        
        # График 1: Stacked area
        ax1.set_title('Cumulative Cost - Last 24 Hours (By Model, Stacked)', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Cumulative Cost ($)', fontsize=12)
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # Создаем накопительные данные
        cumulative_by_model = {}
        for model in top_model_names:
            cumulative = []
            total = 0
            for val in model_values[model]:
                total += val
                cumulative.append(total)
            cumulative_by_model[model] = cumulative
        
        # Stacked area
        x_range = range(len(all_intervals))
        y_stack = np.zeros(len(all_intervals))
        
        for model in reversed(top_model_names):
            y_values = np.array(cumulative_by_model[model])
            ax1.fill_between(x_range, y_stack, y_stack + y_values, 
                           alpha=0.7, color=model_colors[model], label=model)
            y_stack += y_values
        
        # X-axis labels
        step = 6
        ax1.set_xticks(range(0, len(all_intervals), step))
        ax1.set_xticklabels([all_intervals[i][-5:] for i in range(0, len(all_intervals), step)], 
                          rotation=45, ha='right', fontsize=8)
        ax1.legend(fontsize=9, loc='upper left', ncol=2)
        
        # График 2: Stacked bar chart
        ax2.set_title('Cost Distribution (10-min intervals, Stacked by Model, Grey=Night)', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Time', fontsize=12)
        ax2.set_ylabel('Cost ($)', fontsize=12)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        
        bottom = np.zeros(len(all_intervals))
        for model in top_model_names:
            values = model_values[model]
            ax2.bar(range(len(all_intervals)), values, bottom=bottom, color=model_colors[model], 
                   alpha=0.8, edgecolor='none', linewidth=0, label=model)
            bottom += np.array(values)
        
        # Подсветка ночи
        for i, t in enumerate(all_intervals):
            if self._is_night(t):
                ax2.axvspan(i-0.5, i+0.5, color='grey', alpha=0.1)
        
        ax2.set_xticks(range(0, len(all_intervals), step))
        ax2.set_xticklabels([all_intervals[i][-5:] for i in range(0, len(all_intervals), step)], 
                          rotation=45, ha='right', fontsize=8)
        ax2.legend(fontsize=9, loc='upper left', ncol=2)
        
        plt.tight_layout()
        self.save_figure('cost_timeline_by_model_last_day.png')

    # ========== Графики запросов (аналогично стоимости) ==========

    def create_request_timeline_all_period(self, all_timestamps):
        """График 9: Количество запросов за весь период, 200 точек."""
        print("  ├─ График запросов за весь период (200 точек)...")
        if not all_timestamps: return
        num_buckets = min(200, len(all_timestamps))
        bucket_size = max(1, len(all_timestamps) // num_buckets)
        buckets_req = []
        buckets_labels = []
        for i in range(0, len(all_timestamps), bucket_size):
            bucket = all_timestamps[i:i+bucket_size]
            if bucket:
                buckets_req.append(len(bucket))
                buckets_labels.append(bucket[0][0].strftime('%Y-%m-%d'))
        
        cumulative = []
        total = 0
        for val in buckets_req:
            total += val
            cumulative.append(total)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        ax1.fill_between(range(len(cumulative)), cumulative, alpha=0.3, color='#2ecc71')
        ax1.plot(range(len(cumulative)), cumulative, color='#2ecc71', linewidth=2.5, marker='o', markersize=3)
        ax1.set_title('Cumulative Requests - All Period (200 points)', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Total Requests', fontsize=12)
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        step = max(1, len(buckets_labels) // 10)
        ax1.set_xticks(range(0, len(buckets_labels), step))
        ax1.set_xticklabels([buckets_labels[i] for i in range(0, len(buckets_labels), step)], rotation=45, ha='right', fontsize=9)
        
        colors = [self._get_bar_color(l, '#3498db') for l in buckets_labels]
        ax2.bar(range(len(buckets_req)), buckets_req, color=colors, alpha=0.8, edgecolor='white', linewidth=0.5)
        ax2.set_title('Requests Distribution', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Time Period', fontsize=12)
        ax2.set_ylabel('Requests Count', fontsize=12)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        
        ax2.set_xticks(range(0, len(buckets_labels), step))
        ax2.set_xticklabels([buckets_labels[i] for i in range(0, len(buckets_labels), step)], rotation=45, ha='right', fontsize=9)
        
        plt.tight_layout()
        self.save_figure('request_timeline_all_period.png')

    def create_request_timeline_last_month(self, daily_usage):
        """График 10: Количество запросов за месяц, по дням."""
        print("  ├─ График запросов за последний месяц (по дням)...")
        from datetime import datetime, timedelta
        if not daily_usage: return
        end_date = datetime.now() + timedelta(hours=7)
        all_days = [(end_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]
        
        daily_req = []
        bar_colors = []
        for day in all_days:
            count = sum(daily_usage.get(day, {}).values())
            daily_req.append(count)
            bar_colors.append(self._get_bar_color(day, '#3498db', weekend_color='#e67e22'))
            
        cumulative = []
        total = 0
        for val in daily_req:
            total += val
            cumulative.append(total)
            
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        ax1.fill_between(range(len(cumulative)), cumulative, alpha=0.3, color='#3498db')
        ax1.plot(range(len(cumulative)), cumulative, color='#3498db', linewidth=2.5, marker='o', markersize=4)
        ax1.set_title('Cumulative Requests - Last 30 Days', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Total Requests', fontsize=12)
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        step = 3
        ax1.set_xticks(range(0, len(all_days), step))
        ax1.set_xticklabels([all_days[i] for i in range(0, len(all_days), step)], rotation=45, ha='right', fontsize=9)
        
        ax2.bar(range(len(daily_req)), daily_req, color=bar_colors, alpha=0.8, edgecolor='white', linewidth=0.5)
        ax2.set_title('Daily Requests (Orange = Weekend)', fontsize=16, fontweight='bold')
        ax2.set_ylabel('Requests', fontsize=12)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        ax2.set_xticks(range(0, len(all_days), step))
        ax2.set_xticklabels([all_days[i] for i in range(0, len(all_days), step)], rotation=45, ha='right', fontsize=9)
        
        plt.tight_layout()
        self.save_figure('request_timeline_last_month.png')

    def create_request_timeline_last_week(self, hourly_requests_full):
        """График 11: Количество запросов за неделю, по часам."""
        print("  ├─ График запросов за последнюю неделю (по часам)...")
        from datetime import datetime, timedelta
        if not hourly_requests_full: return
        end_time = datetime.now() + timedelta(hours=7)
        start_time = end_time - timedelta(days=7)
        all_hours = [(start_time + timedelta(hours=i+1)).strftime('%Y-%m-%d %H:00') for i in range(168)]
        
        req_values = [hourly_requests_full.get(t, 0) for t in all_hours]
        bar_colors = [self._get_bar_color(t, '#e74c3c', night_color='#2c3e50', weekend_color='#e67e22') for t in all_hours]
        
        cumulative = []
        total = 0
        for val in req_values:
            total += val
            cumulative.append(total)
            
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        ax1.fill_between(range(len(cumulative)), cumulative, alpha=0.3, color='#e74c3c')
        ax1.plot(range(len(cumulative)), cumulative, color='#e74c3c', linewidth=2, markersize=2)
        ax1.set_title('Cumulative Requests - Last 7 Days', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Total Requests', fontsize=12)
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        for i, t in enumerate(all_hours):
            if t.endswith(' 00:00'):
                dt = datetime.strptime(t, '%Y-%m-%d %H:00')
                ax1.axvline(x=i, color='white', linestyle=':', alpha=0.4)
                ax1.text(i, ax1.get_ylim()[1]*0.9, dt.strftime('%A'), color='white', rotation=90, alpha=0.6, fontsize=8)
                ax2.axvline(x=i, color='white', linestyle=':', alpha=0.4)
        
        step = 12
        ax1.set_xticks(range(0, len(all_hours), step))
        ax1.set_xticklabels([all_hours[i][-5:] if i % 24 != 0 else all_hours[i][5:10] for i in range(0, len(all_hours), step)], rotation=45, ha='right', fontsize=9)
        
        ax2.bar(range(len(req_values)), req_values, color=bar_colors, alpha=0.7, edgecolor='none', linewidth=0)
        ax2.set_title('Hourly Requests (Grey=Night, Orange=Weekend)', fontsize=16, fontweight='bold')
        ax2.set_ylabel('Requests', fontsize=12)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        ax2.set_xticks(range(0, len(all_hours), step))
        ax2.set_xticklabels([all_hours[i][-5:] if i % 24 != 0 else all_hours[i][5:10] for i in range(0, len(all_hours), step)], rotation=45, ha='right', fontsize=9)
        
        plt.tight_layout()
        self.save_figure('request_timeline_last_week.png')

    def create_request_timeline_last_day(self, ten_min_requests):
        """График 12: Количество запросов за день, по 10 минут."""
        print("  ├─ График запросов за последний день (по 10 минут)...")
        from datetime import datetime, timedelta
        if not ten_min_requests: return
        end_time = datetime.now() + timedelta(hours=7)
        start_time = end_time - timedelta(days=1)
        all_intervals = [((start_time + timedelta(minutes=(i+1)*10)).strftime('%Y-%m-%d %H:%M'))[:-1] + '0' for i in range(144)]
        
        req_values = [ten_min_requests.get(t, 0) for t in all_intervals]
        bar_colors = [self._get_bar_color(t, '#9b59b6', night_color='#2c3e50') for t in all_intervals]
        
        cumulative = []
        total = 0
        for val in req_values:
            total += val
            cumulative.append(total)
            
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        ax1.fill_between(range(len(cumulative)), cumulative, alpha=0.3, color='#9b59b6')
        ax1.plot(range(len(cumulative)), cumulative, color='#9b59b6', linewidth=2, markersize=2)
        ax1.set_title('Cumulative Requests - Last 24 Hours (10-min intervals)', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Total Requests', fontsize=12)
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        step = 6
        ax1.set_xticks(range(0, len(all_intervals), step))
        ax1.set_xticklabels([all_intervals[i][-5:] for i in range(0, len(all_intervals), step)], rotation=45, ha='right', fontsize=8)
        
        ax2.bar(range(len(req_values)), req_values, color=bar_colors, alpha=0.7, edgecolor='none', linewidth=0)
        ax2.set_title('Requests Distribution (10-min intervals, Grey=Night)', fontsize=16, fontweight='bold')
        ax2.set_ylabel('Requests', fontsize=12)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        ax2.set_xticks(range(0, len(all_intervals), step))
        ax2.set_xticklabels([all_intervals[i][-5:] for i in range(0, len(all_intervals), step)], rotation=45, ha='right', fontsize=8)
        
        plt.tight_layout()
        self.save_figure('request_timeline_last_day.png')

    def create_request_timeline_by_model_all_period(self, all_timestamps, models):
        """График 13: Запросы за весь период по моделям."""
        print("  ├─ График запросов по моделям за весь период...")
        if not all_timestamps: return
        num_buckets = min(200, len(all_timestamps))
        bucket_size = max(1, len(all_timestamps) // num_buckets)
        buckets_data = []
        buckets_labels = []
        for i in range(0, len(all_timestamps), bucket_size):
            bucket = all_timestamps[i:i+bucket_size]
            if bucket:
                buckets_labels.append(bucket[0][0].strftime('%Y-%m-%d'))
                counts = defaultdict(int)
                for item in bucket: counts[item[1]] += 1
                buckets_data.append(dict(counts))
        
        timeframe_data = {i: data for i, data in enumerate(buckets_data)}
        top_model_names = self._get_top_models(timeframe_data, n=10)
        model_colors = self._get_model_colors(top_model_names)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        ax1.set_title('Cumulative Requests - All Period (By Model, Stacked)', fontsize=16, fontweight='bold')
        
        y_stack = np.zeros(len(buckets_data))
        for model in reversed(top_model_names):
            y_values = []
            total = 0
            for data in buckets_data:
                total += data.get(model, 0)
                y_values.append(total)
            ax1.fill_between(range(len(buckets_data)), y_stack, y_stack + np.array(y_values), alpha=0.7, color=model_colors[model], label=model)
            y_stack += np.array(y_values)
        
        step = max(1, len(buckets_labels) // 10)
        ax1.set_xticks(range(0, len(buckets_labels), step))
        ax1.set_xticklabels([buckets_labels[i] for i in range(0, len(buckets_labels), step)], rotation=45, ha='right', fontsize=9)
        ax1.legend(fontsize=9, loc='upper left', ncol=2)
        
        bottom = np.zeros(len(buckets_data))
        for model in top_model_names:
            values = [data.get(model, 0) for data in buckets_data]
            ax2.bar(range(len(buckets_data)), values, bottom=bottom, color=model_colors[model], alpha=0.8, label=model)
            bottom += np.array(values)
        
        ax2.set_xticks(range(0, len(buckets_labels), step))
        ax2.set_xticklabels([buckets_labels[i] for i in range(0, len(buckets_labels), step)], rotation=45, ha='right', fontsize=9)
        plt.tight_layout()
        self.save_figure('request_timeline_by_model_all_period.png')

    def create_request_timeline_by_model_last_month(self, daily_usage, models):
        """График 14: Запросы за месяц по моделям."""
        print("  ├─ График запросов по моделям за последний месяц...")
        from datetime import datetime, timedelta
        if not daily_usage: return
        end_date = datetime.now() + timedelta(hours=7)
        all_days = [(end_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]
        
        filtered_data = {day: daily_usage.get(day, {}) for day in all_days}
        top_model_names = self._get_top_models(filtered_data, n=10)
        model_colors = self._get_model_colors(top_model_names)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        ax1.set_title('Cumulative Requests - Last 30 Days (By Model, Stacked)', fontsize=16, fontweight='bold')
        
        y_stack = np.zeros(len(all_days))
        for model in reversed(top_model_names):
            y_values = []
            total = 0
            for day in all_days:
                total += daily_usage.get(day, {}).get(model, 0)
                y_values.append(total)
            ax1.fill_between(range(len(all_days)), y_stack, y_stack + np.array(y_values), alpha=0.7, color=model_colors[model], label=model)
            y_stack += np.array(y_values)
            
        step = 3
        ax1.set_xticks(range(0, len(all_days), step))
        ax1.set_xticklabels([all_days[i] for i in range(0, len(all_days), step)], rotation=45, ha='right', fontsize=9)
        ax1.legend(fontsize=9, loc='upper left', ncol=2)
        
        bottom = np.zeros(len(all_days))
        for model in top_model_names:
            values = [daily_usage.get(day, {}).get(model, 0) for day in all_days]
            ax2.bar(range(len(all_days)), values, bottom=bottom, color=model_colors[model], alpha=0.8, label=model)
            bottom += np.array(values)
            
        for i, day in enumerate(all_days):
            if self._is_weekend(day): ax2.axvspan(i-0.5, i+0.5, color='orange', alpha=0.1)
            
        ax2.set_xticks(range(0, len(all_days), step))
        ax2.set_xticklabels([all_days[i] for i in range(0, len(all_days), step)], rotation=45, ha='right', fontsize=9)
        plt.tight_layout()
        self.save_figure('request_timeline_by_model_last_month.png')

    def create_request_timeline_by_model_last_week(self, hourly_requests_by_model_full, models):
        """График 15: Запросы за неделю по моделям."""
        print("  ├─ График запросов по моделям за последнюю неделю...")
        from datetime import datetime, timedelta
        if not hourly_requests_by_model_full: return
        end_time = datetime.now() + timedelta(hours=7)
        start_time = end_time - timedelta(days=7)
        all_hours = [(start_time + timedelta(hours=i+1)).strftime('%Y-%m-%d %H:00') for i in range(168)]
        
        filtered_data = {t: hourly_requests_by_model_full.get(t, {}) for t in all_hours}
        top_model_names = self._get_top_models(filtered_data, n=10)
        model_colors = self._get_model_colors(top_model_names)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        ax1.set_title('Cumulative Requests - Last 7 Days (By Model, Stacked)', fontsize=16, fontweight='bold')
        
        y_stack = np.zeros(len(all_hours))
        for model in reversed(top_model_names):
            y_values = []
            total = 0
            for t in all_hours:
                total += hourly_requests_by_model_full.get(t, {}).get(model, 0)
                y_values.append(total)
            ax1.fill_between(range(len(all_hours)), y_stack, y_stack + np.array(y_values), alpha=0.7, color=model_colors[model], label=model)
            y_stack += np.array(y_values)
            
        for i, t in enumerate(all_hours):
            if t.endswith(' 00:00'):
                dt = datetime.strptime(t, '%Y-%m-%d %H:00')
                ax1.axvline(x=i, color='white', linestyle=':', alpha=0.4)
                ax1.text(i, ax1.get_ylim()[1]*0.9, dt.strftime('%A'), color='white', rotation=90, alpha=0.6, fontsize=8)
                ax2.axvline(x=i, color='white', linestyle=':', alpha=0.4)
                
        step = 12
        ax1.set_xticks(range(0, len(all_hours), step))
        ax1.set_xticklabels([all_hours[i][-5:] if i % 24 != 0 else all_hours[i][5:10] for i in range(0, len(all_hours), step)], rotation=45, ha='right', fontsize=9)
        ax1.legend(fontsize=9, loc='upper left', ncol=2)
        
        bottom = np.zeros(len(all_hours))
        for model in top_model_names:
            values = [hourly_requests_by_model_full.get(t, {}).get(model, 0) for t in all_hours]
            ax2.bar(range(len(all_hours)), values, bottom=bottom, color=model_colors[model], alpha=0.8, edgecolor='none', label=model)
            bottom += np.array(values)
            
        for i, t in enumerate(all_hours):
            if self._is_night(t): ax2.axvspan(i-0.5, i+0.5, color='grey', alpha=0.1)
            if self._is_weekend(t): ax2.axvspan(i-0.5, i+0.5, color='orange', alpha=0.05)
            
        ax2.set_xticks(range(0, len(all_hours), step))
        ax2.set_xticklabels([all_hours[i][-5:] if i % 24 != 0 else all_hours[i][5:10] for i in range(0, len(all_hours), step)], rotation=45, ha='right', fontsize=9)
        plt.tight_layout()
        self.save_figure('request_timeline_by_model_last_week.png')

    def create_request_timeline_by_model_last_day(self, ten_min_requests_by_model, models):
        """График 16: Запросы за день по моделям."""
        print("  ├─ График запросов по моделям за последний день...")
        from datetime import datetime, timedelta
        if not ten_min_requests_by_model: return
        end_time = datetime.now() + timedelta(hours=7)
        start_time = end_time - timedelta(days=1)
        all_intervals = [((start_time + timedelta(minutes=(i+1)*10)).strftime('%Y-%m-%d %H:%M'))[:-1] + '0' for i in range(144)]
        
        filtered_data = {t: ten_min_requests_by_model.get(t, {}) for t in all_intervals}
        top_model_names = self._get_top_models(filtered_data, n=10)
        model_colors = self._get_model_colors(top_model_names)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        ax1.set_title('Cumulative Requests - Last 24 Hours (By Model, Stacked)', fontsize=16, fontweight='bold')
        
        y_stack = np.zeros(len(all_intervals))
        for model in reversed(top_model_names):
            y_values = []
            total = 0
            for t in all_intervals:
                total += ten_min_requests_by_model.get(t, {}).get(model, 0)
                y_values.append(total)
            ax1.fill_between(range(len(all_intervals)), y_stack, y_stack + np.array(y_values), alpha=0.7, color=model_colors[model], label=model)
            y_stack += np.array(y_values)
            
        step = 6
        ax1.set_xticks(range(0, len(all_intervals), step))
        ax1.set_xticklabels([all_intervals[i][-5:] for i in range(0, len(all_intervals), step)], rotation=45, ha='right', fontsize=8)
        ax1.legend(fontsize=9, loc='upper left', ncol=2)
        
        bottom = np.zeros(len(all_intervals))
        for model in top_model_names:
            values = [ten_min_requests_by_model.get(t, {}).get(model, 0) for t in all_intervals]
            ax2.bar(range(len(all_intervals)), values, bottom=bottom, color=model_colors[model], alpha=0.8, edgecolor='none', label=model)
            bottom += np.array(values)
            
        for i, t in enumerate(all_intervals):
            if self._is_night(t): ax2.axvspan(i-0.5, i+0.5, color='grey', alpha=0.1)
            
        ax2.set_xticks(range(0, len(all_intervals), step))
        ax2.set_xticklabels([all_intervals[i][-5:] for i in range(0, len(all_intervals), step)], rotation=45, ha='right', fontsize=8)
        plt.tight_layout()
        self.save_figure('request_timeline_by_model_last_day.png')




