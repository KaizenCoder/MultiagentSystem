#!/usr/bin/env python3
"""
Agent Analyseur - Analyse Approfondie des Outils Imports
Mission: Analyser la structure, les dpendances et les fonctionnalits des outils
"""

import json
import ast
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Set

class AgentAnalyseurOutils:
    """Agent spcialis dans l'analyse approfondie des outils"""
    
    def __init__(self):
        self.agent_id = f"ANALYSEUR_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.base_path = Path(__file__).parent
        self.imported_tools_path = self.base_path / "tools" / "imported_tools"
        
        # Configuration logging
        self.setup_logging()
        
    def setup_logging(self):
        """Configuration du systme de logging"""
        log_dir = self.base_path / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"AgentAnalyseur_{self.agent_id}")
        
        # Handler spcifique pour cet agent
        handler = logging.FileHandler(log_dir / f"{self.agent_id}_analyseur.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
    def analyser_outil_complet(self, nom_outil: str, info_outil: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse complte d'un outil spcifique"""
        self.logger.info(f"[SEARCH] Analyse approfondie de l'outil: {nom_outil}")
        
        # Rcupration du chemin du fichier principal
        chemin_outil = Path(info_outil["path"])
        if not chemin_outil.exists():
            chemin_outil = self.base_path / info_outil["path"]
            
        if not chemin_outil.exists():
            self.logger.error(f"[CROSS] Fichier introuvable: {info_outil['path']}")
            return {"erreur": "fichier_introuvable", "chemin": str(chemin_outil)}
            
        analyse = {
            "nom": nom_outil,
            "chemin_original": str(chemin_outil),
            "categorie": info_outil["category"],
            "priorite": info_outil["priority"],
            "score_utilite": info_outil["utility_score"],
            "analyse_code": self.analyser_code_python(chemin_outil),
            "dependances": self.extraire_dependances(chemin_outil),
            "fonctionnalites": self.identifier_fonctionnalites(chemin_outil),
            "complexite": self.evaluer_complexite(chemin_outil),
            "adaptations_requises": self.identifier_adaptations_requises(chemin_outil),
            "recommandations": self.generer_recommandations(nom_outil, chemin_outil)
        }
        
        self.logger.info(f"[CHECK] Analyse termine pour {nom_outil}: {len(analyse['fonctionnalites'])} fonctionnalits identifies")
        return analyse
        
    def analyser_code_python(self, chemin_fichier: Path) -> Dict[str, Any]:
        """Analyse le code Python pour extraire les mtadonnes"""
        try:
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                contenu = f.read()
                
            tree = ast.parse(contenu)
            
            analyse = {
                "lignes_code": len(contenu.split('\n')),
                "classes": [],
                "fonctions": [],
                "imports": [],
                "variables_globales": [],
                "docstring": ast.get_docstring(tree) or "Aucune documentation"
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    analyse["classes"].append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    analyse["fonctions"].append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        analyse["imports"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        for alias in node.names:
                            analyse["imports"].append(f"{node.module}.{alias.name}")
                            
            return analyse
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur lors de l'analyse du code: {e}")
            return {"erreur": str(e)}
            
    def extraire_dependances(self, chemin_fichier: Path) -> List[str]:
        """Extrait les dpendances du fichier"""
        dependances = set()
        
        try:
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                contenu = f.read()
                
            tree = ast.parse(contenu)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        dependances.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        dependances.add(node.module.split('.')[0])
                        
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur extraction dpendances: {e}")
            
        # Filtrer les modules standard Python
        modules_standard = {'os', 'sys', 'json', 'datetime', 'pathlib', 'logging', 'subprocess', 're', 'collections'}
        dependances_externes = dependances - modules_standard
        
        return list(dependances_externes)
        
    def identifier_fonctionnalites(self, chemin_fichier: Path) -> List[Dict[str, str]]:
        """Identifie les fonctionnalits principales de l'outil"""
        fonctionnalites = []
        
        try:
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                contenu = f.read()
                
            tree = ast.parse(contenu)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    docstring = ast.get_docstring(node) or "Fonction sans documentation"
                    fonctionnalites.append({
                        "nom": node.name,
                        "type": "fonction",
                        "description": docstring[:100] + "..." if len(docstring) > 100 else docstring,
                        "arguments": len(node.args.args)
                    })
                elif isinstance(node, ast.ClassDef):
                    docstring = ast.get_docstring(node) or "Classe sans documentation"
                    fonctionnalites.append({
                        "nom": node.name,
                        "type": "classe",
                        "description": docstring[:100] + "..." if len(docstring) > 100 else docstring,
                        "methodes": len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                    })
                    
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur identification fonctionnalits: {e}")
            
        return fonctionnalites
        
    def evaluer_complexite(self, chemin_fichier: Path) -> Dict[str, Any]:
        """value la complexit du code"""
        try:
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                contenu = f.read()
                
            tree = ast.parse(contenu)
            
            complexite = {
                "lignes_code": len([line for line in contenu.split('\n') if line.strip() and not line.strip().startswith('#')]),
                "nombre_fonctions": len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]),
                "nombre_classes": len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]),
                "profondeur_imbrication": self.calculer_profondeur_imbrication(tree),
                "niveau_complexite": "FAIBLE"  # Par dfaut
            }
            
            # Calcul du niveau de complexit
            score_complexite = (
                complexite["lignes_code"] * 0.1 +
                complexite["nombre_fonctions"] * 2 +
                complexite["nombre_classes"] * 3 +
                complexite["profondeur_imbrication"] * 5
            )
            
            if score_complexite > 100:
                complexite["niveau_complexite"] = "ELEVEE"
            elif score_complexite > 50:
                complexite["niveau_complexite"] = "MOYENNE"
                
            return complexite
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur valuation complexit: {e}")
            return {"erreur": str(e)}
            
    def calculer_profondeur_imbrication(self, tree: ast.AST) -> int:
        """Calcule la profondeur d'imbrication maximale"""
        max_depth = 0
        
        def calculer_profondeur(node, depth=0):
            nonlocal max_depth
            max_depth = max(max_depth, depth)
            
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                    calculer_profondeur(child, depth + 1)
                else:
                    calculer_profondeur(child, depth)
                    
        calculer_profondeur(tree)
        return max_depth
        
    def identifier_adaptations_requises(self, chemin_fichier: Path) -> List[str]:
        """Identifie les adaptations ncessaires pour NextGeneration"""
        adaptations = []
        
        try:
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                contenu = f.read()
                
            # Vrifications spcifiques  NextGeneration
            if "SuperWhisper" in contenu:
                adaptations.append("Remplacer les rfrences SuperWhisper par NextGeneration")
                
            if "print(" in contenu and "logging" not in contenu:
                adaptations.append("Remplacer print() par logging pour intgration NextGeneration")
                
            if "hardcoded" in contenu.lower() or "/absolute/path" in contenu:
                adaptations.append("Remplacer les chemins hardcods par des chemins relatifs")
                
            if "config" not in contenu.lower():
                adaptations.append("Ajouter support configuration NextGeneration")
                
            if "__name__ == '__main__'" not in contenu:
                adaptations.append("Ajouter point d'entre principal")
                
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur identification adaptations: {e}")
            
        return adaptations
        
    def generer_recommandations(self, nom_outil: str, chemin_fichier: Path) -> List[str]:
        """Gnre des recommandations d'amlioration"""
        recommandations = []
        
        # Recommandations bases sur l'analyse
        recommandations.extend([
            f"Crer rpertoire ddi: tools/{nom_outil}/",
            f"Ajouter documentation: tools/{nom_outil}/README.md",
            f"Crer tests unitaires: tests/unit/test_{nom_outil}.py",
            f"Ajouter configuration: tools/{nom_outil}/config.json",
            "Intgrer logging NextGeneration",
            "Valider compatibilit Python 3.8+",
            "Optimiser performance si ncessaire"
        ])
        
        return recommandations
        
    def executer_analyse_complete(self) -> Dict[str, Any]:
        """Excute l'analyse complte de tous les outils"""
        self.logger.info("[ROCKET] Dmarrage de l'analyse complte des outils")
        
        # Lecture configuration
        config_file = self.imported_tools_path / "tools_config.json"
        with open(config_file, 'r') as f:
            config = json.load(f)
            
        resultats_analyse = {
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat(),
            "outils_analyses": {},
            "resume_global": {},
            "recommandations_globales": []
        }
        
        # Analyse de chaque outil
        for outil in config["nextgeneration_tools"]["tools"]:
            nom_outil = outil["name"]
            analyse_outil = self.analyser_outil_complet(nom_outil, outil)
            resultats_analyse["outils_analyses"][nom_outil] = analyse_outil
            
        # Gnration du rsum global
        resultats_analyse["resume_global"] = self.generer_resume_global(resultats_analyse["outils_analyses"])
        resultats_analyse["recommandations_globales"] = self.generer_recommandations_globales(resultats_analyse["outils_analyses"])
        
        # Sauvegarde du rapport
        self.sauvegarder_rapport(resultats_analyse)
        
        self.logger.info(f"[CHECK] Analyse complte termine: {len(resultats_analyse['outils_analyses'])} outils analyss")
        return resultats_analyse
        
    def generer_resume_global(self, analyses: Dict[str, Any]) -> Dict[str, Any]:
        """Gnre un rsum global des analyses"""
        total_outils = len(analyses)
        total_fonctionnalites = sum(len(analyse.get("fonctionnalites", [])) for analyse in analyses.values())
        dependances_uniques = set()
        
        for analyse in analyses.values():
            if "dependances" in analyse:
                dependances_uniques.update(analyse["dependances"])
                
        return {
            "nombre_outils_total": total_outils,
            "nombre_fonctionnalites_total": total_fonctionnalites,
            "dependances_externes_uniques": list(dependances_uniques),
            "nombre_dependances_uniques": len(dependances_uniques),
            "complexite_moyenne": "MOYENNE",  # Calcul simplifi
            "taux_readiness": 0.75  # Estimation base sur l'analyse
        }
        
    def generer_recommandations_globales(self, analyses: Dict[str, Any]) -> List[str]:
        """Gnre des recommandations globales"""
        return [
            "Crer structure modulaire tools/{nom_outil}/ pour chaque outil",
            "Standardiser le logging avec le systme NextGeneration",
            "Crer suite de tests complte pour validation",
            "Documenter API et usage de chaque outil",
            "Optimiser les dpendances communes",
            "Intgrer monitoring et observabilit",
            "Valider scurit et permissions",
            "Crer scripts d'installation automatiss"
        ]
        
    def sauvegarder_rapport(self, resultats: Dict[str, Any]) -> None:
        """Sauvegarde le rapport d'analyse"""
        rapport_file = self.base_path / "logs" / f"{self.agent_id}_analyse_complete.json"
        
        with open(rapport_file, 'w', encoding='utf-8') as f:
            json.dump(resultats, f, indent=2, ensure_ascii=False)
            
        self.logger.info(f"[CHART] Rapport d'analyse sauvegard: {rapport_file}")

if __name__ == "__main__":
    agent = AgentAnalyseurOutils()
    rapport = agent.executer_analyse_complete()
    
    print(f"\n[SEARCH] Analyse complte termine")
    print(f"[CLIPBOARD] Agent ID: {rapport['agent_id']}")
    print(f"[TOOL] Outils analyss: {rapport['resume_global']['nombre_outils_total']}")
    print(f" Fonctionnalits identifies: {rapport['resume_global']['nombre_fonctionnalites_total']}")
    print(f" Dpendances externes: {rapport['resume_global']['nombre_dependances_uniques']}") 