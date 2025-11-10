"""Визуализатор графиков для моделей."""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from .base_visualizer import BaseVisualizer


class ModelChartsVisualizer(BaseVisualizer):
    """Класс для создания графиков по моделям."""
    
    def create_models_overview(self, models):
        """Создает обзорный график распределения запросов и стоимости."""
        print("  ├─ Обзор моделей...")
        model_names = list(models.keys())
        costs = [m['included_cost'] + m['on_demand_cost'] for m in models.values()]
        total_requests = [m['included_requests'] + m['on_demand_requests'] for m in models.values()]
        
        # Создаем единую цветовую схему для всех моделей
        all_colors = plt.cm.tab20(np.linspace(0, 1, len(model_names)))
        color_map = {model_names[i]: all_colors[i] for i in range(len(model_names))}
        
        # Сортировка по запросам
        sorted_indices_requests = sorted(range(len(model_names)), key=lambda i: total_requests[i], reverse=True)
        model_names_requests = [model_names[i] for i in sorted_indices_requests]
        total_requests_sorted = [total_requests[i] for i in sorted_indices_requests]
        colors_requests = [color_map[name] for name in model_names_requests]
        
        # Сортировка по стоимости
        sorted_indices_costs = sorted(range(len(model_names)), key=lambda i: costs[i], reverse=True)
        model_names_costs = [model_names[i] for i in sorted_indices_costs]
        costs_sorted = [costs[i] for i in sorted_indices_costs]
        colors_costs = [color_map[name] for name in model_names_costs]
        
        # Средняя стоимость на запрос
        cost_per_request = []
        for i in range(len(model_names)):
            total_cost = costs[i]
            total_reqs = total_requests[i]
            avg_cost = (total_cost / total_reqs) if total_reqs > 0 else 0
            cost_per_request.append(avg_cost)
        
        sorted_indices_avg = sorted(range(len(model_names)), key=lambda i: cost_per_request[i], reverse=True)
        model_names_avg = [model_names[i] for i in sorted_indices_avg]
        cost_per_request_sorted = [cost_per_request[i] for i in sorted_indices_avg]
        colors_avg = [color_map[name] for name in model_names_avg]
        
        # Создаем 3x2 сетку
        fig = plt.figure(figsize=(20, 22))
        gs = fig.add_gridspec(3, 3, width_ratios=[1, 1, 0.3], hspace=0.35, wspace=0.3)
        
        ax1 = fig.add_subplot(gs[0, 0])  # Верхний левый - pie по запросам
        ax2 = fig.add_subplot(gs[0, 1])  # Верхний правый - bar по запросам
        ax3 = fig.add_subplot(gs[1, 0])  # Средний левый - pie по цене
        ax4 = fig.add_subplot(gs[1, 1])  # Средний правый - bar по цене
        ax5 = fig.add_subplot(gs[2, 0])  # Нижний левый - pie по avg cost
        ax6 = fig.add_subplot(gs[2, 1])  # Нижний правый - bar по avg cost
        
        # ВЕРХНИЙ РЯД - ЗАПРОСЫ
        # Pie chart - запросы
        wedges1, texts1, autotexts1 = ax1.pie(
            total_requests_sorted, labels=None, autopct='%1.1f%%',
            colors=colors_requests, startangle=90, pctdistance=1.15,
            textprops={'color': 'white', 'weight': 'bold', 'fontsize': 10}
        )
        for autotext in autotexts1:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_weight('bold')
        ax1.set_title('Request Distribution', fontsize=14, fontweight='bold', pad=20)
        
        # Bar chart - запросы
        bars1 = ax2.bar(range(len(model_names_requests)), total_requests_sorted, 
                       color=colors_requests, alpha=0.8, edgecolor='white', linewidth=1.5)
        ax2.set_title('Requests by Models', fontsize=14, fontweight='bold', pad=20)
        ax2.set_ylabel('Number of Requests', fontsize=11)
        ax2.set_xticks(range(len(model_names_requests)))
        ax2.set_xticklabels(model_names_requests, rotation=45, ha='right', fontsize=9)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        
        for bar, count in zip(bars1, total_requests_sorted):
            if count > 0:
                ax2.annotate(f'{int(count)}',
                           xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                           xytext=(0, 3), textcoords="offset points",
                           ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # НИЖНИЙ РЯД - СТОИМОСТЬ
        # Pie chart - стоимость
        wedges2, texts2, autotexts2 = ax3.pie(
            costs_sorted, labels=None, autopct='%1.1f%%',
            colors=colors_costs, startangle=90, pctdistance=1.15,
            textprops={'color': 'white', 'weight': 'bold', 'fontsize': 10}
        )
        for autotext in autotexts2:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_weight('bold')
        ax3.set_title('Cost Distribution', fontsize=14, fontweight='bold', pad=20)
        
        # Bar chart - стоимость
        bars2 = ax4.bar(range(len(model_names_costs)), costs_sorted,
                       color=colors_costs, alpha=0.8, edgecolor='white', linewidth=1.5)
        ax4.set_title('Cost by Models ($)', fontsize=14, fontweight='bold', pad=20)
        ax4.set_ylabel('Cost ($)', fontsize=11)
        ax4.set_xticks(range(len(model_names_costs)))
        ax4.set_xticklabels(model_names_costs, rotation=45, ha='right', fontsize=9)
        ax4.grid(axis='y', alpha=0.3, linestyle='--')
        
        for bar, cost in zip(bars2, costs_sorted):
            if cost > 0:
                ax4.annotate(f'${cost:.1f}',
                           xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                           xytext=(0, 3), textcoords="offset points",
                           ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # НИЖНИЙ РЯД - СРЕДНЯЯ СТОИМОСТЬ НА ЗАПРОС
        # Pie chart - avg cost per request
        wedges3, texts3, autotexts3 = ax5.pie(
            cost_per_request_sorted, labels=None, autopct='%1.1f%%',
            colors=colors_avg, startangle=90, pctdistance=1.15,
            textprops={'color': 'white', 'weight': 'bold', 'fontsize': 10}
        )
        for autotext in autotexts3:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_weight('bold')
        ax5.set_title('Avg Cost Per Request Distribution', fontsize=14, fontweight='bold', pad=20)
        
        # Bar chart - avg cost per request
        bars3 = ax6.bar(range(len(model_names_avg)), cost_per_request_sorted,
                       color=colors_avg, alpha=0.8, edgecolor='white', linewidth=1.5)
        ax6.set_title('Avg Cost Per Request by Models ($)', fontsize=14, fontweight='bold', pad=20)
        ax6.set_ylabel('Cost per Request ($)', fontsize=11)
        ax6.set_xticks(range(len(model_names_avg)))
        ax6.set_xticklabels(model_names_avg, rotation=45, ha='right', fontsize=9)
        ax6.grid(axis='y', alpha=0.3, linestyle='--')
        
        for bar, avg_cost in zip(bars3, cost_per_request_sorted):
            if avg_cost > 0:
                ax6.annotate(f'${avg_cost:.3f}',
                           xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                           xytext=(0, 3), textcoords="offset points",
                           ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # ЛЕГЕНДА ПО ЦЕНТРУ (используем модели отсортированные по запросам)
        fig.legend(wedges1, model_names_requests, loc='center', bbox_to_anchor=(0.85, 0.5),
                  fontsize=10, frameon=False, title='Models', title_fontsize=12)
        
        self.save_figure('models_overview.png')
    
    def create_included_vs_ondemand(self, models):
        """Создает график сравнения Included vs On-Demand."""
        print("  ├─ Included vs On-Demand...")
        model_names = list(models.keys())
        costs = [m['included_cost'] + m['on_demand_cost'] for m in models.values()]
        
        sorted_indices = sorted(range(len(model_names)), key=lambda i: costs[i], reverse=True)
        model_names_sorted = [model_names[i] for i in sorted_indices]
        
        included_reqs = [models[model_names[i]]['included_requests'] for i in sorted_indices]
        on_demand_reqs = [models[model_names[i]]['on_demand_requests'] for i in sorted_indices]
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        x = np.arange(len(model_names_sorted))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, included_reqs, width, label='Included', 
                       color='#2ecc71', alpha=0.85, edgecolor='white', linewidth=1)
        bars2 = ax.bar(x + width/2, on_demand_reqs, width, label='On-Demand', 
                       color='#e74c3c', alpha=0.85, edgecolor='white', linewidth=1)
        
        ax.set_title('Included vs On-Demand', fontsize=16, fontweight='bold')
        ax.set_xlabel('Models', fontsize=12)
        ax.set_ylabel('Number of Requests', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(model_names_sorted, rotation=45, ha='right', fontsize=10)
        ax.legend(fontsize=11)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Добавляем числа на бары
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.annotate(f'{int(height)}',
                               xy=(bar.get_x() + bar.get_width() / 2, height),
                               xytext=(0, 3), textcoords="offset points",
                               ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        self.save_figure('included_vs_ondemand.png')
    
    def create_tokens_detailed(self, models):
        """Создает детальный график по токенам."""
        print("  ├─ Детальная статистика токенов...")
        model_names = list(models.keys())
        costs = [m['included_cost'] + m['on_demand_cost'] for m in models.values()]
        
        sorted_indices = sorted(range(len(model_names)), key=lambda i: costs[i], reverse=True)
        model_names_sorted = [model_names[i] for i in sorted_indices]
        
        input_tokens = [models[model_names[i]]['input_tokens'] for i in sorted_indices]
        output_tokens = [models[model_names[i]]['output_tokens'] for i in sorted_indices]
        cache_read = [models[model_names[i]]['cache_read'] for i in sorted_indices]
        cache_write = [models[model_names[i]]['cache_write'] for i in sorted_indices]
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Input Tokens
        ax1.bar(range(len(model_names_sorted)), input_tokens, color='#3498db', 
                alpha=0.8, edgecolor='white', linewidth=1)
        ax1.set_title('Input Tokens')
        ax1.set_xticks(range(len(model_names_sorted)))
        ax1.set_xticklabels(model_names_sorted, rotation=45, ha='right', fontsize=9)
        ax1.grid(axis='y', alpha=0.3)
        
        # Output Tokens
        ax2.bar(range(len(model_names_sorted)), output_tokens, color='#e74c3c', 
                alpha=0.8, edgecolor='white', linewidth=1)
        ax2.set_title('Output Tokens')
        ax2.set_xticks(range(len(model_names_sorted)))
        ax2.set_xticklabels(model_names_sorted, rotation=45, ha='right', fontsize=9)
        ax2.grid(axis='y', alpha=0.3)
        
        # Cache Read
        ax3.bar(range(len(model_names_sorted)), cache_read, color='#2ecc71', 
                alpha=0.8, edgecolor='white', linewidth=1)
        ax3.set_title('Cache Read')
        ax3.set_xticks(range(len(model_names_sorted)))
        ax3.set_xticklabels(model_names_sorted, rotation=45, ha='right', fontsize=9)
        ax3.grid(axis='y', alpha=0.3)
        
        # Cache Write
        ax4.bar(range(len(model_names_sorted)), cache_write, color='#f39c12', 
                alpha=0.8, edgecolor='white', linewidth=1)
        ax4.set_title('Cache Write')
        ax4.set_xticks(range(len(model_names_sorted)))
        ax4.set_xticklabels(model_names_sorted, rotation=45, ha='right', fontsize=9)
        ax4.grid(axis='y', alpha=0.3)
        
        plt.suptitle('Detailed Token Statistics', fontsize=16, fontweight='bold')
        
        self.save_figure('tokens_detailed.png')
    
    def create_cost_per_request(self, models):
        """Создает график стоимости на один запрос."""
        print("  └─ Стоимость на запрос...")
        model_names = list(models.keys())
        costs = [m['included_cost'] + m['on_demand_cost'] for m in models.values()]
        
        sorted_indices = sorted(range(len(model_names)), key=lambda i: costs[i], reverse=True)
        model_names_sorted = [model_names[i] for i in sorted_indices]
        
        cost_per_request = []
        for i in sorted_indices:
            model_name = model_names[i]
            model_data = models[model_name]
            total_reqs = model_data['included_requests'] + model_data['on_demand_requests']
            total_cost = model_data['included_cost'] + model_data['on_demand_cost']
            cost_per_req = (total_cost / total_reqs) if total_reqs > 0 else 0
            cost_per_request.append(cost_per_req)
        
        colors = plt.cm.tab20(np.linspace(0, 1, len(model_names_sorted)))
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        bars = ax.bar(range(len(model_names_sorted)), cost_per_request, color=colors, 
                      alpha=0.8, edgecolor='white', linewidth=1.5)
        ax.set_title('Average Cost Per Request', fontsize=16, fontweight='bold')
        ax.set_ylabel('Cost per Request ($)', fontsize=12)
        ax.set_xticks(range(len(model_names_sorted)))
        ax.set_xticklabels(model_names_sorted, rotation=45, ha='right', fontsize=10)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Добавляем числа на бары
        for bar, cost in zip(bars, cost_per_request):
            if cost > 0:
                ax.annotate(f'${cost:.3f}',
                           xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                           xytext=(0, 3), textcoords="offset points",
                           ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        self.save_figure('cost_per_request.png')
    
    def create_cost_distribution_boxplot(self, request_costs_by_model):
        """Создает box plot распределения стоимости запросов по моделям."""
        print("  └─ Box plot распределения стоимости...")
        
        # Фильтруем только модели с платными запросами
        filtered_data = {model: costs for model, costs in request_costs_by_model.items() 
                        if costs and any(c > 0 for c in costs)}
        
        if not filtered_data:
            print("     [!] Нет данных для box plot")
            return
        
        # Сортируем модели по медианной стоимости
        median_costs = {model: np.median(costs) for model, costs in filtered_data.items()}
        sorted_models = sorted(median_costs.keys(), key=lambda x: median_costs[x], reverse=True)
        
        # Подготавливаем данные для box plot
        data_to_plot = [filtered_data[model] for model in sorted_models]
        
        # Создаем график
        fig, ax = plt.subplots(figsize=(16, 10))
        
        # Создаем box plot с настройками
        bp = ax.boxplot(data_to_plot, labels=sorted_models, patch_artist=True,
                       notch=True,  # Вырезы показывают доверительный интервал медианы
                       showmeans=True,  # Показываем среднее значение
                       meanprops=dict(marker='D', markerfacecolor='red', markersize=8, 
                                     markeredgecolor='darkred', linewidth=1.5),
                       medianprops=dict(color='darkblue', linewidth=2),
                       boxprops=dict(facecolor='lightblue', edgecolor='darkblue', linewidth=1.5),
                       whiskerprops=dict(color='darkblue', linewidth=1.5),
                       capprops=dict(color='darkblue', linewidth=1.5),
                       flierprops=dict(marker='o', markerfacecolor='orange', markersize=6,
                                      markeredgecolor='darkorange', alpha=0.6))
        
        ax.set_title('Cost Distribution Per Request by Model\n(Box Plot with Median, Quartiles & Outliers)', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('Cost per Request ($)', fontsize=13, fontweight='bold')
        ax.set_xlabel('Models', fontsize=13, fontweight='bold')
        ax.set_xticklabels(sorted_models, rotation=45, ha='right', fontsize=10)
        ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.7)
        
        # Добавляем легенду
        from matplotlib.patches import Patch
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], color='darkblue', linewidth=2, label='Median'),
            Line2D([0], [0], marker='D', color='w', markerfacecolor='red', 
                   markersize=8, markeredgecolor='darkred', label='Mean'),
            Patch(facecolor='lightblue', edgecolor='darkblue', label='Q1-Q3 (IQR)'),
            Line2D([0], [0], color='darkblue', linewidth=1.5, label='Min-Max (whiskers)'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', 
                   markersize=6, markeredgecolor='darkorange', label='Outliers')
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=10, framealpha=0.9)
        
        # Добавляем статистику для каждой модели
        for i, model in enumerate(sorted_models, 1):
            costs = filtered_data[model]
            median = np.median(costs)
            mean = np.mean(costs)
            q1 = np.percentile(costs, 25)
            q3 = np.percentile(costs, 75)
            
            # Выводим медиану над боксом
            ax.text(i, median, f'${median:.3f}', 
                   ha='center', va='bottom', fontsize=8, 
                   fontweight='bold', color='darkblue',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                            edgecolor='darkblue', alpha=0.8))
        
        self.save_figure('cost_distribution_boxplot.png')

