from dataclasses import dataclass
from enum import Enum

class RiskCategory(str, Enum):
    SECURITY = 'Security'
    GOVERNANCE = 'Governance'
    LIQUIDITY = 'Liquidity'
    OPERATIONAL = 'Operational'

class Severity(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'

@dataclass(frozen=True)
class RiskSignal:
    category: RiskCategory
    description: str
    severity: Severity
    rationale: str
    source: str = 'heuristic'
