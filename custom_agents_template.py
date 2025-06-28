#!/usr/bin/env python3
"""
Template de base pour crer un agent personnalis
Compatible avec l'orchestrateur NextGeneration
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class AgentType(Enum):
    """Types d'agents disponibles"""
    ANALYZER = "analyzer"
    WRITER = "writer"
    CODER = "coder"
    RESEARCHER = "researcher"
    VALIDATOR = "validator"

class TaskPriority(Enum):
    """Priorits des tches"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class AgentTask:
    """Structure d'une tche pour agent"""
    id: str
    description: str
    agent_type: AgentType
    priority: TaskPriority
    max_tokens: int = 1000
    model_preference: str = "openai"  # ou "anthropic"
    context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}

@dataclass
class AgentResponse:
    """Structure de rponse d'un agent"""
    task_id: str
    agent_id: str
    status: str  # "success", "error", "partial"
    result: str
    metadata: Dict[str, Any] = None
    processing_time: float = 0.0
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class BaseAgent:
    """Classe de base pour tous les agents"""
    
    def __init__(self, agent_id: str, agent_type: AgentType, config: Dict[str, Any] = None):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.config = config or {}
        self.is_busy = False
        self.task_history: List[AgentTask] = []
    
    async def can_handle_task(self, task: AgentTask) -> bool:
        """Vrifie si l'agent peut traiter cette tche"""
        return (
            not self.is_busy and
            task.agent_type == self.agent_type
        )
    
    async def process_task(self, task: AgentTask) -> AgentResponse:
        """Traite une tche ( override par les agents spcialiss)"""
        import time
        start_time = time.time()
        
        try:
            self.is_busy = True
            self.task_history.append(task)
            
            # Simulation du traitement
            await asyncio.sleep(0.1)
            result = await self._execute_task(task)
            
            processing_time = time.time() - start_time
            
            return AgentResponse(
                task_id=task.id,
                agent_id=self.agent_id,
                status="success",
                result=result,
                processing_time=processing_time,
                metadata={
                    "model_used": task.model_preference,
                    "tokens_used": len(result.split()) * 1.3  # Estimation
                }
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            return AgentResponse(
                task_id=task.id,
                agent_id=self.agent_id,
                status="error",
                result=f"Erreur: {str(e)}",
                processing_time=processing_time
            )
        finally:
            self.is_busy = False
    
    async def _execute_task(self, task: AgentTask) -> str:
        """Excution spcifique de la tche ( override)"""
        return f"Tche '{task.description}' traite par {self.agent_id}"
    
    def get_stats(self) -> Dict[str, Any]:
        """Statistiques de l'agent"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type.value,
            "is_busy": self.is_busy,
            "tasks_completed": len(self.task_history),
            "total_processing_time": sum(
                getattr(task, 'processing_time', 0) 
                for task in self.task_history
            )
        }

# Exemple d'agents spcialiss
class AnalyzerAgent(BaseAgent):
    """Agent spcialis dans l'analyse"""
    
    def __init__(self, agent_id: str):
        super().__init__(agent_id, AgentType.ANALYZER)
    
    async def _execute_task(self, task: AgentTask) -> str:
        """Analyse spcialise"""
        await asyncio.sleep(0.2)  # Simulation traitement
        
        analysis_points = [
            "[CHART] Analyse des donnes principales",
            "[SEARCH] Identification des tendances",
            "  Points d'attention dtects",
            "[BULB] Recommandations suggres"
        ]
        
        return f"""
ANALYSE COMPLTE - {task.description}

{chr(10).join(analysis_points)}

 Rsum: L'analyse rvle des lments intressants ncessitant une attention particulire.
[TARGET] Prochaines tapes recommandes pour optimiser les rsultats.
        """.strip()

class WriterAgent(BaseAgent):
    """Agent spcialis dans la rdaction"""
    
    def __init__(self, agent_id: str):
        super().__init__(agent_id, AgentType.WRITER)
    
    async def _execute_task(self, task: AgentTask) -> str:
        """Rdaction spcialise"""
        await asyncio.sleep(0.3)  # Simulation traitement
        
        return f"""
# {task.description}

## Introduction
Ce document prsente une approche structure pour traiter la demande formule.

## Dveloppement
Les lments cls  considrer incluent une analyse approfondie des besoins,
une planification mthodique, et une excution soigne.

## Conclusion
Cette approche garantit un rsultat de qualit rpondant aux attentes.

---
*Document gnr par {self.agent_id} - Agent de rdaction spcialis*
        """.strip()

class CoderAgent(BaseAgent):
    """Agent spcialis dans le dveloppement"""
    
    def __init__(self, agent_id: str):
        super().__init__(agent_id, AgentType.CODER)
    
    async def _execute_task(self, task: AgentTask) -> str:
        """Dveloppement spcialis"""
        await asyncio.sleep(0.4)  # Simulation traitement
        
        code_example = '''
def process_request(data):
    """
    Traite une requte selon la demande: {description}
    """
    try:
        # Validation des donnes
        if not data:
            raise ValueError("Donnes manquantes")
        
        # Traitement principal
        result = analyze_and_process(data)
        
        # Retour du rsultat
        return {{
            "status": "success",
            "result": result,
            "metadata": {{
                "processed_at": datetime.now().isoformat(),
                "agent": "{agent_id}"
            }}
        }}
        
    except Exception as e:
        return {{
            "status": "error",
            "error": str(e)
        }}

# Utilisation
# result = process_request(your_data)
'''.format(description=task.description, agent_id=self.agent_id)
        
        return f"```python{code_example}```"

# Exemple d'utilisation
async def demo_agents():
    """Dmonstration des agents personnaliss"""
    print("[ROBOT] DMONSTRATION DES AGENTS PERSONNALISS")
    print("=" * 50)
    
    # Crer des agents
    analyzer = AnalyzerAgent("analyzer_001")
    writer = WriterAgent("writer_001")  
    coder = CoderAgent("coder_001")
    
    agents = [analyzer, writer, coder]
    
    # Crer des tches
    tasks = [
        AgentTask("task_1", "Analyser les performances du systme", AgentType.ANALYZER, TaskPriority.HIGH),
        AgentTask("task_2", "Rdiger un rapport de synthse", AgentType.WRITER, TaskPriority.NORMAL),
        AgentTask("task_3", "Dvelopper une fonction de traitement", AgentType.CODER, TaskPriority.HIGH)
    ]
    
    # Traiter les tches
    for task in tasks:
        print(f"\n[CLIPBOARD] Traitement: {task.description}")
        
        for agent in agents:
            if await agent.can_handle_task(task):
                print(f"   [ROBOT] Assign : {agent.agent_id}")
                response = await agent.process_task(task)
                print(f"   [CHECK] Status: {response.status}")
                print(f"     Temps: {response.processing_time:.2f}s")
                print(f"    Rsultat (aperu): {response.result[:100]}...")
                break
        else:
            print(f"   [CROSS] Aucun agent disponible pour cette tche")
    
    # Afficher les stats
    print(f"\n[CHART] STATISTIQUES DES AGENTS")
    print("-" * 30)
    for agent in agents:
        stats = agent.get_stats()
        print(f"[ROBOT] {stats['agent_id']}: {stats['tasks_completed']} tches")

if __name__ == "__main__":
    asyncio.run(demo_agents())




