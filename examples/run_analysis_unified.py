import sys
import json
from sentinelzero.core.models import RiskSignal
from sentinelzero.signals.governance import governance_signals
from sentinelzero.scoring.calculator import calculate_risk

ENTITIES = {
    'aave': {'name': 'Aave', 'type': 'protocol', 'tvl': 3_000_000_000},
    'makerdao': {'name': 'MakerDAO', 'type': 'protocol', 'tvl': 2_500_000_000},
    'link': {'name': 'Chainlink', 'type': 'token'}
}

def run_analysis(symbol: str):
    entity = ENTITIES.get(symbol.lower(), {'name': symbol, 'type': 'unknown'})
    signals: list[RiskSignal] = []

    # coleta de sinais
    signals.extend(governance_signals(entity))
    # TODO: adicionar outros sinais

    score = calculate_risk(entity_type=entity['type'], tvl=entity.get('tvl'), signals=signals)

    result = {
        'entity': entity['name'],
        'type': entity['type'],
        'tvl': entity.get('tvl'),
        'risk_findings': [s.__dict__ for s in signals],
        'risk_score': score
    }

    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python -m examples.run_analysis_unified <symbol>')
        sys.exit(1)
    run_analysis(sys.argv[1])
