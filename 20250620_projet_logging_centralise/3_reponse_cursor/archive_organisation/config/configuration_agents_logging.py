#!/usr/bin/env python3
"""
🔧 CONFIGURATION AGENTS - LOGGING NEXTGENERATION
Adapte chaque agent spécialisé pour utiliser le système de logging centralisé

Ce script configure automatiquement chaque agent pour :
1. Utiliser LoggingManager NextGeneration
2. Transmettre ses rapports dans le répertoire autorisé
3. Structurer ses logs selon les standards définis
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

# Configuration des chemins
PROJECT_ROOT = Path(__file__).parent.parent.parent
AGENTS_DIR = PROJECT_ROOT / "agent_factory_implementation" / "agents"
REPORTS_DIR = Path(__file__).parent / "reports_equipe_agents"
CONFIG_DIR = Path(__file__).parent / "config"

# Créer répertoires
REPORTS_DIR.mkdir(exist_ok=True)
CONFIG_DIR.mkdir(exist_ok=True)

class ConfigurationAgentsLogging:
    """
    🔧 Configurateur des Agents pour Logging NextGeneration
    
    Génère les configurations spécialisées pour chaque agent
    """
    
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Configuration par type d'agent
        self.agents_configs = {
            "agent_01_coordinateur_principal": {
                "logging_level": "INFO",
                "report_format": "coordination_rapport",
                "metrics_enabled": True,
                "elasticsearch_enabled": True,
                "security_level": "high",
                "specialized_handlers": ["coordination", "team_management"],
                "report_structure": {
                    "sections": ["coordination_status", "team_metrics", "sprint_progress", "blockers"],
                    "format": "markdown",
                    "charts_enabled": True
                }
            },
            
            "agent_11_auditeur_qualite": {
                "logging_level": "DEBUG", 
                "report_format": "audit_qualite_rapport",
                "metrics_enabled": True,
                "elasticsearch_enabled": True,
                "security_level": "high",
                "specialized_handlers": ["quality_audit", "code_analysis"],
                "report_structure": {
                    "sections": ["quality_metrics", "code_coverage", "technical_debt", "recommendations"],
                    "format": "json_detailed",
                    "scoring_enabled": True
                }
            },
            
            "agent_15_testeur_specialise": {
                "logging_level": "DEBUG",
                "report_format": "tests_specialises_rapport", 
                "metrics_enabled": True,
                "elasticsearch_enabled": True,
                "security_level": "medium",
                "specialized_handlers": ["testing", "performance_testing"],
                "report_structure": {
                    "sections": ["test_results", "performance_metrics", "coverage_analysis", "failures"],
                    "format": "junit_xml",
                    "real_time_reporting": True
                }
            },
            
            "agent_16_peer_reviewer_senior": {
                "logging_level": "INFO",
                "report_format": "peer_review_senior_rapport",
                "metrics_enabled": True, 
                "elasticsearch_enabled": True,
                "security_level": "high",
                "specialized_handlers": ["peer_review", "senior_analysis"],
                "report_structure": {
                    "sections": ["review_summary", "architecture_feedback", "best_practices", "mentoring_notes"],
                    "format": "structured_markdown",
                    "approval_workflow": True
                }
            },
            
            "agent_17_peer_reviewer_technique": {
                "logging_level": "DEBUG",
                "report_format": "peer_review_technique_rapport",
                "metrics_enabled": True,
                "elasticsearch_enabled": True, 
                "security_level": "high",
                "specialized_handlers": ["technical_review", "code_analysis"],
                "report_structure": {
                    "sections": ["technical_analysis", "code_quality", "security_review", "performance_impact"],
                    "format": "technical_json",
                    "code_snippets_enabled": True
                }
            },
            
            "agent_18_auditeur_securite": {
                "logging_level": "INFO",
                "report_format": "audit_securite_rapport",
                "metrics_enabled": True,
                "elasticsearch_enabled": True,
                "security_level": "critical",
                "specialized_handlers": ["security_audit", "vulnerability_scan"],
                "report_structure": {
                    "sections": ["security_status", "vulnerabilities", "compliance_check", "remediation_plan"],
                    "format": "security_json",
                    "encryption_required": True,
                    "confidentiality": "restricted"
                }
            },
            
            "agent_19_auditeur_performance": {
                "logging_level": "DEBUG",
                "report_format": "audit_performance_rapport",
                "metrics_enabled": True,
                "elasticsearch_enabled": True,
                "security_level": "medium", 
                "specialized_handlers": ["performance_audit", "profiling"],
                "report_structure": {
                    "sections": ["performance_metrics", "bottlenecks", "optimization_opportunities", "benchmarks"],
                    "format": "performance_json",
                    "real_time_metrics": True,
                    "charts_enabled": True
                }
            },
            
            "agent_20_auditeur_conformite": {
                "logging_level": "INFO",
                "report_format": "audit_conformite_rapport",
                "metrics_enabled": True,
                "elasticsearch_enabled": True,
                "security_level": "high",
                "specialized_handlers": ["compliance_audit", "standards_check"],
                "report_structure": {
                    "sections": ["compliance_status", "standards_adherence", "gaps_analysis", "action_plan"],
                    "format": "compliance_json",
                    "regulatory_tracking": True,
                    "audit_trail": True
                }
            },
            
            # Configuration spécialisée pour Pattern Factory Core
            "agent_factory_architecture": {
                "logger_name": "nextgen.pattern_factory.core",
                "log_level": "INFO", 
                "elasticsearch_enabled": True,
                "encryption_enabled": True,
                "performance_monitoring": True,
                "structured_logging": True,
                "context_data": {
                    "component": "pattern_factory_core",
                    "criticality": "ABSOLUTE",
                    "usage_intensity": "HIGH",  # 21 occurrences logging
                    "architecture_layer": "CORE"
                },
                "custom_handlers": ["elasticsearch", "encrypted_file", "performance"],
                "metrics_enabled": True,
                "trace_enabled": True,
                "backup_enabled": True
            }
        }

    def generer_configuration_complete(self) -> Dict[str, Any]:
        """
        🎯 Génère la configuration complète pour tous les agents
        
        Returns:
            Dict avec configurations détaillées par agent
        """
        print("🔧 Génération configuration complète des agents...")
        
        configuration_complete = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "1.0.0",
                "logging_system": "NextGeneration",
                "target_agents": list(self.agents_configs.keys())
            },
            "global_settings": {
                "logging_manager_path": "./logging_manager_optimized.py",
                "reports_directory": str(REPORTS_DIR),
                "logs_directory": "./logs",
                "backup_enabled": True,
                "compression_enabled": True,
                "retention_days": 30
            },
            "agents_configurations": {}
        }
        
        # Générer config pour chaque agent
        for agent_id, base_config in self.agents_configs.items():
            agent_config = self._generer_config_agent(agent_id, base_config)
            configuration_complete["agents_configurations"][agent_id] = agent_config
        
        # Sauvegarde configuration
        config_file = CONFIG_DIR / f"agents_logging_config_{self.timestamp}.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(configuration_complete, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Configuration sauvegardée: {config_file}")
        return configuration_complete

    def _generer_config_agent(self, agent_id: str, base_config: Dict[str, Any]) -> Dict[str, Any]:
        """Génère la configuration spécialisée pour un agent"""
        
        # Configuration de base LoggingManager
        logging_config = {
            "logger_name": f"nextgen.agent.{agent_id}",
            "level": base_config["logging_level"],
            "handlers": {
                "console": {
                    "enabled": True,
                    "level": "INFO",
                    "format": "detailed"
                },
                "file": {
                    "enabled": True,
                    "path": f"./logs/{agent_id}_{self.timestamp}.log",
                    "level": base_config["logging_level"],
                    "rotation": "daily",
                    "compression": True
                },
                "elasticsearch": {
                    "enabled": base_config["elasticsearch_enabled"],
                    "index": f"agents-{agent_id}",
                    "level": "INFO",
                    "buffer_size": 100
                }
            },
            "metrics": {
                "enabled": base_config["metrics_enabled"],
                "collection_interval": 60,
                "specialized_metrics": base_config["specialized_handlers"]
            },
            "security": {
                "level": base_config["security_level"],
                "encryption_enabled": base_config.get("security_level") in ["high", "critical"],
                "audit_trail": True
            }
        }
        
        # Configuration rapports
        reports_config = {
            "format": base_config["report_format"],
            "output_directory": str(REPORTS_DIR / agent_id),
            "structure": base_config["report_structure"],
            "auto_generation": True,
            "versioning": True,
            "backup": True
        }
        
        # Configuration spécialisée selon le type d'agent
        specialized_config = self._generer_config_specialisee(agent_id, base_config)
        
        return {
            "agent_id": agent_id,
            "logging": logging_config,
            "reports": reports_config,
            "specialized": specialized_config,
            "integration": {
                "logging_manager_import": "import sys
from pathlib import Path
from core import logging_manager",
                "initialization_code": f"self.logger = logging_manager.get_logger('custom_agent_logger', custom_config={'logger_name': 'Agent', 'extra_fields': {}})",
                "report_method": f"self.logger.log_structured_report(report_data, '{base_config['report_format']}')"
            }
        }

    def _generer_config_specialisee(self, agent_id: str, base_config: Dict[str, Any]) -> Dict[str, Any]:
        """Génère la configuration spécialisée selon le type d'agent"""
        
        if "coordinateur" in agent_id:
            return {
                "coordination_metrics": ["team_velocity", "sprint_progress", "blockers_count"],
                "team_monitoring": True,
                "dashboard_generation": True,
                "stakeholder_reports": True
            }
        
        elif "auditeur_qualite" in agent_id:
            return {
                "quality_metrics": ["code_coverage", "technical_debt", "complexity_score"],
                "automated_analysis": True,
                "quality_gates": True,
                "trend_analysis": True
            }
        
        elif "testeur" in agent_id:
            return {
                "test_metrics": ["pass_rate", "coverage", "execution_time"],
                "automated_reporting": True,
                "failure_analysis": True,
                "performance_tracking": True
            }
        
        elif "peer_reviewer" in agent_id:
            return {
                "review_metrics": ["review_time", "feedback_quality", "approval_rate"],
                "collaboration_tracking": True,
                "knowledge_sharing": True,
                "mentoring_metrics": "senior" in agent_id
            }
        
        elif "auditeur_securite" in agent_id:
            return {
                "security_metrics": ["vulnerability_count", "risk_score", "compliance_rate"],
                "threat_monitoring": True,
                "incident_tracking": True,
                "compliance_reporting": True,
                "confidentiality_level": "restricted"
            }
        
        elif "auditeur_performance" in agent_id:
            return {
                "performance_metrics": ["response_time", "throughput", "resource_usage"],
                "bottleneck_detection": True,
                "optimization_tracking": True,
                "benchmark_comparison": True
            }
        
        elif "auditeur_conformite" in agent_id:
            return {
                "compliance_metrics": ["standards_adherence", "gap_count", "action_items"],
                "regulatory_tracking": True,
                "audit_trail": True,
                "certification_status": True
            }
        
        else:
            return {
                "generic_metrics": ["execution_time", "success_rate", "error_count"],
                "basic_monitoring": True
            }

    def generer_scripts_integration(self) -> List[str]:
        """
        🚀 Génère les scripts d'intégration pour chaque agent
        
        Returns:
            Liste des chemins des scripts générés
        """
        print("🚀 Génération scripts d'intégration...")
        
        scripts_generes = []
        
        for agent_id in self.agents_configs.keys():
            script_path = self._generer_script_integration_agent(agent_id)
            scripts_generes.append(script_path)
        
        print(f"✅ {len(scripts_generes)} scripts d'intégration générés")
        return scripts_generes

    def _generer_script_integration_agent(self, agent_id: str) -> str:
        """Génère le script d'intégration pour un agent spécifique"""
        
        script_content = f'''#!/usr/bin/env python3
"""
🔧 SCRIPT D'INTÉGRATION LOGGING - {agent_id.upper()}
Intègre l'agent au système de logging NextGeneration

Généré automatiquement le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

import sys
from pathlib import Path

# Ajouter le chemin du système de logging
sys.path.insert(0, str(Path(__file__).parent))

import sys
from pathlib import Path
from core import logging_manager

class {agent_id.replace('_', '').title()}LoggingIntegration:
    """
    Intégration logging pour {agent_id}
    """
    
    def __init__(self, agent_instance):
        self.agent = agent_instance
        self.logger = logging_manager.get_logger('custom_agent_logger', custom_config={'logger_name': 'Agent', 'extra_fields': {}})
        
        # Configuration spécialisée
        self.reports_dir = Path(__file__).parent / "reports_equipe_agents" / "{agent_id}"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"🚀 Intégration logging activée pour {{self.agent.__class__.__name__}}")
    
    def log_mission_start(self, mission_data: dict):
        """Log le démarrage d'une mission"""
        self.logger.info(f"🎯 Démarrage mission: {{mission_data.get('mission_type', 'unknown')}}")
        self.logger.log_structured_data("mission_start", mission_data)
    
    def log_mission_progress(self, progress_data: dict):
        """Log le progrès d'une mission"""
        self.logger.info(f"📊 Progrès mission: {{progress_data.get('completion_rate', 0)}}%")
        self.logger.log_structured_data("mission_progress", progress_data)
    
    def log_mission_completion(self, result_data: dict):
        """Log la completion d'une mission"""
        self.logger.info(f"✅ Mission terminée - Score: {{result_data.get('score', 'N/A')}}")
        self.logger.log_structured_data("mission_completion", result_data)
        
        # Génération rapport structuré
        self._generate_structured_report(result_data)
    
    def log_error(self, error_data: dict):
        """Log une erreur avec contexte"""
        self.logger.error(f"❌ Erreur: {{error_data.get('message', 'Unknown error')}}")
        self.logger.log_structured_data("error", error_data)
    
    def _generate_structured_report(self, result_data: dict):
        """Génère un rapport structuré dans le répertoire autorisé"""
        import json
        from datetime import datetime
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.reports_dir / f"rapport_{{timestamp}}.json"
        
        structured_report = {{
            "agent_id": "{agent_id}",
            "timestamp": datetime.now().isoformat(),
            "mission_data": result_data,
            "logging_metrics": self.logger.get_metrics() if hasattr(self.logger, 'get_metrics') else {{}},
            "report_version": "1.0.0"
        }}
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(structured_report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"📄 Rapport structuré généré: {{report_file}}")
        return str(report_file)

def integrate_logging(agent_instance):
    """
    🚀 Point d'entrée pour intégrer le logging à un agent
    
    Usage:
        from {agent_id}_logging_integration import integrate_logging
        logging_integration = integrate_logging(mon_agent)
    """
    return {agent_id.replace('_', '').title()}LoggingIntegration(agent_instance)

# Test d'intégration
if __name__ == "__main__":
    print(f"🔧 Test intégration logging pour {agent_id}")
    
    # Simulation d'agent
    class MockAgent:
        def __init__(self):
            self.name = "{agent_id}"
    
    mock_agent = MockAgent()
    integration = integrate_logging(mock_agent)
    
    # Test des fonctionnalités
    integration.log_mission_start({{"mission_type": "test", "target": "logging_validation"}})
    integration.log_mission_progress({{"completion_rate": 50, "current_phase": "analysis"}})
    integration.log_mission_completion({{"score": 8.5, "status": "success", "findings": ["Test successful"]}})
    
    print("✅ Test d'intégration réussi")
'''
        
        # Sauvegarde script
        script_file = CONFIG_DIR / f"{agent_id}_logging_integration.py"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return str(script_file)

    def generer_documentation_integration(self) -> str:
        """Génère la documentation d'intégration"""
        
        doc_content = f"""# 📚 **DOCUMENTATION INTÉGRATION LOGGING AGENTS**

## 🎯 **Objectif**
Documentation pour intégrer le système de logging NextGeneration dans chaque agent spécialisé.

## 🚀 **Agents Configurés**

"""
        
        for agent_id, config in self.agents_configs.items():
            doc_content += f"""
### 🤖 **{agent_id.replace('_', ' ').title()}**

**Configuration:**
- **Niveau de logging:** {config['logging_level']}
- **Format rapport:** {config['report_format']}
- **Sécurité:** {config['security_level']}
- **Handlers spécialisés:** {', '.join(config['specialized_handlers'])}

**Intégration:**
```python
# Import
from {agent_id}_logging_integration import integrate_logging

# Dans votre agent
class MonAgent:
    def __init__(self):
        self.logging_integration = integrate_logging(self)
    
    def execute_mission(self, mission_data):
        # Log démarrage
        self.logging_integration.log_mission_start(mission_data)
        
        try:
            # Votre logique métier
            result = self.process_mission(mission_data)
            
            # Log completion
            self.logging_integration.log_mission_completion(result)
            return result
            
        except Exception as e:
            # Log erreur
            self.logging_integration.log_error({{"message": str(e), "context": mission_data}})
            raise
```

**Répertoire des rapports:** `./reports_equipe_agents/{agent_id}/`

"""
        
        doc_content += f"""

## 📋 **Instructions Générales**

### 1. **Installation**
```bash
# Copier les scripts d'intégration
cp config/*_logging_integration.py ./

# Vérifier le système de logging
python logging_manager_optimized.py --test
```

### 2. **Configuration**
```python
# Charger la configuration
import json
with open('config/agents_logging_config_{self.timestamp}.json') as f:
    config = json.load(f)
```

### 3. **Utilisation Standard**
```python
# Pour chaque agent
import sys
from pathlib import Path
from core import logging_manager

class MonAgent:
    def __init__(self):
        self.logger = logging_manager.get_logger('custom_agent_logger', custom_config={'logger_name': 'Agent', 'extra_fields': {}})
    
    def process(self, data):
        self.logger.info("🚀 Démarrage traitement")
        # ... votre logique
        self.logger.info("✅ Traitement terminé")
```

### 4. **Rapports Structurés**
Tous les rapports sont automatiquement sauvegardés dans `./reports_equipe_agents/` avec:
- **Format JSON structuré**
- **Horodatage automatique** 
- **Métriques de logging intégrées**
- **Versioning des rapports**

## 🎯 **Validation**

Pour valider l'intégration:
```bash
python orchestrateur_equipe_agents_logging.py
```

---

*Documentation générée automatiquement le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # Sauvegarde documentation
        doc_file = CONFIG_DIR / f"DOCUMENTATION_INTEGRATION_AGENTS_{self.timestamp}.md"
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write(doc_content)
        
        print(f"📚 Documentation générée: {doc_file}")
        return str(doc_file)


def main():
    """Point d'entrée principal"""
    print("🔧 CONFIGURATION AGENTS - LOGGING NEXTGENERATION")
    print("=" * 60)
    
    configurateur = ConfigurationAgentsLogging()
    
    try:
        # 1. Génération configuration complète
        print("\n📋 Étape 1: Génération configuration complète...")
        config = configurateur.generer_configuration_complete()
        print(f"✅ Configuration générée pour {len(config['agents_configurations'])} agents")
        
        # 2. Génération scripts d'intégration
        print("\n🚀 Étape 2: Génération scripts d'intégration...")
        scripts = configurateur.generer_scripts_integration()
        print(f"✅ {len(scripts)} scripts d'intégration générés")
        
        # 3. Génération documentation
        print("\n📚 Étape 3: Génération documentation...")
        doc_path = configurateur.generer_documentation_integration()
        print(f"✅ Documentation générée: {Path(doc_path).name}")
        
        print("\n🎯 CONFIGURATION TERMINÉE AVEC SUCCÈS")
        print(f"📂 Fichiers générés dans: {CONFIG_DIR}")
        print(f"📄 Rapports seront dans: {REPORTS_DIR}")
        
        # Instructions suivantes
        print("\n🚀 PROCHAINES ÉTAPES:")
        print("1. Exécuter: python orchestrateur_equipe_agents_logging.py")
        print("2. Vérifier les rapports dans ./reports_equipe_agents/")
        print("3. Intégrer les scripts dans vos agents existants")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 




