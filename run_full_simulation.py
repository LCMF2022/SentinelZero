#!/usr/bin/env python3
"""
SentinelZero Pre-Production Simulation + PDF + Dashboard v3.7
Autor: Luis Carlos
Descrição: Simulação completa de protocolos/tokens com logging, backup,
validacao JSON schema, PDF institucional e dashboard HTML interativo.
"""

import os
import sys
import subprocess
import json
import shutil
import importlib.util
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Dependências obrigatórias
REQUIRED_MODULES = ["requests", "pytest", "jsonschema", "reportlab"]

# Diretórios
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, "sentinelzero")
TESTS_DIR = os.path.join(PROJECT_ROOT, "tests")
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
BACKUP_DIR = os.path.join(PROJECT_ROOT, "backup")
CACHE_DIR = os.path.join(PROJECT_ROOT, "cache")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
REPORT_TXT = os.path.join(LOGS_DIR, f"report_{TIMESTAMP}.txt")
REPORT_HTML = os.path.join(LOGS_DIR, f"report_{TIMESTAMP}.html")
REPORT_PDF = os.path.join(REPORTS_DIR, f"report_{TIMESTAMP}.pdf")
DASHBOARD_HTML = os.path.join(REPORTS_DIR, f"dashboard_{TIMESTAMP}.html")

TOKENS_PROTOCOLS = [
    "aave", "uni", "compound", "makerdao", "curve",
    "sushi", "balancer", "yearn", "dydx"
]

RISK_CATEGORIES = ["Governance", "Liquidity", "Oracle"]
CACHE_TTL = timedelta(hours=1)

# Schema JSON do output
OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "protocol": {"type": "string"},
        "tvl_usd": {"type": ["number", "null"]},
        "market_cap_usd": {"type": ["number", "null"]},
        "volume_24h_usd": {"type": ["number", "null"]},
        "risk_score": {"type": "integer", "minimum": 0, "maximum": 100},
        "risk_findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"category": {"type": "string"}, "description": {"type": "string"}},
                "required": ["category", "description"]
            }
        },
        "risk_summary": {"type": "object"}
    },
    "required": ["protocol", "risk_score", "risk_findings"]
}

API_PING_URLS = {
    "coingecko": "https://api.coingecko.com/api/v3/ping",
    "defillama": "https://api.llama.fi/protocols"
}

# Logger
class SimulationLogger:
    def __init__(self):
        self.report_lines: List[str] = []
        for d in [LOGS_DIR, BACKUP_DIR, CACHE_DIR, REPORTS_DIR]:
            os.makedirs(d, exist_ok=True)

    def log(self, msg: str, level: str = "INFO") -> None:
        symbols = {"INFO": "ℹ️", "OK": "✔️", "ERROR": "❌", "WARN": "⚠️", "FIXED": "🛠️", "DONE": "🏁"}
        timestamp = datetime.now().strftime('%H:%M:%S')
        line = f"[{timestamp}] {symbols.get(level, ' ')} {level}: {msg}"
        print(line)
        self.report_lines.append(line)

    def save_txt_report(self) -> str:
        with open(REPORT_TXT, "w", encoding="utf-8") as f:
            f.write("\n".join(self.report_lines))
        return REPORT_TXT

    def save_html_report(self) -> str:
        html = "<!DOCTYPE html><html lang='pt-BR'><head><meta charset='utf-8'><title>SentinelZero Report</title>"
        html += "<style>body{font-family:monospace;background:#f8f9fa;padding:20px;}\
                .ok{color:green;}.error{color:red;}.warn{color:orange;}.fixed{color:blue;}.done{color:purple;font-weight:bold;}\
                pre{background:white;padding:15px;border-radius:8px;}</style></head><body>"
        html += f"<h2>SentinelZero Report - {TIMESTAMP}</h2><pre>"
        for line in self.report_lines:
            cls=""
            if "✔️" in line: cls="ok"
            elif "❌" in line: cls="error"
            elif "⚠️" in line: cls="warn"
            elif "🛠️" in line: cls="fixed"
            elif "🏁" in line: cls="done"
            html += f'<span class="{cls}">{line}</span>\n'
        html += "</pre></body></html>"
        with open(REPORT_HTML, "w", encoding="utf-8") as f:
            f.write(html)
        return REPORT_HTML

    def save_pdf_report(self) -> str:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(REPORT_PDF, pagesize=letter)
        width, height = letter
        y = height - 50
        c.setFont("Courier", 10)
        c.drawString(50, y, f"SentinelZero Report - {TIMESTAMP}")
        y -= 20
        for line in self.report_lines:
            if y < 50:
                c.showPage()
                y = height - 50
                c.setFont("Courier", 10)
            c.drawString(50, y, line)
            y -= 12
        c.save()
        return REPORT_PDF

    def save_dashboard_html(self, data_summary: Dict[str, int]) -> str:
        chart_data = [data_summary.get(cat,0) for cat in RISK_CATEGORIES]
        html = f"""<!DOCTYPE html>
<html lang='pt-BR'>
<head><meta charset='utf-8'><title>Dashboard SentinelZero</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
<h2>Dashboard SentinelZero - {TIMESTAMP}</h2>
<canvas id="riskChart" width="600" height="400"></canvas>
<script>
const ctx = document.getElementById('riskChart').getContext('2d');
new Chart(ctx, {{
    type: 'bar',
    data: {{
        labels: {RISK_CATEGORIES},
        datasets: [{{
            label: 'Achados por Categoria',
            data: {chart_data},
            backgroundColor: ['rgba(75,192,192,0.6)','rgba(255,206,86,0.6)','rgba(255,99,132,0.6)']
        }}]
    }},
    options: {{responsive:true,plugins:{{legend:{{position:'top'}}}}}}
}});
</script>
</body>
</html>"""
        with open(DASHBOARD_HTML, "w", encoding="utf-8") as f:
            f.write(html)
        return DASHBOARD_HTML

# Funções auxiliares
def install_module(module: str):
    subprocess.check_call([sys.executable, "-m", "pip", "install", module])

def check_modules(logger: SimulationLogger):
    logger.log("Verificando dependências...")
    for mod in REQUIRED_MODULES:
        if importlib.util.find_spec(mod) is None:
            logger.log(f"Instalando {mod}...", "WARN")
            install_module(mod)
            logger.log(f"{mod} instalado com sucesso", "FIXED")
        else:
            logger.log(f"{mod} já instalado", "OK")

def auto_fix_pythonpath(logger: SimulationLogger) -> bool:
    pp = os.environ.get("PYTHONPATH", "")
    if SRC_DIR not in pp.split(os.pathsep):
        os.environ["PYTHONPATH"] = f"{SRC_DIR}{os.pathsep}{pp}"
        logger.log(f"PYTHONPATH atualizado: {SRC_DIR}", "FIXED")
        return True
    logger.log("PYTHONPATH já configurado", "OK")
    return False

def backup_project(logger: SimulationLogger):
    backup_path = os.path.join(BACKUP_DIR, f"backup_{TIMESTAMP}")
    try:
        shutil.copytree(
            PROJECT_ROOT, backup_path,
            ignore=shutil.ignore_patterns('venv*', '__pycache__', 'logs', 'backup', 'cache')
        )
        logger.log(f"Backup completo criado: {backup_path}", "OK")
    except Exception as e:
        logger.log(f"Falha no backup: {e}", "ERROR")

def check_apis(logger: SimulationLogger):
    import requests
    logger.log("Testando conectividade das APIs...")
    for name,url in API_PING_URLS.items():
        try:
            r=requests.get(url,timeout=10)
            r.raise_for_status()
            logger.log(f"{name} OK (status {r.status_code})","OK")
        except Exception as e:
            logger.log(f"Falha em {name}: {e}","ERROR")

def run_pytest(logger: SimulationLogger):
    logger.log("Rodando testes unitários...")
    if not os.path.exists(TESTS_DIR):
        logger.log(f"Diretório de testes não encontrado: {TESTS_DIR}","WARN")
        return
    try:
        result=subprocess.run(
            [sys.executable,"-m","pytest",TESTS_DIR,"-q","--disable-warnings"],
            capture_output=True,text=True,check=True
        )
        logger.log("Testes passaram com sucesso","OK")
        if result.stdout.strip():
            logger.log("Saída pytest:\n"+result.stdout)
    except subprocess.CalledProcessError as e:
        logger.log(f"Testes falharam (código {e.returncode})","ERROR")
        logger.log(e.stdout)
        logger.log(e.stderr)

def run_example(entity: str, logger: SimulationLogger) -> Dict[str,int]:
    import jsonschema
    import random

    logger.log(f"Analisando {entity}...")
    # Mock de output realista
    data = {
        "protocol": entity,
        "tvl_usd": random.randint(10_000_000,100_000_000),
        "market_cap_usd": random.randint(50_000_000,500_000_000),
        "volume_24h_usd": random.randint(1_000_000,50_000_000),
        "risk_score": random.randint(0,100),
        "risk_findings":[
            {"category":"Governance","description":"Example finding"} if random.random()<0.3 else
            {"category":"Liquidity","description":"Example finding"} if random.random()<0.2 else
            {"category":"Oracle","description":"Example finding"} if random.random()<0.1 else
            {}
            for _ in range(random.randint(0,3))
        ],
        "risk_summary":{"total": random.randint(0,5)}
    }
    # Remover achados vazios
    data["risk_findings"] = [f for f in data["risk_findings"] if f]
    try:
        jsonschema.validate(instance=data,schema=OUTPUT_SCHEMA)
        logger.log(f"{entity} → JSON válido e conforme schema","OK")
        summary = {cat:len([f for f in data["risk_findings"] if f["category"]==cat]) for cat in RISK_CATEGORIES}
        for cat,count in summary.items():
            logger.log(f"  {cat}: {count} achados","INFO")
        return summary
    except jsonschema.ValidationError as e:
        logger.log(f"JSON não conforme schema: {e.message}","ERROR")
        return {cat:0 for cat in RISK_CATEGORIES}

def main():
    logger=SimulationLogger()
    logger.log("=== Iniciando Simulação SentinelZero v3.7 ===","DONE")
    check_modules(logger)
    auto_fix_pythonpath(logger)
    backup_project(logger)
    check_apis(logger)
    run_pytest(logger)

    # Acumular resumo de achados
    dashboard_summary = {cat:0 for cat in RISK_CATEGORIES}
    for entity in TOKENS_PROTOCOLS:
        entity_summary = run_example(entity,logger)
        for cat in RISK_CATEGORIES:
            dashboard_summary[cat]+=entity_summary.get(cat,0)

    txt_path = logger.save_txt_report()
    html_path = logger.save_html_report()
    pdf_path = logger.save_pdf_report()
    dashboard_path = logger.save_dashboard_html(dashboard_summary)

    logger.log(f"Relatório TXT: {txt_path}","DONE")
    logger.log(f"Relatório HTML: {html_path}","DONE")
    logger.log(f"Relatório PDF: {pdf_path}","DONE")
    logger.log(f"Dashboard HTML: {dashboard_path}","DONE")

    # Abrir arquivos automaticamente
    try:
        if os.name=="nt":
            os.startfile(pdf_path)
            os.startfile(dashboard_path)
        else:
            subprocess.run(["open",pdf_path])
            subprocess.run(["open",dashboard_path])
    except Exception as e:
        logger.log(f"Falha ao abrir relatórios automaticamente: {e}","WARN")

    # Resumo final
    errors=sum(1 for l in logger.report_lines if "❌" in l)
    warns=sum(1 for l in logger.report_lines if "⚠️" in l)
    fixes=sum(1 for l in logger.report_lines if "🛠️" in l)
    print("\n"+"="*60)
    print("Resumo Final:")
    print(f"  Erros:     {errors}")
    print(f"  Avisos:    {warns}")
    print(f"  Auto-fixes:{fixes}")
    print("="*60)
    if errors>0:
        print("⚠️  ATENÇÃO: Existem erros críticos! Revisar antes de produção.")
    else:
        print("✅  Simulação concluída com sucesso. Pronto para produção!")

if __name__=="__main__":
    main()
