import asyncio
import json
from pathlib import Path
import sys
from datetime import datetime
import inspect

# Ajout du répertoire parent au path pour résoudre les imports locaux
sys.path.append(str(Path(__file__).resolve().parent.parent))

from agents.agent_05_maitre_tests_validation import Agent05MaitreTestsValidation
from core.agent_factory_architecture import Task

async def main():
    """
    Fonction principale pour tester la génération de rapports d'auto-évaluation
    par l'agent 05.
    """
    print(f"🕵️ Module de la classe Task: {Task.__module__}")
    try:
        print(f"📄 Fichier de la classe Task: {inspect.getfile(Task)}")
    except TypeError:
        print("📄 Fichier de la classe Task: Impossible de déterminer (peut-être un module built-in ou C)")

    print("🤖 Démarrage du test de l'Agent 05 - Maître Tests & Validation (Auto-Évaluation)...")
    agent = Agent05MaitreTestsValidation()

    # Création du répertoire des rapports s'il n'existe pas
    reports_dir = Path(__file__).resolve().parent.parent / "reports" / "agent_05_self_assessment"
    reports_dir.mkdir(parents=True, exist_ok=True)
    print(f"📂 Les rapports seront sauvegardés dans : {reports_dir.resolve()}")

    await agent.startup()
    print("✅ Agent démarré.")

    health = await agent.health_check()
    print(f"🩺 Health Check initial: {health}")
    if not agent.templates_loaded:
        print("⚠️ Attention: Le TemplateManager n'a pas pu être chargé. Les tests peuvent être limités.")

    report_types_to_test = ['tests', 'validation', 'performance', 'qualite']
    base_context = {"source_test_script": str(Path(__file__).resolve())}

    for report_type in report_types_to_test:
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"--- Génération du rapport d'auto-évaluation type: '{report_type}' ---")

        # 1. Générer le rapport JSON
        task_json_params = {"type_rapport": report_type, "context": base_context.copy()}
        task_json = Task(type="generer_rapport_strategique", params=task_json_params)
        
        print(f"▶️ Exécution de la tâche JSON pour le rapport '{report_type}' (ID: {task_json.id})...")
        result_json = await agent.execute_task(task_json)

        if result_json.success and result_json.data:
            print(f"✔️  Succès de la génération du rapport JSON pour '{report_type}'.")
            report_json_content = result_json.data
            
            json_filename = reports_dir / f"self_assessment_A05_{report_type}_{timestamp_str}.json"
            with open(json_filename, "w", encoding="utf-8") as f:
                json.dump(report_json_content, f, indent=2, ensure_ascii=False)
            print(f"📄 Rapport JSON sauvegardé : {json_filename}")

            # 2. Générer le rapport Markdown à partir du JSON
            task_md_params = {
                "rapport_json": report_json_content, 
                "type_rapport": report_type,
                "context": base_context.copy()
            }
            task_markdown = Task(type="generer_rapport_markdown", params=task_md_params)
            
            print(f"▶️ Exécution de la tâche Markdown pour le rapport '{report_type}' (ID: {task_markdown.id})...")
            result_markdown = await agent.execute_task(task_markdown)

            if result_markdown.success and result_markdown.data:
                print(f"✔️  Succès de la génération du rapport Markdown pour '{report_type}'.")
                report_markdown_content = result_markdown.data
                
                md_filename = reports_dir / f"self_assessment_A05_{report_type}_{timestamp_str}.md"
                with open(md_filename, "w", encoding="utf-8") as f:
                    f.write(report_markdown_content)
                print(f"📄 Rapport Markdown sauvegardé : {md_filename}")
            else:
                print(f"❌ Échec de la génération du rapport Markdown pour '{report_type}'.")
                print(f"   Message d'erreur: {result_markdown.message}")
                if result_markdown.data:
                    print(f"   Données d'erreur: {result_markdown.data}")
        else:
            print(f"❌ Échec de la génération du rapport JSON pour '{report_type}'.")
            print(f"   Message d'erreur: {result_json.message}")
            if result_json.data:
                print(f"   Données d'erreur: {result_json.data}")
        print("--- Fin de la génération ---")

    print("⏳ Exécution des smoke tests internes...")
    smoke_results = agent.run_smoke_tests()
    print(f"💨 Résultats des Smoke Tests Internes :")
    current_timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(json.dumps(smoke_results, indent=2, ensure_ascii=False))
    smoke_filename = reports_dir / f"smoke_tests_A05_internal_{current_timestamp_str}.json"
    with open(smoke_filename, "w", encoding="utf-8") as f:
        json.dump(smoke_results, f, indent=2, ensure_ascii=False)
    print(f"📄 Résultats des smoke tests sauvegardés : {smoke_filename}")

    await agent.shutdown()
    print("✅ Agent arrêté.")
    print("🎉 Test de l'Agent 05 terminé.")

if __name__ == "__main__":
    asyncio.run(main()) 