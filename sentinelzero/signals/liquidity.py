from sentinelzero.core.models import RiskSignal, RiskCategory, Severity
from sentinelzero.core.enums import RiskCategory, Severity


def liquidity_signals(entity: dict) -> list[RiskSignal]:
    return [
        RiskSignal(
            category=RiskCategory.LIQUIDITY,
            description="Liquidity concentration risk",
            severity=Severity.MEDIUM,
            rationale=(
                "Liquidity may be concentrated in a small number of pools, "
                "increasing slippage and exit risk."
            )
        )
    ]
