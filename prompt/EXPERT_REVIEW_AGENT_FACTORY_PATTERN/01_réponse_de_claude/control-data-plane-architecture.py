# === Control Plane (Gouvernance) ===

from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, JSON, DateTime, Integer, Boolean
import asyncio
from datetime import datetime
import hashlib
import subprocess
from pydantic import BaseModel

Base = declarative_base()

# === Modèles ORM ===

class TemplateORM(Base):
    """Template versionné avec migration"""
    __tablename__ = "templates"
    
    id = Column(String, primary_key=True)
    name = Column(String, index=True)
    version = Column(String)
    content = Column(JSON)
    checksum = Column(String)
    signature = Column(String)  # Cosign signature
    migrations = Column(JSON)  # ["v1->v2.py", "v2->v3.py"]
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class AgentRegistryORM(Base):
    """Registre des agents avec métadonnées"""
    __tablename__ = "agent_registry"
    
    agent_id = Column(String, primary_key=True)
    template_id = Column(String)
    template_version = Column(String)
    deployment_status = Column(String)  # pending, running, failed
    node_assignment = Column(String)  # data-plane node
    resource_allocation = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_health_check = Column(DateTime)

# === Control Plane API ===

class ControlPlaneAPI:
    """API de gouvernance - séparée de l'exécution"""
    
    def __init__(self, db_url: str, s3_bucket: str):
        self.engine = create_async_engine(db_url, pool_pre_ping=True)
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        self.s3_bucket = s3_bucket
        self.app = FastAPI(title="Agent Factory Control Plane")
        self._setup_routes()
    
    def _setup_routes(self):
        """Configure les routes FastAPI"""
        
        @self.app.post("/templates/{name}/versions")
        async def upload_template(
            name: str,
            template: Dict[str, Any],
            db: AsyncSession = Depends(self.get_db)
        ):
            """Upload et valide un nouveau template"""
            # Validation avec OPA
            if not await self._validate_with_opa(template):
                raise HTTPException(400, "Template rejected by OPA policy")
            
            # Génération version et checksum
            version = self._generate_version(name, template)
            checksum = hashlib.sha256(str(template).encode()).hexdigest()
            
            # Signature Cosign
            signature = await self._sign_with_cosign(template, checksum)
            
            # Stockage S3 pour les artefacts
            s3_key = f"templates/{name}/{version}/template.json"
            await self._upload_to_s3(s3_key, template)
            
            # Enregistrement DB
            template_orm = TemplateORM(
                id=f"{name}:{version}",
                name=name,
                version=version,
                content=template,
                checksum=checksum,
                signature=signature,
                migrations=template.get("migrations", [])
            )
            
            db.add(template_orm)
            await db.commit()
            
            return {"id": template_orm.id, "version": version, "checksum": checksum}
        
        @self.app.post("/agents/create")
        async def create_agent(
            template_name: str,
            template_version: Optional[str] = None,
            config: Dict[str, Any] = None,
            db: AsyncSession = Depends(self.get_db)
        ):
            """Crée un agent - délègue l'exécution au data plane"""
            # Résolution de version
            if not template_version:
                template_version = await self._get_latest_version(template_name, db)
            
            # Chargement du template
            template = await self._load_template(template_name, template_version, db)
            
            # Application des migrations si nécessaire
            current_version = await self._get_current_version(template_name)
            if current_version and current_version != template_version:
                template = await self._migrate_template(
                    template, current_version, template_version
                )
            
            # Allocation de ressources
            node = await self._select_data_plane_node(template)
            resources = self._calculate_resources(template, config)
            
            # Enregistrement
            agent_orm = AgentRegistryORM(
                agent_id=str(uuid.uuid4()),
                template_id=f"{template_name}:{template_version}",
                template_version=template_version,
                deployment_status="pending",
                node_assignment=node,
                resource_allocation=resources
            )
            
            db.add(agent_orm)
            await db.commit()
            
            # Déploiement asynchrone sur data plane
            asyncio.create_task(
                self._deploy_to_data_plane(agent_orm, template, config)
            )
            
            return {"agent_id": agent_orm.agent_id, "status": "creating"}
    
    async def _validate_with_opa(self, template: Dict[str, Any]) -> bool:
        """Validation OPA du template"""
        # Appel à OPA Gatekeeper
        policy_input = {
            "template": template,
            "user": "current_user",  # From auth context
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # En production : vraie intégration OPA
        # response = await opa_client.evaluate("agent_factory.template.allow", policy_input)
        # return response.result
        
        # Validation basique pour l'exemple
        required_fields = ["name", "role", "domain", "capabilities"]
        return all(field in template for field in required_fields)
    
    async def _sign_with_cosign(self, template: Dict[str, Any], checksum: str) -> str:
        """Signe le template avec Cosign"""
        # En production : vraie signature Cosign
        # subprocess.run(["cosign", "sign", "--key", "cosign.key", ...])
        return f"cosign-signature-{checksum[:8]}"
    
    async def _deploy_to_data_plane(
        self,
        agent_orm: AgentRegistryORM,
        template: Dict[str, Any],
        config: Dict[str, Any]
    ):
        """Déploie l'agent sur le data plane sélectionné"""
        # Appel gRPC ou HTTP vers le data plane node
        data_plane_client = DataPlaneClient(agent_orm.node_assignment)
        
        try:
            await data_plane_client.deploy_agent(
                agent_id=agent_orm.agent_id,
                template=template,
                config=config,
                resources=agent_orm.resource_allocation
            )
            
            # Mise à jour du statut
            async with self.async_session() as db:
                agent_orm.deployment_status = "running"
                db.add(agent_orm)
                await db.commit()
                
        except Exception as e:
            async with self.async_session() as db:
                agent_orm.deployment_status = "failed"
                db.add(agent_orm)
                await db.commit()
            raise
    
    async def get_db(self) -> AsyncSession:
        """Dependency pour les sessions DB"""
        async with self.async_session() as session:
            yield session

# === Data Plane (Exécution) ===

from ray import serve
import ray
from typing import Any, Dict

@serve.deployment(
    num_replicas="auto",
    autoscaling_config={
        "min_replicas": 1,
        "max_replicas": 100,
        "target_num_ongoing_requests_per_replica": 10
    },
    ray_actor_options={
        "num_cpus": 2,
        "num_gpus": 0  # Overridé selon le template
    }
)
class DataPlaneAgent:
    """Agent exécuté sur le data plane avec Ray Serve"""
    
    def __init__(self, agent_id: str, template: Dict[str, Any], config: Dict[str, Any]):
        self.agent_id = agent_id
        self.template = template
        self.config = config
        self.processor = self._create_processor()
        
    def _create_processor(self):
        """Crée le processeur selon le template"""
        # Injection des capacités selon le template
        capabilities = self.template.get("capabilities", [])
        
        if "gpu_inference" in capabilities:
            return GPUProcessor(self.template)
        elif "cpu_optimized" in capabilities:
            return CPUProcessor(self.template)
        else:
            return DefaultProcessor(self.template)
    
    async def __call__(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Point d'entrée Ray Serve"""
        # Métriques
        start_time = time.time()
        
        try:
            result = await self.processor.process(
                request.get("data"),
                request.get("context", {})
            )
            
            # Métriques de succès
            await self._record_metrics({
                "agent_id": self.agent_id,
                "duration": time.time() - start_time,
                "success": True
            })
            
            return result
            
        except Exception as e:
            # Métriques d'échec
            await self._record_metrics({
                "agent_id": self.agent_id,
                "duration": time.time() - start_time,
                "success": False,
                "error": str(e)
            })
            raise
    
    async def _record_metrics(self, metrics: Dict[str, Any]):
        """Enregistre les métriques dans Prometheus"""
        # ray.util.metrics.Counter, Gauge, etc.
        pass

class DataPlaneOrchestrator:
    """Orchestrateur local du data plane"""
    
    def __init__(self, node_id: str, control_plane_url: str):
        self.node_id = node_id
        self.control_plane_url = control_plane_url
        self.deployed_agents: Dict[str, serve.Deployment] = {}
        
        # Initialisation Ray
        ray.init(
            runtime_env={
                "pip": ["langchain", "numpy", "scikit-learn"],
                "env_vars": {"NODE_ID": node_id}
            }
        )
        serve.start()
    
    async def deploy_agent(
        self,
        agent_id: str,
        template: Dict[str, Any],
        config: Dict[str, Any],
        resources: Dict[str, Any]
    ):
        """Déploie un agent avec les ressources allouées"""
        
        # Configuration Ray selon les ressources
        ray_options = {
            "num_cpus": resources.get("cpu", 2),
            "num_gpus": resources.get("gpu", 0),
            "memory": resources.get("memory_mb", 2048) * 1024 * 1024
        }
        
        # Création du deployment Ray Serve
        deployment = DataPlaneAgent.options(
            name=f"agent-{agent_id}",
            ray_actor_options=ray_options
        ).bind(agent_id, template, config)
        
        # Déploiement
        handle = serve.run(deployment, route_prefix=f"/agents/{agent_id}")
        self.deployed_agents[agent_id] = handle
        
        # Notification au control plane
        await self._notify_control_plane(agent_id, "running")
    
    async def health_check_loop(self):
        """Boucle de health check des agents"""
        while True:
            for agent_id, handle in self.deployed_agents.items():
                try:
                    # Test simple
                    result = await handle.remote({"health": "check"})
                    await self._notify_control_plane(agent_id, "healthy")
                except Exception as e:
                    await self._notify_control_plane(agent_id, "unhealthy", str(e))
            
            await asyncio.sleep(30)
    
    async def _notify_control_plane(
        self,
        agent_id: str,
        status: str,
        error: Optional[str] = None
    ):
        """Notifie le control plane du statut"""
        # HTTP ou gRPC vers control plane
        pass

# === GPU/CPU Tiering ===

class ResourceTieringManager:
    """Gestionnaire de tiering GPU/CPU"""
    
    def __init__(self):
        self.gpu_nodes = []  # Nodes avec GPU
        self.cpu_nodes = []  # Nodes CPU only
        self.gpu_utilization = {}  # Monitoring GPU
    
    async def select_node_for_template(
        self,
        template: Dict[str, Any]
    ) -> str:
        """Sélectionne le meilleur node selon le template"""
        requires_gpu = template.get("requires_gpu", False)
        
        if requires_gpu:
            # Chercher un GPU disponible
            for node in self.gpu_nodes:
                utilization = self.gpu_utilization.get(node, 0)
                if utilization < 70:  # Seuil configurable
                    return node
            
            # Fallback sur CPU avec modèle distillé
            print(f"GPU saturé, fallback sur CPU pour {template['name']}")
            template["model_override"] = "distilled-cpu-model"
            return self._select_cpu_node()
        
        return self._select_cpu_node()
    
    def _select_cpu_node(self) -> str:
        """Sélectionne un node CPU avec le moins de charge"""
        # Round-robin simple, ou intégration avec Kubernetes metrics
        return self.cpu_nodes[0] if self.cpu_nodes else "default-node"

# === Migration de Templates ===

class TemplateMigrationEngine:
    """Moteur de migration pour les templates"""
    
    async def migrate(
        self,
        template: Dict[str, Any],
        from_version: str,
        to_version: str,
        migrations: List[str]
    ) -> Dict[str, Any]:
        """Applique les migrations entre versions"""
        current_template = template.copy()
        
        # Trouver le chemin de migration
        migration_path = self._find_migration_path(
            from_version, to_version, migrations
        )
        
        # Appliquer chaque migration
        for migration_file in migration_path:
            migration_func = await self._load_migration(migration_file)
            current_template = await migration_func(current_template)
        
        return current_template
    
    def _find_migration_path(
        self,
        from_v: str,
        to_v: str,
        available: List[str]
    ) -> List[str]:
        """Trouve le chemin de migration optimal"""
        # Exemple : ["v1->v2.py", "v2->v3.py"] pour v1 vers v3
        path = []
        current = from_v
        
        while current != to_v:
            for migration in available:
                if migration.startswith(f"{current}->"):
                    path.append(migration)
                    current = migration.split("->")[1].replace(".py", "")
                    break
            else:
                raise ValueError(f"No migration path from {from_v} to {to_v}")
        
        return path

# === Exemple d'utilisation ===

async def main():
    """Exemple de déploiement control/data plane"""
    
    # Control Plane (sur node dédié)
    control_plane = ControlPlaneAPI(
        db_url="postgresql+asyncpg://user:pass@localhost/control_plane",
        s3_bucket="agent-factory-templates"
    )
    
    # Data Plane (sur nodes de calcul)
    data_plane = DataPlaneOrchestrator(
        node_id="data-plane-gpu-01",
        control_plane_url="http://control-plane:8000"
    )
    
    # Démarrage des services
    asyncio.create_task(data_plane.health_check_loop())
    
    # Création d'un agent via control plane
    response = await control_plane.app.post(
        "/agents/create",
        json={
            "template_name": "llm_processor",
            "config": {"model": "gpt-4", "requires_gpu": True}
        }
    )
    
    print(f"Agent created: {response}")

if __name__ == "__main__":
    asyncio.run(main())