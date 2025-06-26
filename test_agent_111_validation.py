#!/usr/bin/env python3
"""
Test de validation pour agent_111_auditeur_qualite.py via Meta-Auditeur
"""
import sys
import asyncio
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent))

async def test_agent_111_via_meta_auditeur():
    """Test de l'agent 111 via le Meta-Auditeur Universel"""
    print("🔍 Test Agent 111 - Auditeur Qualité via Meta-Auditeur")
    
    try:
        from agents.agent_META_AUDITEUR_UNIVERSEL import MetaAuditeurUniversel
        
        meta_auditor = MetaAuditeurUniversel()
        await meta_auditor.startup()
        
        print("✅ Meta-Auditeur Universel initialisé")
        
        # Test audit du fichier agent 111
        agent_111_path = "agents/agent_111_auditeur_qualite.py"
        
        if Path(agent_111_path).exists():
            print(f"📋 Audit universel: {agent_111_path}")
            
            result = await meta_auditor.audit_complet(agent_111_path)
            
            if result.get('status') != 'failed':
                print(f"✅ Meta-audit réussi!")
                print(f"   📊 Score global: {result['global_score']}/100")
                print(f"   🎯 Niveau: {result['quality_level']}")
                print(f"   🤖 Agents utilisés: {len(result['agents_used'])}")
                print(f"   🔍 Issues: {len(result['consolidated_issues'])}")
                
                await meta_auditor.shutdown()
                
                global_score = result.get('global_score', 0)
                return global_score >= 60, global_score
            else:
                print(f"❌ Meta-audit échoué: {result.get('error')}")
                await meta_auditor.shutdown()
                return False, 0
        else:
            print(f"❌ Fichier {agent_111_path} non trouvé")
            await meta_auditor.shutdown()
            return False, 0
            
    except Exception as e:
        print(f"❌ Erreur test Meta-Auditeur: {e}")
        return False, 0

async def compare_agent_111_versions():
    """Compare les deux versions d'agent 111"""
    print("\n🔍 Comparaison Agents 111")
    
    agent_111_base = Path("agents/agent_111_auditeur_qualite.py")
    agent_111_sprint3 = Path("agents/agent_111_auditeur_qualite_sprint3.py")
    
    if not agent_111_base.exists():
        print("❌ agent_111_auditeur_qualite.py non trouvé")
        return False
    
    if not agent_111_sprint3.exists():
        print("❌ agent_111_auditeur_qualite_sprint3.py non trouvé")
        return False
    
    # Lecture des deux fichiers
    with open(agent_111_base, 'r', encoding='utf-8') as f:
        content_base = f.read()
    
    with open(agent_111_sprint3, 'r', encoding='utf-8') as f:
        content_sprint3 = f.read()
    
    print(f"📊 Taille agent_111_base: {len(content_base)} caractères")
    print(f"📊 Taille agent_111_sprint3: {len(content_sprint3)} caractères")
    
    # Vérifications spécifiques
    checks_base = {
        "class Agent111AuditeurQualite(Agent)": "Pattern Factory inheritance",
        "def execute_task(": "execute_task method",
        "async def startup(": "startup method",
        "def get_capabilities(": "get_capabilities method",
        "audit_universel": "Audit universel capability"
    }
    
    checks_sprint3 = {
        "class Agent111AuditeurQualiteSprint3(Agent)": "Pattern Factory inheritance", 
        "def execute_task(": "execute_task method",
        "async def startup(": "startup method",
        "def get_capabilities(": "get_capabilities method",
        "audit_universel": "Audit universel capability"
    }
    
    print("\n📋 Agent 111 Base:")
    base_score = 0
    for pattern, description in checks_base.items():
        if pattern in content_base:
            print(f"   ✅ {description}")
            base_score += 1
        else:
            print(f"   ❌ {description}")
    
    print("\n📋 Agent 111 Sprint3:")
    sprint3_score = 0
    for pattern, description in checks_sprint3.items():
        if pattern in content_sprint3:
            print(f"   ✅ {description}")
            sprint3_score += 1
        else:
            print(f"   ❌ {description}")
    
    print(f"\n📊 Scores:")
    print(f"   Base: {base_score}/{len(checks_base)}")
    print(f"   Sprint3: {sprint3_score}/{len(checks_sprint3)}")
    
    # Recommandation
    if sprint3_score > base_score:
        print("🎯 RECOMMANDATION: Utiliser agent_111_auditeur_qualite_sprint3.py")
        return True
    else:
        print("🎯 RECOMMANDATION: Améliorer agent_111_auditeur_qualite.py")
        return False

if __name__ == "__main__":
    print("🌟 ANALYSE AGENT 111 - AUDITEUR QUALITÉ")
    print("=" * 50)
    
    # Test 1: Meta-Auditeur sur version base
    success_base, score_base = asyncio.run(test_agent_111_via_meta_auditeur())
    
    # Test 2: Comparaison versions
    sprint3_better = asyncio.run(compare_agent_111_versions())
    
    print(f"\n🎯 RÉSULTAT ANALYSE AGENT 111")
    print("=" * 40)
    print(f"📊 Score Meta-Audit base: {score_base}/100")
    print(f"🔄 Sprint3 supérieur: {'✅' if sprint3_better else '❌'}")
    
    if sprint3_better:
        print("✅ RECOMMANDATION: Agent 111 Sprint3 déjà optimisé")
        print("✅ Capacité audit universel déjà implémentée")
        print("✅ Passer au prochain agent PHASE 2")
    elif success_base and score_base >= 70:
        print("✅ Agent 111 base fonctionnel")
        print("⚠️ Améliorations possibles avec version Sprint3")
    else:
        print("❌ Agent 111 base nécessite des améliorations")
        print("📋 Considérer migration vers Sprint3")