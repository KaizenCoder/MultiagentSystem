# 🚀 **PLAN D'ACTION RÉVISÉ - AGENT FACTORY PATTERN**
## **Roadmap Optimisée Post-Expert Feedback avec Shift-Left Security**

---

## 📋 **SYNTHÈSE EXÉCUTIVE CONSOLIDÉE**

### **✅ VALIDATION UNANIME DES 3 EXPERTS**
- **Claude (Anthropic)** : Architecture entreprise + Code production-ready ✅
- **ChatGPT (OpenAI)** : Plan d'implémentation pragmatique + Timeline concrète ✅  
- **Gemini (Google)** : Innovations avancées + Vision long terme ✅

### **🎯 OBJECTIF VALIDÉ ET RAFFINÉ**
- **Réduction 80%** du temps de création d'agents (2-3h → 3-5 minutes) ✅
- **Architecture Orchestration as a Service** validée comme future-ready ✅
- **Sécurité Shift-Left** : Signature crypto dès Sprint 2 (non plus Phase 3) ✅

### **⚡ OPTIMISATIONS PLAN RÉVISÉ**
- **Gain temps 20%** : Fusion phases redondantes
- **Sécurité avancée** : Semaine +1 (vs Semaine +2 initialement)
- **Production-ready** : Semaine +4 avec perf + monitoring complets

---

## 🏃‍♂️ **ROADMAP SPRINT-BASED OPTIMISÉE**

### **📅 SPRINT 0 - KICK-OFF (J+0 → J+2)**
*Fusion des anciennes Phase 1 J+0 et J+1 pour gagner 1 jour*

#### **🎯 OBJECTIF**
Code base production-ready opérationnelle avec CI/CD

#### **📦 LIVRABLES MAJEURS**
- **Merge code Claude** : Adoption versions optimisées AgentTemplate + TemplateManager
- **Config Pydantic unifiée** : Configuration centralisée avec variables environnement
- **CI "smoke" + lint** : GitHub Actions avec mypy --strict + ruff (fail-fast)

#### **🔧 ACTIONS DÉTAILLÉES**

**J+0 : Migration Code Base (4h)**
```bash
# Backup + adoption versions Claude
cp orchestrator/app/agents/agent_templates.py orchestrator/app/agents/agent_templates.py.bak
cp enhanced-agent-templates.py orchestrator/app/agents/agent_templates.py
cp optimized-template-manager.py orchestrator/app/agents/template_manager.py
```

**J+1 : Configuration Unifiée (3h)**
```python
# orchestrator/app/config/agent_config.py
class AgentFactoryConfig(BaseSettings):
    # Chemins
    templates_dir: Path = Path(__file__).resolve().parent.parent / "agents" / "templates"
    
    # Performance optimisée
    cache_ttl: float = 300.0        # 5 min prod, 60s dev (adaptatif)
    max_workers: int = 8            # ThreadPool auto-tuned
    
    # Sécurité (préparation Sprint 2)
    enable_signature_validation: bool = True  # Activé dès Sprint 2
    rsa_public_key_path: str = "keys/template_signing.pub"
    
    class Config:
        env_prefix = "NG_"
```

**J+2 : CI/CD Pipeline (2h)**
```yaml
# .github/workflows/agent-factory-ci.yml
name: Agent Factory CI
on: [push, pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Lint with ruff
        run: ruff check . --fix
      - name: Type check with mypy
        run: mypy --strict orchestrator/app/agents/
      - name: Security scan
        run: pip-audit --desc
      - name: Smoke tests
        run: pytest tests/test_smoke.py -v
```

#### **✅ DEFINITION OF DONE SPRINT 0**
- ✅ Code Claude intégré et fonctionnel
- ✅ Configuration Pydantic centralisée
- ✅ CI pipeline opérationnelle (lint + type check + smoke tests)
- ✅ 0 vulnérabilité critical/high (pip-audit)

---

### **📅 SPRINT 1 - TESTS & OBSERVABILITÉ DE BASE (J+3 → J+6)**

#### **🎯 OBJECTIF**
Validation robustesse et performance avec monitoring basique

#### **📦 LIVRABLES MAJEURS**
- **Tests complets** : Héritage, hot-reload, performance
- **Endpoint métriques** : /factory/metrics + /health
- **Benchmark Locust** : Validation < 100ms/agent en CI

#### **🧪 TESTS SPÉCIFIQUES**

**J+3-4 : Tests Fonctionnels (6h)**
```python
# tests/test_template_inheritance.py - Héritage templates
# tests/test_hot_reload.py - Rechargement automatique
# tests/test_scalability_load.py - Performance parallèle

# Nouveau : Benchmark Locust intégré CI
# tests/locust_benchmark.py
from locust import HttpUser, task, between

class AgentFactoryUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task
    def create_agent(self):
        response = self.client.post("/factory/agents", 
                                  json={"template_name": "documentaliste"})
        assert response.status_code == 200
        # Validation < 100ms
        assert response.elapsed.total_seconds() < 0.1
```

**J+5-6 : API Métriques (4h)**
```python
# orchestrator/app/main.py - Endpoints monitoring
@app.get("/factory/metrics")
def get_factory_metrics():
    return {
        "templates_loaded": template_manager.get_metrics()["templates_loaded"],
        "cache_hit_rate": template_manager.get_metrics()["cache_hit_rate"],
        "creation_time_p95": template_manager.get_metrics()["creation_time_p95"],
        "active_agents": len(template_manager.active_agents)
    }

@app.get("/health")
def health_check():
    stats = agent_factory.get_factory_stats()
    return {
        "status": "healthy" if stats["templates_loaded"] > 0 else "degraded",
        "version": "1.0.0-sprint1",
        "uptime_seconds": time.time() - start_time
    }
```

#### **✅ DEFINITION OF DONE SPRINT 1**
- ✅ Tests héritage + hot-reload + performance verts
- ✅ Benchmark Locust < 100ms/agent validé en CI
- ✅ API métriques exposée et documentée
- ✅ p95 performance respecté

---

### **📅 SPRINT 2 - SÉCURITÉ "SHIFT-LEFT" (Semaine +1)**
*Avancement majeur : Sécurité cryptographique dès maintenant (non plus Sprint 3)*

#### **🎯 OBJECTIF**
Sécurité entreprise opérationnelle avant staging

#### **📦 LIVRABLES MAJEURS**
- **Signature RSA 2048 + SHA-256** : Validation obligatoire au load des templates
- **Policy OPA basique** : Blacklist tools dangereux
- **Rotation clés** : Intégration Vault + alertes Prometheus

#### **🔐 SÉCURITÉ CRYPTOGRAPHIQUE**

```python
# orchestrator/app/security/crypto_validator.py
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import json
import hashlib
import logging

logger = logging.getLogger(__name__)

class ProductionSecurityValidator:
    """Validation cryptographique production (RSA 2048 + SHA-256)"""
    
    def __init__(self, public_key_path: str):
        try:
            with open(public_key_path, "rb") as f:
                self.public_key = serialization.load_pem_public_key(f.read())
            logger.info(f"Clé publique chargée: {public_key_path}")
        except Exception as e:
            logger.error(f"Échec chargement clé: {e}")
            raise
            
    def verify_template_signature(self, template_data: Dict, signature_b64: str) -> bool:
        """Vérification signature template (obligatoire)"""
        try:
            # Décodage signature base64
            signature = base64.b64decode(signature_b64)
            
            # Hash canonique du template
            template_content = json.dumps(template_data, sort_keys=True, separators=(',', ':'))
            template_hash = hashlib.sha256(template_content.encode('utf-8')).digest()
            
            # Vérification RSA-PSS
            self.public_key.verify(
                signature,
                template_hash,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            logger.debug(f"Signature valide pour template {template_data.get('name')}")
            return True
            
        except Exception as e:
            logger.error(f"Signature invalide: {e}")
            return False
            
    def validate_policy_opa(self, template_data: Dict) -> bool:
        """Validation politique OPA basique"""
        dangerous_tools = [
            "shell_command", "file_system_write", "network_access", 
            "subprocess", "eval", "exec"
        ]
        
        tools = template_data.get("tools", [])
        blocked_tools = [tool for tool in tools if tool in dangerous_tools]
        
        if blocked_tools:
            logger.warning(f"Tools bloqués par politique: {blocked_tools}")
            return False
            
        return True
```

#### **🔄 ROTATION CLÉS & MONITORING**

```python
# orchestrator/app/security/key_rotation.py
import hvac  # HashiCorp Vault
from prometheus_client import Counter

SIGNATURE_FAILURES = Counter('template_signature_failures_total', 
                            'Template signature validation failures')

class KeyRotationManager:
    """Gestion rotation clés via Vault"""
    
    def __init__(self, vault_url: str, vault_token: str):
        self.vault_client = hvac.Client(url=vault_url, token=vault_token)
        
    def get_current_public_key(self) -> str:
        """Récupération clé publique courante depuis Vault"""
        response = self.vault_client.secrets.kv.v2.read_secret_version(
            path='agent-factory/signing-keys'
        )
        return response['data']['data']['public_key']
        
    def rotate_keys_if_needed(self) -> bool:
        """Rotation automatique si nécessaire"""
        # Logique rotation basée sur âge clé + métriques échecs
        failure_rate = SIGNATURE_FAILURES._value.get()
        if failure_rate > 10:  # Seuil alerte
            logger.warning("Taux échec signature élevé - rotation recommandée")
            return True
        return False
```

#### **✅ DEFINITION OF DONE SPRINT 2**
- ✅ Signature RSA obligatoire et fonctionnelle
- ✅ Policy OPA bloque tools dangereux
- ✅ Intégration Vault pour rotation clés
- ✅ Métriques sécurité exposées Prometheus
- ✅ 0 vulnérabilité critical/high Trivy

---

### **📅 SPRINT 3 - CONTROL/DATA PLANE & SANDBOX (Semaine +2)**

#### **🎯 OBJECTIF**
Architecture séparée + Sandbox pour agents à risque

#### **📦 LIVRABLES MAJEURS**
- **Refactor Control/Data Plane** : Séparation gouvernance/exécution
- **WASI sandbox prototype** : Isolation agents risqués
- **RBAC minimale FastAPI** : Authentification/autorisation

#### **🏗️ ARCHITECTURE SÉPARÉE**

```python
# orchestrator/app/planes/control_plane.py
class ControlPlane:
    """Plan contrôle - Gouvernance et politiques"""
    
    def __init__(self):
        self.security_validator = ProductionSecurityValidator("keys/template_signing.pub")
        self.policy_engine = OPAPolicyEngine()
        self.audit_logger = AuditLogger()
        
    async def authorize_agent_creation(self, 
                                     template_name: str, 
                                     user_context: Dict) -> AuthResult:
        """Autorisation création agent avec audit"""
        
        # 1. Validation utilisateur
        if not self._validate_user_permissions(user_context):
            self.audit_logger.log_access_denied(user_context, template_name)
            raise PermissionError("Permissions insuffisantes")
            
        # 2. Validation template sécurisé
        template = await template_manager.get_template_async(template_name)
        if not self.security_validator.verify_template_signature(
            template.data, template.signature
        ):
            self.audit_logger.log_security_violation(template_name, "signature_invalid")
            raise SecurityError("Signature template invalide")
            
        # 3. Validation politique
        if not self.security_validator.validate_policy_opa(template.data):
            self.audit_logger.log_policy_violation(template_name, template.data.get("tools"))
            raise PolicyError("Violation politique sécurité")
            
        return AuthResult(authorized=True, sandbox_required=self._requires_sandbox(template))

# orchestrator/app/planes/data_plane.py
class DataPlane:
    """Plan données - Exécution isolée"""
    
    def __init__(self):
        self.wasi_sandbox = WASISandbox()
        self.native_executor = NativeExecutor()
        
    async def execute_agent_creation(self, 
                                   template_name: str, 
                                   auth_result: AuthResult) -> Agent:
        """Exécution création avec isolation appropriée"""
        
        if auth_result.sandbox_required:
            # Exécution sandboxée WASI
            return await self.wasi_sandbox.create_agent_safely(template_name)
        else:
            # Exécution native optimisée
            return await self.native_executor.create_agent(template_name)
```

#### **🔐 SANDBOX WASI PROTOTYPE**

```python
# orchestrator/app/sandbox/wasi_sandbox.py
import wasmtime
from typing import Dict, Any

class WASISandbox:
    """Sandbox WASI pour agents à risque"""
    
    def __init__(self):
        self.engine = wasmtime.Engine()
        self.overhead_threshold = 0.2  # 20% overhead max
        
    async def create_agent_safely(self, template_name: str) -> Agent:
        """Création agent en environnement isolé"""
        
        start_time = time.time()
        
        # Configuration WASI avec restrictions
        wasi_config = wasmtime.WasiConfig()
        wasi_config.inherit_stdout()
        wasi_config.inherit_stderr()
        # Pas d'accès filesystem par défaut
        
        store = wasmtime.Store(self.engine)
        store.set_wasi(wasi_config)
        
        try:
            # Chargement module WASM agent
            module = wasmtime.Module(self.engine, self._compile_agent_to_wasm(template_name))
            instance = wasmtime.Instance(store, module, [])
            
            # Exécution contrôlée
            agent = self._execute_agent_creation(store, instance, template_name)
            
            # Vérification overhead
            execution_time = time.time() - start_time
            native_time = await self._benchmark_native_creation(template_name)
            overhead = (execution_time - native_time) / native_time
            
            if overhead > self.overhead_threshold:
                logger.warning(f"Sandbox overhead {overhead:.1%} > {self.overhead_threshold:.1%}")
                
            return agent
            
        except Exception as e:
            logger.error(f"Échec sandbox WASI: {e}")
            raise SandboxError(f"Isolation failed: {e}")
```

#### **✅ DEFINITION OF DONE SPRINT 3**
- ✅ Control/Data Plane séparés et opérationnels
- ✅ Sandbox WASI fonctionnel avec overhead < 20%
- ✅ RBAC FastAPI intégré
- ✅ Audit trail complet
- ✅ Tests intégration Control ↔ Data Plane

---

### **📅 SPRINT 4 - OBSERVABILITÉ AVANCÉE & PERF (Semaine +3)**

#### **🎯 OBJECTIF**
Monitoring production-grade + Optimisations performance

#### **📦 LIVRABLES MAJEURS**
- **Tracing OpenTelemetry** : Traces distribuées complètes
- **Prometheus counters** : TTL, cache hits, p95
- **ThreadPool auto-tuned** : CPU × 2 avec adaptation charge
- **Compression .json.zst** : Réduction mémoire 5-10×

#### **📊 OBSERVABILITÉ OPENTELEMETRY**

```python
# orchestrator/app/monitoring/tracing.py
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configuration tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrumentation Agent Factory
class TracedAgentFactory(AgentFactory):
    
    @tracer.start_as_current_span("agent_creation")
    async def create_agent(self, template_name: str, **kwargs):
        span = trace.get_current_span()
        span.set_attribute("template.name", template_name)
        span.set_attribute("template.version", await self._get_template_version(template_name))
        
        start_time = time.time()
        try:
            agent = await super().create_agent(template_name, **kwargs)
            span.set_attribute("creation.success", True)
            return agent
        except Exception as e:
            span.set_attribute("creation.success", False)
            span.set_attribute("error.message", str(e))
            raise
        finally:
            creation_time = time.time() - start_time
            span.set_attribute("creation.duration_ms", creation_time * 1000)
            AGENT_CREATION_TIME.observe(creation_time)
```

#### **⚡ OPTIMISATIONS PERFORMANCE**

```python
# orchestrator/app/optimization/adaptive_threading.py
import psutil
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

class AdaptiveThreadPool:
    """ThreadPool auto-adaptatif selon charge CPU"""
    
    def __init__(self):
        self.base_workers = psutil.cpu_count() * 2
        self.current_workers = self.base_workers
        self.executor = ThreadPoolExecutor(max_workers=self.current_workers)
        self.adjustment_lock = Lock()
        
    def adapt_to_load(self):
        """Adaptation dynamique selon charge système"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        
        with self.adjustment_lock:
            if cpu_percent > 80 and self.current_workers > self.base_workers // 2:
                # Réduction charge CPU élevée
                self.current_workers = max(self.current_workers - 2, self.base_workers // 2)
                self._resize_executor()
            elif cpu_percent < 50 and memory_percent < 70:
                # Augmentation si ressources disponibles
                self.current_workers = min(self.current_workers + 1, self.base_workers * 2)
                self._resize_executor()
                
    def _resize_executor(self):
        """Redimensionnement ThreadPool"""
        old_executor = self.executor
        self.executor = ThreadPoolExecutor(max_workers=self.current_workers)
        old_executor.shutdown(wait=False)
        logger.info(f"ThreadPool redimensionné: {self.current_workers} workers")

# orchestrator/app/optimization/compression.py
import zstandard as zstd
import json

class TemplateCompression:
    """Compression templates JSON avec Zstandard"""
    
    def __init__(self):
        self.compressor = zstd.ZstdCompressor(level=3)
        self.decompressor = zstd.ZstdDecompressor()
        
    def compress_template(self, template_data: Dict) -> bytes:
        """Compression template JSON"""
        json_bytes = json.dumps(template_data, separators=(',', ':')).encode('utf-8')
        compressed = self.compressor.compress(json_bytes)
        
        compression_ratio = len(compressed) / len(json_bytes)
        logger.debug(f"Compression ratio: {compression_ratio:.2%}")
        
        return compressed
        
    def decompress_template(self, compressed_data: bytes) -> Dict:
        """Décompression template"""
        json_bytes = self.decompressor.decompress(compressed_data)
        return json.loads(json_bytes.decode('utf-8'))
```

#### **✅ DEFINITION OF DONE SPRINT 4**
- ✅ Tracing OpenTelemetry opérationnel
- ✅ Métriques Prometheus complètes (p95, cache, TTL)
- ✅ ThreadPool adaptatif selon charge
- ✅ Compression templates active (gain mémoire mesuré)
- ✅ Performance < 50ms/agent validée

---

### **📅 SPRINT 5 - RELEASE CANDIDATE (Semaine +4)**

#### **🎯 OBJECTIF**
Déploiement production avec validation chaos engineering

#### **📦 LIVRABLES MAJEURS**
- **K8s blue-green deploy** : Helm chart production-ready
- **Chaos test** : 25% nodes off + validation résilience
- **Doc "Operator runbook"** : Procédures opérationnelles

#### **🚀 DÉPLOIEMENT KUBERNETES**

```yaml
# helm/agent-factory/values.yaml
replicaCount: 3

image:
  repository: nextgeneration/agent-factory
  tag: "1.0.0-rc1"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 8000

ingress:
  enabled: true
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: agent-factory.nextgen.local
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 2000m
    memory: 4Gi
  requests:
    cpu: 1000m
    memory: 2Gi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

monitoring:
  serviceMonitor:
    enabled: true
    interval: 30s
    path: /metrics
```

#### **💥 CHAOS ENGINEERING**

```python
# tests/chaos/chaos_test.py
import pytest
import kubernetes
import time
import requests

class ChaosTestSuite:
    """Tests résilience avec Chaos Engineering"""
    
    def __init__(self):
        self.k8s_client = kubernetes.client.ApiClient()
        self.base_url = "http://agent-factory.nextgen.local"
        
    @pytest.mark.chaos
    def test_node_failure_resilience(self):
        """Test résilience avec 25% nodes arrêtés"""
        
        # 1. Baseline performance
        baseline_latency = self._measure_average_latency()
        
        # 2. Arrêt 25% des nodes
        nodes_to_stop = self._get_worker_nodes()[:len(self._get_worker_nodes()) // 4]
        
        for node in nodes_to_stop:
            self._cordon_and_drain_node(node)
            
        time.sleep(30)  # Stabilisation
        
        # 3. Validation service toujours opérationnel
        chaos_latency = self._measure_average_latency()
        
        # 4. Assertions
        assert chaos_latency < baseline_latency * 2  # Dégradation < 100%
        assert self._check_service_health()
        
        # 5. Restauration
        for node in nodes_to_stop:
            self._uncordon_node(node)
            
    def _measure_average_latency(self, samples=100) -> float:
        """Mesure latence moyenne création agents"""
        latencies = []
        
        for _ in range(samples):
            start = time.time()
            response = requests.post(f"{self.base_url}/factory/agents",
                                   json={"template_name": "documentaliste"})
            latency = time.time() - start
            
            assert response.status_code == 200
            latencies.append(latency)
            
        return sum(latencies) / len(latencies)
```

#### **📚 OPERATOR RUNBOOK**

```markdown
# Agent Factory - Operator Runbook

## 🚨 Alertes Critiques

### Template Signature Failures > 10/min
**Symptôme**: Métriques `template_signature_failures_total` élevées
**Action**: 
1. Vérifier rotation clés Vault
2. Analyser logs sécurité
3. Déclencher rotation manuelle si nécessaire

### Cache Hit Rate < 80%
**Symptôme**: Performance dégradée, latence élevée
**Action**:
1. Vérifier TTL configuration
2. Analyser patterns d'accès templates
3. Ajuster cache_ttl si nécessaire

### Pod Memory > 90%
**Symptôme**: Risque OOMKilled
**Action**:
1. Vérifier compression templates active
2. Analyser fuites mémoire potentielles
3. Scale horizontal si nécessaire

## 🔧 Procédures Maintenance

### Rotation Clés Signature
```bash
# 1. Génération nouvelle paire
openssl genrsa -out private_new.pem 2048
openssl rsa -in private_new.pem -pubout -out public_new.pem

# 2. Upload Vault
vault kv put agent-factory/signing-keys public_key=@public_new.pem

# 3. Rolling restart
kubectl rollout restart deployment/agent-factory
```

### Mise à jour Templates
```bash
# 1. Signature nouveau template
python scripts/sign_template.py new_template.json

# 2. Déploiement
kubectl create configmap agent-templates --from-file=templates/ --dry-run=client -o yaml | kubectl apply -f -

# 3. Hot-reload automatique (watchdog)
```
```

#### **✅ DEFINITION OF DONE SPRINT 5**
- ✅ Déploiement K8s blue-green fonctionnel
- ✅ Chaos test 25% nodes passant
- ✅ Runbook opérateur complet
- ✅ Monitoring production opérationnel
- ✅ SLA < 100ms p95 respecté en production

---

## 🎯 **BACKLOG NEXT QUARTER**
*Innovations futures hors périmètre MVP*

### **📈 ROADMAP LONG TERME**
- **Agent Marketplace** : Écosystème partage agents (Claude)
- **Interface NLP** : Création agents langage naturel
- **GNN Recommender** : Recommandations agents intelligentes
- **Multi-modal Agents** : Support images/audio/documents (Gemini)

---

## 🔑 **TÂCHES TRANSVERSES**

### **📊 QUALITÉ DE CODE**
- **mypy --strict** : Fail-fast dès Sprint 0
- **ruff** : Linting automatique
- **Coverage** : > 90% tests unitaires + intégration

### **🔒 SUPPLY CHAIN SECURITY**
- **pip-audit** : Scan vulnérabilités intégré CI
- **Trivy** : Scan containers + dépendances
- **SBOM** : Software Bill of Materials généré

### **⚠️ RISQUES & MITIGATIONS**

| Risque | Mitigation | Sprint |
|--------|------------|---------|
| Hot-reload CPU intensif | TTL adaptatif + debounce watchdog | 1 |
| Clé RSA compromise | Rotation Vault + alertes Prometheus | 2 |
| Sandbox overhead > 20% | Benchmark WASI vs Native, activation conditionnelle | 3 |
| Latence production > SLA | Auto-scaling + ThreadPool adaptatif | 4 |

---

## 📉 **ÉCONOMIE TEMPS OBTENUE**

| Étape | Plan Original | Plan Révisé | Gain |
|-------|---------------|-------------|------|
| **Bases fusionnées** | 2 jours | 1 jour | -50% |
| **Sécurité disponible** | Semaine +2 | Semaine +1 | -1 semaine |
| **Production ready** | Semaine +2 post-Phase 4 | Semaine +4 (complet) | +monitoring |

**Gain net : ~20% délai global sans supprimer aucune exigence business**

---

## 🚦 **PROCHAINES ACTIONS IMMÉDIATES**

### **✅ VALIDATION JALONNEMENT**
- Daily team 15min pour validation nouveau planning
- Création branche `roadmap/v2-optimized`
- Issue Sprint 0 avec checklist détaillée

### **🚀 SPRINT 0 KICKOFF**
**Checklist Sprint 0 :**
- [ ] Merge code Claude (AgentTemplate + TemplateManager)
- [ ] Config Pydantic unifiée
- [ ] CI smoke tests + lint (GitHub Actions)
- [ ] Validation imports + tests basiques
- [ ] Documentation Sprint 1 préparée

**Une fois Sprint 0 terminé (J+2) :**
- Revue pipeline CI + rapport Locust
- Validation métriques baseline
- Lancement Sprint 1

---

**🎯 Plan d'action révisé intégrant shift-left security, optimisations temporelles et suppression des redondances pour livraison production-ready Semaine +4** 