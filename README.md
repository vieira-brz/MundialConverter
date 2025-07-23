# 📅 Date Converter API

Uma API robusta para conversão de datas entre diferentes formatos e países, otimizada para deploy no Vercel.

## 🚀 Funcionalidades

- **Detecção automática** de formatos de data
- **Suporte a múltiplos países** (BR, EUA, UK, DE, FR, ISO)
- **Conversão com ou sem horário**
- **Tratamento de timezone**
- **Formatos flexíveis** de entrada

## 📋 Formatos Suportados

### Entrada (Auto-detectados)
- `dd/mm/yyyy` - 23/07/2025
- `dd-mm-yyyy` - 23-07-2025
- `yyyy-mm-dd` - 2025-07-23
- `mm/dd/yyyy` - 07/23/2025 (americano)
- `dd.mm.yyyy` - 23.07.2025
- `yyyy-mm-ddThh:mm:ss` - ISO format
- `dd/mm/yyyy hh:mm:ss` - Com horário
- `yyyymmdd` - Timestamp
- E muitos outros...

### Saída por País
- **BR**: `dd/mm/yyyy` (timezone: America/Sao_Paulo)
- **EUA/USA**: `mm/dd/yyyy` (timezone: America/New_York)
- **UK**: `dd/mm/yyyy` (timezone: Europe/London)
- **DE**: `dd.mm.yyyy` (timezone: Europe/Berlin)
- **FR**: `dd/mm/yyyy` (timezone: Europe/Paris)
- **ISO**: `yyyy-mm-dd` (timezone: UTC)

## 🔗 Endpoints

### `POST /api/converter/date`
Converte uma data para o formato especificado.

**Parâmetros:**
```json
{
  "date": "2025-07-23 15:30:45",    // string (obrigatório)
  "to_type": "BR",                  // string (padrão: "BR")
  "return_hour": true               // boolean (padrão: false)
}
```

**Resposta de sucesso:**
```json
{
  "success": true,
  "input": {
    "original": "2025-07-23 15:30:45",
    "parsed": "2025-07-23T15:30:45",
    "detected_format": "auto-detected"
  },
  "output": {
    "converted": "23/07/2025 15:30:45",
    "format": "BR",
    "with_hour": true,
    "timezone": "America/Sao_Paulo"
  },
  "metadata": {
    "conversion_time": "2025-07-23T18:30:45",
    "api_version": "1.0"
  }
}
```

### `GET /api/converter/date/formats`
Lista todos os formatos e países suportados.

### `GET /api/converter/date/test`
Executa testes com exemplos de conversões.

## 💡 Exemplos de Uso

### Conversão Básica
```bash
curl -X POST https://your-vercel-app.vercel.app/api/converter/date \
  -H "Content-Type: application/json" \
  -d '{
    "date": "23/07/2025",
    "to_type": "EUA"
  }'
```

### Com Horário
```bash
curl -X POST https://your-vercel-app.vercel.app/api/converter/date \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-07-23 15:30:45",
    "to_type": "BR",
    "return_hour": true
  }'
```

### Via GET (query params)
```bash
curl "https://your-vercel-app.vercel.app/api/converter/date?date=23/07/2025&to_type=ISO"
```

## 🛠️ Deploy no Vercel

1. **Clone o repositório**
2. **Instale o Vercel CLI**: `npm i -g vercel`
3. **Deploy**: `vercel --prod`

### Arquivos de Configuração

- `vercel.json` - Configuração do Vercel
- `requirements.txt` - Dependências Python
- `api/converter/date.py` - Código principal da API

## 🧪 Testando Localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar servidor local
python api/converter/date.py

# Testar endpoint
curl -X POST http://localhost:5000/api/converter/date \
  -H "Content-Type: application/json" \
  -d '{"date": "23/07/2025", "to_type": "BR"}'
```

## 🔧 Casos de Uso

- **Sistemas internacionais** que precisam exibir datas no formato local
- **APIs que recebem datas** em formatos variados
- **Conversão de logs** e timestamps
- **Normalização de dados** de diferentes fontes
- **Aplicações multi-idioma**

## ⚠️ Tratamento de Erros

A API retorna erros detalhados:

```json
{
  "error": "Não foi possível interpretar a data: \"invalid-date\"",
  "supported_formats": [
    "dd/mm/yyyy", "dd-mm-yyyy", "yyyy-mm-dd",
    "dd/mm/yyyy hh:mm:ss", "etc."
  ]
}
```

## 🌟 Características Técnicas

- **Detecção automática** de formatos usando regex e parsing
- **Suporte a timezone** com pytz
- **Validação robusta** de entrada
- **Resposta estruturada** com metadados
- **Compatível com Vercel** serverless functions
- **Suporte a GET e POST**
