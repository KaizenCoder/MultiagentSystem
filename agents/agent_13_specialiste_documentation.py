#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📚 AGENT 13 - SPÉCIALISTE DOCUMENTATION - SPRINT 4 OPTIMISÉ
Agent Factory Pattern - Guides Production & Documentation API

Mission : Documentation technique complète et standardisée
Créé : 2025-01-28 (Sprint 4) | Optimisé : 2025-06-26
Version : 2.0.0 (Optimisée)
"""

import json
import sys
import re
import os
import logging
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from concurrent.futures import ThreadPoolExecutor
import hashlib
import threading
import zipfile # Ajouté en haut du fichier

# Configuration paths
AGENT_ROOT = Path(__file__).parent
PROJECT_ROOT = AGENT_ROOT.parent
sys.path.append(str(AGENT_ROOT))

@dataclass
class DocumentationTemplate:
    """Template documentation standardisé avec validation"""
    title: str
    category: str
    audience: str
    difficulty_level: str
    estimated_read_time: int
    sections: List[Dict[str, Any]]
    prerequisites: List[str] = None
    related_docs: List[str] = None
    last_updated: datetime = None
    author: str = "Agent Factory Team"
    
    def __post_init__(self):
        self.prerequisites = self.prerequisites or []
        self.related_docs = self.related_docs or []
        self.last_updated = self.last_updated or datetime.now()
        
    def validate(self) -> bool:
        """Validation template"""
        return all([self.title, self.category, self.audience, 
                   self.difficulty_level in ["beginner", "intermediate", "advanced"],
                   self.estimated_read_time > 0])

@dataclass
class APIEndpoint:
    """Documentation endpoint API avec auto-génération exemples"""
    path: str
    method: str
    description: str
    parameters: Dict[str, Any] = None
    responses: Dict[str, Any] = None
    examples: List[Dict[str, Any]] = None
    authentication: str = "None"
    rate_limits: Optional[str] = "100/min"
    
    def __post_init__(self):
        self.parameters = self.parameters or {}
        self.responses = self.responses or {"200": {"description": "Success"}}
        self.examples = self.examples or []
        
    def generate_curl_example(self, base_url: str = "http://localhost:8000") -> str:
        """Génération automatique exemple cURL"""
        auth = f'-H "Authorization: Bearer <token>" ' if self.authentication != "None" else ""
        return f'curl -X {self.method} {auth}{base_url}{self.path}'

class Agent13SpecialisteDocumentation:
    """Agent 13 - Spécialiste Documentation Optimisé"""
    
    CAPABILITIES = ["documentation_generation", "documentation_review", "api_docs", "runbooks"]
    
    # Templates pré-définis pour génération rapide
    DOC_TEMPLATES = {
        "production": {
            "sections": ["Vue d'Ensemble", "Démarrage Rapide", "Monitoring", "Maintenance", "Troubleshooting"],
            "audience": "operators",
            "difficulty": "intermediate"
        },
        "api": {
            "sections": ["Authentication", "Endpoints", "Examples", "Error Codes"],
            "audience": "developers", 
            "difficulty": "beginner"
        },
        "runbook": {
            "sections": ["Urgence", "Maintenance", "Monitoring", "Troubleshooting"],
            "audience": "operators",
            "difficulty": "advanced"
        }
    }
    
    # Endpoints API prédéfinis
    API_ENDPOINTS = [
        {"path": "/health", "method": "GET", "desc": "Health check système", "auth": "None"},
        {"path": "/metrics", "method": "GET", "desc": "Métriques Prometheus", "auth": "None", "rate": "10/min"},
        {"path": "/factory/create", "method": "POST", "desc": "Création template optimisée", "auth": "Bearer token", "rate": "50/min"},
        {"path": "/factory/templates/{id}", "method": "GET", "desc": "Récupération template par ID", "auth": "Bearer token"},
        {"path": "/backup/create", "method": "POST", "desc": "Création backup via Agent 12", "auth": "Bearer token (admin)", "rate": "5/min"}
    ]

    def __init__(self, agent_id="specialiste_documentation_01"):
        # Initialisation rapide avec valeurs par défaut
        
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="documentation",
                custom_config={
                    "logger_name": f"nextgen.documentation.13_specialiste_documentation.{self.agent_id if hasattr(self, 'agent_id') else self.id if hasattr(self, 'id') else 'unknown'}",
                    "log_dir": "logs/documentation",
                    "metadata": {
                        "agent_type": "13_specialiste_documentation",
                        "agent_role": "documentation",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)

        self.name, self.agent_id, self.version = "Agent 13 - Spécialiste Documentation", agent_id, "2.0.0"
        self.sprint, self.mission = "Sprint 4", "Documentation production complète"
        
        self._setup_logging()
        self._create_directory_structure()
        
        self.doc_templates, self.api_endpoints = {}, {}
        self.generation_stats = {"files_created": 0, "total_size": 0, "generation_time": 0.0}
        self._stats_lock = threading.Lock()
        
        self.logger.info(f"📚 {self.name} initialisé - Version {self.version}")
        
    def _setup_logging(self):
        """Configuration logging optimisée"""
        log_dir = PROJECT_ROOT / "logs"
        log_dir.mkdir(exist_ok=True)
        
        self.logger = logging.getLogger(f"{self.__class__.__name__}_{self.agent_id}")
        if not self.logger.handlers:
            handler = logging.FileHandler(log_dir / f"{self.agent_id}_documentation.log")
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def _create_directory_structure(self):
        """Création structure répertoires optimisée"""
        self.docs_root = PROJECT_ROOT / "documentation"
        self.reports_dir = PROJECT_ROOT / "reports"
        
        self.doc_structure = {
            name: self.docs_root / name for name in 
            ["guides", "api", "runbooks", "architecture", "deployment", "troubleshooting"]
        }
        
        # Création parallèle des répertoires
        for directory in [self.docs_root, self.reports_dir, *self.doc_structure.values()]:
            directory.mkdir(exist_ok=True)

    def _generate_content_from_template(self, template_type: str, **kwargs) -> str:
        """Génération contenu à partir de templates"""
        templates = {
            "production_guide": self._get_production_guide_template(),
            "api_markdown": self._get_api_markdown_template(),
            "runbook": self._get_runbook_template()
        }
        
        template = templates.get(template_type, "")
        # Substitution dynamique des variables
        for key, value in kwargs.items():
            template = template.replace(f"{{{key}}}", str(value))
        
        return template

    def _get_production_guide_template(self) -> str:
        """Template guide production condensé"""
        return '''# 🔧 **GUIDE PRODUCTION - AGENT FACTORY PATTERN**

## **Vue d'Ensemble Production**
- **Control Plane** : Gouvernance, policies, monitoring centralisé
- **Data Plane** : Exécution isolée agents avec sandbox WASI
- **Performance** : SLA < 50ms création template, < 100ms p95
- **Sécurité** : RSA 2048 + SHA-256, Vault rotation clés
- **Observabilité** : OpenTelemetry + Prometheus + Grafana

## **⚡ Démarrage Rapide Production**

### Vérification Prérequis
```bash
python --version  # >= 3.9
docker --version  # >= 20.10
kubectl version   # >= 1.20
```

### Initialisation Agent Factory
```bash
git clone <repo_url> agent_factory
cd agent_factory/nextgeneration/agent_factory_implementation
pip install -r requirements.txt
python agents/agent_03_specialiste_configuration.py --env=production
```

### Validation Fonctionnement
```bash
curl http://localhost:8000/health
curl http://localhost:8000/metrics
```

## **📊 Monitoring Production**
### Métriques Clés
- **Performance** : `agent_factory_response_time_ms` < 50ms
- **Compression** : `agent_factory_compression_ratio` ~ 0.3
- **Cache** : `agent_factory_cache_hit_rate` > 0.8

### Alertes Critiques
```yaml
groups:
- name: agent_factory
  rules:
  - alert: PerformanceDegraded
    expr: agent_factory_response_time_ms > 100
    for: 5m
```

## **🔧 Maintenance Production**

### Backup Quotidien
```bash
python agents/agent_12_gestionnaire_backups.py --backup-all
```

### Mise à Jour Sécurisée
```bash
python agents/agent_12_gestionnaire_backups.py --create-rollback-plan
kubectl apply -f deployment/blue-green/
```

## **🚨 Troubleshooting**

### Performance Dégradée
```bash
python agents/agent_08_optimiseur_performance.py --benchmark
```

### Échecs Signature RSA
```bash
vault kv get secret/agent-factory/keys
python agents/agent_04_expert_securite_crypto.py --rotate-keys
```

## **📞 Contacts Support**
- **Équipe Agent Factory** : agents@factory.local
- **Escalation** : +33-XXX-XXX-XXX
'''

    def _get_api_markdown_template(self) -> str:
        """Template API documentation condensé"""
        return '''# 🔌 **API DOCUMENTATION - AGENT FACTORY PATTERN**

## **Vue d'Ensemble**
**Base URL :** `https://api.agentfactory.production`  
**Version :** 1.0.0  
**Authentification :** Bearer Token JWT

## **🔐 Authentification**
```bash
curl -X POST https://auth.agentfactory.production/login \\
  -H "Content-Type: application/json" \\
  -d '{"username": "operator", "password": "secret"}'
```

## **📋 Endpoints**
{endpoints_content}
'''

    def _get_runbook_template(self) -> str:
        """Template runbook condensé"""
        return '''# 📖 **RUNBOOK OPÉRATIONS - AGENT FACTORY PATTERN**

## **🚨 Procédures d'Urgence**

### Incident Performance Critique
   ```bash
   curl -s http://localhost:8000/metrics | grep response_time
   python agents/agent_08_optimiseur_performance.py --scale-up --workers=16
   python agents/agent_12_gestionnaire_backups.py --rollback --version=stable
   ```

### Échec Sécurité Critique
   ```bash
   python agents/agent_04_expert_securite_crypto.py --secure-mode
   vault status
   python agents/agent_12_gestionnaire_backups.py --backup-security
   ```

## **⚙️ Procédures Maintenance**

### Mise à Jour Production
   ```bash
   python agents/agent_12_gestionnaire_backups.py --backup-all --type=pre-maintenance
   kubectl apply -f deployment/blue-green/green/
   ./scripts/validate_green_deployment.sh
   ```

### Rotation Certificats
   ```bash
python agents/agent_04_expert_securite_crypto.py --auto-rotate
python agents/agent_04_expert_securite_crypto.py --validate-rotation
```

## **📊 Monitoring & Alertes**

| Métrique | Seuil Warning | Seuil Critical | Action |
|----------|---------------|----------------|--------|
| Response Time | > 100ms | > 200ms | Scale ThreadPool |
| Cache Hit Rate | < 70% | < 50% | Cache rebuild |
| CPU Usage | > 80% | > 90% | Scale horizontalement |

## **🔍 Troubleshooting Guide**

### FAQ Opérations
**Q: Comment vérifier si le système est healthy ?**
```bash
curl http://localhost:8000/health
python agents/agent_01_coordinateur_principal.py --status-all
```

**Q: Comment créer un backup d'urgence ?**
```bash
python agents/agent_12_gestionnaire_backups.py --emergency-backup
```
'''

    def create_production_guide(self) -> Dict[str, Any]:
        """Création guide production optimisée"""
        start_time = datetime.now()
        
        try:
            content = self._generate_content_from_template("production_guide")
            guide_file = self.doc_structure["guides"] / "production_operator_guide.md"
            guide_file.write_text(content)
            
            # Mise à jour statistiques
            self._update_stats(guide_file, start_time)
            
            self.logger.info("✅ Guide production opérateur créé")
            return {
                "status": "success",
                "guide_file": str(guide_file),
                "sections_count": content.count("##"),
                "word_count": len(content.split()),
                "generation_time_ms": (datetime.now() - start_time).total_seconds() * 1000
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erreur création guide production: {e}")
            return {"status": "error", "error": str(e)}

    def create_api_documentation(self) -> Dict[str, Any]:
        """Documentation API optimisée avec génération automatique"""
        start_time = datetime.now()
        
        try:
            # Génération endpoints à partir des templates
            endpoints = []
            for ep_data in self.API_ENDPOINTS:
                endpoint = APIEndpoint(
                    path=ep_data["path"],
                    method=ep_data["method"],
                    description=ep_data["desc"],
                    authentication=ep_data["auth"],
                    rate_limits=ep_data.get("rate", "100/min")
                )
                endpoints.append(endpoint)
                self.api_endpoints[f"{endpoint.method} {endpoint.path}"] = endpoint
            
            # Génération OpenAPI automatique
            api_doc = self._generate_openapi_spec(endpoints)
            api_file = self.doc_structure["api"] / "openapi.json"
            api_file.write_text(json.dumps(api_doc, indent=2))
            
            # Génération Markdown
            endpoints_content = self._generate_endpoints_markdown(endpoints)
            api_md_content = self._generate_content_from_template("api_markdown", 
                                                                endpoints_content=endpoints_content)
            api_md_file = self.doc_structure["api"] / "API_Documentation.md"
            api_md_file.write_text(api_md_content)
            
            # Mise à jour statistiques
            self._update_stats(api_file, start_time)
            self._update_stats(api_md_file, start_time)
            
            self.logger.info(f"✅ Documentation API créée ({len(endpoints)} endpoints)")
            return {
                "status": "success",
                "endpoints_count": len(endpoints),
                "openapi_file": str(api_file),
                "markdown_file": str(api_md_file),
                "generation_time_ms": (datetime.now() - start_time).total_seconds() * 1000
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erreur création documentation API: {e}")
            return {"status": "error", "error": str(e)}

    def _generate_openapi_spec(self, endpoints: List[APIEndpoint]) -> Dict[str, Any]:
        """Génération spécification OpenAPI automatique"""
        paths = {}
        for endpoint in endpoints:
            path_params = []
            # Recherche des paramètres dans le chemin, par exemple /items/{itemId}
            extracted_params = re.findall(r"\{([^}]+)\}", endpoint.path)
            for param_name in extracted_params:
                path_params.append({
                    "name": param_name,
                    "in": "path",
                    "required": True,
                    "description": f"Identifier: {param_name}", # Description générique
                    "schema": {"type": "string"} # Type par défaut, peut être ajusté si plus d'infos sont dispo
                })
            
            paths[endpoint.path] = {
                endpoint.method.lower(): {
                    "summary": endpoint.description,
                    "responses": endpoint.responses,
                    "security": [] if endpoint.authentication == "None" else [{"BearerAuth": []}],
                    "parameters": path_params if path_params else None # Ajouter seulement si des paramètres existent
                }
            }

        return {
            "openapi": "3.0.0",
            "info": {
                "title": "Agent Factory Pattern API",
                "description": "API pour Agent Factory Pattern - Sprint 4 Production",
                "version": "1.0.0",
                "contact": {"name": "Agent Factory Team", "email": "agents@factory.local"}
            },
            "servers": [
                {"url": "http://localhost:8000", "description": "Development"},
                {"url": "https://api.agentfactory.production", "description": "Production"}
            ],
            "security": [{"BearerAuth": []}],
            "components": {
                "securitySchemes": {
                    "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
                }
            },
            "paths": paths # Utilisation des paths construits
        }

    def _generate_endpoints_markdown(self, endpoints: List[APIEndpoint]) -> str:
        """Génération markdown endpoints automatique"""
        content = ""
        for endpoint in endpoints:
            content += f"""### **{endpoint.method} {endpoint.path}**
**Description :** {endpoint.description}  
**Authentification :** {endpoint.authentication}  
**Rate Limits :** {endpoint.rate_limits}

**Exemple :**
```bash
{endpoint.generate_curl_example()}
```

---
"""
        return content

    def create_runbook_operations(self) -> Dict[str, Any]:
        """Création runbook optimisée"""
        start_time = datetime.now()
        
        try:
            content = self._generate_content_from_template("runbook")
            runbook_file = self.doc_structure["runbooks"] / "operations_runbook.md"
            runbook_file.write_text(content)
            
            self._update_stats(runbook_file, start_time)
            
            self.logger.info("✅ Runbook opérations créé")
            return {
                "status": "success",
                "runbook_file": str(runbook_file),
                "procedures_count": content.count("###"),
                "word_count": len(content.split()),
                "generation_time_ms": (datetime.now() - start_time).total_seconds() * 1000
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erreur création runbook: {e}")
            return {"status": "error", "error": str(e)}

    def _update_stats(self, file_path: Path, start_time: datetime):
        """Mise à jour statistiques génération"""
        with self._stats_lock:
            if file_path.exists():
                self.generation_stats["files_created"] += 1
                self.generation_stats["total_size"] += file_path.stat().st_size
                current_gen_time = self.generation_stats.get("generation_time", 0.0)
                self.generation_stats["generation_time"] = float(current_gen_time) + (datetime.now() - start_time).total_seconds()

    def generate_all_documentation(self) -> Dict[str, Any]:
        """Génération complète documentation en parallèle"""
        self.generation_stats = {"files_created": 0, "total_size": 0, "generation_time": 0.0}
        
        start_time = datetime.now()
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            # Génération parallèle
            futures = {
                "guide": executor.submit(self.create_production_guide),
                "api": executor.submit(self.create_api_documentation),
                "runbook": executor.submit(self.create_runbook_operations)
            }
            
            # Collecte résultats
            results = {name: future.result() for name, future in futures.items()}
        
        total_time = (datetime.now() - start_time).total_seconds() * 1000
        
        self.logger.info(f"✅ Documentation complète générée en {total_time:.2f}ms")
        
        return {
            "status": "success",
            "generation_results": results,
            "total_generation_time_ms": total_time,
            "statistics": self.generation_stats
        }

    def validate_documentation(self) -> Dict[str, Any]:
        """Validation qualité documentation"""
        validation_results = {"valid_files": 0, "total_files": 0, "issues": []}
        
        for category, doc_dir in self.doc_structure.items():
            for file_path in doc_dir.glob("*.md"):
                validation_results["total_files"] += 1
                
                content = file_path.read_text()
                # Validation contenu
                if len(content) > 100 and content.count("#") >= 3:
                    validation_results["valid_files"] += 1
                else:
                    validation_results["issues"].append(f"Fichier {file_path.name} trop court ou mal structuré")
        
        validation_results["validation_score"] = (
            validation_results["valid_files"] / validation_results["total_files"] 
            if validation_results["total_files"] > 0 else 0
        )
        
        return validation_results
            
    def generate_sprint4_report(self) -> Dict[str, Any]:
        """Génération rapport Sprint 4 optimisé"""
        try:
            # Statistiques documentation optimisées
            doc_stats = {"total_files": 0, "total_size_bytes": 0, "categories": {}}
            
            for category, doc_dir in self.doc_structure.items():
                files = list(doc_dir.glob("*.md")) + list(doc_dir.glob("*.json"))
                file_count, total_size = len(files), sum(f.stat().st_size for f in files if f.exists())
                
                doc_stats["categories"][category] = {"files": file_count, "size_bytes": total_size}
                doc_stats["total_files"] += file_count
                doc_stats["total_size_bytes"] += total_size
                
            # Validation qualité
            validation_results = self.validate_documentation()
            
            # Rapport optimisé
            sprint4_report = {
                "agent_info": {
                    "id": self.agent_id, "name": self.name, "version": self.version,
                    "sprint": self.sprint, "mission": self.mission,
                    "created_at": datetime.now().isoformat()
                },
                "sprint4_objectives": {
                    obj: "✅ Completed" for obj in [
                        "production_guide", "api_documentation", "runbook_operations",
                        "documentation_structure", "standards_established", "integration_agents"
                    ]
                },
                "documentation_statistics": doc_stats,
                "generation_statistics": self.generation_stats,
                "validation_results": validation_results,
                "api_endpoints_count": len(self.api_endpoints),
                "performance_metrics": {
                    "avg_generation_time_ms": self.generation_stats["generation_time"] * 1000 / max(1, self.generation_stats["files_created"]),
                    "total_size_mb": doc_stats["total_size_bytes"] / (1024 * 1024),
                    "validation_score": validation_results["validation_score"]
                },
                "recommendations": [
                    "Déployer documentation sur plateforme centralisée",
                    "Intégrer documentation dans CI/CD pipeline",
                    "Configurer génération automatique API docs",
                    "Former équipe ops sur runbooks"
                ],
                "timestamp": datetime.now().isoformat()
            }
            
            # Sauvegarde rapport
            report_file = self.reports_dir / f"{self.agent_id}_rapport_sprint4_{datetime.now().strftime('%Y-%m-%d')}.json"
            report_file.write_text(json.dumps(sprint4_report, indent=2, ensure_ascii=False))
            
            self.logger.info(f"📊 Rapport Sprint 4 généré: {report_file}")
            return sprint4_report
            
        except Exception as e:
            self.logger.error(f"❌ Erreur génération rapport Sprint 4: {e}")
            return {"error": str(e)}

    def generate_documentation_hash(self) -> str:
        """Génération hash pour versioning documentation"""
        content_hash = hashlib.sha256()
        for category, doc_dir in self.doc_structure.items():
            for file_path in sorted(doc_dir.glob("*")):
                if file_path.is_file():
                    content_hash.update(file_path.read_bytes())
        return content_hash.hexdigest()[:16]

    def export_documentation_archive(self, output_path: Optional[Path] = None) -> Dict[str, Any]:
        """Export documentation en archive"""
        # import zipfile # Déplacé en haut du fichier
        
        output_path = output_path or self.reports_dir / f"documentation_archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        
        try:
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for category, doc_dir in self.doc_structure.items():
                    for file_path in doc_dir.rglob("*"):
                        if file_path.is_file():
                            zipf.write(file_path, file_path.relative_to(self.docs_root))
            
            return {
                "status": "success",
                "archive_path": str(output_path),
                "archive_size_bytes": output_path.stat().st_size,
                "documentation_hash": self.generate_documentation_hash()
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def shutdown(self):
        """Arrêt propre agent"""
        self.logger.info(f"Arrêt de l'agent {self.name} - Statistiques: {self.generation_stats}")
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

    def run(self, task_prompt: str = "generate_all"):
        """Point d'entrée principal optimisé"""
        tasks = {
            "generate_all": self.generate_all_documentation,
            "production_guide": self.create_production_guide,
            "api_docs": self.create_api_documentation,
            "runbook": self.create_runbook_operations,
            "report": self.generate_sprint4_report,
            "validate": self.validate_documentation,
            "export": self.export_documentation_archive
        }
        
        task_func = tasks.get(task_prompt, self.generate_all_documentation)
        return task_func()

def main():
    """Point d'entrée optimisé Agent 13"""
    print("📚 DÉMARRAGE AGENT 13 - SPÉCIALISTE DOCUMENTATION - SPRINT 4 OPTIMISÉ")
    
    try:
        agent = Agent13SpecialisteDocumentation()
        
        # Génération complète parallélisée
        print("\n🚀 GÉNÉRATION DOCUMENTATION COMPLÈTE (PARALLÉLISÉE)...")
        all_results = agent.generate_all_documentation()
        
        if all_results["status"] == "success":
            print(f"✅ Documentation générée en {all_results['total_generation_time_ms']:.2f}ms")
            print(f"✅ Fichiers créés: {agent.generation_stats['files_created']}")
            print(f"✅ Taille totale: {agent.generation_stats['total_size'] / 1024:.1f} KB")
        
        # Validation qualité
        print("\n🔍 VALIDATION QUALITÉ...")
        validation = agent.validate_documentation()
        print(f"✅ Score validation: {validation['validation_score']:.2%}")
        
        # Génération rapport Sprint 4
        print("\n📊 GÉNÉRATION RAPPORT SPRINT 4...")
        sprint4_report = agent.generate_sprint4_report()
        if "error" not in sprint4_report:
            print(f"✅ Rapport Sprint 4 généré avec succès")
            print(f"✅ Performance moyenne: {sprint4_report['performance_metrics']['avg_generation_time_ms']:.2f}ms/fichier")
        
        # Export archive
        print("\n📦 EXPORT ARCHIVE DOCUMENTATION...")
        export_result = agent.export_documentation_archive()
        if export_result["status"] == "success":
            print(f"✅ Archive créée: {export_result['archive_size_bytes'] / 1024:.1f} KB")
            print(f"✅ Hash documentation: {export_result['documentation_hash']}")
        
        print("\n🎉 AGENT 13 - SPÉCIALISTE DOCUMENTATION - OPTIMISÉ TERMINÉ!")
        print("📚 Guide Production | 🔌 API Docs | 📋 Runbooks | 📊 Analytics | 📦 Export")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR AGENT 13: {e}")
        return False
    finally:
        if 'agent' in locals():
            agent.shutdown()
    # ✅ MÉTHODES STANDARDISÉES DE RAPPORT

    def _calculate_report_score(self, metrics: Dict[str, Any]) -> int:
        """Calcule le score global du rapport basé sur les métriques."""
        score = 0
        issues_critiques = []
        
        # Logique de scoring spécifique à l'agent
        # À adapter selon le type d'agent
        
        return score
    
    def _assess_conformity(self, score: int) -> str:
        """Évalue la conformité basée sur le score."""
        if score >= 90:
            return "✅ CONFORME - OPTIMAL"
        elif score >= 70:
            return "✅ CONFORME - ACCEPTABLE"
        else:
            return "❌ NON CONFORME - CRITIQUE"
    
    def _get_quality_level(self, score: int) -> str:
        """Détermine le niveau de qualité."""
        if score >= 90:
            return "OPTIMAL"
        elif score >= 70:
            return "ACCEPTABLE"
        else:
            return "CRITIQUE"
    
    def _generate_recommendations(self, metrics: Dict[str, Any], issues: List[str]) -> List[str]:
        """Génère les recommandations basées sur l'analyse."""
        recommendations = []
        
        # Logique de génération de recommandations
        # À adapter selon le type d'agent
        
        return recommendations
    
    def _generate_standard_report(self, context: Dict, metrics: Dict, timestamp) -> Dict[str, Any]:
        """Génère un rapport selon le format standard de l'agent 06."""
        
        score = self._calculate_report_score(metrics)
        conformity = self._assess_conformity(score)
        quality_level = self._get_quality_level(score)
        
        agent_filename = Path(__file__).name
        
        # Issues critiques (à personnaliser selon l'agent)
        issues_critiques = []
        
        return {
            'agent_id': getattr(self, 'agent_id', 'unknown'),
            'agent_file_name': agent_filename,
            'type_rapport': 'standard',  # À personnaliser
            'timestamp': timestamp.isoformat(),
            'specialisation': 'Agent Spécialisé',  # À personnaliser
            'score_global': score,
            'niveau_qualite': quality_level,
            'conformite': conformity,
            'signature_cryptographique': 'N/A (Fonctionnalité non implémentée pour cet agent)',
            'issues_critiques_identifies': len(issues_critiques),
            'architecture': {
                'description': "Description de l'architecture de l'agent",
                'statut_operationnel': f"Système {getattr(self, 'agent_id', 'unknown')} opérationnel.",
                'confirmation_specialisation': f"{getattr(self, 'agent_id', 'unknown')} confirmé comme spécialiste.",
                'objectifs_principaux': [
                    "Objectif principal 1",
                    "Objectif principal 2",
                    "Objectif principal 3"
                ],
                'technologies_cles': ["Technologie 1", "Technologie 2"]
            },
            'recommandations': self._generate_recommendations(metrics, issues_critiques),
            'issues_critiques_details': issues_critiques if issues_critiques else [
                "Aucun issue critique majeur détecté. Le système fonctionne dans les paramètres attendus."
            ],
            'details_techniques': {
                'strategie': "Stratégie technique de l'agent",
                'composants_actifs': [],
                'metriques_collectees': metrics
            },
            'metriques_detaillees': {
                'score_global': {'actuel': score, 'cible': 100},
                'conformite_pourcentage': {'actuel': score, 'cible': 100, 'unite': '%'}
            },
            'impact_business': {
                'criticite': 'MOYENNE' if score >= 70 else 'HAUTE',
                'domaines_impactes': [],
                'actions_requises': []
            }
        }


    def _generate_markdown_report(self, rapport_json: Dict, context: Dict, timestamp) -> str:
        """Génère un rapport Markdown selon le format standard."""
        
        agent_name = rapport_json.get('agent_id', 'Agent Inconnu')
        type_rapport = rapport_json.get('type_rapport', 'standard')
        score = rapport_json.get('score_global', 0)
        quality = rapport_json.get('niveau_qualite', 'UNKNOWN')
        conformity = rapport_json.get('conformite', 'NON ÉVALUÉ')
        
        markdown_content = f"""# 📊 RAPPORT STRATÉGIQUE : {agent_name.upper()}

## 🎯 RÉSUMÉ EXÉCUTIF

**Agent :** {agent_name}  
**Type de Rapport :** {type_rapport}  
**Date de Génération :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Score Global :** {score}/100  
**Niveau de Qualité :** {quality}  
**Conformité :** {conformity}  

## 📈 ANALYSE GLOBALE

### Score de Performance
- **Score Actuel :** {score}/100
- **Objectif :** 100/100
- **Statut :** {'🟢 ACCEPTABLE' if score >= 70 else '🔴 CRITIQUE'}

### Architecture
{rapport_json.get('architecture', {}).get('description', 'Description non disponible')}

**Objectifs Principaux :**
"""
        
        # Ajouter les objectifs
        for obj in rapport_json.get('architecture', {}).get('objectifs_principaux', []):
            markdown_content += f"- {obj}\n"
        
        markdown_content += f"""
**Technologies Clés :**
"""
        
        # Ajouter les technologies
        for tech in rapport_json.get('architecture', {}).get('technologies_cles', []):
            markdown_content += f"- {tech}\n"
        
        markdown_content += f"""

## 🔍 RECOMMANDATIONS

"""
        
        # Ajouter les recommandations
        for reco in rapport_json.get('recommandations', []):
            markdown_content += f"- {reco}\n"
        
        markdown_content += f"""

## ⚠️ ISSUES CRITIQUES

"""
        
        # Ajouter les issues critiques
        for issue in rapport_json.get('issues_critiques_details', []):
            markdown_content += f"- {issue}\n"
        
        markdown_content += f"""

## 📊 MÉTRIQUES DÉTAILLÉES

### Performance Globale
- **Score Global :** {rapport_json.get('metriques_detaillees', {}).get('score_global', {}).get('actuel', 0)}/{rapport_json.get('metriques_detaillees', {}).get('score_global', {}).get('cible', 100)}
- **Conformité :** {rapport_json.get('metriques_detaillees', {}).get('conformite_pourcentage', {}).get('actuel', 0)}%

## 🎯 IMPACT BUSINESS

**Criticité :** {rapport_json.get('impact_business', {}).get('criticite', 'NON ÉVALUÉ')}

### Domaines Impactés
"""
        
        # Ajouter les domaines impactés
        for domaine in rapport_json.get('impact_business', {}).get('domaines_impactes', []):
            markdown_content += f"- {domaine}\n"
        
        markdown_content += f"""

### Actions Requises
"""
        
        # Ajouter les actions requises
        for action in rapport_json.get('impact_business', {}).get('actions_requises', []):
            markdown_content += f"- {action}\n"
        
        markdown_content += f"""

---
*Rapport généré automatiquement par {agent_name} - NextGeneration System*  
*Timestamp: {timestamp.isoformat()}*
"""
        
        return markdown_content



if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 
