# run_protocol.ps1
param(
    [string]$Protocol = $(Read-Host "Digite o nome do protocolo")
)

$uri = "http://127.0.0.1:8000/risk?protocol=$Protocol"

try {
    $response = Invoke-RestMethod -Uri $uri
    Write-Host "=== SentinelZero Risk Report ===" -ForegroundColor Cyan
    Write-Host "Protocolo: $($response.protocol)"
    Write-Host ("TVL: $" + "{0:N0}" -f $response.tvl_usd)
    Write-Host ("7d Change: " + $response.tvl_change_7d_pct + "%")
    Write-Host ("Risk Score: " + $response.risk_score + "/100")
    Write-Host "Principais Riscos:"
    foreach ($finding in $response.risk_findings) {
        Write-Host (" - [" + $finding.category + "] " + $finding.description)
    }
} catch {
    Write-Host "Erro ao consultar a API:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
