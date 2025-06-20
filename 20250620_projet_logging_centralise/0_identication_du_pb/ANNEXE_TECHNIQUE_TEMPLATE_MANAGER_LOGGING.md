# 📋 Annexe Technique : Code Complet - Centralisation Logging TemplateManager

## 🎯 **Contexte NextGeneration - Écosystème Outils**

### 🔧 **Intégration avec /tools/generate_pitch_document**

L'outil `generate_pitch_document` illustre l'architecture NextGeneration avec :

- **📁 Configuration modulaire** : `agent_factory_config.json` pour intégration avec Agent Factory
- **🔧 Logging intégré** : Système de logs NextGeneration compatible
- **⚙️ Monitoring natif** : Métriques et observabilité intégrées
- **🎯 Patterns standardisés** : Template de configuration réutilisable

```json
// Exemple de configuration standardisée d'outil NextGeneration
{
  "nextgeneration_integration": {
    "use_ng_logging": true,          // ← DOIT utiliser le logging centralisé
    "use_ng_monitoring": true        // ← Monitoring centralisé
  }
}
```

Cette intégration démontre la nécessité d'un système de logging centralisé pour tous les composants NextGeneration.

## 🎯 **Code TemplateManager AVANT Modification**

### 📄 **optimized_template_manager.py (ACTUEL)**

```python
"""
Code Expert NextGeneration - optimized_template_manager
Adapt depuis scripts experts Claude Phase 2 (Production-Ready)
"""

import asyncio
import json
import logging
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path
from threading import RLock
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import aiofiles
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .agent_templates import AgentTemplate, TemplateValidationError
from ..agents.base_agent import BaseAgent
from ..config.agent_config import AgentFactoryConfig

logger = logging.getLogger(__name__)

@dataclass
class TemplateMetrics:
    """Métriques de performance pour les templates."""
    loads_count: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    reload_count: int = 0
    creation_times: List[float] = field(default_factory=list)
    errors: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    last_accessed: Dict[str, datetime] = field(default_factory=dict)

class TemplateFileWatcher(FileSystemEventHandler):
    """Surveille les modifications des fichiers templates."""
    
    def __init__(self, manager: 'TemplateManager'):
        self.manager = manager
        
    def on_modified(self, event):
        """Callback lors de la modification d'un fichier."""
        if event.is_directory or not event.src_path.endswith('.json'):
            return
            
        template_name = Path(event.src_path).stem
        logger.info("Template modifié détecté : %s", template_name)
        
        # Invalider le cache pour ce template
        asyncio.create_task(self.manager.reload_template(template_name))

class TemplateManager:
    """Gestionnaire optimisé de templates avec cache intelligent et métriques."""
    
    def __init__(
        self,
        config: Optional[AgentFactoryConfig] = None,
        enable_hot_reload: bool = True,
        preload_templates: Optional[List[str]] = None
    ):
        self.config = config or AgentFactoryConfig()
        self._lock = RLock()
        self._cache: Dict[str, AgentTemplate] = {}
        self._timestamps: Dict[str, float] = {}
        self._class_cache: Dict[str, type[BaseAgent]] = {}
        self._metrics = TemplateMetrics()
        self._executor = ThreadPoolExecutor(max_workers=4)
        
        # Configuration du hot-reload
        self._observer: Optional[Observer] = None
        if enable_hot_reload:
            self._setup_file_watcher()
        
        # Préchargement des templates critiques
        if preload_templates:
            asyncio.create_task(self._preload_templates(preload_templates))

    def create_agent(
        self,
        template_name: str,
        *,
        suffix: str = "",
        config: Optional[Dict[str, Any]] = None
    ) -> BaseAgent:
        """Crée une instance d'agent à partir d'un template."""
        start_time = time.time()
        
        try:
            # Utiliser la classe en cache si disponible
            with self._lock:
                if template_name in self._class_cache:
                    agent_class = self._class_cache[template_name]
                else:
                    tmpl = self.get_template(template_name)
                    agent_class = tmpl.to_class()
                    self._class_cache[template_name] = agent_class
            
            # Créer l'instance (hors du lock)
            agent = agent_class.create(name_suffix=suffix, config=config)
            
            # Métriques
            creation_time = time.time() - start_time
            with self._lock:
                self._metrics.creation_times.append(creation_time)
            
            logger.debug(
                "Agent créé : %s (template=%s, temps=%.3fs)",
                agent.metadata.name,
                template_name,
                creation_time
            )
            
            return agent
            
        except Exception as e:
            self._metrics.errors[type(e).__name__] += 1
            logger.error("Erreur création agent '%s': %s", template_name, e)
            raise
```

---

## 🔧 **Code Agent AVANT Modification**

### 📄 **agent_0_chef_equipe_coordinateur.py (ACTUEL)**

```python
#!/usr/bin/env python3
"""
🎖️ Agent 0 - Chef d'Équipe Coordinateur
Modèle: Claude Sonnet 4 
Mission: Orchestration centrale de l'équipe de maintenance
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys

# Configuration des logs - PROBLÈME: Basique et non centralisé
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class Agent0ChefEquipeCoordinateur:
    """Agent 0 - Chef d'Équipe Coordinateur avec Claude Sonnet 4"""
    
    def __init__(self, agent_id: str = None, agent_type: str = "chef_equipe_coordinateur", 
                 target_path: str = None, workspace_path: str = None, **config):
        self.agent_id = agent_id or f"agent_0_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.agent_type = agent_type
        self.config = config
        
        # PROBLÈME: Logger non centralisé, nom hard-codé
        self.logger = logging.getLogger("Agent0ChefEquipe")
        
        # Configuration équipe
        self.target_path = Path(target_path) if target_path else Path("../agent_factory_implementation/agents")
        self.workspace_path = Path(workspace_path) if workspace_path else Path(".")
        self.equipe_agents = {}
        
        # PROBLÈME: Log dans répertoire non contrôlé
        self.logger.info(f"🎖️ Agent 0 Chef d'Équipe Coordinateur initialisé - ID: {self.agent_id}")
        
    async def _sauvegarder_rapport_final(self, workflow_result: Dict):
        """Sauvegarde du rapport final consolidé"""
        try:
            # PROBLÈME: Logs et rapports mélangés
            rapport_path = self.workspace_path / "reports" / f"chef_equipe_maintenance_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            rapport_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(rapport_path, 'w', encoding='utf-8') as f:
                json.dump(workflow_result, f, indent=2, ensure_ascii=False, default=str)
            
            # PROBLÈME: Log sans catégorisation ni contrôle destination
            self.logger.info(f"💾 Rapport final sauvegardé: {rapport_path}")
            
        except Exception as e:
            # PROBLÈME: Logs d'erreur non centralisés
            self.logger.error(f"❌ Erreur sauvegarde rapport final: {e}")
```

---

## 🎯 **SOLUTION PROPOSÉE : Code Complet**

### 📄 **1. LoggingManager Centralisé (NOUVEAU)**

```python
#!/usr/bin/env python3
"""
LoggingManager Centralisé NextGeneration
Gestion unifiée de tous les logs du système
"""

import json
import logging
import logging.handlers
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import threading

@dataclass
class LoggingConfig:
    """Configuration de logging pour un composant"""
    logger_name: str
    log_level: str = "INFO"
    log_dir: str = "logs"
    filename_pattern: str = "{component}_{date}.log"
    max_file_size: int = 10485760  # 10MB
    backup_count: int = 5
    console_enabled: bool = True
    file_enabled: bool = True
    format_string: str = "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"

class LoggingManager:
    """Gestionnaire centralisé de logging pour NextGeneration"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self.base_log_dir = Path("logs")
        self.config_file = Path("config/logging_centralized.json")
        self._loggers: Dict[str, logging.Logger] = {}
        self._configs: Dict[str, LoggingConfig] = {}
        
        # Créer l'arborescence de base
        self._setup_directory_structure()
        
        # Charger ou créer la configuration
        self._load_or_create_config()
    
    def _setup_directory_structure(self):
        """Crée l'arborescence de logs centralisée"""
        directories = [
            self.base_log_dir / "agents",
            self.base_log_dir / "agents" / "coordinateur", 
            self.base_log_dir / "agents" / "analyseur",
            self.base_log_dir / "agents" / "evaluateur",
            self.base_log_dir / "agents" / "adaptateur",
            self.base_log_dir / "agents" / "testeur",
            self.base_log_dir / "agents" / "documenteur",
            self.base_log_dir / "agents" / "validateur",
            self.base_log_dir / "tools",
            self.base_log_dir / "tools" / "tts_performance_monitor",
            self.base_log_dir / "tools" / "backup_system", 
            self.base_log_dir / "tools" / "excel_vba_launcher",
            self.base_log_dir / "tools" / "documentation_generator",
            self.base_log_dir / "system",
            self.base_log_dir / "errors",
            Path("config")
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _load_or_create_config(self):
        """Charge ou crée la configuration de logging"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                for name, config in config_data.items():
                    self._configs[name] = LoggingConfig(**config)
        else:
            # Configuration par défaut
            self._create_default_configs()
            self._save_config()
    
    def _create_default_configs(self):
        """Crée les configurations par défaut"""
        default_configs = {
            "template_manager": LoggingConfig(
                logger_name="system.template_manager",
                log_dir="logs/system",
                filename_pattern="template_manager_{date}.log"
            ),
            "agent_factory": LoggingConfig(
                logger_name="system.agent_factory", 
                log_dir="logs/system",
                filename_pattern="agent_factory_{date}.log"
            ),
            "agent_coordinateur": LoggingConfig(
                logger_name="agent.coordination.chef_equipe",
                log_dir="logs/agents/coordinateur",
                filename_pattern="coordinateur_{agent_id}_{date}.log"
            ),
            "agent_analyseur": LoggingConfig(
                logger_name="agent.analysis.structure",
                log_dir="logs/agents/analyseur", 
                filename_pattern="analyseur_{agent_id}_{date}.log"
            ),
            "errors_critical": LoggingConfig(
                logger_name="errors.critical",
                log_dir="logs/errors",
                filename_pattern="critical_errors_{date}.log",
                log_level="ERROR"
            )
        }
        
        self._configs.update(default_configs)
    
    def _save_config(self):
        """Sauvegarde la configuration"""
        config_data = {name: asdict(config) for name, config in self._configs.items()}
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
    
    def generate_agent_logging_config(self, agent_name: str, role: str, domain: str, agent_id: str = None) -> Dict[str, Any]:
        """Génère une configuration de logging pour un agent"""
        agent_id = agent_id or f"{role}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return {
            "logger_name": f"agent.{domain}.{role}.{agent_name}",
            "log_level": "INFO",
            "log_dir": f"logs/agents/{role}",
            "filename_pattern": f"{role}_{agent_id}_{{date}}.log",
            "max_file_size": 10485760,
            "backup_count": 5,
            "console_enabled": True,
            "file_enabled": True,
            "format_string": "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
            "agent_metadata": {
                "agent_id": agent_id,
                "agent_name": agent_name,
                "role": role,
                "domain": domain,
                "created_at": datetime.now().isoformat()
            }
        }
    
    def get_logger(self, config_name: str, custom_config: Dict[str, Any] = None) -> logging.Logger:
        """Obtient un logger configuré"""
        
        if custom_config:
            # Configuration personnalisée (pour agents générés)
            config = LoggingConfig(**custom_config)
            logger_name = config.logger_name
        else:
            # Configuration prédéfinie
            if config_name not in self._configs:
                raise ValueError(f"Configuration de logging '{config_name}' non trouvée")
            config = self._configs[config_name]
            logger_name = config.logger_name
        
        if logger_name in self._loggers:
            return self._loggers[logger_name]
        
        # Créer le logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(getattr(logging, config.log_level))
        logger.handlers.clear()  # Éviter les doublons
        
        # Handler fichier
        if config.file_enabled:
            log_dir = Path(config.log_dir)
            log_dir.mkdir(parents=True, exist_ok=True)
            
            current_date = datetime.now().strftime('%Y%m%d')
            filename = config.filename_pattern.format(
                component=config_name,
                date=current_date,
                **custom_config.get("agent_metadata", {}) if custom_config else {}
            )
            
            log_file = log_dir / filename
            
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=config.max_file_size,
                backupCount=config.backup_count,
                encoding='utf-8'
            )
            file_handler.setFormatter(logging.Formatter(config.format_string))
            logger.addHandler(file_handler)
        
        # Handler console
        if config.console_enabled:
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
        
        self._loggers[logger_name] = logger
        return logger
    
    def get_agent_logger(self, agent_name: str, role: str, domain: str, agent_id: str = None) -> logging.Logger:
        """Obtient un logger pour un agent avec configuration automatique"""
        config = self.generate_agent_logging_config(agent_name, role, domain, agent_id)
        return self.get_logger(None, config)

# Instance globale
logging_manager = LoggingManager()
```

---

### 📄 **2. TemplateManager Modifié (APRÈS)**

```python
#!/usr/bin/env python3
"""
Code Expert NextGeneration - optimized_template_manager
VERSION AVEC LOGGING CENTRALISÉ
"""

import asyncio
import json
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path
from threading import RLock
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import aiofiles
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .agent_templates import AgentTemplate, TemplateValidationError
from ..agents.base_agent import BaseAgent
from ..config.agent_config import AgentFactoryConfig
from ..logging.centralized_logging import logging_manager  # NOUVEAU

# MODIFICATION: Logger centralisé au lieu de logging.getLogger(__name__)
logger = logging_manager.get_logger("template_manager")

@dataclass
class TemplateMetrics:
    """Métriques de performance pour les templates."""
    loads_count: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    reload_count: int = 0
    creation_times: List[float] = field(default_factory=list)
    errors: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    last_accessed: Dict[str, datetime] = field(default_factory=dict)

class TemplateFileWatcher(FileSystemEventHandler):
    """Surveille les modifications des fichiers templates."""
    
    def __init__(self, manager: 'TemplateManager'):
        self.manager = manager
        # MODIFICATION: Logger centralisé
        self.logger = logging_manager.get_logger("template_manager")
        
    def on_modified(self, event):
        """Callback lors de la modification d'un fichier."""
        if event.is_directory or not event.src_path.endswith('.json'):
            return
            
        template_name = Path(event.src_path).stem
        # MODIFICATION: Log centralisé avec catégorie spécifique
        self.logger.info("Template modifié détecté : %s", template_name)
        
        # Invalider le cache pour ce template
        asyncio.create_task(self.manager.reload_template(template_name))

class TemplateManager:
    """Gestionnaire optimisé de templates avec logging centralisé."""
    
    def __init__(
        self,
        config: Optional[AgentFactoryConfig] = None,
        enable_hot_reload: bool = True,
        preload_templates: Optional[List[str]] = None
    ):
        self.config = config or AgentFactoryConfig()
        self._lock = RLock()
        self._cache: Dict[str, AgentTemplate] = {}
        self._timestamps: Dict[str, float] = {}
        self._class_cache: Dict[str, type[BaseAgent]] = {}
        self._metrics = TemplateMetrics()
        self._executor = ThreadPoolExecutor(max_workers=4)
        
        # MODIFICATION: Logger centralisé
        self.logger = logging_manager.get_logger("template_manager")
        
        # Configuration du hot-reload
        self._observer: Optional[Observer] = None
        if enable_hot_reload:
            self._setup_file_watcher()
        
        # Préchargement des templates critiques
        if preload_templates:
            asyncio.create_task(self._preload_templates(preload_templates))
        
        # AJOUT: Log d'initialisation centralisé
        self.logger.info("TemplateManager initialisé avec logging centralisé")

    def create_agent(
        self,
        template_name: str,
        *,
        suffix: str = "",
        config: Optional[Dict[str, Any]] = None
    ) -> BaseAgent:
        """Crée une instance d'agent avec injection automatique de logging centralisé."""
        start_time = time.time()
        
        try:
            # Utiliser la classe en cache si disponible
            with self._lock:
                if template_name in self._class_cache:
                    agent_class = self._class_cache[template_name]
                else:
                    tmpl = self.get_template(template_name)
                    agent_class = tmpl.to_class()
                    self._class_cache[template_name] = agent_class
            
            # MODIFICATION: Injection automatique de la configuration logging
            if config is None:
                config = {}
            
            # Obtenir les informations du template pour la configuration logging
            template = self.get_template(template_name)
            agent_name = f"{template_name}{suffix}"
            agent_id = f"{template_name}_{suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # AJOUT: Génération automatique de la configuration logging
            if "logging" not in config:
                config["logging"] = logging_manager.generate_agent_logging_config(
                    agent_name=agent_name,
                    role=template.role,
                    domain=template.domain,
                    agent_id=agent_id
                )
                
                # Log de l'injection de configuration
                self.logger.debug(
                    "Configuration logging injectée pour agent %s (template=%s, role=%s, domain=%s)",
                    agent_name, template_name, template.role, template.domain
                )
            
            # Créer l'instance (hors du lock)
            agent = agent_class.create(name_suffix=suffix, config=config)
            
            # Métriques
            creation_time = time.time() - start_time
            with self._lock:
                self._metrics.creation_times.append(creation_time)
                if len(self._metrics.creation_times) > 1000:
                    self._metrics.creation_times = self._metrics.creation_times[-1000:]
            
            # MODIFICATION: Log centralisé avec informations enrichies
            self.logger.info(
                "Agent créé avec logging centralisé : %s (template=%s, role=%s, domain=%s, temps=%.3fs)",
                agent.metadata.name,
                template_name,
                template.role,
                template.domain,
                creation_time
            )
            
            return agent
            
        except Exception as e:
            self._metrics.errors[type(e).__name__] += 1
            # MODIFICATION: Log d'erreur centralisé avec contexte enrichi
            self.logger.error(
                "Erreur création agent '%s' (template=%s): %s",
                f"{template_name}{suffix}",
                template_name,
                e,
                exc_info=True
            )
            raise
    
    def bulk_create_agents(
        self,
        specs: List[Dict[str, Any]]
    ) -> Dict[str, BaseAgent]:
        """Crée plusieurs agents en lot avec logging centralisé."""
        agents = {}
        
        # AJOUT: Log de début de création en masse
        self.logger.info("Début création en masse de %d agents", len(specs))
        
        for i, spec in enumerate(specs, 1):
            template_name = spec.get('template')
            if not template_name:
                # MODIFICATION: Log d'avertissement centralisé
                self.logger.warning("Spec %d/%d ignorée (pas de 'template') : %s", i, len(specs), spec)
                continue
            
            suffix = spec.get('suffix', '')
            config = spec.get('config')
            
            try:
                agent = self.create_agent(
                    template_name,
                    suffix=suffix,
                    config=config
                )
                agents[agent.metadata.name] = agent
                
                # AJOUT: Log de progression
                self.logger.debug("Agent %d/%d créé: %s", i, len(specs), agent.metadata.name)
                
            except Exception as e:
                # MODIFICATION: Log d'erreur centralisé avec contexte
                self.logger.error(
                    "Erreur création agent %d/%d (template=%s, suffix=%s): %s",
                    i, len(specs), template_name, suffix, e
                )
        
        # AJOUT: Log de fin avec résumé
        self.logger.info("Création en masse terminée: %d/%d agents créés avec succès", len(agents), len(specs))
        
        return agents

    def get_metrics(self) -> Dict[str, Any]:
        """Retourne les métriques de performance avec informations de logging."""
        with self._lock:
            base_metrics = {
                "loads_count": self._metrics.loads_count,
                "cache_hits": self._metrics.cache_hits,
                "cache_misses": self._metrics.cache_misses,
                "hit_rate": self._metrics.hit_rate,
                "reload_count": self._metrics.reload_count,
                "avg_creation_time": self._metrics.avg_creation_time,
                "total_agents_created": len(self._metrics.creation_times),
                "errors": dict(self._metrics.errors),
                "cache_size": len(self._cache),
                "templates_available": len(self.list_templates())
            }
            
            # AJOUT: Métriques de logging
            base_metrics["logging_info"] = {
                "centralized_logging_enabled": True,
                "logger_name": self.logger.name,
                "log_handlers_count": len(self.logger.handlers),
                "log_level": self.logger.level
            }
            
            return base_metrics
```

---

### 📄 **3. Agent Modifié (APRÈS)**

```python
#!/usr/bin/env python3
"""
🎖️ Agent 0 - Chef d'Équipe Coordinateur
VERSION AVEC LOGGING CENTRALISÉ
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys

# MODIFICATION: Import du LoggingManager centralisé
from ..logging.centralized_logging import logging_manager

class Agent0ChefEquipeCoordinateur:
    """Agent 0 - Chef d'Équipe Coordinateur avec logging centralisé"""
    
    def __init__(self, agent_id: str = None, agent_type: str = "chef_equipe_coordinateur", 
                 target_path: str = None, workspace_path: str = None, **config):
        self.agent_id = agent_id or f"agent_0_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.agent_type = agent_type
        self.config = config
        
        # MODIFICATION: Utilisation du logger centralisé avec configuration spécialisée
        if "logging" in config:
            # Configuration injectée par le TemplateManager
            self.logger = logging_manager.get_logger(None, config["logging"])
        else:
            # Configuration par défaut pour coordination
            self.logger = logging_manager.get_agent_logger(
                agent_name="chef_equipe_coordinateur",
                role="coordinateur", 
                domain="coordination",
                agent_id=self.agent_id
            )
        
        # Configuration équipe
        self.target_path = Path(target_path) if target_path else Path("../agent_factory_implementation/agents")
        self.workspace_path = Path(workspace_path) if workspace_path else Path(".")
        self.equipe_agents = {}
        
        # MODIFICATION: Log centralisé avec métadonnées enrichies
        self.logger.info(
            "🎖️ Agent 0 Chef d'Équipe Coordinateur initialisé avec logging centralisé - ID: %s, Type: %s",
            self.agent_id, self.agent_type,
            extra={
                "agent_id": self.agent_id,
                "agent_type": self.agent_type,
                "target_path": str(self.target_path),
                "workspace_path": str(self.workspace_path),
                "logging_centralized": True
            }
        )
        
    async def startup(self):
        """Démarrage Agent 0 Chef d'Équipe avec logging centralisé"""
        # MODIFICATION: Log structuré avec niveau approprié
        self.logger.info(
            "🚀 Agent 0 Chef d'Équipe %s - DÉMARRAGE",
            self.agent_id,
            extra={"operation": "startup", "agent_id": self.agent_id}
        )
        
        # Vérification des chemins
        if not self.target_path.exists():
            # MODIFICATION: Log d'avertissement centralisé
            self.logger.warning(
                "⚠️ Chemin cible non trouvé: %s - Création automatique",
                self.target_path,
                extra={"operation": "path_creation", "path": str(self.target_path)}
            )
            self.target_path.mkdir(parents=True, exist_ok=True)
        
        # MODIFICATION: Log structuré de configuration
        self.logger.info(
            "✅ Configuration Chef d'Équipe validée",
            extra={
                "operation": "configuration",
                "target_path": str(self.target_path),
                "workspace_path": str(self.workspace_path),
                "workflows_available": len(self.workflows_disponibles)
            }
        )
        
        # MODIFICATION: Log de fin de démarrage
        self.logger.info(
            "✅ Chef d'Équipe prêt à coordonner l'équipe",
            extra={"operation": "startup_complete", "status": "ready"}
        )
        
        return {"status": "started", "agent_id": self.agent_id}
        
    async def _sauvegarder_rapport_final(self, workflow_result: Dict):
        """Sauvegarde du rapport final avec logging centralisé"""
        try:
            # MODIFICATION: Séparation claire logs/rapports avec structure centralisée
            rapport_path = self.workspace_path / "reports" / f"chef_equipe_maintenance_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            rapport_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(rapport_path, 'w', encoding='utf-8') as f:
                json.dump(workflow_result, f, indent=2, ensure_ascii=False, default=str)
            
            # MODIFICATION: Log centralisé avec métadonnées complètes
            self.logger.info(
                "💾 Rapport final sauvegardé avec succès",
                extra={
                    "operation": "report_save",
                    "rapport_path": str(rapport_path),
                    "workflow_status": workflow_result.get("status", "unknown"),
                    "file_size": rapport_path.stat().st_size if rapport_path.exists() else 0,
                    "duration_sec": workflow_result.get("duree_totale_sec", 0)
                }
            )
            
        except Exception as e:
            # MODIFICATION: Log d'erreur centralisé avec contexte complet
            self.logger.error(
                "❌ Erreur sauvegarde rapport final",
                extra={
                    "operation": "report_save_error",
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "workflow_status": workflow_result.get("status", "unknown")
                },
                exc_info=True
            )
            
    async def health_check(self) -> Dict[str, Any]:
        """Vérification santé avec logging centralisé"""
        health_status = {
            "chef_equipe_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": "healthy",
            "agents_disponibles": len(self.equipe_agents),
            "workflows_disponibles": len(self.workflows_disponibles),
            "logging_centralized": True,
            "logger_name": self.logger.name,
            "timestamp": datetime.now().isoformat()
        }
        
        # MODIFICATION: Log de health check avec métriques
        self.logger.info(
            "🏥 Health Check Agent 0 Chef d'Équipe: %s",
            health_status['status'],
            extra={
                "operation": "health_check",
                "health_status": health_status,
                "agents_count": len(self.equipe_agents),
                "workflows_count": len(self.workflows_disponibles)
            }
        )
        
        return health_status
```

---

## 📊 **Plan de Développement Détaillé**

### 🎯 **Phase 1 : Infrastructure (1 semaine)**

#### **Jour 1-2 : LoggingManager**
- [ ] Création classe `LoggingManager` centralisé
- [ ] Tests unitaires configuration et injection
- [ ] Validation arborescence de dossiers

#### **Jour 3-4 : Configuration**
- [ ] Fichier `logging_centralized.json`
- [ ] Templates de configuration par type d'agent
- [ ] Validation JSON Schema

#### **Jour 5-7 : Tests Infrastructure**
- [ ] Tests d'intégration LoggingManager
- [ ] Benchmarks de performance
- [ ] Documentation API

### 🎯 **Phase 2 : Migration TemplateManager (1 semaine)**

#### **Jour 1-3 : Modification TemplateManager**
- [ ] Intégration LoggingManager dans TemplateManager
- [ ] Injection automatique configuration logging
- [ ] Tests création d'agents avec logging centralisé

#### **Jour 4-5 : Optimisations**
- [ ] Cache configuration logging
- [ ] Optimisation performance injection
- [ ] Gestion erreurs et fallbacks

#### **Jour 6-7 : Validation**
- [ ] Tests de non-régression
- [ ] Tests de performance
- [ ] Documentation modifications

### 🎯 **Phase 3 : Migration Agents (2 semaines)**

#### **Semaine 1 : Agents Core**
- [ ] Migration Agent 0 (Coordinateur)
- [ ] Migration Agent 1 (Analyseur)
- [ ] Migration Agent 2 (Évaluateur)
- [ ] Tests fonctionnels

#### **Semaine 2 : Agents Complémentaires**
- [ ] Migration Agents 3-6 (Adaptateur, Testeur, Documenteur, Validateur)
- [ ] Migration outils `/tools/`
- [ ] Tests d'intégration globaux

### 🎯 **Phase 4 : Validation & Déploiement (1 semaine)**

#### **Jour 1-3 : Tests Complets**
- [ ] Tests de charge avec logging centralisé
- [ ] Validation rotation et archivage
- [ ] Tests de récupération après erreur

#### **Jour 4-5 : Documentation**
- [ ] Documentation utilisateur
- [ ] Guide de migration
- [ ] Runbook opérationnel

#### **Jour 6-7 : Déploiement**
- [ ] Déploiement en staging
- [ ] Validation monitoring
- [ ] Migration production

---

## 🚀 **Pistes d'Améliorations**

### 📊 **Monitoring Avancé**
- Dashboard temps réel des logs par agent
- Alertes automatiques sur logs d'erreur
- Métriques de performance logging

### 🔧 **Optimisations Performance**
- Logging asynchrone pour haute charge
- Compression automatique des anciens logs
- Indexation pour recherche rapide

### 🌐 **Intégration Ecosystem**
- Export logs vers Elasticsearch/Splunk
- Intégration Prometheus pour métriques
- Support logging distribué multi-instance

### 🔒 **Sécurité**
- Chiffrement logs sensibles
- Audit trail complet
- Contrôle d'accès par rôle

---

**📅 Durée totale estimée** : 5 semaines  
**👥 Ressources requises** : 2 développeurs senior  
**🎯 Objectif** : Logging centralisé 100% opérationnel 