#!/usr/bin/env python3
"""
Agent Rapport Final - Consolidation Mission Rorganisation
Mission: Gnrer le rapport final complet de la mission de rorganisation des outils
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import subprocess
import sys

class AgentRapportFinal:
    """Agent de consolidation et rapport final"""
    
    def __init__(self):
        self.agent_id = f"RAPPORT_FINAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.base_path = Path(__file__).parent
        self.logs_path = self.base_path / "logs"
        
        # Configuration logging
        self.setup_logging()
        
    def setup_logging(self):
        """Configuration du systme de logging"""
        self.logs_path.mkdir(exist_ok=True)
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"AgentRapportFinal_{self.agent_id}")
        
        # Handler spcifique
        handler = logging.FileHandler(self.logs_path / f"{self.agent_id}_rapport_final.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
    def collecter_rapports_agents(self) -> Dict[str, Any]:
        """Collecte tous les rapports des agents spcialiss"""
        self.logger.info("[CHART] Collecte des rapports d'agents")
        
        rapports = {
            "coordinateur": None,
            "analyseur": None,
            "organisateur": None,
            "adaptateur_doc": None,
            "testeur": None
        }
        
        # Recherche des fichiers de rapports
        for rapport_file in self.logs_path.glob("*.json"):
            if "coordinateur" in rapport_file.name:
                rapports["coordinateur"] = self.charger_rapport(rapport_file)
            elif "analyseur" in rapport_file.name:
                rapports["analyseur"] = self.charger_rapport(rapport_file)
            elif "organisateur" in rapport_file.name:
                rapports["organisateur"] = self.charger_rapport(rapport_file)
            elif "adaptateur_doc" in rapport_file.name:
                rapports["adaptateur_doc"] = self.charger_rapport(rapport_file)
            elif "testeur" in rapport_file.name:
                rapports["testeur"] = self.charger_rapport(rapport_file)
                
        # Filtrage des rapports valides
        rapports_valides = {k: v for k, v in rapports.items() if v is not None}
        
        self.logger.info(f"[CHECK] {len(rapports_valides)} rapports collects")
        return rapports_valides
        
    def charger_rapport(self, fichier_rapport: Path) -> Dict[str, Any]:
        """Charge un rapport JSON"""
        try:
            with open(fichier_rapport, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur chargement rapport {fichier_rapport}: {e}")
            return None
            
    def analyser_etat_final(self) -> Dict[str, Any]:
        """Analyse l'tat final des outils aprs rorganisation"""
        self.logger.info("[SEARCH] Analyse de l'tat final")
        
        tools_path = self.base_path / "tools"
        etat_final = {
            "outils_restructures": [],
            "structure_validee": {},
            "documentation_presente": {},
            "tests_disponibles": {},
            "problemes_detectes": []
        }
        
        # Scan des outils restructurs
        for outil_dir in tools_path.iterdir():
            if outil_dir.is_dir() and outil_dir.name not in ["imported_tools", "__pycache__"]:
                nom_outil = outil_dir.name
                etat_final["outils_restructures"].append(nom_outil)
                
                # Validation structure
                etat_final["structure_validee"][nom_outil] = self.valider_structure_outil(outil_dir)
                
                # Validation documentation
                etat_final["documentation_presente"][nom_outil] = self.valider_documentation_outil(outil_dir)
                
                # Validation tests
                etat_final["tests_disponibles"][nom_outil] = self.valider_tests_outil(nom_outil)
                
        self.logger.info(f"[CHECK] tat final analys: {len(etat_final['outils_restructures'])} outils")
        return etat_final
        
    def valider_structure_outil(self, outil_dir: Path) -> Dict[str, Any]:
        """Valide la structure d'un outil"""
        nom_outil = outil_dir.name
        
        validation = {
            "fichier_principal": (outil_dir / f"{nom_outil}.py").exists(),
            "init_file": (outil_dir / "__init__.py").exists(),
            "readme": (outil_dir / "README.md").exists(),
            "repertoire_config": (outil_dir / "config").exists(),
            "repertoire_docs": (outil_dir / "docs").exists(),
            "repertoire_tests": (outil_dir / "tests").exists(),
            "config_json": (outil_dir / "config" / "config.json").exists()
        }
        
        validation["score"] = sum(validation.values()) / len(validation) * 100
        validation["statut"] = "VALIDE" if validation["score"] >= 80 else "PARTIEL"
        
        return validation
        
    def valider_documentation_outil(self, outil_dir: Path) -> Dict[str, Any]:
        """Valide la documentation d'un outil"""
        docs_dir = outil_dir / "docs"
        
        validation = {
            "readme_principal": (outil_dir / "README.md").exists(),
            "usage_guide": (docs_dir / "USAGE.md").exists(),
            "configuration_guide": (docs_dir / "CONFIGURATION.md").exists(),
            "api_doc": (docs_dir / "API.md").exists(),
            "faq": (docs_dir / "FAQ.md").exists()
        }
        
        # Vrification qualit documentation
        if validation["readme_principal"]:
            readme_size = (outil_dir / "README.md").stat().st_size
            validation["readme_qualite"] = readme_size > 1000
        else:
            validation["readme_qualite"] = False
            
        validation["score"] = sum(validation.values()) / len(validation) * 100
        validation["statut"] = "COMPLETE" if validation["score"] >= 80 else "PARTIELLE"
        
        return validation
        
    def valider_tests_outil(self, nom_outil: str) -> Dict[str, Any]:
        """Valide les tests d'un outil"""
        tests_path = self.base_path / "tests"
        
        validation = {
            "test_unitaire": (tests_path / "unit" / f"test_{nom_outil}.py").exists(),
            "test_integration": (tests_path / "integration" / f"test_{nom_outil}_integration.py").exists()
        }
        
        validation["score"] = sum(validation.values()) / len(validation) * 100
        validation["statut"] = "PRESENTE" if validation["score"] >= 50 else "MANQUANTE"
        
        return validation
        
    def executer_tests_validation(self) -> Dict[str, Any]:
        """Excute les tests pour validation finale"""
        self.logger.info(" Excution tests de validation")
        
        resultats_tests = {
            "tests_unitaires": {"executes": 0, "reussis": 0, "echecs": 0},
            "tests_integration": {"executes": 0, "reussis": 0, "echecs": 0},
            "details": {}
        }
        
        # Tests unitaires
        tests_unit_dir = self.base_path / "tests" / "unit"
        if tests_unit_dir.exists():
            for test_file in tests_unit_dir.glob("test_*.py"):
                nom_test = test_file.stem
                resultats_tests["tests_unitaires"]["executes"] += 1
                
                try:
                    result = subprocess.run([
                        sys.executable, "-m", "pytest", str(test_file), "-v"
                    ], capture_output=True, text=True, timeout=60)
                    
                    if result.returncode == 0:
                        resultats_tests["tests_unitaires"]["reussis"] += 1
                        resultats_tests["details"][nom_test] = "REUSSI"
                    else:
                        resultats_tests["tests_unitaires"]["echecs"] += 1
                        resultats_tests["details"][nom_test] = "ECHEC"
                        
                except Exception as e:
                    resultats_tests["tests_unitaires"]["echecs"] += 1
                    resultats_tests["details"][nom_test] = f"ERREUR: {str(e)}"
                    
        # Tests d'intgration
        tests_int_dir = self.base_path / "tests" / "integration"
        if tests_int_dir.exists():
            for test_file in tests_int_dir.glob("test_*_integration.py"):
                nom_test = test_file.stem
                resultats_tests["tests_integration"]["executes"] += 1
                
                try:
                    result = subprocess.run([
                        sys.executable, "-m", "pytest", str(test_file), "-v"
                    ], capture_output=True, text=True, timeout=120)
                    
                    if result.returncode == 0:
                        resultats_tests["tests_integration"]["reussis"] += 1
                        resultats_tests["details"][nom_test] = "REUSSI"
                    else:
                        resultats_tests["tests_integration"]["echecs"] += 1
                        resultats_tests["details"][nom_test] = "ECHEC"
                        
                except Exception as e:
                    resultats_tests["tests_integration"]["echecs"] += 1
                    resultats_tests["details"][nom_test] = f"ERREUR: {str(e)}"
                    
        self.logger.info("[CHECK] Tests de validation termins")
        return resultats_tests
        
    def generer_recommandations_finales(self, rapports: Dict[str, Any], etat_final: Dict[str, Any]) -> List[str]:
        """Gnre les recommandations finales"""
        recommandations = []
        
        # Analyse des problmes dtects
        for nom_outil, structure in etat_final["structure_validee"].items():
            if structure["score"] < 100:
                recommandations.append(f"Complter la structure de l'outil {nom_outil}")
                
        for nom_outil, doc in etat_final["documentation_presente"].items():
            if doc["score"] < 80:
                recommandations.append(f"Amliorer la documentation de l'outil {nom_outil}")
                
        # Recommandations gnrales
        recommandations.extend([
            "Excuter tests complets avant mise en production",
            "Valider l'intgration avec l'cosystme NextGeneration",
            "Documenter les processus de maintenance",
            "Configurer monitoring continu des outils",
            "Planifier rvision priodique de la documentation"
        ])
        
        return list(set(recommandations))  # Suppression des doublons
        
    def generer_rapport_final_complet(self) -> Dict[str, Any]:
        """Gnre le rapport final complet de la mission"""
        self.logger.info("[ROCKET] Gnration du rapport final complet")
        
        # Collecte des donnes
        rapports_agents = self.collecter_rapports_agents()
        etat_final = self.analyser_etat_final()
        resultats_tests = self.executer_tests_validation()
        
        # Construction du rapport final
        rapport_final = {
            "mission_info": {
                "id": self.agent_id,
                "timestamp_debut": self.extraire_timestamp_debut(rapports_agents),
                "timestamp_fin": datetime.now().isoformat(),
                "duree_mission": self.calculer_duree_mission(rapports_agents)
            },
            "summary_execution": {
                "agents_executes": list(rapports_agents.keys()),
                "outils_traites": len(etat_final["outils_restructures"]),
                "structures_creees": len([s for s in etat_final["structure_validee"].values() if s["statut"] == "VALIDE"]),
                "documentation_complete": len([d for d in etat_final["documentation_presente"].values() if d["statut"] == "COMPLETE"]),
                "tests_disponibles": len([t for t in etat_final["tests_disponibles"].values() if t["statut"] == "PRESENTE"])
            },
            "resultats_detailles": {
                "rapports_agents": rapports_agents,
                "etat_final": etat_final,
                "resultats_tests": resultats_tests
            },
            "evaluation_globale": {
                "statut_mission": self.evaluer_statut_mission(etat_final, resultats_tests),
                "taux_reussite_structure": self.calculer_taux_reussite(etat_final["structure_validee"]),
                "taux_reussite_documentation": self.calculer_taux_reussite(etat_final["documentation_presente"]),
                "taux_reussite_tests": self.calculer_taux_reussite_tests(resultats_tests)
            },
            "recommandations": self.generer_recommandations_finales(rapports_agents, etat_final),
            "prochaines_etapes": [
                "Valider qualit code avec outils d'analyse statique",
                "Excuter tests de charge et performance",
                "Intgrer dans pipeline CI/CD NextGeneration",
                "Former quipe sur nouveaux outils",
                "Dployer en environnement de test",
                "Monitoring et observabilit en production"
            ]
        }
        
        # Sauvegarde du rapport final
        self.sauvegarder_rapport_final(rapport_final)
        
        self.logger.info("[CHECK] Rapport final gnr avec succs")
        return rapport_final
        
    def extraire_timestamp_debut(self, rapports: Dict[str, Any]) -> str:
        """Extrait le timestamp de dbut de mission"""
        timestamps = []
        for rapport in rapports.values():
            if rapport and "timestamp" in rapport:
                timestamps.append(rapport["timestamp"])
                
        return min(timestamps) if timestamps else datetime.now().isoformat()
        
    def calculer_duree_mission(self, rapports: Dict[str, Any]) -> str:
        """Calcule la dure de la mission"""
        try:
            debut = datetime.fromisoformat(self.extraire_timestamp_debut(rapports))
            fin = datetime.now()
            duree = fin - debut
            return str(duree)
        except:
            return "Non calculable"
            
    def evaluer_statut_mission(self, etat_final: Dict[str, Any], resultats_tests: Dict[str, Any]) -> str:
        """value le statut global de la mission"""
        nb_outils = len(etat_final["outils_restructures"])
        structures_valides = len([s for s in etat_final["structure_validee"].values() if s["statut"] == "VALIDE"])
        
        if nb_outils == 0:
            return "ECHEC"
        elif structures_valides == nb_outils:
            return "REUSSI"
        elif structures_valides > nb_outils * 0.7:
            return "LARGEMENT_REUSSI"
        elif structures_valides > nb_outils * 0.5:
            return "PARTIELLEMENT_REUSSI"
        else:
            return "ECHEC_PARTIEL"
            
    def calculer_taux_reussite(self, validations: Dict[str, Any]) -> float:
        """Calcule le taux de russite d'un ensemble de validations"""
        if not validations:
            return 0.0
            
        scores = [v["score"] for v in validations.values() if "score" in v]
        return sum(scores) / len(scores) if scores else 0.0
        
    def calculer_taux_reussite_tests(self, resultats_tests: Dict[str, Any]) -> float:
        """Calcule le taux de russite des tests"""
        total_executes = (resultats_tests["tests_unitaires"]["executes"] + 
                         resultats_tests["tests_integration"]["executes"])
        total_reussis = (resultats_tests["tests_unitaires"]["reussis"] + 
                        resultats_tests["tests_integration"]["reussis"])
        
        return (total_reussis / total_executes * 100) if total_executes > 0 else 0.0
        
    def sauvegarder_rapport_final(self, rapport: Dict[str, Any]) -> None:
        """Sauvegarde le rapport final"""
        # Rapport JSON dtaill
        rapport_json = self.logs_path / f"{self.agent_id}_MISSION_COMPLETE.json"
        with open(rapport_json, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
            
        # Rapport texte lisible
        rapport_txt = self.logs_path / f"{self.agent_id}_MISSION_RESUME.md"
        with open(rapport_txt, 'w', encoding='utf-8') as f:
            f.write(self.generer_resume_markdown(rapport))
            
        self.logger.info(f"[CHART] Rapport final sauvegard: {rapport_json}")
        self.logger.info(f"[DOCUMENT] Rsum sauvegard: {rapport_txt}")
        
    def generer_resume_markdown(self, rapport: Dict[str, Any]) -> str:
        """Gnre un rsum en format Markdown"""
        return f"""# Mission Rorganisation Outils NextGeneration - Rapport Final

## [TARGET] Rsum Excutif

**ID Mission**: {rapport['mission_info']['id']}  
**Dbut**: {rapport['mission_info']['timestamp_debut']}  
**Fin**: {rapport['mission_info']['timestamp_fin']}  
**Dure**: {rapport['mission_info']['duree_mission']}

**Statut Mission**: **{rapport['evaluation_globale']['statut_mission']}**

## [CHART] Rsultats Cls

- **Outils traits**: {rapport['summary_execution']['outils_traites']}
- **Structures cres**: {rapport['summary_execution']['structures_creees']}
- **Documentation complte**: {rapport['summary_execution']['documentation_complete']}
- **Tests disponibles**: {rapport['summary_execution']['tests_disponibles']}

##  Taux de Russite

- **Structure**: {rapport['evaluation_globale']['taux_reussite_structure']:.1f}%
- **Documentation**: {rapport['evaluation_globale']['taux_reussite_documentation']:.1f}%
- **Tests**: {rapport['evaluation_globale']['taux_reussite_tests']:.1f}%

##  Agents Excuts

{chr(10).join(f'- {agent}' for agent in rapport['summary_execution']['agents_executes'])}

## [BULB] Recommandations

{chr(10).join(f'- {rec}' for rec in rapport['recommandations'])}

## [ROCKET] Prochaines tapes

{chr(10).join(f'- {etape}' for etape in rapport['prochaines_etapes'])}

---
*Rapport gnr automatiquement par l'quipe d'agents NextGeneration*
"""

if __name__ == "__main__":
    agent = AgentRapportFinal()
    rapport = agent.generer_rapport_final_complet()
    
    print(f"\n[CLIPBOARD] RAPPORT FINAL DE MISSION")
    print(f"=" * 50)
    print(f"[TARGET] Statut: {rapport['evaluation_globale']['statut_mission']}")
    print(f"[TOOL] Outils traits: {rapport['summary_execution']['outils_traites']}")
    print(f"[FOLDER] Structures: {rapport['evaluation_globale']['taux_reussite_structure']:.1f}%")
    print(f" Documentation: {rapport['evaluation_globale']['taux_reussite_documentation']:.1f}%")
    print(f" Tests: {rapport['evaluation_globale']['taux_reussite_tests']:.1f}%")
    print(f"[BULB] Recommandations: {len(rapport['recommandations'])}")
    print(f"=" * 50) 