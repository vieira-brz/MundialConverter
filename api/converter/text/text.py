import re
import unicodedata
from typing import Union, Optional, Dict, Any, List
import html
import base64
import hashlib

class TextConverter:
    """Classe para conversão e manipulação de texto"""
    
    # Mapeamentos de caracteres especiais
    ACCENT_MAP = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a', 'ä': 'a', 'å': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'õ': 'o', 'ô': 'o', 'ö': 'o', 'ø': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c', 'ñ': 'n',
        'Á': 'A', 'À': 'A', 'Ã': 'A', 'Â': 'A', 'Ä': 'A', 'Å': 'A',
        'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
        'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I',
        'Ó': 'O', 'Ò': 'O', 'Õ': 'O', 'Ô': 'O', 'Ö': 'O', 'Ø': 'O',
        'Ú': 'U', 'Ù': 'U', 'Û': 'U', 'Ü': 'U',
        'Ç': 'C', 'Ñ': 'N'
    }
    
    # Padrões de formatação
    CASE_FORMATS = {
        'lower': str.lower,
        'upper': str.upper,
        'title': str.title,
        'capitalize': str.capitalize,
        'snake_case': lambda x: re.sub(r'[^a-zA-Z0-9]', '_', x).lower(),
        'camel_case': lambda x: ''.join(word.capitalize() for word in re.split(r'[^a-zA-Z0-9]', x) if word),
        'kebab_case': lambda x: re.sub(r'[^a-zA-Z0-9]', '-', x).lower(),
        'pascal_case': lambda x: ''.join(word.capitalize() for word in re.split(r'[^a-zA-Z0-9]', x) if word)
    }
    
    @classmethod
    def remove_accents(cls, text: str) -> str:
        """
        Remove acentos de um texto
        
        Args:
            text: Texto com acentos
            
        Returns:
            Texto sem acentos
        """
        if not isinstance(text, str):
            return str(text)
        
        # Método 1: Mapeamento manual (mais controle)
        result = text
        for accented, plain in cls.ACCENT_MAP.items():
            result = result.replace(accented, plain)
        
        # Método 2: Unicode normalization (backup)
        result = unicodedata.normalize('NFD', result)
        result = ''.join(c for c in result if unicodedata.category(c) != 'Mn')
        
        return result
    
    @classmethod
    def clean_text(cls, text: str, options: Optional[Dict] = None) -> str:
        """
        Limpa e normaliza texto
        
        Args:
            text: Texto a ser limpo
            options: Opções de limpeza
                - remove_accents: Remove acentos (default: False)
                - remove_special: Remove caracteres especiais (default: False)
                - remove_extra_spaces: Remove espaços extras (default: True)
                - remove_numbers: Remove números (default: False)
                - keep_only_alpha: Mantém apenas letras (default: False)
        
        Returns:
            Texto limpo
        """
        if not isinstance(text, str):
            text = str(text)
        
        if not options:
            options = {}
        
        result = text
        
        # Remove acentos
        if options.get('remove_accents', False):
            result = cls.remove_accents(result)
        
        # Remove números
        if options.get('remove_numbers', False):
            result = re.sub(r'\d+', '', result)
        
        # Remove caracteres especiais
        if options.get('remove_special', False):
            result = re.sub(r'[^\w\s]', '', result)
        
        # Mantém apenas letras
        if options.get('keep_only_alpha', False):
            result = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', result)
        
        # Remove espaços extras
        if options.get('remove_extra_spaces', True):
            result = re.sub(r'\s+', ' ', result).strip()
        
        return result
    
    @classmethod
    def change_case(cls, text: str, case_format: str) -> str:
        """
        Altera formato de capitalização do texto
        
        Args:
            text: Texto a ser formatado
            case_format: Formato desejado
                - lower, upper, title, capitalize
                - snake_case, camel_case, kebab_case, pascal_case
        
        Returns:
            Texto formatado
        """
        if not isinstance(text, str):
            text = str(text)
        
        case_format = case_format.lower()
        if case_format not in cls.CASE_FORMATS:
            raise ValueError(f"Formato '{case_format}' não suportado. Disponíveis: {list(cls.CASE_FORMATS.keys())}")
        
        return cls.CASE_FORMATS[case_format](text)
    
    @classmethod
    def extract_numbers(cls, text: str) -> List[str]:
        """
        Extrai números de um texto
        
        Args:
            text: Texto para extrair números
            
        Returns:
            Lista de números encontrados
        """
        if not isinstance(text, str):
            text = str(text)
        
        # Padrão para números (inteiros e decimais)
        pattern = r'-?\d+(?:\.\d+)?'
        return re.findall(pattern, text)
    
    @classmethod
    def extract_emails(cls, text: str) -> List[str]:
        """
        Extrai emails de um texto
        
        Args:
            text: Texto para extrair emails
            
        Returns:
            Lista de emails encontrados
        """
        if not isinstance(text, str):
            text = str(text)
        
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(pattern, text)
    
    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        """
        Extrai URLs de um texto
        
        Args:
            text: Texto para extrair URLs
            
        Returns:
            Lista de URLs encontradas
        """
        if not isinstance(text, str):
            text = str(text)
        
        pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(pattern, text)
    
    @classmethod
    def extract_phones(cls, text: str, country: str = 'BR') -> List[str]:
        """
        Extrai telefones de um texto
        
        Args:
            text: Texto para extrair telefones
            country: País para formato (BR, US, etc.)
            
        Returns:
            Lista de telefones encontrados
        """
        if not isinstance(text, str):
            text = str(text)
        
        patterns = {
            'BR': [
                r'\(\d{2}\)\s*\d{4,5}-?\d{4}',  # (11) 99999-9999
                r'\d{2}\s*\d{4,5}-?\d{4}',      # 11 99999-9999
                r'\+55\s*\d{2}\s*\d{4,5}-?\d{4}' # +55 11 99999-9999
            ],
            'US': [
                r'\(\d{3}\)\s*\d{3}-?\d{4}',    # (555) 123-4567
                r'\d{3}-?\d{3}-?\d{4}',         # 555-123-4567
                r'\+1\s*\d{3}\s*\d{3}\s*\d{4}' # +1 555 123 4567
            ]
        }
        
        phones = []
        for pattern in patterns.get(country, patterns['BR']):
            phones.extend(re.findall(pattern, text))
        
        return phones
    
    @classmethod
    def mask_sensitive_data(cls, text: str, mask_char: str = '*') -> str:
        """
        Mascara dados sensíveis em um texto
        
        Args:
            text: Texto com dados sensíveis
            mask_char: Caractere para mascarar
            
        Returns:
            Texto com dados mascarados
        """
        if not isinstance(text, str):
            text = str(text)
        
        result = text
        
        # Mascara emails (mantém primeiro e último caractere + domínio)
        def mask_email(match):
            email = match.group(0)
            if '@' in email:
                local, domain = email.split('@', 1)
                if len(local) > 2:
                    masked_local = local[0] + mask_char * (len(local) - 2) + local[-1]
                else:
                    masked_local = mask_char * len(local)
                return f"{masked_local}@{domain}"
            return email
        
        result = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', mask_email, result)
        
        # Mascara telefones (mantém apenas últimos 4 dígitos)
        def mask_phone(match):
            phone = match.group(0)
            digits = re.findall(r'\d', phone)
            if len(digits) >= 4:
                masked_digits = [mask_char] * (len(digits) - 4) + digits[-4:]
                masked_phone = phone
                digit_index = 0
                for i, char in enumerate(phone):
                    if char.isdigit():
                        masked_phone = masked_phone[:i] + masked_digits[digit_index] + masked_phone[i+1:]
                        digit_index += 1
                return masked_phone
            return phone
        
        # Padrões de telefone brasileiro
        result = re.sub(r'\(\d{2}\)\s*\d{4,5}-?\d{4}', mask_phone, result)
        result = re.sub(r'\d{2}\s*\d{4,5}-?\d{4}', mask_phone, result)
        
        return result
    
    @classmethod
    def encode_decode(cls, text: str, operation: str, encoding: str = 'utf-8') -> str:
        """
        Codifica/decodifica texto
        
        Args:
            text: Texto a ser processado
            operation: 'encode' ou 'decode'
            encoding: Tipo de codificação (base64, url, html, etc.)
            
        Returns:
            Texto processado
        """
        if not isinstance(text, str):
            text = str(text)
        
        if operation == 'encode':
            if encoding == 'base64':
                return base64.b64encode(text.encode('utf-8')).decode('utf-8')
            elif encoding == 'url':
                import urllib.parse
                return urllib.parse.quote(text)
            elif encoding == 'html':
                return html.escape(text)
            else:
                raise ValueError(f"Codificação '{encoding}' não suportada")
        
        elif operation == 'decode':
            if encoding == 'base64':
                return base64.b64decode(text.encode('utf-8')).decode('utf-8')
            elif encoding == 'url':
                import urllib.parse
                return urllib.parse.unquote(text)
            elif encoding == 'html':
                return html.unescape(text)
            else:
                raise ValueError(f"Decodificação '{encoding}' não suportada")
        
        else:
            raise ValueError("Operação deve ser 'encode' ou 'decode'")
    
    @classmethod
    def generate_hash(cls, text: str, algorithm: str = 'md5') -> str:
        """
        Gera hash de um texto
        
        Args:
            text: Texto para gerar hash
            algorithm: Algoritmo (md5, sha1, sha256, sha512)
            
        Returns:
            Hash do texto
        """
        if not isinstance(text, str):
            text = str(text)
        
        algorithms = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256,
            'sha512': hashlib.sha512
        }
        
        if algorithm not in algorithms:
            raise ValueError(f"Algoritmo '{algorithm}' não suportado. Disponíveis: {list(algorithms.keys())}")
        
        hash_obj = algorithms[algorithm]()
        hash_obj.update(text.encode('utf-8'))
        return hash_obj.hexdigest()
    
    @classmethod
    def word_count(cls, text: str) -> Dict[str, int]:
        """
        Conta palavras, caracteres e linhas
        
        Args:
            text: Texto para contar
            
        Returns:
            Dict com estatísticas
        """
        if not isinstance(text, str):
            text = str(text)
        
        words = len(text.split())
        chars = len(text)
        chars_no_spaces = len(text.replace(' ', ''))
        lines = len(text.split('\n'))
        paragraphs = len([p for p in text.split('\n\n') if p.strip()])
        
        return {
            'words': words,
            'characters': chars,
            'characters_no_spaces': chars_no_spaces,
            'lines': lines,
            'paragraphs': paragraphs
        }

# Funções de conveniência
def clean_text(text: str, **options) -> str:
    """
    Função de conveniência para limpeza de texto
    
    Example:
        >>> clean_text("  Olá, Mundo!  ", remove_accents=True, remove_special=True)
        'Ola Mundo'
    """
    return TextConverter.clean_text(text, options)

def remove_accents(text: str) -> str:
    """
    Remove acentos de um texto
    
    Example:
        >>> remove_accents("São Paulo")
        'Sao Paulo'
    """
    return TextConverter.remove_accents(text)

def change_case(text: str, case_format: str) -> str:
    """
    Altera formato de capitalização
    
    Example:
        >>> change_case("hello world", "camel_case")
        'HelloWorld'
    """
    return TextConverter.change_case(text, case_format)

def extract_data(text: str, data_type: str) -> List[str]:
    """
    Extrai dados específicos de um texto
    
    Args:
        text: Texto para extrair dados
        data_type: Tipo de dado (numbers, emails, urls, phones)
    
    Example:
        >>> extract_data("Contato: joao@email.com ou (11) 99999-9999", "emails")
        ['joao@email.com']
    """
    if data_type == 'numbers':
        return TextConverter.extract_numbers(text)
    elif data_type == 'emails':
        return TextConverter.extract_emails(text)
    elif data_type == 'urls':
        return TextConverter.extract_urls(text)
    elif data_type == 'phones':
        return TextConverter.extract_phones(text)
    else:
        raise ValueError(f"Tipo '{data_type}' não suportado")

# Exemplo de uso
if __name__ == "__main__":
    print("📝 Testando TextConverter...")
    print("=" * 50)
    
    # Texto de exemplo
    sample_text = """
    Olá! Meu nome é João da Silva.
    Email: joao.silva@empresa.com.br
    Telefone: (11) 99999-9999
    Website: https://www.exemplo.com.br
    Valor: R$ 1.234,56
    """
    
    print(f"📄 Texto original:\n{sample_text}")
    
    # Limpeza de texto
    print("\n🧹 Limpeza de texto:")
    cleaned = TextConverter.clean_text(sample_text, {
        'remove_accents': True,
        'remove_extra_spaces': True
    })
    print(f"Limpo: {cleaned[:100]}...")
    
    # Mudança de caso
    print("\n🔤 Mudança de caso:")
    cases = ['lower', 'upper', 'title', 'snake_case', 'camel_case']
    test_phrase = "Olá Mundo Python"
    for case in cases:
        result = TextConverter.change_case(test_phrase, case)
        print(f"{case}: {result}")
    
    # Extração de dados
    print("\n🔍 Extração de dados:")
    emails = TextConverter.extract_emails(sample_text)
    phones = TextConverter.extract_phones(sample_text)
    numbers = TextConverter.extract_numbers(sample_text)
    urls = TextConverter.extract_urls(sample_text)
    
    print(f"Emails: {emails}")
    print(f"Telefones: {phones}")
    print(f"Números: {numbers}")
    print(f"URLs: {urls}")
    
    # Mascaramento
    print("\n🎭 Mascaramento:")
    masked = TextConverter.mask_sensitive_data(sample_text)
    print(f"Mascarado:\n{masked}")
    
    # Estatísticas
    print("\n📊 Estatísticas:")
    stats = TextConverter.word_count(sample_text)
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Codificação
    print("\n🔐 Codificação:")
    text_to_encode = "Texto secreto"
    encoded = TextConverter.encode_decode(text_to_encode, 'encode', 'base64')
    decoded = TextConverter.encode_decode(encoded, 'decode', 'base64')
    print(f"Original: {text_to_encode}")
    print(f"Base64: {encoded}")
    print(f"Decodificado: {decoded}")
    
    # Hash
    print("\n#️⃣ Hash:")
    hash_md5 = TextConverter.generate_hash("Texto para hash", 'md5')
    hash_sha256 = TextConverter.generate_hash("Texto para hash", 'sha256')
    print(f"MD5: {hash_md5}")
    print(f"SHA256: {hash_sha256}")
    
    print("\n✅ Testes concluídos!")
