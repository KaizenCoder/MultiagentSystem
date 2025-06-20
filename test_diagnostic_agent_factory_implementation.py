#!/usr/bin/env python3
"""
🔍 DIAGNOSTIC AGENTS - AGENT FACTORY IMPLEMENTATION
Analyse complète des agents présents dans C:\\Dev\\nextgeneration\\agent_factory_implementation
MODE DIAGNOSTIC UNIQUEMENT - AUCUNE MODIFICATION AUTORISÉE

Utilise l'équipe de maintenance adaptée pour analyser la compatibilité TemplateManager
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime
import json
import traceback
import importlib.util

# Ajouter le répertoire des agents de maintenance au path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import des agents de maintenance adaptés
try:
    from agent_1_analyseur_structure import Agent1AnalyseurStructure
    from agent_2_evaluateur_utilite import Agent2EvaluateurUtilite
    from agent_3_adaptateur_code import Agent3AdaptateurCode
    from agent_4_testeur_integration import Agent4TesteurIntegration
    from agent_5_documenteur import Agent5Documenteur
    from agent_6_validateur_final import Agent6ValidateurFinal
    from agent_0_chef_equipe_coordinateur import Agent0ChefEquipeCoordinateur
    from chef_equipe_pattern_factory import ChefEquipePatternFactory
    from coordinateur_equipe_tools import CoordinateurEquipeTools
    print("✅ Équipe de maintenance chargée avec succès")
except Exception as e:
    print(f"❌ Erreur chargement équipe maintenance: {e}")
    sys.exit(1)

class DiagnosticAgentFactory:
    """Diagnostic complet des agents dans agent_factory_implementation"""
    
    def __init__(self):
        self.target_dir = Path("../agent_factory_implementation")
        self.rapport_diagnostic = {
            "timestamp": datetime.now().isoformat(),
            "target_directory": str(self.target_dir.absolute()),
            "agents_detectes": [],
            "analyse_structure": {},
            "evaluation_utilite": {},
            "compatibilite_templatemanager": {},
            "recommandations": [],
            "statistiques": {}
        }
        
        # Initialisation équipe maintenance
        self.analyseur = Agent1AnalyseurStructure()
        self.evaluateur = Agent2EvaluateurUtilite()
        self.coordinateur = Agent0ChefEquipeCoordinateur()
        
    async def executer_diagnostic_complet(self):
        """Exécute le diagnostic complet des agents"""
        print("🔍 DÉBUT DIAGNOSTIC AGENT FACTORY IMPLEMENTATION")
        print("=" * 60)
        
        try:
            # 1. Découverte des agents
            await self._decouvrir_agents()
            
            # 2. Analyse structure de chaque agent
            await self._analyser_structure_agents()
            
            # 3. Évaluation utilité et compatibilité
            await self._evaluer_agents()
            
            # 4. Test compatibilité TemplateManager
            await self._tester_compatibilite_templatemanager()
            
            # 5. Génération recommandations
            await self._generer_recommandations()
            
            # 6. Sauvegarde rapport
            await self._sauvegarder_rapport()
            
            # 7. Affichage résumé
            self._afficher_resume()
            
        except Exception as e:
            print(f"❌ Erreur durant diagnostic: {e}")
            traceback.print_exc()
    
    async def _decouvrir_agents(self):
        """Découvre tous les agents dans le répertoire cible"""
        print("📂 Découverte des agents...")
        
        agents_trouves = []
        
        # Parcours récursif du répertoire
        for py_file in self.target_dir.rglob("*.py"):
            if py_file.name.startswith("agent_") or "agent" in py_file.name.lower():
                try:
                    # Analyse basique du fichier
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Détection des classes d'agents
                    classes_detectees = []
                    for line in content.split('\n'):
                        if 'class ' in line and ('Agent' in line or 'agent' in line.lower()):
                            class_name = line.split('class ')[1].split('(')[0].split(':')[0].strip()
                            classes_detectees.append(class_name)
                    
                    if classes_detectees:
                        agent_info = {
                            "fichier": str(py_file.relative_to(self.target_dir.parent)),
                            "nom_fichier": py_file.name,
                            "taille": py_file.stat().st_size,
                            "lignes": len(content.split('\n')),
                            "classes_detectees": classes_detectees,
                            "derniere_modification": datetime.fromtimestamp(py_file.stat().st_mtime).isoformat(),
                            "analyse_preliminaire": {
                                "contient_async": "async " in content,
                                "contient_templatemanager": "TemplateManager" in content or "template_manager" in content,
                                "contient_factory": "Factory" in content or "factory" in content.lower(),
                                "contient_pattern": "Pattern" in content or "pattern" in content.lower(),
                                "imports_detectes": len([l for l in content.split('\n') if l.strip().startswith('import ') or l.strip().startswith('from ')])
                            }
                        }
                        agents_trouves.append(agent_info)
                        
                except Exception as e:
                    print(f"⚠️ Erreur analyse {py_file}: {e}")
        
        self.rapport_diagnostic["agents_detectes"] = agents_trouves
        print(f"✅ {len(agents_trouves)} agents détectés")
        
        for agent in agents_trouves:
            print(f"  📁 {agent['nom_fichier']} - {len(agent['classes_detectees'])} classes")
    
    async def _analyser_structure_agents(self):
        """Analyse la structure de chaque agent détecté"""
        print("\n🔍 Analyse structure des agents...")
        
        analyses = {}
        
        for agent_info in self.rapport_diagnostic["agents_detectes"]:
            try:
                print(f"  📊 Analyse {agent_info['nom_fichier']}...")
                
                # Utilisation de l'Agent 1 pour analyser la structure
                fichier_path = Path(agent_info["fichier"])
                
                if fichier_path.exists():
                    analyse = await self.analyseur.analyser_structure_agent(str(fichier_path))
                    analyses[agent_info['nom_fichier']] = {
                        "analyse_reussie": True,
                        "resultats": analyse,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    analyses[agent_info['nom_fichier']] = {
                        "analyse_reussie": False,
                        "erreur": "Fichier non trouvé",
                        "timestamp": datetime.now().isoformat()
                    }
                    
            except Exception as e:
                analyses[agent_info['nom_fichier']] = {
                    "analyse_reussie": False,
                    "erreur": str(e),
                    "timestamp": datetime.now().isoformat()
                }
        
        self.rapport_diagnostic["analyse_structure"] = analyses
        print(f"✅ Analyse structure complétée pour {len(analyses)} agents")
    
    async def _evaluer_agents(self):
        """Évalue l'utilité et la qualité des agents"""
        print("\n📈 Évaluation utilité des agents...")
        
        evaluations = {}
        
        for agent_info in self.rapport_diagnostic["agents_detectes"]:
            try:
                print(f"  🎯 Évaluation {agent_info['nom_fichier']}...")
                
                # Utilisation de l'Agent 2 pour évaluer l'utilité
                structure_analyse = self.rapport_diagnostic["analyse_structure"].get(
                    agent_info['nom_fichier'], {}
                ).get("resultats", {})
                
                if structure_analyse:
                    evaluation = await self.evaluateur.evaluer_utilite_agent(
                        agent_info, structure_analyse
                    )
                    evaluations[agent_info['nom_fichier']] = {
                        "evaluation_reussie": True,
                        "resultats": evaluation,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    evaluations[agent_info['nom_fichier']] = {
                        "evaluation_reussie": False,
                        "erreur": "Pas d'analyse structure disponible",
                        "timestamp": datetime.now().isoformat()
                    }
                    
            except Exception as e:
                evaluations[agent_info['nom_fichier']] = {
                    "evaluation_reussie": False,
                    "erreur": str(e),
                    "timestamp": datetime.now().isoformat()
                }
        
        self.rapport_diagnostic["evaluation_utilite"] = evaluations
        print(f"✅ Évaluation complétée pour {len(evaluations)} agents")
    
    async def _tester_compatibilite_templatemanager(self):
        """Teste la compatibilité avec TemplateManager"""
        print("\n🔧 Test compatibilité TemplateManager...")
        
        compatibilites = {}
        
        for agent_info in self.rapport_diagnostic["agents_detectes"]:
            try:
                print(f"  🧪 Test compatibilité {agent_info['nom_fichier']}...")
                
                fichier_path = Path(agent_info["fichier"])
                
                # Test de compatibilité basique
                compatibilite = {
                    "fichier_accessible": fichier_path.exists(),
                    "contient_interfaces_templatemanager": False,
                    "contient_factory_function": False,
                    "signature_compatible": False,
                    "methodes_requises": {
                        "startup": False,
                        "shutdown": False,
                        "health_check": False,
                        "execute_task": False
                    },
                    "score_compatibilite": 0
                }
                
                if fichier_path.exists():
                    with open(fichier_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Vérifications compatibilité
                    if "async def startup" in content:
                        compatibilite["methodes_requises"]["startup"] = True
                        compatibilite["score_compatibilite"] += 25
                    
                    if "async def shutdown" in content:
                        compatibilite["methodes_requises"]["shutdown"] = True
                        compatibilite["score_compatibilite"] += 25
                    
                    if "async def health_check" in content:
                        compatibilite["methodes_requises"]["health_check"] = True
                        compatibilite["score_compatibilite"] += 25
                    
                    if "async def execute_task" in content:
                        compatibilite["methodes_requises"]["execute_task"] = True
                        compatibilite["score_compatibilite"] += 25
                    
                    if "def create_" in content:
                        compatibilite["contient_factory_function"] = True
                    
                    if "agent_id" in content and "agent_type" in content:
                        compatibilite["signature_compatible"] = True
                    
                    if "TemplateManager" in content:
                        compatibilite["contient_interfaces_templatemanager"] = True
                
                compatibilites[agent_info['nom_fichier']] = {
                    "test_reussi": True,
                    "compatibilite": compatibilite,
                    "timestamp": datetime.now().isoformat()
                }
                
            except Exception as e:
                compatibilites[agent_info['nom_fichier']] = {
                    "test_reussi": False,
                    "erreur": str(e),
                    "timestamp": datetime.now().isoformat()
                }
        
        self.rapport_diagnostic["compatibilite_templatemanager"] = compatibilites
        print(f"✅ Test compatibilité complété pour {len(compatibilites)} agents")
    
    async def _generer_recommandations(self):
        """Génère des recommandations basées sur l'analyse"""
        print("\n💡 Génération recommandations...")
        
        recommandations = []
        stats = {
            "total_agents": len(self.rapport_diagnostic["agents_detectes"]),
            "agents_compatibles": 0,
            "agents_partiellement_compatibles": 0,
            "agents_incompatibles": 0,
            "score_moyen_compatibilite": 0
        }
        
        scores_compatibilite = []
        
        for agent_name, compat_info in self.rapport_diagnostic["compatibilite_templatemanager"].items():
            if compat_info.get("test_reussi", False):
                score = compat_info["compatibilite"]["score_compatibilite"]
                scores_compatibilite.append(score)
                
                if score >= 75:
                    stats["agents_compatibles"] += 1
                elif score >= 25:
                    stats["agents_partiellement_compatibles"] += 1
                else:
                    stats["agents_incompatibles"] += 1
                
                # Recommandations spécifiques
                if score < 100:
                    manquantes = []
                    for methode, presente in compat_info["compatibilite"]["methodes_requises"].items():
                        if not presente:
                            manquantes.append(methode)
                    
                    if manquantes:
                        recommandations.append({
                            "agent": agent_name,
                            "type": "methodes_manquantes",
                            "priorite": "HAUTE" if score < 25 else "MOYENNE",
                            "description": f"Méthodes TemplateManager manquantes: {', '.join(manquantes)}",
                            "action_recommandee": f"Implémenter les méthodes async: {', '.join(manquantes)}"
                        })
        
        if scores_compatibilite:
            stats["score_moyen_compatibilite"] = sum(scores_compatibilite) / len(scores_compatibilite)
        
        # Recommandations générales
        if stats["agents_incompatibles"] > 0:
            recommandations.append({
                "type": "adaptation_generale",
                "priorite": "CRITIQUE",
                "description": f"{stats['agents_incompatibles']} agents nécessitent une adaptation complète",
                "action_recommandee": "Utiliser l'équipe de maintenance pour adapter ces agents au TemplateManager"
            })
        
        if stats["agents_partiellement_compatibles"] > 0:
            recommandations.append({
                "type": "amelioration_partielle",
                "priorite": "HAUTE",
                "description": f"{stats['agents_partiellement_compatibles']} agents nécessitent des améliorations",
                "action_recommandee": "Compléter les interfaces TemplateManager manquantes"
            })
        
        self.rapport_diagnostic["recommandations"] = recommandations
        self.rapport_diagnostic["statistiques"] = stats
        print(f"✅ {len(recommandations)} recommandations générées")
    
    async def _sauvegarder_rapport(self):
        """Sauvegarde le rapport de diagnostic"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        rapport_file = f"diagnostic_agent_factory_implementation_{timestamp}.json"
        
        try:
            with open(rapport_file, 'w', encoding='utf-8') as f:
                json.dump(self.rapport_diagnostic, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Rapport sauvegardé: {rapport_file}")
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde rapport: {e}")
    
    def _afficher_resume(self):
        """Affiche le résumé du diagnostic"""
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DIAGNOSTIC AGENT FACTORY IMPLEMENTATION")
        print("=" * 60)
        
        stats = self.rapport_diagnostic["statistiques"]
        
        print(f"📁 Répertoire analysé: {self.rapport_diagnostic['target_directory']}")
        print(f"🕒 Timestamp: {self.rapport_diagnostic['timestamp']}")
        print()
        
        print("📈 STATISTIQUES AGENTS:")
        print(f"  • Total agents détectés: {stats['total_agents']}")
        print(f"  • Agents compatibles (≥75%): {stats['agents_compatibles']}")
        print(f"  • Agents partiellement compatibles (25-74%): {stats['agents_partiellement_compatibles']}")
        print(f"  • Agents incompatibles (<25%): {stats['agents_incompatibles']}")
        print(f"  • Score moyen compatibilité: {stats['score_moyen_compatibilite']:.1f}%")
        print()
        
        print("🎯 AGENTS DÉTECTÉS:")
        for agent in self.rapport_diagnostic["agents_detectes"]:
            compat_info = self.rapport_diagnostic["compatibilite_templatemanager"].get(agent['nom_fichier'], {})
            if compat_info.get("test_reussi", False):
                score = compat_info["compatibilite"]["score_compatibilite"]
                status = "✅" if score >= 75 else "⚠️" if score >= 25 else "❌"
                print(f"  {status} {agent['nom_fichier']} - {score}% compatible")
                print(f"     Classes: {', '.join(agent['classes_detectees'])}")
                print(f"     Taille: {agent['taille']} bytes, {agent['lignes']} lignes")
            else:
                print(f"  ❓ {agent['nom_fichier']} - Erreur test compatibilité")
        print()
        
        print("💡 RECOMMANDATIONS PRINCIPALES:")
        for i, rec in enumerate(self.rapport_diagnostic["recommandations"][:5], 1):
            priorite_icon = "🔴" if rec["priorite"] == "CRITIQUE" else "🟡" if rec["priorite"] == "HAUTE" else "🟢"
            print(f"  {i}. {priorite_icon} {rec['description']}")
            print(f"     Action: {rec['action_recommandee']}")
        
        if len(self.rapport_diagnostic["recommandations"]) > 5:
            print(f"     ... et {len(self.rapport_diagnostic['recommandations']) - 5} autres recommandations")
        
        print("\n" + "=" * 60)
        print("🎯 DIAGNOSTIC TERMINÉ - MODE LECTURE SEULE RESPECTÉ")
        print("=" * 60)

async def main():
    """Point d'entrée principal"""
    diagnostic = DiagnosticAgentFactory()
    await diagnostic.executer_diagnostic_complet()

if __name__ == "__main__":
    asyncio.run(main()) 