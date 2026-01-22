# run_protocol_dashboard.ps1
# --------------------------
# SentinelZero Professional Risk Dashboard
# --------------------------

# Python environment
$pythonPath = ".\venv\Scripts\python.exe"

# Reports folder
$reportsFolder = ".\reports"
if (-not (Test-Path $reportsFolder)) {
    New-Item -ItemType Directory -Path $reportsFolder | Out-Null
}

# Function to save CSV
function Save-ToCsv($data, $filePath) {
    if ($data -and $data.risk_findings) {
        $data.risk_findings | Export-Csv -Path $filePath -NoTypeInformation -Encoding UTF8
    }
}

# Main Loop
while ($true) {
    $protocol = Read-Host "Enter protocol name or token symbol (e.g., aave, makerdao, link)"
    
    if ([string]::IsNullOrWhiteSpace($protocol)) {
        Write-Host "No protocol entered. Exiting..."
        break
    }

    # Run Python analysis
    $jsonOutput = & $pythonPath run_analysis.py $protocol 2>&1
    $data = $null
    try {
        $data = $jsonOutput | ConvertFrom-Json
    } catch {
        Write-Host "Protocol '$protocol' not found or no data available."
        continue
    }

    Write-Host ""
    Write-Host "=== SentinelZero Professional Risk Dashboard ==="
    Write-Host ""
    Write-Host ("Protocol: " + $data.protocol)
    if ($data.tvl_usd) { Write-Host ("Total Value Locked (TVL): " + ($data.tvl_usd.ToString("C0"))) }
    if ($data.price_usd) { Write-Host ("Token Price (USD): " + ($data.price_usd)) }
    if ($data.market_cap_usd) { Write-Host ("Market Cap (USD): " + ($data.market_cap_usd.ToString("C0"))) }
    if ($data.volume_24h_usd) { Write-Host ("24h Volume (USD): " + ($data.volume_24h_usd.ToString("C0"))) }
    Write-Host ("Risk Score: " + $data.risk_score + "/100")
    Write-Host ""
    
    Write-Host "Detected Risks:"
    if ($data.risk_findings.Count -eq 0) {
        Write-Host "No specific risks detected."
    } else {
        foreach ($r in $data.risk_findings) {
            Write-Host (" - [" + $r.category + "] " + $r.description + " - " + $r.details)
        }
    }

    Write-Host ""
    Write-Host "Summary by Risk Category:"
    if ($data.risk_summary.Count -eq 0) {
        Write-Host "No risks to summarize."
    } else {
        foreach ($cat in $data.risk_summary.Keys) {
            Write-Host (" - " + $cat + ": " + $data.risk_summary[$cat] + " risk(s)")
        }
    }

    # Save reports
    $safeName = $data.protocol -replace '[^a-zA-Z0-9_-]', '_'
    $jsonFile = Join-Path $reportsFolder ("${safeName}_professional_dashboard.json")
    $csvFile  = Join-Path $reportsFolder ("${safeName}_professional_dashboard.csv")
    
    $data | ConvertTo-Json -Depth 5 | Set-Content $jsonFile -Encoding UTF8
    Save-ToCsv -data $data -filePath $csvFile

    Write-Host ""
    Write-Host "Reports generated successfully!"
    Write-Host ("JSON saved to: " + $jsonFile)
    Write-Host ("CSV saved to: " + $csvFile)
    Write-Host "=== End of Dashboard ==="
    Write-Host ""
}
