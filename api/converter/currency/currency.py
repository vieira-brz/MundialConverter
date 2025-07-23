import requests
from typing import Union, Optional, Dict, Any
from datetime import datetime, timedelta
import json
import os

class CurrencyConverter:
    """Classe para conversão de moedas com taxas atualizadas"""
    
    # Moedas suportadas
    SUPPORTED_CURRENCIES = {
        'USD': {'name': 'US Dollar', 'symbol': '$'},
        'EUR': {'name': 'Euro', 'symbol': '€'},
        'BRL': {'name': 'Brazilian Real', 'symbol': 'R$'},
        'GBP': {'name': 'British Pound', 'symbol': '£'},
        'JPY': {'name': 'Japanese Yen', 'symbol': '¥'},
        'CAD': {'name': 'Canadian Dollar', 'symbol': 'C$'},
        'AUD': {'name': 'Australian Dollar', 'symbol': 'A$'},
        'CHF': {'name': 'Swiss Franc', 'symbol': 'CHF'},
        'CNY': {'name': 'Chinese Yuan', 'symbol': '¥'},
        'INR': {'name': 'Indian Rupee', 'symbol': '₹'},
        'KRW': {'name': 'South Korean Won', 'symbol': '₩'},
        'MXN': {'name': 'Mexican Peso', 'symbol': '$'},
        'ARS': {'name': 'Argentine Peso', 'symbol': '$'},
        'CLP': {'name': 'Chilean Peso', 'symbol': '$'},
        'COP': {'name': 'Colombian Peso', 'symbol': '$'},
        'PEN': {'name': 'Peruvian Sol', 'symbol': 'S/'},
        'UYU': {'name': 'Uruguayan Peso', 'symbol': '$U'},
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa o conversor de moedas
        
        Args:
            api_key: Chave da API (opcional, usa API gratuita se não fornecida)
        """
        self.api_key = api_key
        self.base_url = "https://api.exchangerate-api.com/v4/latest/"
        self.backup_url = "https://api.fixer.io/latest"
        self.cache = {}
        self.cache_duration = timedelta(hours=1)  # Cache por 1 hora
    
    def _get_exchange_rates(self, base_currency: str = 'USD') -> Optional[Dict]:
        """
        Obtém taxas de câmbio da API
        """
        # Verifica cache
        cache_key = f"{base_currency}_{datetime.now().strftime('%Y%m%d%H')}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            # Tenta API principal
            response = requests.get(f"{self.base_url}{base_currency}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.cache[cache_key] = data
                return data
        except Exception as e:
            print(f"Erro na API principal: {e}")
        
        # Fallback para taxas fixas (última atualização conhecida)
        return self._get_fallback_rates(base_currency)
    
    def _get_fallback_rates(self, base_currency: str = 'USD') -> Dict:
        """
        Taxas de câmbio de fallback (atualizadas periodicamente)
        """
        # Taxas aproximadas baseadas em USD (atualizar periodicamente)
        fallback_rates = {
            'USD': {
                'rates': {
                    'EUR': 0.85,
                    'BRL': 5.20,
                    'GBP': 0.73,
                    'JPY': 110.0,
                    'CAD': 1.25,
                    'AUD': 1.35,
                    'CHF': 0.92,
                    'CNY': 6.45,
                    'INR': 74.5,
                    'KRW': 1180.0,
                    'MXN': 20.0,
                    'ARS': 98.0,
                    'CLP': 800.0,
                    'COP': 3800.0,
                    'PEN': 3.6,
                    'UYU': 44.0,
                    'USD': 1.0
                },
                'base': 'USD',
                'date': datetime.now().strftime('%Y-%m-%d')
            }
        }
        
        if base_currency in fallback_rates:
            return fallback_rates[base_currency]
        
        # Se não for USD, calcula baseado em USD
        usd_rates = fallback_rates['USD']['rates']
        if base_currency in usd_rates:
            base_rate = usd_rates[base_currency]
            converted_rates = {}
            for currency, rate in usd_rates.items():
                converted_rates[currency] = rate / base_rate
            
            return {
                'rates': converted_rates,
                'base': base_currency,
                'date': datetime.now().strftime('%Y-%m-%d')
            }
        
        return fallback_rates['USD']
    
    def convert(self, amount: Union[int, float], from_currency: str, to_currency: str) -> Optional[Dict[str, Any]]:
        """
        Converte valor entre moedas
        
        Args:
            amount: Valor a ser convertido
            from_currency: Moeda de origem (ex: 'USD')
            to_currency: Moeda de destino (ex: 'BRL')
        
        Returns:
            Dict com resultado da conversão
        """
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        # Validação
        if from_currency not in self.SUPPORTED_CURRENCIES:
            raise ValueError(f"Moeda '{from_currency}' não suportada")
        if to_currency not in self.SUPPORTED_CURRENCIES:
            raise ValueError(f"Moeda '{to_currency}' não suportada")
        
        if amount <= 0:
            raise ValueError("Valor deve ser maior que zero")
        
        # Se for a mesma moeda
        if from_currency == to_currency:
            return {
                'original_amount': amount,
                'converted_amount': amount,
                'from_currency': from_currency,
                'to_currency': to_currency,
                'exchange_rate': 1.0,
                'formatted_result': self._format_currency(amount, to_currency),
                'timestamp': datetime.now().isoformat()
            }
        
        # Obtém taxas de câmbio
        rates_data = self._get_exchange_rates(from_currency)
        if not rates_data or 'rates' not in rates_data:
            raise Exception("Não foi possível obter taxas de câmbio")
        
        rates = rates_data['rates']
        if to_currency not in rates:
            raise ValueError(f"Taxa para '{to_currency}' não encontrada")
        
        # Calcula conversão
        exchange_rate = rates[to_currency]
        converted_amount = amount * exchange_rate
        
        return {
            'original_amount': amount,
            'converted_amount': round(converted_amount, 2),
            'from_currency': from_currency,
            'to_currency': to_currency,
            'exchange_rate': exchange_rate,
            'formatted_original': self._format_currency(amount, from_currency),
            'formatted_result': self._format_currency(converted_amount, to_currency),
            'timestamp': datetime.now().isoformat(),
            'source': rates_data.get('date', 'fallback')
        }
    
    def _format_currency(self, amount: float, currency: str) -> str:
        """
        Formata valor com símbolo da moeda
        """
        if currency not in self.SUPPORTED_CURRENCIES:
            return f"{amount:.2f} {currency}"
        
        symbol = self.SUPPORTED_CURRENCIES[currency]['symbol']
        
        # Formatação específica por moeda
        if currency in ['JPY', 'KRW']:  # Moedas sem decimais
            return f"{symbol} {amount:,.0f}"
        elif currency == 'BRL':
            return f"{symbol} {amount:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        else:
            return f"{symbol} {amount:,.2f}"
    
    def get_supported_currencies(self) -> Dict[str, Dict[str, str]]:
        """
        Retorna lista de moedas suportadas
        """
        return self.SUPPORTED_CURRENCIES
    
    def get_current_rates(self, base_currency: str = 'USD') -> Optional[Dict]:
        """
        Obtém todas as taxas atuais para uma moeda base
        """
        return self._get_exchange_rates(base_currency)

# Funções de conveniência
def convert_currency(amount: Union[int, float], from_currency: str, to_currency: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Função de conveniência para conversão rápida
    
    Args:
        amount: Valor a converter
        from_currency: Moeda de origem
        to_currency: Moeda de destino
        api_key: Chave da API (opcional)
    
    Returns:
        Resultado da conversão
    
    Example:
        >>> convert_currency(100, 'USD', 'BRL')
        {'original_amount': 100, 'converted_amount': 520.0, ...}
    """
    converter = CurrencyConverter(api_key)
    return converter.convert(amount, from_currency, to_currency)

def get_exchange_rate(from_currency: str, to_currency: str, api_key: Optional[str] = None) -> float:
    """
    Obtém apenas a taxa de câmbio entre duas moedas
    
    Args:
        from_currency: Moeda de origem
        to_currency: Moeda de destino
        api_key: Chave da API (opcional)
    
    Returns:
        Taxa de câmbio
    
    Example:
        >>> get_exchange_rate('USD', 'BRL')
        5.20
    """
    result = convert_currency(1, from_currency, to_currency, api_key)
    return result['exchange_rate']

# Exemplo de uso
if __name__ == "__main__":
    print("💱 Testando CurrencyConverter...")
    print("=" * 50)
    
    converter = CurrencyConverter()
    
    # Testes básicos
    test_conversions = [
        (100, 'USD', 'BRL'),
        (50, 'EUR', 'USD'),
        (1000, 'BRL', 'USD'),
        (25, 'GBP', 'EUR'),
        (10000, 'JPY', 'USD')
    ]
    
    for amount, from_curr, to_curr in test_conversions:
        try:
            result = converter.convert(amount, from_curr, to_curr)
            print(f"\n💰 {result['formatted_original']} → {result['formatted_result']}")
            print(f"   Taxa: 1 {from_curr} = {result['exchange_rate']:.4f} {to_curr}")
            print(f"   Fonte: {result['source']}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    # Lista moedas suportadas
    print(f"\n📋 Moedas suportadas: {len(converter.get_supported_currencies())}")
    for code, info in list(converter.get_supported_currencies().items())[:5]:
        print(f"   {code}: {info['name']} ({info['symbol']})")
    print("   ...")
    
    print("\n✅ Testes concluídos!")
