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
    └── text/                    # ✅ Conversor de texto
        ├── text.py
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
- [ ] 🔄 Color Converter - Conversão de cores (HEX, RGB, HSL)
- [ ] 🔄 Coordinate Converter - Conversão de coordenadas
- [ ] 🔄 Number Converter - Conversão de bases numéricas
- [ ] 🔄 Image Converter - Conversão de formatos de imagem

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Vinícius Braz**
- GitHub: [@vieira-brz](https://github.com/vieira-brz)

---

⭐ **Se este projeto foi útil, deixe uma estrela!** ⭐