#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from sentinelzero.datasources.defillama import DefiLlamaSource
from sentinelzero.datasources.coingecko import CoinGeckoSource
from sentinelzero.datasources.incidents import IncidentSource
from sentinelzero.core.engine import RiskEngine
from sentinelzero.reports.schema import build_report

app = FastAPI(title="SentinelZero Risk API", version="1.0")

# Pydantic model para validação de entrada
class ProtocolRequest(BaseModel):
    protocol: str

# Datasources e engine globais
defillama = DefiLlamaSource()
coingecko = CoinGeckoSource()
incidents = IncidentSource()
engine = RiskEngine()


@app.get("/")
def root():
    return {"message": "SentinelZero API — Use /risk?protocol=<protocol_name>"}


@app.get("/risk")
def get_risk(protocol: Optional[str] = None):
    if protocol is None:
        raise HTTPException(status_code=400, detail="Missing protocol parameter")

    protocol = protocol.lower()

    # Fetch snapshot e contexto
    snapshot = defillama.fetch(protocol)
    if snapshot is None:
        raise HTTPException(status_code=404, detail=f"Protocol '{protocol}' not found")

    market_context = coingecko.get_protocol_context(protocol)
    incident_flags = incidents.get_incidents(protocol)

    # Calcula risco
    score, signals = engine.run(snapshot)

    # Retorna JSON pronto
    report = build_report(snapshot, score, signals)
    return report
