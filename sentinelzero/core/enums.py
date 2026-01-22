from enum import Enum

class RiskCategory(Enum):
    LIQUIDITY = "Liquidity"
    GOVERNANCE = "Governance"
    ORACLE = "Oracle"


class Severity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 2
    CRITICAL = 4

