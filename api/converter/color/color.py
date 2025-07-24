from typing import Union, Optional, Dict, Any, Tuple
import re
import colorsys

class ColorConverter:
    """Classe para conversão entre diferentes formatos de cores"""
    
    # Cores nomeadas comuns
    NAMED_COLORS = {
        'red': '#FF0000',
        'green': '#008000',
        'blue': '#0000FF',
        'white': '#FFFFFF',
        'black': '#000000',
        'yellow': '#FFFF00',
        'cyan': '#00FFFF',
        'magenta': '#FF00FF',
        'silver': '#C0C0C0',
        'gray': '#808080',
        'maroon': '#800000',
        'olive': '#808000',
        'lime': '#00FF00',
        'aqua': '#00FFFF',
        'teal': '#008080',
        'navy': '#000080',
        'fuchsia': '#FF00FF',
        'purple': '#800080',
        'orange': '#FFA500',
        'pink': '#FFC0CB',
        'brown': '#A52A2A',
        'gold': '#FFD700',
        'violet': '#EE82EE',
        'indigo': '#4B0082',
        'turquoise': '#40E0D0',
        'coral': '#FF7F50',
        'salmon': '#FA8072',
        'khaki': '#F0E68C',
        'lavender': '#E6E6FA',
        'plum': '#DDA0DD'
    }
    
    @classmethod
    def detect_format(cls, color: str) -> str:
        """Detecta o formato da cor"""
        color = str(color).strip().lower()
        
        # HEX
        if re.match(r'^#?[0-9a-f]{6}$', color) or re.match(r'^#?[0-9a-f]{3}$', color):
            return 'hex'
        
        # RGB
        if re.match(r'^rgb\s*\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)$', color):
            return 'rgb'
        
        # RGBA
        if re.match(r'^rgba\s*\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[\d.]+\s*\)$', color):
            return 'rgba'
        
        # HSL
        if re.match(r'^hsl\s*\(\s*\d+\s*,\s*\d+%?\s*,\s*\d+%?\s*\)$', color):
            return 'hsl'
        
        # HSLA
        if re.match(r'^hsla\s*\(\s*\d+\s*,\s*\d+%?\s*,\s*\d+%?\s*,\s*[\d.]+\s*\)$', color):
            return 'hsla'
        
        # HSV/HSB
        if re.match(r'^hsv\s*\(\s*\d+\s*,\s*\d+%?\s*,\s*\d+%?\s*\)$', color):
            return 'hsv'
        
        # CMYK
        if re.match(r'^cmyk\s*\(\s*\d+%?\s*,\s*\d+%?\s*,\s*\d+%?\s*,\s*\d+%?\s*\)$', color):
            return 'cmyk'
        
        # Nome da cor
        if color in cls.NAMED_COLORS:
            return 'name'
        
        return 'unknown'
    
    @classmethod
    def parse_color(cls, color: str) -> Tuple[int, int, int, float]:
        """Converte qualquer formato para RGB + Alpha"""
        color = str(color).strip().lower()
        format_type = cls.detect_format(color)
        
        if format_type == 'hex':
            return cls._parse_hex(color)
        elif format_type == 'rgb':
            return cls._parse_rgb(color)
        elif format_type == 'rgba':
            return cls._parse_rgba(color)
        elif format_type == 'hsl':
            return cls._parse_hsl(color)
        elif format_type == 'hsla':
            return cls._parse_hsla(color)
        elif format_type == 'hsv':
            return cls._parse_hsv(color)
        elif format_type == 'cmyk':
            return cls._parse_cmyk(color)
        elif format_type == 'name':
            hex_color = cls.NAMED_COLORS[color]
            return cls._parse_hex(hex_color)
        else:
            raise ValueError(f"Formato de cor não reconhecido: {color}")
    
    @classmethod
    def _parse_hex(cls, hex_color: str) -> Tuple[int, int, int, float]:
        """Parse HEX para RGB"""
        hex_color = hex_color.lstrip('#')
        
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        return (r, g, b, 1.0)
    
    @classmethod
    def _parse_rgb(cls, rgb_str: str) -> Tuple[int, int, int, float]:
        """Parse RGB para RGB"""
        match = re.match(r'rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', rgb_str)
        if match:
            r, g, b = map(int, match.groups())
            return (r, g, b, 1.0)
        raise ValueError(f"Formato RGB inválido: {rgb_str}")
    
    @classmethod
    def _parse_rgba(cls, rgba_str: str) -> Tuple[int, int, int, float]:
        """Parse RGBA para RGB + Alpha"""
        match = re.match(r'rgba\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)', rgba_str)
        if match:
            r, g, b = map(int, match.groups()[:3])
            a = float(match.groups()[3])
            return (r, g, b, a)
        raise ValueError(f"Formato RGBA inválido: {rgba_str}")
    
    @classmethod
    def _parse_hsl(cls, hsl_str: str) -> Tuple[int, int, int, float]:
        """Parse HSL para RGB"""
        match = re.match(r'hsl\s*\(\s*(\d+)\s*,\s*(\d+)%?\s*,\s*(\d+)%?\s*\)', hsl_str)
        if match:
            h, s, l = map(int, match.groups())
            h = h / 360.0
            s = s / 100.0
            l = l / 100.0
            
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            return (int(r * 255), int(g * 255), int(b * 255), 1.0)
        raise ValueError(f"Formato HSL inválido: {hsl_str}")
    
    @classmethod
    def _parse_hsla(cls, hsla_str: str) -> Tuple[int, int, int, float]:
        """Parse HSLA para RGB + Alpha"""
        match = re.match(r'hsla\s*\(\s*(\d+)\s*,\s*(\d+)%?\s*,\s*(\d+)%?\s*,\s*([\d.]+)\s*\)', hsla_str)
        if match:
            h, s, l = map(int, match.groups()[:3])
            a = float(match.groups()[3])
            
            h = h / 360.0
            s = s / 100.0
            l = l / 100.0
            
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            return (int(r * 255), int(g * 255), int(b * 255), a)
        raise ValueError(f"Formato HSLA inválido: {hsla_str}")
    
    @classmethod
    def _parse_hsv(cls, hsv_str: str) -> Tuple[int, int, int, float]:
        """Parse HSV para RGB"""
        match = re.match(r'hsv\s*\(\s*(\d+)\s*,\s*(\d+)%?\s*,\s*(\d+)%?\s*\)', hsv_str)
        if match:
            h, s, v = map(int, match.groups())
            h = h / 360.0
            s = s / 100.0
            v = v / 100.0
            
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            return (int(r * 255), int(g * 255), int(b * 255), 1.0)
        raise ValueError(f"Formato HSV inválido: {hsv_str}")
    
    @classmethod
    def _parse_cmyk(cls, cmyk_str: str) -> Tuple[int, int, int, float]:
        """Parse CMYK para RGB"""
        match = re.match(r'cmyk\s*\(\s*(\d+)%?\s*,\s*(\d+)%?\s*,\s*(\d+)%?\s*,\s*(\d+)%?\s*\)', cmyk_str)
        if match:
            c, m, y, k = map(int, match.groups())
            c, m, y, k = c/100.0, m/100.0, y/100.0, k/100.0
            
            r = 255 * (1 - c) * (1 - k)
            g = 255 * (1 - m) * (1 - k)
            b = 255 * (1 - y) * (1 - k)
            
            return (int(r), int(g), int(b), 1.0)
        raise ValueError(f"Formato CMYK inválido: {cmyk_str}")
    
    @classmethod
    def to_hex(cls, r: int, g: int, b: int) -> str:
        """Converte RGB para HEX"""
        return f"#{r:02x}{g:02x}{b:02x}".upper()
    
    @classmethod
    def to_rgb(cls, r: int, g: int, b: int) -> str:
        """Converte para RGB string"""
        return f"rgb({r}, {g}, {b})"
    
    @classmethod
    def to_rgba(cls, r: int, g: int, b: int, a: float) -> str:
        """Converte para RGBA string"""
        return f"rgba({r}, {g}, {b}, {a})"
    
    @classmethod
    def to_hsl(cls, r: int, g: int, b: int) -> str:
        """Converte RGB para HSL"""
        h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
        h = int(h * 360)
        s = int(s * 100)
        l = int(l * 100)
        return f"hsl({h}, {s}%, {l}%)"
    
    @classmethod
    def to_hsla(cls, r: int, g: int, b: int, a: float) -> str:
        """Converte RGB para HSLA"""
        h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
        h = int(h * 360)
        s = int(s * 100)
        l = int(l * 100)
        return f"hsla({h}, {s}%, {l}%, {a})"
    
    @classmethod
    def to_hsv(cls, r: int, g: int, b: int) -> str:
        """Converte RGB para HSV"""
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        h = int(h * 360)
        s = int(s * 100)
        v = int(v * 100)
        return f"hsv({h}, {s}%, {v}%)"
    
    @classmethod
    def to_cmyk(cls, r: int, g: int, b: int) -> str:
        """Converte RGB para CMYK"""
        if r == 0 and g == 0 and b == 0:
            return "cmyk(0%, 0%, 0%, 100%)"
        
        c = 1 - (r / 255.0)
        m = 1 - (g / 255.0)
        y = 1 - (b / 255.0)
        
        k = min(c, m, y)
        c = int(((c - k) / (1 - k)) * 100) if k != 1 else 0
        m = int(((m - k) / (1 - k)) * 100) if k != 1 else 0
        y = int(((y - k) / (1 - k)) * 100) if k != 1 else 0
        k = int(k * 100)
        
        return f"cmyk({c}%, {m}%, {y}%, {k}%)"
    
    @classmethod
    def convert(cls, color: str, to_format: str) -> Dict[str, Any]:
        """
        Converte cor entre diferentes formatos
        
        Args:
            color: Cor de origem (qualquer formato suportado)
            to_format: Formato de destino (hex, rgb, rgba, hsl, hsla, hsv, cmyk)
        
        Returns:
            Dict com resultado da conversão
        """
        try:
            # Parse da cor original
            r, g, b, a = cls.parse_color(color)
            original_format = cls.detect_format(color)
            
            # Conversão para formato desejado
            to_format = to_format.lower()
            
            if to_format == 'hex':
                converted = cls.to_hex(r, g, b)
            elif to_format == 'rgb':
                converted = cls.to_rgb(r, g, b)
            elif to_format == 'rgba':
                converted = cls.to_rgba(r, g, b, a)
            elif to_format == 'hsl':
                converted = cls.to_hsl(r, g, b)
            elif to_format == 'hsla':
                converted = cls.to_hsla(r, g, b, a)
            elif to_format == 'hsv' or to_format == 'hsb':
                converted = cls.to_hsv(r, g, b)
            elif to_format == 'cmyk':
                converted = cls.to_cmyk(r, g, b)
            else:
                raise ValueError(f"Formato de destino não suportado: {to_format}")
            
            return {
                'original_color': str(color),
                'original_format': original_format,
                'converted_color': converted,
                'target_format': to_format,
                'rgb_values': {'r': r, 'g': g, 'b': b, 'a': a},
                'all_formats': {
                    'hex': cls.to_hex(r, g, b),
                    'rgb': cls.to_rgb(r, g, b),
                    'rgba': cls.to_rgba(r, g, b, a),
                    'hsl': cls.to_hsl(r, g, b),
                    'hsla': cls.to_hsla(r, g, b, a),
                    'hsv': cls.to_hsv(r, g, b),
                    'cmyk': cls.to_cmyk(r, g, b)
                }
            }
            
        except Exception as e:
            raise ValueError(f"Erro na conversão de cor: {str(e)}")
    
    @classmethod
    def get_supported_formats(cls) -> List[str]:
        """Retorna lista de formatos suportados"""
        return ['hex', 'rgb', 'rgba', 'hsl', 'hsla', 'hsv', 'hsb', 'cmyk', 'name']
    
    @classmethod
    def get_named_colors(cls) -> Dict[str, str]:
        """Retorna dicionário de cores nomeadas"""
        return cls.NAMED_COLORS.copy()

# Funções de conveniência
def convert_color(color: str, to_format: str) -> Dict[str, Any]:
    """
    Função de conveniência para conversão rápida de cores
    
    Args:
        color: Cor de origem
        to_format: Formato de destino
    
    Returns:
        Resultado da conversão
    
    Example:
        >>> convert_color('#FF0000', 'rgb')
        {'original_color': '#FF0000', 'converted_color': 'rgb(255, 0, 0)', ...}
    """
    return ColorConverter.convert(color, to_format)

def get_color_info(color: str) -> Dict[str, Any]:
    """
    Obtém informações completas sobre uma cor
    
    Args:
        color: Cor para analisar
    
    Returns:
        Dict com todas as representações da cor
    """
    return ColorConverter.convert(color, 'hex')  # Usa hex como base para retornar all_formats

# Exemplo de uso
if __name__ == "__main__":
    print("🎨 Testando ColorConverter...")
    print("=" * 50)
    
    # Testes de conversão
    test_colors = [
        ('#FF0000', 'rgb'),
        ('rgb(0, 255, 0)', 'hex'),
        ('blue', 'hsl'),
        ('hsl(240, 100%, 50%)', 'cmyk'),
        ('rgba(255, 0, 255, 0.5)', 'hsla'),
        ('hsv(60, 100%, 100%)', 'rgb'),
        ('cmyk(100%, 0%, 100%, 0%)', 'hex'),
    ]
    
    for color, target_format in test_colors:
        try:
            result = ColorConverter.convert(color, target_format)
            print(f"\n🔄 {color} → {result['converted_color']}")
            print(f"   Formato original: {result['original_format']}")
            print(f"   RGB: {result['rgb_values']}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    # Lista formatos suportados
    print(f"\n📋 Formatos suportados: {ColorConverter.get_supported_formats()}")
    
    print("\n✅ Testes concluídos!")
