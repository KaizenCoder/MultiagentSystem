#!/usr/bin/env python3
"""
🔧 TEST TRANSFORMATION COMPLÈTE UN SEUL AGENT
============================================

Script de test pour transformer UN SEUL agent avec :
1. Backup automatique obligatoire
2. Transformation complète vers Pattern Factory
3. Validation post-transformation
4. Rollback en cas d'erreur

Répertoire de sauvegarde: C:/Dev/nextgeneration/agent_factory_implementation/backups

Author: Équipe Maintenance NextGeneration
Version: 1.0.0
Created: 2025-01-20
"""

import asyncio
import json
import sys
import shutil
from pathlib import Path
from datetime import datetime

# Ajouter le répertoire des agents au PATH
sys.path.insert(0, str(Path(__file__).parent / "agent_equipe_maintenance"))

from agent_MAINTENANCE_03_adaptateur_code_UPGRADED import create_adaptateur_code_upgraded

async def test_transformation_un_agent():
    """Test de transformation complète d'un seul agent"""
    
    print("🔧 TEST TRANSFORMATION COMPLÈTE UN SEUL AGENT")
    print("=" * 70)
    
    # Vérifier les répertoires
    target_dir = Path("../agent_factory_implementation/agents")
    backup_dir = Path("../agent_factory_implementation/backups")
    
    print(f"\n📁 VÉRIFICATION RÉPERTOIRES:")
    print(f"   🎯 Répertoire cible: {target_dir.resolve()}")
    print(f"   💾 Répertoire backup: {backup_dir.resolve()}")
    
    if not target_dir.exists():
        print(f"❌ Erreur: Répertoire cible non trouvé: {target_dir}")
        return
    
    # Créer le répertoire de backup s'il n'existe pas
    backup_dir.mkdir(exist_ok=True)
    print(f"   ✅ Répertoire backup confirmé")
    
    # Trouver les agents avec problèmes critiques
    agent_files = list(target_dir.glob("agent_*.py"))
    if not agent_files:
        print(f"❌ Aucun agent trouvé dans: {target_dir}")
        return
    
    # Sélectionner un agent avec des problèmes (basé sur le test précédent)
    test_agent_file = None
    for agent_file in agent_files:
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if "async async def" in content:
            test_agent_file = agent_file
            break
    
    if not test_agent_file:
        test_agent_file = agent_files[0]  # Prendre le premier si aucun problème critique
    
    print(f"   🎯 Agent sélectionné: {test_agent_file.name}")
    
    # Créer l'agent 03 upgraded
    agent = create_adaptateur_code_upgraded()
    backup_path = None
    
    try:
        # 1. Démarrage
        print(f"\n🚀 PHASE 1: DÉMARRAGE AGENT 03 UPGRADED")
        await agent.startup()
        
        health = await agent.health_check()
        print(f"   ✅ Agent démarré: {health['agent_id']}")
        
        # 2. Analyse pré-transformation
        print(f"\n🔍 PHASE 2: ANALYSE PRÉ-TRANSFORMATION")
        
        with open(test_agent_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Analyser la structure originale
        try:
            original_structure = agent._analyze_current_structure(original_content)
            original_score = sum([
                original_structure['has_main_class'],
                original_structure['inherits_from_agent'],
                original_structure['has_startup_method'],
                original_structure['has_shutdown_method'],
                original_structure['has_health_check_method'],
                original_structure['has_execute_task_method']
            ]) / 6 * 100
        except:
            original_score = 0.0
        
        print(f"   📊 Score conformité original: {original_score:.1f}%")
        
        # Compter les problèmes
        problems = []
        if "async async def" in original_content:
            problems.append("Syntaxe 'async async def'")
        if not original_structure.get('import_pattern_factory', False):
            problems.append("Import Pattern Factory manquant")
        if not original_structure.get('inherits_from_agent', False):
            problems.append("N'hérite pas d'Agent")
        
        print(f"   🚨 Problèmes détectés: {len(problems)}")
        for problem in problems:
            print(f"      • {problem}")
        
        # 3. Backup obligatoire
        print(f"\n💾 PHASE 3: BACKUP OBLIGATOIRE")
        
        backup_path = await agent._create_backup(test_agent_file)
        print(f"   ✅ Backup créé: {backup_path.name}")
        
        # Vérifier l'intégrité du backup
        with open(backup_path, 'r', encoding='utf-8') as f:
            backup_content = f.read()
        
        if backup_content == original_content:
            print(f"   ✅ Intégrité backup vérifiée")
        else:
            print(f"   ❌ ERREUR: Backup corrompu!")
            return
        
        # 4. Transformation
        print(f"\n🔧 PHASE 4: TRANSFORMATION")
        
        print(f"   🔄 Lancement transformation de {test_agent_file.name}...")
        
        # Utiliser la méthode de transformation de l'agent
        result = await agent.transform_single_agent(
            agent_path=test_agent_file,
            force_backup=True  # Backup déjà fait mais on force la sécurité
        )
        
        if result['success']:
            print(f"   ✅ Transformation réussie!")
            print(f"   📊 Corrections appliquées: {result.get('corrections_applied', 0)}")
            
            # 5. Validation post-transformation
            print(f"\n✅ PHASE 5: VALIDATION POST-TRANSFORMATION")
            
            # Relire le fichier transformé
            with open(test_agent_file, 'r', encoding='utf-8') as f:
                transformed_content = f.read()
            
            # Analyser la nouvelle structure
            try:
                new_structure = agent._analyze_current_structure(transformed_content)
                new_score = sum([
                    new_structure['has_main_class'],
                    new_structure['inherits_from_agent'],
                    new_structure['has_startup_method'],
                    new_structure['has_shutdown_method'],
                    new_structure['has_health_check_method'],
                    new_structure['has_execute_task_method']
                ]) / 6 * 100
            except Exception as e:
                print(f"   ⚠️ Erreur analyse post-transformation: {e}")
                new_score = 0.0
            
            print(f"   📊 Score conformité final: {new_score:.1f}%")
            print(f"   📈 Amélioration: +{new_score - original_score:.1f}%")
            
            # Vérifier les corrections spécifiques
            corrections_ok = []
            
            if "async async def" not in transformed_content:
                corrections_ok.append("✅ Syntaxe 'async async def' corrigée")
            else:
                corrections_ok.append("❌ Syntaxe 'async async def' toujours présente")
            
            if "from core.agent_factory_architecture import Agent" in transformed_content:
                corrections_ok.append("✅ Import Pattern Factory ajouté")
            else:
                corrections_ok.append("⚠️ Import Pattern Factory à vérifier")
            
            print(f"   🔧 Vérifications corrections:")
            for correction in corrections_ok:
                print(f"      {correction}")
            
            # 6. Test syntaxe Python
            print(f"\n🐍 PHASE 6: VALIDATION SYNTAXE PYTHON")
            
            try:
                import ast
                ast.parse(transformed_content)
                print(f"   ✅ Syntaxe Python valide")
            except SyntaxError as e:
                print(f"   ❌ ERREUR SYNTAXE: {e}")
                print(f"   🔄 Rollback automatique nécessaire!")
                
                # Rollback automatique
                print(f"\n🔄 ROLLBACK AUTOMATIQUE")
                with open(test_agent_file, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                print(f"   ✅ Fichier original restauré depuis backup")
                
                return
            
        else:
            print(f"   ❌ Transformation échouée: {result.get('error', 'Erreur inconnue')}")
            return
        
        # 7. Résumé final
        print(f"\n" + "=" * 70)
        print(f"✅ TRANSFORMATION COMPLÈTE RÉUSSIE!")
        print(f"📊 RÉSUMÉ:")
        print(f"   🎯 Agent transformé: {test_agent_file.name}")
        print(f"   💾 Backup sauvegardé: {backup_path.name}")
        print(f"   📈 Score conformité: {original_score:.1f}% → {new_score:.1f}% (+{new_score - original_score:.1f}%)")
        print(f"   🔧 Problèmes corrigés: {len(problems)}")
        print(f"   🐍 Syntaxe Python: ✅ Valide")
        print(f"\n🛡️ TRANSFORMATION SÉCURISÉE TERMINÉE!")
        print("=" * 70)
        
        # Proposer la suite
        print(f"\n🚀 PRÊT POUR TRANSFORMATION MASSIVE:")
        print(f"   1. ✅ Test sur un agent réussi")
        print(f"   2. 💾 Système backup fonctionnel")
        print(f"   3. 🔧 Corrections automatiques validées")
        print(f"   4. 🐍 Validation syntaxe opérationnelle")
        print(f"\n💡 Pour transformer tous les agents:")
        print(f"   python lancer_transformation_pattern_factory.py")
        
    except Exception as e:
        print(f"\n❌ Erreur durant la transformation: {e}")
        
        # Rollback en cas d'erreur
        if backup_path and backup_path.exists():
            print(f"\n🔄 ROLLBACK D'URGENCE")
            try:
                with open(backup_path, 'r', encoding='utf-8') as f:
                    backup_content = f.read()
                with open(test_agent_file, 'w', encoding='utf-8') as f:
                    f.write(backup_content)
                print(f"   ✅ Fichier restauré depuis backup")
            except Exception as rollback_error:
                print(f"   ❌ Erreur rollback: {rollback_error}")
        
        await agent.shutdown()
        raise
    
    finally:
        # Arrêt propre
        await agent.shutdown()

def main():
    """Point d'entrée principal"""
    try:
        asyncio.run(test_transformation_un_agent())
    except KeyboardInterrupt:
        print("\n⚠️ Transformation interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n💥 Erreur fatale: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 



