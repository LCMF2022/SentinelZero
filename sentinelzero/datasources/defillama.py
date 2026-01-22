# sentinelzero/datasources/defillama.py

from typing import Optional

class DefiLlamaSource:
    """
    Mock/fake source para testes.
    Retorna valores de TVL fixos para que a suíte de testes funcione sem conexão externa.
    """

    def __init__(self):
        # Opcional: dicionário de TVL fixo para símbolos de teste
        self.tvl_data = {
            "aave": 3_000_000_000,
            "makerdao": 2_500_000_000,
            "link": 0
        }

    def get_tvl(self, symbol: str) -> Optional[float]:
        """
        Retorna TVL fixo para um símbolo. Se não existir, retorna None.
        """
        return self.tvl_data.get(symbol.lower())
