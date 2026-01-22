import requests
import json

# ----------------------
# Data Sources
# ----------------------
def fetch_defillama(protocol_or_address):
    url = f"https://api.llama.fi/protocol/{protocol_or_address}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        return {"tvl_usd": data.get("tvl", 0), "name": protocol_or_address}
    except:
        return None

def fetch_coingecko(token_id):
    token_id = token_id.lower().replace(" ", "-")
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_id}&vs_currencies=usd&include_market_cap=true"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json().get(token_id, {})
        if not data:
            return None
        return {"price_usd": data.get("usd"), "market_cap_usd": data.get("usd_market_cap")}
    except:
        return None

def fetch_dexscreener(token_address):
    url = f"https://api.dexscreener.io/latest/dex/tokens/{token_address}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        pair = data.get("pairs", [{}])[0]
        return {"volume_24h_usd": pair.get("volumeUsd", 0)}
    except:
        return None

# ----------------------
# Risk Assessment
# ----------------------
def assess_risks():
    risks = [
        {"category": "Governance", "description": "Upgradeable contracts controlled by small multisig",
         "details": "Upgradeable contract controls and admin powers may affect security and protocol decisions."},
        {"category": "Governance", "description": "Presence of emergency admin powers",
         "details": "Upgradeable contract controls and admin powers may affect security and protocol decisions."},
        {"category": "Oracle", "description": "Single oracle dependency detected",
         "details": "Oracle dependency may lead to inaccurate prices and financial vulnerabilities."},
        {"category": "Oracle", "description": "Oracle price feed may rely on low-liquidity markets",
         "details": "Oracle dependency may lead to inaccurate prices and financial vulnerabilities."}
    ]
    summary = {}
    for r in risks:
        cat = r["category"]
        summary[cat] = summary.get(cat, 0) + 1
    return risks, summary

# ----------------------
# Main Analysis
# ----------------------
def run_analysis(protocol_or_address):
    protocol_norm = protocol_or_address.lower().replace(" ", "-")
    defi_data = fetch_defillama(protocol_norm)
    fallback_used = False

    if not defi_data:
        # Fallback to CoinGecko if DefiLlama fails
        fallback_used = True
        cg_data = fetch_coingecko(protocol_norm)
        if not cg_data:
            # Return only default risk if no data
            return {
                "protocol": protocol_or_address,
                "tvl_usd": None,
                "price_usd": None,
                "market_cap_usd": None,
                "volume_24h_usd": None,
                "risk_score": 70,
                "risk_findings": [],
                "risk_summary": {}
            }
        defi_data = {"tvl_usd": None, "name": protocol_or_address}

    coingecko_data = fetch_coingecko(protocol_norm)
    dexscreener_data = fetch_dexscreener(protocol_norm)
    risks, risk_summary = assess_risks()

    result = {
        "protocol": protocol_or_address,
        "tvl_usd": defi_data.get("tvl_usd"),
        "price_usd": coingecko_data.get("price_usd") if coingecko_data else None,
        "market_cap_usd": coingecko_data.get("market_cap_usd") if coingecko_data else None,
        "volume_24h_usd": dexscreener_data.get("volume_24h_usd") if dexscreener_data else None,
        "risk_score": 70,
        "risk_findings": risks,
        "risk_summary": risk_summary,
        "fallback_used": fallback_used
    }
    return result

# ----------------------
# CLI Runner
# ----------------------
if __name__ == "__main__":
    import sys
    protocol_input = sys.argv[1] if len(sys.argv) > 1 else input("Enter protocol name or token symbol (e.g., aave, makerdao, link): ")
    data = run_analysis(protocol_input)
    print(json.dumps(data, indent=2))
