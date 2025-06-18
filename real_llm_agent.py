#!/usr/bin/env python3
"""
Agent personnalis intgr avec l'orchestrateur
Utilise les vraies APIs OpenAI et Anthropic
"""

import asyncio
import json
import httpx
from typing import Dict, Any, Optional
import os
import sys
from pathlib import Path

# Ajouter le chemin pour les imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
os.chdir(project_root / "orchestrator")

try:
    from orchestrator.app.config import settings
    print("[CHECK] Configuration charge")
except ImportError as e:
    print(f"[CROSS] Erreur d'import config: {e}")
    sys.exit(1)

class RealLLMAgent:
    """Agent utilisant les vraies APIs LLM"""
    
    def __init__(self, agent_id: str, preferred_model: str = "openai"):
        self.agent_id = agent_id
        self.preferred_model = preferred_model
        self.session = None
        self.stats = {
            "tasks_completed": 0,
            "total_tokens": 0,
            "errors": 0
        }
    
    async def __aenter__(self):
        """Gestionnaire de contexte asynchrone"""
        self.session = httpx.AsyncClient(timeout=60.0)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Fermeture du client HTTP"""
        if self.session:
            await self.session.aclose()
    
    async def call_openai_api(self, prompt: str, max_tokens: int = 150) -> Dict[str, Any]:
        """Appel direct  l'API OpenAI"""
        try:
            headers = {
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            response = await self.session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                tokens_used = data["usage"]["total_tokens"]
                
                self.stats["total_tokens"] += tokens_used
                
                return {
                    "success": True,
                    "content": content,
                    "tokens_used": tokens_used,
                    "model": "gpt-3.5-turbo"
                }
            else:
                print(f"[CROSS] OpenAI API Error: {response.status_code} - {response.text}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            print(f"[CROSS] OpenAI Exception: {e}")
            return {"success": False, "error": str(e)}
    
    async def call_anthropic_api(self, prompt: str, max_tokens: int = 150) -> Dict[str, Any]:
        """Appel direct  l'API Anthropic"""
        try:
            headers = {
                "x-api-key": settings.ANTHROPIC_API_KEY,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            
            payload = {
                "model": "claude-3-haiku-20240307",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens
            }
            
            response = await self.session.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data["content"][0]["text"]
                
                # Anthropic ne retourne pas toujours les tokens, estimation
                tokens_used = len(content.split()) * 1.3
                self.stats["total_tokens"] += int(tokens_used)
                
                return {
                    "success": True,
                    "content": content,
                    "tokens_used": int(tokens_used),
                    "model": "claude-3-haiku-20240307"
                }
            else:
                print(f"[CROSS] Anthropic API Error: {response.status_code} - {response.text}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            print(f"[CROSS] Anthropic Exception: {e}")
            return {"success": False, "error": str(e)}
    
    async def process_task(self, prompt: str, max_tokens: int = 200, model: Optional[str] = None) -> Dict[str, Any]:
        """Traiter une tche avec le LLM appropri"""
        model_to_use = model or self.preferred_model
        
        print(f"[ROBOT] Agent {self.agent_id} traite: '{prompt[:50]}...'")
        print(f"    Modle: {model_to_use}")
        
        try:
            if model_to_use.lower() == "openai":
                result = await self.call_openai_api(prompt, max_tokens)
            elif model_to_use.lower() == "anthropic":
                result = await self.call_anthropic_api(prompt, max_tokens)
            else:
                # Par dfaut, essayer OpenAI puis Anthropic
                result = await self.call_openai_api(prompt, max_tokens)
                if not result.get("success"):
                    print("    Fallback vers Anthropic...")
                    result = await self.call_anthropic_api(prompt, max_tokens)
            
            if result.get("success"):
                self.stats["tasks_completed"] += 1
                print(f"   [CHECK] Tche termine ({result.get('tokens_used', 0)} tokens)")
            else:
                self.stats["errors"] += 1
                print(f"   [CROSS] chec: {result.get('error', 'Erreur inconnue')}")
            
            return result
            
        except Exception as e:
            self.stats["errors"] += 1
            print(f"   [CROSS] Exception: {e}")
            return {"success": False, "error": str(e)}
    
    def get_stats(self) -> Dict[str, Any]:
        """Statistiques de l'agent"""
        return {
            "agent_id": self.agent_id,
            "preferred_model": self.preferred_model,
            **self.stats
        }

async def demo_real_llm_agent():
    """Dmonstration avec les vraies APIs"""
    print("[ROCKET] DMONSTRATION AGENT LLM REL")
    print("=" * 40)
    
    # Tches de test
    tasks = [
        {
            "prompt": "cris un court pome sur l'intelligence artificielle",
            "model": "openai",
            "max_tokens": 100
        },
        {
            "prompt": "Explique brivement les avantages de Docker",
            "model": "anthropic", 
            "max_tokens": 150
        },
        {
            "prompt": "Cre un exemple de fonction Python pour calculer la factorielle",
            "model": "openai",
            "max_tokens": 200
        }
    ]
    
    # Crer et utiliser l'agent
    async with RealLLMAgent("llm_agent_001") as agent:
        
        for i, task in enumerate(tasks, 1):
            print(f"\n[CLIPBOARD] Tche {i}/{len(tasks)}")
            print("-" * 20)
            
            result = await agent.process_task(
                task["prompt"], 
                task["max_tokens"], 
                task["model"]
            )
            
            if result.get("success"):
                print(f" Rsultat:")
                print(f"   {result['content'][:200]}...")
                if len(result['content']) > 200:
                    print("   [... contenu tronqu]")
            else:
                print(f"[CROSS] Erreur: {result.get('error')}")
            
            # Petite pause entre les requtes
            await asyncio.sleep(1)
        
        # Afficher les statistiques finales
        print(f"\n[CHART] STATISTIQUES FINALES")
        print("-" * 25)
        stats = agent.get_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")

async def test_orchestrator_integration():
    """Test d'intgration avec l'orchestrateur local"""
    print("\n TEST D'INTGRATION ORCHESTRATEUR")
    print("=" * 40)
    
    try:
        # Tester la connexion  l'orchestrateur local
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://localhost:8002/health",
                headers={"X-API-KEY": "demo-key-for-testing"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print("[CHECK] Orchestrateur accessible")
                print(f"   [ROBOT] OpenAI: {'[CHECK]' if data.get('openai_configured') else '[CROSS]'}")
                print(f"    Anthropic: {'[CHECK]' if data.get('anthropic_configured') else '[CROSS]'}")
                
                # Test avec agent LLM
                async with RealLLMAgent("integration_test") as agent:
                    result = await agent.process_task(
                        "Salut! Peux-tu me dire bonjour en franais ?",
                        max_tokens=50,
                        model="openai"
                    )
                    
                    if result.get("success"):
                        print(f"[CHECK] Test LLM russi: {result['content'][:100]}...")
                    else:
                        print(f"[CROSS] Test LLM chou: {result.get('error')}")
            else:
                print(f"[CROSS] Orchestrateur inaccessible: {response.status_code}")
                
    except Exception as e:
        print(f"[CROSS] Erreur d'intgration: {e}")

async def main():
    """Fonction principale"""
    try:
        await demo_real_llm_agent()
        await test_orchestrator_integration()
        
        print(f"\n Dmonstration termine!")
        print("[BULB] Vos agents peuvent maintenant utiliser les vraies APIs LLM")
        
    except KeyboardInterrupt:
        print("\n  Dmonstration interrompue")
    except Exception as e:
        print(f"\n[CROSS] Erreur: {e}")

if __name__ == "__main__":
    asyncio.run(main())
