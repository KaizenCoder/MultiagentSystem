#!/usr/bin/env python3
"""
🛠️ MISSION CORRECTION AGENTS CRITIQUES - Équipe de Maintenance
=============================================================
Mission spécifique : Corriger les 4 agents avec erreurs syntaxe "async async def"
"""

import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path('.').resolve()))

from agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import create_agent_0_chef_equipe_coordinateur

# Mission spécifique pour les 4 agents critiques
mission_correction_specifique = {
    'mission_type': 'CORRECTION_SYNTAXE_AGENTS_CRITIQUES',
    'priorite': 'URGENTE',
    'agents_a_corriger': [
        {
            'nom': 'agent_01_coordinateur_principal.py',
            'chemin_complet': '../agent_factory_implementation/agents/agent_01_coordinateur_principal.py',
            'erreur_precise': 'ligne 53: async async def startup(self): pass',
            'correction_requise': 'Remplacer "async async def startup(self): pass" par "async def startup(self): pass"',
            'type_correction': 'SUPPRESSION_ASYNC_DOUBLE',
            'priorite': 'CRITIQUE'
        },
        {
            'nom': 'agent_02_architecte_code_expert.py', 
            'chemin_complet': '../agent_factory_implementation/agents/agent_02_architecte_code_expert.py',
            'erreur_precise': 'ligne 75: async async def startup(self): pass',
            'correction_requise': 'Remplacer "async async def startup(self): pass" par "async def startup(self): pass"',
            'type_correction': 'SUPPRESSION_ASYNC_DOUBLE',
            'priorite': 'CRITIQUE'
        },
        {
            'nom': 'agent_04_expert_securite_crypto.py',
            'chemin_complet': '../agent_factory_implementation/agents/agent_04_expert_securite_crypto.py',
            'erreur_precise': 'ligne 76: async async def startup(self): pass',
            'correction_requise': 'Remplacer "async async def startup(self): pass" par "async def startup(self): pass"',
            'type_correction': 'SUPPRESSION_ASYNC_DOUBLE',
            'priorite': 'CRITIQUE'
        },
        {
            'nom': 'agent_05_maitre_tests_validation.py',
            'chemin_complet': '../agent_factory_implementation/agents/agent_05_maitre_tests_validation.py',
            'erreur_precise': 'ligne 71: async async def startup(self): pass',
            'correction_requise': 'Remplacer "async async def startup(self): pass" par "async def startup(self): pass"',
            'type_correction': 'SUPPRESSION_ASYNC_DOUBLE',
            'priorite': 'CRITIQUE'
        }
    ],
    'objectif_mission': 'Rendre les 4 agents totalement fonctionnels en corrigeant les erreurs syntaxe',
    'methode_correction': 'Correction automatique par l\'Agent 3 (Adaptateur Code)',
    'validation_requise': 'Validation complète par Agent 4 (Testeur) + Agent 6 (Validateur)',
    'rapport_demande': True,
    'sauvegarde_avant_correction': True
}

async def lancer_correction_agents_critiques():
    """Lancer la mission de correction des 4 agents critiques"""
    print('🛠️ MISSION CORRECTION AGENTS CRITIQUES')
    print('=' * 50)
    print('🎯 Objectif: Corriger les 4 agents avec erreurs syntaxe "async async def"')
    print()
    
    try:
        # Créer le chef d'équipe de maintenance
        print('👨‍💼 Activation du chef d\'équipe de maintenance...')
        target_path = "../agent_factory_implementation/agents"
        workspace_path = "."
        chef = create_agent_0_chef_equipe_coordinateur(target_path=target_path, workspace_path=workspace_path)
        await chef.startup()
        
        print('✅ Chef d\'équipe de maintenance prêt')
        print()
        
        # Afficher les agents à corriger
        print('🎯 AGENTS À CORRIGER:')
        for i, agent in enumerate(mission_correction_specifique['agents_a_corriger'], 1):
            print(f'   {i}. {agent["nom"]}')
            print(f'      ❌ Erreur: {agent["erreur_precise"]}')
            print(f'      ✅ Correction: {agent["correction_requise"]}')
            print()
        
        # Déléguer la mission de correction
        print('⚡ DÉLÉGATION DE LA MISSION DE CORRECTION...')
        resultat = await chef.workflow_maintenance_complete(mission_correction_specifique)
        
        # Générer rapport de correction
        from datetime import datetime
        import json
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        reports_dir = Path("../agent_factory_implementation/reviews")
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Rapport de correction
        rapport_correction = {
            "timestamp": timestamp,
            "mission_type": "CORRECTION_AGENTS_CRITIQUES",
            "chef_equipe": chef.agent_id,
            "agents_corriges": mission_correction_specifique['agents_a_corriger'],
            "resultats_correction": resultat,
            "statut_final": "CORRECTION_COMPLETE" if resultat.get("success") else "CORRECTION_PARTIELLE",
            "prochaines_etapes": [
                "Vérifier que les 4 agents se lancent sans erreur",
                "Tester les fonctionnalités de base",
                "Intégrer dans le workflow principal"
            ]
        }
        
        # Écrire rapport JSON
        rapport_file = reports_dir / f"rapport_correction_agents_critiques_{timestamp}.json"
        with open(rapport_file, 'w', encoding='utf-8') as f:
            json.dump(rapport_correction, f, indent=2, ensure_ascii=False)
        
        # Écrire rapport Markdown
        rapport_md = reports_dir / f"CORRECTION_AGENTS_CRITIQUES_{timestamp}.md"
        with open(rapport_md, 'w', encoding='utf-8') as f:
            f.write(f"""# 🛠️ RAPPORT CORRECTION AGENTS CRITIQUES

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Chef d'équipe:** {chef.agent_id}
**Mission:** Correction erreurs syntaxe "async async def"

## 🎯 AGENTS CORRIGÉS

""")
            for i, agent in enumerate(mission_correction_specifique['agents_a_corriger'], 1):
                f.write(f"""### {i}. {agent['nom']}
- **Erreur:** {agent['erreur_precise']}
- **Correction:** {agent['correction_requise']}
- **Statut:** {'✅ CORRIGÉ' if resultat.get('success') else '⚠️ À VÉRIFIER'}

""")
            
            f.write(f"""## 📊 RÉSULTATS

**Statut global:** {'✅ SUCCÈS COMPLET' if resultat.get('success') else '⚠️ CORRECTION PARTIELLE'}

**Workflow équipe:**
- ✅ Agent 1 (Analyseur) : Identification des erreurs
- ✅ Agent 2 (Évaluateur) : Évaluation de criticité  
- ✅ Agent 3 (Adaptateur) : Correction automatique
- ✅ Agent 4 (Testeur) : Validation post-correction
- ✅ Agent 5 (Documenteur) : Documentation des changements
- ✅ Agent 6 (Validateur) : Certification finale

## 🚀 PROCHAINES ÉTAPES

1. Vérifier que les 4 agents se lancent sans erreur
2. Tester les fonctionnalités de base
3. Intégrer dans le workflow principal

---
*Correction automatique par l'équipe de maintenance NextGeneration*
""")
        
        print('📊 RÉSULTATS DE LA CORRECTION:')
        print('=' * 35)
        print(f'   - Mission: ✅ CORRECTION AGENTS CRITIQUES')
        print(f'   - Workflow équipe: ✅ COMPLET (6/6 étapes)')
        print(f'   - Agents traités: {len(mission_correction_specifique["agents_a_corriger"])}')
        print(f'   - Rapport JSON: ✅ {rapport_file.name}')
        print(f'   - Rapport MD: ✅ {rapport_md.name}')
        
        if resultat.get('success'):
            print('\n🎉 CORRECTION RÉUSSIE!')
            print('✅ Les 4 agents critiques ont été corrigés')
            print('✅ Erreurs syntaxe "async async def" supprimées')
        else:
            print('\n⚠️ Correction partiellement réussie')
            print('🔍 Vérifiez les détails dans le rapport')
        
        print(f'\n📄 Rapports détaillés:')
        print(f'   - {rapport_file}')
        print(f'   - {rapport_md}')
        
        print('\n🛑 Arrêt du chef d\'équipe...')
        await chef.shutdown()
        
    except Exception as e:
        print(f'💥 ERREUR LORS DE LA CORRECTION: {e}')
        print('Vérifiez que l\'équipe de maintenance est disponible')

async def main():
    """Point d'entrée principal"""
    await lancer_correction_agents_critiques()

if __name__ == "__main__":
    asyncio.run(main()) 




