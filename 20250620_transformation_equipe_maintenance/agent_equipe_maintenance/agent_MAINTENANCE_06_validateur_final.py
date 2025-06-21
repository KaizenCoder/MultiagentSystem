#!/usr/bin/env python3
"""
Agent 06 - Validateur Final NextGeneration
Validation finale et certification des transformations de l'équipe de maintenance
"""

import asyncio
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import ast

# Imports Pattern Factory NextGeneration
try:
    from agent_factory_architecture import Agent, Task, Result
    PATTERN_FACTORY_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Pattern Factory non disponible: {e}")
    # Fallback pour compatibilité
    class Agent:
        def __init__(self, agent_type: str, **config):
            self.agent_type = agent_type
            self.config = config
            self.agent_id = f"agent_6_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            # LoggingManager NextGeneration - Agent
            import sys
from pathlib import Path
from core import logging_manager
            self.logger = LoggingManager().get_agent_logger(
                agent_name="Agent",
                role="ai_processor",
                domain="general",
                async_enabled=True
            )
                
        async def startup(self): pass
        async def shutdown(self): pass
        async def health_check(self): return {"status": "healthy"}
        def get_capabilities(self): return []
        
    class Task:
        def __init__(self, task_id: str, description: str, **kwargs):
            self.task_id = task_id
            self.description = description
            
    class Result:
        def __init__(self, success: bool, data: Any = None, error: str = None):
            self.success = success
            self.data = data
            self.error = error
    
    PATTERN_FACTORY_AVAILABLE = False

class ValidateurFinalNextGeneration(Agent):
    """Validateur Final - Certification et validation complète des agents transformés"""
    
    def __init__(self, **config):
        # Initialisation Pattern Factory OBLIGATOIRE
        super().__init__("validateur_final", **config)
        
        # Configuration spécialisée
        self.reports_dir = Path("reports")
        self.certification_dir = Path("reports/certifications")
        
        # Créer les répertoires nécessaires
        self.reports_dir.mkdir(exist_ok=True)
        self.certification_dir.mkdir(exist_ok=True)
        
        # Critères de validation
        self.validation_criteria = {
            "syntax_validation": 0.30,
            "pattern_factory_compliance": 0.40,
            "functionality_validation": 0.30
        }
        
        # Seuils de certification
        self.certification_thresholds = {
            "CERTIFIED_GOLD": 0.95,
            "CERTIFIED_SILVER": 0.85,
            "CERTIFIED_BRONZE": 0.75,
            "VALIDATION_FAILED": 0.60
        }
        
        if hasattr(self, 'logger'):
            self.logger.info(f"🏆 ValidateurFinalNextGeneration initialisé - ID: {self.agent_id}")
        else:
            print(f"🏆 ValidateurFinalNextGeneration initialisé - ID: {self.agent_id}")
    
    # Implémentation méthodes abstraites OBLIGATOIRES
    async def startup(self):
        """Démarrage validateur final"""
        if hasattr(self, 'logger'):
            self.logger.info(f"🚀 ValidateurFinalNextGeneration {self.agent_id} - DÉMARRAGE")
        else:
            print(f"🚀 ValidateurFinalNextGeneration {self.agent_id} - DÉMARRAGE")
        
    async def shutdown(self):
        """Arrêt validateur final"""
        if hasattr(self, 'logger'):
            self.logger.info(f"🛑 ValidateurFinalNextGeneration {self.agent_id} - ARRÊT")
        else:
            print(f"🛑 ValidateurFinalNextGeneration {self.agent_id} - ARRÊT")
        
    async def health_check(self) -> Dict[str, Any]:
        """Vérification santé validateur final"""
        if not hasattr(self, 'agent_id'):
            self.agent_id = f"agent_6_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
        if not hasattr(self, 'agent_type'):
            self.agent_type = "validateur_final"
            
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": "healthy",
            "ready": True,
            "pattern_factory_available": PATTERN_FACTORY_AVAILABLE,
            "timestamp": datetime.now().isoformat()
        }
    
    async def execute_task(self, task: Task) -> Result:
        """Exécution des tâches de validation finale"""
        try:
            if hasattr(self, 'logger'):
                self.logger.info(f"🎯 Exécution tâche: {task.task_id}")
            
            if task.task_id == "validate_team_complete":
                team_directory = getattr(task, 'team_directory', None)
                if not team_directory:
                    return Result(success=False, error="team_directory requis")
                
                results = await self.validate_team_complete(team_directory)
                return Result(success=True, data=results)
                
            else:
                return Result(success=False, error=f"Tâche non reconnue: {task.task_id}")
                
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"❌ Erreur exécution tâche {task.task_id}: {e}")
            return Result(success=False, error=str(e))
    
    def get_capabilities(self) -> List[str]:
        """Retourne les capacités du validateur final"""
        return [
            "execute_mission",
            "validate_team_complete",
            "certify_agents",
            "syntax_validation",
            "pattern_factory_compliance_check",
            "functionality_validation"
        ]

    async def valider_mission(self) -> Dict[str, Any]:
        """Méthode de validation de mission pour le workflow du chef d'équipe"""
        try:
            if hasattr(self, 'logger'):
                self.logger.info("🏆 Démarrage validation finale de mission")
            
            # Valider l'équipe de maintenance
            team_directory = "agent_equipe_maintenance"
            results = await self.validate_team_complete(team_directory)
            
            if hasattr(self, 'logger'):
                self.logger.info("✅ Validation de mission terminée")
                
            return {
                "status": "completed",
                "validation_results": results,
                "timestamp": datetime.now().isoformat(),
                "agent_id": getattr(self, 'agent_id', 'unknown')
            }
            
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"❌ Erreur validation mission: {e}")
            return {
                "status": "error",
                "error": str(e),
                "agent_id": getattr(self, 'agent_id', 'unknown')
            }
    
    async def validate_team_complete(self, team_directory: str) -> Dict[str, Any]:
        """Validation complète de l'équipe de maintenance"""
        team_dir = Path(team_directory)
        
        if not team_dir.exists():
            return {
                "team_directory": str(team_dir),
                "validation_status": "FAILED",
                "error": "Répertoire équipe non trouvé"
            }
        
        # Rechercher tous les agents de maintenance
        agent_files = list(team_dir.glob("agent_MAINTENANCE_*.py"))
        
        if not agent_files:
            return {
                "team_directory": str(team_dir),
                "validation_status": "FAILED",
                "error": "Aucun agent de maintenance trouvé"
            }
        
        # Valider chaque agent
        team_results = {}
        team_scores = []
        
        for agent_file in sorted(agent_files):
            agent_result = await self.validate_single_agent(str(agent_file))
            team_results[agent_file.stem] = agent_result
            if agent_result["validation_status"] == "PASSED":
                team_scores.append(agent_result["overall_score"])
        
        # Calculer les statistiques d'équipe
        team_score = sum(team_scores) / len(team_scores) if team_scores else 0.0
        success_rate = len(team_scores) / len(agent_files) * 100
        
        result = {
            "team_directory": str(team_dir),
            "validation_status": "PASSED" if success_rate >= 85 else "FAILED",
            "team_score": round(team_score, 3),
            "success_rate": round(success_rate, 1),
            "agents_count": len(agent_files),
            "agents_passed": len(team_scores),
            "agents_failed": len(agent_files) - len(team_scores),
            "individual_results": team_results,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    async def validate_single_agent(self, agent_file_path: str) -> Dict[str, Any]:
        """Validation d'un agent unique"""
        agent_path = Path(agent_file_path)
        
        if not agent_path.exists():
            return {
                "agent_file": str(agent_path),
                "validation_status": "FAILED",
                "error": "Fichier agent non trouvé",
                "overall_score": 0.0
            }
        
        try:
            with open(agent_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # Test syntaxe
            syntax_score = 0.0
            try:
                ast.parse(source_code)
                syntax_score = 1.0
            except SyntaxError:
                syntax_score = 0.0
            
            # Test Pattern Factory
            factory_score = 0.0
            if "(Agent)" in source_code:
                factory_score += 0.4
            if "async def startup" in source_code:
                factory_score += 0.2
            if "async def shutdown" in source_code:
                factory_score += 0.2
            if "async def health_check" in source_code:
                factory_score += 0.2
            
            # Test fonctionnalité
            functionality_score = 0.0
            if "async def execute_task" in source_code:
                functionality_score += 0.5
            if "def get_capabilities" in source_code:
                functionality_score += 0.3
            if "try:" in source_code and "except" in source_code:
                functionality_score += 0.2
            
            # Score global
            overall_score = (
                syntax_score * self.validation_criteria["syntax_validation"] +
                factory_score * self.validation_criteria["pattern_factory_compliance"] +
                functionality_score * self.validation_criteria["functionality_validation"]
            )
            
            # Déterminer le statut
            validation_status = "PASSED" if overall_score >= 0.75 else "FAILED"
            
            return {
                "agent_file": str(agent_path),
                "agent_name": agent_path.stem,
                "validation_status": validation_status,
                "overall_score": round(overall_score, 3),
                "syntax_score": round(syntax_score, 3),
                "factory_score": round(factory_score, 3),
                "functionality_score": round(functionality_score, 3),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "agent_file": str(agent_path),
                "validation_status": "FAILED",
                "error": str(e),
                "overall_score": 0.0
            }

def create_validateur_final(**config) -> ValidateurFinalNextGeneration:
    """Factory function pour créer l'agent validateur final"""
    return ValidateurFinalNextGeneration(**config)

def create_agent_6ValidateurFinal(**config) -> ValidateurFinalNextGeneration:
    """Factory function pour créer l'agent 6 (alias pour compatibilité)"""
    return ValidateurFinalNextGeneration(**config)

async def main():
    """Test du validateur final"""
    agent = create_validateur_final()
    
    await agent.startup()
    health = await agent.health_check()
    print(f"🏆 Validateur Final - Santé: {health}")
    
    await agent.shutdown()

if __name__ == "__main__":
    asyncio.run(main())




