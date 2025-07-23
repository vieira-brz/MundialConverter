# 🚀 Deployment Guide

Guia completo para usar o MundialConverter em diferentes ambientes de produção.

## 📦 Instalação em Produção

### Método 1: Instalação via Git
```bash
# Clone o repositório
git clone https://github.com/vieira-brz/MundialConverter.git
cd MundialConverter

# Instale as dependências
pip install -r requirements.txt

# Teste a instalação
python -c "from api.converter.date.date import DateConverter; print('✅ Instalação OK!')"
```

### Método 2: Como Submódulo
```bash
# Adicione como submódulo ao seu projeto
git submodule add https://github.com/vieira-brz/MundialConverter.git libs/MundialConverter
git submodule update --init --recursive

# Adicione ao PYTHONPATH
export PYTHONPATH="$PYTHONPATH:./libs/MundialConverter"
```

### Método 3: Cópia Direta
```bash
# Copie apenas os conversores necessários
cp -r MundialConverter/api/converter/date/ seu_projeto/utils/
```

## 🐳 Docker

### Dockerfile Exemplo
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copie os arquivos necessários
COPY requirements.txt .
COPY api/ ./api/

# Instale dependências
RUN pip install --no-cache-dir -r requirements.txt

# Comando padrão
CMD ["python", "-c", "from api.converter.date.date import DateConverter; print('MundialConverter ready!')"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  app:
    build: .
    volumes:
      - ./api:/app/api
    environment:
      - PYTHONPATH=/app
```

## ☁️ Cloud Deployment

### AWS Lambda
```python
# lambda_function.py
import sys
sys.path.append('./libs/MundialConverter')

from api.converter.date.date import DateConverter

def lambda_handler(event, context):
    date_input = event.get('date')
    to_type = event.get('to_type', 'BR')
    
    parsed_date = DateConverter.detect_and_parse(date_input)
    converted = DateConverter.convert_to_format(parsed_date, to_type)
    
    return {
        'statusCode': 200,
        'body': {'converted_date': converted}
    }
```

### Google Cloud Functions
```python
# main.py
from api.converter.date.date import DateConverter

def convert_date(request):
    request_json = request.get_json()
    
    date_input = request_json.get('date')
    to_type = request_json.get('to_type', 'BR')
    
    parsed_date = DateConverter.detect_and_parse(date_input)
    converted = DateConverter.convert_to_format(parsed_date, to_type)
    
    return {'converted_date': converted}
```

### Azure Functions
```python
# __init__.py
import azure.functions as func
from api.converter.date.date import DateConverter

def main(req: func.HttpRequest) -> func.HttpResponse:
    date_input = req.params.get('date')
    to_type = req.params.get('to_type', 'BR')
    
    parsed_date = DateConverter.detect_and_parse(date_input)
    converted = DateConverter.convert_to_format(parsed_date, to_type)
    
    return func.HttpResponse(
        f"{{\"converted_date\": \"{converted}\"}}",
        mimetype="application/json"
    )
```

## 🌐 Web Frameworks

### Flask Integration
```python
from flask import Flask, request, jsonify
from api.converter.date.date import DateConverter

app = Flask(__name__)

@app.route('/convert/date', methods=['POST'])
def convert_date():
    data = request.get_json()
    
    date_input = data.get('date')
    to_type = data.get('to_type', 'BR')
    return_hour = data.get('return_hour', False)
    
    try:
        parsed_date = DateConverter.detect_and_parse(date_input)
        converted = DateConverter.convert_to_format(parsed_date, to_type, return_hour)
        
        return jsonify({
            'success': True,
            'converted_date': converted
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)
```

### FastAPI Integration
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from api.converter.date.date import DateConverter

app = FastAPI(title="MundialConverter API")

class DateRequest(BaseModel):
    date: str
    to_type: str = "BR"
    return_hour: bool = False

@app.post("/convert/date")
async def convert_date(request: DateRequest):
    try:
        parsed_date = DateConverter.detect_and_parse(request.date)
        converted = DateConverter.convert_to_format(
            parsed_date, request.to_type, request.return_hour
        )
        
        return {
            "success": True,
            "converted_date": converted
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### Django Integration
```python
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from api.converter.date.date import DateConverter

@csrf_exempt
def convert_date(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        date_input = data.get('date')
        to_type = data.get('to_type', 'BR')
        return_hour = data.get('return_hour', False)
        
        try:
            parsed_date = DateConverter.detect_and_parse(date_input)
            converted = DateConverter.convert_to_format(parsed_date, to_type, return_hour)
            
            return JsonResponse({
                'success': True,
                'converted_date': converted
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
```

## 📊 Performance e Otimização

### Cache de Timezone
```python
# Para aplicações com muitas conversões, use cache
from functools import lru_cache
import pytz

@lru_cache(maxsize=128)
def get_timezone(tz_name):
    return pytz.timezone(tz_name)

# Use no lugar de pytz.timezone() diretamente
```

### Batch Processing
```python
# Para processar muitas datas de uma vez
def batch_convert_dates(dates_list, to_type="BR", return_hour=False):
    results = []
    
    for date_input in dates_list:
        try:
            parsed_date = DateConverter.detect_and_parse(date_input)
            converted = DateConverter.convert_to_format(parsed_date, to_type, return_hour)
            results.append({
                'input': date_input,
                'output': converted,
                'success': True
            })
        except Exception as e:
            results.append({
                'input': date_input,
                'error': str(e),
                'success': False
            })
    
    return results
```

## 🔒 Segurança

### Validação de Entrada
```python
import re
from datetime import datetime

def validate_date_input(date_input):
    """Valida entrada antes de processar"""
    if not isinstance(date_input, (str, datetime)):
        raise ValueError("Input deve ser string ou datetime")
    
    if isinstance(date_input, str):
        # Remove caracteres perigosos
        cleaned = re.sub(r'[^\d\-/:.T\s]', '', date_input.strip())
        if len(cleaned) > 50:  # Limite de tamanho
            raise ValueError("Input muito longo")
        return cleaned
    
    return date_input
```

### Rate Limiting (Flask)
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/convert/date', methods=['POST'])
@limiter.limit("10 per minute")
def convert_date():
    # ... código da conversão
```

## 📈 Monitoramento

### Logging
```python
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('MundialConverter')

# Usar no código
def convert_with_logging(date_input, to_type):
    logger.info(f"Converting {date_input} to {to_type}")
    
    try:
        result = DateConverter.detect_and_parse(date_input)
        converted = DateConverter.convert_to_format(result, to_type)
        logger.info(f"Conversion successful: {converted}")
        return converted
    except Exception as e:
        logger.error(f"Conversion failed: {str(e)}")
        raise
```

### Métricas (Prometheus)
```python
from prometheus_client import Counter, Histogram, generate_latest

# Métricas
CONVERSION_COUNTER = Counter('conversions_total', 'Total conversions', ['type', 'status'])
CONVERSION_DURATION = Histogram('conversion_duration_seconds', 'Conversion duration')

@CONVERSION_DURATION.time()
def convert_with_metrics(date_input, to_type):
    try:
        result = DateConverter.detect_and_parse(date_input)
        converted = DateConverter.convert_to_format(result, to_type)
        CONVERSION_COUNTER.labels(type=to_type, status='success').inc()
        return converted
    except Exception as e:
        CONVERSION_COUNTER.labels(type=to_type, status='error').inc()
        raise
```

## 🧪 Testes em Produção

### Health Check
```python
@app.route('/health')
def health_check():
    try:
        # Teste básico
        test_date = DateConverter.detect_and_parse("2025-01-01")
        DateConverter.convert_to_format(test_date, "BR")
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500
```

## 🔧 Troubleshooting

### Problemas Comuns

1. **Erro de Timezone**
   ```bash
   pip install pytz --upgrade
   ```

2. **Formato não reconhecido**
   ```python
   # Adicione logs para debug
   logger.debug(f"Trying to parse: {date_input}")
   ```

3. **Performance lenta**
   ```python
   # Use cache para timezones
   # Processe em lotes
   # Considere async para I/O
   ```

---

📞 **Precisa de ajuda?** Abra uma [issue no GitHub](https://github.com/vieira-brz/MundialConverter/issues)!