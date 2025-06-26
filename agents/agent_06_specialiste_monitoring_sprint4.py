#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 AGENT 06 - MONITORING AVANCÉ
Mission: Observabilité distribuée avec OpenTelemetry et Prometheus.
"""
import sys
from pathlib import Path

# Ajout du répertoire parent au path pour résoudre les imports locaux
sys.path.append(str(Path(__file__).resolve().parent.parent))

import asyncio
import logging
from typing import Dict, List, Optional, Any
from core.manager import LoggingManager

from core.agent_factory_architecture import Agent, Task, Result

__version__ = "0.1.0-sprint4"

try:
    from opentelemetry import trace, metrics
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.metrics import MeterProvider
    OPENTELEMETRY_AVAILABLE = True
except ImportError:
    OPENTELEMETRY_AVAILABLE = False


class Agent06AdvancedMonitoring(Agent):
    """
    📊 AGENT 06 - MONITORING AVANCÉ - Version restructurée et fonctionnelle.
    """
    
    def __init__(self, agent_id="agent_06_specialiste_monitoring", agent_type="monitoring", version="0.1.0-sprint4", **kwargs):
        logging_manager = LoggingManager()
        custom_log_config = {
            "logger_name": f"agent.{agent_id}",
            "metadata": {
                "agent_name": agent_id,
                "role": "monitoring",
                "domain": "observability"
            }
        }
        logger = logging_manager.get_logger(config_name="default", custom_config=custom_log_config)
        super().__init__(agent_id=agent_id, agent_type=agent_type, logger=logger, **kwargs)
        self.logger = logger
        self.agent_id = agent_id
        self.version = version
        
        self.tracer_provider = None
        self.meter_provider = None
        self.tracer = None
        self.meter = None
        
        if OPENTELEMETRY_AVAILABLE:
            self._setup_opentelemetry()
        else:
            self.logger.warning("⚠️ OpenTelemetry non disponible - mode dégradé.")

    def _setup_opentelemetry(self):
        """Initialisation propre d'OpenTelemetry."""
        try:
            self.tracer_provider = TracerProvider()
            trace.set_tracer_provider(self.tracer_provider)
            self.tracer = trace.get_tracer(__name__)
            
            self.meter_provider = MeterProvider()
            metrics.set_meter_provider(self.meter_provider)
            self.meter = metrics.get_meter(__name__)
            
            self.logger.info("✅ OpenTelemetry initialisé avec succès.")
        except Exception as e:
            self.logger.error(f"❌ Erreur initialisation OpenTelemetry: {e}")
            global OPENTELEMETRY_AVAILABLE
            OPENTELEMETRY_AVAILABLE = False

    async def execute_task(self, task: Task) -> Result:
        if task.type == "generate_strategic_report":
            try:
                context = task.params
                type_rapport = task.params.get('type_rapport', 'monitoring')
                format_sortie = task.params.get('format_sortie', 'json')
                
                rapport = await self.generer_rapport_strategique(context, type_rapport)
                
                if format_sortie == 'markdown':
                    rapport_md = await self.generer_rapport_markdown(rapport, type_rapport, context)
                    
                    import os
                    from datetime import datetime 
                    reports_dir = "reports"
                    os.makedirs(reports_dir, exist_ok=True)
                    
                    timestamp_val = datetime.now() 
                    filename = f"strategic_report_agent_06_monitoring_{type_rapport}_{timestamp_val.strftime('%Y-%m-%d_%H%M%S')}.md"
                    filepath = os.path.join(reports_dir, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(rapport_md)
                    
                    return Result(success=True, data={
                        'rapport_json': rapport, 
                        'rapport_markdown': rapport_md,
                        'fichier_sauvegarde': filepath
                    })
                
                return Result(success=True, data=rapport)
            except Exception as e:
                self.logger.error(f"Erreur génération rapport monitoring: {e}")
                return Result(success=False, error=f"Exception rapport monitoring: {str(e)}")
        else:
            self.logger.info(f"⚙️ Exécution de la tâche de monitoring: {task.id}")
            if self.tracer and OPENTELEMETRY_AVAILABLE:
                with self.tracer.start_as_current_span("monitoring_task") as span:
                    span.set_attribute("task.id", task.id)
                    status = self.get_system_status()
                    span.set_attribute("system.status", "ok" if status.get("success") else "error")
                    return Result(success=True, data=status)
            else:
                status = self.get_system_status()
                return Result(success=True, data=status)

    def get_system_status(self) -> Dict[str, Any]:
        return {
            "success": True,
            "timestamp": asyncio.get_event_loop().time(),
            "opentelemetry_enabled": OPENTELEMETRY_AVAILABLE,
        }

    async def startup(self):
        self.logger.info(f"📊 {self.agent_id} v{self.version} - DÉMARRAGE")

    async def shutdown(self):
        self.logger.info(f"📊 {self.agent_id} v{self.version} - ARRÊT")

    async def generer_rapport_strategique(self, context: Dict[str, Any], type_rapport: str = 'monitoring') -> Dict[str, Any]:
        self.logger.info(f"Génération rapport monitoring/observabilité: {type_rapport}")
        metriques_base = await self._collecter_metriques_monitoring()
        from datetime import datetime 
        timestamp_val = datetime.now() 
        
        if type_rapport == 'monitoring':
            return await self._generer_rapport_monitoring(context, metriques_base, timestamp_val)
        elif type_rapport == 'observabilite':
            return await self._generer_rapport_observabilite(context, metriques_base, timestamp_val)
        elif type_rapport == 'performance': 
            return await self._generer_rapport_performance_monitoring(context, metriques_base, timestamp_val)
        elif type_rapport == 'alertes':
            return await self._generer_rapport_alertes(context, metriques_base, timestamp_val)
        else: 
            return await self._generer_rapport_monitoring(context, metriques_base, timestamp_val)

    async def _collecter_metriques_monitoring(self) -> Dict[str, Any]:
        try:
            system_status = self.get_system_status()
            from datetime import datetime 
            current_iso_timestamp = datetime.now().isoformat()
            
            # Simulation de données plus riches pour les rapports
            services_monitores_actifs = 10
            total_services_infrastructure = 12
            alert_rules_actives = 15
            
            monitoring_metrics = {
                'opentelemetry_enabled': OPENTELEMETRY_AVAILABLE,
                'tracer_provider_active': self.tracer_provider is not None,
                'meter_provider_active': self.meter_provider is not None,
                'monitoring_active': system_status.get('success', False)
            }
            observability_metrics = { # Ces métriques sont plus génériques et peuvent être utilisées par d'autres types de rapports
                'traces_collected_total': 2450,  
                'metrics_collected_total': 12800,  
                'logs_processed_total': 102400,    
                'alert_rules_count_total': alert_rules_actives, # Nombre total de règles, peut être différent des actives pour un type de rapport
                'dashboards_active_count': 8,
                'services_monitores_actifs': services_monitores_actifs,
                'total_services_infrastructure': total_services_infrastructure
            }
            monitoring_health = {
                'telemetry_operational': OPENTELEMETRY_AVAILABLE,
                'tracing_enabled': self.tracer is not None,
                'metrics_enabled': self.meter is not None,
                'system_responsive': system_status.get('success', False)
            }
            return {
                'monitoring_metrics': monitoring_metrics,
                'observability_metrics': observability_metrics, # Renommé pour plus de clarté
                'monitoring_health': monitoring_health,
                'system_status': system_status,
                'derniere_maj': current_iso_timestamp
            }
        except Exception as e:
            self.logger.error(f"Erreur collecte métriques monitoring: {e}")
            return {'erreur': str(e), 'metriques_partielles': True}

    async def _generer_rapport_monitoring(self, context: Dict, metriques: Dict, timestamp) -> Dict[str, Any]:
        """Génère le contenu du rapport de monitoring stratégique."""
        monitoring_metrics = metriques.get('monitoring_metrics', {})
        observability_data = metriques.get('observability_metrics', {}) # Utilisation des données d'observabilité générales
        monitoring_health = metriques.get('monitoring_health', {})
        
        agent_filename = Path(__file__).name

        score_monitoring = 0
        issues_critiques_details_list = [] 
        if monitoring_health.get('telemetry_operational'): score_monitoring += 30
        else: issues_critiques_details_list.append("OpenTelemetry indisponible ou non opérationnel.")
        if monitoring_health.get('tracing_enabled'): score_monitoring += 25
        else: issues_critiques_details_list.append("Système de Tracing distribué inactif ou mal configuré.")
        if monitoring_health.get('metrics_enabled'): score_monitoring += 25
        else: issues_critiques_details_list.append("Collecte des métriques système et applicatives inactive.")
        if monitoring_health.get('system_responsive'): score_monitoring += 20
        else: issues_critiques_details_list.append("Le système de monitoring global ne répond pas ou est dégradé.")
        
        niveau_qualite_val = "OPTIMAL" if score_monitoring >= 90 else "ACCEPTABLE" if score_monitoring >= 70 else "CRITIQUE"
        conformite_val = "✅ CONFORME" if score_monitoring >= 70 else "❌ NON CONFORME"
        issues_critiques_count_val = len(issues_critiques_details_list)

        reco_telemetry = ('✅ OpenTelemetry est pleinement opérationnel, assurant une collecte de données de télémétrie complète.' 
                          if monitoring_health.get('telemetry_operational') 
                          else '⚠️ OpenTelemetry est indisponible ou rencontre des problèmes. Investigation immédiate requise pour restaurer la visibilité.')
        reco_tracing = ('✅ Le tracing distribué est actif et correctement configuré, permettant une analyse fine des flux transactionnels.' 
                        if monitoring_health.get('tracing_enabled') 
                        else '⚠️ Le tracing distribué est inactif. Vérifier la configuration du provider de traces et les agents d\'instrumentation.')
        reco_metrics = ('✅ La collecte des métriques est active et les données sont agrégées de manière fiable.' 
                        if monitoring_health.get('metrics_enabled') 
                        else '⚠️ La collecte des métriques est inactive. Vérifier le meter provider et les points de collecte.')
        reco_systeme = ('✅ Le système de monitoring est réactif et performant, garantissant des données en temps réel.' 
                        if monitoring_health.get('system_responsive') 
                        else '⚠️ Le système de monitoring présente des latences ou des indisponibilités. Identifier et corriger la cause racine.')

        return {
            'agent_id': self.agent_id,
            'agent_file_name': agent_filename, # NOUVEAU
            'type_rapport': 'monitoring',
            'timestamp': timestamp.isoformat(),
            'specialisation': 'Spécialiste Monitoring & Observabilité Stratégique', # Plus descriptif
            'score_global': score_monitoring, 
            'niveau_qualite': niveau_qualite_val, 
            'conformite': conformite_val, 
            'signature_cryptographique': 'N/A (Fonctionnalité non implémentée pour cet agent)', # NOUVEAU
            'issues_critiques_identifies': issues_critiques_count_val, 
            'architecture_monitoring': { 
                'description': "Système de monitoring stratégique avancé, s'appuyant sur OpenTelemetry pour une observabilité distribuée complète et une visibilité approfondie de la performance applicative et de l'infrastructure.",
                'statut_operationnel': 'Système de monitoring OpenTelemetry globalement opérationnel.', # NOUVEAU
                'confirmation_specialisation': f"{self.agent_id} confirmé comme Spécialiste Monitoring & Observabilité.", # NOUVEAU
                'objectifs_principaux': [
                    "Assurer une collecte exhaustive et en temps réel des traces distribuées à travers tous les services.",
                    "Surveiller en continu les métriques de performance clés (KPIs) de l'application et de l'infrastructure.",
                    "Permettre une agrégation et une analyse centralisée des logs pour un diagnostic rapide des incidents.",
                    "Faciliter la configuration et la gestion proactive des alertes critiques basées sur des seuils et des anomalies."
                ],
                'technologies_cles': ["OpenTelemetry (OTLP)", "Prometheus (simulation pour agrégation métriques)", "Grafana (simulation pour dashboards et visualisation)", "Python Asyncio"]
            },
            'recommandations_monitoring': [ # Recommandations plus descriptives
                f"📊 TÉLÉMÉTRIE: {reco_telemetry}",
                f"🔍 TRACING: {reco_tracing}",
                f"📈 MÉTRIQUES: {reco_metrics}",
                f"⚡ SYSTÈME MONITORING: {reco_systeme}"
            ],
            'issues_critiques_monitoring_details': issues_critiques_details_list if issues_critiques_count_val > 0 else ["Aucun issue critique de monitoring majeur détecté. Le système fonctionne dans les paramètres attendus."], 
             'details_techniques_monitoring': { 
                'strategie_monitoring': "Observabilité distribuée full-stack avec OpenTelemetry, axée sur la collecte proactive de traces, métriques et logs.", # NOUVEAU
                'collecteurs_donnees': ["Traces (OTLP via agents OpenTelemetry)", "Métriques (OTLP/Prometheus via SDKs et exporters)", "Logs (Potentiel pour FluentBit vers OTLP, non actif)"], # NOUVEAU
                'opentelemetry_disponible': monitoring_metrics.get('opentelemetry_enabled', False),
                'tracer_provider_actif': monitoring_metrics.get('tracer_provider_active', False),
                'meter_provider_actif': monitoring_metrics.get('meter_provider_active', False),
                'traces_collectees_session': observability_data.get('traces_collected_total', 0), # Changé pour refléter le total (simulé)
                'metriques_collectees_session': observability_data.get('metrics_collected_total', 0), # Changé
                'logs_traites_session': observability_data.get('logs_processed_total', 0), # Changé
                'alert_rules_actives_monitoring': observability_data.get('alert_rules_count_total',0), # Spécifique au monitoring
                'dashboards_actifs_monitoring': observability_data.get('dashboards_active_count',0) # Spécifique au monitoring
            },
            'metriques_monitoring_detaillees': {  # Scores structurés
                'score_monitoring_global': {'actuel': score_monitoring, 'cible': 100},
                'sante_telemetrie': {'actuel': 100 if monitoring_health.get('telemetry_operational') else 30, 'cible': 100, 'unite': '%'},
                'efficacite_tracing': {'actuel': 100 if monitoring_health.get('tracing_enabled') else 30, 'cible': 100, 'unite': '%'},
                'couverture_metriques': {'actuel': 100 if monitoring_health.get('metrics_enabled') else 30, 'cible': 100, 'unite': '%'},
                'reactivite_systeme_monitoring': {'actuel': 100 if monitoring_health.get('system_responsive') else 30, 'cible': 100, 'unite': '%'},
                'services_monitores_ok': {'actuel': observability_data.get('services_monitores_actifs',0) , 'total': observability_data.get('total_services_infrastructure',0), 'unite': 'services'},
                'regles_alertes_configurees_monitoring': {'actuel': observability_data.get('alert_rules_count_total',0), 'unite': 'règles'}
            },
            'metadonnees': { 
                'version_agent': self.version, # Utiliser la version de l'agent
                'version_rapport': '1.1.0', # Version de la structure du rapport
                'notes_qualite': "Rapport généré conformément aux standards de qualité v1.2 de l'équipe NextGeneration.", # NOUVEAU
                'dependances_simulation': ["OpenTelemetry SDK", "Prometheus (simulation)", "Grafana (simulation)"],
                'context_analyse': context.get('cible', 'Analyse générale du système de monitoring stratégique')
            }
        }

    async def _generer_rapport_observabilite(self, context: Dict, metriques: Dict, timestamp) -> Dict[str, Any]:
        """Génère le contenu du rapport d'observabilité stratégique."""
        observability_data = metriques.get('observability_metrics', {})
        agent_filename = Path(__file__).name

        score = 0
        issues_details = []

        traces_collectees = observability_data.get('traces_collected_total', 0)
        metriques_collectees = observability_data.get('metrics_collected_total', 0)
        logs_traites = observability_data.get('logs_processed_total', 0)
        dashboards_actifs = observability_data.get('dashboards_active_count', 0)

        if traces_collectees > 1000: score += 25
        else: issues_details.append(f"Couverture des traces ({traces_collectees}) inférieure à l'objectif de 1000.")
        if metriques_collectees > 5000: score += 25
        else: issues_details.append(f"Volume des métriques ({metriques_collectees}) inférieur à l'objectif de 5000.")
        if logs_traites > 50000: score += 25
        else: issues_details.append(f"Volume des logs traités ({logs_traites}) inférieur à l'objectif de 50000.")
        if dashboards_actifs >= 5: score += 25
        else: issues_details.append(f"Nombre de dashboards actifs ({dashboards_actifs}) insuffisant (cible: 5+).")
        
        score_observabilite_global = score
        niveau_qualite = "OPTIMAL" if score_observabilite_global >= 90 else "ACCEPTABLE" if score_observabilite_global >= 70 else "CRITIQUE"
        conformite = "✅ CONFORME" if score_observabilite_global >= 70 else "❌ NON CONFORME"
        issues_critiques_count = len(issues_details)

        # Simplification des f-strings pour les recommandations
        if traces_collectees > 1000:
            reco_traces_text = f"Traces: {traces_collectees} collectées. Maintenir une haute couverture et envisager l'échantillonnage adaptatif pour les systèmes à haut volume."
        else:
            reco_traces_text = f"Traces: {traces_collectees} collectées. Augmenter la couverture des traces sur les services critiques et les flux utilisateurs clés."

        if metriques_collectees > 5000:
            reco_metriques_text = f"Métriques: {metriques_collectees} collectées. Assurer la pertinence des métriques (RED, USE) et explorer les métriques personnalisées."
        else:
            reco_metriques_text = f"Métriques: {metriques_collectees} collectées. Étoffer la collecte avec des métriques orientées business et expérience utilisateur."

        if logs_traites > 50000:
            reco_logs_text = f"Logs: {logs_traites} traités. Optimiser la corrélation des logs avec les traces et métriques via des identifiants partagés."
        else:
            reco_logs_text = f"Logs: {logs_traites} traités. Standardiser les formats de logs (ex: JSON structuré) et enrichir avec des contextes applicatifs."

        if dashboards_actifs >= 5:
            reco_dashboards_text = f"Dashboards: {dashboards_actifs} actifs. Personnaliser les dashboards par équipe/service et intégrer des visualisations d'alertes."
        else:
            reco_dashboards_text = f"Dashboards: {dashboards_actifs} actifs. Développer davantage de dashboards pour les KPIs clés et les flux critiques."

        return {
            'agent_id': self.agent_id,
            'agent_file_name': agent_filename,
            'type_rapport': 'observabilite',
            'timestamp': timestamp.isoformat(),
            'specialisation': 'Observabilité Système & Applicative Distribuée',
            'score_global': score_observabilite_global,
            'niveau_qualite': niveau_qualite,
            'conformite': conformite,
            'signature_cryptographique': 'N/A (Fonctionnalité non implémentée pour cet agent)',
            'issues_critiques_identifies': issues_critiques_count,
            'architecture_observabilite': {
                'description': "Plateforme d'observabilité centralisée conçue pour offrir une visibilité de bout en bout sur la santé, la performance et le comportement des systèmes distribués.",
                'statut_operationnel': 'Plateforme d\'observabilité pleinement opérationnelle et intégrée aux flux CI/CD.',
                'confirmation_specialisation': f"{self.agent_id} confirmé comme expert en conception et implémentation de stratégies d\'observabilité.",
                'piliers': ['Traces distribuées (Tracing)', 'Métriques temporelles (Metrics)', 'Logs structurés (Logging)', 'Visualisation & Alerting Intégré'],
                'outils_simules': ['OpenTelemetry (Collector & SDKs)', 'Prometheus/VictoriaMetrics (Time-Series DB)', 'Grafana/Kibana (Visualisation)', 'ELK Stack/Loki (Log Management)']
            },
            'recommandations_observabilite': [
                f"🔍 {reco_traces_text}",
                f"📊 {reco_metriques_text}",
                f"📝 {reco_logs_text}",
                f"📋 {reco_dashboards_text}",
                "⚙️ AUTOMATION: Envisager l'automatisation de la détection d'anomalies basée sur le machine learning pour les métriques et logs."
            ],
            'issues_critiques_observabilite_details': issues_details if issues_critiques_count > 0 else ["Aucun issue critique d'observabilité majeur détecté. La plateforme répond aux exigences actuelles."],
            'details_techniques_observabilite': {
                'strategie_observabilite': "Approche 'Three Pillars of Observability' (Traces, Metrics, Logs) augmentée par une forte capacité de visualisation et d'analyse.",
                'indicateurs_cles_suivis': [
                    'Latence de bout en bout par transaction', 
                    'Taux d\'erreurs par service/endpoint (RED)',
                    'Saturation et utilisation des ressources (USE)',
                    'Santé des dépendances critiques',
                    'Volume et types d\'erreurs dans les logs'
                ],
                'collecte_traces_volume': f"{traces_collectees} traces/période (simulé)",
                'granularite_metriques_freq': '15 secondes - 1 minute (simulé)',
                'retention_logs_duree': '90 jours pour logs critiques, 30 jours pour logs applicatifs (simulé)',
                'utilisateurs_plateforme_actifs': f"{dashboards_actifs * 5} utilisateurs réguliers (simulé)"
            },
            'metriques_observabilite_detaillees': {
                'score_observabilite_global': {'actuel': score_observabilite_global, 'cible': 100, 'unite': 'points'},
                'couverture_tracing_services': {'actuel': traces_collectees, 'cible': 1000, 'seuil_critique': 500, 'unite': 'traces_indicatives'},
                'volume_metriques_pertinentes': {'actuel': metriques_collectees, 'cible': 5000, 'seuil_critique': 2000, 'unite': 'metriques_indicatives'},
                'centralisation_logs_efficace': {'actuel': logs_traites, 'cible': 50000, 'seuil_critique': 10000, 'unite': 'logs_indicatifs'},
                'disponibilite_dashboards_cles': {'actuel': dashboards_actifs, 'cible': 5, 'seuil_critique': 2, 'unite': 'dashboards'}
            },
            'metadonnees': {
                'version_agent': self.version,
                'version_rapport': '1.1.0',
                'notes_qualite': "Ce rapport d'observabilité est conforme aux standards v1.2 de l'équipe NextGeneration.",
                'dependances_simulation': ['OpenTelemetry', 'Prometheus', 'Grafana', 'ELK Stack'],
                'context_analyse': context.get('cible', 'Analyse stratégique de la plateforme d\'observabilité globale')
            }
        }

    async def _generer_rapport_performance_monitoring(self, context: Dict, metriques: Dict, timestamp) -> Dict[str, Any]:
        """Génère le contenu du rapport de performance stratégique lié au monitoring."""
        observability_data = metriques.get('observability_metrics', {}) # utiliser les données d'observabilité générales
        monitoring_health = metriques.get('monitoring_health', {})
        agent_filename = Path(__file__).name

        score = 0
        issues_details = []
        
        # Simulation de données plus spécifiques à la performance du monitoring
        latence_collecte_ms_simule = observability_data.get('latence_collecte_ms_p95', 8) # P95
        overhead_agent_simule_pourcentage = observability_data.get('overhead_agent_cpu_avg', 1.5) # % CPU moyen
        debit_traitement_events_sec_simule = observability_data.get('debit_traitement_metrics_sec', 15000)
        utilisation_cpu_monitoring_simule = observability_data.get('cpu_usage_monitoring_total_avg', 12) # % CPU total moyen

        # Critères de scoring pour la performance du monitoring
        if latence_collecte_ms_simule < 10: score += 25
        else: issues_details.append(f"Latence de collecte P95 élevée: {latence_collecte_ms_simule}ms (cible < 10ms)")
        if overhead_agent_simule_pourcentage < 2: score += 25
        else: issues_details.append(f"Overhead moyen des agents de monitoring: {overhead_agent_simule_pourcentage}% (cible < 2%)")
        if debit_traitement_events_sec_simule >= 10000 : score += 25
        else: issues_details.append(f"Débit de traitement des données de télémétrie: {debit_traitement_events_sec_simule} events/sec (cible >= 10000)")
        if monitoring_health.get('system_responsive'): score += 25 # La réactivité générale du système reste un pilier
        else: issues_details.append("Système de monitoring global non réactif, impactant la performance perçue de l'analyse.")
        
        score_performance_global = score
        niveau_qualite = "OPTIMAL" if score_performance_global >= 90 else "ACCEPTABLE" if score_performance_global >= 70 else "CRITIQUE"
        conformite = "✅ CONFORME" if score_performance_global >= 70 else "❌ NON CONFORME"
        issues_critiques_count = len(issues_details)
        
        # Recommandations améliorées
        reco_latence = (f"Latence de collecte (P95): {latence_collecte_ms_simule}ms. Maintenir sous 10ms pour une réactivité optimale."
                        if latence_collecte_ms_simule < 10
                        else f"Latence de collecte (P95): {latence_collecte_ms_simule}ms. Investiguer les causes de cette latence (réseau, charge agents). Cible < 10ms.")
        reco_overhead = (f"Overhead agents: {overhead_agent_simule_pourcentage}% CPU. Excellent, impact minimal sur les applications monitorées."
                         if overhead_agent_simule_pourcentage < 2
                         else f"Overhead agents: {overhead_agent_simule_pourcentage}% CPU. Analyser les agents consommateurs et optimiser leur configuration/ressources. Cible < 2%.")
        reco_debit = (f"Débit traitement: {debit_traitement_events_sec_simule} events/sec. Capacité de traitement adéquate."
                      if debit_traitement_events_sec_simule >= 10000
                      else f"Débit traitement: {debit_traitement_events_sec_simule} events/sec. Évaluer la scalabilité de la pipeline de collecte et de traitement. Cible >= 10000 events/sec.")
        reco_reactivite_sys = ("Réactivité système monitoring: Optimale."
                               if monitoring_health.get('system_responsive')
                               else "Réactivité système monitoring: Dégradée. Identifier les goulots d'étranglement internes au système de monitoring.")

        return {
            'agent_id': self.agent_id,
            'agent_file_name': agent_filename,
            'type_rapport': 'performance',
            'timestamp': timestamp.isoformat(),
            'specialisation': 'Analyse & Optimisation de Performance des Systèmes de Monitoring',
            'score_global': score_performance_global,
            'niveau_qualite': niveau_qualite,
            'conformite': conformite,
            'signature_cryptographique': 'N/A (Fonctionnalité non implémentée pour cet agent)',
            'issues_critiques_identifies': issues_critiques_count,
            'architecture_performance_monitoring': {
                'description': "Analyse approfondie de la performance intrinsèque du système de monitoring, incluant la latence de collecte, l'overhead des agents, le débit de traitement des données de télémétrie, et la consommation globale des ressources.",
                'statut_operationnel_performance': "Système d'analyse de performance du monitoring pleinement opérationnel.",
                'confirmation_specialisation_performance': f"{self.agent_id} est confirmé pour l'analyse et l'optimisation de la performance des systèmes de monitoring distribués.",
                'indicateurs_cles_performance_architecture': [
                    'Latence de collecte des données (P95, P99)', 
                    'Overhead CPU/Mémoire des agents de monitoring sur les hôtes applicatifs',
                    'Débit de traitement des données de télémétrie (événements/seconde)', 
                    'Utilisation CPU/Mémoire par les composants centraux du système de monitoring (collecteurs, bases de données, etc.)',
                    'Temps de réponse des APIs de configuration et de requêtage du monitoring'
                ]
            },
            'recommandations_performance': [
                f"⚡ {reco_latence}",
                f"🔬 {reco_overhead}",
                f"🚀 {reco_debit}",
                f"💻 {reco_reactivite_sys}",
                "📈 PROJECTION: Modéliser la croissance des données de télémétrie pour anticiper les besoins futurs en capacité de la plateforme de monitoring."
            ],
            'issues_critiques_performance_monitoring_details': issues_details if issues_critiques_count > 0 else ["Aucun issue critique de performance majeur détecté pour le système de monitoring lui-même."],
            'details_techniques_performance_monitoring': {
                'strategie_analyse_performance': "Analyse proactive et continue des goulots d'étranglement, optimisation des configurations d'agents et des ressources allouées à la plateforme de monitoring.",
                'kpis_cles_performance_suivis': [
                    f"Latence de collecte (P95): {latence_collecte_ms_simule}ms",
                    f"Overhead moyen des agents CPU: {overhead_agent_simule_pourcentage}%",
                    f"Débit de traitement des données: {debit_traitement_events_sec_simule} events/sec",
                    f"Utilisation CPU moyenne du système de monitoring: {utilisation_cpu_monitoring_simule}%"
                ],
                'outils_analyse_performance_simules': ['Profilers (e.g., cProfile, Pyflame)', 'Benchmarking tools', 'Simulateurs de charge'],
                'ressources_allouees_monitoring_simule': 'CPU: 8 vCores, RAM: 32GB, Disque: 1TB SSD (cluster de monitoring)'
            },
            'metriques_performance_monitoring_detaillees': {
                'score_performance_monitoring_global': {'actuel': score_performance_global, 'cible': 100, 'unite': 'points'},
                'latence_collecte_p95_ms': {'actuel': latence_collecte_ms_simule, 'cible': 10, 'unite': 'ms'},
                'overhead_agents_cpu_pourcentage': {'actuel': overhead_agent_simule_pourcentage, 'cible': 2, 'unite': '%'},
                'debit_traitement_events_par_sec': {'actuel': debit_traitement_events_sec_simule, 'cible': 10000, 'unite': 'events/sec'},
                'reactivite_systeme_monitoring_sante': {'actuel': 100 if monitoring_health.get('system_responsive') else 30, 'cible': 100, 'unite': '%'}
            },
            'metadonnees': {
                'version_agent': self.version,
                'version_rapport': '1.1.0',
                'notes_qualite': "Rapport de performance du système de monitoring conforme aux standards v1.2.",
                'specialisation_agent': 'performance_analysis_monitoring_systems',
                'context_analyse': context.get('cible', 'Analyse de performance du système de monitoring distribué')
            }
        }

    async def _generer_rapport_alertes(self, context: Dict, metriques: Dict, timestamp) -> Dict[str, Any]:
        """Génère le contenu du rapport d'alertes stratégique."""
        observability_metrics = metriques.get('observability_metrics', {})
        score = 0
        issues_details = []
        regles_alertes_simule = observability_metrics.get('alert_rules', 0)
        alertes_actives_simule = 3 
        couverture_alertes_simule = 95 
        if regles_alertes_simule >= 10: score += 30
        else: issues_details.append(f"Nombre de règles d'alertes faible: {regles_alertes_simule}")
        if alertes_actives_simule <= 5: score += 30 
        else: issues_details.append(f"Nombre élevé d'alertes actives: {alertes_actives_simule}")
        if couverture_alertes_simule >= 90: score += 40
        else: issues_details.append(f"Couverture des alertes insuffisante: {couverture_alertes_simule}%")
        score_alertes_global = score
        niveau_qualite = "OPTIMAL" if score_alertes_global >= 90 else "ACCEPTABLE" if score_alertes_global >= 70 else "CRITIQUE"
        conformite = "✅ CONFORME" if score_alertes_global >= 70 else "❌ NON CONFORME"
        issues_critiques_count = len(issues_details)
        return {
            'agent_id': 'agent_06_specialiste_monitoring_sprint4',
            'type_rapport': 'alertes',
            'timestamp': timestamp.isoformat(),
            'specialisation': 'Gestion Stratégique des Alertes',
            'score_global': score_alertes_global,
            'niveau_qualite': niveau_qualite,
            'conformite': conformite,
            'issues_critiques_identifies': issues_critiques_count,
            'architecture_alertes': {
                'description': "Système de gestion des alertes conçu pour une détection proactive et une notification rapide des incidents.",
                'composants_cles': ['Moteur de règles d\'alertes', 'Système de notification multi-canal', 'Tableau de bord de suivi des alertes', 'Processus d\'escalade']
            },
            'recommandations_alertes': [
                f"🚨 RÈGLES D'ALERTES: {regles_alertes_simule} configurées. Réviser et affiner régulièrement.",
                f"⚠️ ALERTES ACTIVES: {alertes_actives_simule} en cours. Prioriser et traiter.",
                f"🎯 COUVERTURE DES ALERTES: {couverture_alertes_simule}%. Viser une couverture de 99%+ des services critiques.",
                f"📚 DOCUMENTATION: S'assurer que chaque alerte a une procédure de réponse documentée (runbook)."
            ],
            'issues_critiques_alertes_details': issues_details if issues_critiques_count > 0 else ["Aucun issue critique majeur dans la gestion des alertes détecté."],
            'details_techniques_alertes': {
                'nombre_regles_actives': regles_alertes_simule,
                'temps_moyen_detection': '< 1 min (simulé)',
                'canaux_notification': ['Email', 'Slack', 'PagerDuty (simulé)'],
                'severite_niveaux': ['Critique', 'Avertissement', 'Information']
            },
            'metriques_alertes_detaillees': {
                'score_alertes_global': score_alertes_global,
                'nombre_regles_configurees': regles_alertes_simule,
                'alertes_actives_en_cours': alertes_actives_simule,
                'pourcentage_couverture_alertes': couverture_alertes_simule,
                'score_nombre_regles': 30 if regles_alertes_simule >= 10 else 5,
                'score_alertes_actives': 30 if alertes_actives_simule <= 5 else 5,
                'score_couverture': 40 if couverture_alertes_simule >= 90 else 10
            },
            'metadonnees': {
                'specialisation_agent': 'gestion_alertes_intelligentes',
                'context_analyse': context.get('cible', 'analyse_systeme_alertes')
            }
        }

    async def generer_rapport_markdown(self, rapport_json: Dict[str, Any], type_rapport: str, context: Dict[str, Any]) -> str:
        from datetime import datetime 
        timestamp_val = datetime.now() 
        if type_rapport == 'monitoring':
            return await self._generer_markdown_monitoring(rapport_json, context, timestamp_val)
        elif type_rapport == 'observabilite':
            return await self._generer_markdown_observabilite(rapport_json, context, timestamp_val)
        elif type_rapport == 'performance': 
            return await self._generer_markdown_performance_monitoring(rapport_json, context, timestamp_val)
        elif type_rapport == 'alertes':
            return await self._generer_markdown_alertes(rapport_json, context, timestamp_val)
        else:
            self.logger.warning(f"Type de rapport Markdown inconnu: {type_rapport}. Utilisation du rapport monitoring par défaut.")
            return await self._generer_markdown_monitoring(rapport_json, context, timestamp_val)

    async def _generer_markdown_monitoring(self, rapport: Dict, context: Dict, timestamp) -> str:
        score = rapport.get('score_global', 0)
        niveau_qualite = rapport.get('niveau_qualite', 'N/A')
        conformite = rapport.get('conformite', 'N/A')
        signature_crypto = rapport.get('signature_cryptographique', 'N/A')
        agent_file_name = rapport.get('agent_file_name', rapport.get('agent_id', 'N/A'))
        issues_count = rapport.get('issues_critiques_identifies', 0)
        architecture = rapport.get('architecture_monitoring', {})
        recommandations = rapport.get('recommandations_monitoring', [])
        issues_details = rapport.get('issues_critiques_monitoring_details', [])
        details_tech = rapport.get('details_techniques_monitoring', {})
        metriques_detaillees = rapport.get('metriques_monitoring_detaillees', {})

        objectifs_str_list = [f"- {o}" for o in architecture.get('objectifs_principaux', [])]
        objectifs_block = "\\n".join(objectifs_str_list)
        
        tech_cles_list = architecture.get('technologies_cles', [])
        tech_cles_str = ", ".join(tech_cles_list) if tech_cles_list else "Non spécifiées"
        
        recommandations_str_list = [f"- {r}" for r in recommandations]
        recommandations_block = "\\n".join(recommandations_str_list)
        
        issues_critiques_str_list = [f"- 🔴 {i}" for i in issues_details] if issues_count > 0 else ["- Aucun issue critique majeur de monitoring détecté."]
        issues_block = "\\n".join(issues_critiques_str_list)

        otel_disponible_icon = '✅' if details_tech.get('opentelemetry_disponible') else '❌'
        tracer_provider_status = '✅ actif' if details_tech.get('tracer_provider_actif') else '❌ inactif'
        meter_provider_status = '✅ actif' if details_tech.get('meter_provider_actif') else '❌ inactif'
        
        reactivite_val = metriques_detaillees.get('reactivite_systeme_monitoring', {}).get('actuel', 0)
        if reactivite_val >= 70:
            reactivite_systeme_icon = '✅ Réactif'
        elif reactivite_val >= 40:
            reactivite_systeme_icon = '🔶 Moyen'
        else:
            reactivite_systeme_icon = '❌ Non Réactif'

        collecteurs_donnees_list = details_tech.get('collecteurs_donnees', [])
        collecteurs_donnees_str_list = [f"  - {cd}" for cd in collecteurs_donnees_list]
        collecteurs_donnees_block = "\\n".join(collecteurs_donnees_str_list) if collecteurs_donnees_list else "  - Non spécifiés"

        md_content = f"""# 📈 **RAPPORT MONITORING STRATÉGIQUE : {rapport.get('agent_id', 'N/A')}**

**Date :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
**Module :** {agent_file_name}
**Score Global** : {score/10:.1f}/10
**Niveau Qualité** : {niveau_qualite}
**Conformité** : {conformite}
**Signature Cryptographique** : {signature_crypto}
**Issues Critiques** : {issues_count}

## 🏗️ Architecture Monitoring
{architecture.get('description', 'Description non disponible.')}
- **Statut Opérationnel :** {architecture.get('statut_operationnel', 'Non spécifié.')}
- **Confirmation Spécialisation :** {architecture.get('confirmation_specialisation', 'Non confirmée.')}

**Objectifs principaux :**
{objectifs_block}

**Technologies clés (simulées) :** {tech_cles_str}

## 🔧 Recommandations Monitoring
{recommandations_block}

## 🚨 Issues Critiques Monitoring
{issues_block}

## 📋 Détails Techniques Monitoring
- **Stratégie Monitoring :** {details_tech.get('strategie_monitoring', 'Non définie.')}
- **Collecteurs de Données Principaux :**
{collecteurs_donnees_block}
- **OpenTelemetry disponible :** {otel_disponible_icon}
- **Tracer Provider :** {tracer_provider_status}
- **Meter Provider :** {meter_provider_status}
- **Traces collectées (session) :** {details_tech.get('traces_collectees_session', 0)}
- **Métriques collectées (session) :** {details_tech.get('metriques_collectees_session', 0)}
- **Logs traités (session) :** {details_tech.get('logs_traites_session', 0)}
- **Règles d'alertes (monitoring) :** {details_tech.get('alert_rules_actives_monitoring', 0)}
- **Dashboards actifs (monitoring) :** {details_tech.get('dashboards_actifs_monitoring', 0)}

## 📊 Métriques Monitoring Détaillées
- **Score Monitoring Global :** {metriques_detaillees.get('score_monitoring_global', {}).get('actuel',0)}/{metriques_detaillees.get('score_monitoring_global', {}).get('cible',100)}
- **Santé Télémétrie :** {metriques_detaillees.get('sante_telemetrie', {}).get('actuel',0)}/{metriques_detaillees.get('sante_telemetrie', {}).get('cible',100)} {metriques_detaillees.get('sante_telemetrie', {}).get('unite','%')}
- **Efficacité Tracing :** {metriques_detaillees.get('efficacite_tracing', {}).get('actuel',0)}/{metriques_detaillees.get('efficacite_tracing', {}).get('cible',100)} {metriques_detaillees.get('efficacite_tracing', {}).get('unite','%')}
- **Couverture Métriques :** {metriques_detaillees.get('couverture_metriques', {}).get('actuel',0)}/{metriques_detaillees.get('couverture_metriques', {}).get('cible',100)} {metriques_detaillees.get('couverture_metriques', {}).get('unite','%')}
- **Réactivité Système Monitoring :** {reactivite_systeme_icon} ({metriques_detaillees.get('reactivite_systeme_monitoring', {}).get('actuel',0)}/{metriques_detaillees.get('reactivite_systeme_monitoring', {}).get('cible',100)} {metriques_detaillees.get('reactivite_systeme_monitoring', {}).get('unite','%')})
- **Services Monitorés OK :** {metriques_detaillees.get('services_monitores_ok', {}).get('actuel',0)}/{metriques_detaillees.get('services_monitores_ok', {}).get('total',0)} {metriques_detaillees.get('services_monitores_ok', {}).get('unite','services')}
- **Règles d'Alertes Configurées (pour Monitoring) :** {metriques_detaillees.get('regles_alertes_configurees_monitoring', {}).get('actuel',0)} {metriques_detaillees.get('regles_alertes_configurees_monitoring', {}).get('unite','règles')}

--- 

*Rapport Monitoring généré par {rapport.get('agent_id', 'Agent Inconnu')} - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}*
*📊 {rapport.get('specialisation', 'Spécialiste Monitoring & Observabilité')}*
*📂 Sauvegardé dans : reports/*
"""
        return md_content

    async def _generer_markdown_observabilite(self, rapport: Dict, context: Dict, timestamp) -> str:
        score = rapport.get('score_global', 0)
        niveau_qualite = rapport.get('niveau_qualite', 'N/A')
        conformite = rapport.get('conformite', 'N/A')
        signature_crypto = rapport.get('signature_cryptographique', 'N/A')
        agent_file_name = rapport.get('agent_file_name', rapport.get('agent_id', 'N/A'))
        issues_count = rapport.get('issues_critiques_identifies', 0)
        architecture = rapport.get('architecture_observabilite', {})
        recommandations = rapport.get('recommandations_observabilite', [])
        issues_details = rapport.get('issues_critiques_observabilite_details', [])
        details_tech = rapport.get('details_techniques_observabilite', {})
        metriques_detaillees = rapport.get('metriques_observabilite_detaillees', {})

        piliers_str_list = [f"- {p}" for p in architecture.get('piliers', [])]
        piliers_block = "\\n".join(piliers_str_list)
        
        outils_simules_list = architecture.get('outils_simules', [])
        outils_simules_str = ", ".join(outils_simules_list) if outils_simules_list else "Non spécifiés"
        
        recommandations_str_list = [f"- {r}" for r in recommandations]
        recommandations_block = "\\n".join(recommandations_str_list)
        
        issues_critiques_str_list = [f"- 🔴 {i}" for i in issues_details] if issues_count > 0 else ["- Aucun issue critique majeur d'observabilité détecté."]
        issues_block = "\\n".join(issues_critiques_str_list)

        indicateurs_cles_list = details_tech.get('indicateurs_cles_suivis', [])
        indicateurs_cles_str_list = [f"  - {ic}" for ic in indicateurs_cles_list]
        indicateurs_cles_block = "\\n".join(indicateurs_cles_str_list) if indicateurs_cles_list else "  - Non spécifiés"

        md_content = f"""# 💡 **RAPPORT D'OBSERVABILITÉ STRATÉGIQUE : {rapport.get('agent_id', 'N/A')}**

**Date :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
**Module :** {agent_file_name}
**Score Global** : {score/10:.1f}/10
**Niveau Qualité** : {niveau_qualite}
**Conformité** : {conformite}
**Signature Cryptographique** : {signature_crypto}
**Issues Critiques** : {issues_count}

## 🏗️ Architecture d'Observabilité
{architecture.get('description', 'Description non disponible.')}
- **Statut Opérationnel :** {architecture.get('statut_operationnel', 'Non spécifié.')}
- **Confirmation Spécialisation :** {architecture.get('confirmation_specialisation', 'Non confirmée.')}

**Piliers clés :**
{piliers_block}

**Outils principaux (simulés) :** {outils_simules_str}

## 🔧 Recommandations Stratégiques d'Observabilité
{recommandations_block}

## 🚨 Issues Critiques d'Observabilité
{issues_block}

## 📋 Détails Techniques de la Plateforme d'Observabilité
- **Stratégie d'Observabilité :** {details_tech.get('strategie_observabilite', 'Non définie.')}
- **Indicateurs Clés Suivis :**
{indicateurs_cles_block}
- **Volume de Collecte des Traces :** {details_tech.get('collecte_traces_volume', 'N/A')}
- **Fréquence de Granularité des Métriques :** {details_tech.get('granularite_metriques_freq', 'N/A')}
- **Durée de Rétention des Logs :** {details_tech.get('retention_logs_duree', 'N/A')}
- **Nombre d'Utilisateurs Actifs de la Plateforme :** {details_tech.get('utilisateurs_plateforme_actifs', 'N/A')}

## 📊 Métriques d'Observabilité Détaillées
- **Score Global d'Observabilité :** {metriques_detaillees.get('score_observabilite_global', {}).get('actuel',0)}/{metriques_detaillees.get('score_observabilite_global', {}).get('cible',100)} {metriques_detaillees.get('score_observabilite_global', {}).get('unite','points')}
- **Couverture Tracing des Services (indic.) :** {metriques_detaillees.get('couverture_tracing_services', {}).get('actuel',0)}/{metriques_detaillees.get('couverture_tracing_services', {}).get('cible',1000)} {metriques_detaillees.get('couverture_tracing_services', {}).get('unite','traces')} (Seuil critique: {metriques_detaillees.get('couverture_tracing_services', {}).get('seuil_critique',0)})
- **Volume Métriques Pertinentes (indic.) :** {metriques_detaillees.get('volume_metriques_pertinentes', {}).get('actuel',0)}/{metriques_detaillees.get('volume_metriques_pertinentes', {}).get('cible',5000)} {metriques_detaillees.get('volume_metriques_pertinentes', {}).get('unite','métriques')} (Seuil critique: {metriques_detaillees.get('volume_metriques_pertinentes', {}).get('seuil_critique',0)})
- **Efficacité Centralisation Logs (indic.) :** {metriques_detaillees.get('centralisation_logs_efficace', {}).get('actuel',0)}/{metriques_detaillees.get('centralisation_logs_efficace', {}).get('cible',50000)} {metriques_detaillees.get('centralisation_logs_efficace', {}).get('unite','logs')} (Seuil critique: {metriques_detaillees.get('centralisation_logs_efficace', {}).get('seuil_critique',0)})
- **Disponibilité Dashboards Clés :** {metriques_detaillees.get('disponibilite_dashboards_cles', {}).get('actuel',0)}/{metriques_detaillees.get('disponibilite_dashboards_cles', {}).get('cible',5)} {metriques_detaillees.get('disponibilite_dashboards_cles', {}).get('unite','dashboards')} (Seuil critique: {metriques_detaillees.get('disponibilite_dashboards_cles', {}).get('seuil_critique',0)})

--- 

*Rapport d'Observabilité généré par {rapport.get('agent_id', 'Agent Inconnu')} - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}*
*💡 {rapport.get('specialisation', 'Expert en Observabilité Système & Applicative Distribuée')}*
*📂 Sauvegardé dans : reports/*
"""
        return md_content

    async def _generer_markdown_performance_monitoring(self, rapport: Dict, context: Dict, timestamp) -> str:
        score = rapport.get('score_global', 0)
        niveau_qualite = rapport.get('niveau_qualite', 'N/A')
        conformite = rapport.get('conformite', 'N/A')
        signature_crypto = rapport.get('signature_cryptographique', 'N/A')
        agent_file_name = rapport.get('agent_file_name', rapport.get('agent_id', 'N/A'))
        issues_count = rapport.get('issues_critiques_identifies', 0)
        architecture = rapport.get('architecture_performance_monitoring', {})
        recommandations = rapport.get('recommandations_performance', [])
        issues_details = rapport.get('issues_critiques_performance_monitoring_details', [])
        details_tech = rapport.get('details_techniques_performance_monitoring', {})
        metriques_detaillees = rapport.get('metriques_performance_monitoring_detaillees', {})

        indicateurs_arch_list = architecture.get('indicateurs_cles_performance_architecture', [])
        indicateurs_arch_block = "\\\\n".join([f"- {i}" for i in indicateurs_arch_list]) if indicateurs_arch_list else "- Non spécifiés"
        
        recommandations_str_list = [f"- {r}" for r in recommandations]
        recommandations_block = "\\\\n".join(recommandations_str_list)
        
        issues_critiques_str_list = [f"- 🔴 {i}" for i in issues_details] if issues_count > 0 else ["- Aucun issue critique majeur de performance pour le système de monitoring détecté."]
        issues_block = "\\\\n".join(issues_critiques_str_list)

        kpis_suivis_list = details_tech.get('kpis_cles_performance_suivis', [])
        kpis_suivis_block = "\\\\n".join([f"  - {kpi}" for kpi in kpis_suivis_list]) if kpis_suivis_list else "  - Non spécifiés"
        
        outils_analyse_list = details_tech.get('outils_analyse_performance_simules', [])
        outils_analyse_str = ", ".join(outils_analyse_list) if outils_analyse_list else "Non spécifiés"

        md_content = f"""# 🚀 **RAPPORT PERFORMANCE DU SYSTÈME DE MONITORING : {rapport.get('agent_id', 'N/A')}**

**Date :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
**Module :** {agent_file_name}
**Score Global** : {score/10:.1f}/10
**Niveau Qualité** : {niveau_qualite}
**Conformité** : {conformite}
**Signature Cryptographique** : {signature_crypto}
**Issues Critiques** : {issues_count}

## 🏗️ Architecture d'Analyse de Performance du Monitoring
{architecture.get('description', 'Description non disponible.')}
- **Statut Opérationnel (Analyse Perf.) :** {architecture.get('statut_operationnel_performance', 'Non spécifié.')}
- **Confirmation Spécialisation (Analyse Perf.) :** {architecture.get('confirmation_specialisation_performance', 'Non confirmée.')}

**Indicateurs Clés de Performance de l'Architecture de Monitoring Suivis :**
{indicateurs_arch_block}

## 🔧 Recommandations d'Optimisation de Performance
{recommandations_block}

## 🚨 Issues Critiques de Performance du Monitoring
{issues_block}

## 📋 Détails Techniques d'Analyse de Performance
- **Stratégie d'Analyse de Performance :** {details_tech.get('strategie_analyse_performance', 'Non définie.')}
- **KPIs Clés de Performance Suivis (Détail) :**
{kpis_suivis_block}
- **Outils d'Analyse de Performance (simulés) :** {outils_analyse_str}
- **Ressources Allouées au Monitoring (simulé) :** {details_tech.get('ressources_allouees_monitoring_simule', 'N/A')}

## 📊 Métriques de Performance du Monitoring Détaillées
- **Score Global de Performance Monitoring :** {metriques_detaillees.get('score_performance_monitoring_global', {}).get('actuel',0)}/{metriques_detaillees.get('score_performance_monitoring_global', {}).get('cible',100)} {metriques_detaillees.get('score_performance_monitoring_global', {}).get('unite','points')}
- **Latence de Collecte (P95) :** {metriques_detaillees.get('latence_collecte_p95_ms', {}).get('actuel','N/A')}/{metriques_detaillees.get('latence_collecte_p95_ms', {}).get('cible','N/A')} {metriques_detaillees.get('latence_collecte_p95_ms', {}).get('unite','ms')}
- **Overhead Moyen des Agents (CPU) :** {metriques_detaillees.get('overhead_agents_cpu_pourcentage', {}).get('actuel','N/A')}/{metriques_detaillees.get('overhead_agents_cpu_pourcentage', {}).get('cible','N/A')} {metriques_detaillees.get('overhead_agents_cpu_pourcentage', {}).get('unite','%')}
- **Débit de Traitement des Données :** {metriques_detaillees.get('debit_traitement_events_par_sec', {}).get('actuel','N/A')}/{metriques_detaillees.get('debit_traitement_events_par_sec', {}).get('cible','N/A')} {metriques_detaillees.get('debit_traitement_events_par_sec', {}).get('unite','events/sec')}
- **Réactivité Globale du Système de Monitoring (Santé) :** {metriques_detaillees.get('reactivite_systeme_monitoring_sante', {}).get('actuel','N/A')}/{metriques_detaillees.get('reactivite_systeme_monitoring_sante', {}).get('cible','N/A')} {metriques_detaillees.get('reactivite_systeme_monitoring_sante', {}).get('unite','%')}

--- 

*Rapport Performance Monitoring généré par {rapport.get('agent_id', 'Agent Inconnu')} - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}*
*🚀 {rapport.get('specialisation', 'Analyse & Optimisation de Performance des Systèmes de Monitoring')}*
*📂 Sauvegardé dans : reports/*
"""
        return md_content

    async def _generer_markdown_alertes(self, rapport: Dict, context: Dict, timestamp) -> str:
        score = rapport.get('score_global', 0)
        niveau_qualite = rapport.get('niveau_qualite', 'N/A')
        conformite = rapport.get('conformite', 'N/A')
        issues_count = rapport.get('issues_critiques_identifies', 0)
        architecture = rapport.get('architecture_alertes', {})
        recommandations = rapport.get('recommandations_alertes', [])
        issues_details = rapport.get('issues_critiques_alertes_details', [])
        details_tech = rapport.get('details_techniques_alertes', {})
        metriques_detaillees = rapport.get('metriques_alertes_detaillees', {})

        composants_cles_str_list = [f"- {c}" for c in architecture.get('composants_cles', [])]
        composants_cles_block = "\\n".join(composants_cles_str_list)
        recommandations_str_list = [f"- {r}" for r in recommandations]
        recommandations_block = "\\n".join(recommandations_str_list)
        issues_critiques_str_list = [f"- 🔴 {i}" for i in issues_details] if issues_count > 0 else ["- Aucun issue critique majeur dans la gestion des alertes détecté."]
        issues_block = "\\n".join(issues_critiques_str_list)
        canaux_notification_str = ", ".join(details_tech.get('canaux_notification', []))
        severite_niveaux_str = ", ".join(details_tech.get('severite_niveaux', []))

        md_content = f"""# 🚨 **RAPPORT ALERTES : {rapport.get('agent_id', 'N/A')}**

**Date :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
**Module :** {rapport.get('agent_id', 'N/A')}
**Score Global** : {score/10:.1f}/10
**Niveau Qualité** : {niveau_qualite}
**Conformité** : {conformite}
**Issues Critiques** : {issues_count}

## 🏗️ Architecture Alertes
{architecture.get('description', 'Description non disponible.')}
**Composants clés :**
{composants_cles_block}

## 🔧 Recommandations Alertes
{recommandations_block}

## 🚨 Issues Critiques Alertes
{issues_block}

## 📋 Détails Techniques Alertes
- Nombre de règles actives : {details_tech.get('nombre_regles_actives', 'N/A')}
- Temps moyen de détection : {details_tech.get('temps_moyen_detection', 'N/A')}
- Canaux de notification : {canaux_notification_str}
- Niveaux de sévérité : {severite_niveaux_str}

## 📊 Métriques Alertes Détaillées
- Score Alertes Global : {metriques_detaillees.get('score_alertes_global', 0)}/100
- Nombre de Règles Configurées : {metriques_detaillees.get('nombre_regles_configurees', 0)}
- Alertes Actives en Cours : {metriques_detaillees.get('alertes_actives_en_cours', 0)}
- Pourcentage Couverture Alertes : {metriques_detaillees.get('pourcentage_couverture_alertes', 0)}%
- Score Nombre de Règles : {metriques_detaillees.get('score_nombre_regles', 0)}/30
- Score Alertes Actives : {metriques_detaillees.get('score_alertes_actives', 0)}/30
- Score Couverture : {metriques_detaillees.get('score_couverture', 0)}/40

--- 

*Rapport Alertes généré par {rapport.get('agent_id', 'Agent Inconnu')} - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}*
*📂 Sauvegardé dans : /mnt/c/Dev/nextgeneration/reports/*
"""
        return md_content

    def get_capabilities(self) -> list[str]: 
        return ["monitoring", "observability", "opentelemetry", "generate_strategic_report"]

    async def health_check(self) -> dict: 
        return {"status": "ok", "opentelemetry_available": OPENTELEMETRY_AVAILABLE}

def create_agent_06_specialiste_monitoring_sprint4(**config):
    return Agent06AdvancedMonitoring(**config)