from .schema import build_report
import json

def format_report(snapshot, score, signals):
    report = build_report(snapshot, score, signals)

    lines = [
        "SentinelZero Listing Risk Report",
        f"Protocol: {report['protocol']}",
        f"TVL: ${report['tvl_usd']:,}",
        f"7d Change: {report['tvl_change_7d_pct']}%",
        "",
        f"Overall Risk Score: {report['risk_score']}/100",
        "",
        "Detected Risk Findings:",
    ]

    for r in report["risk_findings"]:
        lines.append(
            f"- [{r['category']}] {r['description']}"
        )

    return "\n".join(lines)
