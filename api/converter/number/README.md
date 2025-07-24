# 🔢 Number Converter

Conversor robusto entre diferentes bases numéricas (Binário, Octal, Decimal, Hexadecimal, Base32, Base64) com detecção automática de formato.

## ✨ Características

- **Detecção Automática**: Identifica automaticamente a base do número de entrada
- **Múltiplas Bases**: Suporte para 6 bases diferentes (2, 8, 10, 16, 32, 64)
- **Prefixos Inteligentes**: Reconhece e gera prefixos padrão (0b, 0o, 0x)
- **Validação Robusta**: Validação rigorosa de números para cada base
- **Representações Completas**: Mostra o número em todas as bases simultaneamente

## 🎯 Bases Suportadas

### Binário (Base 2)
- **Caracteres**: `0, 1`
- **Prefixo**: `0b`
- **Exemplo**: `0b1010` = `10` decimal

### Octal (Base 8)
- **Caracteres**: `0-7`
- **Prefixo**: `0o`
- **Exemplo**: `0o377` = `255` decimal

### Decimal (Base 10)
- **Caracteres**: `0-9`
- **Prefixo**: Nenhum
- **Exemplo**: `255` = `255` decimal

### Hexadecimal (Base 16)
- **Caracteres**: `0-9, A-F`
- **Prefixo**: `0x`
- **Exemplo**: `0xFF` = `255` decimal

### Base32
- **Caracteres**: `A-Z, 2-7`
- **Prefixo**: Nenhum
- **Exemplo**: `H4` = `255` decimal

### Base64
- **Caracteres**: `A-Z, a-z, 0-9, +, /`
- **Prefixo**: Nenhum
- **Exemplo**: `D/` = `255` decimal

## 🚀 Como Usar

### Importação
```python
from api.converter.number.number import NumberConverter, convert_number, detect_number_base
```

### Conversão Básica
```python
# Binário para Decimal
result = NumberConverter.convert('1010', 'binary', 'decimal')
print(result['converted_number'])  # 10

# Decimal para Hexadecimal
result = convert_number('255', 'decimal', 'hexadecimal')
print(result['converted_number'])  # FF
```

### Detecção Automática
```python
# Detecta automaticamente a base
result = convert_number('0xFF', 'auto', 'binary')
print(result['converted_number'])  # 11111111

# Detectar base manualmente
base = detect_number_base('0b1010')
print(base)  # binary
```

### Representações Completas
```python
from api.converter.number.number import get_all_representations

# Obter número em todas as bases
all_bases = get_all_representations('42', 'decimal')
print(all_bases)
# {
#     'binary': '101010',
#     'octal': '52',
#     'decimal': '42',
#     'hexadecimal': '2A',
#     'base32': 'BK',
#     'base64': 'q'
# }
```

## 📋 Exemplos Práticos

### Conversões Comuns
```python
# Programação: Hexadecimal para Binário
result = convert_number('0xFF', 'auto', 'binary')
# 11111111

# Sistemas: Octal para Decimal
result = convert_number('755', 'octal', 'decimal')
# 493

# Encoding: Decimal para Base64
result = convert_number('1000', 'decimal', 'base64')
# Po

# Criptografia: Base32 para Hexadecimal
result = convert_number('HELLO', 'base32', 'hexadecimal')
# 48656C6C6F
```

### Análise de Números
```python
# Analisar um número em todas as bases
number = '255'
result = NumberConverter.convert(number, 'decimal', 'decimal')

print("Representações do número 255:")
for base, value in result['all_bases'].items():
    base_info = NumberConverter.get_base_info(base)
    print(f"{base_info['name']}: {value}")

# Com prefixos
print("\nCom prefixos:")
for base, value in result['with_prefixes'].items():
    print(f"{base}: {value}")
```

### Conversão em Lote
```python
# Lista de números para converter
numbers = [
    ('1010', 'binary', 'decimal'),
    ('0xFF', 'auto', 'octal'),
    ('777', 'octal', 'hexadecimal'),
    ('42', 'decimal', 'base32')
]

for num, from_base, to_base in numbers:
    result = convert_number(num, from_base, to_base)
    print(f"{num} → {result['converted_number']} ({to_base})")
```

### Validação de Números
```python
# Verificar se um número é válido para uma base
valid = NumberConverter.validate_number('1010', 'binary')  # True
valid = NumberConverter.validate_number('1019', 'binary')  # False

# Calcular dígitos necessários
digits = NumberConverter.calculate_digits_needed(255, 'binary')  # 8
digits = NumberConverter.calculate_digits_needed(255, 'hexadecimal')  # 2
```

## 🔧 Métodos da Classe

### `NumberConverter.convert(number, from_base, to_base)`
Método principal de conversão entre bases.

### `NumberConverter.detect_base(number)`
Detecta automaticamente a base do número.

### `NumberConverter.validate_number(number, base)`
Valida se o número é válido para a base especificada.

### `NumberConverter.to_decimal(number, from_base)`
Converte qualquer base para decimal.

### `NumberConverter.from_decimal(decimal_value, to_base)`
Converte decimal para qualquer base.

### `NumberConverter.get_supported_bases()`
Lista todas as bases suportadas.

### `NumberConverter.get_base_info(base)`
Retorna informações detalhadas sobre uma base.

## 📊 Estrutura de Retorno

```python
{
    'original_number': '1010',
    'original_base': 'binary',
    'converted_number': '10',
    'target_base': 'decimal',
    'decimal_value': 10,
    'formatted_result': '10',
    'all_bases': {
        'binary': '1010',
        'octal': '12',
        'decimal': '10',
        'hexadecimal': 'A',
        'base32': 'K',
        'base64': 'K'
    },
    'with_prefixes': {
        'binary': '0b1010',
        'octal': '0o12',
        'decimal': '10',
        'hexadecimal': '0xA',
        'base32': 'K',
        'base64': 'K'
    }
}
```

## 🎯 Casos de Uso

### Programação
```python
# Conversão de cores em CSS
hex_color = convert_number('255', 'decimal', 'hexadecimal')  # FF
rgb_value = convert_number('FF', 'hexadecimal', 'decimal')   # 255

# Máscaras de bits
binary_mask = convert_number('255', 'decimal', 'binary')     # 11111111
```

### Sistemas Operacionais
```python
# Permissões Unix (octal)
permissions = convert_number('755', 'octal', 'binary')      # 111101101
decimal_perm = convert_number('755', 'octal', 'decimal')    # 493
```

### Encoding/Decoding
```python
# Base64 encoding simulation
base64_value = convert_number('1000', 'decimal', 'base64')  # Po
original = convert_number('Po', 'base64', 'decimal')        # 1000
```

### Análise de Dados
```python
# Conversão de IDs em diferentes sistemas
user_id_hex = convert_number('12345', 'decimal', 'hexadecimal')  # 3039
user_id_b32 = convert_number('12345', 'decimal', 'base32')       # C0P
```

## 🔍 Detecção Automática

O conversor pode detectar automaticamente a base baseado em:

- **Prefixos**: `0b` (binário), `0o` (octal), `0x` (hexadecimal)
- **Caracteres**: Analisa os caracteres válidos para cada base
- **Padrões**: Reconhece padrões específicos (Base32, Base64)

```python
# Exemplos de detecção automática
detect_number_base('0b1010')    # binary
detect_number_base('0xFF')      # hexadecimal
detect_number_base('777')       # octal (se apenas 0-7)
detect_number_base('HELLO')     # base32
detect_number_base('QWE=')      # base64
```

## ⚠️ Limitações

- **Números Negativos**: Não suportados
- **Números Decimais**: Apenas inteiros
- **Tamanho**: Limitado pela precisão do Python para inteiros
- **Base64 Padding**: Automaticamente tratado

## ⚠️ Tratamento de Erros

```python
try:
    result = convert_number('XYZ', 'binary', 'decimal')
except ValueError as e:
    print(f"Erro: {e}")
    # Erro: Número inválido para base binary: XYZ
```

## 🧪 Testando

Execute o arquivo diretamente para ver exemplos:

```bash
python number.py
```

## 🔄 Integração com Outros Conversores

O Number Converter pode ser usado em conjunto com outros conversores do MundialConverter para workflows completos de processamento de dados numéricos.
