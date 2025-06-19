"""
Agent Factory Enterprise SDK Client
==================================

Usage:
    from agent_factory_sdk import AgentFactoryClient
    
    client = AgentFactoryClient(
        base_url="https://api.enterprise.com",
        api_key="your_api_key"
    )
    
    # Créer agent
    agent = client.create_agent("database", {"host": "localhost"})
    
    # Exécuter tâche
    result = client.execute_task(agent.id, "backup", {"tables": ["users"]})
"""

import requests
from typing import Dict, Any, Optional

class AgentFactoryClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def create_agent(self, agent_type: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Créer un agent"""
        response = self.session.post(
            f"{self.base_url}/agents",
            json={
                "agent_type": agent_type,
                "config": config or {},
                "priority": "medium",
                "tags": []
            }
        )
        response.raise_for_status()
        return response.json()
    
    def execute_task(self, agent_id: str, action: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Exécuter une tâche"""
        response = self.session.post(
            f"{self.base_url}/agents/{agent_id}/tasks",
            json={
                "agent_id": agent_id,
                "action": action,
                "params": params or {},
                "timeout": 30,
                "async_execution": False
            }
        )
        response.raise_for_status()
        return response.json()
    
    def list_agents(self) -> Dict[str, Any]:
        """Lister les agents"""
        response = self.session.get(f"{self.base_url}/agents")
        response.raise_for_status()
        return response.json()
    
    def get_metrics(self) -> Dict[str, Any]:
        """Obtenir les métriques"""
        response = self.session.get(f"{self.base_url}/metrics")
        response.raise_for_status()
        return response.json()
