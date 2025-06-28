# 🛠️ **PLAN D'IMPLÉMENTATION TECHNIQUE DÉTAILLÉ**
## **Guide Technique Sprint-by-Sprint selon Roadmap Optimisée**

---

## 📋 **ARCHITECTURE TECHNIQUE CIBLE**

### **🏗️ STRUCTURE FINALE OPTIMISÉE**
```
nextgeneration/orchestrator/app/
├── agents/
│   ├── agent_templates.py     # 🔄 Version Claude optimisée
│   ├── template_manager.py    # 🔄 Version Claude thread-safe
│   ├── agent_factory.py       # 🔄 Délégation TemplateManager
│   └── templates/             # 📁 JSON signés cryptographiquement
├── config/
│   └── agent_config.py        # 🆕 Pydantic centralisé
├── security/
│   ├── crypto_validator.py    # 🆕 RSA 2048 + SHA-256
│   └── key_rotation.py        # 🆕 Vault integration
├── planes/
│   ├── control_plane.py       # 🆕 Gouvernance
│   └── data_plane.py          # 🆕 Exécution isolée
├── monitoring/
│   └── tracing.py             # 🆕 OpenTelemetry
└── optimization/
    ├── adaptive_threading.py  # 🆕 ThreadPool auto-tuned
    └── compression.py         # 🆕 Zstandard compression
```

---

## 🏃‍♂️ **SPRINT 0 - DÉTAILS TECHNIQUES (J+0 → J+2)**

### **🔧 MIGRATION CODE CLAUDE - SPÉCIFICATIONS**

#### **AgentTemplate Optimisé (enhanced-agent-templates.py)**
```python
"""AgentTemplate avec optimisations Claude"""
from __future__ import annotations
import json
import hashlib
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Type
from dataclasses import dataclass, field
import threading
from functools import lru_cache

@dataclass
class TemplateMetadata:
    """Métadonnées template avec versioning"""
    content_hash: str
    load_time: float
    signature: Optional[str] = None
    version: str = "1.0.0"
    parent_template: Optional[str] = None

class AgentTemplate:
    """Template agent avec héritage et validation avancée"""
    
    def __init__(self, name: str, 
                 templates_dir: Optional[Path] = None,
                 template_data: Optional[Dict] = None):
        self.name = name
        self.templates_dir = templates_dir or Path("templates")
        self._lock = threading.RLock()
        self._data: Optional[Dict] = None
        self._metadata: Optional[TemplateMetadata] = None
        
        if template_data:
            self._load_from_data(template_data)
        else:
            self._load_from_file()
    
    def _load_from_file(self):
        """Chargement thread-safe depuis fichier"""
        with self._lock:
            template_path = self.templates_dir / f"{self.name}.json"
            
            if not template_path.exists():
                raise FileNotFoundError(f"Template {self.name} introuvable: {template_path}")
            
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self._data = json.loads(content)
                
            # Calcul hash pour cache invalidation
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            self._metadata = TemplateMetadata(
                content_hash=content_hash,
                load_time=time.time(),
                signature=self._data.get("_signature"),
                version=self._data.get("_version", "1.0.0"),
                parent_template=self._data.get("parent")
            )
            
            # Héritage si parent spécifié
            if self._metadata.parent_template:
                self._merge_with_parent()
    
    def _merge_with_parent(self):
        """Fusion avec template parent (héritage)"""
        parent_template = AgentTemplate(self._metadata.parent_template, self.templates_dir)
        parent_data = parent_template.data
        
        # Fusion capabilities et tools
        self._data["capabilities"] = list(set(
            parent_data.get("capabilities", []) + self._data.get("capabilities", [])
        ))
        self._data["tools"] = list(set(
            parent_data.get("tools", []) + self._data.get("tools", [])
        ))
        
        # Héritage config par défaut
        parent_config = parent_data.get("default_config", {})
        child_config = self._data.get("default_config", {})
        self._data["default_config"] = {**parent_config, **child_config}
    
    @property
    def data(self) -> Dict:
        return self._data.copy() if self._data else {}
    
    @property
    def metadata(self) -> TemplateMetadata:
        return self._metadata
    
    @property
    def capabilities(self) -> List[str]:
        return self._data.get("capabilities", [])
    
    @property
    def tools(self) -> List[str]:
        return self._data.get("tools", [])
    
    def to_class(self, suffix: str = "") -> Type:
        """Génération dynamique classe agent"""
        from .base_agent import BaseAgent
        
        class_name = f"{self.name.title()}Agent{suffix}"
        
        class DynamicAgent(BaseAgent):
            def __init__(self, config: Optional[Dict] = None):
                super().__init__(config or self._data.get("default_config", {}))
                self.template_name = self.name
                self.template_metadata = self._metadata
            
            async def process(self, query: str) -> str:
                """Traitement basique template-aware"""
                if "analysis" in query.lower():
                    return f"Analyse par {self.template_name}: {query}"
                elif "agent" in query.lower():
                    return f"Agent {self.template_name} prêt"
                elif "role" in query.lower():
                    return f"Rôle: {self._data.get('role', 'undefined')}"
                else:
                    return f"Traitement {self.template_name}: {query}"
            
            def get_capabilities(self) -> List[str]:
                return self.capabilities.copy()
        
        DynamicAgent.__name__ = class_name
        DynamicAgent.__qualname__ = class_name
        return DynamicAgent
    
    def create_instance(self, suffix: str = "", config: Optional[Dict] = None):
        """Factory method pour création instance"""
        agent_class = self.to_class(suffix)
        return agent_class(config)
```

#### **TemplateManager Thread-Safe (optimized-template-manager.py)**
```python
"""TemplateManager optimisé avec cache LRU et hot-reload"""
import asyncio
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from functools import lru_cache
from threading import RLock
from concurrent.futures import ThreadPoolExecutor
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logger = logging.getLogger(__name__)

class TemplateChangeHandler(FileSystemEventHandler):
    """Handler pour hot-reload templates"""
    
    def __init__(self, template_manager):
        self.template_manager = template_manager
        self.debounce_time = 1.0  # Debounce 1 seconde
        self.last_modified = {}
    
    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith('.json'):
            return
            
        now = time.time()
        if (event.src_path in self.last_modified and 
            now - self.last_modified[event.src_path] < self.debounce_time):
            return
            
        self.last_modified[event.src_path] = now
        template_name = Path(event.src_path).stem
        
        logger.info(f"Template modifié détecté: {template_name}")
        asyncio.create_task(self.template_manager.reload_template_async(template_name))

class OptimizedTemplateManager:
    """Manager templates avec cache LRU et monitoring"""
    
    def __init__(self, config):
        self.config = config
        self._cache: Dict[str, AgentTemplate] = {}
        self._cache_times: Dict[str, float] = {}
        self._lock = RLock()
        self._metrics = {
            "templates_loaded": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "reload_count": 0,
            "creation_times": []
        }
        
        # ThreadPool pour opérations async
        self.executor = ThreadPoolExecutor(max_workers=config.max_workers)
        
        # Hot-reload si activé
        if config.enable_hot_reload:
            self._setup_hot_reload()
        
        # Préchargement templates
        self._preload_templates()
    
    def _setup_hot_reload(self):
        """Configuration hot-reload avec watchdog"""
        self.observer = Observer()
        handler = TemplateChangeHandler(self)
        self.observer.schedule(handler, str(self.config.templates_dir), recursive=False)
        self.observer.start()
        logger.info("Hot-reload activé")
    
    def _preload_templates(self):
        """Préchargement templates configurés"""
        for template_name in self.config.preload:
            try:
                self.get_template(template_name)
                logger.debug(f"Template préchargé: {template_name}")
            except Exception as e:
                logger.warning(f"Échec préchargement {template_name}: {e}")
    
    @lru_cache(maxsize=128)
    def get_template(self, name: str) -> AgentTemplate:
        """Récupération template avec cache LRU"""
        with self._lock:
            now = time.time()
            
            # Vérification cache + TTL
            if (name in self._cache and 
                name in self._cache_times and
                now - self._cache_times[name] < self.config.cache_ttl):
                self._metrics["cache_hits"] += 1
                return self._cache[name]
            
            # Cache miss - chargement
            self._metrics["cache_misses"] += 1
            template = AgentTemplate(name, self.config.templates_dir)
            
            self._cache[name] = template
            self._cache_times[name] = now
            self._metrics["templates_loaded"] += 1
            
            logger.debug(f"Template chargé: {name}")
            return template
    
    async def reload_template_async(self, name: str):
        """Rechargement asynchrone template"""
        def _reload():
            with self._lock:
                if name in self._cache:
                    del self._cache[name]
                if name in self._cache_times:
                    del self._cache_times[name]
                
                # Invalidation cache LRU
                self.get_template.cache_clear()
                
                # Rechargement
                self.get_template(name)
                self._metrics["reload_count"] += 1
                
        await asyncio.get_event_loop().run_in_executor(self.executor, _reload)
        logger.info(f"Template rechargé: {name}")
    
    def create_agent(self, template_name: str, suffix: str = "", config: Optional[Dict] = None):
        """Création agent synchrone"""
        start_time = time.time()
        try:
            template = self.get_template(template_name)
            agent = template.create_instance(suffix, config)
            
            creation_time = time.time() - start_time
            self._metrics["creation_times"].append(creation_time)
            
            return agent
        except Exception as e:
            logger.error(f"Échec création agent {template_name}: {e}")
            raise
    
    async def create_agent_async(self, template_name: str, suffix: str = "", config: Optional[Dict] = None):
        """Création agent asynchrone"""
        return await asyncio.get_event_loop().run_in_executor(
            self.executor, 
            self.create_agent, 
            template_name, 
            suffix, 
            config
        )
    
    def bulk_create_agents(self, specs: List[Dict]) -> Dict[str, Any]:
        """Création en lot avec parallélisation"""
        results = {}
        
        def create_single(spec):
            template_name = spec["template_name"]
            suffix = spec.get("suffix", "")
            config = spec.get("config")
            
            try:
                agent = self.create_agent(template_name, suffix, config)
                return f"{template_name}{suffix}", agent
            except Exception as e:
                logger.error(f"Échec création {template_name}: {e}")
                return f"{template_name}{suffix}", None
        
        # Exécution parallèle
        futures = [self.executor.submit(create_single, spec) for spec in specs]
        
        for future in futures:
            agent_id, agent = future.result()
            results[agent_id] = agent
            
        return results
    
    def get_metrics(self) -> Dict[str, Any]:
        """Métriques détaillées manager"""
        with self._lock:
            creation_times = self._metrics["creation_times"]
            cache_total = self._metrics["cache_hits"] + self._metrics["cache_misses"]
            
            return {
                "templates_loaded": self._metrics["templates_loaded"],
                "cache_hit_rate": self._metrics["cache_hits"] / max(cache_total, 1),
                "cache_hits": self._metrics["cache_hits"],
                "cache_misses": self._metrics["cache_misses"],
                "reload_count": self._metrics["reload_count"],
                "creation_time_avg": sum(creation_times) / max(len(creation_times), 1),
                "creation_time_p95": sorted(creation_times)[int(len(creation_times) * 0.95)] if creation_times else 0,
                "active_templates": len(self._cache),
                "executor_threads": self.executor._threads
            }
    
    def list_templates(self) -> List[str]:
        """Liste templates disponibles"""
        template_files = self.config.templates_dir.glob("*.json")
        return [f.stem for f in template_files]
    
    def shutdown(self):
        """Arrêt propre manager"""
        if hasattr(self, 'observer'):
            self.observer.stop()
            self.observer.join()
        self.executor.shutdown(wait=True)

# Instance globale
from ..config.agent_config import config
template_manager = OptimizedTemplateManager(config)
```

### **🔬 TESTS VALIDATION SPRINT 0**

#### **Test Smoke Complet**
```python
# tests/test_smoke.py
"""Tests smoke pour validation Sprint 0"""
import pytest
import json
from pathlib import Path
from orchestrator.app.agents.agent_templates import AgentTemplate
from orchestrator.app.agents.template_manager import template_manager
from orchestrator.app.config.agent_config import config

def test_config_loading():
    """Test chargement configuration"""
    assert config.templates_dir.exists()
    assert config.cache_ttl > 0
    assert len(config.preload) > 0

def test_agent_template_loading():
    """Test chargement template basique"""
    template = AgentTemplate("documentaliste")
    assert template.name == "documentaliste"
    assert len(template.capabilities) > 0
    assert template.metadata.content_hash

def test_template_manager_basic():
    """Test manager basique"""
    template = template_manager.get_template("documentaliste")
    assert template is not None
    
    metrics = template_manager.get_metrics()
    assert "templates_loaded" in metrics
    assert metrics["templates_loaded"] > 0

def test_agent_creation():
    """Test création agent"""
    agent = template_manager.create_agent("documentaliste")
    assert agent is not None
    assert hasattr(agent, "process")
    assert hasattr(agent, "get_capabilities")
    
    capabilities = agent.get_capabilities()
    assert len(capabilities) > 0

@pytest.mark.asyncio
async def test_async_creation():
    """Test création asynchrone"""
    agent = await template_manager.create_agent_async("documentaliste")
    assert agent is not None

def test_bulk_creation():
    """Test création en lot"""
    specs = [
        {"template_name": "documentaliste", "suffix": "_test1"},
        {"template_name": "genie_logiciel", "suffix": "_test2"}
    ]
    
    results = template_manager.bulk_create_agents(specs)
    assert len(results) == 2
    assert "documentaliste_test1" in results
    assert "genie_logiciel_test2" in results

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

---

## 🧪 **SPRINT 1 - TESTS AVANCÉS (J+3 → J+6)**

### **🔥 Test Hot-Reload Production**
```python
# tests/test_hot_reload_production.py
"""Test hot-reload avec conditions production"""
import pytest
import asyncio
import json
import time
from pathlib import Path
from unittest.mock import patch
from orchestrator.app.agents.template_manager import template_manager

@pytest.mark.asyncio
async def test_hot_reload_under_load(tmp_path):
    """Test hot-reload sous charge"""
    
    # Setup template temporaire
    template_data = {
        "name": "load_test_agent",
        "role": "load_tester",
        "domain": "testing",
        "capabilities": ["load_testing"],
        "tools": ["artillery", "k6"]
    }
    
    template_path = tmp_path / "load_test_agent.json"
    template_path.write_text(json.dumps(template_data))
    
    # Configuration manager temporaire
    with patch.object(template_manager, 'config') as mock_config:
        mock_config.templates_dir = tmp_path
        mock_config.cache_ttl = 1.0  # TTL court pour test
        
        # Chargement initial
        await template_manager.reload_template_async("load_test_agent")
        
        # Création agents en parallèle pendant modification
        async def create_agents():
            agents = []
            for i in range(50):
                agent = await template_manager.create_agent_async("load_test_agent", suffix=f"_{i}")
                agents.append(agent)
                await asyncio.sleep(0.01)  # 10ms entre créations
            return agents
        
        async def modify_template():
            await asyncio.sleep(0.25)  # Attendre démarrage créations
            
            # Modification template
            template_data["tools"].append("locust")
            template_path.write_text(json.dumps(template_data))
            
            await asyncio.sleep(0.1)  # Temps propagation
        
        # Exécution parallèle
        agents_task = asyncio.create_task(create_agents())
        modify_task = asyncio.create_task(modify_template())
        
        agents, _ = await asyncio.gather(agents_task, modify_task)
        
        # Vérifications
        assert len(agents) == 50
        
        # Vérifier que nouveaux agents ont la modification
        new_agent = await template_manager.create_agent_async("load_test_agent", suffix="_new")
        assert "locust" in new_agent.get_capabilities() or "locust" in template_manager.get_template("load_test_agent").tools

@pytest.mark.asyncio 
async def test_hot_reload_debouncing():
    """Test debouncing modifications rapides"""
    # Test que modifications rapides successives ne causent qu'un seul reload
    pass

def test_hot_reload_memory_leak():
    """Test absence fuite mémoire lors hot-reload répétés"""
    import psutil
    import gc
    
    process = psutil.Process()
    initial_memory = process.memory_info().rss
    
    # 100 hot-reloads
    for i in range(100):
        template_manager.get_template.cache_clear()
        template_manager.get_template("documentaliste")
        
        if i % 10 == 0:
            gc.collect()
    
    final_memory = process.memory_info().rss
    memory_growth = (final_memory - initial_memory) / initial_memory
    
    # Croissance mémoire < 10%
    assert memory_growth < 0.1, f"Fuite mémoire détectée: {memory_growth:.1%}"
```

### **⚡ Benchmark Locust Intégré**
```python
# tests/locust_benchmark.py
"""Benchmark Locust pour validation performance CI"""
from locust import HttpUser, task, between, events
import time
import logging

# Configuration logging pour CI
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentFactoryUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    def on_start(self):
        """Setup utilisateur"""
        self.templates = ["documentaliste", "genie_logiciel", "hardware"]
        self.creation_times = []
    
    @task(3)
    def create_single_agent(self):
        """Création agent unique"""
        template_name = self.random.choice(self.templates)
        
        start_time = time.time()
        with self.client.post("/factory/agents", 
                             json={"template_name": template_name},
                             catch_response=True) as response:
            
            duration = time.time() - start_time
            self.creation_times.append(duration)
            
            if response.status_code == 200:
                if duration < 0.1:  # < 100ms
                    response.success()
                else:
                    response.failure(f"Trop lent: {duration:.3f}s > 100ms")
            else:
                response.failure(f"Status {response.status_code}")
    
    @task(1)
    def bulk_create_agents(self):
        """Création en lot"""
        specs = [
            {"template_name": template, "suffix": f"_bulk_{int(time.time())}"}
            for template in self.templates
        ]
        
        with self.client.post("/factory/agents/bulk",
                             json={"specs": specs},
                             catch_response=True) as response:
            
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Bulk creation failed: {response.status_code}")
    
    @task(1)
    def get_metrics(self):
        """Récupération métriques"""
        with self.client.get("/factory/metrics") as response:
            if response.status_code == 200:
                metrics = response.json()
                cache_hit_rate = metrics.get("cache_hit_rate", 0)
                
                if cache_hit_rate > 0.8:  # > 80%
                    logger.info(f"Cache hit rate OK: {cache_hit_rate:.1%}")
                else:
                    logger.warning(f"Cache hit rate faible: {cache_hit_rate:.1%}")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Validation métriques finales"""
    logger.info("=== RÉSULTATS BENCHMARK ===")
    
    stats = environment.stats.total
    logger.info(f"Requêtes totales: {stats.num_requests}")
    logger.info(f"Échecs: {stats.num_failures}")
    logger.info(f"Taux succès: {(1 - stats.num_failures/stats.num_requests)*100:.1f}%")
    logger.info(f"Temps réponse moyen: {stats.avg_response_time:.1f}ms")
    logger.info(f"Temps réponse p95: {stats.get_response_time_percentile(0.95):.1f}ms")
    
    # Assertions pour CI
    assert stats.num_failures / stats.num_requests < 0.01, "Taux échec > 1%"
    assert stats.avg_response_time < 100, f"Temps moyen {stats.avg_response_time:.1f}ms > 100ms"
    assert stats.get_response_time_percentile(0.95) < 200, "P95 > 200ms"
    
    logger.info("✅ Benchmark validé - Performance OK")

# Configuration Locust pour CI
if __name__ == "__main__":
    import subprocess
    import sys
    
    # Lancement Locust en mode headless pour CI
    cmd = [
        "locust", 
        "-f", __file__,
        "--host", "http://localhost:8000",
        "--users", "50",
        "--spawn-rate", "10", 
        "--run-time", "2m",
        "--headless"
    ]
    
    result = subprocess.run(cmd)
    sys.exit(result.returncode)
```

---

## 🔒 **SPRINT 2 - SÉCURITÉ CRYPTOGRAPHIQUE (Semaine +1)**

### **🔐 Implémentation Signature RSA Production**
```python
# orchestrator/app/security/template_signer.py
"""Signature et validation cryptographique templates"""
import base64
import json
import hashlib
from pathlib import Path
from typing import Dict, Tuple
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

class TemplateSigner:
    """Signature cryptographique templates (RSA 2048 + SHA-256)"""
    
    def __init__(self, private_key_path: str):
        """Chargement clé privée pour signature"""
        with open(private_key_path, "rb") as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(), 
                password=None
            )
    
    def sign_template(self, template_data: Dict) -> str:
        """Signature template JSON"""
        # Hash canonique
        canonical_json = json.dumps(template_data, sort_keys=True, separators=(',', ':'))
        template_hash = hashlib.sha256(canonical_json.encode('utf-8')).digest()
        
        # Signature RSA-PSS
        signature = self.private_key.sign(
            template_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return base64.b64encode(signature).decode('ascii')
    
    def sign_template_file(self, template_path: Path) -> Dict:
        """Signature fichier template avec injection signature"""
        with open(template_path, 'r', encoding='utf-8') as f:
            template_data = json.load(f)
        
        # Suppression signature existante pour calcul
        template_data.pop('_signature', None)
        
        # Génération signature
        signature = self.sign_template(template_data)
        
        # Injection signature
        template_data['_signature'] = signature
        template_data['_signed_at'] = time.time()
        
        # Sauvegarde template signé
        with open(template_path, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, indent=2, ensure_ascii=False)
        
        return template_data

# Script signature en lot
if __name__ == "__main__":
    import sys
    import time
    
    if len(sys.argv) != 3:
        print("Usage: python template_signer.py <private_key_path> <templates_dir>")
        sys.exit(1)
    
    private_key_path = sys.argv[1]
    templates_dir = Path(sys.argv[2])
    
    signer = TemplateSigner(private_key_path)
    
    for template_file in templates_dir.glob("*.json"):
        print(f"Signature {template_file.name}...")
        try:
            signer.sign_template_file(template_file)
            print(f"✅ {template_file.name} signé")
        except Exception as e:
            print(f"❌ Échec signature {template_file.name}: {e}")
    
    print("Signature templates terminée")
```

### **🔄 Intégration Vault Production**
```python
# orchestrator/app/security/vault_integration.py
"""Intégration HashiCorp Vault pour gestion clés"""
import hvac
import logging
from typing import Optional, Dict
from datetime import datetime, timedelta
from prometheus_client import Counter, Gauge

logger = logging.getLogger(__name__)

# Métriques Vault
VAULT_OPERATIONS = Counter('vault_operations_total', 'Vault operations', ['operation', 'status'])
VAULT_KEY_AGE = Gauge('vault_key_age_days', 'Age of current signing key in days')

class VaultKeyManager:
    """Gestionnaire clés via Vault"""
    
    def __init__(self, vault_url: str, vault_token: str, mount_point: str = "kv"):
        self.client = hvac.Client(url=vault_url, token=vault_token)
        self.mount_point = mount_point
        self.key_path = "agent-factory/signing-keys"
        
        # Vérification connexion
        if not self.client.is_authenticated():
            raise ConnectionError("Authentification Vault échouée")
        
        logger.info(f"Vault connecté: {vault_url}")
    
    def get_current_keys(self) -> Dict[str, str]:
        """Récupération paire clés courante"""
        try:
            response = self.client.secrets.kv.v2.read_secret_version(
                path=self.key_path,
                mount_point=self.mount_point
            )
            
            keys_data = response['data']['data']
            VAULT_OPERATIONS.labels(operation='read_keys', status='success').inc()
            
            # Calcul âge clé
            created_at = keys_data.get('created_at')
            if created_at:
                key_age = (datetime.now() - datetime.fromisoformat(created_at)).days
                VAULT_KEY_AGE.set(key_age)
            
            return {
                'public_key': keys_data['public_key'],
                'private_key': keys_data.get('private_key'),  # Optionnel
                'created_at': created_at,
                'key_id': keys_data.get('key_id', 'default')
            }
            
        except Exception as e:
            VAULT_OPERATIONS.labels(operation='read_keys', status='error').inc()
            logger.error(f"Échec lecture clés Vault: {e}")
            raise
    
    def rotate_keys(self, reason: str = "scheduled") -> Dict[str, str]:
        """Rotation paire clés"""
        try:
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.primitives.asymmetric import rsa
            
            # Génération nouvelle paire RSA 2048
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            
            public_key = private_key.public_key()
            
            # Sérialisation PEM
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode('utf-8')
            
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')
            
            # Stockage Vault
            new_keys_data = {
                'public_key': public_pem,
                'private_key': private_pem,
                'created_at': datetime.now().isoformat(),
                'key_id': f"key_{int(datetime.now().timestamp())}",
                'rotation_reason': reason
            }
            
            self.client.secrets.kv.v2.create_or_update_secret(
                path=self.key_path,
                secret=new_keys_data,
                mount_point=self.mount_point
            )
            
            VAULT_OPERATIONS.labels(operation='rotate_keys', status='success').inc()
            VAULT_KEY_AGE.set(0)  # Nouvelle clé
            
            logger.info(f"Rotation clés réussie - Raison: {reason}")
            
            return new_keys_data
            
        except Exception as e:
            VAULT_OPERATIONS.labels(operation='rotate_keys', status='error').inc()
            logger.error(f"Échec rotation clés: {e}")
            raise
    
    def should_rotate_keys(self) -> bool:
        """Vérification nécessité rotation"""
        try:
            keys = self.get_current_keys()
            created_at = keys.get('created_at')
            
            if not created_at:
                logger.warning("Date création clé manquante - rotation recommandée")
                return True
            
            # Rotation si > 90 jours
            key_age = datetime.now() - datetime.fromisoformat(created_at)
            if key_age > timedelta(days=90):
                logger.info(f"Clé ancienne ({key_age.days} jours) - rotation nécessaire")
                return True
            
            # Rotation si taux échec signature élevé
            from .crypto_validator import SIGNATURE_FAILURES
            failure_rate = SIGNATURE_FAILURES._value.get()
            if failure_rate > 50:  # Seuil ajustable
                logger.warning(f"Taux échec signature élevé ({failure_rate}) - rotation recommandée")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Erreur vérification rotation: {e}")
            return False
```

---

## 🎯 **VALIDATION FINALE & MÉTRIQUES**

### **📊 Dashboard Monitoring Production**
```python
# orchestrator/app/monitoring/dashboard.py
"""Dashboard métriques production"""
from prometheus_client import start_http_server, Summary, Counter, Histogram, Gauge
import time
import psutil

# Métriques Agent Factory
AGENT_CREATION_TIME = Summary('agent_creation_seconds', 'Time to create agents', ['template'])
TEMPLATE_CACHE_HITS = Counter('template_cache_hits_total', 'Template cache hits')
TEMPLATE_CACHE_MISSES = Counter('template_cache_misses_total', 'Template cache misses')
ACTIVE_AGENTS = Gauge('active_agents_total', 'Number of active agents')
TEMPLATE_SIGNATURE_VALIDATIONS = Counter('template_signature_validations_total', 
                                        'Template signature validations', ['status'])

# Métriques système
SYSTEM_CPU_PERCENT = Gauge('system_cpu_percent', 'System CPU usage')
SYSTEM_MEMORY_PERCENT = Gauge('system_memory_percent', 'System memory usage')
THREAD_POOL_SIZE = Gauge('thread_pool_size', 'Current thread pool size')

class ProductionMetrics:
    """Collecteur métriques production"""
    
    def __init__(self):
        self.start_time = time.time()
        
    def start_metrics_server(self, port: int = 9090):
        """Démarrage serveur métriques Prometheus"""
        start_http_server(port)
        logger.info(f"Serveur métriques démarré sur port {port}")
        
        # Collecte métriques système périodique
        import threading
        self.metrics_thread = threading.Thread(target=self._collect_system_metrics, daemon=True)
        self.metrics_thread.start()
    
    def _collect_system_metrics(self):
        """Collecte métriques système en continu"""
        while True:
            try:
                # CPU et mémoire
                SYSTEM_CPU_PERCENT.set(psutil.cpu_percent(interval=1))
                SYSTEM_MEMORY_PERCENT.set(psutil.virtual_memory().percent)
                
                # ThreadPool
                from ..agents.template_manager import template_manager
                if hasattr(template_manager, 'executor'):
                    THREAD_POOL_SIZE.set(len(template_manager.executor._threads))
                
                time.sleep(30)  # Collecte toutes les 30s
                
            except Exception as e:
                logger.error(f"Erreur collecte métriques: {e}")
                time.sleep(60)
    
    @staticmethod
    def record_agent_creation(template_name: str, duration: float):
        """Enregistrement création agent"""
        AGENT_CREATION_TIME.labels(template=template_name).observe(duration)
    
    @staticmethod
    def record_cache_hit():
        """Enregistrement cache hit"""
        TEMPLATE_CACHE_HITS.inc()
    
    @staticmethod
    def record_cache_miss():
        """Enregistrement cache miss"""
        TEMPLATE_CACHE_MISSES.inc()
    
    @staticmethod
    def record_signature_validation(success: bool):
        """Enregistrement validation signature"""
        status = 'success' if success else 'failure'
        TEMPLATE_SIGNATURE_VALIDATIONS.labels(status=status).inc()

# Instance globale
production_metrics = ProductionMetrics()
```

---

**🎯 Plan d'implémentation technique détaillé optimisé pour delivery Sprint 5 - Production ready avec monitoring complet et sécurité shift-left** 