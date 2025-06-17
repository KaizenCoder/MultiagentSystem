#!/usr/bin/env python3
"""
Template de base pour créer un agent personnalisé
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
    """Priorités des tâches"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class AgentTask:
    """Structure d'une tâche pour agent"""
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
    """Structure de réponse d'un agent"""
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
        """Vérifie si l'agent peut traiter cette tâche"""
        return (
            not self.is_busy and
            task.agent_type == self.agent_type
        )
    
    async def process_task(self, task: AgentTask) -> AgentResponse:
        """Traite une tâche (à override par les agents spécialisés)"""
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
        """Exécution spécifique de la tâche (à override)"""
        return f"Tâche '{task.description}' traitée par {self.agent_id}"
    
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

# Exemple d'agents spécialisés
class AnalyzerAgent(BaseAgent):
    """Agent spécialisé dans l'analyse"""
    
    def __init__(self, agent_id: str):
        super().__init__(agent_id, AgentType.ANALYZER)
    
    async def _execute_task(self, task: AgentTask) -> str:
        """Analyse spécialisée"""
        await asyncio.sleep(0.2)  # Simulation traitement
        
        analysis_points = [
            "📊 Analyse des données principales",
            "🔍 Identification des tendances",
            "⚠️  Points d'attention détectés",
            "💡 Recommandations suggérées"
        ]
        
        return f"""
ANALYSE COMPLÈTE - {task.description}

{chr(10).join(analysis_points)}

📈 Résumé: L'analyse révèle des éléments intéressants nécessitant une attention particulière.
🎯 Prochaines étapes recommandées pour optimiser les résultats.
        """.strip()

class WriterAgent(BaseAgent):
    """Agent spécialisé dans la rédaction"""
    
    def __init__(self, agent_id: str):
        super().__init__(agent_id, AgentType.WRITER)
    
    async def _execute_task(self, task: AgentTask) -> str:
        """Rédaction spécialisée"""
        await asyncio.sleep(0.3)  # Simulation traitement
        
        return f"""
# {task.description}

## Introduction
Ce document présente une approche structurée pour traiter la demande formulée.

## Développement
Les éléments clés à considérer incluent une analyse approfondie des besoins,
une planification méthodique, et une exécution soignée.

## Conclusion
Cette approche garantit un résultat de qualité répondant aux attentes.

---
*Document généré par {self.agent_id} - Agent de rédaction spécialisé*
        """.strip()

class CoderAgent(BaseAgent):
    """Agent spécialisé dans le développement"""
    
    def __init__(self, agent_id: str):
        super().__init__(agent_id, AgentType.CODER)
    
    async def _execute_task(self, task: AgentTask) -> str:
        """Développement spécialisé"""
        await asyncio.sleep(0.4)  # Simulation traitement
        
        code_example = '''
def process_request(data):
    """
    Traite une requête selon la demande: {description}
    """
    try:
        # Validation des données
        if not data:
            raise ValueError("Données manquantes")
        
        # Traitement principal
        result = analyze_and_process(data)
        
        # Retour du résultat
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
    """Démonstration des agents personnalisés"""
    print("🤖 DÉMONSTRATION DES AGENTS PERSONNALISÉS")
    print("=" * 50)
    
    # Créer des agents
    analyzer = AnalyzerAgent("analyzer_001")
    writer = WriterAgent("writer_001")  
    coder = CoderAgent("coder_001")
    
    agents = [analyzer, writer, coder]
    
    # Créer des tâches
    tasks = [
        AgentTask("task_1", "Analyser les performances du système", AgentType.ANALYZER, TaskPriority.HIGH),
        AgentTask("task_2", "Rédiger un rapport de synthèse", AgentType.WRITER, TaskPriority.NORMAL),
        AgentTask("task_3", "Développer une fonction de traitement", AgentType.CODER, TaskPriority.HIGH)
    ]
    
    # Traiter les tâches
    for task in tasks:
        print(f"\n📋 Traitement: {task.description}")
        
        for agent in agents:
            if await agent.can_handle_task(task):
                print(f"   🤖 Assigné à: {agent.agent_id}")
                response = await agent.process_task(task)
                print(f"   ✅ Status: {response.status}")
                print(f"   ⏱️  Temps: {response.processing_time:.2f}s")
                print(f"   📝 Résultat (aperçu): {response.result[:100]}...")
                break
        else:
            print(f"   ❌ Aucun agent disponible pour cette tâche")
    
    # Afficher les stats
    print(f"\n📊 STATISTIQUES DES AGENTS")
    print("-" * 30)
    for agent in agents:
        stats = agent.get_stats()
        print(f"🤖 {stats['agent_id']}: {stats['tasks_completed']} tâches")

if __name__ == "__main__":
    asyncio.run(demo_agents())
