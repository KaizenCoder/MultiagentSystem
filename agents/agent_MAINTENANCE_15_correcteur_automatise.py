import sys
import re
import logging
from pathlib import Path
from typing import Dict, Any, List

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from agents.agent_04_expert_securite_crypto import Agent04ExpertSecuriteCrypto, SecurityException
except ImportError:
    Agent04ExpertSecuriteCrypto = None
    SecurityException = Exception

# ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
try:
    from core.manager import LoggingManager
    # Configuration logging unifié pour agent MAINTENANCE
    logging_manager = LoggingManager()
    log = logging_manager.get_logger(
        config_name="maintenance",
        custom_config={
            "logger_name": "nextgen.maintenance.correcteur_automatise",
            "log_dir": "logs/maintenance/correcteur",
            "metadata": {
                "agent_type": "MAINTENANCE_15_correcteur_automatise",
                "agent_role": "correcteur_automatise",
                "system": "nextgeneration"
            }
        }
    )
except ImportError:
    # Fallback en cas d'indisponibilité du LoggingManager
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log = logging.getLogger(__name__)

class AgentMAINTENANCE15CorrecteurAutomatise:
    """
    Agent spécialisé dans l'application de corrections automatiques sur le code.
    Prend un plan d'action structuré et tente de modifier les fichiers en conséquence.
    """
    def __init__(self, security_agent: 'Agent04ExpertSecuriteCrypto'):
        self.name = "Agent 15 - Correcteur Automatisé"
        if not security_agent:
            raise ValueError("Un agent de sécurité est requis pour l'initialisation.")
        self.security_agent = security_agent
        log.info(f"🤖 {self.name} initialisé avec une dépendance de sécurité.")

    def run_correction_mission(self, signed_correction_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute un plan de correction signé après vérification de sa signature.
        """
        log.info("🎯 Réception d'un plan de correction pour exécution...")
        
        # 1. Vérification de la signature
        try:
            is_valid = self.security_agent.verify_correction_plan(signed_correction_plan)
            if not is_valid:
                raise SecurityException("ÉCHEC DE LA VÉRIFICATION DE SIGNATURE. Le plan est invalide ou corrompu. Opération avortée.")
        except SecurityException as e:
            log.error(f"[ALERTE SÉCURITÉ] {e}")
            return {"status": "aborted", "error": str(e)}

        log.info("✅ Signature du plan vérifiée. Début des corrections.")
        
        correction_plan = signed_correction_plan.get("plan", [])
        report = {
            "total_actions": len(correction_plan),
            "successful_corrections": 0,
            "failed_corrections": 0,
            "details": []
        }

        for action in correction_plan:
            action_type = action.get("action")
            file_path_str = action.get("file_path")
            
            if not action_type or not file_path_str:
                report["details"].append({"action": action, "status": "failed", "error": "Action ou chemin de fichier manquant."})
                report["failed_corrections"] += 1
                continue

            file_path = Path(file_path_str)
            if not file_path.exists():
                report["details"].append({"action": action, "status": "failed", "error": f"Fichier non trouvé: {file_path}"})
                report["failed_corrections"] += 1
                continue

            success = False
            error_message = ""
            try:
                if action_type == "add_docstring":
                    success = self._add_docstring_to_function(file_path, action.get("target_function"))
                else:
                    error_message = f"Type d'action non supporté: {action_type}"

            except Exception as e:
                success = False
                error_message = str(e)
                log.error(f"Erreur lors de l'action '{action_type}' sur {file_path}: {e}", exc_info=True)

            if success:
                report["successful_corrections"] += 1
                report["details"].append({"action": action, "status": "success"})
            else:
                report["failed_corrections"] += 1
                report["details"].append({"action": action, "status": "failed", "error": error_message})

        log.info(f"✅ Mission de correction terminée. Succès: {report['successful_corrections']}, Échecs: {report['failed_corrections']}.")
        return report

    def _add_docstring_to_function(self, file_path: Path, function_name: str) -> bool:
        """
        Ajoute un docstring placeholder à une fonction spécifique dans un fichier.
        """
        if not function_name:
            return False
            
        content = file_path.read_text(encoding="utf-8")
        lines = content.splitlines()

        # Regex pour trouver la définition de la fonction
        func_regex = re.compile(r"^[ \t]*def\s+" + re.escape(function_name) + r"\s*\(.*?\):")
        
        target_line_index = -1
        for i, line in enumerate(lines):
            if func_regex.match(line):
                target_line_index = i
                break
        
        if target_line_index == -1:
            log.error(f"Fonction '{function_name}' non trouvée dans {file_path}.")
            return False

        # Vérifier si un docstring existe déjà
        if len(lines) > target_line_index + 1 and (lines[target_line_index + 1].strip().startswith('"""') or lines[target_line_index + 1].strip().startswith("'''")):
            log.warning(f"La fonction '{function_name}' a déjà un docstring. Correction ignorée.")
            return True # Considéré comme un succès car l'état désiré est atteint

        # Insérer le docstring
        indentation = re.match(r"^[ \t]*", lines[target_line_index + 1]).group(0) if len(lines) > target_line_index + 1 else "    "
        placeholder_docstring = f'{indentation}"""TODO: Documenter cette fonction."""'
        lines.insert(target_line_index + 1, placeholder_docstring)
        
        file_path.write_text("\n".join(lines), encoding="utf-8")
        log.info(f"Docstring ajouté à la fonction '{function_name}' dans {file_path}.")
        
        return True

def main():
    """Point d'entrée pour un test simple."""
    log.info("--- Test de l'Agent 15 Correcteur ---")
    
    # Créer un fichier de test
    test_file_path = Path("temp_test_file.py")
    test_file_content = """
def function_with_docstring():
    '''This is a docstring.'''
    pass

def function_without_docstring(a, b):
    return a + b
"""
    test_file_path.write_text(test_file_content, encoding="utf-8")

    # Définir un plan de correction
    plan = [
        {
            "action": "add_docstring",
            "file_path": str(test_file_path),
            "target_function": "function_without_docstring"
        },
        {
            "action": "add_docstring",
            "file_path": str(test_file_path),
            "target_function": "function_with_docstring" # Devrait être ignoré
        }
    ]

    # Dépendance de sécurité
    secu_agent = Agent04ExpertSecuriteCrypto()
    # Dans un vrai scénario, il faudrait gérer le startup asynchrone
    import asyncio
    asyncio.run(secu_agent.startup())

    # Signer le plan
    signed_plan = secu_agent.sign_correction_plan(plan)
    print("\n--- Plan signé ---")
    print(json.dumps(signed_plan, indent=2))

    agent = AgentMAINTENANCE15CorrecteurAutomatise(security_agent=secu_agent)
    result = agent.run_correction_mission(signed_plan)

    print("\n--- Rapport de Correction ---")
    print(json.dumps(result, indent=2))
    
    print("\n--- Contenu du Fichier Modifié ---")
    print(test_file_path.read_text(encoding="utf-8"))

    # Nettoyage
    test_file_path.unlink()

if __name__ == "__main__":
    main() 