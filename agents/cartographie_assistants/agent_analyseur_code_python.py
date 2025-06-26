# agents/cartographie_assistants/agent_analyseur_code_python.py
import ast
import logging
from typing import Dict, Any, List, Optional

# Configuration du logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AgentAnalyseurCodePython:
    """
    Agent responsable de l'analyse statique de fichiers de code Python.
    Il peut extraire des informations telles que :
    - La structure du code (classes, fonctions, imports)
    - Les docstrings
    - La version de l'agent (si définie par une variable __version__)
    - La conformité à certaines conventions (ex: Pattern Factory)
    """
    __version__ = "0.1.0"

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"Initialisation de {self.__class__.__name__} version {self.__version__}")

    def get_capabilities(self) -> Dict[str, Any]:
        """Retourne les capacités de l'agent."""
        return {
            "name": self.__class__.__name__,
            "version": self.__version__,
            "description": "Analyse statique de fichiers de code Python pour en extraire la structure, les docstrings, et vérifier la conformité.",
            "tasks": [
                {"name": "analyser_fichier_python", "description": "Analyse un fichier Python et retourne un dictionnaire structuré d'informations."},
                {"name": "verifier_conformite_pattern_factory", "description": "Vérifie si un fichier Python semble se conformer au Pattern Factory."}
            ]
        }

    def analyser_fichier_python(self, chemin_fichier: str) -> Optional[Dict[str, Any]]:
        """
        Analyse un fichier Python donné et extrait sa structure.

        Args:
            chemin_fichier: Le chemin vers le fichier Python à analyser.

        Returns:
            Un dictionnaire contenant des informations sur le fichier (classes, fonctions, imports, docstrings),
            ou None si le fichier ne peut pas être lu ou parsé.
        """
        self.logger.info(f"Début de l'analyse du fichier : {chemin_fichier}")
        try:
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            arbre_syntaxique = ast.parse(contenu)
            analyse_resultat = {
                "chemin_fichier": chemin_fichier,
                "imports": [],
                "classes": [],
                "fonctions": [],
                "docstring_module": ast.get_docstring(arbre_syntaxique),
                "version_agent": None
            }
            
            # Pour stocker les ClassDef originaux pour une recherche ultérieure de __version__ de classe
            class_defs_nodes = {} 

            for node in arbre_syntaxique.body:
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        analyse_resultat["imports"].append({"name": alias.name, "asname": alias.asname})
                elif isinstance(node, ast.ImportFrom):
                    module_name = node.module if node.module else "." * node.level
                    for alias in node.names:
                        analyse_resultat["imports"].append({"module": module_name, "name": alias.name, "asname": alias.asname})
                elif isinstance(node, ast.FunctionDef):
                    analyse_resultat["fonctions"].append({
                        "nom": node.name,
                        "docstring": ast.get_docstring(node),
                        "args": [arg.arg for arg in node.args.args]
                    })
                elif isinstance(node, ast.ClassDef):
                    class_defs_nodes[node.name] = node # Stocker le nœud ClassDef
                    classe_info = {
                        "nom": node.name,
                        "docstring": ast.get_docstring(node),
                        "methodes": [],
                        "attributes": [] # Attributs de classe (noms seulement)
                    }
                    for item_class_body in node.body:
                        if isinstance(item_class_body, ast.FunctionDef):
                            classe_info["methodes"].append({
                                "nom": item_class_body.name,
                                "docstring": ast.get_docstring(item_class_body),
                                "args": [arg.arg for arg in item_class_body.args.args]
                            })
                        elif isinstance(item_class_body, (ast.Assign, ast.AnnAssign)): # Attribut de classe
                            targets_attr = []
                            if isinstance(item_class_body, ast.Assign):
                                targets_attr = item_class_body.targets
                            elif isinstance(item_class_body, ast.AnnAssign):
                                targets_attr = [item_class_body.target]
                            
                            for target in targets_attr:
                                if isinstance(target, ast.Name):
                                    classe_info["attributes"].append(target.id)

                    analyse_resultat["classes"].append(classe_info)
                elif isinstance(node, ast.Assign): # Assignation au niveau du module
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == "__version__":
                            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                                analyse_resultat["version_agent"] = node.value.value
                            elif hasattr(ast, 'Str') and isinstance(node.value, ast.Str) and isinstance(node.value.s, str): # Python < 3.8
                                analyse_resultat["version_agent"] = node.value.s
            
            # Si __version__ n'a pas été trouvé au niveau module, chercher dans les classes
            if analyse_resultat["version_agent"] is None:
                for class_name, class_node_def in class_defs_nodes.items():
                    for item_class_body in class_node_def.body:
                        if isinstance(item_class_body, ast.Assign):
                            for target in item_class_body.targets:
                                if isinstance(target, ast.Name) and target.id == "__version__":
                                    if isinstance(item_class_body.value, ast.Constant) and isinstance(item_class_body.value.value, str):
                                        analyse_resultat["version_agent"] = item_class_body.value.value
                                        break # Prendre la première version de classe trouvée
                                    elif hasattr(ast, 'Str') and isinstance(item_class_body.value, ast.Str) and isinstance(item_class_body.value.s, str): # Python < 3.8
                                        analyse_resultat["version_agent"] = item_class_body.value.s
                                        break 
                            if analyse_resultat["version_agent"] is not None:
                                break # Sortir de la boucle des items de classe
                    if analyse_resultat["version_agent"] is not None:
                        self.logger.info(f"__version__ trouvée dans la classe {class_name}: {analyse_resultat['version_agent']}")
                        break # Sortir de la boucle des classes

            self.logger.info(f"Analyse terminée avec succès pour : {chemin_fichier}")
            return analyse_resultat

        except FileNotFoundError:
            self.logger.error(f"Fichier non trouvé : {chemin_fichier}")
            return None
        except SyntaxError as e:
            self.logger.error(f"Erreur de syntaxe dans le fichier {chemin_fichier}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Erreur inattendue lors de l'analyse de {chemin_fichier}: {e}", exc_info=True)
            return None

    def verifier_conformite_pattern_factory(self, chemin_fichier: str) -> Dict[str, Any]:
        """
        Vérifie si un fichier Python semble se conformer aux conventions de base
        d'un agent basé sur le Pattern Factory (présence de get_capabilities, execute_task).
        Ceci est une vérification simplifiée.

        Args:
            chemin_fichier: Le chemin vers le fichier Python à vérifier.

        Returns:
            Un dictionnaire avec un booléen 'conforme' et une liste de 'details'.
        """
        self.logger.info(f"Vérification de conformité Pattern Factory pour : {chemin_fichier}")
        analyse = self.analyser_fichier_python(chemin_fichier)
        resultat = {"conforme": False, "details": [], "version_pf_supposee": None}

        if not analyse:
            resultat["details"].append("Impossible d'analyser le fichier.")
            return resultat

        if not analyse["classes"]:
            resultat["details"].append("Le fichier ne contient aucune classe.")
            return resultat # Non conforme s'il n'y a pas de classes

        classe_agent_principale = None
        for classe_info in analyse["classes"]:
            method_names = [methode["nom"] for methode in classe_info["methodes"]]
            if "get_capabilities" in method_names and "execute_task" in method_names:
                classe_agent_principale = classe_info
                resultat["details"].append(f"Classe agent potentielle identifiée: {classe_agent_principale['nom']}")
                break
        
        if not classe_agent_principale:
            resultat["details"].append("Aucune classe principale d'agent (avec get_capabilities ET execute_task) n'a été trouvée.")
            # On ne retourne pas immédiatement, car on veut quand même vérifier la présence de __version__ au niveau module
            # et ajouter les détails sur les méthodes manquantes même si aucune classe ne les combine.
        
        # Vérification de __version__ (module ou classe, déjà géré par analyser_fichier_python)
        version_trouvee = analyse.get("version_agent") is not None
        if version_trouvee:
            resultat["details"].append(f"Attribut '__version__' trouvé (valeur: {analyse['version_agent']}).")
        else:
            resultat["details"].append("Attribut '__version__' MANQUANT (module ou classe).")

        # Vérification des méthodes clés, même si classe_agent_principale n'est pas définie (pour loguer les manques)
        has_get_capabilities_globally = False
        has_execute_task_globally = False

        if classe_agent_principale: # Si une classe candidate a été trouvée
            methodes_presentes = [m["nom"] for m in classe_agent_principale["methodes"]]
            has_get_capabilities_globally = "get_capabilities" in methodes_presentes
            has_execute_task_globally = "execute_task" in methodes_presentes
        else: # Aucune classe candidate, vérifier si les méthodes existent quelque part (moins strict, mais informatif)
            for classe_info_iter in analyse["classes"]:
                 method_names_iter = [methode["nom"] for methode in classe_info_iter["methodes"]]
                 if "get_capabilities" in method_names_iter:
                     has_get_capabilities_globally = True
                 if "execute_task" in method_names_iter:
                     has_execute_task_globally = True
            if not analyse["classes"]: # Double check, devrait être couvert plus haut
                resultat["details"].append("Le fichier ne contient aucune classe pour rechercher les méthodes.")


        if has_get_capabilities_globally:
            resultat["details"].append("Au moins une méthode 'get_capabilities' trouvée dans une classe.")
        else:
            resultat["details"].append("Méthode 'get_capabilities' MANQUANTE dans toutes les classes.")

        if has_execute_task_globally:
            resultat["details"].append("Au moins une méthode 'execute_task' trouvée dans une classe.")
        else:
            resultat["details"].append("Méthode 'execute_task' MANQUANTE dans toutes les classes.")
        
        # La conformité stricte requiert que la même classe ait les deux méthodes ET qu'une version soit présente
        is_strictly_conforme = bool(classe_agent_principale and version_trouvee)

        if is_strictly_conforme:
            resultat["conforme"] = True
            resultat["version_pf_supposee"] = analyse['version_agent'] # Mettre la version seulement si conforme
            resultat["details"].append("L'agent semble conforme aux conventions de base du Pattern Factory.")
        else:
            resultat["conforme"] = False # Assurer que c'est false si non strictement conforme
            resultat["details"].append("L'agent NE SEMBLE PAS strictement conforme aux conventions de base du Pattern Factory.")
            # Nettoyer les détails redondants potentiels si aucune classe principale trouvée
            if not classe_agent_principale and "Aucune classe principale d'agent (avec get_capabilities ET execute_task) n'a été trouvée." not in resultat["details"]:
                 resultat["details"].insert(0, "Aucune classe principale d'agent (avec get_capabilities ET execute_task) n'a été trouvée.")

        # Filtrer les détails dupliqués pour la clarté
        unique_details = []
        for detail in resultat["details"]:
            if detail not in unique_details:
                unique_details.append(detail)
        resultat["details"] = unique_details
            
        return resultat

    def execute_task(self, task_name: str, task_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute une tâche spécifique.
        """
        self.logger.info(f"Exécution de la tâche '{task_name}' avec les paramètres : {task_params}")
        if task_name == "analyser_fichier_python":
            chemin_fichier = task_params.get("chemin_fichier")
            if not chemin_fichier:
                return {"status": "erreur", "message": "Le paramètre 'chemin_fichier' est manquant."}
            resultat_analyse = self.analyser_fichier_python(chemin_fichier)
            if resultat_analyse:
                return {"status": "succes", "resultat": resultat_analyse}
            else:
                return {"status": "erreur", "message": f"Échec de l'analyse du fichier {chemin_fichier}."}
        
        elif task_name == "verifier_conformite_pattern_factory":
            chemin_fichier = task_params.get("chemin_fichier")
            if not chemin_fichier:
                return {"status": "erreur", "message": "Le paramètre 'chemin_fichier' est manquant."}
            resultat_conformite = self.verifier_conformite_pattern_factory(chemin_fichier)
            return {"status": "succes", "resultat": resultat_conformite}
            
        else:
            self.logger.warning(f"Tâche inconnue : {task_name}")
            return {"status": "erreur", "message": f"Tâche inconnue : {task_name}"}

if __name__ == '__main__':
    import json
    # Exemple d'utilisation
    analyseur = AgentAnalyseurCodePython()
    
    # Test avec un fichier existant (par exemple, lui-même)
    chemin_test_fichier_agent = __file__ 
    
    print("\\n--- Capacités de l'agent ---")
    print(json.dumps(analyseur.get_capabilities(), indent=2))

    print(f"\\n--- Analyse du fichier AGENT : {chemin_test_fichier_agent} ---")
    resultat_task_analyse_agent = analyseur.execute_task("analyser_fichier_python", {"chemin_fichier": chemin_test_fichier_agent})
    
    if resultat_task_analyse_agent and resultat_task_analyse_agent.get("status") == "succes":
        resultat_analyse_contenu = resultat_task_analyse_agent.get("resultat", {})
        print("Version Agent:", resultat_analyse_contenu.get("version_agent"))
        print("Docstring Module:", resultat_analyse_contenu.get("docstring_module") is not None) # Afficher True/False
        print("Extrait Docstring Module:", (resultat_analyse_contenu.get("docstring_module") or "")[:100] + "...")
        print("Nombre d'imports:", len(resultat_analyse_contenu.get("imports", [])))
        print("Nombre de fonctions globales:", len(resultat_analyse_contenu.get("fonctions", [])))
        print("Nombre de classes:", len(resultat_analyse_contenu.get("classes", [])))
        for classe in resultat_analyse_contenu.get("classes", []):
            print(f"  Classe: {classe.get('nom')}, Méthodes: {len(classe.get('methodes',[]))}, Attributs: {len(classe.get('attributes',[]))}")
    else:
        print(f"Échec de l'analyse AGENT : {resultat_task_analyse_agent.get('message')}")

    print(f"\\n--- Vérification conformité Pattern Factory pour AGENT : {chemin_test_fichier_agent} ---")
    resultat_task_conformite_agent = analyseur.execute_task("verifier_conformite_pattern_factory", {"chemin_fichier": chemin_test_fichier_agent})
    if resultat_task_conformite_agent and resultat_task_conformite_agent.get("status") == "succes":
        print(json.dumps(resultat_task_conformite_agent.get("resultat"), indent=2, ensure_ascii=False))
    else:
        print(f"Échec de la vérification de conformité AGENT : {resultat_task_conformite_agent.get('message')}")

    # Test avec un fichier potentiellement non conforme ou simple
    dummy_file_content = """\"\"\"Ceci est un docstring de module pour le fichier factice.\"\"\"
__version__ = "0.0.1" # Version module
import os

def hello_world():
    'Salutation.'
    print("Hello")

class NotAnAgent:
    # __version__ = "0.0.2" # Version classe (test)
    pass

class AnotherClass:
    def get_capabilities(self):
        return {}
""" # Assurez-vous que la chaîne multiligne se termine ici correctement
    dummy_file_path = "dummy_test_file.py"
    with open(dummy_file_path, "w", encoding="utf-8") as f:
        f.write(dummy_file_content)
    
    print(f"\\n--- Analyse du fichier DUMMY : {dummy_file_path} ---")
    res_dummy_analyse = analyseur.execute_task("analyser_fichier_python", {"chemin_fichier": dummy_file_path})
    if res_dummy_analyse and res_dummy_analyse.get("status") == "succes":
         print(json.dumps(res_dummy_analyse.get("resultat"), indent=2, ensure_ascii=False))
    else:
        print(f"Échec de l'analyse DUMMY : {res_dummy_analyse.get('message')}")

    print(f"\\n--- Vérification conformité Pattern Factory pour DUMMY : {dummy_file_path} ---")
    res_dummy_conformite = analyseur.execute_task("verifier_conformite_pattern_factory", {"chemin_fichier": dummy_file_path})
    if res_dummy_conformite and res_dummy_conformite.get("status") == "succes":
        print(json.dumps(res_dummy_conformite.get("resultat"), indent=2, ensure_ascii=False))
    else:
        print(f"Échec de la vérification de conformité DUMMY: {res_dummy_conformite.get('message')}")
    
    # Nettoyage du fichier dummy
    import os
    try:
        os.remove(dummy_file_path)
        print(f"Fichier {dummy_file_path} supprimé.")
    except OSError as e:
        print(f"Erreur lors de la suppression de {dummy_file_path}: {e}")