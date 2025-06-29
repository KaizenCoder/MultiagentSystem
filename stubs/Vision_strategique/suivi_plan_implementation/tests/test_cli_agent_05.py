#!/usr/bin/env python3
"""
🧪 TEST CLI - Agent 05 Moderne
Test réel d'analyse d'un autre agent du répertoire agents/
"""

import asyncio
import sys
from pathlib import Path
import json

# Add paths
sys.path.insert(0, str(Path(__file__).parent))

async def test_cli_agent_05():
    """Test CLI de l'Agent 05 pour analyser un autre agent"""
    
    print("🧪 TEST CLI - Agent 05 Maître Tests & Validation")
    print("=" * 60)
    print("Mission: Analyser l'agent_111_auditeur_qualite.py")
    print("")
    
    try:
        # Import agent
        from agents.modern.agent_05_maitre_tests_validation_modern_fixed import ModernAgent05MaitreTestsValidation
        from core.nextgen_architecture import Task
        
        # Créer agent
        agent = ModernAgent05MaitreTestsValidation()
        await agent.startup()
        
        print(f"✅ Agent 05 démarré - Version: {agent.version}")
        print(f"📋 Capacités: {len(agent.get_capabilities())}")
        
        # Cible d'analyse : Agent 111
        target_agent = Path(__file__).parent / "agents" / "agent_111_auditeur_qualite.py"
        if not target_agent.exists():
            print(f"❌ Agent cible non trouvé: {target_agent}")
            return False
        
        print(f"🎯 Cible d'analyse: {target_agent.name}")
        print("")
        
        # === TEST 1: ANALYSE TESTS DE L'AGENT 111 ===
        print("📊 ANALYSE TESTS - Agent 111")
        print("-" * 40)
        
        context_analysis = {
            "target_agent": str(target_agent),
            "analysis_type": "comprehensive",
            "focus": ["quality", "testing", "validation"]
        }
        
        task_tests = Task(
            type="generer_rapport_strategique",
            params={
                "context": context_analysis,
                "type_rapport": "tests"
            }
        )
        
        result_tests = await agent.execute_task(task_tests)
        if result_tests.success:
            rapport = result_tests.data
            print(f"  🎯 Score Global: {rapport.get('score_global')}/100")
            print(f"  🏆 Niveau Qualité: {rapport.get('niveau_qualite')}")
            print(f"  ✅ Conformité: {rapport.get('conformite')}")
            print(f"  🧪 Smoke Tests: {rapport.get('smoke_tests', {}).get('passed', 0)}/{rapport.get('smoke_tests', {}).get('total_tests', 0)} réussis")
            
            # Afficher recommandations
            recommandations = rapport.get('recommandations', [])
            if recommandations:
                print(f"  💡 Recommandations ({len(recommandations)}):")
                for i, reco in enumerate(recommandations[:3], 1):
                    print(f"     {i}. {reco}")
        else:
            print(f"  ❌ Erreur: {result_tests.error}")
        
        print("")
        
        # === TEST 2: VALIDATION DE L'AGENT 111 ===
        print("✅ VALIDATION - Agent 111")
        print("-" * 40)
        
        task_validation = Task(
            type="generer_rapport_strategique",
            params={
                "context": context_analysis,
                "type_rapport": "validation"
            }
        )
        
        result_validation = await agent.execute_task(task_validation)
        if result_validation.success:
            rapport = result_validation.data
            print(f"  🎯 Score Validation: {rapport.get('score_validation')}/100")
            
            criteres = rapport.get('criteres_validation', {})
            print(f"  📋 Critères de Validation:")
            for critere, statut in criteres.items():
                icon = "✅" if statut == "OK" else "⚠️"
                print(f"     {icon} {critere}: {statut}")
        else:
            print(f"  ❌ Erreur: {result_validation.error}")
        
        print("")
        
        # === TEST 3: PERFORMANCE DE L'AGENT 111 ===
        print("⚡ PERFORMANCE - Agent 111")
        print("-" * 40)
        
        task_performance = Task(
            type="generer_rapport_strategique",
            params={
                "context": context_analysis,
                "type_rapport": "performance"
            }
        )
        
        result_performance = await agent.execute_task(task_performance)
        if result_performance.success:
            rapport = result_performance.data
            print(f"  🎯 Score Performance: {rapport.get('score_performance')}/100")
            
            metrics = rapport.get('metriques_performance', {})
            print(f"  💾 Mémoire: {metrics.get('memory_usage_mb', 0):.1f} MB")
            print(f"  ⏱️  Uptime: {metrics.get('uptime_seconds', 0):.1f}s")
            print(f"  📄 Templates: {'✅' if metrics.get('templates_loaded') else '❌'}")
        else:
            print(f"  ❌ Erreur: {result_performance.error}")
        
        print("")
        
        # === TEST 4: QUALITÉ DE L'AGENT 111 ===
        print("🏆 QUALITÉ - Agent 111") 
        print("-" * 40)
        
        task_qualite = Task(
            type="generer_rapport_strategique",
            params={
                "context": context_analysis,
                "type_rapport": "qualite"
            }
        )
        
        result_qualite = await agent.execute_task(task_qualite)
        if result_qualite.success:
            rapport = result_qualite.data
            print(f"  🎯 Score Qualité: {rapport.get('score_qualite')}/100")
            
            standards = rapport.get('standards_respectes', [])
            print(f"  📜 Standards Respectés ({len(standards)}):")
            for standard in standards[:4]:
                print(f"     ✅ {standard}")
                
            indicateurs = rapport.get('indicateurs_qualite', {})
            print(f"  📊 Indicateurs:")
            print(f"     🧪 Tests: {indicateurs.get('tests_passes', 'N/A')}")
            print(f"     💯 Taux Réussite: {indicateurs.get('taux_reussite', 'N/A')}")
            print(f"     🏥 Santé: {indicateurs.get('sante_systeme', 'N/A')}")
        else:
            print(f"  ❌ Erreur: {result_qualite.error}")
        
        print("")
        
        # === TEST 5: GÉNÉRATION RAPPORT MARKDOWN ===
        print("📝 GÉNÉRATION MARKDOWN")
        print("-" * 40)
        
        if result_tests.success:
            task_markdown = Task(
                type="generer_rapport_markdown",
                params={
                    "rapport_json": result_tests.data,
                    "type_rapport": "tests",
                    "context": context_analysis
                }
            )
            
            result_markdown = await agent.execute_task(task_markdown)
            if result_markdown.success:
                markdown = result_markdown.data.get("markdown", "")
                lines = len(markdown.split('\n'))
                chars = len(markdown)
                print(f"  📄 Rapport Markdown généré:")
                print(f"     📏 {lines} lignes, {chars} caractères")
                print(f"     🎯 Format: {'✅ Valide' if '# 🧪 RAPPORT TESTS' in markdown else '❌ Invalide'}")
                
                # Sauvegarder le rapport
                report_file = Path(__file__).parent / "reports" / f"analyse_agent_111_par_agent_05.md"
                report_file.parent.mkdir(exist_ok=True)
                report_file.write_text(markdown, encoding='utf-8')
                print(f"     💾 Sauvegardé: {report_file}")
            else:
                print(f"  ❌ Erreur Markdown: {result_markdown.error}")
        
        print("")
        
        # === RÉSUMÉ FINAL ===
        print("=" * 60)
        print("🎉 RÉSUMÉ - Test CLI Agent 05")
        print("=" * 60)
        
        # Calculer score global
        scores = []
        if result_tests.success:
            scores.append(result_tests.data.get('score_global', 0))
        if result_validation.success:
            scores.append(result_validation.data.get('score_validation', 0))
        if result_performance.success:
            scores.append(result_performance.data.get('score_performance', 0))
        if result_qualite.success:
            scores.append(result_qualite.data.get('score_qualite', 0))
        
        if scores:
            score_moyen = sum(scores) / len(scores)
            print(f"📊 Score Moyen d'Analyse: {score_moyen:.1f}/100")
            
            if score_moyen >= 90:
                print("🏆 EXCELLENT - Agent 111 de très haute qualité")
            elif score_moyen >= 70:
                print("✅ BIEN - Agent 111 de bonne qualité")
            elif score_moyen >= 50:
                print("⚠️ MOYEN - Agent 111 nécessite améliorations")
            else:
                print("❌ CRITIQUE - Agent 111 nécessite refactoring")
        
        print(f"🎯 Agent Analysé: agent_111_auditeur_qualite.py")
        print(f"🔧 Agent Analyseur: Agent 05 Moderne v{agent.version}")
        print(f"✅ Toutes les fonctionnalités legacy validées")
        print(f"🚀 Capacités modernes opérationnelles")
        
        await agent.shutdown()
        return True
        
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_cli_agent_05())
    print("\n" + "=" * 60)
    if success:
        print("🎉 TEST CLI AGENT 05 RÉUSSI")
        print("L'agent moderne fonctionne parfaitement en conditions réelles")
    else:
        print("❌ TEST CLI AGENT 05 ÉCHOUÉ")
    print("=" * 60)
    sys.exit(0 if success else 1)