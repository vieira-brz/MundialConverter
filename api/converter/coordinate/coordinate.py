from typing import Union, Optional, Dict, Any, Tuple
import math
import re

class CoordinateConverter:
    """Classe para conversão entre diferentes sistemas de coordenadas"""
    
    # Constantes para conversões
    EARTH_RADIUS_KM = 6371.0
    EARTH_RADIUS_MI = 3959.0
    
    @classmethod
    def detect_format(cls, coordinate: str) -> str:
        """Detecta o formato da coordenada"""
        coord = str(coordinate).strip().upper()
        
        # Decimal Degrees (DD)
        if re.match(r'^-?\d+\.?\d*$', coord.replace(' ', '')):
            return 'decimal'
        
        # Degrees Minutes Seconds (DMS)
        if re.match(r'^\d+°\s*\d+\'\s*[\d.]+\"?\s*[NSEW]?$', coord):
            return 'dms'
        
        # Degrees Decimal Minutes (DDM)
        if re.match(r'^\d+°\s*[\d.]+\'\s*[NSEW]?$', coord):
            return 'ddm'
        
        # UTM
        if re.match(r'^\d+[A-Z]\s+\d+\s+\d+$', coord):
            return 'utm'
        
        # MGRS
        if re.match(r'^\d+[A-Z][A-Z][A-Z]\d+$', coord):
            return 'mgrs'
        
        return 'unknown'
    
    @classmethod
    def dms_to_decimal(cls, degrees: int, minutes: int, seconds: float, direction: str = '') -> float:
        """
        Converte DMS (Degrees Minutes Seconds) para Decimal
        
        Args:
            degrees: Graus
            minutes: Minutos
            seconds: Segundos
            direction: Direção (N, S, E, W)
        
        Returns:
            Coordenada em decimal
        """
        decimal = degrees + minutes/60 + seconds/3600
        
        if direction.upper() in ['S', 'W']:
            decimal = -decimal
            
        return decimal
    
    @classmethod
    def decimal_to_dms(cls, decimal: float, is_latitude: bool = True) -> Dict[str, Any]:
        """
        Converte Decimal para DMS (Degrees Minutes Seconds)
        
        Args:
            decimal: Coordenada em decimal
            is_latitude: Se é latitude (True) ou longitude (False)
        
        Returns:
            Dict com graus, minutos, segundos e direção
        """
        is_negative = decimal < 0
        decimal = abs(decimal)
        
        degrees = int(decimal)
        minutes_float = (decimal - degrees) * 60
        minutes = int(minutes_float)
        seconds = (minutes_float - minutes) * 60
        
        if is_latitude:
            direction = 'S' if is_negative else 'N'
        else:
            direction = 'W' if is_negative else 'E'
        
        return {
            'degrees': degrees,
            'minutes': minutes,
            'seconds': round(seconds, 2),
            'direction': direction,
            'formatted': f"{degrees}° {minutes}' {seconds:.2f}\" {direction}"
        }
    
    @classmethod
    def ddm_to_decimal(cls, degrees: int, minutes: float, direction: str = '') -> float:
        """
        Converte DDM (Degrees Decimal Minutes) para Decimal
        
        Args:
            degrees: Graus
            minutes: Minutos decimais
            direction: Direção (N, S, E, W)
        
        Returns:
            Coordenada em decimal
        """
        decimal = degrees + minutes/60
        
        if direction.upper() in ['S', 'W']:
            decimal = -decimal
            
        return decimal
    
    @classmethod
    def decimal_to_ddm(cls, decimal: float, is_latitude: bool = True) -> Dict[str, Any]:
        """
        Converte Decimal para DDM (Degrees Decimal Minutes)
        
        Args:
            decimal: Coordenada em decimal
            is_latitude: Se é latitude (True) ou longitude (False)
        
        Returns:
            Dict com graus, minutos decimais e direção
        """
        is_negative = decimal < 0
        decimal = abs(decimal)
        
        degrees = int(decimal)
        minutes = (decimal - degrees) * 60
        
        if is_latitude:
            direction = 'S' if is_negative else 'N'
        else:
            direction = 'W' if is_negative else 'E'
        
        return {
            'degrees': degrees,
            'minutes': round(minutes, 4),
            'direction': direction,
            'formatted': f"{degrees}° {minutes:.4f}' {direction}"
        }
    
    @classmethod
    def parse_dms_string(cls, dms_str: str) -> Tuple[int, int, float, str]:
        """Parse string DMS para componentes"""
        dms_str = dms_str.strip().upper()
        
        # Regex para capturar DMS
        pattern = r'(\d+)°?\s*(\d+)\'?\s*([\d.]+)\"?\s*([NSEW])?'
        match = re.match(pattern, dms_str)
        
        if match:
            degrees = int(match.group(1))
            minutes = int(match.group(2))
            seconds = float(match.group(3))
            direction = match.group(4) or ''
            return degrees, minutes, seconds, direction
        
        raise ValueError(f"Formato DMS inválido: {dms_str}")
    
    @classmethod
    def parse_ddm_string(cls, ddm_str: str) -> Tuple[int, float, str]:
        """Parse string DDM para componentes"""
        ddm_str = ddm_str.strip().upper()
        
        # Regex para capturar DDM
        pattern = r'(\d+)°?\s*([\d.]+)\'?\s*([NSEW])?'
        match = re.match(pattern, ddm_str)
        
        if match:
            degrees = int(match.group(1))
            minutes = float(match.group(2))
            direction = match.group(3) or ''
            return degrees, minutes, direction
        
        raise ValueError(f"Formato DDM inválido: {ddm_str}")
    
    @classmethod
    def calculate_distance(cls, lat1: float, lon1: float, lat2: float, lon2: float, unit: str = 'km') -> float:
        """
        Calcula distância entre duas coordenadas usando fórmula de Haversine
        
        Args:
            lat1, lon1: Primeira coordenada
            lat2, lon2: Segunda coordenada
            unit: Unidade ('km' ou 'mi')
        
        Returns:
            Distância entre as coordenadas
        """
        # Converte para radianos
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Diferenças
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        # Fórmula de Haversine
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Distância
        radius = cls.EARTH_RADIUS_MI if unit.lower() == 'mi' else cls.EARTH_RADIUS_KM
        distance = radius * c
        
        return round(distance, 2)
    
    @classmethod
    def calculate_bearing(cls, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calcula o bearing (direção) entre duas coordenadas
        
        Args:
            lat1, lon1: Primeira coordenada
            lat2, lon2: Segunda coordenada
        
        Returns:
            Bearing em graus (0-360)
        """
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        dlon_rad = math.radians(lon2 - lon1)
        
        y = math.sin(dlon_rad) * math.cos(lat2_rad)
        x = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon_rad)
        
        bearing_rad = math.atan2(y, x)
        bearing_deg = math.degrees(bearing_rad)
        
        # Normaliza para 0-360
        bearing_deg = (bearing_deg + 360) % 360
        
        return round(bearing_deg, 2)
    
    @classmethod
    def get_cardinal_direction(cls, bearing: float) -> str:
        """Converte bearing para direção cardinal"""
        directions = [
            "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
        ]
        
        index = round(bearing / 22.5) % 16
        return directions[index]
    
    @classmethod
    def convert(cls, coordinate: str, from_format: str, to_format: str, is_latitude: bool = True) -> Dict[str, Any]:
        """
        Converte coordenada entre diferentes formatos
        
        Args:
            coordinate: Coordenada de origem
            from_format: Formato de origem (decimal, dms, ddm)
            to_format: Formato de destino (decimal, dms, ddm)
            is_latitude: Se é latitude (True) ou longitude (False)
        
        Returns:
            Dict com resultado da conversão
        """
        try:
            from_format = from_format.lower()
            to_format = to_format.lower()
            
            # Converte para decimal primeiro
            if from_format == 'decimal':
                decimal_value = float(coordinate)
            elif from_format == 'dms':
                degrees, minutes, seconds, direction = cls.parse_dms_string(coordinate)
                decimal_value = cls.dms_to_decimal(degrees, minutes, seconds, direction)
            elif from_format == 'ddm':
                degrees, minutes, direction = cls.parse_ddm_string(coordinate)
                decimal_value = cls.ddm_to_decimal(degrees, minutes, direction)
            else:
                raise ValueError(f"Formato de origem não suportado: {from_format}")
            
            # Converte para formato de destino
            if to_format == 'decimal':
                converted = str(decimal_value)
                formatted = f"{decimal_value:.6f}"
            elif to_format == 'dms':
                dms_data = cls.decimal_to_dms(decimal_value, is_latitude)
                converted = dms_data['formatted']
                formatted = converted
            elif to_format == 'ddm':
                ddm_data = cls.decimal_to_ddm(decimal_value, is_latitude)
                converted = ddm_data['formatted']
                formatted = converted
            else:
                raise ValueError(f"Formato de destino não suportado: {to_format}")
            
            return {
                'original_coordinate': str(coordinate),
                'original_format': from_format,
                'converted_coordinate': converted,
                'target_format': to_format,
                'decimal_value': decimal_value,
                'formatted_result': formatted,
                'is_latitude': is_latitude,
                'all_formats': {
                    'decimal': f"{decimal_value:.6f}",
                    'dms': cls.decimal_to_dms(decimal_value, is_latitude)['formatted'],
                    'ddm': cls.decimal_to_ddm(decimal_value, is_latitude)['formatted']
                }
            }
            
        except Exception as e:
            raise ValueError(f"Erro na conversão de coordenada: {str(e)}")
    
    @classmethod
    def convert_coordinate_pair(cls, lat: str, lon: str, from_format: str, to_format: str) -> Dict[str, Any]:
        """
        Converte um par de coordenadas (latitude, longitude)
        
        Args:
            lat: Latitude
            lon: Longitude
            from_format: Formato de origem
            to_format: Formato de destino
        
        Returns:
            Dict com ambas as coordenadas convertidas
        """
        lat_result = cls.convert(lat, from_format, to_format, is_latitude=True)
        lon_result = cls.convert(lon, from_format, to_format, is_latitude=False)
        
        return {
            'latitude': lat_result,
            'longitude': lon_result,
            'coordinate_pair': {
                'original': f"{lat}, {lon}",
                'converted': f"{lat_result['converted_coordinate']}, {lon_result['converted_coordinate']}",
                'decimal': f"{lat_result['decimal_value']:.6f}, {lon_result['decimal_value']:.6f}"
            }
        }
    
    @classmethod
    def get_supported_formats(cls) -> list:
        """Retorna lista de formatos suportados"""
        return ['decimal', 'dms', 'ddm']

# Funções de conveniência
def convert_coordinate(coordinate: str, from_format: str, to_format: str, is_latitude: bool = True) -> Dict[str, Any]:
    """
    Função de conveniência para conversão rápida de coordenadas
    
    Args:
        coordinate: Coordenada de origem
        from_format: Formato de origem
        to_format: Formato de destino
        is_latitude: Se é latitude ou longitude
    
    Returns:
        Resultado da conversão
    
    Example:
        >>> convert_coordinate('40.7128', 'decimal', 'dms')
        {'converted_coordinate': "40° 42' 46.08\" N", ...}
    """
    return CoordinateConverter.convert(coordinate, from_format, to_format, is_latitude)

def convert_coordinate_pair(lat: str, lon: str, from_format: str, to_format: str) -> Dict[str, Any]:
    """
    Converte par de coordenadas
    
    Args:
        lat: Latitude
        lon: Longitude
        from_format: Formato de origem
        to_format: Formato de destino
    
    Returns:
        Resultado da conversão do par
    """
    return CoordinateConverter.convert_coordinate_pair(lat, lon, from_format, to_format)

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float, unit: str = 'km') -> float:
    """
    Calcula distância entre duas coordenadas
    
    Args:
        lat1, lon1: Primeira coordenada
        lat2, lon2: Segunda coordenada
        unit: Unidade ('km' ou 'mi')
    
    Returns:
        Distância entre as coordenadas
    """
    return CoordinateConverter.calculate_distance(lat1, lon1, lat2, lon2, unit)

def calculate_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> Dict[str, Any]:
    """
    Calcula bearing entre duas coordenadas
    
    Args:
        lat1, lon1: Primeira coordenada
        lat2, lon2: Segunda coordenada
    
    Returns:
        Dict com bearing em graus e direção cardinal
    """
    bearing = CoordinateConverter.calculate_bearing(lat1, lon1, lat2, lon2)
    cardinal = CoordinateConverter.get_cardinal_direction(bearing)
    
    return {
        'bearing_degrees': bearing,
        'cardinal_direction': cardinal,
        'formatted': f"{bearing}° ({cardinal})"
    }

# Exemplo de uso
if __name__ == "__main__":
    print("🗺️ Testando CoordinateConverter...")
    print("=" * 50)
    
    # Testes de conversão
    test_coordinates = [
        ('40.7128', 'decimal', 'dms', True),   # Latitude NYC
        ('-74.0060', 'decimal', 'dms', False), # Longitude NYC
        ('40° 42\' 46.08" N', 'dms', 'decimal', True),
        ('74° 0\' 21.60" W', 'dms', 'decimal', False),
        ('40.7128', 'decimal', 'ddm', True),
        ('40° 42.768\' N', 'ddm', 'decimal', True),
    ]
    
    for coord, from_fmt, to_fmt, is_lat in test_coordinates:
        try:
            result = CoordinateConverter.convert(coord, from_fmt, to_fmt, is_lat)
            coord_type = "Latitude" if is_lat else "Longitude"
            print(f"\n🔄 {coord_type}: {coord} ({from_fmt.upper()}) → {result['converted_coordinate']} ({to_fmt.upper()})")
            print(f"   Decimal: {result['decimal_value']:.6f}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    # Teste de par de coordenadas
    print(f"\n📍 Convertendo par de coordenadas:")
    try:
        pair_result = CoordinateConverter.convert_coordinate_pair(
            '40.7128', '-74.0060', 'decimal', 'dms'
        )
        print(f"   Original: {pair_result['coordinate_pair']['original']}")
        print(f"   Convertido: {pair_result['coordinate_pair']['converted']}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste de distância
    print(f"\n📏 Calculando distância entre NYC e LA:")
    try:
        # NYC: 40.7128, -74.0060
        # LA: 34.0522, -118.2437
        distance_km = calculate_distance(40.7128, -74.0060, 34.0522, -118.2437, 'km')
        distance_mi = calculate_distance(40.7128, -74.0060, 34.0522, -118.2437, 'mi')
        print(f"   Distância: {distance_km} km ({distance_mi} milhas)")
        
        bearing_info = calculate_bearing(40.7128, -74.0060, 34.0522, -118.2437)
        print(f"   Direção: {bearing_info['formatted']}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Lista formatos suportados
    print(f"\n📋 Formatos suportados: {CoordinateConverter.get_supported_formats()}")
    
    print("\n✅ Testes concluídos!")
