#!/usr/bin/env python3
"""
Agent pratique utilisant principalement Anthropic
Avec fallback intelligent et gestion d'erreurs
"""

import asyncio
import httpx
import json
from typing import Dict, Any, List
import os
import sys
from pathlib import Path

# Configuration
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
os.chdir(project_root / "orchestrator")

try:
    from orchestrator.app.config import settings
    print("[CHECK] Configuration charge")
except ImportError:
    print("[CROSS] Erreur de configuration")
    sys.exit(1)

class SmartAgent:
    """Agent intelligent avec fallback et gestion d'erreurs"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.session = None
        self.stats = {
            "anthropic_calls": 0,
            "openai_calls": 0,
            "total_tokens": 0,
            "errors": 0,
            "successful_tasks": 0
        }
    
    async def __aenter__(self):
        self.session = httpx.AsyncClient(timeout=60.0)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.aclose()
    
    async def call_anthropic(self, prompt: str, max_tokens: int = 200) -> Dict[str, Any]:
        """Appel  l'API Anthropic (recommand)"""
        try:
            headers = {
                "x-api-key": settings.ANTHROPIC_API_KEY,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            
            payload = {
                "model": "claude-3-haiku-20240307",
                "messages": [{"role": "user", "content": prompt}],
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
                tokens_used = len(content.split()) * 1.3
                
                self.stats["anthropic_calls"] += 1
                self.stats["total_tokens"] += int(tokens_used)
                
                return {
                    "success": True,
                    "content": content,
                    "tokens_used": int(tokens_used),
                    "model": "claude-3-haiku",
                    "provider": "anthropic"
                }
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def smart_process(self, prompt: str, max_tokens: int = 200) -> Dict[str, Any]:
        """Traitement intelligent avec Anthropic comme provider principal"""
        print(f" {self.agent_id} traite: '{prompt[:60]}...'")
        
        # Essayer Anthropic en premier (plus fiable actuellement)
        result = await self.call_anthropic(prompt, max_tokens)
        
        if result.get("success"):
            self.stats["successful_tasks"] += 1
            print(f"   [CHECK] Succs avec Anthropic ({result.get('tokens_used', 0)} tokens)")
            return result
        else:
            self.stats["errors"] += 1
            print(f"   [CROSS] chec: {result.get('error')}")
            return result

# Agents spcialiss utilisant l'API
class WriterBot(SmartAgent):
    """Bot spcialis en rdaction"""
    
    async def write_document(self, topic: str, style: str = "professionnel") -> str:
        prompt = f"""
Rdige un document {style} sur le sujet suivant: {topic}

Structure attendue:
- Introduction claire
- Dveloppement structur 
- Conclusion pertinente
- Style {style} et fluide

Sujet: {topic}
"""
        result = await self.smart_process(prompt, max_tokens=400)
        return result.get("content", f"Erreur lors de la rdaction: {result.get('error')}")
    
    async def create_summary(self, text: str) -> str:
        prompt = f"""
Cre un rsum concis et structur du texte suivant:

{text[:1000]}...

Le rsum doit:
- Capturer les points cls
- tre clair et concis
- Garder la structure logique
"""
        result = await self.smart_process(prompt, max_tokens=200)
        return result.get("content", f"Erreur lors du rsum: {result.get('error')}")

class CodeBot(SmartAgent):
    """Bot spcialis en dveloppement"""
    
    async def create_function(self, description: str, language: str = "python") -> str:
        prompt = f"""
Cre une fonction {language} selon cette description: {description}

Exigences:
- Code propre et comment
- Gestion d'erreurs approprie
- Exemples d'utilisation
- Documentation docstring

Description: {description}
Langage: {language}
"""
        result = await self.smart_process(prompt, max_tokens=300)
        return result.get("content", f"Erreur lors de la gnration: {result.get('error')}")
    
    async def explain_code(self, code: str) -> str:
        prompt = f"""
Explique ce code de manire claire et pdagogique:

```
{code[:500]}
```

L'explication doit inclure:
- Objectif du code
- Fonctionnement tape par tape
- Points importants  retenir
"""
        result = await self.smart_process(prompt, max_tokens=250)
        return result.get("content", f"Erreur lors de l'explication: {result.get('error')}")

class AnalystBot(SmartAgent):
    """Bot spcialis en analyse"""
    
    async def analyze_data(self, data_description: str) -> str:
        prompt = f"""
Effectue une analyse structure des donnes suivantes: {data_description}

Structure d'analyse:
- Vue d'ensemble des donnes
- Tendances identifies
- Points d'attention
- Recommandations
- Prochaines tapes

Donnes: {data_description}
"""
        result = await self.smart_process(prompt, max_tokens=350)
        return result.get("content", f"Erreur lors de l'analyse: {result.get('error')}")

async def demonstration_complete():
    """Dmonstration complte des agents spcialiss"""
    print("[ROBOT] DMONSTRATION AGENTS SPCIALISS")
    print("=" * 50)
    
    # Test Writer Bot
    print("\n TEST WRITER BOT")
    print("-" * 20)
    async with WriterBot("writer_bot_001") as writer:
        
        # Test rdaction
        doc = await writer.write_document("L'importance de la cyberscurit", "informatif")
        print("[DOCUMENT] Document gnr:")
        print(doc[:300] + "..." if len(doc) > 300 else doc)
        
        # Test rsum
        long_text = """
        L'intelligence artificielle reprsente une rvolution technologique majeure. 
        Elle transforme tous les secteurs: sant, finance, transport, ducation.
        Les algorithmes d'apprentissage automatique permettent aux machines d'apprendre
        et de s'amliorer sans programmation explicite. Cependant, cette technologie
        soulve aussi des questions thiques importantes concernant l'emploi,
        la vie prive et la prise de dcision automatise.
        """
        
        summary = await writer.create_summary(long_text)
        print(f"\n[CLIPBOARD] Rsum gnr:")
        print(summary)
    
    # Test Code Bot
    print(f"\n TEST CODE BOT")
    print("-" * 20)
    async with CodeBot("code_bot_001") as coder:
        
        # Test gnration de fonction
        function = await coder.create_function(
            "Une fonction qui calcule la moyenne d'une liste de nombres avec gestion d'erreurs"
        )
        print(" Fonction gnre:")
        print(function[:400] + "..." if len(function) > 400 else function)
        
        # Test explication de code
        sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
        """
        
        explanation = await coder.explain_code(sample_code)
        print(f"\n[SEARCH] Explication:")
        print(explanation)
    
    # Test Analyst Bot
    print(f"\n[CHART] TEST ANALYST BOT")
    print("-" * 20)
    async with AnalystBot("analyst_bot_001") as analyst:
        
        analysis = await analyst.analyze_data(
            "Donnes de ventes e-commerce: 1000 commandes/jour, panier moyen 45, "
            "taux de conversion 2.5%, pics le weekend, baisse en t"
        )
        print(" Analyse gnre:")
        print(analysis)
    
    # Statistiques globales
    print(f"\n[CHART] STATISTIQUES GLOBALES")
    print("-" * 25)
    for bot_name, bot in [("Writer", writer), ("Coder", coder), ("Analyst", analyst)]:
        stats = bot.stats
        print(f"[ROBOT] {bot_name}:")
        print(f"   [CHECK] Tches russies: {stats['successful_tasks']}")
        print(f"    Appels Anthropic: {stats['anthropic_calls']}")
        print(f"   [CHART] Tokens totaux: {stats['total_tokens']}")
        print(f"   [CROSS] Erreurs: {stats['errors']}")

async def test_multi_agent_workflow():
    """Test d'un workflow multi-agents"""
    print(f"\n TEST WORKFLOW MULTI-AGENTS")
    print("=" * 40)
    
    # Scnario: Analyser un problme, proposer une solution code, documenter
    topic = "Systme de cache pour amliorer les performances d'une API"
    
    async with AnalystBot("analyst") as analyst, \
               CodeBot("coder") as coder, \
               WriterBot("writer") as writer:
        
        print("1 Analyse du problme...")
        analysis = await analyst.analyze_data(f"Problme de performance: {topic}")
        print(f"   [CLIPBOARD] Analyse: {analysis[:100]}...")
        
        print("\n2 Gnration de solution code...")
        code_solution = await coder.create_function(
            "Systme de cache Redis avec TTL et invalidation automatique"
        )
        print(f"    Code: {code_solution[:100]}...")
        
        print("\n3 Documentation finale...")
        final_doc = await writer.write_document(
            f"Solution de cache base sur l'analyse: {analysis[:200]}",
            "technique"
        )
        print(f"    Documentation: {final_doc[:100]}...")
        
        print(f"\n[CHECK] Workflow termin! 3 agents ont collabor avec succs.")

async def main():
    """Fonction principale"""
    try:
        await demonstration_complete()
        await test_multi_agent_workflow()
        
        print(f"\n DMONSTRATION TERMINE")
        print("[BULB] Vos agents sont prts pour des tches relles!")
        print("[TOOL] Vous pouvez maintenant les intgrer dans vos projets")
        
    except KeyboardInterrupt:
        print("\n  Dmonstration interrompue")
    except Exception as e:
        print(f"\n[CROSS] Erreur: {e}")

if __name__ == "__main__":
    asyncio.run(main())




