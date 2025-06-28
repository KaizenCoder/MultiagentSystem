# agents/cartographie_assistants/agent_comparateur_synchroniseur.py
import logging
from typing import Dict, Any, List, Optional
import difflib

# Configuration du logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AgentComparateurSynchroniseur:
    """
    Agent responsable de comparer les informations extraites du code Python (par AACP)
    et de la documentation Markdown (par AADM) pour un agent donné.
    Il identifie les écarts et peut proposer des actions de synchronisation.
    """
    __version__ = "0.1.0"

    def __init__(self, analyseur_code_agent, analyseur_doc_agent):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"Initialisation de {self.__class__.__name__} version {self.__version__}")
        self.analyseur_code = analyseur_code_agent # Instance de AgentAnalyseurCodePython
        self.analyseur_doc = analyseur_doc_agent   # Instance de AgentAnalyseurDocumentationMarkdown
        if not (hasattr(self.analyseur_code, 'execute_task') and callable(self.analyseur_code.execute_task)):
            raise ValueError("analyseur_code_agent doit avoir une méthode execute_task")
        if not (hasattr(self.analyseur_doc, 'execute_task') and callable(self.analyseur_doc.execute_task)):
            raise ValueError("analyseur_doc_agent doit avoir une méthode execute_task")

    def get_capabilities(self) -> Dict[str, Any]:
        """Retourne les capacités de l'agent."""
        return {
            "name": self.__class__.__name__,
            "version": self.__version__,
            "description": "Compare les analyses de code et de documentation pour identifier les écarts et suggérer des synchronisations.",
            "tasks": [
                {"name": "comparer_code_et_doc", "description": "Compare les données extraites du code et de la documentation d'un agent."
                },
                {"name": "generer_rapport_ecarts", "description": "Génère un rapport sur les écarts constatés entre code et documentation."}
            ]
        }

    def comparer_code_et_doc(self, chemin_fichier_python: str, chemin_fichier_markdown: str) -> Dict[str, Any]:
        """
        Compare les informations extraites du code et de la documentation.

        Args:
            chemin_fichier_python: Chemin vers le fichier Python de l'agent.
            chemin_fichier_markdown: Chemin vers le fichier Markdown de documentation de l'agent.

        Returns:
            Un dictionnaire contenant les données du code, les données de la doc, et une section d'écarts.
        """
        self.logger.info(f"Comparaison entre {chemin_fichier_python} et {chemin_fichier_markdown}")

        donnees_code_response = self.analyseur_code.execute_task(
            "analyser_fichier_python", 
            {"chemin_fichier": chemin_fichier_python}
        )
        donnees_doc_response = self.analyseur_doc.execute_task(
            "analyser_fichier_markdown", 
            {"chemin_fichier": chemin_fichier_markdown}
        )

        donnees_code = None
        if donnees_code_response.get("status") == "succes":
            donnees_code = donnees_code_response.get("resultat")
        else:
            self.logger.error(f"Erreur d'analyse code pour {chemin_fichier_python}: {donnees_code_response.get('message')}")
            # Retourner une erreur ou un résultat partiel peut être une option

        donnees_doc = None
        if donnees_doc_response.get("status") == "succes":
            donnees_doc = donnees_doc_response.get("resultat")
        else:
            self.logger.error(f"Erreur d'analyse doc pour {chemin_fichier_markdown}: {donnees_doc_response.get('message')}")

        if not donnees_code or not donnees_doc:
             return {
                "status": "erreur",
                "message": "Échec de l'analyse d'un ou des deux fichiers. Comparaison impossible.",
                "details_code": donnees_code_response,
                "details_doc": donnees_doc_response
            }

        ecarts = []

        # 1. Comparaison de version
        version_code = donnees_code.get("version_agent")
        version_doc = donnees_doc.get("version_documentee")
        if version_code != version_doc:
            ecarts.append({
                "type": "Version",
                "code": version_code,
                "doc": version_doc,
                "message": f"Différence de version détectée. Code: {version_code}, Doc: {version_doc}"
            })
        else:
            ecarts.append({"type": "Version", "code": version_code, "doc": version_doc, "message": "Versions synchronisées."}) 

        # 2. Comparaison des capacités/fonctions (simplifié)
        # On pourrait comparer les noms des fonctions/méthodes vs les sections de la doc
        # Pour l'instant, on fait une comparaison simple de présence
        fonctions_code = [f["nom"] for f in donnees_code.get("fonctions", [])]
        methodes_code = []
        for classe in donnees_code.get("classes", []):
            methodes_code.extend([m["nom"] for m in classe.get("methodes", [])])
        
        # Supposons que la doc liste les capacités dans une section "Fonctionnalités Clés" ou similaire
        capacites_doc_str = ""
        for section in donnees_doc.get("sections", []):
            if "capacit" in section.get("titre", "").lower() or \
               "fonctionnalit" in section.get("titre", "").lower():
                capacites_doc_str += section.get("contenu", "") + "\n"
        
        # Simple vérification de présence pour l'exemple
        # Une analyse plus poussée nécessiterait de parser la sémantique de la doc

        # 3. Comparaison des docstrings (très simplifié)
        # Comparer le docstring du module
        docstring_module_code = donnees_code.get("docstring_module", "").strip()
        # Supposons que la description générale est au début de la doc, ou dans une section "Description Générale"
        description_generale_doc = ""
        if donnees_doc.get("sections") and donnees_doc["sections"][0]["level"] == 1:
            description_generale_doc = donnees_doc["sections"][0].get("contenu","").strip() # Premier contenu H1
        else:
            for section in donnees_doc.get("sections", []):
                if "description g" in section.get("titre","").lower(): # Casse insensible
                     description_generale_doc = section.get("contenu","").strip()
                     break
        
        if not description_generale_doc and docstring_module_code: # Fallback: titre principal si pas de H1
             if donnees_doc.get("titre_principal") and not donnees_doc.get("sections"):
                 # Ceci n'est pas idéal, il faudrait une structure de doc plus prévisible
                 pass

        # Utilisation de difflib pour une comparaison textuelle simple
        diff = list(difflib.unified_diff(
            docstring_module_code.splitlines(),
            description_generale_doc.splitlines(),
            fromfile='docstring_code', 
            tofile='description_doc',
            lineterm=''
        ))
        if diff:
            ecarts.append({
                "type": "Docstring Module vs Description Doc",
                "message": "Différences trouvées entre le docstring du module Python et la description générale dans la documentation.",
                "diff": "\n".join(diff)
            })
        else:
            if docstring_module_code or description_generale_doc: # Si au moins un a du contenu
                 ecarts.append({"type": "Docstring Module vs Description Doc", "message": "Semble synchronisé ou similaire."})
            
        return {
            "status": "succes",
            "donnees_code": donnees_code,
            "donnees_doc": donnees_doc,
            "ecarts": ecarts
        }

    def generer_rapport_ecarts(self, resultat_comparaison: Dict[str, Any], format_rapport: str = "markdown") -> Optional[str]:
        """
        Génère un rapport formaté (Markdown par défaut) des écarts trouvés.
        """
        if resultat_comparaison.get("status") != "succes" or not resultat_comparaison.get("ecarts"):
            self.logger.warning("Aucun écart à rapporter ou comparaison échouée.")
            return "Aucun écart significatif trouvé ou la comparaison a échoué."
        
        ecarts = resultat_comparaison["ecarts"]
        chemin_code = resultat_comparaison.get("donnees_code", {}).get("chemin_fichier", "N/A")
        chemin_doc = resultat_comparaison.get("donnees_doc", {}).get("chemin_fichier", "N/A")

        if format_rapport == "markdown":
            rapport_md = f"# Rapport d'Écarts : Code vs Documentation\n\n"
            rapport_md += f"**Fichier Code Python :** `{chemin_code}`\n"
            rapport_md += f"**Fichier Documentation :** `{chemin_doc}`\n\n"
            rapport_md += f"## Détail des Écarts ({len(ecarts)}):\n\n"

            for idx, ecart in enumerate(ecarts):
                rapport_md += f"### Écart {idx+1}: {ecart.get('type')}\n"
                rapport_md += f"- **Message :** {ecart.get('message', 'N/A')}\n"
                if ecart.get('code') is not None:
                    rapport_md += f"- **Valeur Code :** `{ecart.get('code')}`\n"
                if ecart.get('doc') is not None:
                    rapport_md += f"- **Valeur Doc :** `{ecart.get('doc')}`\n"
                if ecart.get('diff'):
                    rapport_md += f"- **Différences Détaillées :**\n```diff\n{ecart.get('diff')}\n```\n"
                rapport_md += "\n"
            return rapport_md
        else:
            self.logger.error(f"Format de rapport non supporté : {format_rapport}")
            return None # Ou retourner un JSON des écarts

    def execute_task(self, task_name: str, task_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute une tâche spécifique.
        """
        self.logger.info(f"Exécution de la tâche ACS '{task_name}' avec les paramètres : {task_params}")
        if task_name == "comparer_code_et_doc":
            chemin_py = task_params.get("chemin_fichier_python")
            chemin_md = task_params.get("chemin_fichier_markdown")
            if not chemin_py or not chemin_md:
                return {"status": "erreur", "message": "Les paramètres 'chemin_fichier_python' et/ou 'chemin_fichier_markdown' sont manquants."}
            return self.comparer_code_et_doc(chemin_py, chemin_md)
        
        elif task_name == "generer_rapport_ecarts":
            resultat_comp = task_params.get("resultat_comparaison")
            if not resultat_comp:
                return {"status": "erreur", "message": "Le paramètre 'resultat_comparaison' est manquant."}
            format_rapport = task_params.get("format_rapport", "markdown")
            rapport = self.generer_rapport_ecarts(resultat_comp, format_rapport)
            if rapport:
                return {"status": "succes", "rapport": rapport, "format": format_rapport}
            else:
                return {"status": "erreur", "message": f"Échec de la génération du rapport au format {format_rapport}."}
            
        else:
            self.logger.warning(f"Tâche inconnue : {task_name}")
            return {"status": "erreur", "message": f"Tâche inconnue : {task_name}"}


if __name__ == '__main__':
    import json
    from pathlib import Path
    # Pour des tests, il faudrait instancier AACP et AADM ici
    # Cela nécessiterait d'importer ces classes, ce qui créerait une dépendance circulaire
    # si ce fichier est dans le même répertoire. 
    # Une meilleure approche pour les tests d'intégration serait un script de test dédié.
    
    # Création de Mocks pour AACP et AADM pour l'exemple
    class MockAnalyseurCode:
        def execute_task(self, task_name, params):
            if task_name == "analyser_fichier_python":
                return {"status": "succes", "resultat": {
                    "chemin_fichier": params["chemin_fichier"],
                    "version_agent": "1.2.3",
                    "docstring_module": "Ceci est le docstring du code.",
                    "fonctions": [{"nom": "main"}, {"nom": "helper"}]
                }}
            return {"status": "erreur", "message": "MockAnalyseurCode: Tâche inconnue"}

    class MockAnalyseurDoc:
        def execute_task(self, task_name, params):
            if task_name == "analyser_fichier_markdown":
                return {"status": "succes", "resultat": {
                    "chemin_fichier": params["chemin_fichier"],
                    "version_documentee": "1.2.4", # Différence intentionnelle
                    "sections": [
                        {"level": 1, "titre": "Description Générale", "contenu": "Ceci est la description dans la doc."} 
                    ]
                }}
            return {"status": "erreur", "message": "MockAnalyseurDoc: Tâche inconnue"}

    mock_aacp = MockAnalyseurCode()
    mock_aadm = MockAnalyseurDoc()

    comparateur = AgentComparateurSynchroniseur(analyseur_code_agent=mock_aacp, analyseur_doc_agent=mock_aadm)

    print("\n--- Capacités de l'agent ACS ---")
    print(json.dumps(comparateur.get_capabilities(), indent=2))

    # Simuler des chemins de fichiers pour le test
    dummy_py_path = "dummy_agent.py"
    dummy_md_path = "dummy_agent.md"

    print(f"\n--- Comparaison pour {dummy_py_path} et {dummy_md_path} (avec Mocks) ---")
    resultat_comp = comparateur.execute_task(
        "comparer_code_et_doc",
        {"chemin_fichier_python": dummy_py_path, "chemin_fichier_markdown": dummy_md_path}
    )
    print("Résultat brut de comparaison:")
    print(json.dumps(resultat_comp, indent=2, ensure_ascii=False))

    if resultat_comp.get("status") == "succes":
        print("\n--- Génération du rapport d'écarts (Markdown) ---")
        rapport_gen_result = comparateur.execute_task("generer_rapport_ecarts", {"resultat_comparaison": resultat_comp})
        if rapport_gen_result.get("status") == "succes":
            print(rapport_gen_result.get("rapport"))
        else:
            print(f"Échec génération rapport: {rapport_gen_result.get('message')}")
    else:
        print(f"\nComparaison échouée: {resultat_comp.get('message')}") 