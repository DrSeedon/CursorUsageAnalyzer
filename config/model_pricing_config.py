# Конфигурация цен для различных моделей ИИ (официальные цены Cursor)
# Цены указаны в долларах за 1M токенов
# Источник: https://www.cursor.com/pricing

MODEL_PRICING = {
    # Claude модели (Anthropic)
    'claude-4-opus': {
        'input': 15.0,
        'output': 75.0,
        'cache_write': 18.75,
        'cache_read': 1.50
    },
    
    'claude-4.1-opus': {
        'input': 15.0,
        'output': 75.0,
        'cache_write': 18.75,
        'cache_read': 1.50
    },
    
    'claude-4.5-opus': {
        'input': 3.0,
        'output': 15.0,
        'cache_write': 3.75,
        'cache_read': 0.30
    },
    
    'claude-4.5-opus-high-thinking': {
        'input': 3.0,
        'output': 15.0,
        'cache_write': 3.75,
        'cache_read': 0.30
    },
    
    'claude-4-sonnet': {
        'input_under_200k': 3.0,
        'output_under_200k': 15.0,
        'cache_write_under_200k': 3.75,
        'cache_read_under_200k': 0.30,
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
    
    'gemini-3-pro': {
        'input': 1.25,
        'output': 10.0,
        'cache_write': 1.25,
        'cache_read': 0.125
    },
    
    'gemini-3-pro-preview': {
        'input': 2.0,
        'output': 12.0,
        'cache_write': 2.0,
        'cache_read': 0.20
    },
    
    # DeepSeek модели
    'deepseek-r1': {
        'input': 3.0,
        'output': 8.0,
        'cache_write': 3.0,
        'cache_read': 3.0
    },
    
    'deepseek-v3.1': {
        'input': 0.56,
        'output': 1.68,
        'cache_write': 0.56,
        'cache_read': 0.56
    },

    # OpenAI модели
    'gpt-4.1': {
        'input': 2.0,
        'output': 8.0,
        'cache_write': 2.0,
        'cache_read': 0.50
    },
    
    'gpt-5': {
        'input': 1.25,
        'output': 10.0,
        'cache_write': 1.25,
        'cache_read': 0.125
    },
    
    'gpt-5-fast': {
        'input': 2.5,
        'output': 20.0,
        'cache_write': 2.5,
        'cache_read': 0.25
    },
    
    'gpt-5-mini': {
        'input': 0.25,
        'output': 2.0,
        'cache_write': 0.25,
        'cache_read': 0.025
    },
    
    'gpt-5-codex': {
        'input': 1.25,
        'output': 10.0,
        'cache_write': 1.25,
        'cache_read': 0.125
    },
    
    'gpt-5-pro': {
        'input': 15.0,
        'output': 120.0,
        'cache_write': 15.0,
        'cache_read': 1.5
    },
    
    'gpt-5.1': {
        'input': 1.25,
        'output': 10.0,
        'cache_write': 1.25,
        'cache_read': 0.125
    },
    
    'gpt-5.1-codex': {
        'input': 1.25,
        'output': 10.0,
        'cache_write': 1.25,
        'cache_read': 0.125
    },
    
    'gpt-5.1-codex-mini': {
        'input': 0.25,
        'output': 2.0,
        'cache_write': 0.25,
        'cache_read': 0.025
    },
    
    'o3': {
        'input': 2.0,
        'output': 8.0,
        'cache_write': 2.0,
        'cache_read': 0.50
    },
    
    # xAI модели
    'grok-code-fast-1': {
        'input': 0.20,
        'output': 1.50,
        'cache_write': 0.20,
        'cache_read': 0.02
    },
    
    'grok-4': {
        'input': 3.0,
        'output': 15.0,
        'cache_write': 3.0,
        'cache_read': 0.75
    },
    
    'grok-4-fast': {
        'input': 0.20,
        'output': 0.50,
        'cache_write': 0.20,
        'cache_read': 0.05
    },
    
    'grok-4-fast-reasoning': {
        'input': 0.20,
        'output': 0.50,
        'cache_write': 0.20,
        'cache_read': 0.05
    },
    
    'grok-4-0709': {
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