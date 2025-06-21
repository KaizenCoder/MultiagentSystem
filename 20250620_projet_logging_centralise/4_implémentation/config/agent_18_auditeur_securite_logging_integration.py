#!/usr/bin/env python3
"""
🔧 SCRIPT D'INTÉGRATION LOGGING - AGENT_18_AUDITEUR_SECURITE
Intègre l'agent au système de logging NextGeneration

Généré automatiquement le 2025-06-21 02:12:49
"""

import sys
from pathlib import Path

# Ajouter le chemin du système de logging
sys.path.insert(0, str(Path(__file__).parent))

from logging_manager_optimized import LoggingManager

class Agent18AuditeursecuriteLoggingIntegration:
    """
    Intégration logging pour agent_18_auditeur_securite
    """
    
    def __init__(self, agent_instance):
        self.agent = agent_instance
        self.logger = LoggingManager().get_agent_logger('agent_18_auditeur_securite')
        
        # Configuration spécialisée
        self.reports_dir = Path(__file__).parent / "reports_equipe_agents" / "agent_18_auditeur_securite"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"🚀 Intégration logging activée pour {self.agent.__class__.__name__}")
    
    def log_mission_start(self, mission_data: dict):
        """Log le démarrage d'une mission"""
        self.logger.info(f"🎯 Démarrage mission: {mission_data.get('mission_type', 'unknown')}")
        self.logger.log_structured_data("mission_start", mission_data)
    
    def log_mission_progress(self, progress_data: dict):
        """Log le progrès d'une mission"""
        self.logger.info(f"📊 Progrès mission: {progress_data.get('completion_rate', 0)}%")
        self.logger.log_structured_data("mission_progress", progress_data)
    
    def log_mission_completion(self, result_data: dict):
        """Log la completion d'une mission"""
        self.logger.info(f"✅ Mission terminée - Score: {result_data.get('score', 'N/A')}")
        self.logger.log_structured_data("mission_completion", result_data)
        
        # Génération rapport structuré
        self._generate_structured_report(result_data)
    
    def log_error(self, error_data: dict):
        """Log une erreur avec contexte"""
        self.logger.error(f"❌ Erreur: {error_data.get('message', 'Unknown error')}")
        self.logger.log_structured_data("error", error_data)
    
    def _generate_structured_report(self, result_data: dict):
        """Génère un rapport structuré dans le répertoire autorisé"""
        import json
        from datetime import datetime
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.reports_dir / f"rapport_{timestamp}.json"
        
        structured_report = {
            "agent_id": "agent_18_auditeur_securite",
            "timestamp": datetime.now().isoformat(),
            "mission_data": result_data,
            "logging_metrics": self.logger.get_metrics() if hasattr(self.logger, 'get_metrics') else {},
            "report_version": "1.0.0"
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(structured_report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"📄 Rapport structuré généré: {report_file}")
        return str(report_file)

def integrate_logging(agent_instance):
    """
    🚀 Point d'entrée pour intégrer le logging à un agent
    
    Usage:
        from agent_18_auditeur_securite_logging_integration import integrate_logging
        logging_integration = integrate_logging(mon_agent)
    """
    return Agent18AuditeursecuriteLoggingIntegration(agent_instance)

# Test d'intégration
if __name__ == "__main__":
    print(f"🔧 Test intégration logging pour agent_18_auditeur_securite")
    
    # Simulation d'agent
    class MockAgent:
        def __init__(self):
            self.name = "agent_18_auditeur_securite"
    
    mock_agent = MockAgent()
    integration = integrate_logging(mock_agent)
    
    # Test des fonctionnalités
    integration.log_mission_start({"mission_type": "test", "target": "logging_validation"})
    integration.log_mission_progress({"completion_rate": 50, "current_phase": "analysis"})
    integration.log_mission_completion({"score": 8.5, "status": "success", "findings": ["Test successful"]})
    
    print("✅ Test d'intégration réussi")
