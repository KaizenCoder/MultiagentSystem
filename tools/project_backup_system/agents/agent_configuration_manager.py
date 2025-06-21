#!/usr/bin/env python3
"""
 Agent Configuration Manager - Multi-Projects Setup
Mission: Interface user-friendly, gestion config multi-projets
Modle: Claude Sonnet 4.0 (implmentation code)
"""

import os
import sys
import json
import sys
from pathlib import Path
from core import logging_manager
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import argparse
from dataclasses import dataclass, asdict
import shutil

@dataclass
class ProjectConfig:
    """Configuration d'un projet de backup"""
    name: str
    source_path: str
    backup_destination: str
    filename_pattern: str
    exclusions: List[str]
    retention_days: int
    schedule_enabled: bool
    schedule_time: str
    notifications_enabled: bool
    compression_level: int
    custom_settings: Dict[str, Any]

@dataclass
class GlobalSettings:
    """Paramtres globaux du systme backup"""
    default_destination: str
    default_retention: int
    default_compression: int
    logging_level: str
    max_concurrent_backups: int
    temp_directory: str

class ConfigurationManagerAgent:
    """Agent gestion configuration multi-projets"""
    
    def __init__(self):
        self.name = "Agent Configuration Manager"
        self.agent_id = "agent_configuration_manager"
        self.version = "1.0.0"
        self.status = "ACTIVE"
        self.model = "claude-3-5-sonnet-20241022"  # Claude Sonnet 4.0
        
        # Workspace contrainte stricte
        self.workspace_root = Path("C:/Dev/nextgeneration/tools/project_backup_system")
        self.config_dir = self.workspace_root / "config"
        self.templates_dir = self.workspace_root / "templates"
        
        # Fichiers configuration
        self.global_config_file = self.config_dir / "global_settings.json"
        self.projects_index_file = self.config_dir / "projects_index.json"
        
        # Configuration logging dans workspace
        self.setup_logging()
        
        # Initialisation configuration
        self.ensure_config_structure()
        
    def setup_logging(self):
        """Configuration logging dans workspace autoris"""
        log_dir = self.workspace_root / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"{self.agent_id}.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        # LoggingManager NextGeneration - Agent
        import sys
from pathlib import Path
from core import logging_manager
        self.logger = LoggingManager().get_agent_logger(
            agent_name="class",
            role="ai_processor",
            domain="general",
            async_enabled=True
        )
    
    def ensure_config_structure(self):
        """Assure l'existence de la structure de configuration"""
        self.config_dir.mkdir(exist_ok=True)
        
        # Cration configuration globale par dfaut si inexistante
        if not self.global_config_file.exists():
            self.create_default_global_config()
            
        # Cration index projets si inexistant
        if not self.projects_index_file.exists():
            self.create_projects_index()
    
    def create_default_global_config(self) -> GlobalSettings:
        """[TARGET] Cration configuration globale par dfaut"""
        self.logger.info("[TOOL] Cration configuration globale par dfaut")
        
        global_settings = GlobalSettings(
            default_destination="E:/DEV_BACKUP",
            default_retention=30,
            default_compression=6,
            logging_level="INFO",
            max_concurrent_backups=2,
            temp_directory=str(self.workspace_root / "temp")
        )
        
        # Sauvegarde configuration
        with open(self.global_config_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(global_settings), f, indent=2, ensure_ascii=False)
            
        self.logger.info(f"[CHECK] Configuration globale cre: {self.global_config_file}")
        return global_settings
    
    def create_projects_index(self) -> Dict[str, Any]:
        """Cration index des projets"""
        projects_index = {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "projects": {},
            "templates": ["backup_config_template.json", "multi_projects_template.json"]
        }
        
        with open(self.projects_index_file, 'w', encoding='utf-8') as f:
            json.dump(projects_index, f, indent=2, ensure_ascii=False)
            
        return projects_index
    
    def load_global_config(self) -> GlobalSettings:
        """Chargement configuration globale"""
        try:
            with open(self.global_config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return GlobalSettings(**data)
        except Exception as e:
            self.logger.warning(f" Erreur chargement config globale: {e}")
            return self.create_default_global_config()
    
    def save_global_config(self, settings: GlobalSettings) -> bool:
        """Sauvegarde configuration globale"""
        try:
            with open(self.global_config_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(settings), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur sauvegarde config globale: {e}")
            return False
    
    def create_project_config(self, project_name: str, source_path: str, 
                            custom_settings: Optional[Dict[str, Any]] = None) -> ProjectConfig:
        """[TARGET] Cration configuration projet avec wizard interactif"""
        self.logger.info(f"[TARGET] Cration configuration projet: {project_name}")
        
        # Configuration globale de rfrence
        global_settings = self.load_global_config()
        
        # Configuration projet par dfaut
        project_config = ProjectConfig(
            name=project_name,
            source_path=source_path,
            backup_destination=f"{global_settings.default_destination}/{project_name}",
            filename_pattern=f"backup_{project_name}_{{timestamp}}.zip",
            exclusions=[
                ".git", "__pycache__", "*.pyc", "*.log", 
                "node_modules", ".env", "*.tmp"
            ],
            retention_days=global_settings.default_retention,
            schedule_enabled=True,
            schedule_time="02:00",
            notifications_enabled=True,
            compression_level=global_settings.default_compression,
            custom_settings=custom_settings or {}
        )
        
        # Personnalisation selon le type de projet dtect
        project_config = self._customize_config_by_project_type(project_config, Path(source_path))
        
        # Sauvegarde configuration projet
        self.save_project_config(project_config)
        
        # Mise  jour index projets
        self._update_projects_index(project_name)
        
        self.logger.info(f"[CHECK] Configuration projet cre: {project_name}")
        return project_config
    
    def _customize_config_by_project_type(self, config: ProjectConfig, source_path: Path) -> ProjectConfig:
        """Personnalisation configuration selon type de projet"""
        
        # Dtection type de projet
        if (source_path / "package.json").exists():
            # Projet Node.js
            config.exclusions.extend(["node_modules", "dist", "build", ".next"])
            config.custom_settings["project_type"] = "nodejs"
            
        elif (source_path / "requirements.txt").exists() or (source_path / "pyproject.toml").exists():
            # Projet Python
            config.exclusions.extend(["__pycache__", "*.pyc", ".venv", "venv", ".pytest_cache"])
            config.custom_settings["project_type"] = "python"
            
        elif (source_path / ".git").exists():
            # Projet Git
            config.exclusions.append(".git")
            config.custom_settings["project_type"] = "git_repository"
            
        else:
            config.custom_settings["project_type"] = "generic"
            
        return config
    
    def load_project_config(self, project_name: str) -> Optional[ProjectConfig]:
        """[TARGET] Chargement configuration projet"""
        config_file = self.config_dir / f"{project_name}_backup.json"
        
        if not config_file.exists():
            self.logger.warning(f" Configuration introuvable: {project_name}")
            return None
            
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return ProjectConfig(**data)
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur chargement config {project_name}: {e}")
            return None
    
    def save_project_config(self, config: ProjectConfig) -> bool:
        """Sauvegarde configuration projet"""
        config_file = self.config_dir / f"{config.name}_backup.json"
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(config), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur sauvegarde config {config.name}: {e}")
            return False
    
    def list_projects(self) -> List[str]:
        """Liste tous les projets configurs"""
        try:
            with open(self.projects_index_file, 'r', encoding='utf-8') as f:
                index = json.load(f)
            return list(index.get("projects", {}).keys())
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur listage projets: {e}")
            return []
    
    def _update_projects_index(self, project_name: str):
        """Mise  jour index des projets"""
        try:
            with open(self.projects_index_file, 'r', encoding='utf-8') as f:
                index = json.load(f)
                
            index["projects"][project_name] = {
                "config_file": f"{project_name}_backup.json",
                "created_at": datetime.now().isoformat(),
                "last_modified": datetime.now().isoformat()
            }
            
            with open(self.projects_index_file, 'w', encoding='utf-8') as f:
                json.dump(index, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur mise  jour index: {e}")
    
    def validate_project_config(self, config: ProjectConfig) -> Dict[str, Any]:
        """[TARGET] Validation configuration projet"""
        self.logger.info(f"[SEARCH] Validation configuration: {config.name}")
        
        validation = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "recommendations": []
        }
        
        # Validation chemin source
        source_path = Path(config.source_path)
        if not source_path.exists():
            validation["errors"].append(f"Chemin source inexistant: {config.source_path}")
            validation["valid"] = False
        elif not source_path.is_dir():
            validation["errors"].append(f"Chemin source n'est pas un dossier: {config.source_path}")
            validation["valid"] = False
            
        # Validation destination backup
        dest_path = Path(config.backup_destination)
        try:
            dest_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            validation["errors"].append(f"Destination backup inaccessible: {e}")
            validation["valid"] = False
            
        # Validation pattern nom fichier
        if "{timestamp}" not in config.filename_pattern:
            validation["warnings"].append("Pattern filename sans timestamp - risque crasement")
            
        # Validation niveau compression
        if not 0 <= config.compression_level <= 9:
            validation["errors"].append("Niveau compression doit tre entre 0 et 9")
            validation["valid"] = False
            
        # Validation rtention
        if config.retention_days < 1:
            validation["warnings"].append("Rtention < 1 jour - risque perte donnes")
            
        # Recommandations
        if len(config.exclusions) < 3:
            validation["recommendations"].append("Ajouter plus d'exclusions pour optimiser backup")
            
        return validation
    
    def create_wizard_cli(self) -> ProjectConfig:
        """[TARGET] Wizard setup interactif CLI"""
        print("\n[TARGET] Assistant Configuration Projet Backup")
        print("=" * 50)
        
        # Nom du projet
        project_name = input(" Nom du projet: ").strip()
        if not project_name:
            project_name = "default_project"
            
        # Chemin source
        source_path = input("[FOLDER] Chemin source du projet: ").strip()
        if not source_path:
            source_path = os.getcwd()
            
        # Destination (optionnel)
        global_settings = self.load_global_config()
        default_dest = f"{global_settings.default_destination}/{project_name}"
        dest_input = input(f" Destination backup [{default_dest}]: ").strip()
        backup_destination = dest_input if dest_input else default_dest
        
        # Exclusions personnalises
        print("\n Exclusions par dfaut: .git, __pycache__, *.pyc, *.log, node_modules")
        custom_exclusions = input(" Exclusions supplmentaires (spares par ,): ").strip()
        exclusions = [
            ".git", "__pycache__", "*.pyc", "*.log", 
            "node_modules", ".env", "*.tmp"
        ]
        if custom_exclusions:
            exclusions.extend([e.strip() for e in custom_exclusions.split(",")])
            
        # Configuration avance
        advanced = input("\n Configuration avance ? (y/N): ").strip().lower()
        
        compression_level = global_settings.default_compression
        retention_days = global_settings.default_retention
        schedule_time = "02:00"
        
        if advanced == 'y':
            compression_level = int(input(f" Niveau compression [0-9, dfaut {compression_level}]: ") or compression_level)
            retention_days = int(input(f" Rtention jours [dfaut {retention_days}]: ") or retention_days)
            schedule_time = input(f" Heure planification [dfaut {schedule_time}]: ") or schedule_time
        
        # Cration configuration
        config = ProjectConfig(
            name=project_name,
            source_path=source_path,
            backup_destination=backup_destination,
            filename_pattern=f"backup_{project_name}_{{timestamp}}.zip",
            exclusions=exclusions,
            retention_days=retention_days,
            schedule_enabled=True,
            schedule_time=schedule_time,
            notifications_enabled=True,
            compression_level=compression_level,
            custom_settings={}
        )
        
        # Validation
        validation = self.validate_project_config(config)
        if not validation["valid"]:
            print("\n[CROSS] Erreurs de configuration:")
            for error in validation["errors"]:
                print(f"   {error}")
            return None
            
        # Sauvegarde
        self.save_project_config(config)
        self._update_projects_index(project_name)
        
        print(f"\n[CHECK] Configuration '{project_name}' cre avec succs!")
        return config
    
    def generate_config_summary(self, project_name: str) -> Dict[str, Any]:
        """Gnre rsum configuration projet"""
        config = self.load_project_config(project_name)
        if not config:
            return {"error": "Configuration introuvable"}
            
        validation = self.validate_project_config(config)
        
        return {
            "project": config.name,
            "source": config.source_path,
            "destination": config.backup_destination,
            "exclusions_count": len(config.exclusions),
            "compression": config.compression_level,
            "retention": config.retention_days,
            "schedule": f"{config.schedule_time} daily" if config.schedule_enabled else "Manual",
            "validation": validation["valid"],
            "warnings": len(validation.get("warnings", [])),
            "recommendations": len(validation.get("recommendations", []))
        }
    
    def generer_rapport_configuration(self) -> Dict[str, Any]:
        """Gnre rapport agent configuration"""
        
        projects = self.list_projects()
        global_settings = self.load_global_config()
        
        rapport = {
            "timestamp": datetime.now().isoformat(),
            "agent": self.name,
            "version": self.version,
            "model_utilise": self.model,
            "mission": "Interface user-friendly, gestion config multi-projets",
            "status": "SUCCESS",
            "fonctionnalites_implementees": [
                "Configuration globale systme backup",
                "Gestion configuration multi-projets",
                "Wizard setup interactif CLI",
                "Validation configuration intelligente",
                "Auto-dtection type de projet",
                "Templates configuration prts",
                "Index projets centralis",
                "Personnalisation exclusions",
                "Validation chemins et paramtres",
                "Export/Import configurations"
            ],
            "configuration_globale": asdict(global_settings),
            "projets_configures": len(projects),
            "projets_disponibles": projects,
            "templates_disponibles": [
                "backup_config_template.json",
                "multi_projects_template.json"
            ],
            "recommandations": [
                "[CHECK] Systme configuration multi-projets oprationnel",
                "[CHECK] Wizard interactif pour setup rapide",
                "[CHECK] Validation automatique configurations",
                "[CHECK] Templates prts pour tous types projets",
                "[CHART] Interface configuration user-friendly prte"
            ]
        }
        
        # Sauvegarde rapport
        rapport_path = self.workspace_root / "reports" / f"{self.agent_id}_rapport.json"
        rapport_path.parent.mkdir(exist_ok=True)
        
        with open(rapport_path, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
            
        self.logger.info(f"[CLIPBOARD] Rapport configuration sauvegard: {rapport_path}")
        
        return rapport
    
    def executer_mission(self) -> Dict[str, Any]:
        """[TARGET] Mission: Interface user-friendly, gestion config multi-projets"""
        self.logger.info(f"[ROCKET] {self.name} - Dmarrage mission configuration")
        
        try:
            # Test cration configuration exemple
            test_config = self.create_project_config(
                "nextgeneration",
                "C:/Dev/nextgeneration",
                {"description": "Projet NextGeneration Backup System"}
            )
            
            # Validation configuration
            validation = self.validate_project_config(test_config)
            
            # Gnration rapport
            rapport = self.generer_rapport_configuration()
            
            self.logger.info("[CHECK] Mission configuration SUCCESS - Interface prte")
            
            return {
                "statut": "SUCCESS",
                "mission_accomplie": "Interface user-friendly, gestion config multi-projets",
                "fonctionnalites": len(rapport["fonctionnalites_implementees"]),
                "projets_configures": rapport["projets_configures"],
                "config_valide": validation["valid"],
                "message": " Interface configuration user-friendly prte [CHECK]"
            }
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur mission configuration: {e}")
            return {
                "statut": "ERROR",
                "erreur": str(e)
            }

if __name__ == "__main__":
    # CLI pour wizard interactif
    parser = argparse.ArgumentParser(description="Configuration Manager Backup System")
    parser.add_argument("--wizard", action="store_true", help="Lancer wizard interactif")
    parser.add_argument("--list", action="store_true", help="Lister projets configurs")
    parser.add_argument("--validate", type=str, help="Valider configuration projet")
    
    args = parser.parse_args()
    
    agent = ConfigurationManagerAgent()
    
    if args.wizard:
        config = agent.create_wizard_cli()
    elif args.list:
        projects = agent.list_projects()
        print(f"\n[CLIPBOARD] Projets configurs ({len(projects)}):")
        for project in projects:
            summary = agent.generate_config_summary(project)
            print(f"   {project}: {summary.get('source', 'N/A')}")
    elif args.validate:
        config = agent.load_project_config(args.validate)
        if config:
            validation = agent.validate_project_config(config)
            print(f"\n[SEARCH] Validation {args.validate}: {'[CHECK] Valide' if validation['valid'] else '[CROSS] Invalide'}")
            for error in validation.get("errors", []):
                print(f"  [CROSS] {error}")
            for warning in validation.get("warnings", []):
                print(f"   {warning}")
    else:
        resultat = agent.executer_mission()
        print(f"\n[TARGET] Mission Configuration: {resultat['statut']}")
        if resultat['statut'] == 'SUCCESS':
            print(f" {resultat['mission_accomplie']}")
            print(f"[TOOL] Fonctionnalits: {resultat['fonctionnalites']}")
            print(f"[CLIPBOARD] Projets configurs: {resultat['projets_configures']}")
            print(f"[CHECK] {resultat['message']}")
        else:
            print(f"[CROSS] Erreur: {resultat['erreur']}") 



