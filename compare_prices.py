"""
Сравнение цен Cursor vs OpenRouter.
"""

# Cursor официальные цены (из docs.cursor.com/models)
CURSOR_PRICES = {
    'claude-4.5-opus': {'input': 3, 'cache_write': 3.75, 'cache_read': 0.3, 'output': 15},
    'claude-4.5-sonnet': {'input': 3, 'cache_write': 3.75, 'cache_read': 0.3, 'output': 15},
    'claude-4.5-sonnet-1M': {'input': 6, 'cache_write': 7.5, 'cache_read': 0.6, 'output': 22.5},
    'claude-4.5-haiku': {'input': 1, 'cache_write': 1.25, 'cache_read': 0.1, 'output': 5},
    'gemini-3-pro': {'input': 1.25, 'cache_write': 1.25, 'cache_read': 0.125, 'output': 10},
    'gemini-3-pro-preview': {'input': 2, 'cache_write': 2, 'cache_read': 0.2, 'output': 12},
    'gpt-5.1': {'input': 1.25, 'cache_write': 1.25, 'cache_read': 0.125, 'output': 10},
    'grok-4': {'input': 3, 'cache_write': 3, 'cache_read': 0.75, 'output': 15},
}

# OpenRouter цены
OPENROUTER_PRICES = {
    'claude-4.5-opus': {'input': 5, 'cache_write': 6.25, 'cache_read': 0.5, 'output': 25},
    'claude-4.5-sonnet': {'input': 3, 'cache_write': 3.75, 'cache_read': 0.3, 'output': 15},
    'claude-4.5-sonnet-1M': {'input': 6, 'cache_write': 7.5, 'cache_read': 0.6, 'output': 22.5},
    'claude-4.5-haiku': {'input': 1, 'cache_write': 1.25, 'cache_read': 0.1, 'output': 5},
    'gemini-3-pro-preview': {'input': 2, 'cache_write': 2.375, 'cache_read': 0.2, 'output': 12},
    'gemini-3-pro-preview-1M': {'input': 4, 'cache_write': 4.375, 'cache_read': 0.4, 'output': 18},
}


def compare():
    print("=" * 80)
    print("CURSOR vs OPENROUTER PRICES (per 1M tokens)")
    print("=" * 80)
    
    for model in sorted(set(CURSOR_PRICES.keys()) & set(OPENROUTER_PRICES.keys())):
        cursor = CURSOR_PRICES[model]
        openrouter = OPENROUTER_PRICES[model]
        
        print(f"\n{model}:")
        print(f"  {'':20} {'Cursor':>10} {'OpenRouter':>12} {'Diff':>10}")
        print(f"  {'-'*54}")
        
        for key in ['input', 'output', 'cache_read', 'cache_write']:
            c_val = cursor.get(key, 0)
            o_val = openrouter.get(key, 0)
            diff = c_val - o_val
            diff_str = f"{diff:+.2f}" if diff != 0 else "="
            match = "[OK]" if abs(diff) < 0.01 else "[!!]"
            
            print(f"  {key:20} ${c_val:>8.2f}  ${o_val:>10.2f}  {diff_str:>8} {match}")
    
    print("\n" + "=" * 80)
    print("KEY DIFFERENCES:")
    print("=" * 80)
    
    print("\n[!!] Claude 4.5 Opus:")
    print("     Cursor:     $3 input, $15 output")
    print("     OpenRouter: $5 input, $25 output")
    print("     -> Cursor is 40% CHEAPER for Opus!")
    
    print("\n[OK] Claude 4.5 Sonnet/Haiku:")
    print("     Prices match between Cursor and OpenRouter")
    
    print("\n[!!] Gemini 3 Pro Preview:")
    print("     cache_write differs slightly ($2 vs $2.375)")


if __name__ == '__main__':
    compare()

