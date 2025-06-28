#!/usr/bin/env python3
"""
SCRIPT VALIDATION MIGRATION LOGGING - AGENTS MAINTENANCE
========================================================

Script pour valider que la migration du système de logging
a été effectuée correctement sur tous les agents MAINTENANCE.

Author: Migration Team NextGeneration
Version: 1.0.0
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

def validate_agent_logging(agent_file: Path) -> Dict[str, any]:
    """
    Valide la migration du logging pour un agent spécifique.
    
    Args:
        agent_file: Chemin vers le fichier agent à valider
        
    Returns:
        Dict: Résultats de validation
    """
    try:
        content = agent_file.read_text(encoding='utf-8')
        
        # Critères de validation
        validation_results = {
            "agent": agent_file.name,
            "migrated": False,
            "has_fallback": False,
            "has_metadata": False,
            "uses_maintenance_config": False,
            "has_basicconfig_fallback": False,
            "issues": [],
            "status": "UNKNOWN"
        }
        
        # Vérification migration LoggingManager
        if "from core.manager import LoggingManager" in content:
            validation_results["migrated"] = True
        else:
            validation_results["issues"].append("❌ LoggingManager non importé")
            
        # Vérification fallback
        if "except ImportError:" in content and "logging.getLogger" in content:
            validation_results["has_fallback"] = True
        else:
            validation_results["issues"].append("❌ Fallback manquant ou incorrect")
            
        # Vérification métadonnées
        if '"agent_type":' in content and '"system": "nextgeneration"' in content:
            validation_results["has_metadata"] = True
        else:
            validation_results["issues"].append("⚠️  Métadonnées incomplètes")
            
        # Vérification configuration maintenance
        if 'config_name="maintenance"' in content:
            validation_results["uses_maintenance_config"] = True
        else:
            validation_results["issues"].append("⚠️  Configuration maintenance non utilisée")
            
        # Vérification fallback basicConfig (attendu pour agents critiques)
        if "logging.basicConfig" in content and "except ImportError:" in content:
            validation_results["has_basicconfig_fallback"] = True
            
        # Détermination du statut global
        if validation_results["migrated"] and validation_results["has_fallback"]:
            if len(validation_results["issues"]) == 0:
                validation_results["status"] = "✅ PARFAIT"
            elif len(validation_results["issues"]) <= 2:
                validation_results["status"] = "✅ BON"
            else:
                validation_results["status"] = "⚠️  AMÉLIORABLE"
        else:
            validation_results["status"] = "❌ ÉCHEC"
            
        return validation_results
        
    except Exception as e:
        return {
            "agent": agent_file.name,
            "migrated": False,
            "status": "❌ ERREUR",
            "issues": [f"Erreur validation: {e}"]
        }

def generate_migration_report(validations: List[Dict]) -> str:
    """Génère un rapport de migration détaillé."""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Statistiques globales
    total_agents = len(validations)
    migrated_agents = sum(1 for v in validations if v["migrated"])
    perfect_agents = sum(1 for v in validations if v["status"] == "✅ PARFAIT")
    good_agents = sum(1 for v in validations if v["status"] == "✅ BON")
    
    success_rate = (migrated_agents / total_agents) * 100 if total_agents > 0 else 0
    
    report = f"""# 📊 RAPPORT VALIDATION MIGRATION LOGGING AGENTS MAINTENANCE

**Date de validation :** {timestamp}  
**Agents analysés :** {total_agents}  
**Taux de migration :** {success_rate:.1f}%  

## 🎯 Résumé Exécutif

La migration du système de logging des agents MAINTENANCE vers le LoggingManager unifié a été **{'complétée avec succès' if success_rate >= 95 else 'partiellement réalisée'}**.

### 📈 Statistiques Globales
- ✅ **Agents migrés :** {migrated_agents}/{total_agents}
- 🏆 **Status parfait :** {perfect_agents}
- 👍 **Status bon :** {good_agents}
- ⚠️  **Nécessitent amélioration :** {total_agents - perfect_agents - good_agents}

## 📋 Détail par Agent

"""
    
    # Détail par agent
    for validation in sorted(validations, key=lambda x: x["agent"]):
        agent_name = validation["agent"]
        status = validation["status"]
        
        report += f"### {agent_name}\n"
        report += f"**Statut :** {status}  \n"
        
        if validation["migrated"]:
            report += f"✅ **Migration :** LoggingManager intégré  \n"
        else:
            report += f"❌ **Migration :** Non effectuée  \n"
            
        if validation.get("has_fallback"):
            report += f"✅ **Fallback :** Présent  \n"
        else:
            report += f"❌ **Fallback :** Manquant  \n"
            
        if validation.get("has_metadata"):
            report += f"✅ **Métadonnées :** Configurées  \n"
        else:
            report += f"⚠️  **Métadonnées :** Incomplètes  \n"
            
        if validation.get("uses_maintenance_config"):
            report += f"✅ **Configuration :** Maintenance  \n"
        else:
            report += f"⚠️  **Configuration :** Standard  \n"
            
        if validation.get("issues"):
            report += f"**Issues identifiées :**  \n"
            for issue in validation["issues"]:
                report += f"- {issue}  \n"
                
        report += "\\n"
    
    # Recommandations
    report += f"""## 💡 Recommandations

### Actions Immédiates
"""
    
    if success_rate < 100:
        report += f"1. **Compléter migration** des agents non migrés\n"
        
    failing_agents = [v for v in validations if v["status"] == "❌ ÉCHEC"]
    if failing_agents:
        report += f"2. **Corriger échecs** sur {len(failing_agents)} agents\n"
        
    improvable_agents = [v for v in validations if "AMÉLIORABLE" in v["status"]]
    if improvable_agents:
        report += f"3. **Améliorer configuration** sur {len(improvable_agents)} agents\n"
        
    report += f"""
### Actions Préventives
1. **Tests fonctionnels** avec LoggingManager activé
2. **Formation équipe** sur nouveau système
3. **Monitoring continu** des logs de maintenance
4. **Documentation** mise à jour

## 🎉 Conclusion

"""
    
    if success_rate >= 95:
        report += f"**SUCCÈS COMPLET** - La migration a été réalisée avec excellence. Le système de logging unifié est maintenant opérationnel sur l'ensemble des agents de maintenance NextGeneration."
    elif success_rate >= 80:
        report += f"**SUCCÈS PARTIEL** - La migration a été largement réussie avec quelques ajustements mineurs nécessaires."
    else:
        report += f"**MIGRATION INCOMPLÈTE** - Des actions correctives sont nécessaires avant mise en production."
        
    report += f"""

---
*Rapport généré automatiquement par l'outil de validation migration logging*  
*NextGeneration Maintenance Team - {timestamp}*
"""
    
    return report

def main():
    """Point d'entrée principal du script de validation."""
    print("🔍 VALIDATION MIGRATION LOGGING AGENTS MAINTENANCE")
    print("=" * 60)
    
    # Répertoire des agents
    agents_dir = Path(__file__).parent / "agents"
    
    if not agents_dir.exists():
        print(f"❌ Répertoire agents non trouvé: {agents_dir}")
        return False
        
    # Recherche des agents MAINTENANCE
    agent_files = list(agents_dir.glob("agent_MAINTENANCE_*.py"))
    
    if not agent_files:
        print(f"❌ Aucun agent MAINTENANCE trouvé dans: {agents_dir}")
        return False
        
    print(f"📊 Agents trouvés: {len(agent_files)}")
    
    # Validation de chaque agent
    validations = []
    for agent_file in sorted(agent_files):
        print(f"🔍 Validation: {agent_file.name}")
        validation = validate_agent_logging(agent_file)
        validations.append(validation)
        print(f"   {validation['status']}")
    
    # Génération du rapport
    print(f"\\n📋 Génération rapport...")
    report = generate_migration_report(validations)
    
    # Sauvegarde du rapport
    report_file = Path(__file__).parent / f"RAPPORT_VALIDATION_MIGRATION_LOGGING_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report_file.write_text(report, encoding='utf-8')
    
    # Résumé final
    total_agents = len(validations)
    migrated_agents = sum(1 for v in validations if v["migrated"])
    success_rate = (migrated_agents / total_agents) * 100
    
    print(f"\\n{'=' * 60}")
    print(f"📊 VALIDATION TERMINÉE")
    print(f"{'=' * 60}")
    print(f"✅ Agents validés: {migrated_agents}/{total_agents}")
    print(f"📊 Taux de succès: {success_rate:.1f}%")
    print(f"📄 Rapport sauvegardé: {report_file}")
    
    if success_rate >= 95:
        print(f"🎉 VALIDATION RÉUSSIE!")
        return True
    else:
        print(f"⚠️  Validation partielle. Voir rapport pour détails.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)