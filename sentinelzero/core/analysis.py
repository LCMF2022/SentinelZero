from sentinelzero.utils.resolver import resolve_identifier
from sentinelzero.signals.governance import governance_signals
from sentinelzero.signals.oracle import oracle_signals
from sentinelzero.scoring.calculator import calculate_risk

def run_unified_analysis(identifier: str) -> dict:
    entity = resolve_identifier(identifier)

    if entity["type"] == "unknown":
        return {"error": "Identifier not found"}

    signals = []
    signals.extend(governance_signals(entity))
    signals.extend(oracle_signals(entity))

    score = calculate_risk(
        entity_type=entity["type"],
        tvl=entity.get("tvl"),
        signals=signals
    )

    summary = {}
    for s in signals:
        summary[s.category.value] = summary.get(s.category.value, 0) + 1

    return {
        "protocol": entity.get("name", identifier),
        "risk_score": score,
        "risk_findings": [s.to_dict() for s in signals],
        "risk_summary": summary
    }
