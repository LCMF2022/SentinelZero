# run_analysis.py (trecho ajustado)

def calculate_risk_score(tvl_usd, volume_24h_usd, risks):
    """
    Calcula o risco de um protocolo DeFi baseado em TVL, volume e sinais de risco.
    tvl_usd e volume_24h_usd podem ser int, float ou lista.
    """
    # Garantir que sejam números
    if isinstance(tvl_usd, list):
        tvl_usd = sum(tvl_usd)  # soma todos os valores se for lista
    if isinstance(volume_24h_usd, list):
        volume_24h_usd = sum(volume_24h_usd)

    # Risco baseado em TVL
    risk_score = 0
    if tvl_usd < 10_000_000:
        risk_score += 2
    elif tvl_usd < 50_000_000:
        risk_score += 1

    # Risco baseado em volume
    if volume_24h_usd < 500_000:
        risk_score += 1

    # Adiciona riscos detectados
    risk_score += len(risks)

    return risk_score

def run_analysis(protocol_input):
    """
    Executa análise completa para o protocolo informado.
    """
    from sentinelzero.datasources.defillama import DefiLlamaSource
    from sentinelzero.datasources.dexscreener import DexScreenerSource
    from sentinelzero.core.scoring import calculate_risk_score

    defi_data = DefiLlamaSource.get_protocol_data(protocol_input)
    dexscreener_data = DexScreenerSource.get_protocol_data(protocol_input)
    risks = defi_data.get("risks", [])

    tvl_usd = defi_data.get("tvl_usd") or 0
    volume_24h_usd = dexscreener_data.get("volume_24h_usd") if dexscreener_data else 0

    # Corrigir se forem listas
    if isinstance(tvl_usd, list):
        tvl_usd = sum(tvl_usd)
    if isinstance(volume_24h_usd, list):
        volume_24h_usd = sum(volume_24h_usd)

    risk_score = calculate_risk_score(tvl_usd, volume_24h_usd, risks)

    print(f"[INFO] {protocol_input} → TVL: {tvl_usd}, Volume 24h: {volume_24h_usd}, Score: {risk_score}")
    return {
        "protocol": protocol_input,
        "tvl_usd": tvl_usd,
        "volume_24h_usd": volume_24h_usd,
        "risks": risks,
        "risk_score": risk_score
    }

if __name__ == "__main__":
    protocol_input = input("Enter protocol name or token symbol (e.g., aave, makerdao, link): ").strip()
    run_analysis(protocol_input)
