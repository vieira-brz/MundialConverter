# Units Converter

Conversor completo de unidades de medida com suporte a 8 categorias diferentes.

## Características

- 📏 **8 categorias**: Comprimento, Peso, Temperatura, Volume, Área, Velocidade, Energia, Potência
- 🔄 **60+ unidades**: Métricas, imperiais, brasileiras e especiais
- 🌡️ **Temperatura especial**: Celsius, Fahrenheit, Kelvin, Rankine
- 🎯 **Detecção automática**: Identifica categoria automaticamente
- 📊 **Formatação inteligente**: Notação científica para valores extremos

## Uso Rápido

```python
from api.converter.units.units import convert_units

# Conversão simples
result = convert_units(100, 'cm', 'm')
print(result['formatted_result'])  # "1 M (Metro)"

# Temperatura
result = convert_units(100, 'c', 'f')
print(result['formatted_result'])  # "212 F (Fahrenheit)"

# Peso
result = convert_units(1, 'kg', 'lb')
print(result['formatted_result'])  # "2.20462 LB (Libra)"
```

## Categorias e Unidades

### 📏 Comprimento (Length)
**Métricas**: mm, cm, dm, m, dam, hm, km  
**Imperiais**: in (polegada), ft (pé), yd (jarda), mi (milha)  
**Náuticas**: nmi (milha náutica)

### ⚖️ Peso/Massa (Weight)
**Métricas**: mg, g, kg, t (tonelada)  
**Imperiais**: oz (onça), lb (libra), st (stone)  
**Brasileiras**: arroba

### 🌡️ Temperatura (Temperature)
**Unidades**: c (Celsius), f (Fahrenheit), k (Kelvin), r (Rankine)

### 🥤 Volume (Volume)
**Métricas**: ml, cl, dl, l, dal, hl, kl  
**Imperiais**: tsp, tbsp, fl_oz, cup, pt, qt, gal  
**Cúbicas**: cm3, m3

### 📐 Área (Area)
**Métricas**: mm2, cm2, m2, dam2, hm2, km2  
**Agrárias**: ha (hectare), a (are)  
**Imperiais**: in2, ft2, yd2, ac (acre), mi2

### 🏃 Velocidade (Speed)
**Unidades**: m/s, km/h, mph, ft/s, knot (nó)

### ⚡ Energia (Energy)
**Unidades**: j, kj, cal, kcal, wh, kwh, btu

### 🔌 Potência (Power)
**Unidades**: w, kw, mw, hp (cavalo-vapor), cv (cavalo-vapor métrico)

## API Completa

### Classe UnitsConverter

```python
from api.converter.units.units import UnitsConverter

# Conversão com categoria específica
result = UnitsConverter.convert(100, 'cm', 'm', 'length')
print(result)
# {
#     'original_value': 100,
#     'converted_value': 1.0,
#     'from_unit': 'CM',
#     'to_unit': 'M',
#     'from_unit_name': 'Centímetro',
#     'to_unit_name': 'Metro',
#     'category': 'Comprimento',
#     'formatted_result': '1 M (Metro)'
# }

# Listar categorias
categories = UnitsConverter.get_categories()
print(categories)  # ['length', 'weight', 'temperature', ...]

# Unidades de uma categoria
units = UnitsConverter.get_units_in_category('length')
print(units['units'].keys())  # ['mm', 'cm', 'm', 'km', ...]
```

### Funções de Conveniência

```python
from api.converter.units.units import convert_units, get_available_units

# Conversão rápida (categoria detectada automaticamente)
result = convert_units(1, 'km', 'mi')

# Ver todas as unidades disponíveis
all_units = get_available_units()

# Ver unidades de uma categoria específica
length_units = get_available_units('length')
```

## Exemplos Avançados

### Calculadora de Construção

```python
def construction_calculator():
    """Calculadora para construção civil"""
    
    # Área do terreno
    area_m2 = convert_units(500, 'm2', 'ha')
    print(f"Terreno: {area_m2['formatted_result']}")
    
    # Conversão de materiais
    cement_bags = convert_units(2, 't', 'kg')  # 2 toneladas de cimento
    print(f"Cimento: {cement_bags['formatted_result']}")
    
    # Distâncias
    wall_length = convert_units(15, 'm', 'ft')
    print(f"Parede: {wall_length['formatted_result']}")

# construction_calculator()
```

### Conversor Culinário

```python
def cooking_converter():
    """Conversor para receitas culinárias"""
    
    conversions = [
        (250, 'ml', 'cup', 'volume'),      # Leite
        (500, 'g', 'lb', 'weight'),        # Farinha
        (180, 'c', 'f', 'temperature'),    # Forno
        (2, 'tbsp', 'ml', 'volume'),       # Óleo
    ]
    
    ingredients = ['Leite', 'Farinha', 'Forno', 'Óleo']
    
    for i, (value, from_unit, to_unit, category) in enumerate(conversions):
        result = convert_units(value, from_unit, to_unit, category)
        print(f"{ingredients[i]}: {value} {from_unit.upper()} = {result['formatted_result']}")

# cooking_converter()
```

### Monitor de Exercícios

```python
def fitness_tracker():
    """Conversor para atividades físicas"""
    
    # Distância da corrida
    distance = convert_units(5, 'km', 'mi')
    print(f"Corrida: {distance['formatted_result']}")
    
    # Peso corporal
    weight = convert_units(70, 'kg', 'lb')
    print(f"Peso: {weight['formatted_result']}")
    
    # Velocidade média
    speed = convert_units(12, 'km/h', 'mph')
    print(f"Velocidade: {speed['formatted_result']}")

# fitness_tracker()
```

### Conversão em Lote

```python
def batch_conversion():
    """Converte múltiplas unidades de uma vez"""
    
    measurements = [
        (100, 'cm', 'm'),
        (1, 'kg', 'lb'),
        (25, 'c', 'f'),
        (1, 'l', 'gal'),
        (100, 'km/h', 'mph')
    ]
    
    results = []
    for value, from_unit, to_unit in measurements:
        try:
            result = convert_units(value, from_unit, to_unit)
            results.append(result)
            print(f"{value} {from_unit.upper()} → {result['formatted_result']}")
        except Exception as e:
            print(f"Erro: {e}")
    
    return results

# batch_conversion()
```

### Tratamento de Erros

```python
try:
    # Unidade inválida
    result = convert_units(100, 'xyz', 'm')
except ValueError as e:
    print(f"Erro de validação: {e}")

try:
    # Valor negativo (exceto temperatura)
    result = convert_units(-10, 'kg', 'lb')
except ValueError as e:
    print(f"Erro de valor: {e}")

try:
    # Categoria incompatível
    result = convert_units(100, 'cm', 'kg')  # Comprimento para peso
except ValueError as e:
    print(f"Erro de categoria: {e}")
```

## Casos de Uso Especiais

### Temperatura
- Suporta valores negativos
- Conversão direta entre todas as escalas
- Precisão mantida em conversões múltiplas

### Valores Extremos
- Notação científica automática para valores muito grandes/pequenos
- Precisão de 6 dígitos significativos
- Suporte a valores de qualquer magnitude

### Detecção Automática
- Identifica categoria baseada nas unidades fornecidas
- Não precisa especificar categoria na maioria dos casos
- Validação automática de compatibilidade

## Testes

Execute o arquivo diretamente para ver exemplos:

```bash
python api/converter/units/units.py
```

## Dependências

Apenas bibliotecas built-in do Python:
- `typing` (hints de tipo)
- `math` (operações matemáticas)

Não requer instalação de pacotes externos!
