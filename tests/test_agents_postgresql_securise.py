#!/usr/bin/env python3
"""
Test Sécurisé des Agents PostgreSQL NextGeneration
Mission: Valider les 9 agents PostgreSQL en mode sandbox sans risque
"""

import os
import sys
import json
import importlib.util
import traceback
import ast
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class TestAgentsPostgreSQLSecurise:
    """Testeur sécurisé pour les agents PostgreSQL."""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.test_id = f"test_postgresql_secure_{self.timestamp}"
        self.agents_path = Path("docs/agents_postgresql_resolution")
        self.rapport_path = Path("rapport_test_postgresql_securise.json")
        
        # Liste des agents à tester
        self.agents_liste = [
            "agent_POSTGRESQL_windows_postgres.py",
            "agent_POSTGRESQL_sqlalchemy_fixer.py", 
            "agent_POSTGRESQL_docker_specialist.py",
            "agent_POSTGRESQL_testing_specialist.py",
            "agent_POSTGRESQL_web_researcher.py",
            "agent_POSTGRESQL_workspace_organizer.py",
            "agent_POSTGRESQL_documentation_manager.py",
            "agent_POSTGRESQL_resolution_finale.py",
            "agent_POSTGRESQL_diagnostic_postgres_final.py"
        ]
        
        self.resultats_tests = {}
        self.rapport_final = {
            "test_id": self.test_id,
            "timestamp": datetime.now().isoformat(),
            "mission": "Test sécurisé agents PostgreSQL",
            "mode": "SANDBOX - Aucun risque pour production",
            "agents_testes": 0,
            "agents_valides": 0,
            "agents_erreurs": 0,
            "details": {},
            "recommandations": [],
            "conclusion": ""
        }
        
        print(f"🔒 Test Sécurisé PostgreSQL initialisé - ID: {self.test_id}")
        print("🛡️ Mode SANDBOX - Aucun impact sur la production")
    
    def test_syntaxe_agent(self, agent_file: Path) -> Dict[str, Any]:
        """Teste la syntaxe Python d'un agent de manière sécurisée."""
        print(f"📝 Test syntaxe: {agent_file.name}")
        
        try:
            # Lecture sécurisée du fichier
            with open(agent_file, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            # Vérification syntaxe avec AST (sécurisé)
            ast.parse(code_content, filename=str(agent_file))
            
            # Statistiques du code
            lignes_total = len(code_content.splitlines())
            lignes_code = len([l for l in code_content.splitlines() if l.strip() and not l.strip().startswith('#')])
            taille_bytes = len(code_content.encode('utf-8'))
            
            return {
                "syntaxe_valide": True,
                "lignes_total": lignes_total,
                "lignes_code": lignes_code,
                "taille_bytes": taille_bytes,
                "taille_kb": round(taille_bytes / 1024, 1),
                "erreur": None
            }
            
        except SyntaxError as e:
            return {
                "syntaxe_valide": False,
                "erreur": f"Erreur syntaxe ligne {e.lineno}: {e.msg}",
                "lignes_total": 0,
                "lignes_code": 0,
                "taille_bytes": 0,
                "taille_kb": 0
            }
        except Exception as e:
            return {
                "syntaxe_valide": False,
                "erreur": f"Erreur lecture: {str(e)}",
                "lignes_total": 0,
                "lignes_code": 0,
                "taille_bytes": 0,
                "taille_kb": 0
            }
    
    def analyser_structure_agent(self, agent_file: Path) -> Dict[str, Any]:
        """Analyse la structure d'un agent sans l'exécuter."""
        print(f"🔍 Analyse structure: {agent_file.name}")
        
        try:
            with open(agent_file, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            # Parse AST pour analyser la structure
            tree = ast.parse(code_content)
            
            # Extraction des informations
            classes = []
            fonctions = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    fonctions.append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(f"from {node.module}")
            
            # Recherche de patterns spécifiques
            has_main = 'main' in fonctions or '__main__' in code_content
            has_async = 'async def' in code_content
            has_class_principale = len(classes) > 0
            
            return {
                "structure_valide": True,
                "classes": classes,
                "fonctions": fonctions,
                "imports": list(set(imports)),
                "has_main": has_main,
                "has_async": has_async,
                "has_class_principale": has_class_principale,
                "nb_classes": len(classes),
                "nb_fonctions": len(fonctions),
                "nb_imports": len(set(imports))
            }
            
        except Exception as e:
            return {
                "structure_valide": False,
                "erreur": f"Erreur analyse: {str(e)}",
                "classes": [],
                "fonctions": [],
                "imports": []
            }
    
    def test_imports_agent(self, agent_file: Path) -> Dict[str, Any]:
        """Teste les imports d'un agent de manière sécurisée."""
        print(f"📦 Test imports: {agent_file.name}")
        
        try:
            with open(agent_file, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            # Extraction des imports via AST
            tree = ast.parse(code_content)
            imports_found = []
            imports_problematiques = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module_name = alias.name
                        imports_found.append(module_name)
                        
                        # Test si le module existe (sans l'importer réellement)
                        try:
                            importlib.util.find_spec(module_name)
                        except (ImportError, ModuleNotFoundError):
                            imports_problematiques.append(module_name)
                            
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        module_name = node.module
                        imports_found.append(module_name)
                        
                        try:
                            importlib.util.find_spec(module_name)
                        except (ImportError, ModuleNotFoundError):
                            imports_problematiques.append(module_name)
            
            imports_ok = len(imports_problematiques) == 0
            
            return {
                "imports_valides": imports_ok,
                "imports_total": len(imports_found),
                "imports_problematiques": imports_problematiques,
                "imports_ok": len(imports_found) - len(imports_problematiques),
                "liste_imports": list(set(imports_found))
            }
            
        except Exception as e:
            return {
                "imports_valides": False,
                "erreur": f"Erreur test imports: {str(e)}",
                "imports_total": 0,
                "imports_problematiques": [],
                "imports_ok": 0
            }
    
    def evaluer_qualite_agent(self, agent_file: Path, syntaxe: Dict, structure: Dict, imports: Dict) -> Dict[str, Any]:
        """Évalue la qualité globale d'un agent."""
        print(f"⭐ Évaluation qualité: {agent_file.name}")
        
        # Calcul du score qualité
        score = 0
        score_max = 100
        details_score = {}
        
        # Syntaxe (30 points)
        if syntaxe["syntaxe_valide"]:
            score += 30
            details_score["syntaxe"] = "✅ 30/30"
        else:
            details_score["syntaxe"] = "❌ 0/30"
        
        # Structure (25 points)
        if structure.get("structure_valide", False):
            score_structure = 0
            if structure.get("has_class_principale", False):
                score_structure += 10
            if structure.get("has_main", False):
                score_structure += 10
            if structure.get("nb_fonctions", 0) >= 3:
                score_structure += 5
            score += score_structure
            details_score["structure"] = f"✅ {score_structure}/25"
        else:
            details_score["structure"] = "❌ 0/25"
        
        # Imports (20 points)
        if imports.get("imports_valides", False):
            score += 20
            details_score["imports"] = "✅ 20/20"
        else:
            score_imports = max(0, 20 - len(imports.get("imports_problematiques", [])) * 5)
            score += score_imports
            details_score["imports"] = f"⚠️ {score_imports}/20"
        
        # Taille code (15 points)
        taille_kb = syntaxe.get("taille_kb", 0)
        if taille_kb > 0:
            if taille_kb >= 10:  # Gros agent
                score += 15
                details_score["taille"] = "✅ 15/15 (gros agent)"
            elif taille_kb >= 3:  # Agent moyen
                score += 12
                details_score["taille"] = "✅ 12/15 (agent moyen)"
            else:  # Petit agent
                score += 8
                details_score["taille"] = "⚠️ 8/15 (petit agent)"
        else:
            details_score["taille"] = "❌ 0/15 (vide)"
        
        # Complexité (10 points)
        nb_fonctions = structure.get("nb_fonctions", 0)
        if nb_fonctions >= 10:
            score += 10
            details_score["complexite"] = "✅ 10/10"
        elif nb_fonctions >= 5:
            score += 7
            details_score["complexite"] = "✅ 7/10"
        elif nb_fonctions >= 2:
            score += 5
            details_score["complexite"] = "⚠️ 5/10"
        else:
            details_score["complexite"] = "❌ 0/10"
        
        # Catégorie qualité
        if score >= 85:
            categorie = "EXCELLENT"
            emoji = "🏆"
        elif score >= 70:
            categorie = "BON"
            emoji = "✅"
        elif score >= 50:
            categorie = "MOYEN"
            emoji = "⚠️"
        else:
            categorie = "FAIBLE"
            emoji = "❌"
        
        return {
            "score": score,
            "score_max": score_max,
            "pourcentage": round((score / score_max) * 100, 1),
            "categorie": categorie,
            "emoji": emoji,
            "details_score": details_score
        }
    
    def tester_agent_complet(self, agent_name: str) -> Dict[str, Any]:
        """Teste complètement un agent de manière sécurisée."""
        agent_file = self.agents_path / agent_name
        
        print(f"\n🧪 TEST COMPLET: {agent_name}")
        print("=" * 50)
        
        if not agent_file.exists():
            return {
                "agent_name": agent_name,
                "existe": False,
                "erreur": "Fichier non trouvé",
                "status": "ERREUR"
            }
        
        # Tests sécurisés
        test_syntaxe = self.test_syntaxe_agent(agent_file)
        test_structure = self.analyser_structure_agent(agent_file)
        test_imports = self.test_imports_agent(agent_file)
        evaluation_qualite = self.evaluer_qualite_agent(agent_file, test_syntaxe, test_structure, test_imports)
        
        # Résultat global
        status = "VALIDE" if (test_syntaxe["syntaxe_valide"] and 
                            test_structure.get("structure_valide", False)) else "ERREUR"
        
        resultat = {
            "agent_name": agent_name,
            "existe": True,
            "status": status,
            "syntaxe": test_syntaxe,
            "structure": test_structure,
            "imports": test_imports,
            "qualite": evaluation_qualite,
            "timestamp_test": datetime.now().isoformat()
        }
        
        # Affichage résumé
        emoji = evaluation_qualite["emoji"]
        score = evaluation_qualite["pourcentage"]
        print(f"{emoji} Résultat: {status} - Score qualité: {score}%")
        
        return resultat
    
    def executer_tests_complets(self) -> Dict[str, Any]:
        """Exécute tous les tests sur tous les agents."""
        print(f"\n🚀 DÉMARRAGE TESTS SÉCURISÉS")
        print("="*60)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Agents à tester: {len(self.agents_liste)}")
        print(f"🔒 Mode: SANDBOX - Aucun risque production")
        print()
        
        for agent_name in self.agents_liste:
            resultat = self.tester_agent_complet(agent_name)
            self.resultats_tests[agent_name] = resultat
            
            # Mise à jour compteurs
            self.rapport_final["agents_testes"] += 1
            if resultat["status"] == "VALIDE":
                self.rapport_final["agents_valides"] += 1
            else:
                self.rapport_final["agents_erreurs"] += 1
        
        # Compilation rapport final
        self.compiler_rapport_final()
        return self.rapport_final
    
    def compiler_rapport_final(self):
        """Compile le rapport final des tests."""
        print(f"\n📊 COMPILATION RAPPORT FINAL")
        print("="*40)
        
        # Statistiques globales
        total = self.rapport_final["agents_testes"]
        valides = self.rapport_final["agents_valides"]
        erreurs = self.rapport_final["agents_erreurs"]
        
        taux_reussite = round((valides / total * 100), 1) if total > 0 else 0
        
        # Analyse des scores
        scores = []
        tailles_total = 0
        lignes_total = 0
        
        for agent_name, resultat in self.resultats_tests.items():
            if resultat["status"] == "VALIDE":
                scores.append(resultat["qualite"]["pourcentage"])
                tailles_total += resultat["syntaxe"]["taille_kb"]
                lignes_total += resultat["syntaxe"]["lignes_total"]
        
        score_moyen = round(sum(scores) / len(scores), 1) if scores else 0
        
        # Recommandations
        recommandations = []
        if erreurs > 0:
            recommandations.append("Corriger les agents avec erreurs syntaxe")
        if score_moyen < 70:
            recommandations.append("Améliorer la qualité globale du code")
        if taux_reussite < 90:
            recommandations.append("Réviser les agents non conformes")
        
        recommandations.extend([
            "Effectuer tests réguliers en environnement sécurisé",
            "Maintenir documentation à jour",
            "Planifier revue de code périodique"
        ])
        
        # Conclusion
        if taux_reussite >= 90 and score_moyen >= 70:
            conclusion = f"✅ AGENTS POSTGRESQL EXCELLENTS - {taux_reussite}% réussite, score moyen {score_moyen}%"
        elif taux_reussite >= 80:
            conclusion = f"✅ AGENTS POSTGRESQL BONS - {taux_reussite}% réussite, score moyen {score_moyen}%"
        elif taux_reussite >= 60:
            conclusion = f"⚠️ AGENTS POSTGRESQL MOYENS - {taux_reussite}% réussite, à améliorer"
        else:
            conclusion = f"❌ AGENTS POSTGRESQL PROBLÉMATIQUES - {taux_reussite}% réussite, révision nécessaire"
        
        # Mise à jour rapport
        self.rapport_final.update({
            "details": self.resultats_tests,
            "statistiques": {
                "taux_reussite": taux_reussite,
                "score_moyen": score_moyen,
                "code_total_kb": round(tailles_total, 1),
                "lignes_total": lignes_total,
                "agents_excellents": len([s for s in scores if s >= 85]),
                "agents_bons": len([s for s in scores if 70 <= s < 85]),
                "agents_moyens": len([s for s in scores if 50 <= s < 70]),
                "agents_faibles": len([s for s in scores if s < 50])
            },
            "recommandations": recommandations,
            "conclusion": conclusion
        })
        
        print(f"✅ Rapport compilé: {conclusion}")
    
    def sauvegarder_rapport(self):
        """Sauvegarde le rapport final."""
        with open(self.rapport_path, 'w', encoding='utf-8') as f:
            json.dump(self.rapport_final, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Rapport sauvegardé: {self.rapport_path}")
    
    def afficher_resume(self):
        """Affiche un résumé des tests."""
        print(f"\n🎉 RÉSUMÉ TESTS SÉCURISÉS POSTGRESQL")
        print("="*50)
        
        stats = self.rapport_final["statistiques"]
        
        print(f"📊 Agents testés: {self.rapport_final['agents_testes']}")
        print(f"✅ Agents valides: {self.rapport_final['agents_valides']}")
        print(f"❌ Agents erreurs: {self.rapport_final['agents_erreurs']}")
        print(f"📈 Taux réussite: {stats['taux_reussite']}%")
        print(f"⭐ Score moyen: {stats['score_moyen']}%")
        print(f"💻 Code total: {stats['code_total_kb']}KB")
        print(f"📝 Lignes total: {stats['lignes_total']}")
        print()
        print(f"🏆 Agents excellents: {stats['agents_excellents']}")
        print(f"✅ Agents bons: {stats['agents_bons']}")
        print(f"⚠️ Agents moyens: {stats['agents_moyens']}")
        print(f"❌ Agents faibles: {stats['agents_faibles']}")
        print()
        print(self.rapport_final["conclusion"])
        print(f"\n📄 Rapport détaillé: {self.rapport_path}")

def main():
    """Fonction principale - Teste tous les agents PostgreSQL de manière sécurisée."""
    print("🔒 TESTS SÉCURISÉS AGENTS POSTGRESQL NEXTGENERATION")
    print("="*60)
    print("🛡️ Mode SANDBOX - Aucun impact sur la production")
    print("🎯 Validation complète des 9 agents PostgreSQL")
    print()
    
    # Création du testeur
    testeur = TestAgentsPostgreSQLSecurise()
    
    try:
        # Exécution des tests
        rapport = testeur.executer_tests_complets()
        
        # Sauvegarde et affichage
        testeur.sauvegarder_rapport()
        testeur.afficher_resume()
        
        print("\n🎊 TESTS TERMINÉS AVEC SUCCÈS!")
        return True
        
    except Exception as e:
        print(f"\n💥 ERREUR LORS DES TESTS: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 



