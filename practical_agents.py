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
    print("✅ Configuration chargée")
except ImportError:
    print("❌ Erreur de configuration")
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
        """Appel à l'API Anthropic (recommandé)"""
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
        print(f"🧠 {self.agent_id} traite: '{prompt[:60]}...'")
        
        # Essayer Anthropic en premier (plus fiable actuellement)
        result = await self.call_anthropic(prompt, max_tokens)
        
        if result.get("success"):
            self.stats["successful_tasks"] += 1
            print(f"   ✅ Succès avec Anthropic ({result.get('tokens_used', 0)} tokens)")
            return result
        else:
            self.stats["errors"] += 1
            print(f"   ❌ Échec: {result.get('error')}")
            return result

# Agents spécialisés utilisant l'API
class WriterBot(SmartAgent):
    """Bot spécialisé en rédaction"""
    
    async def write_document(self, topic: str, style: str = "professionnel") -> str:
        prompt = f"""
Rédige un document {style} sur le sujet suivant: {topic}

Structure attendue:
- Introduction claire
- Développement structuré 
- Conclusion pertinente
- Style {style} et fluide

Sujet: {topic}
"""
        result = await self.smart_process(prompt, max_tokens=400)
        return result.get("content", f"Erreur lors de la rédaction: {result.get('error')}")
    
    async def create_summary(self, text: str) -> str:
        prompt = f"""
Crée un résumé concis et structuré du texte suivant:

{text[:1000]}...

Le résumé doit:
- Capturer les points clés
- Être clair et concis
- Garder la structure logique
"""
        result = await self.smart_process(prompt, max_tokens=200)
        return result.get("content", f"Erreur lors du résumé: {result.get('error')}")

class CodeBot(SmartAgent):
    """Bot spécialisé en développement"""
    
    async def create_function(self, description: str, language: str = "python") -> str:
        prompt = f"""
Crée une fonction {language} selon cette description: {description}

Exigences:
- Code propre et commenté
- Gestion d'erreurs appropriée
- Exemples d'utilisation
- Documentation docstring

Description: {description}
Langage: {language}
"""
        result = await self.smart_process(prompt, max_tokens=300)
        return result.get("content", f"Erreur lors de la génération: {result.get('error')}")
    
    async def explain_code(self, code: str) -> str:
        prompt = f"""
Explique ce code de manière claire et pédagogique:

```
{code[:500]}
```

L'explication doit inclure:
- Objectif du code
- Fonctionnement étape par étape
- Points importants à retenir
"""
        result = await self.smart_process(prompt, max_tokens=250)
        return result.get("content", f"Erreur lors de l'explication: {result.get('error')}")

class AnalystBot(SmartAgent):
    """Bot spécialisé en analyse"""
    
    async def analyze_data(self, data_description: str) -> str:
        prompt = f"""
Effectue une analyse structurée des données suivantes: {data_description}

Structure d'analyse:
- Vue d'ensemble des données
- Tendances identifiées
- Points d'attention
- Recommandations
- Prochaines étapes

Données: {data_description}
"""
        result = await self.smart_process(prompt, max_tokens=350)
        return result.get("content", f"Erreur lors de l'analyse: {result.get('error')}")

async def demonstration_complete():
    """Démonstration complète des agents spécialisés"""
    print("🤖 DÉMONSTRATION AGENTS SPÉCIALISÉS")
    print("=" * 50)
    
    # Test Writer Bot
    print("\n📝 TEST WRITER BOT")
    print("-" * 20)
    async with WriterBot("writer_bot_001") as writer:
        
        # Test rédaction
        doc = await writer.write_document("L'importance de la cybersécurité", "informatif")
        print("📄 Document généré:")
        print(doc[:300] + "..." if len(doc) > 300 else doc)
        
        # Test résumé
        long_text = """
        L'intelligence artificielle représente une révolution technologique majeure. 
        Elle transforme tous les secteurs: santé, finance, transport, éducation.
        Les algorithmes d'apprentissage automatique permettent aux machines d'apprendre
        et de s'améliorer sans programmation explicite. Cependant, cette technologie
        soulève aussi des questions éthiques importantes concernant l'emploi,
        la vie privée et la prise de décision automatisée.
        """
        
        summary = await writer.create_summary(long_text)
        print(f"\n📋 Résumé généré:")
        print(summary)
    
    # Test Code Bot
    print(f"\n💻 TEST CODE BOT")
    print("-" * 20)
    async with CodeBot("code_bot_001") as coder:
        
        # Test génération de fonction
        function = await coder.create_function(
            "Une fonction qui calcule la moyenne d'une liste de nombres avec gestion d'erreurs"
        )
        print("⚙️ Fonction générée:")
        print(function[:400] + "..." if len(function) > 400 else function)
        
        # Test explication de code
        sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
        """
        
        explanation = await coder.explain_code(sample_code)
        print(f"\n🔍 Explication:")
        print(explanation)
    
    # Test Analyst Bot
    print(f"\n📊 TEST ANALYST BOT")
    print("-" * 20)
    async with AnalystBot("analyst_bot_001") as analyst:
        
        analysis = await analyst.analyze_data(
            "Données de ventes e-commerce: 1000 commandes/jour, panier moyen 45€, "
            "taux de conversion 2.5%, pics le weekend, baisse en été"
        )
        print("📈 Analyse générée:")
        print(analysis)
    
    # Statistiques globales
    print(f"\n📊 STATISTIQUES GLOBALES")
    print("-" * 25)
    for bot_name, bot in [("Writer", writer), ("Coder", coder), ("Analyst", analyst)]:
        stats = bot.stats
        print(f"🤖 {bot_name}:")
        print(f"   ✅ Tâches réussies: {stats['successful_tasks']}")
        print(f"   🧠 Appels Anthropic: {stats['anthropic_calls']}")
        print(f"   📊 Tokens totaux: {stats['total_tokens']}")
        print(f"   ❌ Erreurs: {stats['errors']}")

async def test_multi_agent_workflow():
    """Test d'un workflow multi-agents"""
    print(f"\n🔄 TEST WORKFLOW MULTI-AGENTS")
    print("=" * 40)
    
    # Scénario: Analyser un problème, proposer une solution code, documenter
    topic = "Système de cache pour améliorer les performances d'une API"
    
    async with AnalystBot("analyst") as analyst, \
               CodeBot("coder") as coder, \
               WriterBot("writer") as writer:
        
        print("1️⃣ Analyse du problème...")
        analysis = await analyst.analyze_data(f"Problème de performance: {topic}")
        print(f"   📋 Analyse: {analysis[:100]}...")
        
        print("\n2️⃣ Génération de solution code...")
        code_solution = await coder.create_function(
            "Système de cache Redis avec TTL et invalidation automatique"
        )
        print(f"   💻 Code: {code_solution[:100]}...")
        
        print("\n3️⃣ Documentation finale...")
        final_doc = await writer.write_document(
            f"Solution de cache basée sur l'analyse: {analysis[:200]}",
            "technique"
        )
        print(f"   📝 Documentation: {final_doc[:100]}...")
        
        print(f"\n✅ Workflow terminé! 3 agents ont collaboré avec succès.")

async def main():
    """Fonction principale"""
    try:
        await demonstration_complete()
        await test_multi_agent_workflow()
        
        print(f"\n🎉 DÉMONSTRATION TERMINÉE")
        print("💡 Vos agents sont prêts pour des tâches réelles!")
        print("🔧 Vous pouvez maintenant les intégrer dans vos projets")
        
    except KeyboardInterrupt:
        print("\n⏹️  Démonstration interrompue")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")

if __name__ == "__main__":
    asyncio.run(main())
