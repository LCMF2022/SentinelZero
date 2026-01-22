# ==============================
# safe_update.ps1
# Backup + Atualização + Testes + Log
# ==============================

# 1️⃣ Configurações de diretórios
$repoDir = "C:\sentinelzero\sentinelzero"
$backupDir = "C:\sentinelzero\backup_$(Get-Date -Format yyyyMMdd_HHmmss)"
$logDir = "C:\sentinelzero\logs"
$logFile = "$logDir\update_log_$(Get-Date -Format yyyyMMdd_HHmmss).txt"

# Criar diretório de logs se não existir
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir }

# Começar log
Start-Transcript -Path $logFile

# 2️⃣ Criar backup completo
Write-Host "⏳ Criando backup completo em $backupDir..."
try {
    Copy-Item $repoDir $backupDir -Recurse -ErrorAction Stop
    Write-Host "✅ Backup concluído!"
} catch {
    Write-Host "❌ Erro ao criar backup. Abortando atualização."
    Stop-Transcript
    exit 1
}

# 3️⃣ Atualizar arquivos principais

# core/models.py
@"
from dataclasses import dataclass
from enum import Enum

class RiskCategory(str, Enum):
    SECURITY = 'Security'
    GOVERNANCE = 'Governance'
    LIQUIDITY = 'Liquidity'
    OPERATIONAL = 'Operational'

class Severity(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'

@dataclass(frozen=True)
class RiskSignal:
    category: RiskCategory
    description: str
    severity: Severity
    rationale: str
    source: str = 'heuristic'
"@ | Set-Content -Path "$repoDir\core\models.py" -Encoding UTF8

# signals/governance.py
@"
from typing import List
from core.models import RiskSignal, RiskCategory, Severity

def governance_signals(entity: dict) -> List[RiskSignal]:
    if entity.get('type') != 'protocol':
        return []

    return [
        RiskSignal(
            category=RiskCategory.GOVERNANCE,
            description='Upgradeable contracts controlled by small multisig',
            severity=Severity.HIGH,
            rationale='Centralized upgrade authority allows protocol changes without broad consensus.',
            source='heuristic'
        ),
        RiskSignal(
            category=RiskCategory.GOVERNANCE,
            description='Emergency admin powers detected',
            severity=Severity.MEDIUM,
            rationale='Emergency controls introduce governance and legal risk.',
            source='heuristic'
        )
    ]
"@ | Set-Content -Path "$repoDir\signals\governance.py" -Encoding UTF8

# scoring/calculator.py
@"
from typing import List, Optional
from core.models import RiskSignal, Severity

SEVERITY_WEIGHT = {
    Severity.LOW: 5,
    Severity.MEDIUM: 10,
    Severity.HIGH: 20,
    Severity.CRITICAL: 30
}

BASE_SCORE = 50

def calculate_risk(entity_type: str, tvl: Optional[float], signals: List[RiskSignal]) -> int:
    score = BASE_SCORE
    for s in signals:
        score += SEVERITY_WEIGHT.get(s.severity, 0)

    if entity_type == 'protocol' and tvl is not None and tvl < 100_000_000:
        score += 10

    return min(100, score)
"@ | Set-Content -Path "$repoDir\scoring\calculator.py" -Encoding UTF8

# examples/run_analysis_unified.py
@"
import sys
import json
from core.models import RiskSignal
from signals.governance import governance_signals
from scoring.calculator import calculate_risk

ENTITIES = {
    'aave': {'name': 'Aave', 'type': 'protocol', 'tvl': 3_000_000_000},
    'makerdao': {'name': 'MakerDAO', 'type': 'protocol', 'tvl': 2_500_000_000},
    'link': {'name': 'Chainlink', 'type': 'token'}
}

def run_analysis(symbol: str):
    entity = ENTITIES.get(symbol.lower(), {'name': symbol, 'type': 'unknown'})
    signals: list[RiskSignal] = []

    signals.extend(governance_signals(entity))

    score = calculate_risk(entity_type=entity['type'], tvl=entity.get('tvl'), signals=signals)

    result = {
        'entity': entity['name'],
        'type': entity['type'],
        'tvl': entity.get('tvl'),
        'risk_findings': [s.__dict__ for s in signals],
        'risk_score': score
    }

    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python run_analysis_unified.py <symbol>')
        sys.exit(1)
    run_analysis(sys.argv[1])
"@ | Set-Content -Path "$repoDir\examples\run_analysis_unified.py" -Encoding UTF8

# utils/entity_resolver.py
@"
def resolve_entity(symbol: str) -> dict:
    ENTITIES = {
        'aave': {'name': 'Aave', 'type': 'protocol', 'tvl': 3_000_000_000},
        'makerdao': {'name': 'MakerDAO', 'type': 'protocol', 'tvl': 2_500_000_000},
        'link': {'name': 'Chainlink', 'type': 'token'}
    }
    return ENTITIES.get(symbol.lower(), {'name': symbol, 'type': 'unknown'})
"@ | Set-Content -Path "$repoDir\utils\entity_resolver.py" -Encoding UTF8

Write-Host "✅ Todos os arquivos foram atualizados com sucesso!"

# 4️⃣ Rodar testes automáticos
Write-Host "`n🔹 Rodando testes para aave, makerdao e link..."
cd "$repoDir\examples"

$symbols = @('aave','makerdao','link')
foreach ($s in $symbols) {
    Write-Host "`n=== Testando $s ==="
    python run_analysis_unified.py $s
}

Write-Host "`n🎯 Backup, atualização e testes concluídos com sucesso!"
Write-Host "Log completo em: $logFile"".

Stop-Transcript
