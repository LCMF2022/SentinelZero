#!/usr/bin/env python3
"""
SentinelZero Full Pre-Production Simulation v3.3
Autor: Luis Carlos
Descrição:
- Logging completo
- Backup seguro
- Validação de output JSON
- Cache para APIs externas
- Relatório TXT, HTML e PDF
- Timeout e tratamento de erros robusto
"""

import os
import sys
import subprocess
import json
import shutil
import importlib.util
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Dependências
REQUIRED_MODULES = ["requests", "pytest", "jsonschema", "reportlab"]

# Diretórios
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, "sentinelzero")
TESTS_DIR = os.path.join(PROJECT_ROOT, "tests")
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
BACKUP_DIR = os.path.join(PROJECT_ROOT, "backup")
CACHE_DIR = os.path.join(PROJECT_ROOT, "cache")

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
REPORT_TXT = os.path.join(LOGS_DIR, f"full_prod_sim_report_{TIMESTAMP}.txt")
REPORT_HTML = os.path.join(LOGS_DIR, f"full_prod_sim_report_{TIMESTAMP}.html")
REPORT_PDF = os.path.join(LOGS_DIR, f"full_prod_sim_report_{TIMESTAMP}.pdf")

TOKENS_PROTOCOLS = ["aave", "uni", "compound", "makerdao", "curve", "sushi", "balancer", "yearn", "dydx"]
RISK_CATEGORIES = ["Governance", "Liquidity", "Oracle"]

CACHE_TTL = timedelta(hours=1)
CACHE_FILES = {
    "coingecko": os.path.join(CACHE_DIR, "coingecko.json"),
    "defillama": os.path.join(CACHE_DIR, "defillama.json")
}

API_PING_URLS = {
    "coingecko": "https://api.coingecko.com/api/v3/ping",
    "defillama": "https://api.llama.fi/protocols"
}

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
                "properties": {
                    "category": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["category", "description"]
            }
        },
        "risk_summary": {"type": "object"}
    },
    "required": ["protocol", "risk_score", "risk_findings"]
}

# -----------------------
# Logger
# -----------------------
class SimulationLogger:
    def __init__(self):
        self.report_lines: List[str] = []
        for d in [LOGS_DIR, BACKUP_DIR, CACHE_DIR]:
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
        html = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head><meta charset="utf-8"><title>SentinelZero Report</title>
        <style>
        body {{ font-family: monospace; background: #f8f9fa; padding:20px; }}
        .ok{{color:green}} .error{{color:red}} .warn{{color:orange}} .fixed{{color:blue}} .done{{color:purple;font-weight:bold}}
        pre{{background:white;padding:15px;border-radius:8px;}}
        </style></head><body>
        <h2>SentinelZero Production Simulation Report - {TIMESTAMP}</h2><pre>
        """
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
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            c = canvas.Canvas(REPORT_PDF, pagesize=letter)
            text = c.beginText(40, 750)
            text.setFont("Courier", 10)
            for line in self.report_lines:
                text.textLine(line)
            c.drawText(text)
            c.showPage()
            c.save()
            return REPORT_PDF
        except ImportError:
            self.log("reportlab não instalado, PDF não gerado", "WARN")
            return ""

# -----------------------
# Cache APIs
# -----------------------
def load_cache(name: str) -> Any:
    path = CACHE_FILES.get(name)
    if not path or not os.path.exists(path):
        return None
    with open(path, "r") as f:
        data = json.load(f)
    ts = datetime.fromisoformat(data["timestamp"])
    if datetime.now() - ts < CACHE_TTL:
        return data["data"]
    return None

def save_cache(name: str, data: Any):
    path = CACHE_FILES.get(name)
    if not path:
        return
    with open(path, "w") as f:
        json.dump({"timestamp": datetime.now().isoformat(), "data": data}, f)

# -----------------------
# Funções Auxiliares
# -----------------------
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

def auto_fix_pythonpath(logger: SimulationLogger):
    pp=os.environ.get("PYTHONPATH","")
    if SRC_DIR not in pp.split(os.pathsep):
        os.environ["PYTHONPATH"] = f"{SRC_DIR}{os.pathsep}{pp}"
        logger.log(f"PYTHONPATH atualizado: {SRC_DIR}", "FIXED")
    else:
        logger.log("PYTHONPATH já configurado", "OK")

def backup_project(logger: SimulationLogger):
    backup_path = os.path.join(BACKUP_DIR,f"backup_{TIMESTAMP}")
    try:
        shutil.copytree(PROJECT_ROOT, backup_path, ignore=shutil.ignore_patterns('venv*','__pycache__','logs','backup','cache'))
        logger.log(f"Backup completo criado: {backup_path}", "OK")
    except Exception as e:
        logger.log(f"Falha no backup: {e}", "ERROR")

def check_apis(logger: SimulationLogger):
    import requests
    logger.log("Testando conectividade das APIs...")
    for name,url in API_PING_URLS.items():
        data = load_cache(name)
        if data:
            logger.log(f"{name} cache válido encontrado", "OK")
            continue
        try:
            r=requests.get(url,timeout=10)
            r.raise_for_status()
            logger.log(f"{name} OK (status {r.status_code})", "OK")
            save_cache(name,r.json() if name=="coingecko" else r.text)
        except Exception as e:
            logger.log(f"Falha em {name}: {e}", "ERROR")

def run_pytest(logger: SimulationLogger):
    logger.log("Rodando testes unitários...")
    try:
        result = subprocess.run([sys.executable,"-m","pytest",TESTS_DIR,"-q","--disable-warnings"],capture_output=True,text=True,check=True)
        logger.log("Testes passaram com sucesso","OK")
        if result.stdout.strip():
            logger.log("Saída pytest:\n"+result.stdout)
    except subprocess.CalledProcessError as e:
        logger.log(f"Testes falharam (código {e.returncode})","ERROR")
        logger.log(e.stdout)
        logger.log(e.stderr)

def run_example(entity: str, logger: SimulationLogger):
    logger.log(f"Analisando {entity}...")
    script = os.path.join(SRC_DIR,"examples","run_analysis_unified.py")
    if not os.path.exists(script):
        logger.log("Script de análise não encontrado!", "ERROR")
        return
    try:
        env=os.environ.copy()
        env["PYTHONPATH"]=f"{SRC_DIR}{os.pathsep}{env.get('PYTHONPATH','')}"
        result=subprocess.run([sys.executable,script,entity],capture_output=True,text=True,env=env,timeout=60,check=True)
        output=result.stdout.strip()
        try:
            data:Dict[str,Any]=json.loads(output)
            import jsonschema
            jsonschema.validate(instance=data,schema=OUTPUT_SCHEMA)
            logger.log(f"{entity} → JSON válido e conforme schema","OK")
            findings=data.get("risk_findings",[])
            for cat in RISK_CATEGORIES:
                count=len([f for f in findings if f.get("category")==cat])
                logger.log(f"  {cat}: {count} achados")
        except json.JSONDecodeError as e:
            logger.log(f"JSON inválido: {e}","WARN")
        except jsonschema.ValidationError as e:
            logger.log(f"JSON não conforme schema: {e.message}","ERROR")
    except subprocess.TimeoutExpired:
        logger.log(f"Timeout executando {entity} (60s)","ERROR")
    except subprocess.CalledProcessError as e:
        logger.log(f"Falha na execução de {entity}: {e.stderr.strip()}","ERROR")
    except Exception as e:
        logger.log(f"Erro crítico em {entity}: {str(e)}","ERROR")

# -----------------------
# Execução Principal
# -----------------------
def main():
    logger = SimulationLogger()
    logger.log("=== Iniciando Simulação SentinelZero v3.3 ===","DONE")
    check_modules(logger)
    auto_fix_pythonpath(logger)
    backup_project(logger)
    check_apis(logger)
    run_pytest(logger)
    for entity in TOKENS_PROTOCOLS:
        run_example(entity,logger)
    logger.save_txt_report()
    logger.save_html_report()
    logger.save_pdf_report()
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
        print("✅  Simulação concluída com sucesso. Pronto para deploy real!")

if __name__=="__main__":
    main()
