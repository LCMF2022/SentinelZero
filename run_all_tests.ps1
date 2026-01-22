# ==============================================
# SentinelZero - Test Runner Completo Windows
# ==============================================

# Caminho para o pacote
$packageDir = "$PWD\sentinelzero"

# Caminho para os testes
$testsDir = "$PWD\tests"

# Configura PYTHONPATH para a subpasta sentinelzero
$env:PYTHONPATH = $packageDir
Write-Host "✅ PYTHONPATH configurado para $packageDir"

# Instalar dependências essenciais
Write-Host "⏳ Instalando dependências..."
python -m pip install --upgrade pip
python -m pip install requests pytest --quiet
Write-Host "✅ Dependências instaladas"

# Gerar log
$logFile = "$PWD\logs\test_log_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
if (-not (Test-Path "$PWD\logs")) { New-Item -ItemType Directory -Path "$PWD\logs" }

# Rodar pytest e salvar log
Write-Host "⏳ Rodando todos os testes..."
pytest $testsDir --maxfail=1 --disable-warnings -v | Tee-Object $logFile

Write-Host "✅ Testes concluídos! Log salvo em: $logFile"
