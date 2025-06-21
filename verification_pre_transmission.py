#!/usr/bin/env python3
"""
🔍 VÉRIFICATION PRÉ-TRANSMISSION - TASKMASTER NEXTGENERATION
============================================================

🎯 Mission : Vérifier l'état du système avant transmission de mission
         au Chef d'Équipe de Maintenance

📊 Vérifications :
   - Structure des répertoires
   - Agents de l'équipe de maintenance
   - Agents experts cibles
   - Configuration système

Author: Assistant IA - Vérification système
Created: 2025-01-21
"""

import sys
from pathlib import Path
from datetime import datetime
import json

class VerificateurPreTransmission:
    """Vérificateur système pré-transmission"""
    
    def __init__(self):
        self.projet_root = Path(__file__).parent
        self.erreurs = []
        self.avertissements = []
        self.verifications_reussies = []
    
    def verifier_structure_projet(self):
        """Vérifier la structure du projet"""
        print("🔍 Vérification de la structure du projet...")
        
        # Répertoires essentiels
        repertoires_requis = [
            "20250620_transformation_equipe_maintenance",
            "20250620_transformation_equipe_maintenance/agent_equipe_maintenance",
            "20250620_transformation_equipe_maintenance/docs",
            "agent_factory_experts_team"
        ]
        
        for repertoire in repertoires_requis:
            chemin = self.projet_root / repertoire
            if chemin.exists():
                self.verifications_reussies.append(f"✅ {repertoire}")
            else:
                self.erreurs.append(f"❌ Répertoire manquant: {repertoire}")
        
        # Fichiers essentiels
        fichiers_requis = [
            "20250620_transformation_equipe_maintenance/agent_equipe_maintenance/agent_MAINTENANCE_00_chef_equipe_coordinateur.py",
            "transmission_mission_chef_equipe_maintenance.py",
            "lancer_transmission_mission.bat"
        ]
        
        for fichier in fichiers_requis:
            chemin = self.projet_root / fichier
            if chemin.exists():
                self.verifications_reussies.append(f"✅ {fichier}")
            else:
                self.erreurs.append(f"❌ Fichier manquant: {fichier}")
    
    def verifier_equipe_maintenance(self):
        """Vérifier l'équipe de maintenance"""
        print("🔍 Vérification de l'équipe de maintenance...")
        
        equipe_path = self.projet_root / "20250620_transformation_equipe_maintenance" / "agent_equipe_maintenance"
        
        if not equipe_path.exists():
            self.erreurs.append("❌ Répertoire équipe de maintenance introuvable")
            return
        
        # Agents requis
        agents_requis = [
            "agent_MAINTENANCE_00_chef_equipe_coordinateur.py",
            "agent_MAINTENANCE_01_analyseur_structure.py",
            "agent_MAINTENANCE_02_evaluateur_utilite.py",
            "agent_MAINTENANCE_03_adaptateur_code.py",
            "agent_MAINTENANCE_04_testeur_anti_faux_agents.py",
            "agent_MAINTENANCE_05_documenteur_peer_reviewer.py",
            "agent_MAINTENANCE_06_validateur_final.py"
        ]
        
        agents_presents = 0
        for agent in agents_requis:
            chemin = equipe_path / agent
            if chemin.exists():
                agents_presents += 1
                self.verifications_reussies.append(f"✅ Agent maintenance: {agent}")
            else:
                self.erreurs.append(f"❌ Agent manquant: {agent}")
        
        print(f"   📊 {agents_presents}/{len(agents_requis)} agents de maintenance présents")
    
    def verifier_agents_experts(self):
        """Vérifier les agents experts cibles"""
        print("🔍 Vérification des agents experts...")
        
        experts_path = self.projet_root / "agent_factory_experts_team"
        
        if not experts_path.exists():
            self.erreurs.append("❌ Répertoire agents experts introuvable")
            return
        
        # Recherche des agents experts
        agents_experts = []
        for fichier in experts_path.iterdir():
            if fichier.is_file() and fichier.name.endswith('.py'):
                if 'expert' in fichier.name or 'coordinateur' in fichier.name:
                    agents_experts.append(fichier.name)
        
        if agents_experts:
            self.verifications_reussies.append(f"✅ {len(agents_experts)} agents experts trouvés")
            for agent in agents_experts:
                print(f"   📄 {agent}")
        else:
            self.avertissements.append("⚠️ Aucun agent expert trouvé")
        
        return agents_experts
    
    def verifier_python_modules(self):
        """Vérifier les modules Python requis"""
        print("🔍 Vérification des modules Python...")
        
        modules_requis = [
            "asyncio",
            "json", 
            "pathlib",
            "datetime",
            "sys"
        ]
        
        modules_manquants = []
        for module in modules_requis:
            try:
                __import__(module)
                self.verifications_reussies.append(f"✅ Module: {module}")
            except ImportError:
                modules_manquants.append(module)
                self.erreurs.append(f"❌ Module manquant: {module}")
        
        if not modules_manquants:
            print("   ✅ Tous les modules requis sont disponibles")
    
    def generer_rapport(self):
        """Générer le rapport de vérification"""
        print("\n" + "="*80)
        print("📋 RAPPORT DE VÉRIFICATION PRÉ-TRANSMISSION")
        print("="*80)
        
        print(f"\n✅ VÉRIFICATIONS RÉUSSIES: {len(self.verifications_reussies)}")
        for verification in self.verifications_reussies:
            print(f"   {verification}")
        
        if self.avertissements:
            print(f"\n⚠️ AVERTISSEMENTS: {len(self.avertissements)}")
            for avertissement in self.avertissements:
                print(f"   {avertissement}")
        
        if self.erreurs:
            print(f"\n❌ ERREURS: {len(self.erreurs)}")
            for erreur in self.erreurs:
                print(f"   {erreur}")
        
        # Statut global
        print(f"\n🎯 STATUT GLOBAL:")
        if not self.erreurs:
            print("   ✅ SYSTÈME PRÊT POUR LA TRANSMISSION")
            statut = "READY"
        elif len(self.erreurs) <= 2:
            print("   ⚠️ SYSTÈME PARTIELLEMENT PRÊT (corrections mineures requises)")
            statut = "PARTIAL"
        else:
            print("   ❌ SYSTÈME NON PRÊT (corrections majeures requises)")
            statut = "NOT_READY"
        
        # Sauvegarde du rapport
        rapport = {
            "timestamp": datetime.now().isoformat(),
            "statut": statut,
            "verifications_reussies": len(self.verifications_reussies),
            "avertissements": len(self.avertissements),
            "erreurs": len(self.erreurs),
            "details": {
                "succes": self.verifications_reussies,
                "avertissements": self.avertissements,
                "erreurs": self.erreurs
            }
        }
        
        rapport_file = self.projet_root / f"rapport_verification_pretransmission_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(rapport_file, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
        
        print(f"\n📋 Rapport sauvegardé: {rapport_file.name}")
        
        return statut == "READY"

def main():
    """Point d'entrée principal"""
    print("🎯 TaskMaster NextGeneration - Vérification Pré-Transmission")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    verificateur = VerificateurPreTransmission()
    
    try:
        # Vérifications séquentielles
        verificateur.verifier_structure_projet()
        verificateur.verifier_equipe_maintenance()
        agents_experts = verificateur.verifier_agents_experts()
        verificateur.verifier_python_modules()
        
        # Génération du rapport
        systeme_pret = verificateur.generer_rapport()
        
        # Instructions finales
        print(f"\n💡 INSTRUCTIONS:")
        if systeme_pret:
            print("   🚀 Vous pouvez lancer la transmission avec:")
            print("      - Windows: lancer_transmission_mission.bat")
            print("      - Python: python transmission_mission_chef_equipe_maintenance.py")
        else:
            print("   🔧 Corrigez les erreurs identifiées avant de lancer la transmission")
        
        print(f"\n📊 Agents experts identifiés: {len(agents_experts) if 'agents_experts' in locals() else 0}")
        
        return 0 if systeme_pret else 1
        
    except KeyboardInterrupt:
        print(f"\n⏹️ Vérification interrompue par l'utilisateur")
        return 1
    except Exception as e:
        print(f"\n💥 Erreur lors de la vérification: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())




