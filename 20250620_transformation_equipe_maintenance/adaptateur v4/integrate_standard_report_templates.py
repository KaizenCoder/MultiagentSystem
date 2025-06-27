#!/usr/bin/env python3
"""
SCRIPT INTÉGRATION TEMPLATES RAPPORTS STANDARDISÉS
=================================================

Intègre les méthodes de génération de rapports standardisées
dans les agents de maintenance selon le référentiel agent 06.

Généré automatiquement le 2025-06-27 15:51:06
"""

import sys
from pathlib import Path

# Méthodes standardisées à intégrer
STANDARD_METHODS = """
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
"""

# Agents à mettre à jour
AGENTS_TO_UPDATE = ['agent_MAINTENANCE_00_chef_equipe_coordinateur.py', 'agent_MAINTENANCE_05_documenteur_peer_reviewer.py', 'agent_MAINTENANCE_08_analyseur_performance.py', 'agent_MAINTENANCE_09_analyseur_securite.py', 'agent_MAINTENANCE_10_auditeur_qualite_normes.py']

def integrate_standard_methods():
    """Intègre les méthodes standardisées dans les agents."""
    
    agents_dir = Path(__file__).parent / "agents"
    
    for agent_file in AGENTS_TO_UPDATE:
        agent_path = agents_dir / agent_file
        
        if not agent_path.exists():
            print(f"⚠️  Agent non trouvé: {agent_file}")
            continue
            
        print(f"🔧 Mise à jour: {agent_file}")
        
        # Lecture contenu actuel
        content = agent_path.read_text(encoding='utf-8')
        
        # Vérification si déjà intégré
        if "_generate_standard_report" in content:
            print(f"   ✅ Déjà mis à jour")
            continue
            
        # Recherche point d'insertion (avant dernière méthode)
        lines = content.split('\n')
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
        agent_path.write_text('\n'.join(lines), encoding='utf-8')
        print(f"   ✅ Méthodes standardisées intégrées")

if __name__ == "__main__":
    integrate_standard_methods()
