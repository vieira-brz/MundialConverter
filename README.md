# 🌍 MundialConverter

Uma biblioteca Python completa de utilitários de conversão para desenvolvedores. Converta datas, moedas, unidades, texto e muito mais com facilidade e precisão.

## 🚀 Conversores Disponíveis

### 📅 [Date Converter](./api/converter/date/)
Conversão robusta de datas entre diferentes formatos e países.
- ✅ **30+ formatos** de entrada suportados
- ✅ **6 países/padrões**: BR, EUA, UK, DE, FR, ISO
- ✅ **Detecção automática** de formato
- ✅ **Suporte a timezone** e horários

```python
from api.converter.date.date import DateConverter

# Conversão simples
result = DateConverter.detect_and_parse("23/07/2025")
converted = DateConverter.convert_to_format(result, "EUA")
print(converted)  # 07/23/2025
```

### 💰 [Currency Converter](./api/converter/currency/) *(Em desenvolvimento)*
Conversão de moedas com taxas atualizadas.
- 🔄 Taxas de câmbio em tempo real
- 🌎 150+ moedas suportadas
- 📊 Histórico de cotações

### 📏 [Units Converter](./api/converter/units/) *(Em desenvolvimento)*
Conversão entre diferentes unidades de medida.
- ⚖️ Peso: kg, lb, oz, g
- 📐 Distância: m, ft, in, km, mi
- 🌡️ Temperatura: °C, °F, K
- 📦 Volume: L, gal, ml, fl oz

### 🔤 [Text Converter](./api/converter/text/) *(Em desenvolvimento)*
Conversão e manipulação de texto.
- 🔄 Encoding: UTF-8, ASCII, Latin-1
- 📝 Case: UPPER, lower, Title, camelCase
- 🌐 Transliteração e normalização

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
from api.converter.date.date import DateConverter
# from api.converter.currency.currency import CurrencyConverter  # Em breve
# from api.converter.units.units import UnitsConverter            # Em breve

# Exemplo: Conversão de data
date_input = "2025-07-23 15:30"
parsed_date = DateConverter.detect_and_parse(date_input)
br_format = DateConverter.convert_to_format(parsed_date, "BR", True)
print(f"Formato BR: {br_format}")  # 23/07/2025 15:30:00
```

## 📚 Documentação

- 📖 [Getting Started](./docs/getting-started.md) - Guia de início rápido
- 🚀 [Deployment](./docs/deployment.md) - Como usar em produção
- 📅 [Date Converter](./api/converter/date/README.md) - Documentação completa

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
    ├── currency/                # 🔄 Em desenvolvimento
    ├── units/                   # 🔄 Em desenvolvimento
    └── text/                    # 🔄 Em desenvolvimento
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
- [ ] 🔄 Currency Converter - Conversão de moedas
- [ ] 🔄 Units Converter - Conversão de unidades
- [ ] 🔄 Text Converter - Manipulação de texto
- [ ] 🔄 Color Converter - Conversão de cores (HEX, RGB, HSL)
- [ ] 🔄 Coordinate Converter - Conversão de coordenadas

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Vinícius Braz**
- GitHub: [@vieira-brz](https://github.com/vieira-brz)
- LinkedIn: [Vinícius Braz](https://linkedin.com/in/vinicius-braz)

---

⭐ **Se este projeto foi útil, deixe uma estrela!** ⭐