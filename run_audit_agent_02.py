#!/usr/bin/env python3
"""
Script pour auditer agent_02_architecte_code_expert.py avec agent_20_auditeur_conformite.py
"""

import asyncio
import sys
from pathlib import Path

# Import de l'agent 20 et de ses composants Pattern Factory
from agents.agent_20_auditeur_conformite import create_compliance_audit_agent
from core.agent_factory_architecture import Task

async def main():
    print("🚀 Lancement de l'audit de l'Agent 02 par l'Agent 20...")
    
    try:
        # Créer une instance de l'Agent 20 via sa fonction factory
        agent20 = create_compliance_audit_agent(
            environment="production",
            log_level="INFO",
            audit_target="agent_02_architecte_code_expert.py"
        )
        
        # Démarrer l'Agent 20
        await agent20.startup()
        print(f"✅ Agent 20 ({agent20.agent_id}) démarré.")

        # Préparer la tâche d'audit universel pour l'Agent 02
        audit_task = Task(
            id="audit_agent_02",
            type="universal_audit",
            params={
                "target_path": "agents/agent_02_architecte_code_expert.py",
                "module_name": "agent_02_architecte_code_expert"
            }
        )
        print(f"📋 Tâche d'audit créée pour: {audit_task.params['target_path']}")

        # Exécuter la tâche
        audit_result = await agent20.execute_task(audit_task)
        
        print("\n--- RÉSULTAT DE L'AUDIT ---")
        if audit_result.success:
            print("🎉 Audit réussi !")
            print("Détails de l'audit:")
            import json
            print(json.dumps(audit_result.data, indent=2, ensure_ascii=False))
            if audit_result.data.get('global_score'):
                print(f"\nScore Global de l'Agent 02: {audit_result.data['global_score']:.1f}/10")
            
        else:
            print(f"❌ Audit échoué: {audit_result.error}")
            if audit_result.data:
                import json
                print("Données de l'erreur:")
                print(json.dumps(audit_result.data, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"❌ Une erreur inattendue est survenue: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Arrêter l'Agent 20
        if 'agent20' in locals() and agent20.status != "shutdown":
            await agent20.shutdown()
            print("🛑 Agent 20 arrêté.")
        print("--- FIN DE L'AUDIT ---")

if __name__ == "__main__":
    asyncio.run(main()) 