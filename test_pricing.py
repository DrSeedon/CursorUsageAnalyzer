"""
Тестовый скрипт для проверки правильности расчета цен.
Сравнивает расчетные цены с ценами из CSV.
"""

import csv
from config import MODEL_PRICING


def calculate_cost(model, input_no_cache, output_tokens, cache_read, cache_write, input_with_cache=0):
    """
    Рассчитывает стоимость запроса.
    
    ВАЖНО: Cursor похоже берет деньги за Input(w/ Cache Write) по cache_write_price,
    а не за разницу! То есть cache_write - это весь Input(w/ Cache Write).
    """
    if model not in MODEL_PRICING:
        return None, f"Model {model} not in config"
    
    pricing = MODEL_PRICING[model]
    cost = 0.0
    
    # Определяем контекст (для 1M context models)
    # Haiku имеет только 200k, так что для него не применяем over_200k
    total_context = input_no_cache + cache_read + cache_write
    is_over_200k = total_context > 200000 and 'haiku' not in model
    
    # Поддержка формата с under/over 200k
    if 'input_under_200k' in pricing:
        suffix = '_over_200k' if is_over_200k else '_under_200k'
        input_price = pricing.get(f'input{suffix}', pricing.get('input_under_200k', 0))
        output_price = pricing.get(f'output{suffix}', pricing.get('output_under_200k', 0))
        cache_read_price = pricing.get(f'cache_read{suffix}', pricing.get('cache_read_under_200k', 0))
        cache_write_price = pricing.get(f'cache_write{suffix}', pricing.get('cache_write_under_200k', input_price))
    else:
        input_price = pricing.get('input', 0)
        output_price = pricing.get('output', 0)
        cache_read_price = pricing.get('cache_read', 0)
        cache_write_price = pricing.get('cache_write', input_price)
    
    # Основной расчет
    cost += input_no_cache * input_price / 1_000_000
    cost += output_tokens * output_price / 1_000_000
    
    if cache_read > 0:
        cost += cache_read * cache_read_price / 1_000_000
    
    if cache_write > 0:
        cost += cache_write * cache_write_price / 1_000_000
    
    return cost, None


def test_csv_pricing(csv_file, limit=100):
    """Тестирует расчет цен на первых N строках CSV."""
    print("=" * 80)
    print("ТЕСТ РАСЧЕТА ЦЕН")
    print("=" * 80)
    
    errors = []
    matches = 0
    total = 0
    model_stats = {}
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for i, row in enumerate(reader):
            if i >= limit:
                break
            
            model = row['Model']
            kind = row['Kind']
            
            if kind == 'Rate Limited':
                continue
            
            # Парсим токены
            input_with_cache = int(row.get('Input (w/ Cache Write)', 0) or 0)
            input_no_cache = int(row.get('Input (w/o Cache Write)', 0) or 0)
            cache_read = int(row.get('Cache Read', 0) or 0)
            output_tokens = int(row.get('Output Tokens', 0) or 0)
            csv_cost = float(row.get('Cost', 0) or 0)
            
            cache_write = max(0, input_with_cache - input_no_cache)
            
            # Рассчитываем
            calc_cost, error = calculate_cost(model, input_no_cache, output_tokens, cache_read, cache_write)
            
            if error:
                if model not in model_stats:
                    model_stats[model] = {'missing': True, 'count': 0}
                model_stats[model]['count'] += 1
                continue
            
            total += 1
            diff = abs(calc_cost - csv_cost)
            diff_pct = (diff / csv_cost * 100) if csv_cost > 0 else 0
            
            # Инициализация статистики модели
            if model not in model_stats:
                model_stats[model] = {
                    'missing': False,
                    'count': 0,
                    'matches': 0,
                    'total_diff': 0,
                    'max_diff': 0,
                    'examples': []
                }
            
            model_stats[model]['count'] += 1
            
            # Считаем совпадением если разница < 10%
            if diff_pct < 10:
                matches += 1
                model_stats[model]['matches'] += 1
            else:
                model_stats[model]['total_diff'] += diff
                model_stats[model]['max_diff'] = max(model_stats[model]['max_diff'], diff_pct)
                if len(model_stats[model]['examples']) < 3:
                    model_stats[model]['examples'].append({
                        'row': i + 2,
                        'csv': csv_cost,
                        'calc': calc_cost,
                        'diff_pct': diff_pct,
                        'input': input_no_cache,
                        'output': output_tokens,
                        'cache_read': cache_read,
                        'cache_write': cache_write,
                        'total_context': input_no_cache + cache_read + cache_write
                    })
    
    # Вывод результатов
    print(f"\nПроверено строк: {total}")
    print(f"Совпадений (< 10% разницы): {matches} ({matches/total*100:.1f}%)")
    print(f"Расхождений: {total - matches}")
    
    print("\n" + "=" * 80)
    print("СТАТИСТИКА ПО МОДЕЛЯМ")
    print("=" * 80)
    
    for model, stats in sorted(model_stats.items()):
        if stats.get('missing'):
            print(f"\n[XX] {model}: NOT IN CONFIG ({stats['count']} requests)")
            continue
        
        match_rate = stats['matches'] / stats['count'] * 100 if stats['count'] > 0 else 0
        status = "[OK]" if match_rate >= 90 else "[??]" if match_rate >= 50 else "[XX]"
        
        print(f"\n{status} {model}:")
        print(f"   Запросов: {stats['count']}, Совпадений: {stats['matches']} ({match_rate:.1f}%)")
        
        if stats['examples']:
            print(f"   Макс. расхождение: {stats['max_diff']:.1f}%")
            print("   Примеры расхождений:")
            for ex in stats['examples']:
                over_200k = " [>200k]" if ex['total_context'] > 200000 else ""
                print(f"      Строка {ex['row']}: CSV=${ex['csv']:.2f}, Расчет=${ex['calc']:.2f} "
                      f"({ex['diff_pct']:+.1f}%){over_200k}")
                print(f"         input={ex['input']}, output={ex['output']}, "
                      f"cache_read={ex['cache_read']}, cache_write={ex['cache_write']}")


def reverse_engineer_price(csv_file, model_filter=None, limit=20):
    """Обратный расчет цен из CSV данных."""
    print("\n" + "=" * 80)
    print("REVERSE ENGINEERING")
    print("=" * 80)
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for i, row in enumerate(reader):
            if i >= limit:
                break
            
            model = row['Model']
            if model_filter and model != model_filter:
                continue
            
            if row['Kind'] == 'Rate Limited':
                continue
            
            input_with_cache = int(row.get('Input (w/ Cache Write)', 0) or 0)
            input_no_cache = int(row.get('Input (w/o Cache Write)', 0) or 0)
            cache_read = int(row.get('Cache Read', 0) or 0)
            output_tokens = int(row.get('Output Tokens', 0) or 0)
            csv_cost = float(row.get('Cost', 0) or 0)
            total_tokens = int(row.get('Total Tokens', 0) or 0)
            
            cache_write = max(0, input_with_cache - input_no_cache)
            is_over_200k = total_tokens > 200000
            
            print(f"\nRow {i+2}: {model} {'[>200k]' if is_over_200k else ''}")
            print(f"  Input w/ cache: {input_with_cache:,}")
            print(f"  Input w/o cache: {input_no_cache:,}")
            print(f"  Cache Read: {cache_read:,}")
            print(f"  Output: {output_tokens:,}")
            print(f"  CSV Cost: ${csv_cost:.4f}")
            
            # Тест разных гипотез
            # Универсальные гипотезы для всех Claude моделей
            if 'haiku' in model:
                inp, out, cr, cw = 1, 5, 0.1, 1.25
                inp2, out2, cr2, cw2 = 2, 10, 0.2, 2.5  # over_200k
            elif 'opus' in model:
                inp, out, cr, cw = 3, 15, 0.3, 3.75
                inp2, out2, cr2, cw2 = 6, 22.5, 0.6, 7.5  # over_200k
            else:  # sonnet
                inp, out, cr, cw = 3, 15, 0.3, 3.75
                inp2, out2, cr2, cw2 = 6, 22.5, 0.6, 7.5  # over_200k
            
            # Выбираем цены в зависимости от контекста
            if is_over_200k:
                inp, out, cr, cw = inp2, out2, cr2, cw2
            
            # H1: Текущая формула (input_no_cache + cache_write diff)
            h1 = (input_no_cache * inp + output_tokens * out + cache_read * cr + cache_write * cw) / 1_000_000
            # H2: Без cache_write
            h2 = (input_no_cache * inp + output_tokens * out + cache_read * cr) / 1_000_000
            # H3: Input(w/ cache) * input_price + output + cache_read
            h3 = (input_with_cache * inp + output_tokens * out + cache_read * cr) / 1_000_000
            # H4: Input(w/ cache) * cw_price + output (NO cache_read!)
            h4 = (input_with_cache * cw + output_tokens * out) / 1_000_000
            # H5: Только Input(w/ cache) * input + output (NO cache!)  
            h5 = (input_with_cache * inp + output_tokens * out) / 1_000_000
            
            print(f"  H1 (current): ${h1:.4f} ({(h1-csv_cost)/csv_cost*100:+.1f}%)")
            print(f"  H2 (no cw): ${h2:.4f} ({(h2-csv_cost)/csv_cost*100:+.1f}%)")
            print(f"  H3 (inp_w_c*inp): ${h3:.4f} ({(h3-csv_cost)/csv_cost*100:+.1f}%)")
            print(f"  H4 (inp_w_c*cw): ${h4:.4f} ({(h4-csv_cost)/csv_cost*100:+.1f}%)")
            print(f"  H5 (inp_w_c*inp no cr): ${h5:.4f} ({(h5-csv_cost)/csv_cost*100:+.1f}%)")


if __name__ == '__main__':
    import sys
    from utils import find_csv_file
    
    csv_file = find_csv_file()
    print(f"CSV файл: {csv_file}\n")
    
    # Тест расчета цен
    test_csv_pricing(csv_file, limit=200)
    
    # Reverse engineering для проблемных моделей
    reverse_engineer_price(csv_file, model_filter='claude-4.5-haiku', limit=50)

