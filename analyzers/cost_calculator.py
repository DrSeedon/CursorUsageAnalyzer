"""Калькулятор стоимости использования моделей."""

from config import MODEL_PRICING


class CostCalculator:
    """Класс для расчета стоимости использования AI моделей."""
    
    @staticmethod
    def calculate_cost(model, input_tokens, output_tokens, cache_read, cache_write):
        """
        Рассчитывает стоимость запроса к модели.
        
        Args:
            model: Название модели
            input_tokens: Количество входных токенов
            output_tokens: Количество выходных токенов
            cache_read: Количество токенов cache read
            cache_write: Количество токенов cache write
            
        Returns:
            float: Стоимость в долларах
        """
        if model not in MODEL_PRICING:
            return 0.0
        
        pricing = MODEL_PRICING[model]
        cost = 0.0
        
        # Определяем контекст (под или над 200k токенов)
        total_context = input_tokens + cache_read + cache_write
        is_over_200k = total_context > 200000
        
        # Поддержка старого формата (input_under_200k/input_over_200k)
        if 'input_under_200k' in pricing:
            input_price = pricing['input_over_200k'] if is_over_200k else pricing['input_under_200k']
            output_price = pricing['output_over_200k'] if is_over_200k else pricing['output_under_200k']
            
            cost += input_tokens * input_price / 1_000_000
            cost += output_tokens * output_price / 1_000_000
            
            # Cache для старого формата
            if cache_read > 0:
                cache_read_key = 'cache_read_over_200k' if is_over_200k else 'cache_read_under_200k'
                cost += cache_read * pricing.get(cache_read_key, 0) / 1_000_000
            
            if cache_write > 0:
                cache_write_key = 'cache_write_over_200k' if is_over_200k else 'cache_write_under_200k'
                cost += cache_write * pricing.get(cache_write_key, input_price) / 1_000_000
        
        # Новый формат (input/output)
        else:
            context_key = 'over_200k' if is_over_200k else 'input'
            input_price = pricing.get(context_key, pricing.get('input', 0))
            output_price = pricing.get('output', 0)
            
            cost += input_tokens * input_price / 1_000_000
            cost += output_tokens * output_price / 1_000_000
            
            # Cache read
            if cache_read > 0 and 'cache_read' in pricing:
                cost += cache_read * pricing['cache_read'] / 1_000_000
            
            # Cache write
            if cache_write > 0:
                if 'cache_write' in pricing:
                    cost += cache_write * pricing['cache_write'] / 1_000_000
                else:
                    cost += cache_write * input_price / 1_000_000
        
        return cost

