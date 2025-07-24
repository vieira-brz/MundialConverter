from typing import Union, Optional, Dict, Any, List
import re
import math

class NumberConverter:
    """Classe para conversão entre diferentes bases numéricas"""
    
    # Bases suportadas
    SUPPORTED_BASES = {
        'binary': {'base': 2, 'prefix': '0b', 'name': 'Binário', 'chars': '01'},
        'octal': {'base': 8, 'prefix': '0o', 'name': 'Octal', 'chars': '01234567'},
        'decimal': {'base': 10, 'prefix': '', 'name': 'Decimal', 'chars': '0123456789'},
        'hexadecimal': {'base': 16, 'prefix': '0x', 'name': 'Hexadecimal', 'chars': '0123456789ABCDEF'},
        'base32': {'base': 32, 'prefix': '', 'name': 'Base32', 'chars': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'},
        'base64': {'base': 64, 'prefix': '', 'name': 'Base64', 'chars': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'}
    }
    
    @classmethod
    def detect_base(cls, number: str) -> str:
        """Detecta automaticamente a base do número"""
        number = str(number).strip()
        
        # Remove espaços e converte para uppercase para análise
        clean_number = number.replace(' ', '').upper()
        
        # Verifica prefixos
        if clean_number.startswith('0B'):
            return 'binary'
        elif clean_number.startswith('0O'):
            return 'octal'
        elif clean_number.startswith('0X'):
            return 'hexadecimal'
        
        # Verifica caracteres válidos para cada base
        # Remove prefixos para análise
        clean_number = clean_number.lstrip('0B').lstrip('0O').lstrip('0X')
        
        # Binário: apenas 0 e 1
        if re.match(r'^[01]+$', clean_number):
            return 'binary'
        
        # Octal: apenas 0-7
        elif re.match(r'^[0-7]+$', clean_number):
            return 'octal'
        
        # Decimal: apenas 0-9
        elif re.match(r'^[0-9]+$', clean_number):
            return 'decimal'
        
        # Hexadecimal: 0-9, A-F
        elif re.match(r'^[0-9A-F]+$', clean_number):
            return 'hexadecimal'
        
        # Base32: A-Z, 2-7
        elif re.match(r'^[A-Z2-7]+$', clean_number):
            return 'base32'
        
        # Base64: A-Z, a-z, 0-9, +, /
        elif re.match(r'^[A-Za-z0-9+/]+=*$', clean_number):
            return 'base64'
        
        return 'unknown'
    
    @classmethod
    def clean_number(cls, number: str, base: str) -> str:
        """Remove prefixos e limpa o número"""
        number = str(number).strip().upper()
        
        # Remove prefixos conhecidos
        prefixes = ['0B', '0O', '0X']
        for prefix in prefixes:
            if number.startswith(prefix):
                number = number[len(prefix):]
                break
        
        # Remove espaços e caracteres especiais para base64
        if base == 'base64':
            return number.replace(' ', '')
        
        return number.replace(' ', '')
    
    @classmethod
    def validate_number(cls, number: str, base: str) -> bool:
        """Valida se o número é válido para a base especificada"""
        if base not in cls.SUPPORTED_BASES:
            return False
        
        clean_num = cls.clean_number(number, base)
        valid_chars = cls.SUPPORTED_BASES[base]['chars']
        
        # Verifica se todos os caracteres são válidos
        for char in clean_num:
            if char not in valid_chars:
                return False
        
        return True
    
    @classmethod
    def to_decimal(cls, number: str, from_base: str) -> int:
        """Converte de qualquer base para decimal"""
        if from_base not in cls.SUPPORTED_BASES:
            raise ValueError(f"Base não suportada: {from_base}")
        
        clean_num = cls.clean_number(number, from_base)
        
        if not cls.validate_number(number, from_base):
            raise ValueError(f"Número inválido para base {from_base}: {number}")
        
        base_info = cls.SUPPORTED_BASES[from_base]
        base_value = base_info['base']
        
        # Casos especiais para bases não numéricas
        if from_base == 'base32':
            return cls._base32_to_decimal(clean_num)
        elif from_base == 'base64':
            return cls._base64_to_decimal(clean_num)
        
        # Conversão padrão para bases numéricas
        return int(clean_num, base_value)
    
    @classmethod
    def from_decimal(cls, decimal_value: int, to_base: str) -> str:
        """Converte de decimal para qualquer base"""
        if to_base not in cls.SUPPORTED_BASES:
            raise ValueError(f"Base não suportada: {to_base}")
        
        if decimal_value < 0:
            raise ValueError("Números negativos não são suportados")
        
        base_info = cls.SUPPORTED_BASES[to_base]
        
        # Casos especiais
        if to_base == 'decimal':
            return str(decimal_value)
        elif to_base == 'binary':
            return bin(decimal_value)[2:]  # Remove '0b'
        elif to_base == 'octal':
            return oct(decimal_value)[2:]  # Remove '0o'
        elif to_base == 'hexadecimal':
            return hex(decimal_value)[2:].upper()  # Remove '0x' e converte para maiúscula
        elif to_base == 'base32':
            return cls._decimal_to_base32(decimal_value)
        elif to_base == 'base64':
            return cls._decimal_to_base64(decimal_value)
        
        # Conversão genérica para outras bases
        if decimal_value == 0:
            return '0'
        
        chars = base_info['chars']
        base_value = base_info['base']
        result = ''
        
        while decimal_value > 0:
            result = chars[decimal_value % base_value] + result
            decimal_value //= base_value
        
        return result
    
    @classmethod
    def _base32_to_decimal(cls, base32_str: str) -> int:
        """Converte Base32 para decimal"""
        chars = cls.SUPPORTED_BASES['base32']['chars']
        result = 0
        
        for char in base32_str:
            result = result * 32 + chars.index(char)
        
        return result
    
    @classmethod
    def _decimal_to_base32(cls, decimal_value: int) -> str:
        """Converte decimal para Base32"""
        if decimal_value == 0:
            return 'A'
        
        chars = cls.SUPPORTED_BASES['base32']['chars']
        result = ''
        
        while decimal_value > 0:
            result = chars[decimal_value % 32] + result
            decimal_value //= 32
        
        return result
    
    @classmethod
    def _base64_to_decimal(cls, base64_str: str) -> int:
        """Converte Base64 para decimal"""
        chars = cls.SUPPORTED_BASES['base64']['chars']
        result = 0
        
        # Remove padding
        base64_str = base64_str.rstrip('=')
        
        for char in base64_str:
            result = result * 64 + chars.index(char)
        
        return result
    
    @classmethod
    def _decimal_to_base64(cls, decimal_value: int) -> str:
        """Converte decimal para Base64"""
        if decimal_value == 0:
            return 'A'
        
        chars = cls.SUPPORTED_BASES['base64']['chars']
        result = ''
        
        while decimal_value > 0:
            result = chars[decimal_value % 64] + result
            decimal_value //= 64
        
        return result
    
    @classmethod
    def convert(cls, number: str, from_base: str, to_base: str) -> Dict[str, Any]:
        """
        Converte número entre diferentes bases
        
        Args:
            number: Número de origem
            from_base: Base de origem
            to_base: Base de destino
        
        Returns:
            Dict com resultado da conversão
        """
        try:
            # Normaliza nomes das bases
            from_base = from_base.lower()
            to_base = to_base.lower()
            
            # Aliases para bases comuns
            base_aliases = {
                'bin': 'binary', 'oct': 'octal', 'dec': 'decimal', 'hex': 'hexadecimal',
                '2': 'binary', '8': 'octal', '10': 'decimal', '16': 'hexadecimal',
                '32': 'base32', '64': 'base64'
            }
            
            from_base = base_aliases.get(from_base, from_base)
            to_base = base_aliases.get(to_base, to_base)
            
            # Detecta base automaticamente se não especificada
            if from_base == 'auto':
                from_base = cls.detect_base(number)
                if from_base == 'unknown':
                    raise ValueError(f"Não foi possível detectar a base do número: {number}")
            
            # Converte para decimal primeiro
            decimal_value = cls.to_decimal(number, from_base)
            
            # Converte para base de destino
            converted = cls.from_decimal(decimal_value, to_base)
            
            # Adiciona prefixo se necessário
            prefix = cls.SUPPORTED_BASES[to_base]['prefix']
            formatted_result = prefix + converted if prefix else converted
            
            return {
                'original_number': str(number),
                'original_base': from_base,
                'converted_number': converted,
                'target_base': to_base,
                'decimal_value': decimal_value,
                'formatted_result': formatted_result,
                'all_bases': {
                    'binary': cls.from_decimal(decimal_value, 'binary'),
                    'octal': cls.from_decimal(decimal_value, 'octal'),
                    'decimal': str(decimal_value),
                    'hexadecimal': cls.from_decimal(decimal_value, 'hexadecimal'),
                    'base32': cls.from_decimal(decimal_value, 'base32'),
                    'base64': cls.from_decimal(decimal_value, 'base64')
                },
                'with_prefixes': {
                    'binary': '0b' + cls.from_decimal(decimal_value, 'binary'),
                    'octal': '0o' + cls.from_decimal(decimal_value, 'octal'),
                    'decimal': str(decimal_value),
                    'hexadecimal': '0x' + cls.from_decimal(decimal_value, 'hexadecimal'),
                    'base32': cls.from_decimal(decimal_value, 'base32'),
                    'base64': cls.from_decimal(decimal_value, 'base64')
                }
            }
            
        except Exception as e:
            raise ValueError(f"Erro na conversão: {str(e)}")
    
    @classmethod
    def get_supported_bases(cls) -> List[str]:
        """Retorna lista de bases suportadas"""
        return list(cls.SUPPORTED_BASES.keys())
    
    @classmethod
    def get_base_info(cls, base: str) -> Dict[str, Any]:
        """Retorna informações sobre uma base específica"""
        if base not in cls.SUPPORTED_BASES:
            raise ValueError(f"Base não suportada: {base}")
        
        return cls.SUPPORTED_BASES[base].copy()
    
    @classmethod
    def calculate_digits_needed(cls, decimal_value: int, base: str) -> int:
        """Calcula quantos dígitos são necessários para representar um número em uma base"""
        if base not in cls.SUPPORTED_BASES:
            raise ValueError(f"Base não suportada: {base}")
        
        if decimal_value == 0:
            return 1
        
        base_value = cls.SUPPORTED_BASES[base]['base']
        return math.floor(math.log(decimal_value, base_value)) + 1

# Funções de conveniência
def convert_number(number: str, from_base: str, to_base: str) -> Dict[str, Any]:
    """
    Função de conveniência para conversão rápida entre bases
    
    Args:
        number: Número de origem
        from_base: Base de origem (ou 'auto' para detecção automática)
        to_base: Base de destino
    
    Returns:
        Resultado da conversão
    
    Example:
        >>> convert_number('1010', 'binary', 'decimal')
        {'converted_number': '10', 'decimal_value': 10, ...}
    """
    return NumberConverter.convert(number, from_base, to_base)

def detect_number_base(number: str) -> str:
    """
    Detecta automaticamente a base de um número
    
    Args:
        number: Número para analisar
    
    Returns:
        Base detectada
    """
    return NumberConverter.detect_base(number)

def get_all_representations(number: str, from_base: str = 'auto') -> Dict[str, str]:
    """
    Obtém representações do número em todas as bases
    
    Args:
        number: Número de origem
        from_base: Base de origem (padrão: detecção automática)
    
    Returns:
        Dict com número em todas as bases
    """
    result = NumberConverter.convert(number, from_base, 'decimal')
    return result['all_bases']

# Exemplo de uso
if __name__ == "__main__":
    print("🔢 Testando NumberConverter...")
    print("=" * 50)
    
    # Testes de conversão
    test_numbers = [
        ('1010', 'binary', 'decimal'),
        ('255', 'decimal', 'hexadecimal'),
        ('FF', 'hexadecimal', 'binary'),
        ('377', 'octal', 'decimal'),
        ('0x1A', 'auto', 'binary'),
        ('0b1111', 'auto', 'decimal'),
        ('42', 'decimal', 'base32'),
        ('100', 'decimal', 'base64'),
    ]
    
    for number, from_base, to_base in test_numbers:
        try:
            result = NumberConverter.convert(number, from_base, to_base)
            print(f"\n🔄 {number} ({result['original_base'].upper()}) → {result['converted_number']} ({to_base.upper()})")
            print(f"   Decimal: {result['decimal_value']}")
            print(f"   Formatado: {result['formatted_result']}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    # Teste de detecção automática
    print(f"\n🔍 Testando detecção automática:")
    test_detection = ['1010', '0xFF', '0o777', '0b1111', 'HELLO', 'QWE=']
    
    for num in test_detection:
        detected = NumberConverter.detect_base(num)
        print(f"   {num} → {detected}")
    
    # Teste de representações completas
    print(f"\n📊 Representações do número 42:")
    try:
        all_reps = get_all_representations('42', 'decimal')
        for base, value in all_reps.items():
            base_info = NumberConverter.get_base_info(base)
            print(f"   {base_info['name']}: {value}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Lista bases suportadas
    print(f"\n📋 Bases suportadas: {NumberConverter.get_supported_bases()}")
    
    print("\n✅ Testes concluídos!")
