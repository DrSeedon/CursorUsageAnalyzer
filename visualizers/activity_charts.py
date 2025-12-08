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
    
    def create_cumulative_cost_daily(self, daily_cost):
        """Создает график накопительной стоимости по дням."""
        print("  ├─ Накопительная стоимость по дням...")
        
        if not daily_cost:
            print("     [!] Нет данных о стоимости по дням")
            return
        
        # Сортируем по дате
        sorted_days = sorted(daily_cost.keys())
        daily_values = [daily_cost[day] for day in sorted_days]
        
        # Накопительная сумма
        cumulative = []
        total = 0
        for val in daily_values:
            total += val
            cumulative.append(total)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        
        # График 1: Накопительная стоимость
        ax1.fill_between(range(len(sorted_days)), cumulative, alpha=0.3, color='#2ecc71')
        ax1.plot(range(len(sorted_days)), cumulative, color='#2ecc71', linewidth=3, marker='o', markersize=4)
        ax1.set_title('Cumulative Cost Over Time', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Total Cost ($)', fontsize=12)
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # Подписи на графике
        for i in [0, len(cumulative)//4, len(cumulative)//2, 3*len(cumulative)//4, -1]:
            if i < len(cumulative):
                ax1.annotate(f'${cumulative[i]:.2f}', 
                           xy=(i, cumulative[i]), 
                           xytext=(5, 10), textcoords='offset points',
                           fontsize=9, fontweight='bold', color='#2ecc71')
        
        # X-axis labels
        step = max(1, len(sorted_days) // 10)
        ax1.set_xticks(range(0, len(sorted_days), step))
        ax1.set_xticklabels([sorted_days[i] for i in range(0, len(sorted_days), step)], 
                          rotation=45, ha='right', fontsize=9)
        
        # График 2: Дневная стоимость (bar chart)
        colors = ['#e74c3c' if v > np.mean(daily_values) else '#3498db' for v in daily_values]
        ax2.bar(range(len(sorted_days)), daily_values, color=colors, alpha=0.8, edgecolor='white', linewidth=0.5)
        ax2.axhline(y=np.mean(daily_values), color='yellow', linestyle='--', linewidth=2, 
                   label=f'Average: ${np.mean(daily_values):.2f}/day')
        ax2.set_title('Daily Cost', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_ylabel('Cost ($)', fontsize=12)
        ax2.legend(fontsize=10)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        
        ax2.set_xticks(range(0, len(sorted_days), step))
        ax2.set_xticklabels([sorted_days[i] for i in range(0, len(sorted_days), step)], 
                          rotation=45, ha='right', fontsize=9)
        
        plt.tight_layout()
        self.save_figure('cumulative_cost_daily.png')
    
    def create_cumulative_cost_hourly(self, hourly_cost):
        """Создает график накопительной стоимости по часам."""
        print("  └─ Накопительная стоимость по часам...")
        
        if not hourly_cost:
            print("     [!] Нет данных о стоимости по часам")
            return
        
        # Заполняем все 24 часа (даже если нет данных)
        hours = list(range(24))
        hourly_values = [hourly_cost.get(h, 0) for h in hours]
        
        # Накопительная сумма
        cumulative = []
        total = 0
        for val in hourly_values:
            total += val
            cumulative.append(total)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        
        # Цвета для разных периодов дня
        hour_colors = []
        for h in hours:
            if 6 <= h < 12:
                hour_colors.append('#f1c40f')  # Утро - желтый
            elif 12 <= h < 18:
                hour_colors.append('#e67e22')  # День - оранжевый
            elif 18 <= h < 22:
                hour_colors.append('#9b59b6')  # Вечер - фиолетовый
            else:
                hour_colors.append('#34495e')  # Ночь - серый
        
        # График 1: Накопительная стоимость по часам
        ax1.fill_between(hours, cumulative, alpha=0.3, color='#e74c3c')
        ax1.plot(hours, cumulative, color='#e74c3c', linewidth=3, marker='o', markersize=6)
        ax1.set_title('Cumulative Cost by Hour of Day (Total Across All Days)', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Total Cost ($)', fontsize=12)
        ax1.set_xticks(hours)
        ax1.set_xticklabels([f'{h:02d}:00' for h in hours], rotation=45, ha='right', fontsize=9)
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # Аннотации
        ax1.annotate(f'Total: ${cumulative[-1]:.2f}', 
                    xy=(23, cumulative[-1]), 
                    xytext=(-50, 10), textcoords='offset points',
                    fontsize=11, fontweight='bold', color='#e74c3c',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#e74c3c'))
        
        # График 2: Стоимость по часам (bar chart)
        bars = ax2.bar(hours, hourly_values, color=hour_colors, alpha=0.8, edgecolor='white', linewidth=1)
        ax2.axhline(y=np.mean(hourly_values), color='red', linestyle='--', linewidth=2,
                   label=f'Average: ${np.mean(hourly_values):.2f}/hour')
        ax2.set_title('Cost Distribution by Hour of Day', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Hour (UTC+7)', fontsize=12)
        ax2.set_ylabel('Total Cost ($)', fontsize=12)
        ax2.set_xticks(hours)
        ax2.set_xticklabels([f'{h:02d}' for h in hours], fontsize=10)
        ax2.legend(fontsize=10)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Легенда периодов дня
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#f1c40f', label='Morning (6-12)'),
            Patch(facecolor='#e67e22', label='Afternoon (12-18)'),
            Patch(facecolor='#9b59b6', label='Evening (18-22)'),
            Patch(facecolor='#34495e', label='Night (22-6)')
        ]
        ax2.legend(handles=legend_elements, loc='upper right', fontsize=9)
        
        plt.tight_layout()
        self.save_figure('cumulative_cost_hourly.png')

