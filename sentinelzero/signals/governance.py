from typing import List
from sentinelzero.core.models import RiskSignal, RiskCategory, Severity

def governance_signals(entity: dict) -> List[RiskSignal]:
    if entity.get('type') != 'protocol':
        return []

    return [
        RiskSignal(
            category=RiskCategory.GOVERNANCE,
            description='Upgradeable contracts controlled by small multisig',
            severity=Severity.HIGH,
            rationale='Centralized upgrade authority allows protocol changes without broad consensus.',
            source='heuristic'
        ),
        RiskSignal(
            category=RiskCategory.GOVERNANCE,
            description='Emergency admin powers detected',
            severity=Severity.MEDIUM,
            rationale='Emergency controls introduce governance and legal risk.',
            source='heuristic'
        )
    ]
