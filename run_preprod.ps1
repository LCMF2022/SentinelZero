# ==================================================
# run_preprod.ps1 — Automatização de Pré-Produção
# ==================================================

# Caminhos
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPath = Join-Path $repoRoot "venv"
$testsSrc = Join-Path $repoRoot "sentinelzero\tests"
$testsDest = Join-Path $repoRoot "tests"

Write-Host "Iniciando rotina de pré-produção SentinelZero v3.7..." -ForegroundColor Cyan

# 1️⃣ Copiar /tests para a raiz se não existir
if (-Not (Test-Path $testsDest)) {
    Write-Host "Copiando /tests para a raiz..." -ForegroundColor Yellow
    Copy-Item -Path $testsSrc -Destination $testsDest -Recurse
    Write-Host "/tests copiada para a raiz"
} else {
    Write-Host "/tests já existe na raiz, pulando cópia"
}

# 2️⃣ Ativar virtualenv
$activate = Join-Path $venvPath "Scripts\Activate.ps1"
if (Test-Path $activate) {
    Write-Host "Ativando venv..."
    & $activate
} else {
    Write-Host "venv não encontrada! Execute primeiro: python -m venv venv" -ForegroundColor Red
    exit 1
}

# 3️⃣ Instalar dependências (se necessário)
Write-Host "Instalando dependências..." -ForegroundColor Yellow
pip install -r "$repoRoot\requirements.txt"

# 4️⃣ Rodar simulação completa
Write-Host "Rodando run_full_simulation.py..." -ForegroundColor Cyan
python "$repoRoot\run_full_simulation.py"

Write-Host "Rotina de pré-produção finalizada!" -ForegroundColor Green
