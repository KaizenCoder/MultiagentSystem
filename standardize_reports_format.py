#!/usr/bin/env python3
"""
Script de standardisation des formats de rapports selon l'agent 06.
Applique le format standard à tous les agents générant des rapports.
"""
import os
import re
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

def backup_file(file_path: Path) -> str:
    """Crée une sauvegarde du fichier original."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup_reports_{timestamp}"
    shutil.copy2(file_path, backup_path)
    return backup_path

def detect_report_methods(content: str) -> List[str]:
    """Détecte les méthodes de génération de rapports dans un agent."""
    report_methods = []
    
    # Patterns de méthodes de rapport
    patterns = [
        r'def\s+(.*rapport.*)\(',
        r'def\s+(.*report.*)\(',
        r'def\s+(generer.*)\(',
        r'def\s+(generate.*)\(',
        r'def\s+(.*validation.*)\(',
        r'def\s+(.*audit.*)\(',
        r'def\s+(.*analyse.*)\(',
        r'def\s+(.*analysis.*)\(',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        report_methods.extend(matches)
    
    return list(set(report_methods))

def generate_standard_report_structure() -> str:
    """Génère la structure standard de rapport selon l'agent 06."""
    
    return '''
    def _calculate_report_score(self, metrics: Dict[str, Any]) -> int:
        """Calcule le score global du rapport basé sur les métriques."""
        score = 0
        issues_critiques = []
        
        # Logique de scoring spécifique à l'agent
        # À adapter selon le type d'agent
        
        return score
    
    def _assess_conformity(self, score: int) -> str:
        """Évalue la conformité basée sur le score."""
        if score >= 90:
            return "✅ CONFORME - OPTIMAL"
        elif score >= 70:
            return "✅ CONFORME - ACCEPTABLE"
        else:
            return "❌ NON CONFORME - CRITIQUE"
    
    def _get_quality_level(self, score: int) -> str:
        """Détermine le niveau de qualité."""
        if score >= 90:
            return "OPTIMAL"
        elif score >= 70:
            return "ACCEPTABLE"
        else:
            return "CRITIQUE"
    
    def _generate_recommendations(self, metrics: Dict[str, Any], issues: List[str]) -> List[str]:
        """Génère les recommandations basées sur l'analyse."""
        recommendations = []
        
        # Logique de génération de recommandations
        # À adapter selon le type d'agent
        
        return recommendations
    
    def _generate_standard_report(self, context: Dict, metrics: Dict, timestamp) -> Dict[str, Any]:
        """Génère un rapport selon le format standard de l'agent 06."""
        
        score = self._calculate_report_score(metrics)
        conformity = self._assess_conformity(score)
        quality_level = self._get_quality_level(score)
        
        agent_filename = Path(__file__).name
        
        # Issues critiques (à personnaliser selon l'agent)
        issues_critiques = []
        
        return {
            'agent_id': getattr(self, 'agent_id', 'unknown'),
            'agent_file_name': agent_filename,
            'type_rapport': 'standard',  # À personnaliser
            'timestamp': timestamp.isoformat(),
            'specialisation': 'Agent Spécialisé',  # À personnaliser
            'score_global': score,
            'niveau_qualite': quality_level,
            'conformite': conformity,
            'signature_cryptographique': 'N/A (Fonctionnalité non implémentée pour cet agent)',
            'issues_critiques_identifies': len(issues_critiques),
            'architecture': {
                'description': "Description de l'architecture de l'agent",
                'statut_operationnel': f"Système {getattr(self, 'agent_id', 'unknown')} opérationnel.",
                'confirmation_specialisation': f"{getattr(self, 'agent_id', 'unknown')} confirmé comme spécialiste.",
                'objectifs_principaux': [
                    "Objectif principal 1",
                    "Objectif principal 2",
                    "Objectif principal 3"
                ],
                'technologies_cles': ["Technologie 1", "Technologie 2"]
            },
            'recommandations': self._generate_recommendations(metrics, issues_critiques),
            'issues_critiques_details': issues_critiques if issues_critiques else [
                "Aucun issue critique majeur détecté. Le système fonctionne dans les paramètres attendus."
            ],
            'details_techniques': {
                'strategie': "Stratégie technique de l'agent",
                'composants_actifs': [],
                'metriques_collectees': metrics
            },
            'metriques_detaillees': {
                'score_global': {'actuel': score, 'cible': 100},
                'conformite_pourcentage': {'actuel': score, 'cible': 100, 'unite': '%'}
            },
            'impact_business': {
                'criticite': 'MOYENNE' if score >= 70 else 'HAUTE',
                'domaines_impactes': [],
                'actions_requises': []
            }
        }
'''

def generate_markdown_report_method() -> str:
    """Génère la méthode de génération de rapport Markdown standard."""
    
    return '''
    def _generate_markdown_report(self, rapport_json: Dict, context: Dict, timestamp) -> str:
        """Génère un rapport Markdown selon le format standard."""
        
        agent_name = rapport_json.get('agent_id', 'Agent Inconnu')
        type_rapport = rapport_json.get('type_rapport', 'standard')
        score = rapport_json.get('score_global', 0)
        quality = rapport_json.get('niveau_qualite', 'UNKNOWN')
        conformity = rapport_json.get('conformite', 'NON ÉVALUÉ')
        
        markdown_content = f"""# 📊 RAPPORT STRATÉGIQUE : {agent_name.upper()}

## 🎯 RÉSUMÉ EXÉCUTIF

**Agent :** {agent_name}  
**Type de Rapport :** {type_rapport}  
**Date de Génération :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Score Global :** {score}/100  
**Niveau de Qualité :** {quality}  
**Conformité :** {conformity}  

## 📈 ANALYSE GLOBALE

### Score de Performance
- **Score Actuel :** {score}/100
- **Objectif :** 100/100
- **Statut :** {'🟢 ACCEPTABLE' if score >= 70 else '🔴 CRITIQUE'}

### Architecture
{rapport_json.get('architecture', {}).get('description', 'Description non disponible')}

**Objectifs Principaux :**
"""
        
        # Ajouter les objectifs
        for obj in rapport_json.get('architecture', {}).get('objectifs_principaux', []):
            markdown_content += f"- {obj}\\n"
        
        markdown_content += f"""
**Technologies Clés :**
"""
        
        # Ajouter les technologies
        for tech in rapport_json.get('architecture', {}).get('technologies_cles', []):
            markdown_content += f"- {tech}\\n"
        
        markdown_content += f"""

## 🔍 RECOMMANDATIONS

"""
        
        # Ajouter les recommandations
        for reco in rapport_json.get('recommandations', []):
            markdown_content += f"- {reco}\\n"
        
        markdown_content += f"""

## ⚠️ ISSUES CRITIQUES

"""
        
        # Ajouter les issues critiques
        for issue in rapport_json.get('issues_critiques_details', []):
            markdown_content += f"- {issue}\\n"
        
        markdown_content += f"""

## 📊 MÉTRIQUES DÉTAILLÉES

### Performance Globale
- **Score Global :** {rapport_json.get('metriques_detaillees', {}).get('score_global', {}).get('actuel', 0)}/{rapport_json.get('metriques_detaillees', {}).get('score_global', {}).get('cible', 100)}
- **Conformité :** {rapport_json.get('metriques_detaillees', {}).get('conformite_pourcentage', {}).get('actuel', 0)}%

## 🎯 IMPACT BUSINESS

**Criticité :** {rapport_json.get('impact_business', {}).get('criticite', 'NON ÉVALUÉ')}

### Domaines Impactés
"""
        
        # Ajouter les domaines impactés
        for domaine in rapport_json.get('impact_business', {}).get('domaines_impactes', []):
            markdown_content += f"- {domaine}\\n"
        
        markdown_content += f"""

### Actions Requises
"""
        
        # Ajouter les actions requises
        for action in rapport_json.get('impact_business', {}).get('actions_requises', []):
            markdown_content += f"- {action}\\n"
        
        markdown_content += f"""

---
*Rapport généré automatiquement par {agent_name} - NextGeneration System*  
*Timestamp: {timestamp.isoformat()}*
"""
        
        return markdown_content
'''

def analyze_agent_for_reports(file_path: Path) -> Dict[str, Any]:
    """Analyse un agent pour détecter s'il génère des rapports."""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {"error": f"Erreur lecture fichier: {str(e)}"}
    
    analysis = {
        "file_name": file_path.name,
        "has_reports": False,
        "report_methods": [],
        "needs_standardization": False,
        "current_format": "unknown"
    }
    
    # Détecter les méthodes de rapport
    report_methods = detect_report_methods(content)
    analysis["report_methods"] = report_methods
    
    if report_methods:
        analysis["has_reports"] = True
        
        # Vérifier si déjà standardisé
        if "_generate_standard_report" in content:
            analysis["current_format"] = "standard"
        elif "score_global" in content and "conformite" in content:
            analysis["current_format"] = "partial_standard"
            analysis["needs_standardization"] = True
        else:
            analysis["current_format"] = "custom"
            analysis["needs_standardization"] = True
    
    return analysis

def standardize_agent_reports(file_path: Path) -> bool:
    """Standardise les rapports d'un agent selon le format de l'agent 06."""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Créer une sauvegarde
        backup_path = backup_file(file_path)
        print(f"💾 {file_path.name} - Sauvegarde créée: {Path(backup_path).name}")
        
        # Ajouter les méthodes standard si pas présentes
        if "_generate_standard_report" not in content:
            
            # Trouver un bon endroit pour insérer les méthodes
            # Rechercher la fin de la dernière méthode de classe
            class_pattern = r'class\s+\w+.*?:'
            class_match = re.search(class_pattern, content)
            
            if class_match:
                # Insérer avant la dernière ligne de la classe ou avant les tests
                insertion_patterns = [
                    r'\n\n# Test.*',
                    r'\n\nif __name__ == "__main__"',
                    r'\n\ndef test.*',
                    r'\n\nasync def main\(',
                ]
                
                insertion_point = len(content)  # Par défaut à la fin
                
                for pattern in insertion_patterns:
                    match = re.search(pattern, content)
                    if match:
                        insertion_point = match.start()
                        break
                
                # Insérer les méthodes standard
                standard_methods = generate_standard_report_structure()
                markdown_method = generate_markdown_report_method()
                
                new_content = (content[:insertion_point] + 
                              '\n    # ✅ MÉTHODES STANDARDISÉES DE RAPPORT\n' +
                              standard_methods + '\n' +
                              markdown_method + '\n' +
                              content[insertion_point:])
                
                # Écrire le nouveau contenu
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ {file_path.name} - Standardisation réussie")
                return True
            else:
                print(f"❌ {file_path.name} - Impossible de trouver la classe")
                return False
        else:
            print(f"✅ {file_path.name} - Déjà standardisé")
            return True
            
    except Exception as e:
        print(f"❌ {file_path.name} - Erreur: {str(e)}")
        return False

def main():
    """Fonction principale."""
    print("📊 STANDARDISATION DES FORMATS DE RAPPORTS")
    print("=" * 60)
    print("Modèle de référence: agent_06_specialiste_monitoring_sprint4")
    print("")
    
    agents_dir = Path("agents")
    if not agents_dir.exists():
        print("❌ Répertoire agents/ non trouvé!")
        return
    
    # Analyser tous les agents
    agents_with_reports = []
    total_agents = 0
    
    for file_path in agents_dir.glob("agent_*.py"):
        if file_path.is_file():
            total_agents += 1
            analysis = analyze_agent_for_reports(file_path)
            
            if analysis.get("has_reports"):
                agents_with_reports.append(analysis)
    
    print(f"📈 ANALYSE GLOBALE")
    print(f"Total agents analysés: {total_agents}")
    print(f"Agents avec rapports: {len(agents_with_reports)}")
    
    # Agents nécessitant une standardisation
    need_standardization = [a for a in agents_with_reports if a.get("needs_standardization")]
    
    print(f"Agents à standardiser: {len(need_standardization)}")
    print("")
    
    if not need_standardization:
        print("✅ Tous les agents avec rapports sont déjà standardisés!")
        return
    
    # Statistiques par format actuel
    format_stats = {}
    for agent in agents_with_reports:
        fmt = agent.get("current_format", "unknown")
        format_stats[fmt] = format_stats.get(fmt, 0) + 1
    
    print("📊 RÉPARTITION DES FORMATS:")
    for fmt, count in format_stats.items():
        print(f"  {fmt}: {count} agents")
    print("")
    
    # Standardisation
    print("🔧 STANDARDISATION EN COURS...")
    print("-" * 40)
    
    success_count = 0
    failed_count = 0
    
    for agent_analysis in need_standardization:
        file_path = agents_dir / agent_analysis["file_name"]
        
        if standardize_agent_reports(file_path):
            success_count += 1
        else:
            failed_count += 1
    
    print(f"\n📈 RÉSUMÉ STANDARDISATION")
    print("-" * 40)
    print(f"✅ Succès: {success_count}")
    print(f"❌ Échecs: {failed_count}")
    print(f"📊 Total traité: {success_count + failed_count}")
    
    if success_count > 0:
        print(f"\n🎉 Standardisation terminée!")
        print("Les agents peuvent maintenant générer des rapports selon le format uniforme.")

if __name__ == "__main__":
    main()