#!/usr/bin/env python3
"""
🔧 CORRECTION AGENT 2 - DÉLÉGATION AU CHEF D'ÉQUIPE
Mission spécifique : Corriger l'erreur "division by zero" dans l'Agent 2
MODE DÉLÉGATION - Le chef d'équipe supervise la correction
"""

import asyncio
import sys
from pathlib import Path

# Import du chef d'équipe de maintenance
sys.path.insert(0, str(Path(__file__).parent))

try:
    from agent_0_chef_equipe_coordinateur import Agent0ChefEquipeCoordinateur
    print("✅ Chef d'équipe de maintenance chargé")
except Exception as e:
    print(f"❌ Erreur chargement chef d'équipe: {e}")
    sys.exit(1)

class CorrectionAgent2:
    """Correction spécifique de l'Agent 2 via délégation"""
    
    def __init__(self):
        self.chef_equipe = Agent0ChefEquipeCoordinateur()
        
    async def deleguer_correction_agent_2(self):
        """Délègue la correction spécifique de l'Agent 2 au chef d'équipe"""
        print("🔧 CORRECTION AGENT 2 - DÉLÉGATION AU CHEF D'ÉQUIPE")
        print("=" * 60)
        
        # Instructions spécifiques pour la correction de l'Agent 2
        mission_correction_agent_2 = {
            "type_mission": "correction_agent_specifique",
            "agent_cible": "Agent 2 - Évaluateur Utilité",
            "probleme_identifie": "division by zero",
            "priorite": "CRITIQUE",
            "instructions_detaillees": {
                "diagnostic": [
                    "Analyser le code de l'Agent 2 (agent_2_evaluateur_utilite.py)",
                    "Identifier la ligne causant l'erreur 'division by zero'",
                    "Localiser le calcul de score problématique",
                    "Vérifier les données d'entrée qui causent le dénominateur nul"
                ],
                "correction": [
                    "Ajouter une vérification avant division (if denominator != 0)",
                    "Implémenter une valeur par défaut sécurisée",
                    "Ajouter une gestion d'erreur appropriée",
                    "Documenter la correction dans le code"
                ],
                "validation": [
                    "Tester la correction avec les données qui causaient l'erreur",
                    "Vérifier que l'Agent 2 fonctionne correctement",
                    "Valider l'évaluation d'utilité complète",
                    "Confirmer l'intégration avec le workflow"
                ]
            },
            "contraintes": [
                "Ne pas modifier la logique métier existante",
                "Maintenir la compatibilité avec les autres agents",
                "Conserver les interfaces TemplateManager",
                "Documenter toutes les modifications"
            ],
            "livrable_attendu": "Agent 2 fonctionnel sans erreur division by zero"
        }
        
        print("🎯 MISSION SPÉCIFIQUE AGENT 2:")
        print(f"🔴 Problème: {mission_correction_agent_2['probleme_identifie']}")
        print(f"👤 Agent cible: {mission_correction_agent_2['agent_cible']}")
        print(f"⚡ Priorité: {mission_correction_agent_2['priorite']}")
        print()
        
        print("📋 INSTRUCTIONS POUR LE CHEF D'ÉQUIPE:")
        for phase, instructions in mission_correction_agent_2["instructions_detaillees"].items():
            print(f"\n🔍 Phase {phase.upper()}:")
            for i, instruction in enumerate(instructions, 1):
                print(f"   {i}. {instruction}")
        
        print(f"\n🚫 CONTRAINTES:")
        for contrainte in mission_correction_agent_2["contraintes"]:
            print(f"   • {contrainte}")
        
        print(f"\n🎯 LIVRABLE: {mission_correction_agent_2['livrable_attendu']}")
        print()
        
        print("🤝 DÉLÉGATION DE LA CORRECTION AU CHEF D'ÉQUIPE...")
        
        try:
            # Démarrage du chef d'équipe
            await self.chef_equipe.startup()
            
            # Délégation de la mission de correction
            resultats = await self.chef_equipe.execute_task(mission_correction_agent_2)
            
            print("✅ CORRECTION DÉLÉGUÉE AVEC SUCCÈS")
            print("=" * 60)
            
            # Analyse des résultats
            if resultats.get("workflow_id"):
                print("📊 RÉSULTATS DE LA CORRECTION:")
                print(f"🆔 ID Workflow: {resultats.get('workflow_id')}")
                print(f"👤 Chef d'équipe: {resultats.get('chef_equipe_id')}")
                
                # Vérification du statut de l'Agent 2
                etapes = resultats.get("etapes", {})
                agent_2_status = None
                
                for etape_nom, etape_info in etapes.items():
                    if "2" in etape_nom or "evaluation" in etape_nom.lower():
                        agent_2_status = etape_info.get("status")
                        if agent_2_status == "complete":
                            print("✅ Agent 2 - Correction réussie !")
                            print(f"   ⏱️ Durée: {etape_info.get('resultats', {}).get('duree_secondes', 0):.2f}s")
                        elif agent_2_status == "erreur":
                            print("❌ Agent 2 - Erreur persistante")
                            print(f"   🔍 Détail: {etape_info.get('erreur', 'Non spécifiée')}")
                        break
                
                if agent_2_status == "complete":
                    print("\n🎉 MISSION ACCOMPLIE !")
                    print("✅ Agent 2 fonctionnel")
                    print("✅ Erreur 'division by zero' corrigée")
                    print("✅ Workflow de maintenance opérationnel")
                else:
                    print("\n⚠️ CORRECTION PARTIELLE")
                    await self._instructions_correction_manuelle()
                    
            else:
                print("⚠️ Résultats partiels - Le chef d'équipe continue les corrections")
                print(f"📄 Statut: {resultats}")
            
            # Arrêt du chef d'équipe
            await self.chef_equipe.shutdown()
            
        except Exception as e:
            print(f"❌ Erreur durant la correction: {e}")
            print("\n💡 INSTRUCTIONS DIRECTES POUR LE CHEF D'ÉQUIPE:")
            await self._instructions_correction_manuelle()
    
    async def _instructions_correction_manuelle(self):
        """Instructions manuelles pour la correction de l'Agent 2"""
        print("\n🛠️ INSTRUCTIONS MANUELLES - CORRECTION AGENT 2")
        print("=" * 50)
        
        print("📝 ÉTAPES DE CORRECTION:")
        print("\n1. 🔍 DIAGNOSTIC:")
        print("   • Ouvrir agent_2_evaluateur_utilite.py")
        print("   • Chercher les calculs de division dans les méthodes")
        print("   • Identifier où le dénominateur peut être zéro")
        print("   • Localiser la méthode causant l'erreur")
        
        print("\n2. 🔧 CORRECTION:")
        print("   • Ajouter: if denominator != 0:")
        print("   • Avant chaque division par une variable")
        print("   • Définir une valeur par défaut (ex: score = 0)")
        print("   • Ajouter un log d'avertissement si nécessaire")
        
        print("\n3. ✅ VALIDATION:")
        print("   • Tester l'Agent 2 isolément")
        print("   • Vérifier avec les données qui causaient l'erreur")
        print("   • Valider l'intégration dans le workflow complet")
        print("   • Confirmer que l'évaluation d'utilité fonctionne")
        
        print("\n🎯 OBJECTIF:")
        print("   Agent 2 doit pouvoir évaluer l'utilité sans erreur 'division by zero'")

async def main():
    """Point d'entrée principal"""
    correction = CorrectionAgent2()
    await correction.deleguer_correction_agent_2()

if __name__ == "__main__":
    asyncio.run(main()) 