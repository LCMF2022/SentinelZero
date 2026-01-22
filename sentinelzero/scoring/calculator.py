from typing import List, Optional
from sentinelzero.core.models import RiskSignal, Severity

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

    if entity_type == 'protocol' and tvl is not None and tvl < 100_000_000:
        score += 10

    return min(100, score)
