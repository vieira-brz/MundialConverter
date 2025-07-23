# 🚀 Getting Started

Guia rápido para começar a usar o MundialConverter em seus projetos Python.

## 📋 Pré-requisitos

- Python 3.7+
- pip (gerenciador de pacotes Python)
- Git (opcional, para clonar o repositório)

## ⚡ Instalação Rápida

### Opção 1: Clone do GitHub
```bash
# Clone o repositório
git clone https://github.com/vieira-brz/MundialConverter.git
cd MundialConverter

# Instale as dependências
pip install -r requirements.txt
```

### Opção 2: Download Direto
1. Baixe o ZIP do projeto
2. Extraia para uma pasta
3. Execute: `pip install -r requirements.txt`

## 🎯 Primeiro Uso

### Teste Básico
```python
# Teste se está funcionando
from api.converter.date.date import DateConverter

# Conversão simples
date_input = "23/07/2025"
parsed_date = DateConverter.detect_and_parse(date_input)
converted = DateConverter.convert_to_format(parsed_date, "EUA")

print(f"Original: {date_input}")
print(f"Convertido: {converted}")  # 07/23/2025
```

## 📅 Date Converter - Exemplos Práticos

### Conversão Básica de Formatos
```python
from api.converter.date.date import DateConverter

# Diferentes formatos de entrada
dates_to_test = [
    "23/07/2025",           # Formato brasileiro
    "2025-07-23",           # Formato ISO
    "07/23/2025",           # Formato americano
    "23-07-2025 15:30",     # Com horário
    "2025-07-23T15:30:45",  # ISO com horário
    "23.07.2025",           # Formato alemão
]

for date_str in dates_to_test:
    try:
        # Detecta automaticamente o formato
        parsed = DateConverter.detect_and_parse(date_str)
        
        # Converte para diferentes países
        br_format = DateConverter.convert_to_format(parsed, "BR")
        usa_format = DateConverter.convert_to_format(parsed, "EUA")
        iso_format = DateConverter.convert_to_format(parsed, "ISO")
        
        print(f"Original: {date_str}")
        print(f"  BR:  {br_format}")
        print(f"  EUA: {usa_format}")
        print(f"  ISO: {iso_format}")
        print("-" * 40)
        
    except Exception as e:
        print(f"Erro ao processar {date_str}: {e}")
```

### Conversão com Horário
```python
from api.converter.date.date import DateConverter

# Data com horário
date_with_time = "2025-07-23 15:30:45"
parsed_date = DateConverter.detect_and_parse(date_with_time)

# Converter mantendo o horário
br_with_time = DateConverter.convert_to_format(parsed_date, "BR", return_hour=True)
usa_with_time = DateConverter.convert_to_format(parsed_date, "EUA", return_hour=True)

print(f"Original: {date_with_time}")
print(f"BR com horário: {br_with_time}")   # 23/07/2025 15:30:45
print(f"EUA com horário: {usa_with_time}") # 07/23/2025 15:30:45

# Converter só a data (sem horário)
br_date_only = DateConverter.convert_to_format(parsed_date, "BR", return_hour=False)
print(f"BR só data: {br_date_only}")      # 23/07/2025
```

### Trabalhando com Timezones
```python
from api.converter.date.date import DateConverter
from datetime import datetime
import pytz

# Data atual em UTC
utc_now = datetime.now(pytz.UTC)
print(f"UTC: {utc_now}")

# Converter para diferentes fusos
br_time = DateConverter.convert_to_format(utc_now, "BR", return_hour=True)
usa_time = DateConverter.convert_to_format(utc_now, "EUA", return_hour=True)
uk_time = DateConverter.convert_to_format(utc_now, "UK", return_hour=True)

print(f"Brasil: {br_time}")
print(f"EUA: {usa_time}")
print(f"Reino Unido: {uk_time}")
```

## 🔧 Integração em Projetos

### Função Utilitária
```python
# utils/date_utils.py
from api.converter.date.date import DateConverter

def normalize_date(date_input, target_country="BR", include_time=False):
    """
    Normaliza uma data para o formato do país especificado
    
    Args:
        date_input: Data em qualquer formato suportado
        target_country: País de destino (BR, EUA, UK, etc.)
        include_time: Se deve incluir horário na saída
    
    Returns:
        String com a data formatada
    """
    try:
        parsed_date = DateConverter.detect_and_parse(date_input)
        return DateConverter.convert_to_format(parsed_date, target_country, include_time)
    except Exception as e:
        raise ValueError(f"Não foi possível converter a data '{date_input}': {e}")

# Exemplo de uso
if __name__ == "__main__":
    # Testes
    test_dates = ["23/07/2025", "2025-07-23", "07/23/2025"]
    
    for date in test_dates:
        normalized = normalize_date(date, "BR")
        print(f"{date} → {normalized}")
```

### Processamento em Lote
```python
# batch_processor.py
from api.converter.date.date import DateConverter
import pandas as pd

def process_date_column(df, date_column, target_country="BR", include_time=False):
    """
    Processa uma coluna de datas em um DataFrame
    
    Args:
        df: DataFrame do pandas
        date_column: Nome da coluna com as datas
        target_country: País de destino
        include_time: Se deve incluir horário
    
    Returns:
        DataFrame com coluna adicional de datas convertidas
    """
    def convert_date(date_value):
        try:
            if pd.isna(date_value):
                return None
            parsed = DateConverter.detect_and_parse(str(date_value))
            return DateConverter.convert_to_format(parsed, target_country, include_time)
        except:
            return None
    
    df[f'{date_column}_converted'] = df[date_column].apply(convert_date)
    return df

# Exemplo de uso
if __name__ == "__main__":
    # Criar DataFrame de exemplo
    data = {
        'id': [1, 2, 3, 4],
        'date_field': ['23/07/2025', '2025-07-23', '07/23/2025', '23-07-2025']
    }
    
    df = pd.DataFrame(data)
    print("DataFrame original:")
    print(df)
    
    # Processar datas
    df_processed = process_date_column(df, 'date_field', 'BR')
    print("\nDataFrame processado:")
    print(df_processed)
```

## 🛡️ Tratamento de Erros

```python
from api.converter.date.date import DateConverter

def safe_date_conversion(date_input, target_country="BR", default_value=None):
    """
    Conversão segura com tratamento de erros
    """
    try:
        parsed_date = DateConverter.detect_and_parse(date_input)
        return DateConverter.convert_to_format(parsed_date, target_country)
    except Exception as e:
        print(f"Erro ao converter '{date_input}': {e}")
        return default_value

# Exemplos de uso
test_cases = [
    "23/07/2025",      # Válido
    "invalid-date",    # Inválido
    "2025-13-45",      # Data impossível
    "23/07/25",        # Válido (ano de 2 dígitos)
    "",                 # Vazio
    None                # None
]

for test_case in test_cases:
    result = safe_date_conversion(test_case, "BR", "Data inválida")
    print(f"{test_case} → {result}")
```

## 📊 Validação e Debugging

```python
from api.converter.date.date import DateConverter

def debug_date_parsing(date_input):
    """
    Função para debugar problemas de parsing
    """
    print(f"Tentando fazer parse de: '{date_input}'")
    print(f"Tipo: {type(date_input)}")
    
    try:
        # Tenta fazer o parse
        parsed = DateConverter.detect_and_parse(date_input)
        print(f"✅ Parse bem-sucedido: {parsed}")
        print(f"Ano: {parsed.year}, Mês: {parsed.month}, Dia: {parsed.day}")
        
        if parsed.hour or parsed.minute or parsed.second:
            print(f"Horário: {parsed.hour:02d}:{parsed.minute:02d}:{parsed.second:02d}")
        
        # Testa conversões
        countries = ['BR', 'EUA', 'UK', 'ISO']
        for country in countries:
            try:
                converted = DateConverter.convert_to_format(parsed, country)
                print(f"  {country}: {converted}")
            except Exception as e:
                print(f"  {country}: ERRO - {e}")
                
    except Exception as e:
        print(f"❌ Erro no parse: {e}")
        print("Formatos suportados:")
        print("  - dd/mm/yyyy (23/07/2025)")
        print("  - yyyy-mm-dd (2025-07-23)")
        print("  - mm/dd/yyyy (07/23/2025)")
        print("  - dd-mm-yyyy (23-07-2025)")
        print("  - E muitos outros...")

# Teste com diferentes entradas
test_inputs = [
    "23/07/2025",
    "2025-07-23T15:30:45",
    "invalid",
    "23.07.2025",
    "07/23/2025 3:30 PM"
]

for test_input in test_inputs:
    debug_date_parsing(test_input)
    print("-" * 50)
```

## 🎨 Casos de Uso Avançados

### API REST Simples
```python
# simple_api.py
from flask import Flask, request, jsonify
from api.converter.date.date import DateConverter

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_date_api():
    data = request.get_json()
    
    date_input = data.get('date')
    target_country = data.get('country', 'BR')
    include_time = data.get('include_time', False)
    
    if not date_input:
        return jsonify({'error': 'Campo "date" é obrigatório'}), 400
    
    try:
        parsed_date = DateConverter.detect_and_parse(date_input)
        converted = DateConverter.convert_to_format(parsed_date, target_country, include_time)
        
        return jsonify({
            'success': True,
            'input': date_input,
            'output': converted,
            'country': target_country
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)
```

### Script de Linha de Comando
```python
#!/usr/bin/env python3
# date_converter_cli.py
import argparse
from api.converter.date.date import DateConverter

def main():
    parser = argparse.ArgumentParser(description='Conversor de datas MundialConverter')
    parser.add_argument('date', help='Data para converter')
    parser.add_argument('--country', '-c', default='BR', 
                       choices=['BR', 'EUA', 'UK', 'DE', 'FR', 'ISO'],
                       help='País de destino (padrão: BR)')
    parser.add_argument('--time', '-t', action='store_true',
                       help='Incluir horário na saída')
    
    args = parser.parse_args()
    
    try:
        parsed_date = DateConverter.detect_and_parse(args.date)
        converted = DateConverter.convert_to_format(parsed_date, args.country, args.time)
        
        print(f"Entrada: {args.date}")
        print(f"Saída ({args.country}): {converted}")
        
    except Exception as e:
        print(f"Erro: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
```

Uso do CLI:
```bash
python date_converter_cli.py "23/07/2025" --country EUA
python date_converter_cli.py "2025-07-23 15:30" --country BR --time
```

## 🔍 Próximos Passos

1. **Explore outros conversores** (quando disponíveis):
   - Currency Converter
   - Units Converter
   - Text Converter

2. **Leia a documentação completa**:
   - [Date Converter README](../api/converter/date/README.md)
   - [Deployment Guide](./deployment.md)

3. **Contribua com o projeto**:
   - Reporte bugs
   - Sugira novos formatos
   - Adicione novos conversores

---

🎉 **Parabéns!** Você já sabe o básico do MundialConverter. Para dúvidas, consulte a [documentação completa](../README.md) ou abra uma [issue no GitHub](https://github.com/vieira-brz/MundialConverter/issues).