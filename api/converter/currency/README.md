# Currency Converter

Conversor de moedas com taxas de câmbio atualizadas em tempo real.

## Características

- 💱 **17+ moedas suportadas**: USD, EUR, BRL, GBP, JPY, CAD, AUD, CHF, CNY, INR, KRW, MXN, ARS, CLP, COP, PEN, UYU
- 🔄 **Taxas em tempo real**: APIs atualizadas automaticamente
- 💾 **Cache inteligente**: Evita chamadas desnecessárias
- 🛡️ **Fallback robusto**: Funciona mesmo sem internet
- 💰 **Formatação automática**: Símbolos e formatos por país

## Uso Rápido

```python
from api.converter.currency.currency import convert_currency

# Conversão simples
result = convert_currency(100, 'USD', 'BRL')
print(result['formatted_result'])  # "R$ 520,00"

# Apenas a taxa
from api.converter.currency.currency import get_exchange_rate
rate = get_exchange_rate('EUR', 'USD')
print(f"1 EUR = {rate} USD")
```

## Moedas Suportadas

| Código | Moeda | Símbolo |
|--------|-------|---------|
| USD | US Dollar | $ |
| EUR | Euro | € |
| BRL | Brazilian Real | R$ |
| GBP | British Pound | £ |
| JPY | Japanese Yen | ¥ |
| CAD | Canadian Dollar | C$ |
| AUD | Australian Dollar | A$ |
| CHF | Swiss Franc | CHF |
| CNY | Chinese Yuan | ¥ |
| INR | Indian Rupee | ₹ |
| KRW | South Korean Won | ₩ |
| MXN | Mexican Peso | $ |
| ARS | Argentine Peso | $ |
| CLP | Chilean Peso | $ |
| COP | Colombian Peso | $ |
| PEN | Peruvian Sol | S/ |
| UYU | Uruguayan Peso | $U |

## API Completa

### Classe CurrencyConverter

```python
from api.converter.currency.currency import CurrencyConverter

# Inicialização
converter = CurrencyConverter()
# ou com API key para maior precisão
converter = CurrencyConverter(api_key="sua_api_key")

# Conversão completa
result = converter.convert(100, 'USD', 'BRL')
print(result)
# {
#     'original_amount': 100,
#     'converted_amount': 520.0,
#     'from_currency': 'USD',
#     'to_currency': 'BRL',
#     'exchange_rate': 5.20,
#     'formatted_original': '$ 100.00',
#     'formatted_result': 'R$ 520,00',
#     'timestamp': '2025-07-23T18:48:06',
#     'source': '2025-07-23'
# }
```

### Funções de Conveniência

```python
from api.converter.currency.currency import convert_currency, get_exchange_rate

# Conversão rápida
result = convert_currency(50, 'EUR', 'USD')

# Apenas taxa de câmbio
rate = get_exchange_rate('GBP', 'BRL')
```

## Exemplos Avançados

### Processamento em Lote

```python
converter = CurrencyConverter()

conversions = [
    (100, 'USD', 'BRL'),
    (50, 'EUR', 'USD'),
    (1000, 'BRL', 'USD')
]

results = []
for amount, from_curr, to_curr in conversions:
    result = converter.convert(amount, from_curr, to_curr)
    results.append(result)
    print(f"{result['formatted_original']} → {result['formatted_result']}")
```

### Monitoramento de Taxas

```python
import time

def monitor_rate(from_currency, to_currency, interval=300):
    """Monitora taxa de câmbio a cada 5 minutos"""
    converter = CurrencyConverter()
    
    while True:
        try:
            result = converter.convert(1, from_currency, to_currency)
            rate = result['exchange_rate']
            timestamp = result['timestamp']
            
            print(f"[{timestamp}] 1 {from_currency} = {rate:.4f} {to_currency}")
            time.sleep(interval)
            
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(60)  # Aguarda 1 minuto em caso de erro

# monitor_rate('USD', 'BRL')
```

### Calculadora de Investimentos

```python
def calculate_investment_return(initial_amount, from_currency, to_currency, months):
    """Calcula retorno de investimento considerando câmbio"""
    converter = CurrencyConverter()
    
    # Conversão inicial
    initial_converted = converter.convert(initial_amount, from_currency, to_currency)
    
    print(f"Investimento inicial: {initial_converted['formatted_original']}")
    print(f"Valor convertido: {initial_converted['formatted_result']}")
    print(f"Taxa atual: 1 {from_currency} = {initial_converted['exchange_rate']:.4f} {to_currency}")
    
    return initial_converted

# Exemplo: investir USD em mercado brasileiro
# result = calculate_investment_return(1000, 'USD', 'BRL', 12)
```

### Tratamento de Erros

```python
try:
    result = convert_currency(100, 'USD', 'XYZ')  # Moeda inválida
except ValueError as e:
    print(f"Erro de validação: {e}")
except Exception as e:
    print(f"Erro geral: {e}")
```

## Configuração com API Key

Para maior precisão e limites maiores, use uma API key:

```python
# Registre-se em https://exchangerate-api.com/ para obter uma chave gratuita
converter = CurrencyConverter(api_key="sua_api_key_aqui")
```

## Cache e Performance

- **Cache automático**: Taxas são cacheadas por 1 hora
- **Fallback offline**: Funciona mesmo sem conexão
- **Timeout inteligente**: 10 segundos máximo por requisição
- **Retry automático**: Tenta APIs alternativas em caso de falha

## Testes

Execute o arquivo diretamente para ver exemplos:

```bash
python api/converter/currency/currency.py
```

## Dependências

```bash
pip install requests
```

## APIs Utilizadas

- **Principal**: [ExchangeRate-API](https://exchangerate-api.com/) (gratuita)
- **Backup**: [Fixer.io](https://fixer.io/) (fallback)
- **Offline**: Taxas fixas atualizadas periodicamente
