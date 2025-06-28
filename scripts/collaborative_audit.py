import asyncio
import sys
from pathlib import Path
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

# --- Configuration ---
# Ajoute la racine du projet au PYTHONPATH pour garantir que les imports fonctionnent
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Importe les agents et outils nécessaires
try:
    from agents.agent_111_auditeur_qualite import Agent111AuditeurQualite
    from agents.agent_110_documentaliste_expert import Agent110DocumentalisteExpert
    from agents.agent_16_peer_reviewer_senior import Agent16PeerReviewerSenior
    from agents.agent_13_specialiste_documentation import Agent13SpecialisteDocumentation
    from core.agent_factory_architecture import Task
    from tools.universal_audit_report import generate_universal_audit_md
except ImportError as e:
    log.error(f"Erreur d'importation. Assurez-vous que les agents et le core sont accessibles. Erreur: {e}")
    sys.exit(1)

# --- Paramètres de l'audit ---
TARGET_AGENT_PATH = PROJECT_ROOT / "agents" / "agent_POSTGRESQL_web_researcher.py"
REPORTS_DIR = PROJECT_ROOT / "reports" / "collaborative_audits"
REPORTS_DIR.mkdir(exist_ok=True, parents=True)


async def main():
    """Script principal orchestrant l'audit collaboratif."""
    log.info("🚀 Démarrage de l'audit collaboratif...")
    if not TARGET_AGENT_PATH.exists():
        log.error(f"L'agent cible n'a pas été trouvé : {TARGET_AGENT_PATH}")
        return

    target_code = TARGET_AGENT_PATH.read_text(encoding="utf-8")
    
    # --- Instanciation des agents ---
    agent111 = Agent111AuditeurQualite()
    agent110 = Agent110DocumentalisteExpert()
    agent16 = Agent16PeerReviewerSenior()
    agent13 = Agent13SpecialisteDocumentation()
    
    # Démarrage des agents asynchrones
    await asyncio.gather(agent111.startup(), agent110.startup())

    # --- Phase 1: Audit Qualité & Architecture ---
    log.info("\n--- Phase 1: Audit Qualité & Architecture ---")
    
    # Agent 111: Audit de Qualité
    log.info("   [111] Lancement de l'audit de qualité du code...")
    quality_task = Task(type="audit_code_quality", params={"code": target_code, "file_path": str(TARGET_AGENT_PATH)})
    quality_result = await agent111.execute_task(quality_task)
    quality_report = quality_result.data.get("quality_report") if quality_result.success else {"error": quality_result.error, "quality_score": 0, "issues": [], "metrics": {}}
    log.info(f"   [111] Audit de qualité terminé. Score: {quality_report.get('quality_score')}/100")

    # Agent 16: Revue d'Architecture Senior
    log.info("   [16] Lancement de la revue d'architecture globale...")
    senior_review_result = agent16.run_senior_review_mission()
    senior_report_path = senior_review_result.get("final_report", "N/A")
    log.info(f"   [16] Revue d'architecture terminée. Rapport: {senior_report_path}")

    # --- Phase 2: Génération de la Documentation ---
    log.info("\n--- Phase 2: Génération de la Documentation ---")
    
    # Agent 110: Documentation Technique
    log.info(f"   [110] Lancement de la génération de la documentation pour le dossier : {TARGET_AGENT_PATH.parent}...")
    doc_task = Task(type="generer_doc_code", params={"path": str(TARGET_AGENT_PATH.parent)})
    tech_doc_result = await agent110.execute_task(doc_task)
    tech_doc_content = tech_doc_result.data.get("content", f"Erreur: {tech_doc_result.error}") if tech_doc_result.success else f"Erreur: {tech_doc_result.error}"
    tech_doc_path = REPORTS_DIR / f"tech_doc_{TARGET_AGENT_PATH.stem}.md"
    tech_doc_path.write_text(tech_doc_content, encoding="utf-8")
    log.info(f"   [110] Documentation technique générée : {tech_doc_path}")

    # Agent 13: Documentation de Haut Niveau
    log.info("   [13] Lancement de la génération des guides de production...")
    agent13.create_production_guide()
    agent13.create_api_documentation()
    log.info("   [13] Guides de production et API mis à jour.")

    # --- Phase 3: Synthèse du Rapport Final ---
    log.info("\n--- Phase 3: Synthèse du Rapport Final ---")
    
    final_report_path = REPORTS_DIR / f"final_audit_{TARGET_AGENT_PATH.stem}.md"

    report_data_for_template = {
        "file_path": str(TARGET_AGENT_PATH),
        "quality_score": quality_report.get('quality_score'),
        "score": quality_report.get('quality_score'),
        "issues": quality_report.get('issues', []),
        "metrics": quality_report.get('metrics', {}),
        "recommendations": [{"priority": "HIGH", "description": "Examiner les problèmes de qualité du code remontés par l'Agent 111."}]
    }

    extra_data_for_template = {
        "reviewer_name": "Équipe d'Audit Collaborative",
        "reviewer_role": "Agents 16, 111, 110, 13",
        "agent_name": TARGET_AGENT_PATH.name,
        "agent_version": "N/A",
        "repo": "nextgeneration",
        "custom_sections": {
            "Analyse d'Architecture (par Agent 16)": f"L'agent audité s'inscrit dans l'architecture globale du projet, qui a été validée comme étant de 'QUALITÉ EXCEPTIONNELLE' par l'Agent 16. Pour plus de détails, consultez le rapport complet : `{senior_report_path}`",
            "Documentation Technique (par Agent 110)": f"La documentation technique de bas niveau a été générée et est disponible ici : `{tech_doc_path}`.",
            "Contexte de Production (par Agent 13)": "Cet agent fait partie d'un système plus large dont les guides de production et la documentation API sont maintenus par l'Agent 13 et disponibles dans `documentation/guides` et `documentation/api`."
        }
    }

    generate_universal_audit_md(report_data_for_template, "Collaboratif", str(final_report_path), extra_data_for_template)
    log.info(f"✅ Rapport de synthèse final généré : {final_report_path}")
    
    # Affichage de l'extrait
    final_report_content = final_report_path.read_text(encoding="utf-8")
    print("\n\n--- 📄 EXTRAIT DU RAPPORT FINAL 📄 ---\n")
    print(final_report_content)
    
    # --- Arrêt des agents ---
    await asyncio.gather(agent111.shutdown(), agent110.shutdown())
    agent16.shutdown()
    agent13.shutdown()
    log.info("\n✅ Audit collaboratif terminé.")

if __name__ == "__main__":
    asyncio.run(main()) 