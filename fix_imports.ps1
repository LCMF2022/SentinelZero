# fix_imports.ps1
# Uso: roda na raiz do repo SentinelZero
# Objetivo: substituir imports internos de "core", "signals", "scoring", "utils" para "sentinelzero.<pasta>"

# Diretório raiz do repo
$root = Get-Location

# Pastas do projeto que usam imports
$folders = @("core", "signals", "scoring", "utils", "examples", "tests")

# Loop por cada pasta
foreach ($folder in $folders) {
    $files = Get-ChildItem -Path "$root\$folder" -Recurse -Include *.py
    foreach ($file in $files) {
        Write-Host "Processando $($file.FullName)..."

        (Get-Content $file.FullName) |
        ForEach-Object {
            $_ -replace 'from core\.', 'from sentinelzero.core.' `
               -replace 'from signals\.', 'from sentinelzero.signals.' `
               -replace 'from scoring\.', 'from sentinelzero.scoring.' `
               -replace 'from utils\.', 'from sentinelzero.utils.'
        } | Set-Content $file.FullName
    }
}

Write-Host "✅ Todos os imports internos foram atualizados com 'sentinelzero.<pasta>'."
