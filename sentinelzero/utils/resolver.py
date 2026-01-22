ENTITY_REGISTRY = {
    "aave": {
        "type": "protocol",
        "name": "Aave V3",
        "defillama_slug": "aave-v3"
    },
    "makerdao": {
        "type": "protocol",
        "name": "MakerDAO",
        "defillama_slug": "makerdao"
    },
    "link": {
        "type": "token",
        "name": "Chainlink",
        "coingecko_id": "chainlink"
    }
}

def resolve_identifier(query: str) -> dict:
    key = query.lower().strip()

    if key not in ENTITY_REGISTRY:
        return {"type": "unknown"}

    return ENTITY_REGISTRY[key]
