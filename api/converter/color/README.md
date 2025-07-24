# 🎨 Color Converter

Conversor robusto de cores entre diferentes formatos (HEX, RGB, HSL, HSV, CMYK) com detecção automática de formato.

## ✨ Características

- **Detecção Automática**: Identifica automaticamente o formato da cor de entrada
- **Múltiplos Formatos**: Suporte para HEX, RGB, RGBA, HSL, HSLA, HSV, CMYK e cores nomeadas
- **Cores Nomeadas**: Suporte para 30+ cores nomeadas comuns (red, blue, green, etc.)
- **Validação Robusta**: Validação rigorosa de formatos de entrada
- **Informações Completas**: Retorna todas as representações da cor

## 🎯 Formatos Suportados

### Entrada (Detecção Automática)
- **HEX**: `#FF0000`, `#f00`, `FF0000`
- **RGB**: `rgb(255, 0, 0)`
- **RGBA**: `rgba(255, 0, 0, 0.5)`
- **HSL**: `hsl(0, 100%, 50%)`
- **HSLA**: `hsla(0, 100%, 50%, 0.5)`
- **HSV/HSB**: `hsv(0, 100%, 100%)`
- **CMYK**: `cmyk(0%, 100%, 100%, 0%)`
- **Nomes**: `red`, `blue`, `green`, etc.

### Saída
Todos os formatos acima são suportados para conversão.

## 🚀 Como Usar

### Importação
```python
from api.converter.color.color import ColorConverter, convert_color, get_color_info
```

### Conversão Básica
```python
# Conversão simples
result = ColorConverter.convert('#FF0000', 'rgb')
print(result['converted_color'])  # rgb(255, 0, 0)

# Usando função de conveniência
result = convert_color('red', 'hsl')
print(result['converted_color'])  # hsl(0, 100%, 50%)
```

### Informações Completas da Cor
```python
# Obter todas as representações
info = get_color_info('#FF0000')
print(info['all_formats'])
# {
#     'hex': '#FF0000',
#     'rgb': 'rgb(255, 0, 0)',
#     'rgba': 'rgba(255, 0, 0, 1.0)',
#     'hsl': 'hsl(0, 100%, 50%)',
#     'hsla': 'hsla(0, 100%, 50%, 1.0)',
#     'hsv': 'hsv(0, 100%, 100%)',
#     'cmyk': 'cmyk(0%, 100%, 100%, 0%)'
# }
```

### Detecção de Formato
```python
# Detectar formato automaticamente
format_type = ColorConverter.detect_format('#FF0000')
print(format_type)  # hex

format_type = ColorConverter.detect_format('rgb(255, 0, 0)')
print(format_type)  # rgb
```

## 📋 Exemplos Práticos

### Conversões Comuns
```python
# HEX para RGB
result = convert_color('#FF5733', 'rgb')
# rgb(255, 87, 51)

# RGB para HSL
result = convert_color('rgb(255, 87, 51)', 'hsl')
# hsl(11, 100%, 60%)

# Nome para CMYK
result = convert_color('blue', 'cmyk')
# cmyk(100%, 100%, 0%, 0%)

# HSV para HEX
result = convert_color('hsv(240, 100%, 100%)', 'hex')
# #0000FF
```

### Trabalhando com Transparência
```python
# RGBA para HSLA
result = convert_color('rgba(255, 0, 0, 0.5)', 'hsla')
# hsla(0, 100%, 50%, 0.5)

# Transparência é preservada quando aplicável
```

### Cores Nomeadas Disponíveis
```python
# Listar todas as cores nomeadas
named_colors = ColorConverter.get_named_colors()
print(list(named_colors.keys())[:10])
# ['red', 'green', 'blue', 'white', 'black', ...]

# Usar cor nomeada
result = convert_color('orange', 'rgb')
# rgb(255, 165, 0)
```

## 🎨 Cores Nomeadas Suportadas

O conversor suporte 30+ cores nomeadas comuns:

- **Básicas**: red, green, blue, white, black, yellow, cyan, magenta
- **Tons**: silver, gray, maroon, olive, lime, aqua, teal, navy
- **Especiais**: orange, pink, brown, gold, violet, indigo, turquoise
- **Naturais**: coral, salmon, khaki, lavender, plum

## ⚡ Funções de Conveniência

### `convert_color(color, to_format)`
Conversão rápida entre formatos.

### `get_color_info(color)`
Obtém informações completas sobre uma cor, incluindo todas as representações.

## 🔧 Métodos da Classe

### `ColorConverter.convert(color, to_format)`
Método principal de conversão.

### `ColorConverter.detect_format(color)`
Detecta automaticamente o formato da cor.

### `ColorConverter.parse_color(color)`
Converte qualquer formato para RGB + Alpha.

### `ColorConverter.get_supported_formats()`
Lista todos os formatos suportados.

### `ColorConverter.get_named_colors()`
Retorna dicionário de cores nomeadas.

## 📊 Estrutura de Retorno

```python
{
    'original_color': '#FF0000',           # Cor original
    'original_format': 'hex',              # Formato original detectado
    'converted_color': 'rgb(255, 0, 0)',   # Cor convertida
    'target_format': 'rgb',                # Formato de destino
    'rgb_values': {                        # Valores RGB + Alpha
        'r': 255, 'g': 0, 'b': 0, 'a': 1.0
    },
    'all_formats': {                       # Todas as representações
        'hex': '#FF0000',
        'rgb': 'rgb(255, 0, 0)',
        'rgba': 'rgba(255, 0, 0, 1.0)',
        'hsl': 'hsl(0, 100%, 50%)',
        'hsla': 'hsla(0, 100%, 50%, 1.0)',
        'hsv': 'hsv(0, 100%, 100%)',
        'cmyk': 'cmyk(0%, 100%, 100%, 0%)'
    }
}
```

## 🎯 Casos de Uso

- **Web Design**: Conversão entre HEX e RGB para CSS
- **Design Gráfico**: Conversão para CMYK para impressão
- **Análise de Cores**: Obter informações HSL/HSV para manipulação
- **Desenvolvimento**: Padronização de cores em diferentes formatos
- **Acessibilidade**: Análise de contraste e luminosidade

## ⚠️ Tratamento de Erros

```python
try:
    result = convert_color('invalid_color', 'rgb')
except ValueError as e:
    print(f"Erro: {e}")
    # Erro: Formato de cor não reconhecido: invalid_color
```

## 🧪 Testando

Execute o arquivo diretamente para ver exemplos:

```bash
python color.py
```

## 🔄 Integração com Outros Conversores

O Color Converter pode ser usado em conjunto com outros conversores do MundialConverter para criar workflows completos de processamento de dados.
