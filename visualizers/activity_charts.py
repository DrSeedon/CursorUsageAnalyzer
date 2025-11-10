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

