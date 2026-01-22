import sys
import os
# Ajusta path para encontrar o pacote sentinelzero
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
import os
# Ajusta path para encontrar o pacote sentinelzero
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
import os
# Ajusta path para encontrar o pacote sentinelzero
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
import os
# Ajusta path para encontrar o pacote sentinelzero
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
import os
# Ajusta path para encontrar o pacote sentinelzero
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
import os

# Adiciona a subpasta sentinelzero ao início do path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#!/usr/bin/env python3
"""
SentinelZero — Test Engine
Permite testar qualquer protocolo DeFi pelo nome (slug) do DefiLlama.
Exibe relatório resumido no terminal ou em JSON.
"""

import sys
import json

from sentinelzero.datasources.defillama import DefiLlamaSource
from sentinelzero.datasources.coingecko import CoinGeckoSource
from sentinelzero.datasources.incidents import IncidentSource
from sentinelzero.core.engine import RiskEngine
from sentinelzero.reports.formatter import format_report
from sentinelzero.reports.schema import build_report

def parse_args():
    """
    Lê o protocolo da CLI ou fallback para input,
    detecta flags --json e --pretty
    """
    protocol = None
    flags = {"json": False, "pretty": False}

    for arg in sys.argv[1:]:
        if arg.lower() == "--json":
            flags["json"] = True
        elif arg.lower() == "--pretty":
            flags["pretty"] = True
        elif not arg.startswith("--") and protocol is None:
            protocol = arg.lower()

    if protocol is None:
        protocol = input("Digite o nome do protocolo (DefiLlama slug): ").lower()

    return protocol, flags

def main():
    protocol, flags = parse_args()

    # Instancia datasources
    defillama = DefiLlamaSource()
    coingecko = CoinGeckoSource()
    incidents = IncidentSource()

    # Busca dados de protocolo
    try:
        snapshot = defillama.fetch(protocol)
    except Exception:
        print(f"Erro: Protocolo '{protocol}' não encontrado no DefiLlama.")
        return

    market_context = coingecko.get_protocol_context(protocol)
    incident_flags = incidents.get_incidents(protocol)

    # Executa motor de risco
    engine = RiskEngine()
    score, signals = engine.run(snapshot)

    # Saída JSON ou terminal
    if flags["json"]:
        output = build_report(snapshot, score, signals)
        indent = 2 if flags["pretty"] else None
        print(json.dumps(output, indent=indent))
    else:
        print(format_report(snapshot, score, signals))

if __name__ == "__main__":
    main()
