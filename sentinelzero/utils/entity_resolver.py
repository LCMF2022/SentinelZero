def resolve_entity(symbol: str) -> dict:
    ENTITIES = {
        'aave': {'name': 'Aave', 'type': 'protocol', 'tvl': 3_000_000_000},
        'makerdao': {'name': 'MakerDAO', 'type': 'protocol', 'tvl': 2_500_000_000},
        'link': {'name': 'Chainlink', 'type': 'token'}
    }
    return ENTITIES.get(symbol.lower(), {'name': symbol, 'type': 'unknown'})
