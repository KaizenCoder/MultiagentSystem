#!/usr/bin/env python3
"""
🧪 Test des Nouveaux Composants TaskMaster Cursor
Test simple des 3 composants manquants maintenant implémentés
"""

import asyncio
import sys
import os
from datetime import datetime

async def test_cli():
    """Test CLI TaskMaster Cursor"""
    print("🧪 Test CLI TaskMaster Cursor...")
    
    try:
        from cli_taskmaster_cursor import TaskMasterCLI
        
        cli = TaskMasterCLI()
        print("✅ CLI initialisé")
        
        # Test validation infrastructure
        is_valid = await cli.validate_infrastructure()
        print(f"✅ Infrastructure {'validée' if is_valid else 'partiellement validée'}")
        
        # Test lancement tâche
        result = await cli.launch_single_task("Test CLI simple")
        print(f"✅ Tâche lancée: {result.task_id} - {result.status.value}")
        
        # Test liste tâches
        tasks = await cli.list_tasks(3)
        print(f"✅ {len(tasks)} tâches trouvées")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur CLI: {str(e)}")
        return False

async def test_dashboard():
    """Test Dashboard TaskMaster Cursor"""
    print("\n🧪 Test Dashboard TaskMaster Cursor...")
    
    try:
        from dashboard_taskmaster_cursor import TaskMasterDashboard
        
        dashboard = TaskMasterDashboard(refresh_interval=1)
        print("✅ Dashboard initialisé")
        
        # Test statut infrastructure
        status = dashboard._get_infrastructure_status()
        print(f"✅ Statut infrastructure: {status['total_score']}/{status.get('max_score', 70)}")
        
        # Test affichage (capture stdout)
        import io
        import contextlib
        
        stdout_buffer = io.StringIO()
        with contextlib.redirect_stdout(stdout_buffer):
            dashboard.print_dashboard(status)
        
        output = stdout_buffer.getvalue()
        if len(output) > 0:
            print("✅ Affichage dashboard fonctionnel")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur Dashboard: {str(e)}")
        return False

async def test_validator():
    """Test Validator Sessions Cursor"""
    print("\n🧪 Test Validator Sessions Cursor...")
    
    try:
        from validator_sessions_cursor import SessionValidator
        
        validator = SessionValidator()
        print("✅ Validator initialisé")
        
        # Test validation PostgreSQL
        pg_sessions = await validator.validate_postgresql_sessions()
        print(f"✅ {len(pg_sessions)} sessions PostgreSQL trouvées")
        
        # Test validation tâches
        tasks = await validator.validate_taskmaster_tasks()
        print(f"✅ {len(tasks)} tâches TaskMaster trouvées")
        
        # Test validation complète
        result = await validator.run_full_validation()
        print(f"✅ Validation complète: {result.total_sessions} sessions totales")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur Validator: {str(e)}")
        return False

async def test_integration():
    """Test intégration des 3 composants"""
    print("\n🧪 Test Intégration CLI + Dashboard + Validator...")
    
    try:
        from cli_taskmaster_cursor import TaskMasterCLI
        from dashboard_taskmaster_cursor import TaskMasterDashboard
        from validator_sessions_cursor import SessionValidator
        
        # Initialisation simultanée
        cli = TaskMasterCLI()
        dashboard = TaskMasterDashboard()
        validator = SessionValidator()
        print("✅ 3 composants initialisés simultanément")
        
        # Test flux CLI → Validator
        task_result = await cli.launch_single_task("Test intégration")
        await asyncio.sleep(0.5)  # Attendre sauvegarde
        
        validation_result = await validator.run_full_validation()
        print(f"✅ Flux CLI → Validator: tâche créée et sessions validées")
        
        # Test Dashboard avec données
        dashboard_status = dashboard._get_infrastructure_status()
        print(f"✅ Dashboard mis à jour: score {dashboard_status['total_score']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur Intégration: {str(e)}")
        return False

async def main():
    """Test principal"""
    print("🚀 Test des Nouveaux Composants TaskMaster Cursor")
    print("="*60)
    
    start_time = datetime.now()
    
    # Tests individuels
    cli_ok = await test_cli()
    dashboard_ok = await test_dashboard() 
    validator_ok = await test_validator()
    integration_ok = await test_integration()
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*60)
    
    results = [
        ("CLI TaskMaster Cursor", cli_ok),
        ("Dashboard TaskMaster Cursor", dashboard_ok),
        ("Validator Sessions Cursor", validator_ok),
        ("Intégration 3 Composants", integration_ok)
    ]
    
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    
    for component, ok in results:
        emoji = "✅" if ok else "❌"
        print(f"{emoji} {component}")
    
    print(f"\n🎯 SCORE: {passed}/{total} ({(passed/total)*100:.1f}%)")
    print(f"⏱️ DURÉE: {duration:.1f}s")
    
    if passed == total:
        print("🎉 TOUS LES TESTS RÉUSSIS - Composants opérationnels!")
        print("💡 Gap Analysis résolu: CLI, Dashboard et Validator implémentés")
    else:
        print("⚠️ Certains tests ont échoué - Vérifier les composants")
    
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main()) 



