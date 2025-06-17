#!/usr/bin/env python3
"""
Agent personnalisé intégré avec l'orchestrateur
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
    print("✅ Configuration chargée")
except ImportError as e:
    print(f"❌ Erreur d'import config: {e}")
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
        """Appel direct à l'API OpenAI"""
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
                print(f"❌ OpenAI API Error: {response.status_code} - {response.text}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            print(f"❌ OpenAI Exception: {e}")
            return {"success": False, "error": str(e)}
    
    async def call_anthropic_api(self, prompt: str, max_tokens: int = 150) -> Dict[str, Any]:
        """Appel direct à l'API Anthropic"""
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
                print(f"❌ Anthropic API Error: {response.status_code} - {response.text}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            print(f"❌ Anthropic Exception: {e}")
            return {"success": False, "error": str(e)}
    
    async def process_task(self, prompt: str, max_tokens: int = 200, model: Optional[str] = None) -> Dict[str, Any]:
        """Traiter une tâche avec le LLM approprié"""
        model_to_use = model or self.preferred_model
        
        print(f"🤖 Agent {self.agent_id} traite: '{prompt[:50]}...'")
        print(f"   🧠 Modèle: {model_to_use}")
        
        try:
            if model_to_use.lower() == "openai":
                result = await self.call_openai_api(prompt, max_tokens)
            elif model_to_use.lower() == "anthropic":
                result = await self.call_anthropic_api(prompt, max_tokens)
            else:
                # Par défaut, essayer OpenAI puis Anthropic
                result = await self.call_openai_api(prompt, max_tokens)
                if not result.get("success"):
                    print("   🔄 Fallback vers Anthropic...")
                    result = await self.call_anthropic_api(prompt, max_tokens)
            
            if result.get("success"):
                self.stats["tasks_completed"] += 1
                print(f"   ✅ Tâche terminée ({result.get('tokens_used', 0)} tokens)")
            else:
                self.stats["errors"] += 1
                print(f"   ❌ Échec: {result.get('error', 'Erreur inconnue')}")
            
            return result
            
        except Exception as e:
            self.stats["errors"] += 1
            print(f"   ❌ Exception: {e}")
            return {"success": False, "error": str(e)}
    
    def get_stats(self) -> Dict[str, Any]:
        """Statistiques de l'agent"""
        return {
            "agent_id": self.agent_id,
            "preferred_model": self.preferred_model,
            **self.stats
        }

async def demo_real_llm_agent():
    """Démonstration avec les vraies APIs"""
    print("🚀 DÉMONSTRATION AGENT LLM RÉEL")
    print("=" * 40)
    
    # Tâches de test
    tasks = [
        {
            "prompt": "Écris un court poème sur l'intelligence artificielle",
            "model": "openai",
            "max_tokens": 100
        },
        {
            "prompt": "Explique brièvement les avantages de Docker",
            "model": "anthropic", 
            "max_tokens": 150
        },
        {
            "prompt": "Crée un exemple de fonction Python pour calculer la factorielle",
            "model": "openai",
            "max_tokens": 200
        }
    ]
    
    # Créer et utiliser l'agent
    async with RealLLMAgent("llm_agent_001") as agent:
        
        for i, task in enumerate(tasks, 1):
            print(f"\n📋 Tâche {i}/{len(tasks)}")
            print("-" * 20)
            
            result = await agent.process_task(
                task["prompt"], 
                task["max_tokens"], 
                task["model"]
            )
            
            if result.get("success"):
                print(f"📝 Résultat:")
                print(f"   {result['content'][:200]}...")
                if len(result['content']) > 200:
                    print("   [... contenu tronqué]")
            else:
                print(f"❌ Erreur: {result.get('error')}")
            
            # Petite pause entre les requêtes
            await asyncio.sleep(1)
        
        # Afficher les statistiques finales
        print(f"\n📊 STATISTIQUES FINALES")
        print("-" * 25)
        stats = agent.get_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")

async def test_orchestrator_integration():
    """Test d'intégration avec l'orchestrateur local"""
    print("\n🔗 TEST D'INTÉGRATION ORCHESTRATEUR")
    print("=" * 40)
    
    try:
        # Tester la connexion à l'orchestrateur local
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://localhost:8002/health",
                headers={"X-API-KEY": "demo-key-for-testing"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Orchestrateur accessible")
                print(f"   🤖 OpenAI: {'✅' if data.get('openai_configured') else '❌'}")
                print(f"   🧠 Anthropic: {'✅' if data.get('anthropic_configured') else '❌'}")
                
                # Test avec agent LLM
                async with RealLLMAgent("integration_test") as agent:
                    result = await agent.process_task(
                        "Salut! Peux-tu me dire bonjour en français ?",
                        max_tokens=50,
                        model="openai"
                    )
                    
                    if result.get("success"):
                        print(f"✅ Test LLM réussi: {result['content'][:100]}...")
                    else:
                        print(f"❌ Test LLM échoué: {result.get('error')}")
            else:
                print(f"❌ Orchestrateur inaccessible: {response.status_code}")
                
    except Exception as e:
        print(f"❌ Erreur d'intégration: {e}")

async def main():
    """Fonction principale"""
    try:
        await demo_real_llm_agent()
        await test_orchestrator_integration()
        
        print(f"\n🎉 Démonstration terminée!")
        print("💡 Vos agents peuvent maintenant utiliser les vraies APIs LLM")
        
    except KeyboardInterrupt:
        print("\n⏹️  Démonstration interrompue")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")

if __name__ == "__main__":
    asyncio.run(main())
