# 🗺️ Coordinate Converter

Conversor robusto de coordenadas geográficas entre diferentes formatos (Decimal, DMS, DDM) com cálculos de distância e direção.

## ✨ Características

- **Múltiplos Formatos**: Suporte para Decimal Degrees, DMS e DDM
- **Detecção Automática**: Identifica automaticamente o formato da coordenada
- **Cálculo de Distância**: Fórmula de Haversine para distâncias precisas
- **Cálculo de Direção**: Bearing e direções cardinais
- **Validação Robusta**: Validação rigorosa de formatos de entrada
- **Pares de Coordenadas**: Conversão de latitude/longitude em conjunto

## 🎯 Formatos Suportados

### Decimal Degrees (DD)
- **Formato**: `-74.0060` ou `40.7128`
- **Uso**: Sistemas GPS, APIs, bancos de dados

### Degrees Minutes Seconds (DMS)
- **Formato**: `40° 42' 46.08" N` ou `74° 0' 21.60" W`
- **Uso**: Navegação tradicional, mapas topográficos

### Degrees Decimal Minutes (DDM)
- **Formato**: `40° 42.768' N` ou `74° 0.360' W`
- **Uso**: Sistemas de navegação marítima

## 🚀 Como Usar

### Importação
```python
from api.converter.coordinate.coordinate import CoordinateConverter, convert_coordinate, calculate_distance
```

### Conversão Básica
```python
# Decimal para DMS
result = CoordinateConverter.convert('40.7128', 'decimal', 'dms', is_latitude=True)
print(result['converted_coordinate'])  # 40° 42' 46.08" N

# DMS para Decimal
result = convert_coordinate('40° 42\' 46.08" N', 'dms', 'decimal')
print(result['decimal_value'])  # 40.7128
```

### Conversão de Pares de Coordenadas
```python
# Converte latitude e longitude juntas
result = CoordinateConverter.convert_coordinate_pair(
    '40.7128', '-74.0060',  # NYC em decimal
    'decimal', 'dms'
)
print(result['coordinate_pair']['converted'])
# 40° 42' 46.08" N, 74° 0' 21.60" W
```

### Cálculo de Distância
```python
# Distância entre duas coordenadas
distance_km = calculate_distance(
    40.7128, -74.0060,  # NYC
    34.0522, -118.2437, # Los Angeles
    'km'
)
print(f"Distância: {distance_km} km")  # ~3944 km
```

### Cálculo de Direção
```python
from api.converter.coordinate.coordinate import calculate_bearing

# Bearing entre duas coordenadas
bearing_info = calculate_bearing(
    40.7128, -74.0060,  # NYC
    34.0522, -118.2437  # Los Angeles
)
print(bearing_info['formatted'])  # 258.42° (W)
```

## 📋 Exemplos Práticos

### Conversões Comuns
```python
# Latitude de Nova York
lat_nyc = convert_coordinate('40.7128', 'decimal', 'dms', is_latitude=True)
# 40° 42' 46.08" N

# Longitude de Nova York
lon_nyc = convert_coordinate('-74.0060', 'decimal', 'dms', is_latitude=False)
# 74° 0' 21.60" W

# DMS para DDM
coord_ddm = convert_coordinate('40° 42\' 46.08" N', 'dms', 'ddm')
# 40° 42.768' N

# DDM para Decimal
coord_decimal = convert_coordinate('40° 42.768\' N', 'ddm', 'decimal')
# 40.7128
```

### Análise de Rotas
```python
# Pontos de uma rota
pontos = [
    (40.7128, -74.0060),  # NYC
    (41.8781, -87.6298),  # Chicago
    (34.0522, -118.2437)  # Los Angeles
]

# Calcular distâncias e direções
for i in range(len(pontos) - 1):
    lat1, lon1 = pontos[i]
    lat2, lon2 = pontos[i + 1]
    
    distance = calculate_distance(lat1, lon1, lat2, lon2, 'km')
    bearing = calculate_bearing(lat1, lon1, lat2, lon2)
    
    print(f"Trecho {i+1}: {distance} km, direção {bearing['formatted']}")
```

### Conversão em Lote
```python
# Lista de coordenadas para converter
coordinates = [
    ('40.7128', 'decimal', 'dms', True),
    ('-74.0060', 'decimal', 'dms', False),
    ('34.0522', 'decimal', 'ddm', True),
    ('-118.2437', 'decimal', 'ddm', False)
]

for coord, from_fmt, to_fmt, is_lat in coordinates:
    result = convert_coordinate(coord, from_fmt, to_fmt, is_lat)
    print(f"{coord} → {result['converted_coordinate']}")
```

## 🔧 Métodos da Classe

### `CoordinateConverter.convert(coordinate, from_format, to_format, is_latitude)`
Método principal de conversão entre formatos.

### `CoordinateConverter.convert_coordinate_pair(lat, lon, from_format, to_format)`
Converte um par completo de coordenadas.

### `CoordinateConverter.calculate_distance(lat1, lon1, lat2, lon2, unit)`
Calcula distância usando fórmula de Haversine.

### `CoordinateConverter.calculate_bearing(lat1, lon1, lat2, lon2)`
Calcula direção (bearing) entre duas coordenadas.

### `CoordinateConverter.detect_format(coordinate)`
Detecta automaticamente o formato da coordenada.

## 📊 Estrutura de Retorno

### Conversão Simples
```python
{
    'original_coordinate': '40.7128',
    'original_format': 'decimal',
    'converted_coordinate': '40° 42\' 46.08" N',
    'target_format': 'dms',
    'decimal_value': 40.7128,
    'formatted_result': '40° 42\' 46.08" N',
    'is_latitude': True,
    'all_formats': {
        'decimal': '40.712800',
        'dms': '40° 42\' 46.08" N',
        'ddm': '40° 42.768\' N'
    }
}
```

### Par de Coordenadas
```python
{
    'latitude': { ... },    # Resultado da latitude
    'longitude': { ... },   # Resultado da longitude
    'coordinate_pair': {
        'original': '40.7128, -74.0060',
        'converted': '40° 42\' 46.08" N, 74° 0\' 21.60" W',
        'decimal': '40.712800, -74.006000'
    }
}
```

## 🧭 Cálculos Geográficos

### Distância (Fórmula de Haversine)
```python
# Distância em quilômetros
distance_km = calculate_distance(lat1, lon1, lat2, lon2, 'km')

# Distância em milhas
distance_mi = calculate_distance(lat1, lon1, lat2, lon2, 'mi')
```

### Bearing e Direções Cardinais
```python
bearing_info = calculate_bearing(lat1, lon1, lat2, lon2)
# {
#     'bearing_degrees': 258.42,
#     'cardinal_direction': 'W',
#     'formatted': '258.42° (W)'
# }
```

### Direções Cardinais Suportadas
- **Principais**: N, E, S, W
- **Intermediárias**: NE, SE, SW, NW
- **Detalhadas**: NNE, ENE, ESE, SSE, SSW, WSW, WNW, NNW

## 🎯 Casos de Uso

- **Navegação GPS**: Conversão entre formatos de coordenadas
- **Cartografia**: Padronização de dados geográficos
- **Logística**: Cálculo de rotas e distâncias
- **Turismo**: Conversão de coordenadas de pontos de interesse
- **Pesquisa**: Análise de dados geoespaciais
- **Desenvolvimento**: APIs de localização

## ⚠️ Tratamento de Erros

```python
try:
    result = convert_coordinate('invalid_coord', 'decimal', 'dms')
except ValueError as e:
    print(f"Erro: {e}")
    # Erro: Formato de coordenada inválido
```

## 🧪 Testando

Execute o arquivo diretamente para ver exemplos:

```bash
python coordinate.py
```

## 📐 Precisão

- **Decimal**: Até 6 casas decimais (~0.1 metros)
- **DMS**: Segundos com 2 casas decimais (~3 metros)
- **DDM**: Minutos com 4 casas decimais (~0.6 metros)
- **Distância**: Precisão de Haversine (~0.5% para distâncias grandes)

## 🔄 Integração com Outros Conversores

O Coordinate Converter pode ser usado em conjunto com outros conversores do MundialConverter para workflows completos de processamento de dados geográficos.
