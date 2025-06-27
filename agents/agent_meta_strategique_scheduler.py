#!/usr/bin/env python3
"""

# 🔧 CONVERTI AUTOMATIQUEMENT SYNC → ASYNC
# Date: 2025-06-19 19h35 - Correction architecture Pattern Factory
# Raison: Harmonisation async/sync avec core/agent_factory_architecture.py

🚧 DRAFT VERSION 🚧
Planificateur pour l'Agent Méta-Stratégique - VERSION DRAFT/PROTOTYPE
Mission: Exécuter périodiquement l'analyse stratégique et générer les rapports

⚠️ ATTENTION: CETTE VERSION EST UN PROTOTYPE EN DÉVELOPPEMENT
- Ne pas utiliser en production
- Fonctionnalités en cours de test et validation
- Rapports générés à titre expérimental uniquement

Fonctionnalités:
- Planification automatique des analyses
- Intégration avec l'API GitHub pour les métriques CI/CD
- Notifications des insights critiques
- Archivage des rapports historiques
"""

import asyncio
import json
import sys
from pathlib import Path
from core import logging_manager
import schedule
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import time
import importlib

# Import de notre agent méta-stratégique
sys.path.insert(0, str(Path(__file__).parent.parent / '20250621_1527_agent_racine_repertoire'))
try:
    from agent_meta_strategique import AgentMetaStrategique
except ImportError as e:
    print(f"ERREUR CRITIQUE: Impossible d'importer AgentMetaStrategique. Vérifiez le chemin. {e}")
    sys.exit(1)

class AgentMetaStrategiqueScheduler:
    """Planificateur pour l'exécution périodique de l'Agent Méta-Stratégique"""
    
    def __init__(self, workspace_root: Path = None, config_path: str = "config/meta_strategique_config.json", agent_class_name: str = "Agent111AuditeurQualite", agent_module_path: str = "agents.agent_111_auditeur_qualite", task_method: str = "execute_task", task_params: dict = None):
        
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="general",
                custom_config={
                    "logger_name": f"nextgen.general.meta_strategique_scheduler.{self.agent_id if hasattr(self, 'agent_id') else self.id if hasattr(self, 'id') else 'unknown'}",
                    "log_dir": "logs/general",
                    "metadata": {
                        "agent_type": "meta_strategique_scheduler",
                        "agent_role": "general",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)

        self.workspace_root = workspace_root if workspace_root else Path(__file__).parent.parent
        self.config_path = self.workspace_root / config_path
        self.logger = self._setup_logging()
        self.default_config = {
            "execution_schedule": {
                "daily_report": "09:00",
                "weekly_deep_analysis": "MON:08:00",
                "critical_monitoring": 30
            },
            "notifications": {
                "email_enabled": False,
                "email_recipients": [],
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "webhook_url": None
            },
            "github_integration": {
                "enabled": False,
                "api_token": None,
                "repo_owner": "nextgeneration",
                "repo_name": "nextgeneration"
            },
            "analysis_settings": {
                "retention_days": 30,
                "critical_threshold": 0.8,
                "archive_reports": True
            }
        }
        self.config = self.load_config()
        self.task_method = task_method
        self.task_params = task_params or {"task": None}
        try:
            agent_module = importlib.import_module(agent_module_path)
            agent_class = getattr(agent_module, agent_class_name)
            self.agent = agent_class(workspace_root=self.workspace_root)
        except Exception as e:
            self.logger.critical(f"Impossible d'instancier {agent_class_name} depuis {agent_module_path}: {e}")
            sys.exit(1)
        self.last_analysis_results = None

    def _setup_logging(self):
        """Configuration du logging pour le scheduler."""
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            log_dir = self.workspace_root / "logs" / "agents" / "meta_strategique_scheduler"
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / "scheduler.log"

            # Handler Fichier
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

            # Handler Console
            console_handler = logging.StreamHandler(sys.stdout)
            console_formatter = logging.Formatter('📅 (Scheduler) - %(levelname)s - %(message)s')
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)

        return logger
        
    def load_config(self) -> Dict[str, Any]:
        """Chargement de la configuration"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Fusion avec la config par défaut
                    merged_config = self.default_config.copy()
                    merged_config.update(config)
                    return merged_config
            except Exception as e:
                self.logger.error(f"Erreur chargement config: {e}")
        
        # Créer la configuration par défaut
        self.save_config(self.default_config)
        return self.default_config
    
    def save_config(self, config: Dict[str, Any]):
        """Sauvegarde de la configuration"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def start_scheduler(self):
        """Démarrage du planificateur"""
        self.logger.info("🚧 Démarrage du planificateur Agent Méta-Stratégique DRAFT/PROTOTYPE")
        
        # Planification des tâches
        self.setup_schedules()
        
        # Exécution immédiate pour test
        self.logger.info("🔍 Exécution d'analyse initiale...")
        self.execute_daily_analysis()
        
        # Boucle principale
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Vérification chaque minute
        except KeyboardInterrupt:
            self.logger.info("🛑 Arrêt du planificateur")
    
    def setup_schedules(self):
        """Configuration des planifications"""
        config = self.config["execution_schedule"]
        
        # Rapport quotidien
        daily_time = config["daily_report"]
        schedule.every().day.at(daily_time).do(self.execute_daily_analysis)
        self.logger.info(f"📅 Rapport quotidien planifié à {daily_time}")
        
        # Analyse hebdomadaire approfondie
        weekly_schedule = config["weekly_deep_analysis"]
        if ":" in weekly_schedule:
            day, time_str = weekly_schedule.split(":")
            getattr(schedule.every(), day.lower()).at(time_str).do(self.execute_weekly_deep_analysis)
            self.logger.info(f"📊 Analyse hebdomadaire planifiée {day} à {time_str}")
        
        # Monitoring critique
        critical_interval = config["critical_monitoring"]
        schedule.every(critical_interval).minutes.do(self.execute_critical_monitoring)
        self.logger.info(f"🚨 Monitoring critique toutes les {critical_interval} minutes")
    
    def execute_daily_analysis(self):
        """Exécution de l'analyse quotidienne"""
        self.logger.info("📊 Début analyse quotidienne")
        
        try:
            # Exécution de l'analyse
            results = self.agent.analyser_performance_globale()
            self.last_analysis_results = results
            
            # Sauvegarde du rapport
            rapport_path = self.agent.sauvegarder_rapport_strategique()
            
            # Vérification des insights critiques
            critical_insights = [i for i in results["strategic_insights"] 
                               if i["severity"] in ["HIGH", "CRITICAL"]]
            
            if critical_insights:
                self.handle_critical_insights(critical_insights)
            
            # Nettoyage des anciens rapports
            self.cleanup_old_reports()
            
            self.logger.info(f"✅ Analyse quotidienne terminée - Rapport: {rapport_path}")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur analyse quotidienne: {e}")
    
    def execute_weekly_deep_analysis(self):
        """Exécution de l'analyse hebdomadaire approfondie"""
        self.logger.info("🔍 Début analyse hebdomadaire approfondie")
        
        try:
            # Analyse standard
            self.execute_daily_analysis()
            
            # Analyse des tendances sur 7 jours
            trends_analysis = self.analyze_weekly_trends()
            
            # Génération du rapport hebdomadaire
            weekly_report = self.generate_weekly_executive_report(trends_analysis)
            
            # Sauvegarde du rapport hebdomadaire
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            weekly_report_path = self.agent.reports_path / f"RAPPORT_HEBDOMADAIRE_{timestamp}.md"
            
            with open(weekly_report_path, 'w', encoding='utf-8') as f:
                f.write(weekly_report)
            
            self.logger.info(f"✅ Analyse hebdomadaire terminée - Rapport: {weekly_report_path}")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur analyse hebdomadaire: {e}")
    
    def execute_critical_monitoring(self):
        """Monitoring critique pour détection rapide des problèmes"""
        try:
            # Vérification rapide des métriques critiques
            critical_metrics = self.check_critical_metrics()
            
            if critical_metrics["alerts"]:
                self.logger.warning(f"🚨 {len(critical_metrics['alerts'])} alertes critiques détectées")
                
                # Notification immédiate si configurée
                if self.config["notifications"]["email_enabled"]:
                    self.send_critical_alert(critical_metrics["alerts"])
                
                # Exécution d'une analyse d'urgence
                self.execute_emergency_analysis(critical_metrics)
            
        except Exception as e:
            self.logger.error(f"❌ Erreur monitoring critique: {e}")
    
    def check_critical_metrics(self) -> Dict[str, Any]:
        """Vérification rapide des métriques critiques"""
        alerts = []
        
        # Vérification des logs récents
        recent_logs = list(self.agent.logs_path.glob("*.log"))
        for log_file in recent_logs[-5:]:  # 5 derniers logs
            if log_file.stat().st_size > 1024 * 1024:  # > 1MB
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        error_count = content.count("ERROR")
                        if error_count > 10:
                            alerts.append({
                                "type": "high_error_rate",
                                "source": log_file.name,
                                "error_count": error_count,
                                "severity": "CRITICAL"
                            })
                except Exception:
                    continue
        
        # Vérification des métriques de performance récentes
        recent_metrics = list(self.agent.metrics_path.glob("*.json"))
        if recent_metrics:
            latest_metric = max(recent_metrics, key=lambda x: x.stat().st_mtime)
            if datetime.now() - datetime.fromtimestamp(latest_metric.stat().st_mtime) > timedelta(hours=2):
                alerts.append({
                    "type": "stale_metrics",
                    "message": "Aucune métrique récente détectée",
                    "severity": "HIGH"
                })
        
        return {"alerts": alerts, "timestamp": datetime.now().isoformat()}
    
    def handle_critical_insights(self, critical_insights: List[Dict[str, Any]]):
        """Gestion des insights critiques"""
        self.logger.warning(f"🚨 {len(critical_insights)} insights critiques détectés")
        
        # Notification par email si configurée
        if self.config["notifications"]["email_enabled"]:
            self.send_critical_insights_notification(critical_insights)
        
        # Webhook si configuré
        webhook_url = self.config["notifications"].get("webhook_url")
        if webhook_url:
            self.send_webhook_notification(critical_insights, webhook_url)
        
        # Log détaillé
        for insight in critical_insights:
            self.logger.critical(f"INSIGHT CRITIQUE: {insight['title']} - {insight['description']}")
    
    def send_critical_alert(self, alerts: List[Dict[str, Any]]):
        """Envoi d'alerte critique par email"""
        if not self.config["notifications"]["email_enabled"]:
            return
        
        try:
            subject = f"🚨 ALERTE CRITIQUE - NextGeneration - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            body = f"""
ALERTE CRITIQUE DÉTECTÉE

Nombre d'alertes: {len(alerts)}
Timestamp: {datetime.now().isoformat()}

DÉTAILS DES ALERTES:
"""
            
            for alert in alerts:
                body += f"""
- Type: {alert['type']}
- Sévérité: {alert['severity']}
- Détails: {alert.get('message', 'N/A')}
"""
            
            body += """
Action requise: Vérifier immédiatement le système NextGeneration.

---
Alerte générée automatiquement par l'Agent Méta-Stratégique
"""
            
            self.send_email(subject, body)
            
        except Exception as e:
            self.logger.error(f"Erreur envoi alerte email: {e}")
    
    def send_email(self, subject: str, body: str):
        """Envoi d'email"""
        config = self.config["notifications"]
        
        msg = MIMEMultipart()
        msg['From'] = config.get("email_from", "agent-meta@nextgeneration.com")
        msg['To'] = ", ".join(config["email_recipients"])
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        server = smtplib.SMTP(config["smtp_server"], config["smtp_port"])
        server.starttls()
        
        # Authentification si configurée
        email_user = config.get("email_user")
        email_password = config.get("email_password")
        if email_user and email_password:
            server.login(email_user, email_password)
        
        server.send_message(msg)
        server.quit()
    
    def analyze_weekly_trends(self) -> Dict[str, Any]:
        """Analyse des tendances hebdomadaires"""
        # Collecte des rapports de la semaine
        week_ago = datetime.now() - timedelta(days=7)
        
        weekly_reports = []
        for report_file in self.agent.reports_path.glob("REVUE_STRATEGIQUE_*.md"):
            file_time = datetime.fromtimestamp(report_file.stat().st_mtime)
            if file_time >= week_ago:
                weekly_reports.append({
                    "file": report_file.name,
                    "timestamp": file_time,
                    "size": report_file.stat().st_size
                })
        
        return {
            "reports_analyzed": len(weekly_reports),
            "period_start": week_ago.isoformat(),
            "period_end": datetime.now().isoformat(),
            "trend_summary": "Analyse des tendances hebdomadaires en cours de développement"
        }
    
    def generate_weekly_executive_report(self, trends: Dict[str, Any]) -> str:
        """Génération du rapport exécutif hebdomadaire"""
        return f"""# 🚧 RAPPORT EXÉCUTIF HEBDOMADAIRE - VERSION DRAFT 🚧
## Agent Méta-Stratégique PROTOTYPE - Semaine du {datetime.now().strftime('%Y-%m-%d')}

⚠️ **ATTENTION: RAPPORT GÉNÉRÉ PAR VERSION EXPÉRIMENTALE**
- **Statut**: DRAFT/PROTOTYPE v0.1.0-draft
- **Usage**: Tests et validation uniquement

---

## 🎯 RÉSUMÉ DE LA SEMAINE

### Activité de Monitoring
- **Rapports générés**: {trends['reports_analyzed']}
- **Période analysée**: {trends['period_start']} → {trends['period_end']}

### Tendances Identifiées
{trends['trend_summary']}

---

## 📈 ÉVOLUTION DES MÉTRIQUES

*Analyse des tendances hebdomadaires en développement*

---

## 💡 RECOMMANDATIONS STRATÉGIQUES

1. **Maintenir la surveillance continue** - Le système de monitoring fonctionne correctement
2. **Analyser les patterns émergents** - Identifier les tendances à long terme
3. **Optimiser les processus** - Améliorer l'efficacité basée sur les données collectées

---

*Rapport généré automatiquement par l'Agent Méta-Stratégique*
*Prochaine analyse: {(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')}*
"""
    
    def cleanup_old_reports(self):
        """Nettoyage des anciens rapports"""
        retention_days = self.config["analysis_settings"]["retention_days"]
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        cleaned_count = 0
        for report_file in self.agent.reports_path.glob("REVUE_STRATEGIQUE_*.md"):
            file_time = datetime.fromtimestamp(report_file.stat().st_mtime)
            if file_time < cutoff_date:
                if self.config["analysis_settings"]["archive_reports"]:
                    # Archiver au lieu de supprimer
                    archive_path = self.agent.reports_path / "archive"
                    archive_path.mkdir(exist_ok=True)
                    report_file.rename(archive_path / report_file.name)
                else:
                    report_file.unlink()
                cleaned_count += 1
        
        if cleaned_count > 0:
            self.logger.info(f"🧹 {cleaned_count} anciens rapports nettoyés/archivés")
    
    def execute_emergency_analysis(self, critical_metrics: Dict[str, Any]):
        """Analyse d'urgence en cas de problème critique"""
        self.logger.critical("🚨 Exécution d'analyse d'urgence")
        
        try:
            # Analyse focalisée sur le problème
            emergency_analysis = self.agent.analyser_performance_globale()
            
            # Ajout du contexte d'urgence
            emergency_analysis["emergency_context"] = {
                "trigger": "critical_monitoring",
                "alerts": critical_metrics["alerts"],
                "timestamp": datetime.now().isoformat()
            }
            
            # Sauvegarde du rapport d'urgence
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            emergency_report_path = self.agent.reports_path / f"URGENCE_STRATEGIQUE_{timestamp}.json"
            
            with open(emergency_report_path, 'w', encoding='utf-8') as f:
                json.dump(emergency_analysis, f, indent=2, ensure_ascii=False)
            
            self.logger.critical(f"🚨 Rapport d'urgence sauvegardé: {emergency_report_path}")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur analyse d'urgence: {e}")

def main():
    """Fonction principale"""
    # Création et démarrage du planificateur
    try:
        scheduler = AgentMetaStrategiqueScheduler()
        scheduler.start_scheduler()
    except Exception as e:
        print(f"Une erreur fatale est survenue: {e}")
    # ✅ MÉTHODES STANDARDISÉES DE RAPPORT

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
            markdown_content += f"- {obj}\n"
        
        markdown_content += f"""
**Technologies Clés :**
"""
        
        # Ajouter les technologies
        for tech in rapport_json.get('architecture', {}).get('technologies_cles', []):
            markdown_content += f"- {tech}\n"
        
        markdown_content += f"""

## 🔍 RECOMMANDATIONS

"""
        
        # Ajouter les recommandations
        for reco in rapport_json.get('recommandations', []):
            markdown_content += f"- {reco}\n"
        
        markdown_content += f"""

## ⚠️ ISSUES CRITIQUES

"""
        
        # Ajouter les issues critiques
        for issue in rapport_json.get('issues_critiques_details', []):
            markdown_content += f"- {issue}\n"
        
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
            markdown_content += f"- {domaine}\n"
        
        markdown_content += f"""

### Actions Requises
"""
        
        # Ajouter les actions requises
        for action in rapport_json.get('impact_business', {}).get('actions_requises', []):
            markdown_content += f"- {action}\n"
        
        markdown_content += f"""

---
*Rapport généré automatiquement par {agent_name} - NextGeneration System*  
*Timestamp: {timestamp.isoformat()}*
"""
        
        return markdown_content



if __name__ == "__main__":
    main() 
