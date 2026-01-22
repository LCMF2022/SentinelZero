def build_report(snapshot, score, signals):
    return {
        "protocol": snapshot.name,
        "category": snapshot.category,
        "tvl_usd": snapshot.tvl,
        "tvl_change_7d_pct": snapshot.tvl_change_7d,
        "risk_score": score,
        "risk_findings": [
            {
                "category": s.category.value,
                "severity": s.severity.value,
                "description": s.description,
            }
            for s in signals
        ],
    }
