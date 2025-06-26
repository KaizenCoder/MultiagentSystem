import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import asyncio
from agents.agent_MAINTENANCE_09_analyseur_securite import AgentMAINTENANCE09AnalyseurSecurite, Task
from tools.universal_audit_report import generate_universal_audit_md

async def audit_and_export_md():
    # Charger le code à auditer
    with open("agents/agent_POSTGRESQL_web_researcher.py", "r", encoding="utf-8") as f:
        code = f.read()

    # Instancier l'agent
    agent = AgentMAINTENANCE09AnalyseurSecurite()
    await agent.startup()

    # Créer la tâche d'audit
    task = Task(
        type="security_scan",
        params={"code": code, "file_path": "agent_POSTGRESQL_web_researcher.py"}
    )

    # Exécuter l'audit
    result = await agent.execute_task(task)
    if result.success:
        report = result.data["security_report"]
        # Générer le rapport Markdown existant
        output_md = "reports/audits/agent_POSTGRESQL_web_researcher_security_audit.md"
        Path("reports/audits").mkdir(parents=True, exist_ok=True)
        agent.export_security_report_md(report, output_md)
        print(f"Rapport Markdown classique généré : {output_md}")
        # Générer le rapport Markdown universel
        output_md_universal = "reports/audits/agent_POSTGRESQL_web_researcher_security_audit_universal.md"
        generate_universal_audit_md(report, agent_type="sécurité", output_path=output_md_universal, extra={"auditeur": "AgentMAINTENANCE09AnalyseurSecurite"})
        print(f"Rapport Markdown universel généré : {output_md_universal}")
        # Afficher le contenu du rapport universel
        with open(output_md_universal, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("Erreur lors de l'audit :", result.error)

    await agent.shutdown()

if __name__ == "__main__":
    asyncio.run(audit_and_export_md()) 