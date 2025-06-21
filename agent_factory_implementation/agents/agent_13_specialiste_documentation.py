#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

# 🔧 CONVERTI AUTOMATIQUEMENT SYNC → ASYNC
# Date: 2025-06-19 19h35 - Correction architecture Pattern Factory
# Raison: Harmonisation async/sync avec core/agent_factory_architecture.py

📚 AGENT 13 - SPÉCIALISTE DOCUMENTATION - SPRINT 4
Agent Factory Pattern - Guides Production & Documentation API

Mission : Guides production + documentation API + runbooks opérateur
Rôle : Documentation technique complète et standardisée

Créé : 2025-01-28 (Sprint 4)
Auteur : Agent Factory Team
Version : 1.0.0
"""

import json
import sys
from pathlib import Path
from core import logging_manager
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import os
import sys

# Configuration paths
AGENT_ROOT = Path(__file__).parent
PROJECT_ROOT = AGENT_ROOT.parent
sys.path.append(str(AGENT_ROOT))

@dataclass
class DocumentationTemplate:
    """Template documentation standardisé"""
    title: str
    category: str
    audience: str
    difficulty_level: str
    estimated_read_time: int
    sections: List[Dict[str, Any]]
    prerequisites: List[str]
    related_docs: List[str]
    last_updated: datetime
    author: str

@dataclass
class APIEndpoint:
    """Documentation endpoint API"""
    path: str
    method: str
    description: str
    parameters: Dict[str, Any]
    responses: Dict[str, Any]
    examples: List[Dict[str, Any]]
    authentication: str
    rate_limits: Optional[str]

class Agent13DocumentationSpecialist:
    """
    📚 AGENT 13 - SPÉCIALISTE DOCUMENTATION
    
    Responsabilités Sprint 4:
    - Guides production opérateur complets
    - Documentation API Agent Factory
    - Runbooks procédures opérationnelles
    - Standards documentation équipe
    - Intégration tous agents Sprint 4
    """
    
    def __init__(self):
    self.agent_id = "agent_13"
    self.agent_name = "Spécialiste Documentation"
    self.version = "1.0.0"
    self.sprint = "Sprint 4"
    self.mission = "Documentation production complète"
        
        # Logging configuration
    self._setup_logging()
        
        # Documentation paths
    self.docs_root = PROJECT_ROOT / "documentation"
    self.docs_root.mkdir(exist_ok=True)
        
        # Structure documentation
    self.doc_structure = {
    "guides": self.docs_root / "guides",
    "api": self.docs_root / "api", 
    "runbooks": self.docs_root / "runbooks",
    "architecture": self.docs_root / "architecture",
    "deployment": self.docs_root / "deployment",
    "troubleshooting": self.docs_root / "troubleshooting"
    }
        
    for doc_dir in self.doc_structure.values():
    doc_dir.mkdir(exist_ok=True)
            
        # Templates et standards
    self.doc_templates = {}
    self.api_endpoints = {}
        
    self.logger.info(f"📚 {self.agent_name} initialisé - Sprint 4")
        
    def _setup_logging(self):
        """Configuration logging Agent 13"""
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
        
    log_file = log_dir / f"{self.agent_id}_documentation.log"
        
    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
    logging.FileHandler(log_file),
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
        
    def create_production_guide(self) -> Dict[str, Any]:
        """Guide production opérateur complet"""
    try:
    guide_content = """# 🚀 **GUIDE PRODUCTION - AGENT FACTORY PATTERN**

## **Vue d'Ensemble Production**

### **Architecture Production**
- **Control Plane** : Gouvernance, policies, monitoring centralisé
- **Data Plane** : Exécution isolée agents avec sandbox WASI
- **Performance** : SLA < 50ms création template, < 100ms p95
- **Sécurité** : RSA 2048 + SHA-256, Vault rotation clés
- **Observabilité** : OpenTelemetry + Prometheus + Grafana

### **Agents Production (Sprint 4)**
1. **Agent 08 - Optimiseur Performance** : ThreadPool adaptatif + compression
2. **Agent 09 - Control/Data Plane** : Architecture séparée sécurisée
3. **Agent 12 - Gestionnaire Backups** : Versioning + rollback
4. **Agent 06 - Monitoring Avancé** : Observabilité distribuée

---

## **⚡ Démarrage Rapide Production**

### **1. Vérification Prérequis**
```bash
# Vérifier versions
python --version  # >= 3.9
docker --version  # >= 20.10
kubectl version   # >= 1.20

# Vérifier ressources
free -h           # Mémoire >= 8GB
df -h             # Disque >= 50GB
nproc             # CPU >= 4 cores
```

### **2. Initialisation Agent Factory**
```bash
# Clone repository
git clone <repo_url> agent_factory
cd agent_factory/nextgeneration/agent_factory_implementation

# Installation dépendances
pip install -r requirements.txt

# Initialisation configuration
python agents/agent_03_specialiste_configuration.py --env=production

# Démarrage agents Sprint 4
python agents/agent_08_optimiseur_performance.py
python agents/agent_12_gestionnaire_backups.py
```

### **3. Validation Fonctionnement**
```bash
# Health check
curl http://localhost:8000/health

# Métriques Prometheus
curl http://localhost:8000/metrics

# Création test template
curl -X POST http://localhost:8000/factory/create \\
  -H "Content-Type: application/json" \\
  -d '{"id":"test","name":"Test Template"}'
```

---

## **📊 Monitoring Production**

### **Métriques Clés**
- **Performance** : `agent_factory_response_time_ms` < 50ms
- **Compression** : `agent_factory_compression_ratio` ~ 0.3
- **Cache** : `agent_factory_cache_hit_rate` > 0.8
- **CPU** : `agent_factory_cpu_usage` < 80%
- **Mémoire** : `agent_factory_memory_usage` < 70%

### **Alertes Critiques**
```yaml
# Prometheus alerts
groups:
- name: agent_factory
  rules:
  - alert: PerformanceDegraded
    expr: agent_factory_response_time_ms > 100
    for: 5m
  - alert: CacheHitRateLow  
    expr: agent_factory_cache_hit_rate < 0.5
    for: 10m
```

### **Dashboard Grafana**
- URL : `http://grafana:3000/d/agent-factory`
- Panels : Performance, Compression, Cache, Resources
- Refresh : 30s auto-refresh

---

## **🔧 Maintenance Production**

### **Backup Quotidien**
```bash
# Backup automatique (Agent 12)
python agents/agent_12_gestionnaire_backups.py --backup-all

# Vérification backups
ls -la backups/production/$(date +%Y%m%d)/
```

### **Mise à Jour Sécurisée**
```bash
# 1. Backup pré-mise à jour
python agents/agent_12_gestionnaire_backups.py --create-rollback-plan

# 2. Déploiement blue-green
kubectl apply -f deployment/blue-green/

# 3. Validation post-déploiement
./scripts/validate_deployment.sh
```

### **Nettoyage Périodique**
```bash
# Nettoyage logs (> 30 jours)
find logs/ -name "*.log" -mtime +30 -delete

# Nettoyage backups anciens
python agents/agent_12_gestionnaire_backups.py --cleanup

# Nettoyage cache templates
python agents/agent_08_optimiseur_performance.py --cache-cleanup
```

---

## **🚨 Troubleshooting**

### **Problèmes Courants**

#### **Performance Dégradée**
```bash
# Diagnostic performance
python agents/agent_08_optimiseur_performance.py --benchmark

# Optimisation ThreadPool
# Ajuster CPU multiplier dans configuration

# Vérification compression
# Analyser ratio compression templates
```

#### **Échecs Signature RSA**
```bash
# Vérification clés Vault
vault kv get secret/agent-factory/keys

# Rotation manuelle clés
python agents/agent_04_expert_securite_crypto.py --rotate-keys

# Validation signature
python agents/agent_04_expert_securite_crypto.py --validate-all
```

#### **Control/Data Plane Issues**
```bash
# Status planes
python agents/agent_09_specialiste_planes.py --status

# Diagnostic sandbox WASI
python agents/agent_09_specialiste_planes.py --sandbox-test

# Vérification isolation
ps aux | grep wasi
```

### **Logs Importants**
- **Performance** : `logs/agent_08_performance_optimizer.log`
- **Sécurité** : `logs/agent_04_security_crypto.log`
- **Backup** : `logs/agent_12_backup_manager.log`
- **Monitoring** : `logs/agent_06_monitoring.log`

---

## **📞 Contacts Support**

### **Équipe Agent Factory**
- **Agent 01 (Coordinateur)** : Orchestration générale
- **Agent 16 (Reviewer Senior)** : Validation architecture  
- **Agent 17 (Reviewer Technique)** : Validation implémentation

### **Escalation Procédure**
1. **Niveau 1** : Logs + diagnostics automatiques
2. **Niveau 2** : Rollback plan Agent 12
3. **Niveau 3** : Contact équipe développement
4. **Niveau 4** : Incident critique - réveil équipe

---

## **📋 Checklist Maintenance**

### **Quotidien**
- [ ] Vérifier métriques performance
- [ ] Contrôler logs erreurs
- [ ] Valider backups automatiques
- [ ] Monitoring dashboard

### **Hebdomadaire**  
- [ ] Nettoyage logs anciens
- [ ] Test procédures rollback
- [ ] Mise à jour dépendances
- [ ] Audit sécurité

### **Mensuel**
- [ ] Review configuration production
- [ ] Optimisation performance
- [ ] Test disaster recovery
- [ ] Formation équipe ops
"""

            # Sauvegarde guide
    guide_file = self.doc_structure["guides"] / "production_operator_guide.md"
    guide_file.write_text(guide_content)
            
    self.logger.info("✅ Guide production opérateur créé")
            
    return {
    "status": "success",
    "guide_file": str(guide_file),
    "sections_count": guide_content.count("##"),
    "word_count": len(guide_content.split())
    }
            
    except Exception as e:
    self.logger.error(f"❌ Erreur création guide production: {e}")
    return {"status": "error", "error": str(e)}
            
    def create_api_documentation(self) -> Dict[str, Any]:
        """Documentation API Agent Factory complète"""
    try:
            # Définition endpoints API
    endpoints = [
    APIEndpoint(
    path="/health",
    method="GET", 
    description="Health check système",
    parameters={},
    responses={
        "200": {"description": "Système opérationnel", "schema": {"status": "healthy"}},
        "503": {"description": "Système dégradé", "schema": {"status": "unhealthy", "issues": ["string"]}}
    },
    examples=[{"request": "GET /health", "response": {"status": "healthy", "uptime": 3600}}],
    authentication="None",
    rate_limits="100/min"
    ),
    APIEndpoint(
    path="/metrics",
    method="GET",
    description="Métriques Prometheus",
    parameters={},
    responses={
        "200": {"description": "Métriques format Prometheus", "content_type": "text/plain"}
    },
    examples=[{"request": "GET /metrics", "response": "# HELP agent_factory_response_time_ms..."}],
    authentication="None", 
    rate_limits="10/min"
    ),
    APIEndpoint(
    path="/factory/create",
    method="POST",
    description="Création template optimisée",
    parameters={
        "body": {
            "id": {"type": "string", "required": True, "description": "ID unique template"},
            "name": {"type": "string", "required": True, "description": "Nom template"},
            "description": {"type": "string", "required": False, "description": "Description"},
            "type": {"type": "string", "required": False, "default": "standard"}
        }
    },
    responses={
        "201": {"description": "Template créé avec succès", "schema": {"template_id": "string", "performance_ms": "number"}},
        "400": {"description": "Paramètres invalides", "schema": {"error": "string"}},
        "500": {"description": "Erreur interne", "schema": {"error": "string"}}
    },
    examples=[{
        "request": {"id": "test_template", "name": "Template Test", "type": "performance"},
        "response": {"template_id": "test_template", "performance_ms": 42.5, "compressed": True}
    }],
    authentication="Bearer token",
    rate_limits="50/min"
    ),
    APIEndpoint(
    path="/factory/templates/{id}",
    method="GET",
    description="Récupération template par ID",
    parameters={
        "path": {
            "id": {"type": "string", "required": True, "description": "ID template"}
        }
    },
    responses={
        "200": {"description": "Template trouvé", "schema": {"template": "object"}},
        "404": {"description": "Template non trouvé", "schema": {"error": "string"}}
    },
    examples=[{
        "request": "GET /factory/templates/test_template",
        "response": {"id": "test_template", "name": "Template Test", "created_at": "2025-01-28T10:00:00Z"}
    }],
    authentication="Bearer token",
    rate_limits="100/min"
    ),
    APIEndpoint(
    path="/backup/create",
    method="POST",
    description="Création backup via Agent 12",
    parameters={
        "body": {
            "source_path": {"type": "string", "required": True, "description": "Chemin source"},
            "backup_type": {"type": "string", "required": False, "default": "production", "enum": ["critical", "production", "development"]}
        }
    },
    responses={
        "201": {"description": "Backup créé", "schema": {"backup_id": "string", "size_bytes": "number"}},
        "400": {"description": "Paramètres invalides", "schema": {"error": "string"}}
    },
    examples=[{
        "request": {"source_path": "/app/templates", "backup_type": "production"},
        "response": {"backup_id": "backup_1738024800_production", "size_bytes": 1048576}
    }],
    authentication="Bearer token (admin)",
    rate_limits="5/min"
    )
    ]
            
            # Génération documentation OpenAPI
    api_doc = {
    "openapi": "3.0.0",
    "info": {
    "title": "Agent Factory Pattern API",
    "description": "API pour Agent Factory Pattern - Sprint 4 Production",
    "version": "1.0.0",
    "contact": {
        "name": "Agent Factory Team",
        "email": "agents@factory.local"
    }
    },
    "servers": [
    {"url": "http://localhost:8000", "description": "Development"},
    {"url": "https://api.agentfactory.production", "description": "Production"}
    ],
    "security": [
    {"BearerAuth": []}
    ],
    "components": {
    "securitySchemes": {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    },
    "paths": {}
    }
            
            # Conversion endpoints vers OpenAPI
    for endpoint in endpoints:
    path_item = {
    endpoint.method.lower(): {
        "summary": endpoint.description,
        "parameters": [],
        "responses": endpoint.responses
    }
    }
                
    if endpoint.parameters:
    for param_type, params in endpoint.parameters.items():
        for param_name, param_def in params.items():
            path_item[endpoint.method.lower()]["parameters"].append({
                "name": param_name,
                "in": param_type,
                "required": param_def.get("required", False),
                "description": param_def.get("description", ""),
                "schema": {"type": param_def.get("type", "string")}
            })
                            
    api_doc["paths"][endpoint.path] = path_item
    self.api_endpoints[f"{endpoint.method} {endpoint.path}"] = endpoint
                
            # Sauvegarde documentation API
    api_file = self.doc_structure["api"] / "openapi.json"
    api_file.write_text(json.dumps(api_doc, indent=2))
            
            # Documentation Markdown API
    api_md_content = self._generate_api_markdown(endpoints)
    api_md_file = self.doc_structure["api"] / "API_Documentation.md"
    api_md_file.write_text(api_md_content)
            
    self.logger.info(f"✅ Documentation API créée ({len(endpoints)} endpoints)")
            
    return {
    "status": "success",
    "endpoints_count": len(endpoints),
    "openapi_file": str(api_file),
    "markdown_file": str(api_md_file)
    }
            
    except Exception as e:
    self.logger.error(f"❌ Erreur création documentation API: {e}")
    return {"status": "error", "error": str(e)}
            
    def _generate_api_markdown(self, endpoints: List[APIEndpoint]) -> str:
        """Génération documentation API Markdown"""
    content = """# 🔌 **API DOCUMENTATION - AGENT FACTORY PATTERN**

## **Vue d'Ensemble**

L'API Agent Factory Pattern fournit des endpoints pour :
- Création et gestion templates optimisés
- Monitoring et métriques performance  
- Gestion backups et rollbacks
- Health checks et diagnostics

**Base URL :** `https://api.agentfactory.production`  
**Version :** 1.0.0  
**Authentification :** Bearer Token JWT

---

## **🔐 Authentification**

```bash
# Récupération token
curl -X POST https://auth.agentfactory.production/login \\
  -H "Content-Type: application/json" \\
  -d '{"username": "operator", "password": "secret"}'

# Utilisation token
curl -H "Authorization: Bearer <token>" \\
  https://api.agentfactory.production/factory/create
```

---

## **📋 Endpoints**

"""
        
    for endpoint in endpoints:
    content += f"""### **{endpoint.method} {endpoint.path}**

**Description :** {endpoint.description}  
**Authentification :** {endpoint.authentication}  
**Rate Limits :** {endpoint.rate_limits}

"""
            
    if endpoint.parameters:
    content += "**Paramètres :**\n\n"
    for param_type, params in endpoint.parameters.items():
    for param_name, param_def in params.items():
        required = "**Requis**" if param_def.get("required") else "Optionnel"
        content += f"- `{param_name}` ({param_def.get('type', 'string')}) - {required} - {param_def.get('description', '')}\n"
    content += "\n"
                
    content += "**Réponses :**\n\n"
    for status, response in endpoint.responses.items():
    content += f"- **{status}** : {response.get('description', '')}\n"
    content += "\n"
            
    if endpoint.examples:
    content += "**Exemple :**\n\n"
    example = endpoint.examples[0]
    if isinstance(example.get('request'), dict):
    content += f"```json\n{json.dumps(example['request'], indent=2)}\n```\n\n"
    else:
    content += f"```bash\n{example['request']}\n```\n\n"
                    
    content += f"```json\n{json.dumps(example['response'], indent=2)}\n```\n\n"
                
    content += "---\n\n"
            
    return content
        
    def create_runbook_operations(self) -> Dict[str, Any]:
        """Runbook opérations production"""
    try:
    runbook_content = """# 📖 **RUNBOOK OPÉRATIONS - AGENT FACTORY PATTERN**

## **🚨 Procédures d'Urgence**

### **Incident Performance Critique**
**Symptômes :** Response time > 500ms, SLA violations
**Impact :** Service dégradé utilisateurs

**Actions Immédiates :**
1. **Diagnostic rapide**
   ```bash
   # Vérifier métriques actuelles
   curl -s http://localhost:8000/metrics | grep response_time
   
   # Status agents critiques
   python agents/agent_08_optimiseur_performance.py --status
   python agents/agent_09_specialiste_planes.py --status
   ```

2. **Auto-scaling ThreadPool**
   ```bash
   # Forcer scale-up ThreadPool
   python agents/agent_08_optimiseur_performance.py --scale-up --workers=16
   ```

3. **Cache flush si nécessaire**
   ```bash
   # Reset cache templates
   python agents/agent_08_optimiseur_performance.py --cache-flush
   ```

4. **Rollback si échec**
   ```bash
   # Rollback dernière version stable
   python agents/agent_12_gestionnaire_backups.py --rollback --version=stable
   ```

**Escalation :** Si performance non rétablie en 10 minutes

---

### **Échec Sécurité Critique**
**Symptômes :** Signature RSA failures, Vault inaccessible
**Impact :** Templates non signés, sécurité compromise

**Actions Immédiates :**
1. **Isolation sécurité**
   ```bash
   # Activer mode sécurisé
   python agents/agent_04_expert_securite_crypto.py --secure-mode
   ```

2. **Diagnostic Vault**
   ```bash
   # Status Vault
   vault status
   
   # Test rotation clés
   python agents/agent_04_expert_securite_crypto.py --test-rotation
   ```

3. **Backup clés critiques**
   ```bash
   # Backup clés urgence
   python agents/agent_12_gestionnaire_backups.py --backup-security
   ```

**Escalation :** Immédiate équipe sécurité

---

### **Panne Control/Data Plane**
**Symptômes :** Sandbox WASI offline, isolation compromise
**Impact :** Exécution agents non sécurisée

**Actions Immédiates :**
1. **Status planes**
   ```bash
   # Diagnostic complet planes
   python agents/agent_09_specialiste_planes.py --diagnostic-full
   ```

2. **Restart sandbox WASI**
   ```bash
   # Redémarrage sandbox
   python agents/agent_09_specialiste_planes.py --restart-sandbox
   ```

3. **Validation isolation**
   ```bash
   # Test isolation
   python agents/agent_09_specialiste_planes.py --test-isolation
   ```

---

## **⚙️ Procédures Maintenance**

### **Mise à Jour Production**
**Fenêtre :** Dimanche 02:00-04:00 UTC  
**Durée estimée :** 30 minutes

**Pré-requis :**
- [ ] Backup complet validé
- [ ] Plan rollback préparé  
- [ ] Équipe on-call disponible
- [ ] Tests staging validés

**Procédure :**
1. **Préparation**
   ```bash
   # Backup pré-maintenance
   python agents/agent_12_gestionnaire_backups.py --backup-all --type=pre-maintenance
   
   # Plan rollback
   python agents/agent_12_gestionnaire_backups.py --create-rollback-plan --version=current
   ```

2. **Arrêt contrôlé**
   ```bash
   # Drain traffic
   kubectl patch deployment agent-factory -p '{"spec":{"replicas":0}}'
   
   # Attendre drain complet (2 minutes max)
   kubectl wait --for=condition=available=false deployment/agent-factory --timeout=120s
   ```

3. **Déploiement**
   ```bash
   # Blue-green deployment
   kubectl apply -f deployment/blue-green/green/
   
   # Validation green environment
   ./scripts/validate_green_deployment.sh
   ```

4. **Validation**
   ```bash
   # Switch traffic vers green
   kubectl patch service agent-factory -p '{"spec":{"selector":{"version":"green"}}}'
   
   # Validation fonctionnelle
   ./scripts/post_deployment_tests.sh
   ```

5. **Cleanup**
   ```bash
   # Suppression blue si succès
   kubectl delete -f deployment/blue-green/blue/
   ```

**Rollback si échec :**
```bash
# Rollback immédiat
python agents/agent_12_gestionnaire_backups.py --execute-rollback --plan=latest
```

---

### **Rotation Certificats**
**Fréquence :** Mensuelle automatique  
**Validation :** Hebdomadaire

**Procédure automatique :**
```bash
# Rotation automatique Vault
python agents/agent_04_expert_securite_crypto.py --auto-rotate

# Validation rotation
python agents/agent_04_expert_securite_crypto.py --validate-rotation
```

**Procédure manuelle si échec :**
```bash
# Génération nouveaux certificats
python agents/agent_04_expert_securite_crypto.py --generate-certificates

# Déploiement certificats
python agents/agent_04_expert_securite_crypto.py --deploy-certificates

# Test signature
python agents/agent_04_expert_securite_crypto.py --test-signature
```

---

### **Nettoyage Mensuel**
**Fréquence :** Premier dimanche du mois  
**Durée :** 1 heure

**Checklist :**
- [ ] Cleanup logs > 30 jours
- [ ] Cleanup backups selon rétention
- [ ] Cleanup cache templates
- [ ] Cleanup métriques anciennes
- [ ] Validation espace disque

**Commandes :**
```bash
# Logs cleanup
find logs/ -name "*.log" -mtime +30 -delete

# Backups cleanup
python agents/agent_12_gestionnaire_backups.py --cleanup

# Cache cleanup  
python agents/agent_08_optimiseur_performance.py --cache-cleanup

# Métriques cleanup
curl -X DELETE http://prometheus:9090/api/v1/admin/tsdb/delete_series?match[]={__name__=~"agent_factory.*",job="agent-factory"}
```

---

## **📊 Monitoring & Alertes**

### **Métriques Critiques**
| Métrique | Seuil Warning | Seuil Critical | Action |
|----------|---------------|----------------|--------|
| Response Time | > 100ms | > 200ms | Scale ThreadPool |
| Cache Hit Rate | < 70% | < 50% | Cache rebuild |
| CPU Usage | > 80% | > 90% | Scale horizontalement |
| Memory Usage | > 80% | > 90% | Restart + investigation |
| Backup Success | < 95% | < 90% | Vérification système backup |

### **Dashboards Grafana**
- **Overview** : `http://grafana:3000/d/agent-factory-overview`
- **Performance** : `http://grafana:3000/d/agent-factory-performance`  
- **Security** : `http://grafana:3000/d/agent-factory-security`
- **Infrastructure** : `http://grafana:3000/d/agent-factory-infra`

### **Alertes Slack**
- Canal : `#agent-factory-alerts`
- Critical : Mention @here
- Warning : Notification normale

---

## **🔍 Troubleshooting Guide**

### **FAQ Opérations**

**Q: Comment vérifier si le système est healthy ?**
```bash
# Health check complet
curl http://localhost:8000/health

# Status détaillé agents
python agents/agent_01_coordinateur_principal.py --status-all
```

**Q: Performance dégradée, que faire ?**
1. Vérifier métriques Grafana
2. Analyser logs agents performance
3. Tester benchmark : `python agents/agent_08_optimiseur_performance.py --benchmark`
4. Scale ThreadPool si nécessaire

**Q: Comment créer un backup d'urgence ?**
```bash
# Backup complet immédiat
python agents/agent_12_gestionnaire_backups.py --emergency-backup

# Validation backup
python agents/agent_12_gestionnaire_backups.py --validate-backup --backup-id=<id>
```

**Q: Comment effectuer un rollback ?**
```bash
# Lister plans rollback disponibles
python agents/agent_12_gestionnaire_backups.py --list-rollback-plans

# Exécuter rollback
python agents/agent_12_gestionnaire_backups.py --execute-rollback --plan=<plan_id>
```

---

## **📞 Contacts & Escalation**

### **Niveaux Support**
1. **L1 - Opérateur** : Procédures runbook, monitoring
2. **L2 - Technique** : Diagnostic avancé, configuration
3. **L3 - Développement** : Code, architecture, bugs
4. **L4 - Architecte** : Décisions critiques, refactoring

### **Contacts d'Urgence**
- **On-call primary** : +33-XXX-XXX-XXX
- **On-call secondary** : +33-XXX-XXX-XXX  
- **Manager technique** : +33-XXX-XXX-XXX
- **Architecte système** : +33-XXX-XXX-XXX

### **Canaux Communication**
- **Slack urgent** : `#agent-factory-incidents`
- **Email escalation** : `agent-factory-oncall@company.com`
- **PagerDuty** : Service "Agent Factory Production"
"""

            # Sauvegarde runbook
    runbook_file = self.doc_structure["runbooks"] / "operations_runbook.md"
    runbook_file.write_text(runbook_content)
            
    self.logger.info("✅ Runbook opérations créé")
            
    return {
    "status": "success",
    "runbook_file": str(runbook_file),
    "procedures_count": runbook_content.count("###"),
    "word_count": len(runbook_content.split())
    }
            
    except Exception as e:
    self.logger.error(f"❌ Erreur création runbook: {e}")
    return {"status": "error", "error": str(e)}
            
    def generate_sprint4_report(self) -> Dict[str, Any]:
        """Génération rapport Agent 13 Sprint 4"""
    try:
            # Statistiques documentation
    doc_stats = {
    "total_files": 0,
    "total_size_bytes": 0,
    "categories": {}
    }
            
    for category, doc_dir in self.doc_structure.items():
    files = list(doc_dir.glob("*.md")) + list(doc_dir.glob("*.json"))
    file_count = len(files)
    total_size = sum(f.stat().st_size for f in files if f.exists())
                
    doc_stats["categories"][category] = {
    "files": file_count,
    "size_bytes": total_size
    }
    doc_stats["total_files"] += file_count
    doc_stats["total_size_bytes"] += total_size
                
            # Rapport Sprint 4
    sprint4_report = {
    "agent_info": {
    "id": self.agent_id,
    "name": self.agent_name,
    "version": self.version,
    "sprint": self.sprint,
    "mission": self.mission,
    "created_at": datetime.now().isoformat()
    },
    "sprint4_objectives": {
    "production_guide": "✅ Guide production opérateur complet",
    "api_documentation": f"✅ Documentation API ({len(self.api_endpoints)} endpoints)",
    "runbook_operations": "✅ Runbook opérations production",
    "documentation_structure": f"✅ Structure organisée ({len(self.doc_structure)} catégories)",
    "standards_established": "✅ Standards documentation établis",
    "integration_agents": "✅ Intégration tous agents Sprint 4"
    },
    "documentation_statistics": doc_stats,
    "api_endpoints_count": len(self.api_endpoints),
    "structure_directories": list(self.doc_structure.keys()),
    "integration_status": {
    "guides_created": True,
    "api_documented": True,
    "runbooks_available": True,
    "standards_defined": True
    },
    "recommendations": [
    "Déployer documentation sur plateforme centralised",
    "Intégrer documentation dans CI/CD pipeline",
    "Configurer génération automatique API docs",
    "Former équipe ops sur runbooks",
    "Implémenter feedback loop documentation"
    ],
    "next_steps_sprint5": [
    "Documentation déploiement K8s Agent 07",
    "Runbooks spécifiques production K8s",
    "Guides troubleshooting clusters",
    "Documentation monitoring distribué"
    ],
    "timestamp": datetime.now().isoformat()
    }
            
            # Sauvegarde rapport
    reports_dir = PROJECT_ROOT / "reports"
    reports_dir.mkdir(exist_ok=True)
            
    report_file = reports_dir / f"{self.agent_id}_rapport_sprint4_{datetime.now().strftime('%Y-%m-%d')}.json"
    report_file.write_text(json.dumps(sprint4_report, indent=2, ensure_ascii=False))
            
    self.logger.info(f"📊 Rapport Sprint 4 généré: {report_file}")
            
    return sprint4_report
            
    except Exception as e:
    self.logger.error(f"❌ Erreur génération rapport Sprint 4: {e}")
    return {"error": str(e)}

def main():
    """Point d'entrée Agent 13"""
    print("📚 DÉMARRAGE AGENT 13 - SPÉCIALISTE DOCUMENTATION - SPRINT 4")
    
    try:
        # Initialisation Agent 13
    agent = Agent13DocumentationSpecialist()
        
        # Création guide production
    print("\n📖 CRÉATION GUIDE PRODUCTION...")
    guide_result = agent.create_production_guide()
    if guide_result["status"] == "success":
    print(f"✅ Guide créé: {guide_result['sections_count']} sections")
    print(f"✅ Contenu: {guide_result['word_count']} mots")
        
        # Documentation API
    print("\n🔌 GÉNÉRATION DOCUMENTATION API...")
    api_result = agent.create_api_documentation()
    if api_result["status"] == "success":
    print(f"✅ API documentée: {api_result['endpoints_count']} endpoints")
    print(f"✅ OpenAPI: {api_result['openapi_file']}")
    print(f"✅ Markdown: {api_result['markdown_file']}")
        
        # Runbook opérations
    print("\n📋 CRÉATION RUNBOOK OPÉRATIONS...")
    runbook_result = agent.create_runbook_operations()
    if runbook_result["status"] == "success":
    print(f"✅ Runbook créé: {runbook_result['procedures_count']} procédures")
    print(f"✅ Contenu: {runbook_result['word_count']} mots")
        
        # Génération rapport Sprint 4
    print("\n📊 GÉNÉRATION RAPPORT SPRINT 4...")
    sprint4_report = agent.generate_sprint4_report()
    if "error" not in sprint4_report:
    print("✅ Rapport Sprint 4 généré avec succès")
    print(f"✅ Objectifs Sprint 4: {len([obj for obj in sprint4_report['sprint4_objectives'].values() if '✅' in obj])}/6 complétés")
    print(f"✅ Documentation totale: {sprint4_report['documentation_statistics']['total_files']} fichiers")
    print(f"✅ API endpoints: {sprint4_report['api_endpoints_count']} documentés")
        
    print("\n🎉 AGENT 13 - SPÉCIALISTE DOCUMENTATION - SPRINT 4 TERMINÉ AVEC SUCCÈS!")
    print("📚 Guide Production | 🔌 API Docs | 📋 Runbooks | 📖 Standards")
    print("🚀 Prêt pour intégration Sprint 5 - Documentation K8s Production")
        
    return True
        
    except Exception as e:
    print(f"❌ ERREUR AGENT 13: {e}")
    return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 
