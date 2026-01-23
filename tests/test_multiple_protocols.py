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
import json
import csv
from sentinelzero.datasources.defillama import DefiLlamaSource
from sentinelzero.core.engine import RiskEngine
from sentinelzero.reports.formatter import format_report
from sentinelzero.reports.schema import build_report
from sentinelzero.core.models import RiskCategory  # Ajuste conforme seu enum

# Lista de protocolos para teste
PROTOCOLS = [
    "aave",
    "compound-finance",
    "uniswap",
    "curve-dao-token",
    "makerdao"
]

# Função utilitária para converter objetos para JSON serializável
def serialize(obj):
    if isinstance(obj, RiskCategory):
        return obj.name
    return str(obj)

def main():
    engine = RiskEngine()
    source = DefiLlamaSource()
    results = []

    print("=== SentinelZero Multi-Protocol Test ===\n")

    for proto in PROTOCOLS:
        print(f"Fetching data for: {proto}")
        try:
            snapshot = source.fetch(proto)
            if not snapshot:
                print(f"Error: No data returned for {proto}")
                continue

            score, signals = engine.run(snapshot)

            # Imprime relatório no terminal
            print(format_report(snapshot, score, signals))
            print("-" * 50)

            # Adiciona ao resultado serializável
            report = build_report(snapshot, score, signals)
            results.append(report)

        except Exception as e:
            print(f"Error fetching {proto}: {e}")
            print("-" * 50)

    # Salva em JSON
    with open("multi_protocol_results.json", "w") as f:
        json.dump(results, f, indent=2, default=serialize)

    # Salva em CSV simples
    with open("multi_protocol_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["protocol", "tvl_usd", "tvl_change_7d_pct", "risk_score", "top_findings"])
        for r in results:
            top_findings = "; ".join([f"{f['category']}:{f['description']}" for f in r["risk_findings"]])
            writer.writerow([r["protocol"], r["tvl_usd"], r["tvl_change_7d_pct"], r["risk_score"], top_findings])

    print("\nResults saved to multi_protocol_results.json and multi_protocol_results.csv")


if __name__ == "__main__":
    main()
