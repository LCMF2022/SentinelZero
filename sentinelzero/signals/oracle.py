from sentinelzero.core.models import RiskSignal, RiskCategory, Severity
from sentinelzero.core.enums import RiskCategory, Severity

def oracle_signals(entity: dict) -> list[RiskSignal]:
    return [
        RiskSignal(
            category=RiskCategory.ORACLE,
            description="Dependency on external price feeds",
            severity=Severity.MEDIUM,
            rationale="Reliance on third-party oracles introduces trust assumptions."
        ),
        RiskSignal(
            category=RiskCategory.ORACLE,
            description="Oracle price feeds may rely on low-liquidity markets",
            severity=Severity.HIGH,
            rationale="Low-liquidity reference markets increase manipulation risk."
        )
    ]
