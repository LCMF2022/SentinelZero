# sentinelzero/datasources/coingecko.py

from typing import Optional

class CoinGeckoSource:
    """
    Mock/fake source para testes.
    Retorna preços ou dados fixos para que a suíte de testes funcione sem conexão externa.
    """

    def __init__(self):
        # Preço fixo de tokens de teste
        self.price_data = {
            "aave": 90.0,
            "makerdao": 1.0,
            "link": 7.0
        }

    def get_price(self, symbol: str) -> Optional[float]:
        """
        Retorna preço fixo para um símbolo. Se não existir, retorna None.
        """
        return self.price_data.get(symbol.lower())
