import requests
import json

# ----------------------
# Data Sources
# ----------------------

def fetch_defillama(protocol_or_address):
    url = f"https://api.llama.fi/protocol/{protocol_or_address}"
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        return {
            "tvl_usd": data.get("tvl", 0),
            "name": protocol_or_address
        }
    except:
        return None

def fetch_coingecko(token_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_id}&vs_currencies=usd&include_market_cap=true"
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json().get(token_id, {})
        return {"price_usd": data.get("usd"), "market_cap_usd": data.get("usd_market_cap")}
    except:
        return None

def fetch_dexscreener(token_address):
    url = f"https://api.dexscreener.io/latest/dex/tokens/{token_address}"
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        return {"volume_24h_usd": float(data.get("pairs", [{}])[0].get("volumeUsd", 0))}
    except:
        return None

def fetch_dune(query_id):
    return {"dune_metric_example": 123456}

def fetch_moralis(wallet_address):
    return {"wallet_tx_count": 42}

# ----------------------
# Risk Assessment
# ----------------------
def assess_risks():
    risks = [
        {"category": "Governance", "description": "Upgradeable contracts controlled by small multisig", "severity": 2, "details": "Upgradeable contract controls and admin powers may affect security and protocol decisions."},
        {"category": "Governance", "description": "Presence of emergency admin powers", "severity": 2, "details": "Upgradeable contract controls and admin powers may affect security and protocol decisions."},
        {"category": "Oracle", "description": "Single oracle dependency detected", "severity": 4, "details": "Oracle dependency may lead to inaccurate prices and financial vulnerabilities."},
        {"category": "Oracle", "description": "Oracle price feed may rely on low-liquidity markets", "severity": 2, "details": "Oracle dependency may lead to inaccurate prices and financial vulnerabilities."}
    ]
    summary = {}
    for r in risks:
        cat = r["category"]
        summary[cat] = summary.get(cat, 0) + 1
    return risks, summary

# ----------------------
# Dynamic Risk Score
# ----------------------
def calculate_risk_score(tvl_usd, volume_24h_usd, risk_findings):
    score = 50  # base score
    # TVL impact
    if tvl_usd:
        if tvl_usd < 10_000_000:
            score += 20
        elif tvl_usd < 100_000_000:
            score += 10
    # Volume impact
    if volume_24h_usd:
        if volume_24h_usd < 100_000:
            score += 15
        elif volume_24h_usd < 1_000_000:
            score += 5
    # Risk findings
    for r in risk_findings:
        severity = r.get("severity", 2)
        score += severity * 2
    return min(score, 100)

# ----------------------
# Main Analysis
# ----------------------
def run_analysis(protocol_or_address):
    defi_data = fetch_defillama(protocol_or_address)
    
    # Fallback if DefiLlama fails
    if not defi_data:
        coingecko_data = fetch_coingecko(protocol_or_address)
        dexscreener_data = fetch_dexscreener(protocol_or_address)
        if not coingecko_data and not dexscreener_data:
            return None
        defi_data = {"tvl_usd": None, "name": protocol_or_address}
    else:
        coingecko_data = fetch_coingecko(protocol_or_address)
        dexscreener_data = fetch_dexscreener(protocol_or_address)

    dune_data = fetch_dune(protocol_or_address)
    moralis_data = fetch_moralis(protocol_or_address)
    risks, risk_summary = assess_risks()

    risk_score = calculate_risk_score(
        defi_data.get("tvl_usd") or 0,
        dexscreener_data.get("volume_24h_usd") if dexscreener_data else 0,
        risks
    )

    result = {
        "protocol": protocol_or_address,
        "tvl_usd": defi_data.get("tvl_usd"),
        "price_usd": coingecko_data.get("price_usd") if coingecko_data else None,
        "market_cap_usd": coingecko_data.get("market_cap_usd") if coingecko_data else None,
        "volume_24h_usd": dexscreener_data.get("volume_24h_usd") if dexscreener_data else None,
        "risk_score": risk_score,
        "risk_findings": risks,
        "risk_summary": risk_summary,
        "dune_metrics": dune_data,
        "moralis_metrics": moralis_data
    }

    return result

# ----------------------
# CLI Runner
# ----------------------
if __name__ == "__main__":
    import sys
    protocol_input = sys.argv[1] if len(sys.argv) > 1 else input("Enter protocol name or token symbol (e.g., aave, makerdao, link): ")
    data = run_analysis(protocol_input)
    if not data:
        print(f"Protocol '{protocol_input}' not found or no data available.")
    else:
        print(json.dumps(data, indent=2))
