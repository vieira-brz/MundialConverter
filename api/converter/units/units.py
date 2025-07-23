from typing import Union, Optional, Dict, Any, List
import math

class UnitsConverter:
    """Classe para conversão entre diferentes unidades de medida"""
    
    # Definições de unidades por categoria
    UNITS_DATA = {
        'length': {
            'name': 'Comprimento',
            'base_unit': 'meter',
            'units': {
                # Métricas
                'mm': {'name': 'Milímetro', 'to_base': 0.001},
                'cm': {'name': 'Centímetro', 'to_base': 0.01},
                'dm': {'name': 'Decímetro', 'to_base': 0.1},
                'm': {'name': 'Metro', 'to_base': 1.0},
                'dam': {'name': 'Decâmetro', 'to_base': 10.0},
                'hm': {'name': 'Hectômetro', 'to_base': 100.0},
                'km': {'name': 'Quilômetro', 'to_base': 1000.0},
                
                # Imperiais
                'in': {'name': 'Polegada', 'to_base': 0.0254},
                'ft': {'name': 'Pé', 'to_base': 0.3048},
                'yd': {'name': 'Jarda', 'to_base': 0.9144},
                'mi': {'name': 'Milha', 'to_base': 1609.344},
                
                # Náuticas
                'nmi': {'name': 'Milha Náutica', 'to_base': 1852.0},
            }
        },
        
        'weight': {
            'name': 'Peso/Massa',
            'base_unit': 'kilogram',
            'units': {
                # Métricas
                'mg': {'name': 'Miligrama', 'to_base': 0.000001},
                'g': {'name': 'Grama', 'to_base': 0.001},
                'kg': {'name': 'Quilograma', 'to_base': 1.0},
                't': {'name': 'Tonelada', 'to_base': 1000.0},
                
                # Imperiais
                'oz': {'name': 'Onça', 'to_base': 0.0283495},
                'lb': {'name': 'Libra', 'to_base': 0.453592},
                'st': {'name': 'Stone', 'to_base': 6.35029},
                
                # Brasileiras
                'arroba': {'name': 'Arroba', 'to_base': 15.0},
            }
        },
        
        'temperature': {
            'name': 'Temperatura',
            'base_unit': 'celsius',
            'units': {
                'c': {'name': 'Celsius', 'to_base': lambda x: x},
                'f': {'name': 'Fahrenheit', 'to_base': lambda x: (x - 32) * 5/9},
                'k': {'name': 'Kelvin', 'to_base': lambda x: x - 273.15},
                'r': {'name': 'Rankine', 'to_base': lambda x: (x - 491.67) * 5/9},
            }
        },
        
        'volume': {
            'name': 'Volume',
            'base_unit': 'liter',
            'units': {
                # Métricas
                'ml': {'name': 'Mililitro', 'to_base': 0.001},
                'cl': {'name': 'Centilitro', 'to_base': 0.01},
                'dl': {'name': 'Decilitro', 'to_base': 0.1},
                'l': {'name': 'Litro', 'to_base': 1.0},
                'dal': {'name': 'Decalitro', 'to_base': 10.0},
                'hl': {'name': 'Hectolitro', 'to_base': 100.0},
                'kl': {'name': 'Quilolitro', 'to_base': 1000.0},
                
                # Imperiais
                'tsp': {'name': 'Colher de Chá', 'to_base': 0.00492892},
                'tbsp': {'name': 'Colher de Sopa', 'to_base': 0.0147868},
                'fl_oz': {'name': 'Onça Fluida', 'to_base': 0.0295735},
                'cup': {'name': 'Xícara', 'to_base': 0.236588},
                'pt': {'name': 'Pinta', 'to_base': 0.473176},
                'qt': {'name': 'Quarto', 'to_base': 0.946353},
                'gal': {'name': 'Galão', 'to_base': 3.78541},
                
                # Cúbicas
                'cm3': {'name': 'Centímetro Cúbico', 'to_base': 0.001},
                'm3': {'name': 'Metro Cúbico', 'to_base': 1000.0},
            }
        },
        
        'area': {
            'name': 'Área',
            'base_unit': 'square_meter',
            'units': {
                # Métricas
                'mm2': {'name': 'Milímetro Quadrado', 'to_base': 0.000001},
                'cm2': {'name': 'Centímetro Quadrado', 'to_base': 0.0001},
                'm2': {'name': 'Metro Quadrado', 'to_base': 1.0},
                'dam2': {'name': 'Decâmetro Quadrado', 'to_base': 100.0},
                'hm2': {'name': 'Hectômetro Quadrado', 'to_base': 10000.0},
                'km2': {'name': 'Quilômetro Quadrado', 'to_base': 1000000.0},
                
                # Agrárias
                'ha': {'name': 'Hectare', 'to_base': 10000.0},
                'a': {'name': 'Are', 'to_base': 100.0},
                
                # Imperiais
                'in2': {'name': 'Polegada Quadrada', 'to_base': 0.00064516},
                'ft2': {'name': 'Pé Quadrado', 'to_base': 0.092903},
                'yd2': {'name': 'Jarda Quadrada', 'to_base': 0.836127},
                'ac': {'name': 'Acre', 'to_base': 4046.86},
                'mi2': {'name': 'Milha Quadrada', 'to_base': 2589988.11},
            }
        },
        
        'speed': {
            'name': 'Velocidade',
            'base_unit': 'meter_per_second',
            'units': {
                'm/s': {'name': 'Metro por Segundo', 'to_base': 1.0},
                'km/h': {'name': 'Quilômetro por Hora', 'to_base': 0.277778},
                'mph': {'name': 'Milha por Hora', 'to_base': 0.44704},
                'ft/s': {'name': 'Pé por Segundo', 'to_base': 0.3048},
                'knot': {'name': 'Nó', 'to_base': 0.514444},
            }
        },
        
        'energy': {
            'name': 'Energia',
            'base_unit': 'joule',
            'units': {
                'j': {'name': 'Joule', 'to_base': 1.0},
                'kj': {'name': 'Quilojoule', 'to_base': 1000.0},
                'cal': {'name': 'Caloria', 'to_base': 4.184},
                'kcal': {'name': 'Quilocaloria', 'to_base': 4184.0},
                'wh': {'name': 'Watt-hora', 'to_base': 3600.0},
                'kwh': {'name': 'Quilowatt-hora', 'to_base': 3600000.0},
                'btu': {'name': 'BTU', 'to_base': 1055.06},
            }
        },
        
        'power': {
            'name': 'Potência',
            'base_unit': 'watt',
            'units': {
                'w': {'name': 'Watt', 'to_base': 1.0},
                'kw': {'name': 'Quilowatt', 'to_base': 1000.0},
                'mw': {'name': 'Megawatt', 'to_base': 1000000.0},
                'hp': {'name': 'Cavalo-vapor', 'to_base': 745.7},
                'cv': {'name': 'Cavalo-vapor (métrico)', 'to_base': 735.5},
            }
        }
    }
    
    @classmethod
    def get_categories(cls) -> List[str]:
        """Retorna lista de categorias disponíveis"""
        return list(cls.UNITS_DATA.keys())
    
    @classmethod
    def get_units_in_category(cls, category: str) -> Optional[Dict]:
        """Retorna unidades de uma categoria específica"""
        return cls.UNITS_DATA.get(category.lower())
    
    @classmethod
    def convert(cls, value: Union[int, float], from_unit: str, to_unit: str, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Converte valor entre unidades
        
        Args:
            value: Valor a ser convertido
            from_unit: Unidade de origem
            to_unit: Unidade de destino
            category: Categoria (opcional, será detectada automaticamente)
        
        Returns:
            Dict com resultado da conversão
        """
        if value < 0 and category != 'temperature':
            raise ValueError("Valor deve ser positivo (exceto para temperatura)")
        
        # Encontra categoria se não fornecida
        if not category:
            category = cls._find_category(from_unit, to_unit)
            if not category:
                raise ValueError(f"Não foi possível determinar a categoria para '{from_unit}' e '{to_unit}'")
        
        category = category.lower()
        if category not in cls.UNITS_DATA:
            raise ValueError(f"Categoria '{category}' não suportada")
        
        category_data = cls.UNITS_DATA[category]
        units = category_data['units']
        
        # Valida unidades
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        if from_unit not in units:
            raise ValueError(f"Unidade '{from_unit}' não encontrada na categoria '{category}'")
        if to_unit not in units:
            raise ValueError(f"Unidade '{to_unit}' não encontrada na categoria '{category}'")
        
        # Conversão especial para temperatura
        if category == 'temperature':
            result = cls._convert_temperature(value, from_unit, to_unit)
        else:
            # Conversão padrão via unidade base
            from_factor = units[from_unit]['to_base']
            to_factor = units[to_unit]['to_base']
            
            # Converte para unidade base e depois para unidade destino
            base_value = value * from_factor
            result = base_value / to_factor
        
        return {
            'original_value': value,
            'converted_value': round(result, 6),
            'from_unit': from_unit.upper(),
            'to_unit': to_unit.upper(),
            'from_unit_name': units[from_unit]['name'],
            'to_unit_name': units[to_unit]['name'],
            'category': category_data['name'],
            'formatted_result': cls._format_result(result, to_unit, units[to_unit]['name'])
        }
    
    @classmethod
    def _find_category(cls, from_unit: str, to_unit: str) -> Optional[str]:
        """Encontra categoria baseada nas unidades"""
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        for category, data in cls.UNITS_DATA.items():
            units = data['units']
            if from_unit in units and to_unit in units:
                return category
        return None
    
    @classmethod
    def _convert_temperature(cls, value: float, from_unit: str, to_unit: str) -> float:
        """Conversão especial para temperatura"""
        # Converte para Celsius primeiro
        if from_unit == 'c':
            celsius = value
        elif from_unit == 'f':
            celsius = (value - 32) * 5/9
        elif from_unit == 'k':
            celsius = value - 273.15
        elif from_unit == 'r':
            celsius = (value - 491.67) * 5/9
        else:
            raise ValueError(f"Unidade de temperatura '{from_unit}' não suportada")
        
        # Converte de Celsius para unidade destino
        if to_unit == 'c':
            return celsius
        elif to_unit == 'f':
            return celsius * 9/5 + 32
        elif to_unit == 'k':
            return celsius + 273.15
        elif to_unit == 'r':
            return celsius * 9/5 + 491.67
        else:
            raise ValueError(f"Unidade de temperatura '{to_unit}' não suportada")
    
    @classmethod
    def _format_result(cls, value: float, unit: str, unit_name: str) -> str:
        """Formata resultado com unidade"""
        # Formatação especial para valores muito pequenos ou grandes
        if abs(value) >= 1000000:
            return f"{value:.2e} {unit.upper()} ({unit_name})"
        elif abs(value) < 0.001 and value != 0:
            return f"{value:.2e} {unit.upper()} ({unit_name})"
        else:
            return f"{value:.6g} {unit.upper()} ({unit_name})"

# Funções de conveniência
def convert_units(value: Union[int, float], from_unit: str, to_unit: str, category: Optional[str] = None) -> Dict[str, Any]:
    """
    Função de conveniência para conversão rápida
    
    Args:
        value: Valor a converter
        from_unit: Unidade de origem
        to_unit: Unidade de destino
        category: Categoria (opcional)
    
    Returns:
        Resultado da conversão
    
    Example:
        >>> convert_units(100, 'cm', 'm')
        {'original_value': 100, 'converted_value': 1.0, ...}
    """
    return UnitsConverter.convert(value, from_unit, to_unit, category)

def get_available_units(category: Optional[str] = None) -> Dict:
    """
    Obtém unidades disponíveis
    
    Args:
        category: Categoria específica (opcional)
    
    Returns:
        Dict com unidades disponíveis
    """
    if category:
        return UnitsConverter.get_units_in_category(category)
    else:
        return {cat: data['units'] for cat, data in UnitsConverter.UNITS_DATA.items()}

# Exemplo de uso
if __name__ == "__main__":
    print("📏 Testando UnitsConverter...")
    print("=" * 50)
    
    # Testes por categoria
    test_conversions = [
        # Comprimento
        (100, 'cm', 'm', 'length'),
        (1, 'km', 'mi', 'length'),
        (12, 'in', 'cm', 'length'),
        
        # Peso
        (1, 'kg', 'lb', 'weight'),
        (500, 'g', 'oz', 'weight'),
        (1, 'arroba', 'kg', 'weight'),
        
        # Temperatura
        (100, 'c', 'f', 'temperature'),
        (32, 'f', 'c', 'temperature'),
        (273.15, 'k', 'c', 'temperature'),
        
        # Volume
        (1, 'l', 'gal', 'volume'),
        (1, 'cup', 'ml', 'volume'),
        (1, 'm3', 'l', 'volume'),
        
        # Área
        (1, 'ha', 'm2', 'area'),
        (1, 'ac', 'ha', 'area'),
        
        # Velocidade
        (100, 'km/h', 'mph', 'speed'),
        (1, 'knot', 'km/h', 'speed'),
        
        # Energia
        (1, 'kwh', 'j', 'energy'),
        (1000, 'cal', 'j', 'energy'),
        
        # Potência
        (1, 'hp', 'w', 'power'),
        (100, 'cv', 'kw', 'power'),
    ]
    
    for value, from_unit, to_unit, category in test_conversions:
        try:
            result = UnitsConverter.convert(value, from_unit, to_unit, category)
            print(f"\n🔄 {value} {from_unit.upper()} → {result['formatted_result']}")
            print(f"   Categoria: {result['category']}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    # Lista categorias
    print(f"\n📋 Categorias disponíveis: {UnitsConverter.get_categories()}")
    
    print("\n✅ Testes concluídos!")
