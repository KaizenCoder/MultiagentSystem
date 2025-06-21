# 📚 **DOCUMENTATION INTÉGRATION LOGGING AGENTS**

## 🎯 **Objectif**
Documentation pour intégrer le système de logging NextGeneration dans chaque agent spécialisé.

## 🚀 **Agents Configurés**


### 🤖 **Agent 01 Coordinateur Principal**

**Configuration:**
- **Niveau de logging:** INFO
- **Format rapport:** coordination_rapport
- **Sécurité:** high
- **Handlers spécialisés:** coordination, team_management

**Intégration:**
```python
# Import
from agent_01_coordinateur_principal_logging_integration import integrate_logging

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
            self.logging_integration.log_error({"message": str(e), "context": mission_data})
            raise
```

**Répertoire des rapports:** `./reports_equipe_agents/agent_01_coordinateur_principal/`


### 🤖 **Agent 11 Auditeur Qualite**

**Configuration:**
- **Niveau de logging:** DEBUG
- **Format rapport:** audit_qualite_rapport
- **Sécurité:** high
- **Handlers spécialisés:** quality_audit, code_analysis

**Intégration:**
```python
# Import
from agent_11_auditeur_qualite_logging_integration import integrate_logging

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
            self.logging_integration.log_error({"message": str(e), "context": mission_data})
            raise
```

**Répertoire des rapports:** `./reports_equipe_agents/agent_11_auditeur_qualite/`


### 🤖 **Agent 15 Testeur Specialise**

**Configuration:**
- **Niveau de logging:** DEBUG
- **Format rapport:** tests_specialises_rapport
- **Sécurité:** medium
- **Handlers spécialisés:** testing, performance_testing

**Intégration:**
```python
# Import
from agent_15_testeur_specialise_logging_integration import integrate_logging

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
            self.logging_integration.log_error({"message": str(e), "context": mission_data})
            raise
```

**Répertoire des rapports:** `./reports_equipe_agents/agent_15_testeur_specialise/`


### 🤖 **Agent 16 Peer Reviewer Senior**

**Configuration:**
- **Niveau de logging:** INFO
- **Format rapport:** peer_review_senior_rapport
- **Sécurité:** high
- **Handlers spécialisés:** peer_review, senior_analysis

**Intégration:**
```python
# Import
from agent_16_peer_reviewer_senior_logging_integration import integrate_logging

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
            self.logging_integration.log_error({"message": str(e), "context": mission_data})
            raise
```

**Répertoire des rapports:** `./reports_equipe_agents/agent_16_peer_reviewer_senior/`


### 🤖 **Agent 17 Peer Reviewer Technique**

**Configuration:**
- **Niveau de logging:** DEBUG
- **Format rapport:** peer_review_technique_rapport
- **Sécurité:** high
- **Handlers spécialisés:** technical_review, code_analysis

**Intégration:**
```python
# Import
from agent_17_peer_reviewer_technique_logging_integration import integrate_logging

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
            self.logging_integration.log_error({"message": str(e), "context": mission_data})
            raise
```

**Répertoire des rapports:** `./reports_equipe_agents/agent_17_peer_reviewer_technique/`


### 🤖 **Agent 18 Auditeur Securite**

**Configuration:**
- **Niveau de logging:** INFO
- **Format rapport:** audit_securite_rapport
- **Sécurité:** critical
- **Handlers spécialisés:** security_audit, vulnerability_scan

**Intégration:**
```python
# Import
from agent_18_auditeur_securite_logging_integration import integrate_logging

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
            self.logging_integration.log_error({"message": str(e), "context": mission_data})
            raise
```

**Répertoire des rapports:** `./reports_equipe_agents/agent_18_auditeur_securite/`


### 🤖 **Agent 19 Auditeur Performance**

**Configuration:**
- **Niveau de logging:** DEBUG
- **Format rapport:** audit_performance_rapport
- **Sécurité:** medium
- **Handlers spécialisés:** performance_audit, profiling

**Intégration:**
```python
# Import
from agent_19_auditeur_performance_logging_integration import integrate_logging

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
            self.logging_integration.log_error({"message": str(e), "context": mission_data})
            raise
```

**Répertoire des rapports:** `./reports_equipe_agents/agent_19_auditeur_performance/`


### 🤖 **Agent 20 Auditeur Conformite**

**Configuration:**
- **Niveau de logging:** INFO
- **Format rapport:** audit_conformite_rapport
- **Sécurité:** high
- **Handlers spécialisés:** compliance_audit, standards_check

**Intégration:**
```python
# Import
from agent_20_auditeur_conformite_logging_integration import integrate_logging

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
            self.logging_integration.log_error({"message": str(e), "context": mission_data})
            raise
```

**Répertoire des rapports:** `./reports_equipe_agents/agent_20_auditeur_conformite/`



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
with open('config/agents_logging_config_20250621_021249.json') as f:
    config = json.load(f)
```

### 3. **Utilisation Standard**
```python
# Pour chaque agent
from logging_manager_optimized import LoggingManager

class MonAgent:
    def __init__(self):
        self.logger = LoggingManager().get_agent_logger('mon_agent_id')
    
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

*Documentation générée automatiquement le 2025-06-21 02:12:49*
