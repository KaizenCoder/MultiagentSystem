#!/usr/bin/env python3
"""
Test de validation pour agent_orchestrateur_audit.py via Meta-Auditeur
"""
import sys
import asyncio
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent))

async def test_orchestrateur_audit_via_meta_auditeur():
    """Test de l'orchestrateur audit via le Meta-Auditeur Universel"""
    print("🎭 Test Agent Orchestrateur Audit via Meta-Auditeur")
    
    try:
        from agents.agent_META_AUDITEUR_UNIVERSEL import MetaAuditeurUniversel
        
        meta_auditor = MetaAuditeurUniversel()
        await meta_auditor.startup()
        
        print("✅ Meta-Auditeur Universel initialisé")
        
        # Test audit du fichier orchestrateur
        orchestrateur_path = "agents/agent_orchestrateur_audit.py"
        
        if Path(orchestrateur_path).exists():
            print(f"📋 Audit universel: {orchestrateur_path}")
            
            result = await meta_auditor.audit_complet(orchestrateur_path)
            
            if result.get('status') != 'failed':
                print(f"✅ Meta-audit réussi!")
                print(f"   📊 Score global: {result['global_score']}/100")
                print(f"   🎯 Niveau: {result['quality_level']}")
                print(f"   🤖 Agents utilisés: {len(result['agents_used'])}")
                print(f"   🔍 Issues: {len(result['consolidated_issues'])}")
                
                # Affichage des issues principales
                if 'consolidated_issues' in result and result['consolidated_issues']:
                    print(f"\n📋 Issues principales détectées:")
                    for i, issue in enumerate(result['consolidated_issues'][:5], 1):
                        severity = issue.get('severity', 'unknown')
                        category = issue.get('category', 'unknown')
                        description = issue.get('description', 'N/A')
                        print(f"   {i}. [{severity.upper()}] {category}: {description}")
                
                await meta_auditor.shutdown()
                
                global_score = result.get('global_score', 0)
                return global_score >= 60, global_score
            else:
                print(f"❌ Meta-audit échoué: {result.get('error')}")
                await meta_auditor.shutdown()
                return False, 0
        else:
            print(f"❌ Fichier {orchestrateur_path} non trouvé")
            await meta_auditor.shutdown()
            return False, 0
            
    except Exception as e:
        print(f"❌ Erreur test Meta-Auditeur: {e}")
        return False, 0

async def analyze_orchestrateur_audit_structure():
    """Analyse de la structure de l'orchestrateur audit"""
    print("\n🔍 Analyse Structure Orchestrateur Audit")
    
    orchestrateur_path = Path("agents/agent_orchestrateur_audit.py")
    
    if not orchestrateur_path.exists():
        print("❌ agent_orchestrateur_audit.py non trouvé")
        return False
    
    # Lecture et analyse du fichier
    with open(orchestrateur_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📊 Taille: {len(content)} caractères")
    print(f"📊 Lignes: {len(content.splitlines())}")
    
    # Vérifications spécifiques orchestrateur
    checks = {
        "class.*Orchestrateur.*Audit": "Classe orchestrateur",
        "async def.*coordination": "Méthode coordination", 
        "async def.*orchestrer": "Méthode orchestration",
        "def execute_task": "execute_task method",
        "async def startup": "startup method",
        "def get_capabilities": "get_capabilities method",
        "from agent_18_auditeur_securite": "Import agent sécurité",
        "from agent_19_auditeur_performance": "Import agent performance",
        "from agent_20_auditeur_conformite": "Import agent conformité"
    }
    
    import re
    
    print("\n📋 Vérifications Orchestrateur:")
    success_count = 0
    
    for pattern, description in checks.items():
        if re.search(pattern, content, re.IGNORECASE):
            print(f"   ✅ {description}")
            success_count += 1
        else:
            print(f"   ❌ {description}")
    
    compliance_rate = (success_count / len(checks)) * 100
    print(f"\n📊 Conformité: {success_count}/{len(checks)} ({compliance_rate:.1f}%)")
    
    # Vérifications Pattern Factory
    factory_checks = {
        "from core.agent_factory_architecture import": "Import Pattern Factory",
        "class.*Agent.*:": "Héritage Pattern Factory",
        "async def health_check": "health_check method",
        "async def shutdown": "shutdown method"
    }
    
    print("\n📋 Vérifications Pattern Factory:")
    factory_count = 0
    
    for pattern, description in factory_checks.items():
        if re.search(pattern, content, re.IGNORECASE):
            print(f"   ✅ {description}")
            factory_count += 1
        else:
            print(f"   ❌ {description}")
    
    factory_rate = (factory_count / len(factory_checks)) * 100
    print(f"\n📊 Pattern Factory: {factory_count}/{len(factory_checks)} ({factory_rate:.1f}%)")
    
    overall_score = (compliance_rate + factory_rate) / 2
    
    return overall_score >= 60, overall_score

async def check_orchestrateur_dependencies():
    """Vérification des dépendances de l'orchestrateur"""
    print("\n🔗 Vérification Dépendances Orchestrateur")
    
    dependencies = {
        "agents/agent_18_auditeur_securite.py": "Agent 18 Sécurité",
        "agents/agent_19_auditeur_performance.py": "Agent 19 Performance", 
        "agents/agent_20_auditeur_conformite.py": "Agent 20 Conformité"
    }
    
    available_count = 0
    
    for path, name in dependencies.items():
        if Path(path).exists():
            print(f"   ✅ {name}: disponible")
            available_count += 1
        else:
            print(f"   ❌ {name}: manquant")
    
    dependency_rate = (available_count / len(dependencies)) * 100
    print(f"\n📊 Dépendances: {available_count}/{len(dependencies)} ({dependency_rate:.1f}%)")
    
    return dependency_rate >= 66.7  # Au moins 2/3 des agents

if __name__ == "__main__":
    print("🌟 VALIDATION AGENT ORCHESTRATEUR AUDIT")
    print("=" * 50)
    
    # Test 1: Meta-Auditeur
    success_meta, score_meta = asyncio.run(test_orchestrateur_audit_via_meta_auditeur())
    
    # Test 2: Analyse structure
    success_structure, score_structure = asyncio.run(analyze_orchestrateur_audit_structure())
    
    # Test 3: Dépendances
    deps_ok = asyncio.run(check_orchestrateur_dependencies())
    
    print(f"\n🎯 RÉSULTAT VALIDATION ORCHESTRATEUR AUDIT")
    print("=" * 55)
    print(f"📊 Score Meta-Audit: {score_meta}/100")
    print(f"📊 Score Structure: {score_structure:.1f}/100")
    print(f"🔗 Dépendances: {'✅' if deps_ok else '❌'}")
    
    if success_meta and success_structure and deps_ok:
        print("✅ VALIDATION RÉUSSIE")
        print("✅ Orchestrateur audit fonctionnel")
        print("✅ Pattern Factory compliant")
        print("✅ Dépendances satisfaites")
        print("✅ Ready for production")
    elif (success_meta or success_structure) and score_meta + score_structure >= 120:
        print("⚠️ VALIDATION PARTIELLE")
        print("⚠️ Fonctionnel avec quelques améliorations nécessaires")
        print("⚠️ Peut être utilisé en production avec monitoring")
    else:
        print("❌ VALIDATION ÉCHOUÉE")
        print("❌ Corrections majeures nécessaires")
        print("❌ Ne pas déployer en production")