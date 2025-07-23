# Text Converter

Conversor e manipulador de texto com múltiplas funcionalidades para limpeza, formatação e extração de dados.

## Características

- 🧹 **Limpeza avançada**: Remove acentos, caracteres especiais, espaços extras
- 🔤 **Formatação**: 8 formatos de capitalização (camelCase, snake_case, etc.)
- 🔍 **Extração de dados**: Emails, telefones, URLs, números automáticos
- 🎭 **Mascaramento**: Protege dados sensíveis
- 🔐 **Codificação**: Base64, URL, HTML encode/decode
- #️⃣ **Hash**: MD5, SHA1, SHA256, SHA512
- 📊 **Estatísticas**: Contagem de palavras, caracteres, linhas

## Uso Rápido

```python
from api.converter.text.text import clean_text, remove_accents, change_case

# Limpeza básica
result = clean_text("  Olá, Mundo!  ", remove_accents=True)
print(result)  # "Ola, Mundo!"

# Remove acentos
result = remove_accents("São Paulo")
print(result)  # "Sao Paulo"

# Mudança de caso
result = change_case("hello world", "camel_case")
print(result)  # "HelloWorld"
```

## Funcionalidades Principais

### 🧹 Limpeza de Texto

```python
from api.converter.text.text import TextConverter

text = "  Olá, João! Email: joão@test.com (11) 99999-9999  "

# Opções de limpeza
options = {
    'remove_accents': True,      # Remove acentos
    'remove_special': False,     # Remove caracteres especiais
    'remove_extra_spaces': True, # Remove espaços extras
    'remove_numbers': False,     # Remove números
    'keep_only_alpha': False     # Mantém apenas letras
}

cleaned = TextConverter.clean_text(text, options)
print(cleaned)  # "Ola, Joao! Email: joao@test.com (11) 99999-9999"
```

### 🔤 Formatação de Caso

```python
text = "hello world python"

formats = {
    'lower': 'hello world python',
    'upper': 'HELLO WORLD PYTHON', 
    'title': 'Hello World Python',
    'capitalize': 'Hello world python',
    'snake_case': 'hello_world_python',
    'camel_case': 'HelloWorldPython',
    'kebab_case': 'hello-world-python',
    'pascal_case': 'HelloWorldPython'
}

for format_name, expected in formats.items():
    result = TextConverter.change_case(text, format_name)
    print(f"{format_name}: {result}")
```

### 🔍 Extração de Dados

```python
text = """
Contatos:
- João: joao@empresa.com, (11) 99999-9999
- Site: https://www.exemplo.com.br
- Valor: R$ 1.234,56
"""

# Extrai emails
emails = TextConverter.extract_emails(text)
print(emails)  # ['joao@empresa.com']

# Extrai telefones (Brasil)
phones = TextConverter.extract_phones(text, 'BR')
print(phones)  # ['(11) 99999-9999']

# Extrai URLs
urls = TextConverter.extract_urls(text)
print(urls)  # ['https://www.exemplo.com.br']

# Extrai números
numbers = TextConverter.extract_numbers(text)
print(numbers)  # ['11', '99999', '9999', '1.234', '56']
```

### 🎭 Mascaramento de Dados

```python
sensitive_text = "Email: joao.silva@empresa.com, Tel: (11) 99999-9999"

masked = TextConverter.mask_sensitive_data(sensitive_text)
print(masked)
# "Email: j*********a@empresa.com, Tel: (11) *****-9999"

# Caractere personalizado
masked_custom = TextConverter.mask_sensitive_data(sensitive_text, 'X')
print(masked_custom)
# "Email: jXXXXXXXXXa@empresa.com, Tel: (11) XXXXX-9999"
```

### 🔐 Codificação e Decodificação

```python
text = "Texto secreto"

# Base64
encoded = TextConverter.encode_decode(text, 'encode', 'base64')
print(encoded)  # "VGV4dG8gc2VjcmV0bw=="

decoded = TextConverter.encode_decode(encoded, 'decode', 'base64')
print(decoded)  # "Texto secreto"

# URL encoding
url_encoded = TextConverter.encode_decode("hello world", 'encode', 'url')
print(url_encoded)  # "hello%20world"

# HTML encoding
html_encoded = TextConverter.encode_decode("<script>", 'encode', 'html')
print(html_encoded)  # "&lt;script&gt;"
```

### #️⃣ Geração de Hash

```python
text = "Senha123"

# Diferentes algoritmos
md5_hash = TextConverter.generate_hash(text, 'md5')
sha256_hash = TextConverter.generate_hash(text, 'sha256')

print(f"MD5: {md5_hash}")
print(f"SHA256: {sha256_hash}")
```

### 📊 Estatísticas de Texto

```python
text = """
Este é um texto de exemplo.
Tem múltiplas linhas.

E também parágrafos.
"""

stats = TextConverter.word_count(text)
print(stats)
# {
#     'words': 10,
#     'characters': 65,
#     'characters_no_spaces': 52,
#     'lines': 5,
#     'paragraphs': 2
# }
```

## Funções de Conveniência

```python
from api.converter.text.text import (
    clean_text, remove_accents, change_case, extract_data
)

# Limpeza rápida
clean = clean_text("  Texto  ", remove_accents=True, remove_extra_spaces=True)

# Remove acentos
no_accents = remove_accents("Acentuação")

# Mudança de caso
camel = change_case("hello world", "camel_case")

# Extração de dados
emails = extract_data("Email: test@example.com", "emails")
phones = extract_data("Tel: (11) 99999-9999", "phones")
numbers = extract_data("Preço: R$ 123,45", "numbers")
urls = extract_data("Site: https://example.com", "urls")
```

## Exemplos Avançados

### Processador de Dados Pessoais (LGPD)

```python
def anonymize_personal_data(text):
    """Anonimiza dados pessoais para conformidade LGPD"""
    
    # Remove acentos para padronização
    text = TextConverter.remove_accents(text)
    
    # Mascara dados sensíveis
    text = TextConverter.mask_sensitive_data(text)
    
    # Limpa caracteres especiais
    text = TextConverter.clean_text(text, {
        'remove_extra_spaces': True
    })
    
    return text

# Exemplo
personal_data = "Nome: João da Silva, Email: joao@email.com, CPF: 123.456.789-00"
anonymized = anonymize_personal_data(personal_data)
print(anonymized)
```

### Normalizador de Dados

```python
def normalize_database_field(text, field_type='name'):
    """Normaliza campos para banco de dados"""
    
    if field_type == 'name':
        # Nomes: remove acentos, title case, limpa
        text = TextConverter.remove_accents(text)
        text = TextConverter.change_case(text, 'title')
        text = TextConverter.clean_text(text, {
            'remove_special': True,
            'remove_extra_spaces': True,
            'keep_only_alpha': True
        })
    
    elif field_type == 'email':
        # Emails: lowercase, limpa
        text = TextConverter.change_case(text, 'lower')
        text = TextConverter.clean_text(text, {
            'remove_extra_spaces': True
        })
    
    elif field_type == 'slug':
        # Slugs: kebab-case, sem acentos
        text = TextConverter.remove_accents(text)
        text = TextConverter.change_case(text, 'kebab_case')
    
    return text

# Exemplos
name = normalize_database_field("  joão da SILVA  ", 'name')
email = normalize_database_field("  JOAO@EMAIL.COM  ", 'email')
slug = normalize_database_field("Artigo Sobre Python", 'slug')

print(f"Nome: {name}")    # "Joao Da Silva"
print(f"Email: {email}")  # "joao@email.com"
print(f"Slug: {slug}")    # "artigo-sobre-python"
```

### Extrator de Contatos

```python
def extract_contact_info(text):
    """Extrai informações de contato de um texto"""
    
    contacts = {
        'emails': TextConverter.extract_emails(text),
        'phones_br': TextConverter.extract_phones(text, 'BR'),
        'phones_us': TextConverter.extract_phones(text, 'US'),
        'urls': TextConverter.extract_urls(text)
    }
    
    # Remove duplicatas
    for key in contacts:
        contacts[key] = list(set(contacts[key]))
    
    return contacts

# Exemplo
contact_text = """
Empresa XYZ
Email: contato@empresa.com.br
Telefone: (11) 99999-9999
Site: https://www.empresa.com.br
Suporte: suporte@empresa.com.br
"""

contacts = extract_contact_info(contact_text)
print(contacts)
```

### Gerador de Senhas Hash

```python
def generate_secure_hash(password, salt=""):
    """Gera hash seguro para senhas"""
    
    # Combina senha com salt
    combined = password + salt
    
    # Gera múltiplos hashes
    hashes = {}
    algorithms = ['md5', 'sha1', 'sha256', 'sha512']
    
    for algo in algorithms:
        hashes[algo] = TextConverter.generate_hash(combined, algo)
    
    return hashes

# Exemplo
password_hashes = generate_secure_hash("MinhaSenh@123", "salt_secreto")
for algo, hash_value in password_hashes.items():
    print(f"{algo.upper()}: {hash_value}")
```

## Tratamento de Erros

```python
try:
    # Formato de caso inválido
    result = TextConverter.change_case("text", "invalid_case")
except ValueError as e:
    print(f"Erro: {e}")

try:
    # Algoritmo de hash inválido
    hash_result = TextConverter.generate_hash("text", "invalid_algo")
except ValueError as e:
    print(f"Erro: {e}")

try:
    # Codificação inválida
    encoded = TextConverter.encode_decode("text", "encode", "invalid_encoding")
except ValueError as e:
    print(f"Erro: {e}")
```

## Testes

Execute o arquivo diretamente para ver exemplos:

```bash
python api/converter/text/text.py
```

## Dependências

Bibliotecas built-in do Python:
- `re` (expressões regulares)
- `unicodedata` (normalização Unicode)
- `html` (escape/unescape HTML)
- `base64` (codificação Base64)
- `hashlib` (algoritmos de hash)
- `urllib.parse` (codificação URL)

Não requer instalação de pacotes externos!
