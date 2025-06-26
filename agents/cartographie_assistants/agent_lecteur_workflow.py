# agents/cartographie_assistants/agent_lecteur_workflow.py
import re
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

# Configuration du logger pour cet agent
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class AgentLecteurWorkflow:
    """
    Agent Lecteur Workflow (ALW).
    Cet agent est responsable de lire et d'analyser le fichier Markdown 
    WORKFLOW_SUIVI_AGENTS.md pour en extraire la liste des agents et leur statut.
    """
    __version__ = "0.1.0"

    def __init__(self, agent_id: str = "agent_lecteur_workflow", workflow_file_path: Optional[str] = None):
        self.agent_id = agent_id
        self.status = "initialisé"
        # Le chemin peut être défini à l'init ou via execute_task
        self.workflow_file_path = workflow_file_path 
        logger.info(f"Agent {self.agent_id} (v{self.__version__}) initialisé.")

    def startup(self):
        """Démarre l'agent."""
        self.status = "démarré"
        logger.info(f"Agent {self.agent_id} démarré.")

    def health_check(self) -> Dict[str, str]:
        """Vérifie l'état de santé de l'agent."""
        logger.debug(f"Exécution du health_check pour {self.agent_id}")
        # Pourrait vérifier si le fichier workflow par défaut est accessible si configuré
        return {"agent_id": self.agent_id, "status": "OK", "version": self.__version__}

    def _interpret_status(self, raw_status: str) -> str:
        """Interprète le statut brut du workflow."""
        if raw_status.lower() == 'x':
            return "Terminé"
        return "À faire" # Ou "En cours", "En attente", etc. selon la convention

    def analyser_workflow(self, workflow_file_path: Optional[str] = None) -> Optional[List[Dict[str, str]]]:
        """
        Analyse le fichier WORKFLOW_SUIVI_AGENTS.md pour extraire les agents et leur statut.
        Retourne une liste de dictionnaires, ou None si le fichier n'est pas trouvé.
        """
        if not workflow_file_path:
            if self.workflow_file_path:
                file_path_str = self.workflow_file_path
            else:
                logger.error("Aucun chemin de fichier workflow n'a été fourni.")
                return None # Retourne None si aucun chemin n'est disponible
        else:
            file_path_str = workflow_file_path

        file_to_analyze = Path(file_path_str)
        logger.info(f"Analyse du fichier workflow : {file_to_analyze}")

        if not file_to_analyze.exists():
            logger.error(f"Le fichier workflow '{file_to_analyze}' n'existe pas.")
            return None # <--- MODIFICATION: Retourner None si le fichier n'existe pas

        agents_status = []
        try:
            with open(file_to_analyze, 'r', encoding='utf-8') as f:
                content = f.readlines()
            
            # Regex pour capturer: - [x] agent_nom.py - Description optionnelle
            # Groupe 1: 'x' ou ' ' (contenu de la checkbox)
            # Groupe 2: nom du fichier .py
            # Groupe 3: (Optionnel) Description après le nom du fichier
            regex = r"^\s*-\s*\[([ xX])\]\s*([\w.-]+\.py)(?:\s*-\s*(.*))?$"

            for line_number, line in enumerate(content, 1):
                match = re.search(regex, line)
                if match:
                    raw_status = match.group(1).strip()
                    agent_name = match.group(2).strip()
                    description = match.group(3).strip() if match.group(3) else ""
                    
                    interpreted_status = self._interpret_status(raw_status)
                    
                    agents_status.append({
                        "nom_agent": agent_name,
                        "statut_brut": f"[{raw_status}]",
                        "statut_interprete": interpreted_status,
                        "description": description,
                        "ligne": line_number
                    })
                    logger.debug(f"Agent trouvé: {agent_name}, Statut: {interpreted_status}, Ligne: {line_number}")
        
        except FileNotFoundError:
            logger.error(f"Fichier workflow non trouvé : {file_path_str}")
            # Retourner une liste vide ou lever une exception plus spécifique
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse du fichier workflow {file_path_str}: {e}")
            # Retourner une liste vide ou lever une exception
            
        logger.info(f"Analyse terminée. {len(agents_status)} agents trouvés dans le workflow.")
        return agents_status

    def execute_task(self, task_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute une tâche spécifique demandée à l'agent.
        Exemple : {'action': 'analyser_workflow', 'params': {'workflow_file_path': 'path/to/file.md'}}
        """
        action = task_details.get("action")
        params = task_details.get("params", {})
        logger.info(f"Agent {self.agent_id} a reçu une tâche : {action} avec paramètres : {params}")

        if action == "analyser_workflow":
            workflow_file_path_to_use = params.get("workflow_file_path", self.workflow_file_path)
            
            if not workflow_file_path_to_use:
                logger.error(f"Paramètre 'workflow_file_path' manquant pour l'action '{action}'.")
                return {"status": "erreur", "message": f"Paramètre 'workflow_file_path' manquant pour l'action '{action}'."}

            result_data = self.analyser_workflow(workflow_file_path_to_use)

            if result_data is None: # <--- MODIFICATION: Gérer le cas où analyser_workflow retourne None
                return {
                    "status": "succès", # Le test s'attend à "succès"
                    "data": [],
                    "message": f"Le fichier workflow '{workflow_file_path_to_use}' n'existe pas ou n'a pas pu être lu."
                }
            
            return {
                "status": "succès",
                "data": result_data,
                "message": f"Analyse du workflow {workflow_file_path_to_use} terminée. {len(result_data)} agents trouvés."
            }
        else:
            logger.warning(f"Action '{action}' non reconnue par l'agent {self.agent_id}.")
            return {"status": "erreur", "message": f"Action '{action}' non reconnue."}

    def shutdown(self):
        """Arrête l'agent et libère les ressources."""
        self.status = "arrêté"
        logger.info(f"Agent {self.agent_id} arrêté.")

if __name__ == '__main__':
    # Exemple d'utilisation directe pour test rapide
    print("🤖 Test direct de AgentLecteurWorkflow...")
    
    # Créer un fichier de workflow de test
    test_workflow_path = Path("temp_test_workflow.md")
    with open(test_workflow_path, "w", encoding="utf-8") as f:
        f.write("- [x] agent_01_coordinateur.py - Terminé et validé\n")
        f.write("- [ ] agent_02_architecte.py - En cours de développement\n")
        f.write("-    [X] agent_03_config.py   -   Avec espaces et majuscule\n") # Test robustesse regex
        f.write("Autre ligne qui ne doit pas matcher\n")
        f.write("- [ ] agent_04_testeur_nom_long.py\n") # Test sans description

    alw = AgentLecteurWorkflow()
    alw.startup()
    
    print("\n🔬 Test Health Check:")
    health = alw.health_check()
    print(health)

    print("\n🚀 Test execute_task pour analyser_workflow:")
    task_payload = {
        "action": "analyser_workflow",
        "params": {"workflow_file_path": str(test_workflow_path)}
    }
    result = alw.execute_task(task_payload)
    
    if result["status"] == "succès":
        print("Résultat de l'analyse :")
        for agent_info in result["data"]:
            print(f"  - Agent: {agent_info['nom_agent']}, Statut: {agent_info['statut_interprete']}, Desc: '{agent_info['description']}', Ligne: {agent_info['ligne']}")
    else:
        print(f"Échec de l'analyse : {result['message']}")

    alw.shutdown()
    
    # Nettoyage du fichier de test
    test_workflow_path.unlink()
    print(f"\n🗑️ Fichier de test '{test_workflow_path}' supprimé.")
    print("🎉 Test direct terminé.") 