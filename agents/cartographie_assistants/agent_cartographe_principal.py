# agents/cartographie_assistants/agent_cartographe_principal.py
import logging
import json
from typing import Dict, Any, List, Optional
from pathlib import Path

# Importer les classes des agents assistants
# Pour éviter les dépendances circulaires à l'exécution directe de ce fichier,
# on utilisera des placeholders ou des injections de dépendances réelles lors de l'instanciation.
# from .agent_lecteur_workflow import AgentLecteurWorkflow
# from .agent_analyseur_code_python import AgentAnalyseurCodePython
# from .agent_analyseur_documentation_markdown import AgentAnalyseurDocumentationMarkdown
# from .agent_comparateur_synchroniseur import AgentComparateurSynchroniseur

# Configuration du logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AgentCartographePrincipal:
    """
    Agent orchestrateur principal pour la mission de cartographie.
    Il utilise les agents assistants (ALW, AACP, AADM, ACS) pour analyser
    le workflow, le code et la documentation des agents, comparer les informations,
    et générer un rapport de cartographie des écarts.
    """
    __version__ = "0.1.0"

    def __init__(self, lecteur_workflow, analyseur_code, analyseur_doc, comparateur_sync):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"Initialisation de {self.__class__.__name__} version {self.__version__}")
        self.lecteur_workflow = lecteur_workflow
        self.analyseur_code = analyseur_code
        self.analyseur_doc = analyseur_doc
        self.comparateur_sync = comparateur_sync

        # Valider que les assistants ont la méthode execute_task
        for assistant_name, assistant_obj in self.get_assistants().items():
            if not (hasattr(assistant_obj, 'execute_task') and callable(assistant_obj.execute_task)):
                raise ValueError(f"L'assistant {assistant_name} doit avoir une méthode execute_task callable.")

    def get_assistants(self) -> Dict[str, Any]:
        """Retourne un dictionnaire des agents assistants."""
        return {
            "lecteur_workflow": self.lecteur_workflow,
            "analyseur_code": self.analyseur_code,
            "analyseur_doc": self.analyseur_doc,
            "comparateur_sync": self.comparateur_sync
        }

    def get_capabilities(self) -> Dict[str, Any]:
        """Retourne les capacités de l'agent cartographe principal."""
        return {
            "name": self.__class__.__name__,
            "version": self.__version__,
            "description": "Orchestre la cartographie des agents en utilisant les assistants ALW, AACP, AADM, ACS pour analyser et comparer code et documentation.",
            "tasks": [
                {"name": "cartographier_tous_les_agents", "description": "Exécute le processus complet de cartographie pour tous les agents définis dans le workflow."},
                {"name": "cartographier_agent_specifique", "description": "Exécute le processus de cartographie pour un agent spécifique (code et doc)."},
                {"name": "mettre_a_jour_suivi_migration", "description": "Met à jour la section cartographie de SUIVI_MIGRATION_AGENTS.md (simulation pour l'instant)."}
            ]
        }

    def _obtenir_liste_agents_du_workflow(self, chemin_workflow_file: str) -> Optional[List[Dict[str, str]]]:
        """
        Utilise ALW pour obtenir la liste des agents à partir du fichier WORKFLOW_SUIVI_AGENTS.md.
        """
        self.logger.info(f"Lecture du workflow via ALW depuis {chemin_workflow_file}")
        alw_response = self.lecteur_workflow.execute_task(
            "analyser_workflow",
            {"chemin_fichier_workflow": chemin_workflow_file}
        )
        if alw_response.get("status") == "succes" and alw_response.get("resultat"):
            # Supposons que resultat contient une clé "agents" avec la liste
            # La structure exacte dépendra de l'implémentation de l'ALW
            agents_data = alw_response.get("resultat", {}).get("agents", [])
            if not agents_data:
                 self.logger.warning("ALW n'a retourné aucun agent depuis le workflow.")
                 return []
            self.logger.info(f"{len(agents_data)} agents trouvés dans le workflow.")
            return agents_data
        else:
            self.logger.error(f"Échec de la lecture du workflow par ALW: {alw_response.get('message')}")
            return None

    def cartographier_agent_specifique(self, chemin_script_agent: str, chemin_doc_agent: str) -> Optional[Dict[str, Any]]:
        """
        Orchestre l'analyse et la comparaison pour un seul agent.
        """
        self.logger.info(f"Début cartographie pour agent: {chemin_script_agent}, doc: {chemin_doc_agent}")

        # Appel à ACS qui lui-même appellera AACP et AADM
        acs_response = self.comparateur_sync.execute_task(
            "comparer_code_et_doc",
            {
                "chemin_fichier_python": chemin_script_agent,
                "chemin_fichier_markdown": chemin_doc_agent
            }
        )

        if acs_response.get("status") == "succes":
            self.logger.info(f"Comparaison ACS réussie pour {chemin_script_agent}.")
            rapport_ecarts_response = self.comparateur_sync.execute_task(
                "generer_rapport_ecarts",
                {"resultat_comparaison": acs_response} # ACS attend le résultat complet de la comparaison
            )
            if rapport_ecarts_response.get("status") == "succes":
                return {
                    "script_agent": chemin_script_agent,
                    "doc_agent": chemin_doc_agent,
                    "donnees_code": acs_response.get("donnees_code"),
                    "donnees_doc": acs_response.get("donnees_doc"),
                    "ecarts": acs_response.get("ecarts"),
                    "rapport_ecarts_md": rapport_ecarts_response.get("rapport")
                }
            else:
                self.logger.error(f"Échec génération rapport ACS pour {chemin_script_agent}: {rapport_ecarts_response.get('message')}")
                # Retourner quand même les données de comparaison si disponibles
                return {
                     "script_agent": chemin_script_agent,
                    "doc_agent": chemin_doc_agent,
                    "donnees_code": acs_response.get("donnees_code"),
                    "donnees_doc": acs_response.get("donnees_doc"),
                    "ecarts": acs_response.get("ecarts"),
                    "rapport_ecarts_md": None,
                    "erreur_rapport": rapport_ecarts_response.get('message')
                }
        else:
            self.logger.error(f"Échec de la comparaison ACS pour {chemin_script_agent}: {acs_response.get('message')}")
            return None

    def cartographier_tous_les_agents(self, chemin_workflow_file: str, base_path_agents: str, base_path_docs: str) -> List[Dict[str, Any]]:
        """
        Orchestre la cartographie pour tous les agents listés dans le fichier workflow.
        
        Args:
            chemin_workflow_file: Chemin vers WORKFLOW_SUIVI_AGENTS.md
            base_path_agents: Chemin de base du répertoire des scripts agents (ex: "agents/")
            base_path_docs: Chemin de base du répertoire de la documentation des agents (ex: "docs/3_Agents_et_Modeles_IA/agents/")
        """
        self.logger.info("Début de la cartographie de tous les agents.")
        liste_agents_workflow = self._obtenir_liste_agents_du_workflow(chemin_workflow_file)
        resultats_cartographie = []

        if liste_agents_workflow is None:
            self.logger.error("Impossible d'obtenir la liste des agents depuis le workflow. Cartographie annulée.")
            return []
        
        if not liste_agents_workflow:
            self.logger.warning("Aucun agent trouvé dans le workflow. La cartographie n'a rien à traiter.")
            return []

        for agent_info_wf in liste_agents_workflow:
            # La structure de agent_info_wf dépend de la sortie de l'ALW.
            # On suppose qu'elle contient au moins 'script_relatif' et 'doc_md_relative'
            nom_script_agent = agent_info_wf.get("script_python") # Nom du script, ex: agent_01_coordinateur_principal.py
            nom_doc_agent = agent_info_wf.get("doc_md")       # Nom du doc, ex: agent_01_coordinateur_principal.md
            
            if not nom_script_agent:
                self.logger.warning(f"Information de script manquante pour un agent du workflow : {agent_info_wf.get('nom_agent_workflow', 'Nom Inconnu')}. Agent ignoré.")
                continue

            # Construire les chemins complets relatifs au workspace
            # S'assurer que base_path_agents et nom_script_agent se joignent correctement
            # Path gère bien les slashes, mais il faut être prudent avec les chemins initiaux.
            # Exemple: Si base_path_agents = "agents" et nom_script_agent = "agent_X.py" -> "agents/agent_X.py"
            # Si nom_script_agent peut déjà contenir "agents/", il faut normaliser.
            # Pour cet exemple, on assume des noms de fichiers simples.

            chemin_script_complet = str(Path(base_path_agents) / nom_script_agent)
            
            # Pour la doc, c'est un peu plus complexe si ALW ne donne pas le chemin relatif complet depuis la racine du projet.
            # Si nom_doc_agent est juste le nom du fichier, et qu'il est toujours dans le même sous-dossier:
            chemin_doc_complet = None
            if nom_doc_agent:
                chemin_doc_complet = str(Path(base_path_docs) / nom_doc_agent)
            else:
                 # Essayer de déduire le nom du doc depuis le nom du script
                nom_script_sans_ext = Path(nom_script_agent).stem
                chemin_doc_complet = str(Path(base_path_docs) / f"{nom_script_sans_ext}.md")
                self.logger.info(f"Nom de doc non fourni pour {nom_script_agent}, déduction: {chemin_doc_complet}")

            self.logger.info(f"Traitement de l'agent : {chemin_script_complet} avec doc {chemin_doc_complet}")
            
            # Vérifier l'existence des fichiers avant de lancer l'analyse complète
            if not Path(chemin_script_complet).exists():
                self.logger.error(f"Fichier script introuvable: {chemin_script_complet}. Agent ignoré.")
                resultats_cartographie.append({
                    "script_agent": chemin_script_complet,
                    "doc_agent": chemin_doc_complet,
                    "erreur": f"Fichier script introuvable: {chemin_script_complet}"
                })
                continue
            if not Path(chemin_doc_complet).exists():
                self.logger.warning(f"Fichier documentation introuvable: {chemin_doc_complet}. L'analyse de la doc échouera ou sera vide.")
                # On continue quand même pour avoir l'analyse du code

            resultat_agent = self.cartographier_agent_specifique(chemin_script_complet, chemin_doc_complet)
            if resultat_agent:
                resultats_cartographie.append(resultat_agent)
            else:
                # En cas d'échec majeur de cartographier_agent_specifique
                resultats_cartographie.append({
                    "script_agent": chemin_script_complet,
                    "doc_agent": chemin_doc_complet,
                    "erreur": "Échec de la cartographie spécifique pour cet agent."
                })
        
        self.logger.info(f"Cartographie terminée pour {len(resultats_cartographie)} agents.")
        return resultats_cartographie

    def mettre_a_jour_suivi_migration(self, resultats_cartographie: List[Dict[str, Any]], chemin_fichier_suivi: str) -> bool:
        """
        Met à jour (simulé pour l'instant) la section 3 de SUIVI_MIGRATION_AGENTS.md
        avec les informations de PF Conf. et Fonc. Manquantes.
        """
        self.logger.info(f"Simulation de la mise à jour du fichier de suivi : {chemin_fichier_suivi}")
        if not resultats_cartographie:
            self.logger.warning("Aucun résultat de cartographie à écrire dans le suivi.")
            return False

        # Logique de mise à jour du fichier Markdown (complexe et dépend du format exact)
        # Pour l'instant, on affiche juste ce qu'on écrirait
        print("\n--- DEBUT SIMULATION MISE A JOUR SUIVI_MIGRATION_AGENTS.md ---")
        for res_agent in resultats_cartographie:
            script = res_agent.get("script_agent", "Script inconnu")
            ecarts = res_agent.get("ecarts", [])
            pf_conf_msg = "À vérifier"
            fonc_manquantes_msg = "À déterminer"

            if res_agent.get('erreur'):
                pf_conf_msg = f"Erreur: {res_agent.get('erreur')}"
                fonc_manquantes_msg = f"Erreur: {res_agent.get('erreur')}"
            elif ecarts:
                version_ecart = next((e for e in ecarts if e.get("type") == "Version"), None)
                docstring_ecart = next((e for e in ecarts if e.get("type") == "Docstring Module vs Description Doc"), None)
                
                # Exemple simple pour PF Conf. basé sur la version
                if version_ecart:
                    if version_ecart.get("code") and version_ecart.get("doc"):
                        pf_conf_msg = "Oui" if version_ecart["code"] == version_ecart["doc"] else "Non (Version)"
                    elif version_ecart.get("code"):
                        pf_conf_msg = "Partiel (Code seulement)"
                    elif version_ecart.get("doc"):
                        pf_conf_msg = "Partiel (Doc seulement)"
                
                # Exemple pour Fonc. Manquantes
                if docstring_ecart and docstring_ecart.get("diff"):
                    fonc_manquantes_msg = "Écart Docstring/Description"
                elif docstring_ecart and "synchronisé" not in docstring_ecart.get("message","").lower():
                     fonc_manquantes_msg = docstring_ecart.get("message", "Écart Docstring/Description")
                else:
                    fonc_manquantes_msg = "Aucun écart majeur de docstring détecté (basique)"
            else:
                pf_conf_msg = "Oui (Supposé, aucun écart de version)"
                fonc_manquantes_msg = "Aucun écart de docstring détecté (basique)"


            print(f"Agent: {script}")
            print(f"  PF Conf. (déduit): {pf_conf_msg}")
            print(f"  Fonc. Manquantes / Écarts Doc (déduit): {fonc_manquantes_msg}")
            # Ici, on lirait le fichier SUIVI_MIGRATION_AGENTS.md,
            # trouverait la ligne correspondant à `script` dans la table,
            # et mettrait à jour les colonnes "PF Conf." et "Fonc. Manquantes".
            # Cela nécessite un parsing Markdown robuste.
        print("--- FIN SIMULATION MISE A JOUR ---")
        self.logger.info("La mise à jour réelle du fichier Markdown n'est pas implémentée dans cette version.")
        return True # Simule le succès

    def execute_task(self, task_name: str, task_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute une tâche spécifique de l'ACP.
        """
        self.logger.info(f"Exécution de la tâche ACP '{task_name}' avec les paramètres : {task_params}")
        if task_name == "cartographier_agent_specifique":
            chemin_py = task_params.get("chemin_script_agent")
            chemin_md = task_params.get("chemin_doc_agent")
            if not chemin_py or not chemin_md:
                return {"status": "erreur", "message": "Paramètres de chemin manquants pour cartographier_agent_specifique."}
            resultat = self.cartographier_agent_specifique(chemin_py, chemin_md)
            if resultat:
                return {"status": "succes", "resultat_cartographie_agent": resultat}
            else:
                return {"status": "erreur", "message": f"Échec de la cartographie pour {chemin_py}."}

        elif task_name == "cartographier_tous_les_agents":
            chemin_wf = task_params.get("chemin_workflow_file")
            base_agents = task_params.get("base_path_agents", "agents") # Default
            base_docs = task_params.get("base_path_docs", "docs/3_Agents_et_Modeles_IA/agents") #Default
            if not chemin_wf:
                return {"status": "erreur", "message": "Chemin du fichier workflow manquant."}
            
            resultats = self.cartographier_tous_les_agents(chemin_wf, base_agents, base_docs)
            return {"status": "succes", "resultats_cartographie_globale": resultats, "count": len(resultats)}

        elif task_name == "mettre_a_jour_suivi_migration":
            resultats_carto = task_params.get("resultats_cartographie")
            chemin_suivi = task_params.get("chemin_fichier_suivi")
            if not resultats_carto or not chemin_suivi:
                return {"status": "erreur", "message": "Résultats de cartographie ou chemin du fichier de suivi manquants."}
            succes_maj = self.mettre_a_jour_suivi_migration(resultats_carto, chemin_suivi)
            if succes_maj:
                return {"status": "succes", "message": "Mise à jour du suivi (simulée) effectuée."}
            else:
                return {"status": "erreur", "message": "Échec de la mise à jour (simulée) du suivi."}
        else:
            self.logger.warning(f"Tâche ACP inconnue : {task_name}")
            return {"status": "erreur", "message": f"Tâche ACP inconnue : {task_name}"}

# --- Pour tests directs (nécessite mocks ou vraies instances des assistants) ---
# Si on voulait exécuter cela, il faudrait gérer les imports et instancier les assistants.
if __name__ == '__main__':
    # Mocks simplifiés pour les assistants
    class MockLecteurWorkflow: 
        def execute_task(self, task, params):
            if params["chemin_fichier_workflow"] == "WORKFLOW_SUIVI_AGENTS.md":
                return {"status": "succes", "resultat": {"agents": [
                    {"script_python": "agent_01_coordinateur_principal.py", "doc_md": "agent_01_coordinateur_principal.md"},
                    {"script_python": "agent_02_architecte_code_expert.py", "doc_md": "agent_02_architecte_code_expert.md"},
                    {"script_python": "agent_X_sans_doc.py", "doc_md": None}, # Agent sans doc explicite
                    {"script_python": "agent_Y_fichier_inexistant.py"} # Script Python manquant
                ]}}
            return {"status": "erreur", "message": "Workflow non trouvé par Mock ALW"}

    class MockAnalyseurCode: 
        def execute_task(self, task, params):
            path = params["chemin_fichier"]
            if "agent_X_sans_doc.py" in path: # Simuler existence de ce fichier
                 return {"status": "succes", "resultat": {"chemin_fichier": path, "version_agent": "X.1", "docstring_module": "Docstring Agent X"}}
            if Path(path).name == "agent_01_coordinateur_principal.py": # Simuler existence
                return {"status": "succes", "resultat": {"chemin_fichier": path, "version_agent": "1.0.0", "docstring_module": "Coord principal code."}}
            if Path(path).name == "agent_02_architecte_code_expert.py":
                return {"status": "succes", "resultat": {"chemin_fichier": path, "version_agent": "2.0.0", "docstring_module": "Architecte code."}}
            return {"status": "erreur", "message": f"Fichier code non trouvé par Mock AACP: {path}"} 
            
    class MockAnalyseurDoc: 
        def execute_task(self, task, params):
            path = params["chemin_fichier"]
            if Path(path).name == "agent_01_coordinateur_principal.md":
                return {"status": "succes", "resultat": {"chemin_fichier": path, "version_documentee": "1.0.0", "sections":[{"titre":"Desc Doc 01", "contenu":"Coord principal doc."}]}}
            if Path(path).name == "agent_02_architecte_code_expert.md":
                 return {"status": "succes", "resultat": {"chemin_fichier": path, "version_documentee": "2.0.1", "sections":[{"titre":"Desc Doc 02", "contenu":"Architecte doc DIFFERENT."}]}}
            # Pour agent_X_sans_doc.md (déduit), simuler un échec ou une absence
            if Path(path).name == "agent_X_sans_doc.md":
                 return {"status": "erreur", "message": f"Doc {path} non trouvée par Mock AADM."}
            return {"status": "erreur", "message": f"Fichier doc non trouvé par Mock AADM: {path}"}

    # Utilisation du MockComparateur de son propre fichier pour le test interne
    # Dans une vraie app, ACS serait importé et instancié avec les vrais AACP/AADM
    class MockComparateurACS:
        def __init__(self, ac, ad): self.ac=ac; self.ad=ad # Garder la signature pour ACP
        def execute_task(self, task, params):
            if task == "comparer_code_et_doc":
                # Logique simplifiée de comparaison pour le mock
                py_path = params["chemin_fichier_python"]
                md_path = params["chemin_fichier_markdown"]
                # Simuler appel aux vrais analyseurs (ici, on utilise les mocks passés à ACP)
                res_code = self.ac.execute_task("analyser_fichier_python", {"chemin_fichier": py_path})
                res_doc = self.ad.execute_task("analyser_fichier_markdown", {"chemin_fichier": md_path})
                
                ecarts_mock = []
                if res_code.get("status")=="succes" and res_doc.get("status")=="succes":
                    if res_code["resultat"].get("version_agent") != res_doc["resultat"].get("version_documentee"):
                        ecarts_mock.append({"type":"Version", "message":"Ecart version mock"})
                    return {"status":"succes", "donnees_code":res_code["resultat"], "donnees_doc":res_doc["resultat"], "ecarts":ecarts_mock}
                return {"status":"erreur", "message":"Mock ACS: Echec analyse code ou doc"}
            elif task == "generer_rapport_ecarts":
                return {"status": "succes", "rapport": "Rapport Mock ACS: ..."}
            return {"status": "erreur", "message": "MockComparateurACS: Tâche inconnue"}

    mock_alw = MockLecteurWorkflow()
    mock_aacp = MockAnalyseurCode()
    mock_aadm = MockAnalyseurDoc()
    mock_acs = MockComparateurACS(mock_aacp, mock_aadm) # ACS a besoin des instances

    acp = AgentCartographePrincipal(
        lecteur_workflow=mock_alw,
        analyseur_code=mock_aacp, 
        analyseur_doc=mock_aadm,
        comparateur_sync=mock_acs
    )

    print("\n--- Capacités de l'agent ACP ---")
    print(json.dumps(acp.get_capabilities(), indent=2))

    # Créer des dummy files pour que Path().exists() passe dans le code de l'ACP
    # Ces fichiers ne seront pas lus par les mocks, qui ont leur propre logique.
    Path("agents").mkdir(exist_ok=True)
    Path("docs/3_Agents_et_Modeles_IA/agents").mkdir(parents=True, exist_ok=True)
    Path("agents/agent_01_coordinateur_principal.py").touch()
    Path("docs/3_Agents_et_Modeles_IA/agents/agent_01_coordinateur_principal.md").touch()
    Path("agents/agent_02_architecte_code_expert.py").touch()
    Path("docs/3_Agents_et_Modeles_IA/agents/agent_02_architecte_code_expert.md").touch()
    Path("agents/agent_X_sans_doc.py").touch() # Doc sera déduite et non trouvée par mock AADM
    # agent_Y_fichier_inexistant.py n'est pas créé, pour tester ce cas.

    print("\n--- Cartographie de tous les agents (simulation avec Mocks) ---")
    params_tous_agents = {
        "chemin_workflow_file": "WORKFLOW_SUIVI_AGENTS.md", # ALW Mock va le gérer
        "base_path_agents": "agents",
        "base_path_docs": "docs/3_Agents_et_Modeles_IA/agents"
    }
    resultats_globaux = acp.execute_task("cartographier_tous_les_agents", params_tous_agents)
    print(json.dumps(resultats_globaux, indent=2, ensure_ascii=False))

    if resultats_globaux.get("status") == "succes":
        print("\n--- Simulation Mise à Jour Suivi Migration (avec Mocks) ---")
        params_maj_suivi = {
            "resultats_cartographie": resultats_globaux.get("resultats_cartographie_globale"),
            "chemin_fichier_suivi": "agents_migration_workspace/SUIVI_MIGRATION_AGENTS.md"
        }
        res_maj = acp.execute_task("mettre_a_jour_suivi_migration", params_maj_suivi)
        print(json.dumps(res_maj, indent=2))
    
    # Nettoyage des dummy files
    Path("agents/agent_01_coordinateur_principal.py").unlink(missing_ok=True)
    Path("docs/3_Agents_et_Modeles_IA/agents/agent_01_coordinateur_principal.md").unlink(missing_ok=True)
    Path("agents/agent_02_architecte_code_expert.py").unlink(missing_ok=True)
    Path("docs/3_Agents_et_Modeles_IA/agents/agent_02_architecte_code_expert.md").unlink(missing_ok=True)
    Path("agents/agent_X_sans_doc.py").unlink(missing_ok=True)
