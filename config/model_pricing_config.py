# Конфигурация цен для различных моделей ИИ (официальные цены Cursor)
# Цены указаны в долларах за 1M токенов
# Источник: https://www.cursor.com/pricing

MODEL_PRICING = {
    # Claude модели (Anthropic)
    'claude-4-sonnet': {
        # Claude 4 Sonnet (200k context)
        'input_under_200k': 3.0,
        'output_under_200k': 15.0,
        'cache_write_under_200k': 3.75,
        'cache_read_under_200k': 0.30,
        # Claude 4 Sonnet 1M (1M context)
        'input_over_200k': 6.0,
        'output_over_200k': 22.5,
        'cache_write_over_200k': 7.5,
        'cache_read_over_200k': 0.60
    },
    
    'claude-4.5-sonnet': {
        'input': 3.0,
        'output': 15.0,
        'cache_write': 3.75,
        'cache_read': 0.30
    },
    
    'claude-4.5-sonnet-thinking': {
        'input': 3.0,
        'output': 15.0,
        'cache_write': 3.75,
        'cache_read': 0.30
    },
    
    'claude-4.5-haiku': {
        'input': 1.0,
        'output': 5.0,
        'cache_write': 1.25,
        'cache_read': 0.10
    },
    
    'claude-4.5-haiku-thinking': {
        'input': 1.0,
        'output': 5.0,
        'cache_write': 1.25,
        'cache_read': 0.10
    },
    
    # Gemini модели (Google)
    'gemini-2.5-pro': {
        'input_under_200k': 1.25,
        'output_under_200k': 10.0,
        'cache_write_under_200k': 1.25,
        'cache_read_under_200k': 0.13,
        # 1M context (estimated same as base)
        'input_over_200k': 1.25,
        'output_over_200k': 10.0,
        'cache_write_over_200k': 1.25,
        'cache_read_over_200k': 0.13
    },
    
    'gemini-2.5-flash': {
        'input': 0.30,
        'output': 2.50,
        'cache_write': 0.30,
        'cache_read': 0.03
    },
    
    # OpenAI модели
    'gpt-5': {
        'input': 1.25,
        'output': 10.0,
        'cache_write': 1.25,
        'cache_read': 0.13
    },
    
    # xAI модели
    'grok-code-fast-1': {
        'input': 0.20,
        'output': 1.50,
        'cache_write': 0.20,
        'cache_read': 0.02
    },
    
    'grok-4-0709': {
        # Grok 4 Fast
        'input': 0.20,
        'output': 0.50,
        'cache_write': 0.20,
        'cache_read': 0.05
    },
    
    # Cursor модели
    'composer-1': {
        'input': 1.25,
        'output': 10.0,
        'cache_write': 1.25,
        'cache_read': 0.13
    },
    
    'auto': {
        # Mixed model - approximate pricing
        'input': 1.25,
        'output': 6.0,
        'cache_write': 1.25,
        'cache_read': 0.13
    },
    
    'agent_review': {
        # Free internal Cursor tool
        'input': 0.0,
        'output': 0.0
    }
}