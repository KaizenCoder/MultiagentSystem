#!/usr/bin/env python3
"""
🎖️ Agent 0 - Chef d'Équipe Coordinateur
Modèle: Claude Sonnet 4 
Mission: Orchestration centrale de l'équipe de maintenance
Équipe: NextGeneration Tools Migration

Standardisation Pattern Factory:
- Nomenclature agent_0_chef_equipe_coordinateur.py
- Coordination des agents 1-6
- Interface unique pour toutes les tâches
- Workflows automatisés et rapports consolidés
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class Agent0ChefEquipeCoordinateur:
    """Agent 0 - Chef d'Équipe Coordinateur avec Claude Sonnet 4"""
    
    def __init__(self, agent_id: str = None, agent_type: str = "chef_equipe_coordinateur", target_path: str = None, workspace_path: str = None, **config):
        # Configuration TemplateManager
        self.agent_id = agent_id or f"agent_0_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.agent_type = agent_type
        self.config = config
        self.logger = logging.getLogger("Agent0ChefEquipe")
        
        # Configuration équipe
        self.target_path = Path(target_path) if target_path else Path("../agent_factory_implementation/agents")
        self.workspace_path = Path(workspace_path) if workspace_path else Path(".")
        self.equipe_agents = {}
        
        # Workflows disponibles
        self.workflows_disponibles = [
            "analyser_equipe_complete",
            "evaluer_utilite_equipe", 
            "adapter_code_agents",
            "tester_integration",
            "documenter_equipe",
            "validation_finale",
            "maintenance_complete"
        ]
        
        # Configuration workflows
        self.config_workflows = {
            "timeout_default": config.get("timeout", 300),
            "safe_mode": config.get("safe_mode", True),
            "max_agents_parallel": config.get("max_agents_parallel", 6),
            "rapport_detaille": config.get("rapport_detaille", True)
        }
        
        self.logger.info(f"🎖️ Agent 0 Chef d'Équipe Coordinateur initialisé - ID: {self.agent_id}")
        
    async def execute_task(self, task_config: Dict = None) -> Dict[str, Any]:
        """Exécuter la tâche principale - Interface TemplateManager"""
        return await self.workflow_maintenance_complete()
        
    async def startup(self):
        """Démarrage Agent 0 Chef d'Équipe"""
        self.logger.info(f"🚀 Agent 0 Chef d'Équipe {self.agent_id} - DÉMARRAGE")
        
        # Vérification des chemins
        if not self.target_path.exists():
            self.logger.warning(f"⚠️ Chemin cible non trouvé: {self.target_path}")
            self.target_path.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"✅ Configuration Chef d'Équipe:")
        self.logger.info(f"   - Target: {self.target_path}")
        self.logger.info(f"   - Workspace: {self.workspace_path}")
        self.logger.info(f"   - Workflows: {len(self.workflows_disponibles)} disponibles")
        
        # Initialisation équipe agents (lazy loading)
        self.logger.info("✅ Chef d'Équipe prêt à coordonner l'équipe")
        return {"status": "started", "agent_id": self.agent_id}
        
    async def shutdown(self):
        """Arrêt Agent 0 Chef d'Équipe"""
        self.logger.info(f"🛑 Agent 0 Chef d'Équipe {self.agent_id} - ARRÊT")
        
        # Arrêt propre de tous les agents
        for nom_agent, agent in self.equipe_agents.items():
            try:
                if hasattr(agent, 'shutdown'):
                    await agent.shutdown()
                self.logger.info(f"✅ {nom_agent} arrêté proprement")
            except Exception as e:
                self.logger.error(f"❌ Erreur arrêt {nom_agent}: {e}")
                
        self.equipe_agents.clear()
        return {"status": "stopped", "agent_id": self.agent_id}
        
    async def health_check(self) -> Dict[str, Any]:
        """Vérification santé chef équipe et agents"""
        health_status = {
            "chef_equipe_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": "healthy",
            "agents_disponibles": len(self.equipe_agents),
            "workflows_disponibles": len(self.workflows_disponibles),
            "equipe_status": {},
            "configuration": {
                "target_path": str(self.target_path),
                "workspace_path": str(self.workspace_path),
                "safe_mode": self.config_workflows["safe_mode"]
            },
            "timestamp": datetime.now().isoformat()
        }
        
        self.logger.info(f"🏥 Health Check Agent 0 Chef d'Équipe: {health_status['status']}")
        return health_status
    
    def get_capabilities(self) -> List[str]:
        """Capacités du chef d'équipe"""
        return [
            "coordination_equipe_agents",
            "workflows_automatises",
            "rapports_consolides",
            "maintenance_complete",
            "validation_finale"
        ] + self.workflows_disponibles
    
    async def workflow_maintenance_complete(self, config: Dict = None) -> Dict[str, Any]:
        """Workflow complet: Analyse + Évaluation + Adaptation + Tests + Documentation + Validation"""
        self.logger.info("🔄 WORKFLOW MAINTENANCE COMPLÈTE - Démarrage")
        
        workflow_start = datetime.now()
        resultats_workflow = {
            "workflow_id": f"maintenance_complete_{workflow_start.strftime('%Y%m%d_%H%M%S')}",
            "chef_equipe_id": self.agent_id,
            "target_path": str(self.target_path),
            "etapes": {},
            "status": "en_cours",
            "resultats_consolides": {},
            "timestamp_debut": workflow_start.isoformat()
        }
        
        try:
            # Étape 1: Analyse Structure
            self.logger.info("📊 ÉTAPE 1/6: Analyse Structure")
            from agent_1_analyseur_structure import Agent1AnalyseurStructure
            agent_1 = Agent1AnalyseurStructure(str(self.target_path), str(self.workspace_path))
            # Utiliser la vraie méthode de l'agent
            resultat_1 = await agent_1.analyser_structure()
            
            resultats_workflow["etapes"]["etape_1_analyse"] = {
                "status": "complete",
                "resultats": resultat_1,
                "timestamp": datetime.now().isoformat()
            }
            self.logger.info("✅ ÉTAPE 1 terminée")
            
            # Étape 2: Évaluation Utilité
            self.logger.info("🎯 ÉTAPE 2/6: Évaluation Utilité")
            from agent_2_evaluateur_utilite import Agent2EvaluateurUtilite
            agent_2 = Agent2EvaluateurUtilite(resultat_1, str(self.workspace_path))
            resultat_2 = await agent_2.evaluer_utilite()
            
            resultats_workflow["etapes"]["etape_2_evaluation"] = {
                "status": "complete",
                "resultats": resultat_2,
                "timestamp": datetime.now().isoformat()
            }
            self.logger.info("✅ ÉTAPE 2 terminée")
            
            # Étape 3: Adaptation Code (si nécessaire) 
            self.logger.info("🔧 ÉTAPE 3/6: Adaptation Code")
            from agent_3_adaptateur_code import Agent3AdaptateurCode
            # Récupérer les outils sélectionnés par l'Agent 2
            outils_selectionnes = resultat_2.get("outils_selectionnes", [])
            agent_3 = Agent3AdaptateurCode(
                outils_selectionnes=outils_selectionnes,
                source_path=Path(str(self.target_path)),
                target_path=Path(str(self.target_path)) / "adapted_tools",
                workspace_path=Path(str(self.workspace_path))
            )
            resultat_3 = await agent_3.adapter_outils()
            
            resultats_workflow["etapes"]["etape_3_adaptation"] = {
                "status": "complete",
                "resultats": resultat_3,
                "timestamp": datetime.now().isoformat()
            }
            self.logger.info("✅ ÉTAPE 3 terminée")
            
            # Étape 4: Tests Intégration
            self.logger.info("🧪 ÉTAPE 4/6: Tests Intégration")
            from agent_4_testeur_integration import Agent4TesteurIntegration
            # Récupérer la liste des outils adaptés par l'Agent 3
            outils_adaptes = resultat_3.get("outils_adaptes", [])
            agent_4 = Agent4TesteurIntegration(
                outils_adaptes=outils_adaptes,
                target_path=Path(str(self.target_path)) / "adapted_tools",
                workspace_path=Path(str(self.workspace_path))
            )
            resultat_4 = await agent_4.tester_integration()
            
            resultats_workflow["etapes"]["etape_4_tests"] = {
                "status": "complete",
                "resultats": resultat_4,
                "timestamp": datetime.now().isoformat()
            }
            self.logger.info("✅ ÉTAPE 4 terminée")
            
            # Étape 5: Documentation
            self.logger.info("📚 ÉTAPE 5/6: Documentation")
            from agent_5_documenteur import Agent5Documenteur
            agent_5 = Agent5Documenteur(resultat_4, str(self.target_path), str(self.workspace_path))
            resultat_5 = await agent_5.documenter_complete()
            
            resultats_workflow["etapes"]["etape_5_documentation"] = {
                "status": "complete",
                "resultats": resultat_5,
                "timestamp": datetime.now().isoformat()
            }
            self.logger.info("✅ ÉTAPE 5 terminée")
            
            # Étape 6: Validation Finale
            self.logger.info("✅ ÉTAPE 6/6: Validation Finale")
            from agent_6_validateur_final import Agent6ValidateurFinal
            resultats_equipe = {
                "analyse": resultat_1,
                "evaluation": resultat_2,
                "adaptation": resultat_3,
                "tests": resultat_4,
                "documentation": resultat_5
            }
            agent_6 = Agent6ValidateurFinal(resultats_equipe, str(self.target_path), str(self.workspace_path))
            resultat_6 = await agent_6.valider_mission()
            
            resultats_workflow["etapes"]["etape_6_validation"] = {
                "status": "complete",
                "resultats": resultat_6,
                "timestamp": datetime.now().isoformat()
            }
            self.logger.info("✅ ÉTAPE 6 terminée")
            
            # Consolidation finale
            workflow_end = datetime.now()
            duree_totale = (workflow_end - workflow_start).total_seconds()
            
            resultats_workflow.update({
                "status": "complete",
                "timestamp_fin": workflow_end.isoformat(),
                "duree_totale_sec": duree_totale,
                "resultats_consolides": {
                    "agents_analyses": resultat_1.get("nombre_agents_analyses", 0),
                    "agents_valides": resultat_2.get("agents_valides", 0),
                    "adaptations_realisees": resultat_3.get("nombre_adaptations", 0),
                    "tests_executes": resultat_4.get("nombre_tests_executes", 0),
                    "documents_generes": resultat_5.get("nombre_documents", 0),
                    "score_final": resultat_6.get("score_validation", 0)
                },
                "recommandations_chef_equipe": self._generer_recommandations_finales(resultats_workflow),
                "actions_suivantes": self._generer_actions_suivantes(resultats_workflow)
            })
            
            # Sauvegarde rapport final
            await self._sauvegarder_rapport_final(resultats_workflow)
            
            self.logger.info(f"🎉 WORKFLOW MAINTENANCE COMPLÈTE TERMINÉ en {duree_totale:.1f}s")
            return resultats_workflow
            
        except Exception as e:
            self.logger.error(f"❌ Erreur workflow maintenance complète: {e}")
            resultats_workflow.update({
                "status": "erreur",
                "erreur": str(e),
                "timestamp_erreur": datetime.now().isoformat()
            })
            return resultats_workflow
    
    def _generer_recommandations_finales(self, workflow_result: Dict) -> List[str]:
        """Génération des recommandations finales du chef d'équipe"""
        recommandations = []
        
        try:
            etapes = workflow_result.get("etapes", {})
            resultats = workflow_result.get("resultats_consolides", {})
            
            # Analyse des performances
            if resultats.get("agents_valides", 0) < resultats.get("agents_analyses", 1):
                recommandations.append("🔧 Corriger les agents non valides détectés")
            
            if resultats.get("adaptations_realisees", 0) > 0:
                recommandations.append("📋 Vérifier les adaptations de code effectuées")
            
            if resultats.get("score_final", 0) < 80:
                recommandations.append("⚠️ Score de validation faible - Révision nécessaire")
            else:
                recommandations.append("✅ Équipe d'agents en excellent état")
            
            # Recommandations spécifiques
            recommandations.extend([
                "📊 Maintenir une surveillance continue de l'équipe",
                "🔄 Programmer des maintenances préventives régulières",
                "📈 Suivre les métriques de performance des agents"
            ])
            
        except Exception as e:
            recommandations.append(f"⚠️ Erreur génération recommandations: {e}")
        
        return recommandations
    
    def _generer_actions_suivantes(self, workflow_result: Dict) -> List[str]:
        """Génération des actions suivantes recommandées"""
        actions = []
        
        try:
            resultats = workflow_result.get("resultats_consolides", {})
            
            if resultats.get("score_final", 0) >= 90:
                actions.extend([
                    "🎯 Équipe optimale - Déploiement recommandé",
                    "📋 Documenter les bonnes pratiques identifiées",
                    "🔄 Appliquer le pattern aux autres équipes"
                ])
            elif resultats.get("score_final", 0) >= 70:
                actions.extend([
                    "🔧 Corriger les derniers points identifiés",
                    "🧪 Effectuer des tests supplémentaires",
                    "📊 Re-valider après corrections"
                ])
            else:
                actions.extend([
                    "⚠️ Révision majeure nécessaire",
                    "🔍 Analyse approfondie des problèmes",
                    "🛠️ Plan de correction prioritaire"
                ])
            
        except Exception as e:
            actions.append(f"⚠️ Erreur génération actions: {e}")
        
        return actions
    
    async def _sauvegarder_rapport_final(self, workflow_result: Dict):
        """Sauvegarde du rapport final consolidé"""
        try:
            rapport_path = self.workspace_path / "reports" / f"chef_equipe_maintenance_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            rapport_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(rapport_path, 'w', encoding='utf-8') as f:
                json.dump(workflow_result, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.info(f"💾 Rapport final sauvegardé: {rapport_path}")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur sauvegarde rapport final: {e}")

# Factory function pour compatibilité TemplateManager
def create_agent_0ChefEquipeCoordinateur(**config):
    """Factory function pour créer l'agent"""
    return Agent0ChefEquipeCoordinateur(**config)

# Fonction factory pour compatibilité
def create_agent_0_chef_equipe_coordinateur(target_path: str = None, workspace_path: str = None, **config):
    """Factory pour créer Agent 0 Chef d'Équipe Coordinateur"""
    return Agent0ChefEquipeCoordinateur(target_path=target_path, workspace_path=workspace_path, **config)

# Point d'entrée direct
async def main():
    """Point d'entrée principal Agent 0 Chef d'Équipe"""
    print("🎖️ AGENT 0 - CHEF D'ÉQUIPE COORDINATEUR")
    print("=" * 50)
    
    # Configuration par défaut
    target_path = "../agent_factory_implementation/agents"
    workspace_path = "."
    
    # Arguments en ligne de commande
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--help", "-h"]:
            print("""
Usage: python agent_0_chef_equipe_coordinateur.py [TARGET_PATH] [WORKSPACE_PATH]

Arguments:
  TARGET_PATH     Chemin vers le répertoire des agents à analyser
  WORKSPACE_PATH  Chemin vers l'espace de travail
  
Exemples:
  python agent_0_chef_equipe_coordinateur.py
  python agent_0_chef_equipe_coordinateur.py ../agents
  python agent_0_chef_equipe_coordinateur.py ../agents ./workspace
""")
            return
        
        target_path = sys.argv[1]
        if len(sys.argv) > 2:
            workspace_path = sys.argv[2]
    
    try:
        # Création et exécution
        chef_equipe = create_agent_0_chef_equipe_coordinateur(target_path, workspace_path)
        await chef_equipe.startup()
        
        # Health check
        health = await chef_equipe.health_check()
        print(f"🏥 Statut: {health['status']}")
        
        # Lancement workflow maintenance complète
        print("\n🚀 Lancement workflow maintenance complète...")
        resultats = await chef_equipe.workflow_maintenance_complete()
        
        # Affichage résultats
        print("\n📊 RÉSULTATS FINAUX:")
        print(f"Status: {resultats['status']}")
        if resultats['status'] == 'complete':
            consolides = resultats.get('resultats_consolides', {})
            print(f"Agents analysés: {consolides.get('agents_analyses', 0)}")
            print(f"Agents valides: {consolides.get('agents_valides', 0)}")
            print(f"Score final: {consolides.get('score_final', 0)}/100")
            print(f"Durée: {resultats.get('duree_totale_sec', 0):.1f}s")
        
        await chef_equipe.shutdown()
        print("✅ Chef d'équipe terminé avec succès")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(result) 