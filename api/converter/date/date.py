from datetime import datetime
import re
from typing import Union, Optional, Dict, Any
import pytz

class DateConverter:
    """Classe para conversão robusta de datas entre diferentes formatos"""
    
    # Formatos de data suportados (em ordem de prioridade)
    DATE_FORMATS = [
        # Formatos com hora completa
        '%d/%m/%Y %H:%M:%S.%f',     # 23/07/2025 15:30:45.123456
        '%d/%m/%Y %H:%M:%S',        # 23/07/2025 15:30:45
        '%d/%m/%Y %H:%M',           # 23/07/2025 15:30
        '%d-%m-%Y %H:%M:%S.%f',     # 23-07-2025 15:30:45.123456
        '%d-%m-%Y %H:%M:%S',        # 23-07-2025 15:30:45
        '%d-%m-%Y %H:%M',           # 23-07-2025 15:30
        '%Y-%m-%d %H:%M:%S.%f',     # 2025-07-23 15:30:45.123456
        '%Y-%m-%d %H:%M:%S',        # 2025-07-23 15:30:45
        '%Y-%m-%d %H:%M',           # 2025-07-23 15:30
        '%Y/%m/%d %H:%M:%S.%f',     # 2025/07/23 15:30:45.123456
        '%Y/%m/%d %H:%M:%S',        # 2025/07/23 15:30:45
        '%Y/%m/%d %H:%M',           # 2025/07/23 15:30
        
        # Formatos ISO
        '%Y-%m-%dT%H:%M:%S.%fZ',    # 2025-07-23T15:30:45.123456Z
        '%Y-%m-%dT%H:%M:%SZ',       # 2025-07-23T15:30:45Z
        '%Y-%m-%dT%H:%M:%S.%f',     # 2025-07-23T15:30:45.123456
        '%Y-%m-%dT%H:%M:%S',        # 2025-07-23T15:30:45
        
        # Formatos americanos
        '%m/%d/%Y %H:%M:%S.%f',     # 07/23/2025 15:30:45.123456
        '%m/%d/%Y %H:%M:%S',        # 07/23/2025 15:30:45
        '%m/%d/%Y %H:%M',           # 07/23/2025 15:30
        '%m-%d-%Y %H:%M:%S',        # 07-23-2025 15:30:45
        '%m-%d-%Y %H:%M',           # 07-23-2025 15:30
        
        # Formatos só data
        '%d/%m/%Y',                 # 23/07/2025
        '%d-%m-%Y',                 # 23-07-2025
        '%Y-%m-%d',                 # 2025-07-23
        '%Y/%m/%d',                 # 2025/07/23
        '%m/%d/%Y',                 # 07/23/2025
        '%m-%d-%Y',                 # 07-23-2025
        
        # Formatos com ano de 2 dígitos
        '%d/%m/%y',                 # 23/07/25
        '%d-%m-%y',                 # 23-07-25
        '%y-%m-%d',                 # 25-07-23
        '%y/%m/%d',                 # 25/07/23
        '%m/%d/%y',                 # 07/23/25
        '%m-%d-%y',                 # 07-23-25
        
        # Formatos com pontos
        '%d.%m.%Y',                 # 23.07.2025
        '%Y.%m.%d',                 # 2025.07.23
        '%m.%d.%Y',                 # 07.23.2025
        
        # Formatos timestamp
        '%Y%m%d%H%M%S',             # 20250723153045
        '%Y%m%d',                   # 20250723
    ]
    
    # Mapeamento de países para formatos
    COUNTRY_FORMATS = {
        'BR': {
            'date_format': '%d/%m/%Y',
            'datetime_format': '%d/%m/%Y %H:%M:%S',
            'timezone': 'America/Sao_Paulo'
        },
        'EUA': {
            'date_format': '%m/%d/%Y',
            'datetime_format': '%m/%d/%Y %H:%M:%S',
            'timezone': 'America/New_York'
        },
        'USA': {
            'date_format': '%m/%d/%Y',
            'datetime_format': '%m/%d/%Y %H:%M:%S',
            'timezone': 'America/New_York'
        },
        'UK': {
            'date_format': '%d/%m/%Y',
            'datetime_format': '%d/%m/%Y %H:%M:%S',
            'timezone': 'Europe/London'
        },
        'DE': {
            'date_format': '%d.%m.%Y',
            'datetime_format': '%d.%m.%Y %H:%M:%S',
            'timezone': 'Europe/Berlin'
        },
        'FR': {
            'date_format': '%d/%m/%Y',
            'datetime_format': '%d/%m/%Y %H:%M:%S',
            'timezone': 'Europe/Paris'
        },
        'ISO': {
            'date_format': '%Y-%m-%d',
            'datetime_format': '%Y-%m-%dT%H:%M:%S',
            'timezone': 'UTC'
        }
    }
    
    @classmethod
    def detect_and_parse(cls, date_input: Union[str, datetime]) -> Optional[datetime]:
        """
        Detecta automaticamente o formato da data e faz o parse
        """
        if isinstance(date_input, datetime):
            return date_input
            
        if not isinstance(date_input, str):
            return None
            
        date_str = str(date_input).strip()
        
        # Remove caracteres extras comuns
        date_str = re.sub(r'[^\d\-/:.T\s]', '', date_str)
        
        # Tenta cada formato até encontrar um que funcione
        for fmt in cls.DATE_FORMATS:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return parsed_date
            except ValueError:
                continue
                
        # Tenta parsing mais flexível com regex
        return cls._flexible_parse(date_str)
    
    @classmethod
    def _flexible_parse(cls, date_str: str) -> Optional[datetime]:
        """
        Parse mais flexível usando regex para casos especiais
        """
        # Padrões regex para diferentes formatos
        patterns = [
            # dd/mm/yyyy ou dd-mm-yyyy
            (r'(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})', lambda m: datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))),
            # yyyy/mm/dd ou yyyy-mm-dd
            (r'(\d{4})[/\-.](\d{1,2})[/\-.](\d{1,2})', lambda m: datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))),
            # mm/dd/yyyy ou mm-dd-yyyy (formato americano)
            (r'(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})', lambda m: datetime(int(m.group(3)), int(m.group(1)), int(m.group(2)))),
        ]
        
        for pattern, converter in patterns:
            match = re.search(pattern, date_str)
            if match:
                try:
                    return converter(match)
                except ValueError:
                    continue
                    
        return None
    
    @classmethod
    def convert_to_format(cls, date_obj: datetime, to_type: str, return_hour: bool = False) -> str:
        """
        Converte datetime para o formato do país especificado
        """
        if to_type.upper() not in cls.COUNTRY_FORMATS:
            raise ValueError(f"Tipo '{to_type}' não suportado. Tipos disponíveis: {list(cls.COUNTRY_FORMATS.keys())}")
        
        country_config = cls.COUNTRY_FORMATS[to_type.upper()]
        
        # Aplica timezone se necessário
        if date_obj.tzinfo is None:
            tz = pytz.timezone(country_config['timezone'])
            date_obj = tz.localize(date_obj)
        else:
            tz = pytz.timezone(country_config['timezone'])
            date_obj = date_obj.astimezone(tz)
        
        # Escolhe formato com ou sem hora
        if return_hour:
            format_str = country_config['datetime_format']
        else:
            format_str = country_config['date_format']
            
        return date_obj.strftime(format_str)

# Funções de conveniência para uso direto
def convert_date(date_input: Union[str, datetime], to_country: str = "BR", include_time: bool = False) -> str:
    """
    Função de conveniência para conversão rápida de datas
    
    Args:
        date_input: Data em qualquer formato suportado
        to_country: País de destino (BR, EUA, UK, DE, FR, ISO)
        include_time: Se deve incluir horário na saída
    
    Returns:
        String com a data formatada
    
    Example:
        >>> convert_date("2025-07-23", "BR")
        '23/07/2025'
        >>> convert_date("23/07/2025 15:30", "EUA", True)
        '07/23/2025 15:30:00'
    """
    parsed_date = DateConverter.detect_and_parse(date_input)
    if parsed_date is None:
        raise ValueError(f"Não foi possível interpretar a data: {date_input}")
    
    return DateConverter.convert_to_format(parsed_date, to_country, include_time)

def detect_date_format(date_input: Union[str, datetime]) -> Optional[str]:
    """
    Detecta o formato de uma data sem fazer conversão
    
    Args:
        date_input: Data para detectar o formato
    
    Returns:
        String descrevendo o formato detectado ou None se não reconhecido
    """
    if isinstance(date_input, datetime):
        return "datetime object"
    
    if not isinstance(date_input, str):
        return None
    
    date_str = str(date_input).strip()
    date_str = re.sub(r'[^\d\-/:.T\s]', '', date_str)
    
    # Tenta cada formato
    for fmt in DateConverter.DATE_FORMATS:
        try:
            datetime.strptime(date_str, fmt)
            return fmt
        except ValueError:
            continue
    
    return None

# Exemplo de uso
if __name__ == "__main__":
    # Testes básicos
    test_dates = [
        "23/07/2025",
        "2025-07-23",
        "07/23/2025",
        "23-07-2025 15:30",
        "2025-07-23T15:30:45"
    ]
    
    print("🧪 Testando DateConverter...")
    print("=" * 50)
    
    for date_str in test_dates:
        try:
            print(f"\n📅 Testando: {date_str}")
            
            # Detecta formato
            detected_format = detect_date_format(date_str)
            print(f"   Formato detectado: {detected_format}")
            
            # Converte para diferentes países
            br_format = convert_date(date_str, "BR")
            usa_format = convert_date(date_str, "EUA")
            iso_format = convert_date(date_str, "ISO")
            
            print(f"   BR:  {br_format}")
            print(f"   EUA: {usa_format}")
            print(f"   ISO: {iso_format}")
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    print("\n✅ Testes concluídos!")
