#!/usr/bin/env python3
"""
STANDARDISATION FORMATS RAPPORTS - AGENTS MAINTENANCE
=====================================================

Script pour aligner les formats de rapports sur le standard de qualité
établi par l'agent 06 spécialiste monitoring.

Author: Équipe Standardisation NextGeneration
Version: 1.0.0
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

# Standard de référence basé sur agent_06
STANDARD_HEADER_TEMPLATE = '''# 📊 **RAPPORT {category} : {title}**

**Date :** {date}
**Module :** {module}
**Score Global** : {score}/10
**Niveau Qualité** : {quality_level}
**Conformité** : {conformity}
**Issues Critiques** : {critical_issues}

## 🏗️ Architecture et Contexte
{architecture_context}

## 📊 Métriques et KPIs
{metrics_kpis}

## 🔍 Analyse Détaillée
{detailed_analysis}

## 🎯 Recommandations Stratégiques
{strategic_recommendations}

## 📈 Impact Business
{business_impact}

---

*Rapport {category} généré par {module} - {date}*
*📂 Sauvegardé dans : {save_path}*
'''

class ReportStandardizer:
    """Standardisateur de formats de rapports selon référentiel agent 06."""
    
    def __init__(self):
        self.agents_dir = Path(__file__).parent / "agents"
        self.reports_dir = Path(__file__).parent / "reports"
        
        # Agents qui génèrent des rapports
        self.report_generating_agents = [
            "agent_MAINTENANCE_00_chef_equipe_coordinateur.py",
            "agent_MAINTENANCE_05_documenteur_peer_reviewer.py", 
            "agent_MAINTENANCE_08_analyseur_performance.py",
            "agent_MAINTENANCE_09_analyseur_securite.py",
            "agent_MAINTENANCE_10_auditeur_qualite_normes.py"
        ]
        
        # Patterns de détection de rapports non-conformes
        self.non_conforming_patterns = [
            r'# Rapport de Mission',  # Format simple
            r'lines\.append\(.*\)',    # Génération manuelle
            r'f".*{.*}"',             # Templates non-standardisés
        ]
    
    def analyze_current_report_formats(self) -> Dict[str, List[str]]:
        """Analyse les formats de rapports actuels."""
        print("🔍 ANALYSE FORMATS RAPPORTS ACTUELS")
        print("=" * 60)
        
        non_conforming_agents = {}
        
        for agent_file in self.report_generating_agents:
            agent_path = self.agents_dir / agent_file
            
            if not agent_path.exists():
                print(f"⚠️  Agent non trouvé: {agent_file}")
                continue
                
            print(f"\n📋 Analyse: {agent_file}")
            issues = self._check_agent_report_format(agent_path)
            
            if issues:
                non_conforming_agents[agent_file] = issues
                print(f"   ❌ {len(issues)} problèmes détectés")
                for issue in issues:
                    print(f"      - {issue}")
            else:
                print(f"   ✅ Format conforme")
        
        return non_conforming_agents
    
    def _check_agent_report_format(self, agent_path: Path) -> List[str]:
        """Vérifie la conformité d'un agent aux standards de rapport."""
        try:
            content = agent_path.read_text(encoding='utf-8')
            issues = []
            
            # Vérification présence template standardisé
            if "RAPPORT.*:" not in content and "**Date :**" not in content:
                issues.append("❌ En-tête standardisé manquant")
            
            # Vérification sections obligatoires
            required_sections = [
                "Architecture et Contexte",
                "Métriques et KPIs", 
                "Analyse Détaillée",
                "Recommandations Stratégiques",
                "Impact Business"
            ]
            
            for section in required_sections:
                if section not in content:
                    issues.append(f"❌ Section manquante: {section}")
            
            # Vérification émojis standardisés
            required_emojis = ["🏗️", "📊", "🔍", "🎯", "📈"]
            missing_emojis = [emoji for emoji in required_emojis if emoji not in content]
            
            if missing_emojis:
                issues.append(f"⚠️  Émojis manquants: {', '.join(missing_emojis)}")
            
            # Vérification méthodes génération rapport
            if "def _generer_rapport" in content or "def generate_report" in content:
                if "lines.append" in content:
                    issues.append("⚠️  Génération manuelle vs template standardisé")
            
            return issues
            
        except Exception as e:
            return [f"❌ Erreur analyse: {e}"]
    
    def generate_standard_template_methods(self) -> str:
        """Génère les méthodes standardisées pour la génération de rapports."""
        
        return '''
    def _generate_standard_report(self, category: str, title: str, data: Dict[str, Any]) -> str:
        """Génère un rapport conforme au standard agent 06."""
        
        timestamp = datetime.now()
        
        # Calcul automatique du score et niveau qualité
        score = self._calculate_report_score(data)
        quality_level = self._determine_quality_level(score)
        conformity = self._assess_conformity(data)
        critical_issues = self._count_critical_issues(data)
        
        # Génération contenu par section
        architecture_context = self._generate_architecture_context(data)
        metrics_kpis = self._generate_metrics_kpis(data)
        detailed_analysis = self._generate_detailed_analysis(data)
        strategic_recommendations = self._generate_strategic_recommendations(data)
        business_impact = self._generate_business_impact(data)
        
        # Application du template standard
        report = f"""# 📊 **RAPPORT {category.upper()} : {title}**

**Date :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
**Module :** {self.__class__.__name__}
**Score Global** : {score}/10
**Niveau Qualité** : {quality_level}
**Conformité** : {conformity}
**Issues Critiques** : {critical_issues}

## 🏗️ Architecture et Contexte
{architecture_context}

## 📊 Métriques et KPIs
{metrics_kpis}

## 🔍 Analyse Détaillée
{detailed_analysis}

## 🎯 Recommandations Stratégiques
{strategic_recommendations}

## 📈 Impact Business
{business_impact}

---

*Rapport {category} généré par {self.__class__.__name__} - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}*
*📂 Sauvegardé dans : {self._get_report_save_path(category, title)}*
"""
        
        return report
    
    def _calculate_report_score(self, data: Dict[str, Any]) -> float:
        """Calcule le score global du rapport basé sur les données."""
        # Logique de scoring adaptée aux données
        base_score = 8.0
        
        # Bonus pour complétude des données
        if data.get('metrics'):
            base_score += 0.5
        if data.get('recommendations'):
            base_score += 0.5
        if data.get('analysis'):
            base_score += 0.5
        if data.get('business_impact'):
            base_score += 0.5
            
        return min(10.0, base_score)
    
    def _determine_quality_level(self, score: float) -> str:
        """Détermine le niveau de qualité basé sur le score."""
        if score >= 9.0:
            return "OPTIMAL"
        elif score >= 8.0:
            return "EXCELLENT"
        elif score >= 7.0:
            return "BON"
        elif score >= 6.0:
            return "MOYEN"
        else:
            return "INSUFFISANT"
    
    def _assess_conformity(self, data: Dict[str, Any]) -> str:
        """Évalue la conformité aux standards."""
        conformity_score = 0
        total_checks = 5
        
        # Checks de conformité
        if data.get('architecture_documented'):
            conformity_score += 1
        if data.get('metrics_available'):
            conformity_score += 1
        if data.get('analysis_complete'):
            conformity_score += 1
        if data.get('recommendations_actionable'):
            conformity_score += 1
        if data.get('business_impact_quantified'):
            conformity_score += 1
            
        conformity_rate = conformity_score / total_checks
        
        if conformity_rate >= 0.9:
            return "✅ CONFORME"
        elif conformity_rate >= 0.7:
            return "⚠️ PARTIELLEMENT CONFORME"
        else:
            return "❌ NON CONFORME"
    
    def _count_critical_issues(self, data: Dict[str, Any]) -> int:
        """Compte les issues critiques dans les données."""
        critical_count = 0
        
        issues = data.get('issues', [])
        for issue in issues:
            if isinstance(issue, dict) and issue.get('severity') == 'CRITICAL':
                critical_count += 1
            elif isinstance(issue, str) and 'CRITICAL' in issue.upper():
                critical_count += 1
                
        return critical_count
'''
    
    def create_template_integration_script(self) -> str:
        """Crée un script d'intégration des templates dans les agents."""
        
        integration_script = f'''#!/usr/bin/env python3
"""
SCRIPT INTÉGRATION TEMPLATES RAPPORTS STANDARDISÉS
=================================================

Intègre les méthodes de génération de rapports standardisées
dans les agents de maintenance selon le référentiel agent 06.

Généré automatiquement le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

import sys
from pathlib import Path

# Méthodes standardisées à intégrer
STANDARD_METHODS = """{self.generate_standard_template_methods()}"""

# Agents à mettre à jour
AGENTS_TO_UPDATE = {self.report_generating_agents}

def integrate_standard_methods():
    \"\"\"Intègre les méthodes standardisées dans les agents.\"\"\"
    
    agents_dir = Path(__file__).parent / "agents"
    
    for agent_file in AGENTS_TO_UPDATE:
        agent_path = agents_dir / agent_file
        
        if not agent_path.exists():
            print(f"⚠️  Agent non trouvé: {{agent_file}}")
            continue
            
        print(f"🔧 Mise à jour: {{agent_file}}")
        
        # Lecture contenu actuel
        content = agent_path.read_text(encoding='utf-8')
        
        # Vérification si déjà intégré
        if "_generate_standard_report" in content:
            print(f"   ✅ Déjà mis à jour")
            continue
            
        # Recherche point d'insertion (avant dernière méthode)
        lines = content.split('\\n')
        insertion_point = -1
        
        for i, line in enumerate(lines):
            if line.strip().startswith('def ') and i > len(lines) - 50:
                insertion_point = i
                break
                
        if insertion_point == -1:
            print(f"   ❌ Point d'insertion non trouvé")
            continue
            
        # Insertion des méthodes standardisées
        lines.insert(insertion_point, STANDARD_METHODS)
        
        # Sauvegarde
        agent_path.write_text('\\n'.join(lines), encoding='utf-8')
        print(f"   ✅ Méthodes standardisées intégrées")

if __name__ == "__main__":
    integrate_standard_methods()
'''
        
        return integration_script
    
    def generate_migration_recommendations(self, non_conforming_agents: Dict[str, List[str]]) -> str:
        """Génère des recommandations de migration pour chaque agent."""
        
        recommendations = []
        recommendations.append("# 📋 RECOMMANDATIONS MIGRATION FORMATS RAPPORTS")
        recommendations.append("=" * 60)
        recommendations.append("")
        
        if not non_conforming_agents:
            recommendations.append("✅ **TOUS LES AGENTS SONT CONFORMES**")
            recommendations.append("Aucune action requise.")
            return "\n".join(recommendations)
        
        recommendations.append(f"⚠️  **{len(non_conforming_agents)} AGENTS NÉCESSITENT UNE MISE À JOUR**")
        recommendations.append("")
        
        for agent_file, issues in non_conforming_agents.items():
            recommendations.append(f"## 🔧 {agent_file}")
            recommendations.append("")
            
            # Priorité des actions
            critical_issues = [i for i in issues if "❌" in i]
            warning_issues = [i for i in issues if "⚠️" in i]
            
            if critical_issues:
                recommendations.append("### ⚡ Actions Critiques")
                for issue in critical_issues:
                    recommendations.append(f"- {issue}")
                recommendations.append("")
            
            if warning_issues:
                recommendations.append("### 📝 Améliorations Recommandées")
                for issue in warning_issues:
                    recommendations.append(f"- {issue}")
                recommendations.append("")
            
            # Actions spécifiques par agent
            if "05_documenteur" in agent_file:
                recommendations.append("**Actions spécifiques:**")
                recommendations.append("1. Remplacer `_generer_rapport_md_enrichi()` par `_generate_standard_report()`")
                recommendations.append("2. Intégrer calcul automatique score/qualité")
                recommendations.append("3. Ajouter sections Business Impact")
                
            elif "00_chef_equipe" in agent_file:
                recommendations.append("**Actions spécifiques:**")
                recommendations.append("1. Standardiser `_generer_et_sauvegarder_rapports()`")
                recommendations.append("2. Utiliser templates conformes agent 06")
                recommendations.append("3. Ajouter métriques stratégiques")
                
            elif "10_auditeur" in agent_file:
                recommendations.append("**Actions spécifiques:**")
                recommendations.append("1. Aligner rapports d'audit sur format standard")
                recommendations.append("2. Enrichir section Impact Business")
                recommendations.append("3. Standardiser émojis et structure")
            
            recommendations.append("")
            recommendations.append("---")
            recommendations.append("")
        
        # Plan d'action global
        recommendations.append("## 🎯 PLAN D'ACTION GLOBAL")
        recommendations.append("")
        recommendations.append("### Phase 1: Intégration Templates (1-2 jours)")
        recommendations.append("1. Exécuter script d'intégration des méthodes standardisées")
        recommendations.append("2. Mettre à jour les appels de génération de rapports")
        recommendations.append("3. Tester génération avec nouveau format")
        recommendations.append("")
        
        recommendations.append("### Phase 2: Validation Qualité (1 jour)")
        recommendations.append("1. Générer rapports test avec tous les agents")
        recommendations.append("2. Valider conformité au standard agent 06")
        recommendations.append("3. Ajuster calculs de score si nécessaire")
        recommendations.append("")
        
        recommendations.append("### Phase 3: Documentation (0.5 jour)")
        recommendations.append("1. Mettre à jour guides utilisateur")
        recommendations.append("2. Former équipe aux nouveaux standards")
        recommendations.append("3. Documenter processus qualité")
        
        return "\n".join(recommendations)
    
    def run_analysis(self):
        """Exécute l'analyse complète et génère les recommandations."""
        print("🚀 STANDARDISATION FORMATS RAPPORTS - AGENTS MAINTENANCE")
        print("=" * 70)
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("")
        
        # Analyse des formats actuels
        non_conforming_agents = self.analyze_current_report_formats()
        
        # Génération des recommandations
        print(f"\n📋 Génération recommandations...")
        recommendations = self.generate_migration_recommendations(non_conforming_agents)
        
        # Sauvegarde
        recommendations_file = Path(__file__).parent / f"RECOMMANDATIONS_STANDARDISATION_RAPPORTS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        recommendations_file.write_text(recommendations, encoding='utf-8')
        
        # Script d'intégration
        integration_script = self.create_template_integration_script()
        integration_file = Path(__file__).parent / "integrate_standard_report_templates.py"
        integration_file.write_text(integration_script, encoding='utf-8')
        
        # Rapport final
        print(f"\n{'=' * 70}")
        print(f"📊 ANALYSE TERMINÉE")
        print(f"{'=' * 70}")
        print(f"✅ Agents analysés: {len(self.report_generating_agents)}")
        print(f"⚠️  Agents non-conformes: {len(non_conforming_agents)}")
        print(f"📄 Recommandations: {recommendations_file}")
        print(f"🔧 Script intégration: {integration_file}")
        
        if len(non_conforming_agents) == 0:
            print(f"🎉 TOUS LES FORMATS SONT CONFORMES!")
            return True
        else:
            print(f"⚠️  Standardisation requise sur {len(non_conforming_agents)} agents")
            return False

def main():
    standardizer = ReportStandardizer()
    success = standardizer.run_analysis()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())