#!/usr/bin/env python3
"""
📁 CONFIGURATION LOGS MAINTENANCE
Configuration centralisée pour l'organisation des logs de maintenance
"""

from pathlib import Path
from datetime import datetime

class LogsMaintenanceConfig:
    """Configuration centralisée pour les logs de maintenance"""
    
    # Répertoire racine des logs de maintenance
    LOGS_ROOT = Path("logs/maintenance")
    
    # Sous-répertoires par type d'agent
    LOGS_DIRS = {
        "orchestrateur": LOGS_ROOT / "orchestrateur",
        "analyseur": LOGS_ROOT / "analyseur", 
        "evaluateur": LOGS_ROOT / "evaluateur",
        "testeur": LOGS_ROOT / "testeur",
        "docteur": LOGS_ROOT / "docteur"
    }
    
    @classmethod
    def ensure_logs_structure(cls):
        """Assure que la structure de logs existe"""
        for log_dir in cls.LOGS_DIRS.values():
            log_dir.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_log_path(cls, agent_type: str, filename: str) -> Path:
        """Retourne le chemin complet pour un log"""
        cls.ensure_logs_structure()
        
        if agent_type not in cls.LOGS_DIRS:
            agent_type = "orchestrateur"  # Fallback
            
        return cls.LOGS_DIRS[agent_type] / filename
    
    @classmethod
    def get_timestamped_filename(cls, agent_type: str, base_name: str, extension: str = "json") -> str:
        """Génère un nom de fichier avec timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_{agent_type}_{timestamp}.{extension}"
    
    @classmethod
    def get_rapport_path(cls, agent_type: str, rapport_type: str = "rapport") -> Path:
        """Retourne le chemin pour un rapport avec timestamp"""
        filename = cls.get_timestamped_filename(agent_type, rapport_type)
        return cls.get_log_path(agent_type, filename)

# Fonction utilitaire pour compatibilité
def get_maintenance_log_path(agent_type: str, filename: str) -> Path:
    """Fonction utilitaire pour obtenir un chemin de log de maintenance"""
    return LogsMaintenanceConfig.get_log_path(agent_type, filename)

def get_maintenance_rapport_path(agent_type: str, rapport_type: str = "rapport") -> Path:
    """Fonction utilitaire pour obtenir un chemin de rapport de maintenance"""
    return LogsMaintenanceConfig.get_rapport_path(agent_type, rapport_type) 



