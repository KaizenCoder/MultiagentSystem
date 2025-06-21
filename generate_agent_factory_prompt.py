"""
Gnrateur automatique du prompt complet pour l'implmentation du Agent Factory Pattern
Inspir du generate_pitch_document.py de NextGeneration
"""

import os

def generate_agent_factory_code():
    """Gnre le code obligatoire pour l'Agent Factory"""
    
    agent_factory_code = '''
### **1.4 CODE OBLIGATOIRE : Agent Factory Principal**

**Fichier** : `nextgeneration/orchestrator/app/agents/agent_factory.py`

```python
"""
NextGeneration Agent Factory - Gnrateur automatique d'agents
OBLIGATOIRE : Ce factory est le cur du systme de gnration d'agents
"""

from typing import Dict, List, Any, Optional, Type
from logging_manager_optimized import LoggingManager
import importlib
import inspect
from pathlib import Path

from .base_agent import BaseAgent, AgentMetadata
from .agent_templates import TemplateManager, AgentTemplate

# LoggingManager NextGeneration - Agent
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_agent_logger(
            agent_name="AgentFactory",
            role="ai_processor",
            domain="general",
            async_enabled=True
        )

class AgentFactory:
    """
    Factory pour la cration automatique d'agents NextGeneration
    OBLIGATOIRE : Utilis pour gnrer tous les nouveaux agents
    """
    
    def __init__(self, template_manager: TemplateManager = None):
        self.template_manager = template_manager or TemplateManager()
        self.registered_agents: Dict[str, BaseAgent] = {}
        self.agent_classes: Dict[str, Type[BaseAgent]] = {}
        self._load_existing_agents()
    
    def _load_existing_agents(self):
        """Charge les agents existants du projet NextGeneration"""
        try:
            # Importer les agents existants depuis l'architecture actuelle
            # OBLIGATOIRE : Adapter ces imports selon votre structure exacte
            
            agents_module_path = Path(__file__).parent.parent
            logger.info(f"Loading existing agents from: {agents_module_path}")
            
            # Ici, vous devez adapter selon vos agents existants
            # Exemple pour l'architecture NextGeneration :
            
            # from ..supervisor import agent_documentaliste, agent_genie_logiciel, agent_hardware
            
            # self.registered_agents.update({
            #     "documentaliste": agent_documentaliste,
            #     "genie_logiciel": agent_genie_logiciel,
            #     "hardware": agent_hardware
            # })
            
            logger.info(f"Loaded {len(self.registered_agents)} existing agents")
            
        except Exception as e:
            logger.warning(f"Could not load existing agents: {e}")
    
    async def create_agent(
        self,
        template_name: str,
        custom_config: Dict[str, Any] = None,
        name_suffix: str = ""
    ) -> Optional[BaseAgent]:
        """
        Cre un agent  partir d'un template
        OBLIGATOIRE : Mthode principale de cration d'agents
        
        Args:
            template_name: Nom du template  utiliser
            custom_config: Configuration personnalise
            name_suffix: Suffixe pour le nom de l'agent
            
        Returns:
            BaseAgent: Instance de l'agent cr
        """
        
        template = self.template_manager.load_template(template_name)
        if not template:
            logger.error(f"Template not found: {template_name}")
            return None
        
        try:
            # Gnrer le nom unique de l'agent
            agent_name = f"{template.name}{name_suffix}" if name_suffix else template.name
            
            # Fusionner la configuration
            final_config = template.default_config.copy()
            if custom_config:
                final_config.update(custom_config)
            
            # Crer l'agent dynamiquement
            agent = await self._instantiate_agent(template, agent_name, final_config)
            
            if agent:
                # Enregistrer l'agent
                self.registered_agents[agent_name] = agent
                logger.info(f"Created agent: {agent_name} from template {template_name}")
                
                return agent
            
        except Exception as e:
            logger.error(f"Error creating agent from template {template_name}: {e}")
            return None
    
    async def _instantiate_agent(
        self,
        template: AgentTemplate,
        agent_name: str,
        config: Dict[str, Any]
    ) -> Optional[BaseAgent]:
        """
        Instancie un agent  partir d'un template
        OBLIGATOIRE : Logique de cration dynamique
        """
        
        # Crer la classe d'agent dynamiquement
        class DynamicAgent(BaseAgent):
            """Agent gnr dynamiquement par l'AgentFactory"""
            
            def __init__(self, name: str, template: AgentTemplate, config: Dict[str, Any]):
                super().__init__(
                    name=name,
                    role=template.role,
                    domain=template.domain,
                    tools=template.tools.copy(),
                    capabilities=template.capabilities.copy(),
                    config=config
                )
                self.template = template
            
            async def process(self, input_data: Any, context: Dict[str, Any] = None) -> Dict[str, Any]:
                """Traitement gnrique bas sur le template"""
                await self.pre_process(input_data, context)
                
                # Logique de traitement base sur le rle
                result = await self._role_based_processing(input_data, context or {})
                
                return await self.post_process(result)
            
            async def _role_based_processing(self, input_data: Any, context: Dict[str, Any]) -> Dict[str, Any]:
                """Traitement spcialis selon le rle"""
                
                if self.template.role == "analyzer":
                    return await self._analyze_data(input_data, context)
                elif self.template.role == "engineer":
                    return await self._engineer_solution(input_data, context)
                elif self.template.role == "specialist":
                    return await self._specialist_analysis(input_data, context)
                else:
                    return await self._generic_processing(input_data, context)
            
            async def _analyze_data(self, input_data: Any, context: Dict[str, Any]) -> Dict[str, Any]:
                """Traitement pour les agents analystes"""
                return {
                    "agent": self.metadata.name,
                    "role": "analyzer",
                    "analysis": f"Analyse effectue sur les donnes d'entre",
                    "capabilities_used": self.metadata.capabilities,
                    "tools_used": self.metadata.tools,
                    "input_summary": str(input_data)[:200] if input_data else "No input",
                    "context": context,
                    "recommendations": []
                }
            
            async def _engineer_solution(self, input_data: Any, context: Dict[str, Any]) -> Dict[str, Any]:
                """Traitement pour les agents ingnieurs"""
                return {
                    "agent": self.metadata.name,
                    "role": "engineer",
                    "solution": f"Solution technique propose",
                    "capabilities_used": self.metadata.capabilities,
                    "tools_used": self.metadata.tools,
                    "technical_analysis": str(input_data)[:200] if input_data else "No input",
                    "context": context,
                    "implementation_steps": []
                }
            
            async def _specialist_analysis(self, input_data: Any, context: Dict[str, Any]) -> Dict[str, Any]:
                """Traitement pour les agents spcialistes"""
                return {
                    "agent": self.metadata.name,
                    "role": "specialist",
                    "specialist_report": f"Rapport spcialis en {self.metadata.domain}",
                    "capabilities_used": self.metadata.capabilities,
                    "tools_used": self.metadata.tools,
                    "domain_analysis": str(input_data)[:200] if input_data else "No input",
                    "context": context,
                    "expert_recommendations": []
                }
            
            async def _generic_processing(self, input_data: Any, context: Dict[str, Any]) -> Dict[str, Any]:
                """Traitement gnrique"""
                return {
                    "agent": self.metadata.name,
                    "role": self.template.role,
                    "processing_result": f"Traitement effectu",
                    "capabilities_used": self.metadata.capabilities,
                    "tools_used": self.metadata.tools,
                    "input_data": str(input_data)[:200] if input_data else "No input",
                    "context": context
                }
            
            def get_capabilities(self) -> List[str]:
                """Retourne les capacits dfinies dans le template"""
                return self.metadata.capabilities.copy()
        
        # Instancier l'agent
        agent = DynamicAgent(agent_name, template, config)
        return agent
    
    async def bulk_create_agents(
        self,
        agent_specs: List[Dict[str, Any]]
    ) -> Dict[str, BaseAgent]:
        """
        Cration en lot d'agents
        OBLIGATOIRE : Pour crer plusieurs agents simultanment
        
        Args:
            agent_specs: Liste des spcifications d'agents
                Format: [{"template": "nom", "config": {}, "suffix": ""}]
        
        Returns:
            Dict[str, BaseAgent]: Dictionnaire des agents crs
        """
        created_agents = {}
        
        for spec in agent_specs:
            template_name = spec.get("template")
            custom_config = spec.get("config", {})
            name_suffix = spec.get("suffix", "")
            
            if not template_name:
                logger.warning("Agent spec missing template name, skipping")
                continue
            
            agent = await self.create_agent(template_name, custom_config, name_suffix)
            if agent:
                created_agents[agent.metadata.name] = agent
        
        logger.info(f"Bulk created {len(created_agents)} agents")
        return created_agents
    
    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """Rcupre un agent par son nom"""
        return self.registered_agents.get(agent_name)
    
    def list_agents(self) -> List[str]:
        """Liste tous les agents enregistrs"""
        return list(self.registered_agents.keys())
    
    def list_templates(self) -> List[str]:
        """Liste tous les templates disponibles"""
        return self.template_manager.list_templates()
    
    def remove_agent(self, agent_name: str) -> bool:
        """Supprime un agent"""
        if agent_name in self.registered_agents:
            del self.registered_agents[agent_name]
            logger.info(f"Removed agent: {agent_name}")
            return True
        return False
    
    def get_factory_stats(self) -> Dict[str, Any]:
        """Statistiques du factory"""
        return {
            "total_agents": len(self.registered_agents),
            "available_templates": len(self.template_manager.list_templates()),
            "registered_agents": list(self.registered_agents.keys()),
            "available_templates_list": self.template_manager.list_templates()
        }

# Instance globale du factory (OBLIGATOIRE)
agent_factory = AgentFactory()
```'''
    
    return agent_factory_code

def generate_configuration_code():
    """Gnre le code de configuration"""
    
    config_code = '''
### **1.5 CODE OBLIGATOIRE : Configuration**

**Fichier** : `nextgeneration/orchestrator/app/config/agent_config.py`

```python
"""
Configuration pour le systme Agent Factory
OBLIGATOIRE : Extension de la configuration NextGeneration existante
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseSettings, Field
import os

class AgentFactoryConfig(BaseSettings):
    """
    Configuration pour l'Agent Factory Pattern
    OBLIGATOIRE :  intgrer avec la configuration existante
    """
    
    # Configuration Factory
    AGENT_FACTORY_ENABLED: bool = Field(True, description="Active le systme Agent Factory")
    AUTO_AGENT_DISCOVERY: bool = Field(True, description="Dcouverte automatique des agents")
    
    # Chemins
    AGENT_TEMPLATES_PATH: str = Field("orchestrator/app/agents/templates", description="Rpertoire des templates")
    AGENT_LOGS_PATH: str = Field("logs/agents", description="Rpertoire des logs d'agents")
    
    # Limites
    MAX_AGENTS_PER_DOMAIN: int = Field(10, description="Nombre maximum d'agents par domaine")
    MAX_CONCURRENT_AGENTS: int = Field(5, description="Nombre maximum d'agents concurrent")
    AGENT_TIMEOUT_SECONDS: int = Field(300, description="Timeout par dfaut pour les agents")
    
    # Cache
    ENABLE_TEMPLATE_CACHE: bool = Field(True, description="Cache des templates")
    CACHE_TTL_SECONDS: int = Field(3600, description="Dure de vie du cache")
    
    # Monitoring
    ENABLE_AGENT_METRICS: bool = Field(True, description="Mtriques des agents")
    METRICS_COLLECTION_INTERVAL: int = Field(60, description="Intervalle de collecte des mtriques")
    
    # Scurit
    AGENT_SANDBOX_MODE: bool = Field(False, description="Mode sandbox pour les agents")
    ALLOWED_DOMAINS: List[str] = Field(
        ["documentation", "software_engineering", "hardware_analysis", "security", "testing"],
        description="Domaines autoriss pour les agents"
    )
    
    # Intgration avec supervisor existant
    SUPERVISOR_INTEGRATION_ENABLED: bool = Field(True, description="Intgration avec le supervisor")
    AUTO_REGISTER_WITH_SUPERVISOR: bool = Field(True, description="Enregistrement automatique avec supervisor")
    
    # Templates par dfaut
    DEFAULT_AGENT_TEMPLATES: Dict[str, Dict[str, Any]] = Field(
        default={
            "documentaliste": {
                "priority": "high",
                "auto_load": True
            },
            "genie_logiciel": {
                "priority": "high", 
                "auto_load": True
            },
            "hardware": {
                "priority": "medium",
                "auto_load": True
            }
        },
        description="Configuration des templates par dfaut"
    )
    
    class Config:
        env_prefix = "AGENT_FACTORY_"
        case_sensitive = True

# Instance globale de configuration
agent_factory_config = AgentFactoryConfig()
```'''
    
    return config_code

def generate_init_files():
    """Gnre les fichiers __init__.py ncessaires"""
    
    init_code = '''
### **1.6 CODE OBLIGATOIRE : Fichiers d'initialisation**

**Fichier** : `nextgeneration/orchestrator/app/agents/__init__.py`

```python
"""
Module agents pour NextGeneration
OBLIGATOIRE : Expose les composants principaux du systme Agent Factory
"""

from .base_agent import BaseAgent, AgentStatus, AgentMetadata
from .agent_factory import AgentFactory, agent_factory
from .agent_templates import AgentTemplate, TemplateManager

__all__ = [
    "BaseAgent",
    "AgentStatus", 
    "AgentMetadata",
    "AgentFactory",
    "agent_factory",
    "AgentTemplate",
    "TemplateManager"
]
```

**Fichier** : `nextgeneration/orchestrator/app/agents/templates/__init__.py`

```python
"""
Templates d'agents pour NextGeneration
OBLIGATOIRE : Module pour les templates JSON
"""

# Ce module contient les templates JSON pour la gnration d'agents
```'''
    
    return init_code

def generate_json_templates():
    """Gnre les templates JSON"""
    
    json_templates = '''
### **1.7 CODE OBLIGATOIRE : Templates JSON**

**Fichier** : `nextgeneration/orchestrator/app/agents/templates/documentaliste.json`

```json
{
    "name": "documentaliste",
    "role": "analyzer",
    "domain": "documentation",
    "base_class": "DocumentalisteAgent",
    "capabilities": [
        "document_analysis",
        "text_extraction",
        "summary_generation",
        "classification",
        "metadata_extraction"
    ],
    "tools": [
        "file_reader",
        "text_processor",
        "classifier",
        "summarizer"
    ],
    "default_config": {
        "max_file_size": 50000000,
        "supported_formats": [".txt", ".md", ".pdf", ".docx"],
        "summary_length": "medium",
        "classification_threshold": 0.7
    },
    "supervisor_route": "document_analysis",
    "description": "Agent spcialis dans l'analyse et le traitement de documents",
    "dependencies": []
}
```

**Fichier** : `nextgeneration/orchestrator/app/agents/templates/genie_logiciel.json`

```json
{
    "name": "genie_logiciel",
    "role": "engineer",
    "domain": "software_engineering",
    "base_class": "GeniLogicielAgent",
    "capabilities": [
        "code_analysis",
        "architecture_review",
        "bug_detection",
        "performance_optimization",
        "documentation_generation"
    ],
    "tools": [
        "code_analyzer",
        "static_analyzer",
        "performance_profiler",
        "doc_generator"
    ],
    "default_config": {
        "supported_languages": ["python", "javascript", "typescript", "java"],
        "analysis_depth": "deep",
        "performance_threshold": 0.8,
        "documentation_style": "sphinx"
    },
    "supervisor_route": "software_engineering",
    "description": "Agent spcialis en gnie logiciel et analyse de code",
    "dependencies": []
}
```

**Fichier** : `nextgeneration/orchestrator/app/agents/templates/hardware.json`

```json
{
    "name": "hardware",
    "role": "specialist",
    "domain": "hardware_analysis",
    "base_class": "HardwareAgent",
    "capabilities": [
        "system_diagnostics",
        "performance_monitoring",
        "hardware_profiling",
        "compatibility_check",
        "optimization_recommendations"
    ],
    "tools": [
        "psutil",
        "gpu_monitor",
        "disk_analyzer",
        "network_tester"
    ],
    "default_config": {
        "monitoring_interval": 30,
        "performance_baseline": "auto",
        "alert_threshold": 0.9,
        "report_format": "detailed"
    },
    "supervisor_route": "hardware_analysis",
    "description": "Agent spcialis dans l'analyse et le monitoring hardware",
    "dependencies": []
}
```'''
    
    return json_templates

def append_to_prompt_file(content):
    """Ajoute du contenu au fichier prompt existant"""
    prompt_file = "prompt/IMPLEMENTATION_AGENT_FACTORY_PATTERN.md"
    
    with open(prompt_file, 'a', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[CHECK] Contenu ajout au prompt : {len(content)} caractres")

def main():
    """Gnre automatiquement la suite du prompt"""
    print("[ROCKET] Gnration automatique de la suite du prompt Agent Factory Pattern...")
    
    # Gnrer les diffrentes sections
    sections = [
        generate_agent_factory_code(),
        generate_configuration_code(),
        generate_init_files(),
        generate_json_templates()
    ]
    
    # Ajouter chaque section au fichier
    for i, section in enumerate(sections, 1):
        print(f" Ajout de la section {i}/{len(sections)}...")
        append_to_prompt_file(section)
    
    print(" Gnration termine avec succs !")
    print("[DOCUMENT] Fichier complet : nextgeneration/prompt/IMPLEMENTATION_AGENT_FACTORY_PATTERN.md")

if __name__ == "__main__":
    main() 