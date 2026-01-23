import sys
import os
# Ajusta path para encontrar o pacote sentinelzero
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
import os
# Ajusta path para encontrar o pacote sentinelzero
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
import os
# Ajusta path para encontrar o pacote sentinelzero
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
import os
# Ajusta path para encontrar o pacote sentinelzero
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
import os
# Ajusta path para encontrar o pacote sentinelzero
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
import os

# Adiciona a subpasta sentinelzero ao início do path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from sentinelzero.signals.governance import governance_signals
from sentinelzero.core.models import RiskSignal

def test_governance_only_protocol():
    # protocolo deve retornar sinais
    entity_protocol = {"name": "Aave", "type": "protocol"}
    signals = governance_signals(entity_protocol)
    assert len(signals) >= 1
    assert all(isinstance(s, RiskSignal) for s in signals)

    # token não deve retornar sinais
    entity_token = {"name": "Chainlink", "type": "token"}
    signals_token = governance_signals(entity_token)
    assert signals_token == []
