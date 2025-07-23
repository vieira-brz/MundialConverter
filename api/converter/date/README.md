# Date Converter

Conversor robusto de datas entre diferentes formatos e países.

## Características

- ✅ **30+ formatos suportados**: dd/mm/yyyy, yyyy-mm-dd, ISO, timestamps, etc.
- 🌍 **Multi-país**: BR, EUA, UK, DE, FR, ISO
- ⏰ **Suporte a timezone**: Conversão automática de fuso horário
- 🔍 **Detecção automática**: Identifica formato automaticamente
- 📅 **Flexível**: Com ou sem horário

## Uso Rápido

```python
from api.converter.date.date import convert_date

# Conversão simples
result = convert_date("2025-07-23", "BR")
print(result)  # "23/07/2025"

# Com horário
result = convert_date("23/07/2025 15:30", "EUA", include_time=True)
print(result)  # "07/23/2025 15:30:00"
```

## Formatos Suportados

### Entrada (Detecção Automática)
- `23/07/2025`, `23-07-2025`, `23.07.2025`
- `2025-07-23`, `2025/07/23`, `2025.07.23`
- `07/23/2025` (formato americano)
- `2025-07-23T15:30:45` (ISO)
- `23/07/2025 15:30:45.123456`
- `20250723153045` (timestamp)
- E muitos outros...

### Saída por País
- **BR**: `23/07/2025` ou `23/07/2025 15:30:45`
- **EUA**: `07/23/2025` ou `07/23/2025 15:30:45`
- **UK**: `23/07/2025` ou `23/07/2025 15:30:45`
- **DE**: `23.07.2025` ou `23.07.2025 15:30:45`
- **FR**: `23/07/2025` ou `23/07/2025 15:30:45`
- **ISO**: `2025-07-23` ou `2025-07-23T15:30:45`

## API Completa

### Classe DateConverter

```python
from api.converter.date.date import DateConverter
from datetime import datetime

# Parse automático
date_obj = DateConverter.detect_and_parse("23/07/2025")

# Conversão para formato específico
formatted = DateConverter.convert_to_format(date_obj, "EUA", return_hour=True)
```

### Funções de Conveniência

```python
from api.converter.date.date import convert_date, detect_date_format

# Conversão rápida
result = convert_date("2025-07-23", "BR")

# Detecção de formato
format_info = detect_date_format("23/07/2025")
print(format_info)  # "%d/%m/%Y"
```

## Exemplos Avançados

### Processamento em Lote

```python
dates = ["23/07/2025", "2025-07-23", "07/23/2025"]
converted = [convert_date(d, "ISO") for d in dates]
print(converted)  # ['2025-07-23', '2025-07-23', '2025-07-23']
```

### Com Timezone

```python
from datetime import datetime
import pytz

# Data com timezone
date_with_tz = datetime.now(pytz.timezone('America/Sao_Paulo'))
result = DateConverter.convert_to_format(date_with_tz, "EUA", True)
```

### Tratamento de Erros

```python
try:
    result = convert_date("data_inválida", "BR")
except ValueError as e:
    print(f"Erro: {e}")
```

## Testes

Execute o arquivo diretamente para ver exemplos:

```bash
python api/converter/date/date.py
```

## Dependências

- `datetime` (built-in)
- `re` (built-in)
- `pytz` - Para suporte a timezone

```bash
pip install pytz
```
