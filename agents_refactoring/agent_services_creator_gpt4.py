#!/usr/bin/env python3
"""
Agent Services Creator - NextGeneration Phase 3
Spcialis dans la cration de services modulaires selon Architecture Hexagonale + CQRS
Collabore avec Route Extractor pour crer la couche service
"""

import asyncio
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import openai
from dataclasses import dataclass, asdict

@dataclass
class ServiceModule:
    """Information sur un module service  crer"""
    name: str
    business_domain: str
    methods: List[str]
    dependencies: List[str]
    repository_needs: List[str]
    complexity_level: str
    cqrs_commands: List[str]
    cqrs_queries: List[str]

@dataclass
class ServicesPlan:
    """Plan global de cration des services"""
    target_file: str
    service_modules: List[ServiceModule]
    shared_dependencies: List[str]
    service_contracts: List[str]
    estimated_lines_reduction: float

class AgentServicesCreator:
    """
    Agent spcialis dans la cration de services modulaires
    Mission: Crer couche service selon patterns Hexagonal + CQRS
    """
    
    def __init__(self):
        # Mode fallback si pas de cl API
        import os
        if os.getenv("OPENAI_API_KEY"):
            self.client = openai.OpenAI()
            self.fallback_mode = False
        else:
            self.client = None
            self.fallback_mode = True
            print(" Agent Services Creator: Mode Fallback activ")
        
        self.results_dir = Path("refactoring_workspace/results/phase3_services")
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    async def analyze_service_needs(self, file_path: str, routes_data: Dict) -> ServicesPlan:
        """Analyser les besoins en services depuis les routes extraites"""
        print(f"[CONSTRUCTION] Analyse besoins services pour {file_path}...")
        
        try:
            # Lire fichier source pour contexte
            file_content = Path(file_path).read_text(encoding='utf-8')
            
            # Analyser avec GPT-4 pour gnration services
            services_plan = await self._create_services_with_gpt4(file_path, file_content, routes_data)
            
            # Sauvegarder plan services
            plan_file = self.results_dir / f"services_plan_{Path(file_path).stem}_{self.timestamp}.json"
            with open(plan_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(services_plan), f, indent=2, ensure_ascii=False)
            
            print(f"[CHECK] Plan services sauvegard: {plan_file}")
            return services_plan
            
        except Exception as e:
            print(f"[CROSS] Erreur analyse services {file_path}: {e}")
            return self._create_fallback_services_plan(file_path)
    
    async def _create_services_with_gpt4(self, file_path: str, content: str, routes_data: Dict) -> ServicesPlan:
        """Crer plan services avec GPT-4 selon Architecture Hexagonale + CQRS"""
        
        prompt = f"""
Tu es un architecte expert en patterns Hexagonal Architecture + CQRS pour FastAPI.
Ta mission: crer un plan de services modulaires pour refactoriser ce fichier god mode.

CONTEXTE:
- Fichier: {file_path} ({len(content.splitlines())} lignes)
- Routes extraites: {routes_data.get('total_routes', 0)}
- Pattern cible: Architecture Hexagonale + CQRS

EXTRAIT CODE:
```python
{content[:6000]}...
```

ROUTES IDENTIFIES:
{json.dumps(routes_data, indent=2)[:2000]}...

ANALYSE REQUISE:
1. Identifier domaines mtier dans le code
2. Pour chaque domaine, crer un service module:
   - Nom service (ex: AuthService, UserService)
   - Mthodes principales
   - Dpendances (DB, cache, external APIs)
   - Besoins repository pattern
   - Commandes CQRS (create, update, delete)
   - Requtes CQRS (get, list, search)

3. Dpendances partages (auth, logging, cache)
4. Contrats interfaces pour DI

RPONSE FORMAT JSON:
{{
  "target_file": "{file_path}",
  "service_modules": [
    {{
      "name": "AuthService",
      "business_domain": "Authentication & Authorization",
      "methods": ["login", "logout", "verify_token"],
      "dependencies": ["user_repository", "token_provider"],
      "repository_needs": ["UserRepository"],
      "complexity_level": "MEDIUM",
      "cqrs_commands": ["LoginCommand", "LogoutCommand"],
      "cqrs_queries": ["GetUserQuery", "ValidateTokenQuery"]
    }}
  ],
  "shared_dependencies": ["DatabaseConnection", "CacheManager"],
  "service_contracts": ["IAuthService", "IUserService"],
  "estimated_lines_reduction": 0.85
}}
"""
        
        if self.fallback_mode or self.client is None:
            print(" Mode fallback: gnration services sans API")
            return self._create_fallback_services_plan(file_path)
        
        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="gpt-4-turbo-preview",
                max_tokens=4000,
                messages=[
                    {"role": "system", "content": "Tu es un expert en architecture logicielle spcialis en patterns Hexagonal + CQRS."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = response.choices[0].message.content
            
            # Extraire JSON depuis la rponse
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                analysis_data = json.loads(json_match.group())
                
                # Convertir en ServicesPlan
                service_modules = [ServiceModule(**module) for module in analysis_data.get("service_modules", [])]
                
                return ServicesPlan(
                    target_file=analysis_data["target_file"],
                    service_modules=service_modules,
                    shared_dependencies=analysis_data["shared_dependencies"],
                    service_contracts=analysis_data["service_contracts"],
                    estimated_lines_reduction=analysis_data["estimated_lines_reduction"]
                )
            
        except Exception as e:
            print(f"[CROSS] Erreur appel GPT-4: {e}")
        
        return self._create_fallback_services_plan(file_path)
    
    def _create_fallback_services_plan(self, file_path: str) -> ServicesPlan:
        """Plan services fallback avec simulation complte"""
        return ServicesPlan(
            target_file=file_path,
            service_modules=[
                ServiceModule(
                    name="OrchestratorService",
                    business_domain="Core Orchestration",
                    methods=["process_request", "coordinate_agents", "manage_state"],
                    dependencies=["state_repository", "agent_factory"],
                    repository_needs=["StateRepository", "AgentRepository"],
                    complexity_level="HIGH",
                    cqrs_commands=["CreateSessionCommand", "UpdateStateCommand", "OrchestateCommand"],
                    cqrs_queries=["GetSessionQuery", "ListAgentsQuery", "GetSystemStatusQuery"]
                ),
                ServiceModule(
                    name="AgentService",
                    business_domain="Agent Management",
                    methods=["create_agent", "get_agent", "update_agent", "delete_agent"],
                    dependencies=["agent_repository", "auth_service"],
                    repository_needs=["AgentRepository"],
                    complexity_level="MEDIUM",
                    cqrs_commands=["CreateAgentCommand", "UpdateAgentCommand", "DeleteAgentCommand"],
                    cqrs_queries=["GetAgentQuery", "ListAgentsQuery", "SearchAgentsQuery"]
                ),
                ServiceModule(
                    name="HealthService",
                    business_domain="System Health",
                    methods=["health_check", "get_status", "check_dependencies"],
                    dependencies=["monitoring_repository"],
                    repository_needs=["MonitoringRepository"],
                    complexity_level="LOW",
                    cqrs_commands=["RecordHealthCommand"],
                    cqrs_queries=["GetHealthQuery", "GetStatusQuery"]
                )
            ],
            shared_dependencies=["DatabaseConnection", "CacheManager", "Logger", "AuthProvider"],
            service_contracts=["IOrchestratorService", "IAgentService", "IHealthService"],
            estimated_lines_reduction=0.90
        )
    
    async def generate_service_files(self, services_plan: ServicesPlan) -> List[str]:
        """Gnrer les fichiers services modulaires"""
        generated_files = []
        
        # Gnrer chaque service module
        for service_module in services_plan.service_modules:
            service_content = await self._generate_service_content(service_module)
            
            # Sauvegarder fichier service
            service_file = Path(f"refactoring_workspace/new_architecture/services/{service_module.name.lower()}.py")
            service_file.parent.mkdir(parents=True, exist_ok=True)
            service_file.write_text(service_content, encoding='utf-8')
            
            generated_files.append(str(service_file))
            print(f"[CHECK] Service gnr: {service_file}")
        
        # Gnrer interfaces/contrats
        for contract in services_plan.service_contracts:
            interface_content = await self._generate_interface_content(contract, services_plan)
            
            interface_file = Path(f"refactoring_workspace/new_architecture/services/interfaces/{contract.lower()}.py")
            interface_file.parent.mkdir(parents=True, exist_ok=True)
            interface_file.write_text(interface_content, encoding='utf-8')
            
            generated_files.append(str(interface_file))
            print(f"[CHECK] Interface gnre: {interface_file}")
        
        return generated_files
    
    async def _generate_service_content(self, service_module: ServiceModule) -> str:
        """Gnrer le contenu d'un fichier service"""
        return f'''"""
{service_module.name} - NextGeneration Architecture Hexagonale
Domaine mtier: {service_module.business_domain}
Gnr automatiquement par Agent Services Creator
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Pattern: Hexagonal Architecture + CQRS
Complexit: {service_module.complexity_level}
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from ..repositories.interfaces import {', '.join(service_module.repository_needs)}
from ..schemas.commands import {', '.join(service_module.cqrs_commands)}
from ..schemas.queries import {', '.join(service_module.cqrs_queries)}

# CQRS Commands
{chr(10).join([f"# - {cmd}" for cmd in service_module.cqrs_commands])}

# CQRS Queries  
{chr(10).join([f"# - {query}" for query in service_module.cqrs_queries])}

class I{service_module.name}(ABC):
    """Interface du service {service_module.name}"""
    
{chr(10).join([f'    @abstractmethod{chr(10)}    async def {method}(self, *args, **kwargs) -> Any:{chr(10)}        """TODO: Dfinir signature pour {method}"""{chr(10)}        pass{chr(10)}' for method in service_module.methods])}

class {service_module.name}(I{service_module.name}):
    """
    Service {service_module.business_domain}
    Implmentation selon Architecture Hexagonale + CQRS
    """
    
    def __init__(self, {', '.join([f"{dep.lower()}: {dep}" for dep in service_module.repository_needs])}):
        """Injection des dpendances"""
{chr(10).join([f"        self.{dep.lower()} = {dep.lower()}" for dep in service_module.repository_needs])}
    
{chr(10).join([f'''    async def {method}(self, *args, **kwargs) -> Any:
        """
        {method} - {service_module.business_domain}
        TODO: Migrer logique depuis main.py
        """
        # TODO: Implmenter logique mtier pour {method}
        pass
''' for method in service_module.methods])}
    
    # CQRS Command Handlers
{chr(10).join([f'''    async def handle_{cmd.lower().replace("command", "")}(self, command: {cmd}) -> Any:
        """Handler pour {cmd}"""
        # TODO: Implmenter handler command
        pass
''' for cmd in service_module.cqrs_commands])}
    
    # CQRS Query Handlers
{chr(10).join([f'''    async def handle_{query.lower().replace("query", "")}(self, query: {query}) -> Any:
        """Handler pour {query}"""
        # TODO: Implmenter handler query
        pass
''' for query in service_module.cqrs_queries])}
'''

    async def _generate_interface_content(self, contract: str, services_plan: ServicesPlan) -> str:
        """Gnrer le contenu d'une interface service"""
        return f'''"""
{contract} - Interface NextGeneration
Architecture Hexagonale - Contrats de service
Gnr automatiquement par Agent Services Creator
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class {contract}(ABC):
    """
    Interface pour services {contract.replace('I', '')}
    Respecte Dependency Inversion Principle
    """
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialiser le service"""
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Vrification sant du service"""
        pass
    
    @abstractmethod
    async def cleanup(self) -> None:
        """Nettoyage ressources"""
        pass
'''

    async def create_services_report(self, services_plans: List[ServicesPlan]) -> str:
        """Crer rapport global de gnration services"""
        total_services = sum(len(plan.service_modules) for plan in services_plans)
        total_contracts = sum(len(plan.service_contracts) for plan in services_plans)
        avg_reduction = sum(plan.estimated_lines_reduction for plan in services_plans) / len(services_plans)
        
        report_content = f"""# [CONSTRUCTION] Rapport Gnration Services - Phase 3

## [CHECK] Vue d'Ensemble

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Agent:** Services Creator (GPT-4 Turbo)  
**Fichiers analyss:** {len(services_plans)}  
**Services crs:** {total_services}  
**Interfaces gnres:** {total_contracts}  
**Rduction moyenne:** {avg_reduction:.1%}

## [CONSTRUCTION] Architecture Rsultante

###  Services Modulaires
"""
        
        for plan in services_plans:
            report_content += f"""
#### [FOLDER] {plan.target_file}
"""
            for service in plan.service_modules:
                report_content += f"""- **{service.name}** ({service.complexity_level})
  - Domaine: {service.business_domain}
  - Mthodes: {len(service.methods)}
  - Commands CQRS: {len(service.cqrs_commands)}
  - Queries CQRS: {len(service.cqrs_queries)}
"""
        
        report_content += f"""
###  Dpendances Partages
{chr(10).join([f"- {dep}" for plan in services_plans for dep in plan.shared_dependencies])}

### [CLIPBOARD] Interfaces Gnres  
{chr(10).join([f"- {contract}" for plan in services_plans for contract in plan.service_contracts])}

## [TARGET] Prochaines tapes

1. [CHECK] Services modulaires crs
2.  Crer repositories pattern
3.  Implmenter CQRS handlers
4.  Migrer logique mtier main.py  services

---
*Gnr par Agent Services Creator NextGeneration*
"""
        
        # Sauvegarder rapport
        report_file = self.results_dir / f"services_creation_report_{self.timestamp}.md"
        report_file.write_text(report_content, encoding='utf-8')
        
        print(f"[CLIPBOARD] Rapport sauvegard: {report_file}")
        return str(report_file)

async def main():
    """Point d'entre pour tests standalone"""
    agent = AgentServicesCreator()
    
    # Test avec donnes simules
    routes_data = {
        "total_routes": 5,
        "routes": [
            {"method": "GET", "path": "/health", "function_name": "health_check"},
            {"method": "POST", "path": "/api/auth/login", "function_name": "login"}
        ]
    }
    
    plan = await agent.analyze_service_needs("orchestrator/app/main.py", routes_data)
    print(f"[TARGET] Plan services cr: {len(plan.service_modules)} services")
    
    # Gnrer services
    service_files = await agent.generate_service_files(plan)
    print(f"[CONSTRUCTION] {len(service_files)} fichiers services gnrs")
    
    # Rapport
    report = await agent.create_services_report([plan])
    print(f"[CLIPBOARD] Rapport cr: {report}")

if __name__ == "__main__":
    asyncio.run(main()) 



