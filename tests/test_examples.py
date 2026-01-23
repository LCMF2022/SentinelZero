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

import subprocess
import json

SYMBOLS = ["aave", "makerdao", "link"]

def test_run_analysis():
    for s in SYMBOLS:
        result = subprocess.run(
            ["python", "-m", "examples.run_analysis_unified", s],
            capture_output=True, text=True
        )
        assert result.returncode == 0

        data = json.loads(result.stdout)
        assert "entity" in data
        assert "type" in data
        assert "risk_findings" in data
        assert "risk_score" in data

        if data["type"] == "token":
            assert data["risk_findings"] == []
            assert data["risk_score"] == 50
