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
from sentinelzero.core.models import RiskSignal, Severity, RiskCategory
from sentinelzero.scoring.calculator import calculate_risk

def create_signal(severity):
    return RiskSignal(
        category=RiskCategory.GOVERNANCE,
        description="Test",
        severity=severity,
        rationale="Testing",
        source="heuristic"
    )

def test_score_base():
    # sem sinais, score deve ser base 50
    score = calculate_risk("token", None, [])
    assert score == 50

def test_score_with_severities():
    signals = [create_signal(Severity.LOW), create_signal(Severity.MEDIUM)]
    score = calculate_risk("protocol", 200_000_000, signals)
    # Base 50 + 5 + 10 = 65
    assert score == 65

def test_score_with_tvl_penalty():
    signals = [create_signal(Severity.HIGH)]
    score = calculate_risk("protocol", 50_000_000, signals)
    # Base 50 + 20 + 10 (TVL < 100M) = 80
    assert score == 80
