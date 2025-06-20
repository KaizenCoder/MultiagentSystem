#!/usr/bin/env python3
"""
Test de Diagnostic des Agents - Agent Factory Implementation
Analyse complète des agents présents dans C:\Dev\nextgeneration\agent_factory_implementation
MODE DIAGNOSTIC UNIQUEMENT - AUCUNE MODIFICATION AUTORISÉE
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime
import json

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent))

from maintenance_template_manager import MaintenanceTemplateManager

async def test_diagnostic_agents_factory():
    """Test de diagnostic complet des agents dans agent_factory_implementation"""
    print("🔍 DIAGNOSTIC AGENTS - AGENT FACTORY IMPLEMENTATION")
    print("=" * 70)
    print("📋 MODE: DIAGNOSTIC UNIQUEMENT - AUCUNE MODIFICATION")
    print("=" * 70)
    
    # Chemin cible
    target_path = Path(r"C:\Dev\nextgeneration\agent_factory_implementation")
    agents_path = target_path / "agents"
    workspace_path = Path(__file__).parent
    
    # Vérifier l'existence du répertoire
    if not target_path.exists():
        print(f"❌ ERREUR: Répertoire non trouvé: {target_path}")
        return False
    
    if not agents_path.exists():
        print(f"❌ ERREUR: Répertoire agents non trouvé: {agents_path}")
        return False
    
    print(f"📁 Répertoire cible: {target_path}")
    print(f"🤖 Répertoire agents: {agents_path}")
    print(f"💼 Workspace: {workspace_path}")
    
    try:
        # Initialiser le TemplateManager
        print("\n🏭 Initialisation du TemplateManager...")
        template_manager = MaintenanceTemplateManager()
        await template_manager.startup()
        
        # Configuration pour le diagnostic
        config_diagnostic = {
            "workspace_path": str(workspace_path),
            "target_path": str(agents_path),
            "mode": "diagnostic_only",
            "source_path": str(agents_path),
            "safe_mode": True,
            "rapport_detaille": True
        }
        
        print(f"⚙️ Configuration diagnostic: {config_diagnostic['mode']}")
        
        # Résultats globaux du diagnostic
        diagnostic_global = {
            "timestamp": datetime.now().isoformat(),
            "target_path": str(target_path),
            "agents_path": str(agents_path),
            "mode": "diagnostic_only",
            "etapes": {},
            "resultats_consolides": {},
            "recommandations": [],
            "status": "en_cours"
        }
        
        # ÉTAPE 1: Analyse Structure
        print("\n" + "="*50)
        print("📊 ÉTAPE 1/6: ANALYSE STRUCTURE")
        print("="*50)
        
        try:
            agent_1 = await template_manager.create_agent("agent_1_analyseur_structure", config_diagnostic)
            await agent_1.startup()
            
            print("🔍 Analyse de la structure des agents...")
            resultat_analyse = await agent_1.analyser_structure()
            
            diagnostic_global["etapes"]["analyse_structure"] = {
                "status": "complete",
                "agent_id": agent_1.agent_id,
                "resultats": resultat_analyse,
                "timestamp": datetime.now().isoformat()
            }
            
            # Affichage des résultats d'analyse
            if resultat_analyse:
                print(f"✅ Analyse terminée:")
                print(f"   📁 Agents analysés: {resultat_analyse.get('nombre_agents_analyses', 0)}")
                print(f"   📄 Fichiers trouvés: {len(resultat_analyse.get('agents_detectes', []))}")
                print(f"   ⚠️  Problèmes détectés: {len(resultat_analyse.get('problemes_detectes', []))}")
                
                # Détails des agents trouvés
                agents_detectes = resultat_analyse.get('agents_detectes', [])
                if agents_detectes:
                    print(f"\n📋 AGENTS DÉTECTÉS ({len(agents_detectes)}):")
                    for i, agent in enumerate(agents_detectes[:10], 1):  # Limiter à 10 pour l'affichage
                        nom = agent.get('nom', 'Inconnu')
                        taille = agent.get('taille_lignes', 0)
                        print(f"   {i:2d}. {nom} ({taille} lignes)")
                    if len(agents_detectes) > 10:
                        print(f"   ... et {len(agents_detectes) - 10} autres agents")
                
                # Problèmes détectés
                problemes = resultat_analyse.get('problemes_detectes', [])
                if problemes:
                    print(f"\n⚠️  PROBLÈMES DÉTECTÉS ({len(problemes)}):")
                    for i, probleme in enumerate(problemes[:5], 1):  # Limiter à 5 pour l'affichage
                        print(f"   {i}. {probleme}")
                    if len(problemes) > 5:
                        print(f"   ... et {len(problemes) - 5} autres problèmes")
            
            await agent_1.shutdown()
            
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse structure: {e}")
            diagnostic_global["etapes"]["analyse_structure"] = {
                "status": "erreur",
                "erreur": str(e),
                "timestamp": datetime.now().isoformat()
            }
        
        # ÉTAPE 2: Évaluation Utilité
        print("\n" + "="*50)
        print("🎯 ÉTAPE 2/6: ÉVALUATION UTILITÉ")
        print("="*50)
        
        try:
            # Récupérer les résultats de l'analyse pour l'évaluation
            analyse_structure = diagnostic_global["etapes"].get("analyse_structure", {}).get("resultats", {})
            
            config_evaluation = config_diagnostic.copy()
            config_evaluation.update({
                "analyse_structure": analyse_structure
            })
            
            agent_2 = await template_manager.create_agent("agent_2_evaluateur_utilite", config_evaluation)
            await agent_2.startup()
            
            print("🎯 Évaluation de l'utilité des agents...")
            resultat_evaluation = await agent_2.evaluer_utilite()
            
            diagnostic_global["etapes"]["evaluation_utilite"] = {
                "status": "complete",
                "agent_id": agent_2.agent_id,
                "resultats": resultat_evaluation,
                "timestamp": datetime.now().isoformat()
            }
            
            # Affichage des résultats d'évaluation
            if resultat_evaluation:
                print(f"✅ Évaluation terminée:")
                print(f"   ✅ Agents utiles: {len(resultat_evaluation.get('outils_utiles', []))}")
                print(f"   ⚠️  Agents problématiques: {len(resultat_evaluation.get('outils_problematiques', []))}")
                print(f"   📊 Score moyen: {resultat_evaluation.get('score_moyen_utilite', 0):.1f}/10")
                
                # Agents les plus utiles
                outils_utiles = resultat_evaluation.get('outils_utiles', [])
                if outils_utiles:
                    print(f"\n🏆 TOP AGENTS UTILES:")
                    for i, agent in enumerate(outils_utiles[:5], 1):
                        nom = agent.get('nom', 'Inconnu')
                        score = agent.get('score_utilite', 0)
                        print(f"   {i}. {nom} (Score: {score}/10)")
                
                # Agents problématiques
                outils_problematiques = resultat_evaluation.get('outils_problematiques', [])
                if outils_problematiques:
                    print(f"\n⚠️  AGENTS PROBLÉMATIQUES:")
                    for i, agent in enumerate(outils_problematiques[:5], 1):
                        nom = agent.get('nom', 'Inconnu')
                        raison = agent.get('raison', 'Non spécifiée')
                        print(f"   {i}. {nom} - {raison}")
            
            await agent_2.shutdown()
            
        except Exception as e:
            print(f"❌ Erreur lors de l'évaluation utilité: {e}")
            diagnostic_global["etapes"]["evaluation_utilite"] = {
                "status": "erreur",
                "erreur": str(e),
                "timestamp": datetime.now().isoformat()
            }
        
        # ÉTAPE 3: Test Anti-Faux Agents (Agent 4)
        print("\n" + "="*50)
        print("🧪 ÉTAPE 3/6: DÉTECTION FAUX AGENTS")
        print("="*50)
        
        try:
            # Simuler des outils adaptés pour le testeur
            outils_adaptes = []
            if "evaluation_utilite" in diagnostic_global["etapes"]:
                evaluation_results = diagnostic_global["etapes"]["evaluation_utilite"].get("resultats", {})
                outils_adaptes = evaluation_results.get('outils_utiles', [])
            
            config_test = config_diagnostic.copy()
            config_test.update({
                "outils_adaptes": outils_adaptes
            })
            
            agent_4 = await template_manager.create_agent("agent_4_testeur_integration", config_test)
            await agent_4.startup()
            
            print("🔍 Détection des faux agents...")
            resultat_tests = await agent_4.tester_integration()
            
            diagnostic_global["etapes"]["detection_faux_agents"] = {
                "status": "complete",
                "agent_id": agent_4.agent_id,
                "resultats": resultat_tests,
                "timestamp": datetime.now().isoformat()
            }
            
            # Affichage des résultats de détection
            if resultat_tests:
                print(f"✅ Tests terminés:")
                stats = resultat_tests.get('statistiques', {})
                print(f"   🧪 Tests exécutés: {stats.get('nombre_tests_executes', 0)}")
                print(f"   ✅ Tests réussis: {stats.get('tests_passes', 0)}")
                print(f"   ❌ Tests échoués: {stats.get('tests_echecs', 0)}")
                print(f"   📊 Taux de succès: {stats.get('taux_succes', 0):.1f}%")
                
                # Problèmes détectés
                problemes_tests = resultat_tests.get('problemes_detectes', [])
                if problemes_tests:
                    print(f"\n⚠️  PROBLÈMES DÉTECTÉS LORS DES TESTS:")
                    for i, probleme in enumerate(problemes_tests[:5], 1):
                        print(f"   {i}. {probleme}")
                    if len(problemes_tests) > 5:
                        print(f"   ... et {len(problemes_tests) - 5} autres problèmes")
            
            await agent_4.shutdown()
            
        except Exception as e:
            print(f"❌ Erreur lors de la détection faux agents: {e}")
            diagnostic_global["etapes"]["detection_faux_agents"] = {
                "status": "erreur", 
                "erreur": str(e),
                "timestamp": datetime.now().isoformat()
            }
        
        # ÉTAPE 4: Documentation des Résultats
        print("\n" + "="*50)
        print("📚 ÉTAPE 4/6: DOCUMENTATION DIAGNOSTIC")
        print("="*50)
        
        try:
            # Préparer les résultats pour la documentation
            resultats_pour_doc = {}
            for etape, donnees in diagnostic_global["etapes"].items():
                if donnees.get("status") == "complete":
                    resultats_pour_doc[etape] = donnees["resultats"]
            
            config_doc = config_diagnostic.copy()
            config_doc.update({
                "resultats_tests": resultats_pour_doc
            })
            
            agent_5 = await template_manager.create_agent("agent_5_documenteur", config_doc)
            await agent_5.startup()
            
            print("📝 Génération de la documentation diagnostic...")
            resultat_doc = await agent_5.documenter_complete()
            
            diagnostic_global["etapes"]["documentation"] = {
                "status": "complete",
                "agent_id": agent_5.agent_id,
                "resultats": resultat_doc,
                "timestamp": datetime.now().isoformat()
            }
            
            if resultat_doc:
                print(f"✅ Documentation générée:")
                print(f"   📄 Documents créés: {resultat_doc.get('nombre_documents', 0)}")
                docs_generes = resultat_doc.get('documents_generes', [])
                if docs_generes:
                    print(f"   📋 Fichiers générés:")
                    for doc in docs_generes[:3]:
                        print(f"      • {Path(doc).name}")
                    if len(docs_generes) > 3:
                        print(f"      ... et {len(docs_generes) - 3} autres")
            
            await agent_5.shutdown()
            
        except Exception as e:
            print(f"❌ Erreur lors de la documentation: {e}")
            diagnostic_global["etapes"]["documentation"] = {
                "status": "erreur",
                "erreur": str(e),
                "timestamp": datetime.now().isoformat()
            }
        
        # ÉTAPE 5: Validation Finale
        print("\n" + "="*50)
        print("✅ ÉTAPE 5/6: VALIDATION DIAGNOSTIC")
        print("="*50)
        
        try:
            # Préparer tous les résultats pour la validation
            resultats_equipe = {}
            for etape, donnees in diagnostic_global["etapes"].items():
                if donnees.get("status") == "complete":
                    resultats_equipe[etape] = donnees["resultats"]
            
            config_validation = config_diagnostic.copy()
            config_validation.update({
                "resultats_equipe": resultats_equipe
            })
            
            agent_6 = await template_manager.create_agent("agent_6_validateur_final", config_validation)
            await agent_6.startup()
            
            print("🔍 Validation finale du diagnostic...")
            resultat_validation = await agent_6.valider_mission()
            
            diagnostic_global["etapes"]["validation_finale"] = {
                "status": "complete",
                "agent_id": agent_6.agent_id,
                "resultats": resultat_validation,
                "timestamp": datetime.now().isoformat()
            }
            
            if resultat_validation:
                print(f"✅ Validation terminée:")
                print(f"   📊 Score global: {resultat_validation.get('score_global', 0):.1f}/10")
                print(f"   ✅ Validations réussies: {resultat_validation.get('validations_reussies', 0)}")
                print(f"   ⚠️  Points d'attention: {len(resultat_validation.get('points_attention', []))}")
                
                # Recommandations
                recommandations = resultat_validation.get('recommandations', [])
                if recommandations:
                    diagnostic_global["recommandations"] = recommandations
                    print(f"\n💡 RECOMMANDATIONS PRINCIPALES:")
                    for i, rec in enumerate(recommandations[:3], 1):
                        print(f"   {i}. {rec}")
                    if len(recommandations) > 3:
                        print(f"   ... et {len(recommandations) - 3} autres recommandations")
            
            await agent_6.shutdown()
            
        except Exception as e:
            print(f"❌ Erreur lors de la validation: {e}")
            diagnostic_global["etapes"]["validation_finale"] = {
                "status": "erreur",
                "erreur": str(e),
                "timestamp": datetime.now().isoformat()
            }
        
        # ÉTAPE 6: Rapport Final
        print("\n" + "="*50)
        print("📊 ÉTAPE 6/6: RAPPORT FINAL DIAGNOSTIC")
        print("="*50)
        
        # Consolider les résultats
        etapes_reussies = sum(1 for etape in diagnostic_global["etapes"].values() if etape.get("status") == "complete")
        total_etapes = len(diagnostic_global["etapes"])
        
        diagnostic_global["status"] = "complete" if etapes_reussies == total_etapes else "partiel"
        diagnostic_global["resultats_consolides"] = {
            "etapes_reussies": etapes_reussies,
            "total_etapes": total_etapes,
            "taux_succes": (etapes_reussies / total_etapes * 100) if total_etapes > 0 else 0,
            "timestamp_fin": datetime.now().isoformat()
        }
        
        # Sauvegarder le rapport
        rapport_path = workspace_path / "reports" / f"diagnostic_agents_factory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        rapport_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(rapport_path, 'w', encoding='utf-8') as f:
            json.dump(diagnostic_global, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Rapport sauvegardé: {rapport_path}")
        
        # Arrêt du TemplateManager
        await template_manager.shutdown()
        
        # Affichage du rapport final
        print("\n" + "="*70)
        print("📊 RAPPORT FINAL - DIAGNOSTIC AGENTS FACTORY")
        print("="*70)
        
        print(f"📁 Répertoire analysé: {target_path}")
        print(f"⏱️  Durée totale: {datetime.now().isoformat()}")
        print(f"📊 Étapes réussies: {etapes_reussies}/{total_etapes} ({diagnostic_global['resultats_consolides']['taux_succes']:.1f}%)")
        
        # Résumé par étape
        print(f"\n📋 RÉSUMÉ PAR ÉTAPE:")
        for nom_etape, donnees in diagnostic_global["etapes"].items():
            status = donnees.get("status", "inconnu")
            emoji = "✅" if status == "complete" else "❌" if status == "erreur" else "⚠️"
            print(f"   {emoji} {nom_etape.replace('_', ' ').title()}: {status}")
        
        # Recommandations finales
        if diagnostic_global.get("recommandations"):
            print(f"\n💡 RECOMMANDATIONS FINALES:")
            for i, rec in enumerate(diagnostic_global["recommandations"], 1):
                print(f"   {i}. {rec}")
        
        print(f"\n📄 Rapport détaillé: {rapport_path}")
        print("\n🔍 DIAGNOSTIC TERMINÉ - AUCUNE MODIFICATION EFFECTUÉE")
        
        return diagnostic_global["status"] == "complete"
        
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE DIAGNOSTIC: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_diagnostic_agents_factory())
    sys.exit(0 if success else 1) 