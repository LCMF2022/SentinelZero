# ======================================================
# run_all_tests_pro.ps1 - PowerShell limpo e compatível
# ======================================================

# Configurar PYTHONPATH
$env:PYTHONPATH = "C:\sentinelzero\sentinelzero"
Write-Host "[OK] PYTHONPATH configurado: $env:PYTHONPATH"

# Ativar virtual environment se existir
if (Test-Path .\venv\Scripts\Activate.ps1) {
    Write-Host "[OK] Ativando virtual environment..."
    .\venv\Scripts\Activate.ps1
} else {
    Write-Host "[WARN] Virtual environment não encontrado, continuando sem ele..."
}

# Instalar dependências Python
Write-Host "[INFO] Instalando dependências Python..."
pip install -r requirements.txt

# Rodar testes Python
$pythonTests = $false
if (Test-Path .\tests) {
    Write-Host "[INFO] Rodando testes Python com pytest..."
    pytest tests/ --maxfail=1 --disable-warnings
    if ($LASTEXITCODE -eq 0) {
        $pythonTests = $true
    }
} else {
    Write-Host "[WARN] Pasta 'tests' não encontrada, pulando testes Python..."
}

# Rodar simulação completa
$simulation = $false
if (Test-Path .\run_full_simulation.py) {
    Write-Host "[INFO] Rodando simulação completa..."
    python run_full_simulation.py
    if ($LASTEXITCODE -eq 0) {
        $simulation = $true
    }
} else {
    Write-Host "[WARN] run_full_simulation.py não encontrado, pulando simulação..."
}

# Rodar análise completa
$analysis = $false
if (Test-Path .\run_analysis.py) {
    Write-Host "[INFO] Rodando análise completa..."
    python run_analysis.py
    if ($LASTEXITCODE -eq 0) {
        $analysis = $true
    }
} else {
    Write-Host "[WARN] run_analysis.py não encontrado, pulando análise..."
}

# Rodar testes Node.js
$nodeTests = $false
if (Test-Path .\package.json) {
    Write-Host "[INFO] Rodando testes Node.js..."
    npm install
    npm test
    if ($LASTEXITCODE -eq 0) {
        $nodeTests = $true
    }
} else {
    Write-Host "[WARN] package.json não encontrado, pulando testes Node.js..."
}

# ===================== Relatório Final =====================
Write-Host "===================== Relatório Final ====================="
Write-Host ("Python Tests:       " + $pythonTests)
Write-Host ("Simulation:         " + $simulation)
Write-Host ("Analysis:           " + $analysis)
Write-Host ("Node.js Tests:      " + $nodeTests)
Write-Host "[OK] Todos os logs estão em: C:\sentinelzero\logs"
Write-Host "==========================================================="
