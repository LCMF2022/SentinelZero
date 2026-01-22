# ====================================================
# SentinelZero - Testes completos com correção de path
# ====================================================

# Caminho para o pacote
$packageDir = "$PWD"

# Caminho para os testes
$testsDir = Join-Path $packageDir "sentinelzero\tests"

# Criar pasta de logs se não existir
$logDir = Join-Path $packageDir "logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir }

$logFile = Join-Path $logDir ("test_log_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".txt")

Write-Host "Preparando ambiente..."

# 1️⃣ Corrigir todos os testes para adicionar sys.path
Write-Host "Atualizando arquivos de teste para corrigir imports..."
Get-ChildItem -Path $testsDir -Recurse -Include *.py | ForEach-Object {
    $filePath = $_.FullName
    $content = Get-Content $filePath
    if (-not ($content[0] -match "sys\.path\.insert")) {
        $header = @(
            "import sys",
            "import os",
            "# Ajusta path para encontrar o pacote sentinelzero",
            "sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))",
            ""
        )
        $newContent = $header + $content
        Set-Content -Path $filePath -Value $newContent -Force
        Write-Host "Corrigido: $($_.Name)"
    }
}

# 2️⃣ Instalar dependências essenciais
Write-Host "Instalando dependências..."
python -m pip install --upgrade pip --quiet
python -m pip install requests pytest --quiet
Write-Host "Dependências instaladas"

# 3️⃣ Configurar PYTHONPATH
$env:PYTHONPATH = $packageDir
Write-Host "PYTHONPATH configurado para $packageDir"

# 4️⃣ Rodar todos os testes e salvar log
Write-Host "Rodando todos os testes..."
pytest $testsDir --maxfail=1 --disable-warnings -v | Tee-Object $logFile

Write-Host "Testes concluídos! Log salvo em: $logFile"
