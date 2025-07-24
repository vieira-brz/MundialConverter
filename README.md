# 🌍 MundialConverter

Uma biblioteca Python completa de utilitários de conversão para desenvolvedores. Converta datas, moedas, unidades, texto e muito mais com facilidade e precisão.

## 🚀 Conversores Disponíveis

### 📅 Date Converter
Conversor robusto de datas entre diferentes formatos e países.
- ✅ **30+ formatos suportados**: dd/mm/yyyy, yyyy-mm-dd, ISO, timestamps, etc.
- 🌍 **Multi-país**: BR, EUA, UK, DE, FR, ISO
- ⏰ **Suporte a timezone**: Conversão automática de fuso horário
- 🔍 **Detecção automática**: Identifica formato automaticamente

```python
from api.converter.date.date import DateConverter

# Conversão simples
result = DateConverter.detect_and_parse("23/07/2025")
converted = DateConverter.convert_to_format(result, "EUA")
print(converted)  # 07/23/2025
```

### 💱 Currency Converter
Conversor de moedas com taxas atualizadas em tempo real.
- 💰 **17+ moedas suportadas**: USD, EUR, BRL, GBP, JPY, CAD, AUD, CHF, CNY, INR, KRW, MXN, ARS, CLP, COP, PEN, UYU
- 🔄 **Taxas em tempo real**: APIs atualizadas automaticamente
- 💾 **Cache inteligente**: Evita chamadas desnecessárias
- 🛡️ **Fallback robusto**: Funciona mesmo sem internet
- 💰 **Formatação automática**: Símbolos e formatos por país

```python
from api.converter.currency.currency import convert_currency

# Conversão simples
result = convert_currency(100, "USD", "BRL")
print(result['formatted_result'])  # "R$ 520,00"

# Apenas a taxa
from api.converter.currency.currency import get_exchange_rate
rate = get_exchange_rate("EUR", "USD")
print(f"1 EUR = {rate} USD")  # 1 EUR = 1.08 USD
```

### 📏 Units Converter
Conversor completo de unidades de medida com 8 categorias diferentes.
- 📏 **8 categorias**: Comprimento, Peso, Temperatura, Volume, Área, Velocidade, Energia, Potência
- 🔄 **60+ unidades**: Métricas, imperiais, brasileiras e especiais
- 🌡️ **Temperatura especial**: Celsius, Fahrenheit, Kelvin, Rankine
- 🎯 **Detecção automática**: Identifica categoria automaticamente
- 📊 **Formatação inteligente**: Notação científica para valores extremos

```python
from api.converter.units.units import convert_units

# Conversão de comprimento
result = convert_units(100, "cm", "m")
print(result['formatted_result'])  # "1 M (Metro)"

# Conversão de temperatura
result = convert_units(100, "c", "f")
print(result['formatted_result'])  # "212 F (Fahrenheit)"

# Conversão de peso
result = convert_units(1, "kg", "lb")
print(result['formatted_result'])  # "2.20462 LB (Libra)"
```

### 📝 Text Converter
Conversor e manipulador de texto com múltiplas funcionalidades.
- 🧹 **Limpeza avançada**: Remove acentos, caracteres especiais, espaços extras
- 🔤 **Formatação**: 8 formatos de capitalização (camelCase, snake_case, etc.)
- 🔍 **Extração de dados**: Emails, telefones, URLs, números automáticos
- 🎭 **Mascaramento**: Protege dados sensíveis
- 🔐 **Codificação**: Base64, URL, HTML encode/decode
- #️⃣ **Hash**: MD5, SHA1, SHA256, SHA512
- 📊 **Estatísticas**: Contagem de palavras, caracteres, linhas

```python
from api.converter.text.text import clean_text, change_case, extract_data

# Limpeza de texto
result = clean_text("  Olá, Mundo!  ", remove_accents=True)
print(result)  # "Ola, Mundo!"

# Mudança de formato
result = change_case("hello world", "camel_case")
print(result)  # "HelloWorld"

# Extração de dados
emails = extract_data("Contato: joao@email.com", "emails")
print(emails)  # ['joao@email.com']
```

### 🎨 Color Converter
Conversor robusto entre diferentes formatos de cores.
- 🌈 **Múltiplos formatos**: HEX, RGB, RGBA, HSL, HSLA, HSV, CMYK
- 🔍 **Detecção automática**: Identifica formato automaticamente
- 🎯 **Cores nomeadas**: Suporte a 140+ cores CSS
- 🔄 **Conversões precisas**: Algoritmos otimizados para cada formato
- 🎨 **Funções de conveniência**: Geração de paletas e harmonias

```python
from api.converter.color.color import convert_color, detect_color_format

# Conversão HEX para RGB
result = convert_color("#FF5733", "rgb")
print(result['converted_color'])  # rgb(255, 87, 51)

# Detecção automática
format_type = detect_color_format("hsl(15, 100%, 60%)")
print(format_type)  # hsl
```

### 🗺️ Coordinate Converter
Conversor de coordenadas geográficas com cálculos avançados.
- 📍 **Múltiplos formatos**: Decimal (DD), Graus-Minutos-Segundos (DMS), Graus-Minutos Decimais (DDM)
- 🧭 **Cálculos geográficos**: Distância (Haversine), direção e bearing
- 🔄 **Conversões precisas**: Validação e formatação automática
- 🌍 **Direções cardinais**: N, S, E, W com subdivisões

```python
from api.converter.coordinate.coordinate import convert_coordinate, calculate_distance

# Conversão DD para DMS
result = convert_coordinate("-23.5505, -46.6333", "dms")
print(result['converted_coordinate'])  # 23°33'1.8"S, 46°37'59.88"W

# Calcular distância
distance = calculate_distance((-23.5505, -46.6333), (-22.9068, -43.1729))
print(f"{distance:.2f} km")  # 357.04 km
```

### 🔢 Number Converter
Conversor entre diferentes bases numéricas.
- 🔢 **6 bases suportadas**: Binário, Octal, Decimal, Hexadecimal, Base32, Base64
- 🔍 **Detecção automática**: Identifica base por prefixos e padrões
- ✅ **Validação rigorosa**: Verificação de caracteres válidos para cada base
- 🏷️ **Prefixos inteligentes**: Reconhece 0b, 0o, 0x automaticamente

```python
from api.converter.number.number import convert_number, detect_number_base

# Conversão binário para decimal
result = convert_number("1010", "binary", "decimal")
print(result['converted_number'])  # 10

# Detecção automática
base = detect_number_base("0xFF")
print(base)  # hexadecimal
```

### 🖼️ Image Converter
Conversor robusto entre diferentes formatos de imagem.
- 🖼️ **8 formatos suportados**: JPEG, PNG, WebP, BMP, GIF, TIFF, ICO, PDF
- 🔧 **Otimização avançada**: Compressão e redimensionamento inteligente
- 📱 **Base64 support**: Conversão para/de data URLs
- ⚡ **Processamento em lote**: Múltiplas imagens simultaneamente
- 🎯 **Controle de qualidade**: Configurações precisas de compressão

```python
from api.converter.image.image import convert_image, optimize_image

# Conversão JPEG para PNG
result = convert_image("photo.jpg", "png")
print(f"Convertido: {len(result['converted_data'])} bytes")

# Otimização para web
optimized = optimize_image("large_photo.jpg", target_size_kb=500)
print(f"Redução: {optimized['size_info']['size_reduction_percent']}%")
```

## 📦 Instalação

```bash
# Clone o repositório
git clone https://github.com/vieira-brz/MundialConverter.git
cd MundialConverter

# Instale as dependências
pip install -r requirements.txt
```

## 🔧 Uso Rápido

```python
# Importar conversores
from api.converter.date.date import convert_date
from api.converter.currency.currency import convert_currency
from api.converter.units.units import convert_units
from api.converter.text.text import clean_text, remove_accents
from api.converter.color.color import convert_color
from api.converter.coordinate.coordinate import convert_coordinate
from api.converter.number.number import convert_number
from api.converter.image.image import convert_image

# Exemplo: Conversão de data
date_result = convert_date("2025-07-23", "BR")
print(f"Data BR: {date_result}")  # 23/07/2025

# Exemplo: Conversão de moeda
currency_result = convert_currency(100, "USD", "BRL")
print(f"Moeda: {currency_result['formatted_result']}")  # R$ 520,00

# Exemplo: Conversão de unidades
units_result = convert_units(100, "cm", "m")
print(f"Unidade: {units_result['formatted_result']}")  # 1 M (Metro)

# Exemplo: Limpeza de texto
text_result = clean_text("  Olá, Mundo!  ", remove_accents=True)
print(f"Texto: {text_result}")  # "Ola, Mundo!"

# Exemplo: Conversão de cor
color_result = convert_color("#FF5733", "rgb")
print(f"Cor: {color_result['converted_color']}")  # rgb(255, 87, 51)

# Exemplo: Conversão de coordenada
coord_result = convert_coordinate("-23.5505, -46.6333", "dms")
print(f"Coordenada: {coord_result['converted_coordinate']}")  # 23°33'1.8"S, 46°37'59.88"W

# Exemplo: Conversão de número
number_result = convert_number("1010", "binary", "decimal")
print(f"Número: {number_result['converted_number']}")  # 10

# Exemplo: Conversão de imagem
image_result = convert_image("photo.jpg", "png")
print(f"Imagem convertida: {len(image_result['converted_data'])} bytes")
```

## 📚 Documentação

### 📖 Guias Gerais
- 📖 [Getting Started](./docs/getting-started.md) - Guia de início rápido
- 🚀 [Deployment](./docs/deployment.md) - Como usar em produção

### 📋 Documentação dos Conversores
- 📅 [Date Converter](./api/converter/date/README.md) - Conversão de datas
- 💱 [Currency Converter](./api/converter/currency/README.md) - Conversão de moedas
- 📏 [Units Converter](./api/converter/units/README.md) - Conversão de unidades
- 📝 [Text Converter](./api/converter/text/README.md) - Manipulação de texto
- 🎨 [Color Converter](./api/converter/color/README.md) - Conversão de cores
- 🗺️ [Coordinate Converter](./api/converter/coordinate/README.md) - Conversão de coordenadas
- 🔢 [Number Converter](./api/converter/number/README.md) - Conversão de bases numéricas
- 🖼️ [Image Converter](./api/converter/image/README.md) - Conversão de formatos de imagem

## 🛠️ Estrutura do Projeto

```
MundialConverter/
├── README.md                    # Este arquivo
├── requirements.txt             # Dependências
├── docs/                        # Documentação geral
│   ├── getting-started.md
│   └── deployment.md
└── api/converter/               # Conversores
    ├── date/                    # ✅ Conversor de datas
    │   ├── date.py
    │   └── README.md
    ├── currency/                # ✅ Conversor de moedas
    │   ├── currency.py
    │   └── README.md
    ├── units/                   # ✅ Conversor de unidades
    │   ├── units.py
    │   └── README.md
    ├── text/                    # ✅ Conversor de texto
    │   ├── text.py
    │   └── README.md
    ├── color/                   # ✅ Conversor de cores
    │   ├── color.py
    │   └── README.md
    ├── coordinate/              # ✅ Conversor de coordenadas
    │   ├── coordinate.py
    │   └── README.md
    ├── number/                  # ✅ Conversor de números
    │   ├── number.py
    │   └── README.md
    └── image/                   # ✅ Conversor de imagens
        ├── image.py
        └── README.md
```

## 🎯 Casos de Uso

- 🏢 **Sistemas internacionais** que precisam de formatação local
- 📊 **ETL e processamento** de dados de diferentes fontes
- 🌐 **APIs** que recebem dados em formatos variados
- 📱 **Aplicações multi-idioma** e multi-região
- 🔄 **Migração de dados** entre sistemas

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📋 Roadmap

- [x] ✅ Date Converter - Conversão de datas
- [x] ✅ Currency Converter - Conversão de moedas
- [x] ✅ Units Converter - Conversão de unidades
- [x] ✅ Text Converter - Manipulação de texto
- [x] ✅ Color Converter - Conversão de cores (HEX, RGB, HSL, HSV, CMYK)
- [x] ✅ Coordinate Converter - Conversão de coordenadas geográficas
- [x] ✅ Number Converter - Conversão de bases numéricas
- [x] ✅ Image Converter - Conversão de formatos de imagem

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Vinícius Braz**
- GitHub: [@vieira-brz](https://github.com/vieira-brz)

---

⭐ **Se este projeto foi útil, deixe uma estrela!** ⭐