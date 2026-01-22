# ==============================
# Script para atualizar SentinelZero (com subpasta SentinelZero)
# ==============================

# 1️⃣ core/models.py
@"
from dataclasses import dataclass
from enum import Enum

class RiskCategory(str, Enum):
    SECURITY = "Security"
    GOVERNANCE = "Governance"
    LIQUIDITY = "Liquidity"
    OPERATIONAL = "Operational"

class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass(frozen=True)
class RiskSignal:
    category: RiskCategory
    description: str
    severity: Severity
    rationale: str
    source: str = "heuristic"
"@ | Set-Content -Path .\SentinelZero\core\models.py -Encoding UTF8

# 2️⃣ signals/governance.py
@"
from typing import List
from core.models import RiskSignal, RiskCategory, Severity

def governance_signals(entity: dict) -> List[RiskSignal]:
    if entity.get("type") != "protocol":
        return []

    return [
        RiskSignal(
            category=RiskCategory.GOVERNANCE,
            description="Upgradeable contracts controlled by small multisig",
            severity=Severity.HIGH,
            rationale="Centralized upgrade authority allows protocol changes without broad consensus.",
            source="heuristic"
        ),
        RiskSignal(
            category=RiskCategory.GOVERNANCE,
            description="Emergency admin powers detected",
            severity=Severity.MEDIUM,
            rationale="Emergency controls introduce governance and legal risk.",
            source="heuristic"
        )
    ]
"@ | Set-Content -Path .\SentinelZero\signals\governance.py -Encoding UTF8

# 3️⃣ scoring/calculator.py
@"
from typing import List, Optional
from core.models import RiskSignal, Severity

SEVERITY_WEIGHT = {
    Severity.LOW: 5,
    Severity.MEDIUM: 10,
    Severity.HIGH: 20,
    Severity.CRITICAL: 30
}

BASE_SCORE = 50

def calculate_risk(entity_type: str, tvl: Optional[float], signals: List[RiskSignal]) -> int:
    score = BASE_SCORE
    for s in signals:
        score += SEVERITY_WEIGHT.get(s.severity, 0)

    if entity_type == "protocol" and tvl is not None and tvl < 100_000_000:
        score += 10

    return min(100, score)
"@ | Set-Content -Path .\SentinelZero\scoring\calculator.py -Encoding UTF8

# 4️⃣ examples/run_analysis_unified.py
@"
import sys
import json
from core.models import RiskSignal
from signals.governance import governance_signals
from scoring.calculator import calculate_risk

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
"@ | Set-Content -Path .\SentinelZero\examples\run_analysis_unified.py -Encoding UTF8

# 5️⃣ utils/entity_resolver.py
@"
def resolve_entity(symbol: str) -> dict:
    ENTITIES = {
        'aave': {'name': 'Aave', 'type': 'protocol', 'tvl': 3_000_000_000},
        'makerdao': {'name': 'MakerDAO', 'type': 'protocol', 'tvl': 2_500_000_000},
        'link': {'name': 'Chainlink', 'type': 'token'}
    }
    return ENTITIES.get(symbol.lower(), {'name': symbol, 'type': 'unknown'})
"@ | Set-Content -Path .\SentinelZero\utils\entity_resolver.py -Encoding UTF8

Write-Host "✅ Todos os arquivos em SentinelZero foram atualizados com sucesso!"
