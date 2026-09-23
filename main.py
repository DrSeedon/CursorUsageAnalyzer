"""
Анализатор использования Cursor AI.
Модульная версия с разделением на компоненты.
"""

from utils import find_csv_file, setup_output_encoding, clear_directory
from analyzers import CSVAnalyzer
from visualizers.base_visualizer import BaseVisualizer
from visualizers import ModelChartsVisualizer, ActivityChartsVisualizer, HeatmapChartsVisualizer


def select_period():
    """Интерактивный выбор периода анализа."""
    print("\n" + "=" * 70)
    print("ВЫБОР ПЕРИОДА АНАЛИЗА")
    print("=" * 70)
    print("\n1 - Все данные")
    print("2 - Последний месяц (30 дней)")
    print("3 - Последняя неделя (7 дней)")
    print("4 - Последний день (24 часа)")
    
    while True:
        choice = input("\nВыберите вариант (1-4): ").strip()
        if choice == '1':
            return 'all'
        elif choice == '2':
            return 'month'
        elif choice == '3':
            return 'week'
        elif choice == '4':
            return 'day'
        else:
            print("❌ Неправильный выбор. Попробуйте снова (1-4)")


class CursorUsageAnalyzer:
    """Главный класс для анализа использования Cursor."""
    
    def __init__(self, period='all'):
        """Инициализирует анализатор."""
        setup_output_encoding()
        self.csv_file = find_csv_file()
        self.period = period
        self.analyzer = CSVAnalyzer(self.csv_file, period=period)
        self.results = None
    
    def analyze(self):
        """Выполняет анализ CSV файла."""
        period_names = {
            'all': 'Все данные',
            'month': 'Последний месяц',
            'week': 'Последняя неделя',
            'day': 'Последний день'
        }
        
        print("=" * 70)
        print("АНАЛИЗАТОР ИСПОЛЬЗОВАНИЯ CURSOR")
        print("=" * 70)
        print(f"\nФайл: {self.csv_file}")
        print(f"Период: {period_names.get(self.period, self.period)}")
        
        self.results = self.analyzer.analyze()
        
        return self.results
    
    def print_statistics(self):
        """Выводит статистику использования."""
        if not self.results:
            return
        
        models = self.results['models']
        total_cost = self.analyzer.get_total_cost()
        total_requests = self.analyzer.get_total_requests()
        
        print("\n" + "=" * 70)
        print("ОБЩАЯ СТАТИСТИКА")
        print("=" * 70)
        
        print(f"\nВсего моделей использовано: {len(models)}")
        print(f"Общее количество запросов: {total_requests:,}")
        print(f"Общая стоимость: ${total_cost:.2f}")
        
        # Статистика по моделям
        print("\n" + "-" * 70)
        print("СТАТИСТИКА ПО МОДЕЛЯМ:")
        print("-" * 70)
        
        for model_name, stats in sorted(models.items(), 
                                       key=lambda x: x[1]['included_cost'] + x[1]['on_demand_cost'],
                                       reverse=True):
            total_model_cost = stats['included_cost'] + stats['on_demand_cost']
            total_model_requests = stats['included_requests'] + stats['on_demand_requests']
            
            if total_model_requests == 0:
                continue
            
            print(f"\n{model_name}:")
            print(f"  Запросы: {total_model_requests:,} "
                  f"(Included: {stats['included_requests']}, On-Demand: {stats['on_demand_requests']})")
            print(f"  Стоимость: ${total_model_cost:.2f} "
                  f"(Included: ${stats['included_cost']:.2f}, On-Demand: ${stats['on_demand_cost']:.2f})")
            print(f"  Стоимость на запрос: ${total_model_cost / total_model_requests:.4f}")
            
            if stats['errors'] > 0:
                print(f"  Ошибки (Rate Limited): {stats['errors']}")
    
    def create_visualizations(self):
        """Создает все графики."""
        if not self.results:
            return
        
        # Очищаем папку перед созданием новых графиков
        clear_directory('graphics')
        BaseVisualizer.reset_counter()
        
        print("\n" + "=" * 70)
        print("📊 СОЗДАНИЕ ГРАФИКОВ")
        print("=" * 70)
        
        models = self.results['models']
        daily_usage = self.results['daily_usage']
        hourly_usage = self.results['hourly_usage']
        request_costs_by_model = self.results['request_costs_by_model']
        daily_cost = self.results['daily_cost']
        hourly_cost = self.results['hourly_cost']
        daily_cost_by_model = self.results['daily_cost_by_model']
        hourly_cost_by_model = self.results['hourly_cost_by_model']
        hourly_cost_full = self.results['hourly_cost_full']
        hourly_cost_by_model_full = self.results['hourly_cost_by_model_full']
        hourly_requests_full = self.results['hourly_requests_full']
        hourly_requests_by_model_full = self.results['hourly_requests_by_model_full']
        ten_min_cost = self.results['ten_min_cost']
        ten_min_cost_by_model = self.results['ten_min_cost_by_model']
        ten_min_requests = self.results['ten_min_requests']
        ten_min_requests_by_model = self.results['ten_min_requests_by_model']
        all_timestamps = self.results['all_timestamps']
        monthly_cost = self.analyzer.get_total_cost()
        
        print("\n📈 Графики моделей...")
        model_viz = ModelChartsVisualizer()
        model_viz.create_models_overview(models)
        model_viz.create_included_vs_ondemand(models)
        model_viz.create_tokens_detailed(models)
        model_viz.create_cost_per_request(models)
        model_viz.create_cost_distribution_boxplot(request_costs_by_model)
        model_viz.create_token_composition(models)
        
        print("\n📉 Графики активности...")
        activity_viz = ActivityChartsVisualizer()
        activity_viz.create_daily_activity(daily_usage)
        activity_viz.create_daily_activity_separate(daily_usage)
        
        print("\n💰 Графики стоимости...")
        activity_viz.create_cost_timeline_all_period(all_timestamps)
        activity_viz.create_cost_timeline_last_month(daily_cost_by_model)
        activity_viz.create_cost_timeline_last_week(hourly_cost_full)
        activity_viz.create_cost_timeline_last_day(ten_min_cost)
        
        print("\n💰 Графики стоимости по моделям...")
        activity_viz.create_cost_timeline_by_model_all_period(all_timestamps, models)
        activity_viz.create_cost_timeline_by_model_last_month(daily_cost_by_model, models)
        activity_viz.create_cost_timeline_by_model_last_week(hourly_cost_by_model_full, models)
        activity_viz.create_cost_timeline_by_model_last_day(ten_min_cost_by_model, models)
        
        print("\n📊 Графики запросов...")
        activity_viz.create_request_timeline_all_period(all_timestamps)
        activity_viz.create_request_timeline_last_month(daily_usage)
        activity_viz.create_request_timeline_last_week(hourly_requests_full)
        activity_viz.create_request_timeline_last_day(ten_min_requests)
        
        print("\n📊 Графики запросов по моделям...")
        activity_viz.create_request_timeline_by_model_all_period(all_timestamps, models)
        activity_viz.create_request_timeline_by_model_last_month(daily_usage, models)
        activity_viz.create_request_timeline_by_model_last_week(hourly_requests_by_model_full, models)
        activity_viz.create_request_timeline_by_model_last_day(ten_min_requests_by_model, models)
        
        print("\n🔥 Хитмапы...")
        heatmap_viz = HeatmapChartsVisualizer(self.csv_file)
        heatmap_viz.create_combined_requests_heatmap()
        heatmap_viz.create_requests_heatmap_last_month()
        heatmap_viz.create_combined_cost_heatmap()
        heatmap_viz.create_cost_per_request_heatmap()

        print("\n✅ Создано 26 графиков в папке graphics/")
    
    def run(self):
        """Запускает полный анализ."""
        try:
            # Анализ
            self.analyze()
            
            # Вывод статистики
            self.print_statistics()
            
            # Визуализация
            self.create_visualizations()
            
            print("\n" + "=" * 70)
            print("✓ АНАЛИЗ ЗАВЕРШЕН!")
            print("Графики сохранены в папке: graphics/")
            print("=" * 70)
            
        except FileNotFoundError as e:
            print(f"\nОшибка: {e}")
        except Exception as e:
            print(f"\nНепредвиденная ошибка: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Главная функция."""
    period = select_period()
    analyzer = CursorUsageAnalyzer(period=period)
    analyzer.run()


if __name__ == '__main__':
    main()

