from flask import Flask, request, jsonify
from datetime import datetime
import re
from typing import Union, Optional, Dict, Any
import pytz

app = Flask(__name__)

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

@app.route('/api/converter/date', methods=['POST', 'GET'])
def convert_date():
    """
    Endpoint principal para conversão de datas
    
    Parâmetros:
    - date: string ou datetime (obrigatório)
    - to_type: 'BR', 'EUA', 'UK', 'DE', 'FR', 'ISO' (padrão: 'BR')
    - return_hour: True/False (padrão: False)
    
    Exemplo de uso:
    POST /api/converter/date
    {
        "date": "2025-07-23 15:30:45",
        "to_type": "BR",
        "return_hour": true
    }
    """
    try:
        # Obtém parâmetros da requisição
        if request.method == 'POST':
            data = request.get_json() or {}
        else:
            data = request.args.to_dict()
        
        # Parâmetros obrigatórios e opcionais
        date_input = data.get('date')
        to_type = data.get('to_type', 'BR').upper()
        return_hour = str(data.get('return_hour', 'false')).lower() in ['true', '1', 'yes']
        
        # Validações
        if not date_input:
            return jsonify({
                'error': 'Parâmetro "date" é obrigatório',
                'example': {
                    'date': '2025-07-23 15:30:45',
                    'to_type': 'BR',
                    'return_hour': True
                }
            }), 400
        
        # Detecta e faz parse da data
        parsed_date = DateConverter.detect_and_parse(date_input)
        
        if parsed_date is None:
            return jsonify({
                'error': f'Não foi possível interpretar a data: "{date_input}"',
                'supported_formats': [
                    'dd/mm/yyyy', 'dd-mm-yyyy', 'yyyy-mm-dd',
                    'dd/mm/yyyy hh:mm:ss', 'yyyy-mm-ddThh:mm:ss',
                    'mm/dd/yyyy (formato americano)', 'timestamp', 'etc.'
                ]
            }), 400
        
        # Converte para o formato desejado
        try:
            converted_date = DateConverter.convert_to_format(parsed_date, to_type, return_hour)
        except ValueError as e:
            return jsonify({
                'error': str(e),
                'available_types': list(DateConverter.COUNTRY_FORMATS.keys())
            }), 400
        
        # Resposta de sucesso
        return jsonify({
            'success': True,
            'input': {
                'original': date_input,
                'parsed': parsed_date.isoformat(),
                'detected_format': 'auto-detected'
            },
            'output': {
                'converted': converted_date,
                'format': to_type,
                'with_hour': return_hour,
                'timezone': DateConverter.COUNTRY_FORMATS[to_type]['timezone']
            },
            'metadata': {
                'conversion_time': datetime.now().isoformat(),
                'api_version': '1.0'
            }
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro interno: {str(e)}',
            'type': type(e).__name__
        }), 500

@app.route('/api/converter/date/formats', methods=['GET'])
def get_supported_formats():
    """
    Retorna todos os formatos e tipos suportados
    """
    return jsonify({
        'supported_countries': list(DateConverter.COUNTRY_FORMATS.keys()),
        'country_details': DateConverter.COUNTRY_FORMATS,
        'supported_input_formats': [
            'dd/mm/yyyy', 'dd-mm-yyyy', 'yyyy-mm-dd', 'yyyy/mm/dd',
            'mm/dd/yyyy', 'dd.mm.yyyy', 'yyyy.mm.dd',
            'dd/mm/yyyy hh:mm:ss', 'yyyy-mm-dd hh:mm:ss',
            'yyyy-mm-ddThh:mm:ss', 'yyyy-mm-ddThh:mm:ss.fZ',
            'timestamp formats', 'and many more...'
        ],
        'examples': {
            'basic_conversion': {
                'url': '/api/converter/date',
                'method': 'POST',
                'body': {
                    'date': '2025-07-23',
                    'to_type': 'BR'
                }
            },
            'with_time': {
                'url': '/api/converter/date',
                'method': 'POST', 
                'body': {
                    'date': '23/07/2025 15:30:45',
                    'to_type': 'EUA',
                    'return_hour': True
                }
            }
        }
    })

@app.route('/api/converter/date/test', methods=['GET'])
def test_conversions():
    """
    Endpoint de teste com exemplos de conversões
    """
    test_dates = [
        '23/07/2025',
        '2025-07-23 15:30:45',
        '07/23/2025',
        '23-07-2025 15:30',
        '2025/07/23',
        '23.07.2025',
        '20250723'
    ]
    
    results = []
    
    for test_date in test_dates:
        parsed = DateConverter.detect_and_parse(test_date)
        if parsed:
            conversions = {}
            for country in ['BR', 'EUA', 'ISO']:
                try:
                    conversions[country] = {
                        'date_only': DateConverter.convert_to_format(parsed, country, False),
                        'with_time': DateConverter.convert_to_format(parsed, country, True)
                    }
                except:
                    conversions[country] = 'Error'
            
            results.append({
                'input': test_date,
                'parsed': parsed.isoformat(),
                'conversions': conversions
            })
        else:
            results.append({
                'input': test_date,
                'parsed': None,
                'error': 'Could not parse'
            })
    
    return jsonify({
        'test_results': results,
        'total_tests': len(test_dates)
    })

if __name__ == '__main__':
    app.run(debug=True)
