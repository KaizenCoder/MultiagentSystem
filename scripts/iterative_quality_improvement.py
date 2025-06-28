import asyncio
import sys
from pathlib import Path
import logging
import json

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from agents.agent_111_auditeur_qualite import Agent111AuditeurQualite
    from agents.agent_16_peer_reviewer_senior import Agent16PeerReviewerSenior
    from agents.agent_MAINTENANCE_12_correcteur_semantique import CorrecteurSemantique
    from agents.agent_04_expert_securite_crypto import Agent04ExpertSecuriteCrypto
    from agents.agent_110_documentaliste_expert import Agent110DocumentalisteExpert
    from agents.agent_13_specialiste_documentation import Agent13SpecialisteDocumentation
    from core.models import Task, TaskResult, Status
    from tools.universal_audit_report import generate_universal_audit_md
except ImportError as e:
    log.error(f"Erreur d'importation critique. Assurez-vous que les agents sont accessibles. Erreur: {e}", exc_info=True)
    sys.exit(1)

# --- Paramètres de la Boucle d'Amélioration ---
TARGET_FILE = PROJECT_ROOT / "agents" / "agent_MAINTENANCE_12_correcteur_semantique.py"
REPORTS_DIR = PROJECT_ROOT / "reports" / "iterative_audits"
REPORTS_DIR.mkdir(exist_ok=True, parents=True)

TARGET_QUALITY_SCORE = 100
MAX_ITERATIONS = 5

async def main():
    """Script principal orchestrant la boucle d'amélioration continue."""
    log.info(f"🚀 Démarrage de la BOUCLE D'AMÉLIORATION pour: {TARGET_FILE.name}")
    log.info(f"🎯 Objectif de score de qualité: {TARGET_QUALITY_SCORE}/100")
    
    # --- Instanciation des agents ---
    agent_securite = Agent04ExpertSecuriteCrypto()
    agent_auditeur = Agent111AuditeurQualite()
    agent_examinateur = Agent16PeerReviewerSenior()
    agent_correcteur = CorrecteurSemantique(enable_auto_rename=True)
    agent_doc_expert = Agent110DocumentalisteExpert()
    agent_doc_specialiste = Agent13SpecialisteDocumentation()

    await agent_auditeur.startup()
    await agent_securite.startup()
    
    iteration_reports = []
    current_score = 0
    i = 0
    
    # --- La Boucle Itérative ---
    while current_score < TARGET_QUALITY_SCORE and i < MAX_ITERATIONS:
        i += 1
        log.info(f"\n--- 🔄 Itération {i}/{MAX_ITERATIONS} ---")
        
        target_file_path = TARGET_FILE
        
        # 1. Audit Qualité
        log.info(f"   [111] Audit de la qualité du code (itération {i})...")
        quality_report = await agent_auditeur.audit_code_quality(str(target_file_path))
        current_score = quality_report.get("quality_score", 0)
        log.info(f"   [111] Score de qualité actuel: {current_score}/{TARGET_QUALITY_SCORE}")
        
        iteration_reports.append({"iteration": i, "score": current_score, "report": quality_report})
        
        # 2. Condition de sortie
        if current_score >= TARGET_QUALITY_SCORE:
            log.info(f"🎉 Objectif de qualité atteint ! Score final: {current_score}/100.")
            break
            
        # 3. Génération du Plan de Correction Signé
        log.info("   [16] Génération et signature du plan de correction...")
        signed_plan = agent_examinateur.generate_signed_correction_plan(quality_report, agent_securite)
        
        if not signed_plan or not signed_plan.get("plan"):
            log.warning("   [016] Aucun plan de correction généré. La boucle s'arrête.")
            break
        
        log.info(f"   [16] Plan de correction signé généré avec {len(signed_plan['plan'])} action(s).")
        
        # 4. Vérification de la signature du plan (toujours critique)
        log.info("   [004] Vérification de la signature du plan...")
        if not agent_securite.verify_correction_plan(signed_plan):
            log.critical("   [004] 🚨 SIGNATURE INVALIDE ! Mission de correction avortée. 🚨")
            break
        log.info("   [004] Signature du plan valide.")

        # 5. Exécution de la correction déléguée
        plan = signed_plan.get("plan", [])
        correction_made = False
        for action in plan:
            if action.get("action") == "DELEGATE_SEMANTIC_CORRECTION":
                log.info("   [016] -> [012] Délégation de la correction sémantique...")
                
                # Lire le code à corriger
                code_to_correct = target_file_path.read_text(encoding='utf-8')

                # Créer et exécuter la tâche pour l'agent 12
                correction_task = Task(
                        type="correct_semantics",
                        params={"code": code_to_correct}
                )
                
                result = await agent_correcteur.execute_task(correction_task)

                if result.success and result.data and result.data.get("score_improvement", 0) > 0:
                    corrected_code = result.data.get("corrected_code")
                    log.info(f"   [012] Correction sémantique réussie. Amélioration du score de {result.data.get('score_improvement'):.2f} pts.")
                    
                    # Log du code corrigé pour débogage
                    log.info(f"--- CODE CORRIGÉ PAR AGENT 12 ---\n{corrected_code}\n---------------------------------")

                    # Sauvegarder le code corrigé
                    target_file_path.write_text(corrected_code, encoding='utf-8')
                    log.info(f"   [SYS] Fichier '{target_file_path}' mis à jour avec les corrections.")
                    correction_made = True
                    
                    # Stocker le rapport
                    iteration_reports[-1]["correction_details"] = result.data
                else:
                    error_msg = result.error if result.error else "Pas d'amélioration."
                    log.warning(f"   [012] La correction sémantique n'a pas apporté d'amélioration ou a échoué: {error_msg}")
                    iteration_reports[-1]["correction_details"] = {"message": "Pas d'amélioration ou échec", "error": error_msg}
            else:
                 log.warning(f"Action non reconnue dans le plan: {action.get('action')}")
        
        # Si aucune correction n'a été faite, on sort pour éviter une boucle infinie
        if not correction_made:
            log.warning("   [SYS] Aucune correction n'a été appliquée durant cette itération. Arrêt de la boucle.")
            break

    # --- Phase Finale: Documentation et Rapport ---
    log.info("\n--- 🏁 Phase Finale: Documentation et Rapport de Synthèse ---")

    final_report_path = REPORTS_DIR / f"iterative_audit_{TARGET_FILE.stem}.md"
    
    # Documentation par l'Agent 110 et 13
    tech_doc_content = (await agent_doc_expert.execute_task(Task(type="generer_doc_code", params={"path": str(TARGET_FILE.parent)}))).data.get("content", "")
    agent_doc_specialiste.create_production_guide()
    
    # Création du rapport final
    final_report_data = iteration_reports[-1]["report"]
    
    custom_sections = {
        "Résumé de la Boucle d'Amélioration": 
            f"La boucle a tourné {len(iteration_reports)} fois.\n" +
            f"Score Initial: {iteration_reports[0]['score']}/100\n" +
            f"Score Final: {current_score}/100\n" +
            ("✅ L'objectif de qualité a été atteint." if current_score >= TARGET_QUALITY_SCORE else "⚠️ L'objectif de qualité n'a pas été atteint."),
        "Problèmes Restants": "Aucun" if current_score >= TARGET_QUALITY_SCORE else json.dumps(final_report_data.get("issues"), indent=2)
    }

    extra_data_for_template = {
        "reviewer_name": "Orchestrateur de la Boucle d'Amélioration",
        "reviewer_role": "Agents 111, 16, 12",
        "agent_name": TARGET_FILE.name,
        "repo": "nextgeneration",
        "custom_sections": custom_sections
    }

    generate_universal_audit_md(final_report_data, "Itératif", str(final_report_path), extra_data_for_template)
    log.info(f"✅ Rapport de synthèse final généré : {final_report_path}")
    
    print("\n\n--- 📄 RAPPORT FINAL 📄 ---\n")
    print(final_report_path.read_text(encoding="utf-8"))
    
    await agent_auditeur.shutdown()
    await agent_securite.shutdown()

if __name__ == "__main__":
    # Sauvegarder l'état original du fichier pour la restauration
    original_content = TARGET_FILE.read_text(encoding="utf-8")
    try:
        asyncio.run(main())
    finally:
        # Restaurer le fichier original
        TARGET_FILE.write_text(original_content, encoding="utf-8")
        log.info(f"\n🔧 Fichier original restauré : {TARGET_FILE.name}")
        # Supprimer le fichier de test de l'Agent 15 s'il existe
        temp_file = Path("temp_test_file.py")
        if temp_file.exists():
            temp_file.unlink() 