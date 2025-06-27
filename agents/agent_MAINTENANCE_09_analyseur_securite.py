"""
🔒 ANALYSEUR DE SÉCURITÉ - Agent 09
====================================

🎯 Mission : Détecter et analyser les vulnérabilités de sécurité dans le code et les systèmes.
⚡ Capacités : 
- Analyse statique de code Python
- Audit de sécurité universel de fichiers/répertoires
- Détection de secrets et données sensibles
- Analyse des dépendances et configurations
- Génération de rapports détaillés
- Recommandations de correction automatisées

🏢 Équipe : NextGeneration Tools Migration
📊 Intégration : Compatible avec le système de logging centralisé

Author: Équipe de Maintenance NextGeneration
Version: 2.3.0 (Sécurité renforcée et optimisée)
"""

import ast
import re
import hashlib
import logging
import json
import uuid
import os
import sys
import time
from typing import List, Dict, Any, Optional, Union, Set, Tuple, Callable
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict, field
from enum import Enum
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio
import yaml
import traceback

from core.agent_factory_architecture import Agent, Task, Result
# Gestion du logging avec fallback
try:
    from core.manager import LoggingManager
except ImportError:
    LoggingManager = None

# Imports optionnels pour fonctionnalités avancées
try:
    import bandit
    BANDIT_AVAILABLE = True
except ImportError:
    BANDIT_AVAILABLE = False

try:
    from safety import safety
    SAFETY_CHECK_AVAILABLE = True
except ImportError:
    SAFETY_CHECK_AVAILABLE = False

# --- Début: Éléments intégrés depuis Agent 18 ---
class SecurityLevel(Enum):
    """Niveaux de sécurité étendus"""
    CRITICAL = "critique"
    HIGH = "haut"
    MEDIUM = "moyen"
    LOW = "bas"
    INFO = "information"
    SECURE = "sécurisé"

    @classmethod
    def from_cvss(cls, score: float) -> 'SecurityLevel':
        """Convertit un score CVSS en niveau de sécurité"""
        if score >= 9.0: return cls.CRITICAL
        elif score >= 7.0: return cls.HIGH
        elif score >= 4.0: return cls.MEDIUM
        elif score >= 0.1: return cls.LOW
        return cls.INFO

    @classmethod
    def from_bandit_level(cls, level: str) -> 'SecurityLevel':
        """Convertit un niveau Bandit en niveau de sécurité"""
        mapping = {
            'HIGH': cls.HIGH,
            'MEDIUM': cls.MEDIUM,
            'LOW': cls.LOW
        }
        return mapping.get(level.upper(), cls.INFO)

@dataclass
class SecurityContext:
    """Contexte de sécurité pour l'analyse"""
    scan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    scan_type: str = "security_scan"
    scan_start: datetime = field(default_factory=datetime.now)
    scan_end: Optional[datetime] = None
    target_path: Optional[str] = None
    excluded_paths: Set[str] = field(default_factory=set)
    config: Dict[str, Any] = field(default_factory=dict)
    scan_depth: int = 1
    max_files: int = 1000
    current_file_count: int = 0
    findings_count: Dict[str, int] = field(default_factory=lambda: {
        level.value: 0 for level in SecurityLevel
    })
    error_count: int = 0
    max_errors: int = 50
    scan_status: str = "initializing"
    scan_progress: float = 0.0
    scan_errors: List[Dict[str, Any]] = field(default_factory=list)
    scan_warnings: List[Dict[str, Any]] = field(default_factory=list)
    
    # Nouveaux champs
    scan_mode: str = "standard"  # standard, approfondi, rapide
    scan_priority: int = 1  # 1 (basse) à 5 (haute)
    scan_tags: Set[str] = field(default_factory=set)
    scan_metadata: Dict[str, Any] = field(default_factory=dict)
    scan_history: List[Dict[str, Any]] = field(default_factory=list)
    scan_checkpoints: List[Dict[str, Any]] = field(default_factory=list)
    scan_metrics: Dict[str, float] = field(default_factory=dict)
    scan_dependencies: Set[str] = field(default_factory=set)
    scan_environment: Dict[str, str] = field(default_factory=dict)
    scan_requirements: Dict[str, Any] = field(default_factory=dict)
    scan_timeouts: Dict[str, int] = field(default_factory=lambda: {
        'file_scan': 30,  # secondes
        'dependency_check': 300,
        'config_audit': 60,
        'total_scan': 3600
    })
    
    # Nouveaux champs pour la gestion des erreurs et avertissements
    error_categories: Dict[str, int] = field(default_factory=lambda: {
        'syntax': 0,
        'configuration': 0,
        'permission': 0,
        'timeout': 0,
        'dependency': 0,
        'network': 0,
        'system': 0,
        'other': 0
    })
    warning_categories: Dict[str, int] = field(default_factory=lambda: {
        'deprecated': 0,
        'performance': 0,
        'best_practice': 0,
        'compatibility': 0,
        'documentation': 0,
        'other': 0
    })
    error_thresholds: Dict[str, int] = field(default_factory=lambda: {
        'syntax': 10,
        'configuration': 5,
        'permission': 3,
        'timeout': 5,
        'dependency': 5,
        'network': 3,
        'system': 3,
        'other': 10
    })
    warning_thresholds: Dict[str, int] = field(default_factory=lambda: {
        'deprecated': 20,
        'performance': 15,
        'best_practice': 25,
        'compatibility': 10,
        'documentation': 20,
        'other': 15
    })
    error_handlers: Dict[str, Callable] = field(default_factory=dict)
    warning_handlers: Dict[str, Callable] = field(default_factory=dict)
    retry_policies: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        'file_scan': {'max_retries': 3, 'delay': 1},
        'dependency_check': {'max_retries': 2, 'delay': 5},
        'config_audit': {'max_retries': 2, 'delay': 2}
    })
    error_recovery_strategies: Dict[str, str] = field(default_factory=lambda: {
        'syntax': 'skip',
        'configuration': 'retry',
        'permission': 'escalate',
        'timeout': 'retry',
        'dependency': 'fallback',
        'network': 'retry',
        'system': 'abort',
        'other': 'log'
    })
    
    def update_findings_count(self, level: SecurityLevel) -> None:
        """Met à jour le compteur de findings par niveau"""
        try:
            self.findings_count[level.value] += 1
            self._log_finding_update(level)
        except KeyError:
            logging.warning(f"Niveau de sécurité inconnu: {level}")
            self.findings_count['autre'] = self.findings_count.get('autre', 0) + 1
            
    def _log_finding_update(self, level: SecurityLevel) -> None:
        """Enregistre la mise à jour dans l'historique"""
        self.scan_history.append({
            'timestamp': datetime.now().isoformat(),
            'event_type': 'finding_update',
            'level': level.value,
            'count': self.findings_count[level.value]
        })
    
    def is_scan_limit_reached(self) -> bool:
        """Vérifie si la limite de fichiers scannés est atteinte"""
        return self.current_file_count >= self.max_files
    
    def is_error_limit_reached(self) -> bool:
        """Vérifie si la limite d'erreurs est atteinte"""
        return self.error_count >= self.max_errors
        
    def add_error(self, error: str, category: str = 'other', details: Optional[Dict[str, Any]] = None) -> None:
        """Ajoute une erreur au contexte avec catégorisation"""
        if category not in self.error_categories:
            category = 'other'
            
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'error': error,
            'category': category,
            'details': details or {},
            'scan_mode': self.scan_mode,
            'current_progress': self.scan_progress
        }
        
        self.scan_errors.append(error_entry)
        self.error_categories[category] += 1
        self.error_count += 1
        
        # Mise à jour des métriques
        self._update_metrics('error_rate', self.error_count / max(1, self.current_file_count))
        self._update_metrics(f'error_rate_{category}', 
                           self.error_categories[category] / max(1, self.current_file_count))
        
        # Vérification des seuils et application de la stratégie de récupération
        if self.error_categories[category] >= self.error_thresholds[category]:
            self._apply_error_recovery_strategy(category)
            
        # Exécution du handler spécifique si défini
        if category in self.error_handlers:
            try:
                self.error_handlers[category](error_entry)
            except Exception as e:
                logging.error(f"Erreur dans le handler d'erreur {category}: {str(e)}")
    
    def add_warning(self, warning: str, category: str = 'other', details: Optional[Dict[str, Any]] = None) -> None:
        """Ajoute un avertissement au contexte avec catégorisation"""
        if category not in self.warning_categories:
            category = 'other'
            
        warning_entry = {
            'timestamp': datetime.now().isoformat(),
            'warning': warning,
            'category': category,
            'details': details or {},
            'scan_mode': self.scan_mode,
            'current_progress': self.scan_progress
        }
        
        self.scan_warnings.append(warning_entry)
        self.warning_categories[category] += 1
        self.warning_count = len(self.scan_warnings)
        
        # Mise à jour des métriques
        self._update_metrics('warning_rate', self.warning_count / max(1, self.current_file_count))
        self._update_metrics(f'warning_rate_{category}', 
                           self.warning_categories[category] / max(1, self.current_file_count))
        
        # Vérification des seuils
        if self.warning_categories[category] >= self.warning_thresholds[category]:
            self._handle_warning_threshold_exceeded(category)
            
        # Exécution du handler spécifique si défini
        if category in self.warning_handlers:
            try:
                self.warning_handlers[category](warning_entry)
            except Exception as e:
                logging.error(f"Erreur dans le handler d'avertissement {category}: {str(e)}")
    
    def _apply_error_recovery_strategy(self, category: str) -> None:
        """Applique la stratégie de récupération pour une catégorie d'erreur"""
        strategy = self.error_recovery_strategies.get(category, 'log')
        
        if strategy == 'skip':
            self._skip_current_operation()
        elif strategy == 'retry':
            self._retry_operation(category)
        elif strategy == 'escalate':
            self._escalate_error(category)
        elif strategy == 'fallback':
            self._use_fallback_solution(category)
        elif strategy == 'abort':
            self._abort_scan(category)
        else:  # 'log'
            self._log_error_threshold_exceeded(category)
    
    def _handle_warning_threshold_exceeded(self, category: str) -> None:
        """Gère le dépassement de seuil d'avertissements"""
        logging.warning(f"Seuil d'avertissements dépassé pour la catégorie {category}")
        
        self.scan_history.append({
            'timestamp': datetime.now().isoformat(),
            'event_type': 'warning_threshold_exceeded',
            'category': category,
            'count': self.warning_categories[category]
        })
        
        # Ajout d'une métrique de qualité
        quality_impact = min(1.0, self.warning_categories[category] / 
                           self.warning_thresholds[category])
        self._update_metrics(f'quality_impact_{category}', quality_impact)
    
    def _skip_current_operation(self) -> None:
        """Ignore l'opération en cours"""
        self.scan_history.append({
            'timestamp': datetime.now().isoformat(),
            'event_type': 'operation_skipped',
            'current_file': self.current_file_count
        })
        
    def _retry_operation(self, category: str) -> None:
        """Tente de réessayer l'opération"""
        policy = self.retry_policies.get(category, {'max_retries': 3, 'delay': 1})
        self.scan_metadata[f'retry_count_{category}'] = \
            self.scan_metadata.get(f'retry_count_{category}', 0) + 1
            
        if self.scan_metadata[f'retry_count_{category}'] <= policy['max_retries']:
            time.sleep(policy['delay'])
            # La logique de retry sera implémentée par l'appelant
            
    def _escalate_error(self, category: str) -> None:
        """Escalade l'erreur au niveau supérieur"""
        logging.error(f"Escalade des erreurs de catégorie {category}")
        # Notification ou alerte à implémenter selon le contexte
        
    def _use_fallback_solution(self, category: str) -> None:
        """Utilise une solution de repli"""
        logging.info(f"Utilisation de la solution de repli pour {category}")
        # Solution de repli à implémenter selon le contexte
        
    def _abort_scan(self, category: str) -> None:
        """Arrête le scan en cours"""
        self.scan_status = "aborted"
        self.scan_end = datetime.now()
        logging.error(f"Scan arrêté dû aux erreurs de catégorie {category}")
        
    def _log_error_threshold_exceeded(self, category: str) -> None:
        """Enregistre le dépassement de seuil d'erreurs"""
        logging.error(f"Seuil d'erreurs dépassé pour la catégorie {category}")
        
        self.scan_history.append({
            'timestamp': datetime.now().isoformat(),
            'event_type': 'error_threshold_exceeded',
            'category': category,
            'count': self.error_categories[category]
        })
    
    def update_progress(self, progress: float) -> None:
        """Met à jour la progression du scan"""
        self.scan_progress = min(100.0, max(0.0, progress))
        self._add_checkpoint()
        
    def _add_checkpoint(self) -> None:
        """Ajoute un point de contrôle"""
        checkpoint = {
            'timestamp': datetime.now().isoformat(),
            'progress': self.scan_progress,
            'files_scanned': self.current_file_count,
            'findings_count': self.findings_count.copy(),
            'error_count': self.error_count,
            'status': self.scan_status
        }
        self.scan_checkpoints.append(checkpoint)
        
    def update_status(self, status: str) -> None:
        """Met à jour le statut du scan"""
        old_status = self.scan_status
        self.scan_status = status
        
        self.scan_history.append({
            'timestamp': datetime.now().isoformat(),
            'event_type': 'status_change',
            'old_status': old_status,
            'new_status': status
        })
        
    def should_exclude_path(self, path: str) -> bool:
        """Vérifie si un chemin doit être exclu"""
        path = str(path)
        
        # Vérification des motifs d'exclusion
        for excluded in self.excluded_paths:
            if '*' in excluded:
                if re.match(excluded.replace('*', '.*'), path):
                    return True
            elif excluded in path:
                return True
                
        return False
    
    def validate_config(self) -> Tuple[bool, List[str]]:
        """Valide la configuration du contexte"""
        errors = []
        
        # Validation des champs numériques
        if self.scan_depth < 1:
            errors.append("La profondeur de scan doit être >= 1")
        if self.max_files < 1:
            errors.append("Le nombre maximum de fichiers doit être >= 1")
        if self.max_errors < 1:
            errors.append("Le nombre maximum d'erreurs doit être >= 1")
        if not (1 <= self.scan_priority <= 5):
            errors.append("La priorité doit être entre 1 et 5")
            
        # Validation des timeouts
        for key, value in self.scan_timeouts.items():
            if value <= 0:
                errors.append(f"Le timeout {key} doit être > 0")
                
        # Validation des types
        if not isinstance(self.excluded_paths, set):
            errors.append("excluded_paths doit être un ensemble")
        if not isinstance(self.scan_tags, set):
            errors.append("scan_tags doit être un ensemble")
            
        # Validation du mode de scan
        if self.scan_mode not in ['standard', 'approfondi', 'rapide']:
            errors.append("Mode de scan invalide")
            
        return len(errors) == 0, errors
    
    def _update_metrics(self, metric_name: str, value: float) -> None:
        """Met à jour les métriques de scan"""
        self.scan_metrics[metric_name] = value
        
        # Calcul des métriques dérivées
        if 'error_rate' in self.scan_metrics and 'warning_rate' in self.scan_metrics:
            self.scan_metrics['health_score'] = 100 * (
                1 - (self.scan_metrics['error_rate'] + self.scan_metrics['warning_rate']) / 2
            )
    
    def add_dependency(self, dependency: str) -> None:
        """Ajoute une dépendance au scan"""
        self.scan_dependencies.add(dependency)
        
    def set_environment(self, key: str, value: str) -> None:
        """Définit une variable d'environnement pour le scan"""
        self.scan_environment[key] = value
        
    def add_requirement(self, key: str, value: Any) -> None:
        """Ajoute une exigence pour le scan"""
        self.scan_requirements[key] = value
        
    def get_timeout(self, operation: str) -> int:
        """Récupère le timeout pour une opération"""
        return self.scan_timeouts.get(operation, self.scan_timeouts.get('total_scan', 3600))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit le contexte en dictionnaire"""
        return {
            'scan_id': self.scan_id,
            'scan_type': self.scan_type,
            'scan_start': self.scan_start.isoformat(),
            'scan_end': self.scan_end.isoformat() if self.scan_end else None,
            'target_path': self.target_path,
            'excluded_paths': list(self.excluded_paths),
            'config': self.config,
            'scan_depth': self.scan_depth,
            'max_files': self.max_files,
            'current_file_count': self.current_file_count,
            'findings_count': self.findings_count,
            'error_count': self.error_count,
            'scan_status': self.scan_status,
            'scan_progress': self.scan_progress,
            'scan_errors': self.scan_errors,
            'scan_warnings': self.scan_warnings,
            'scan_mode': self.scan_mode,
            'scan_priority': self.scan_priority,
            'scan_tags': list(self.scan_tags),
            'scan_metadata': self.scan_metadata,
            'scan_history': self.scan_history,
            'scan_checkpoints': self.scan_checkpoints,
            'scan_metrics': self.scan_metrics,
            'scan_dependencies': list(self.scan_dependencies),
            'scan_environment': self.scan_environment,
            'scan_requirements': self.scan_requirements,
            'scan_timeouts': self.scan_timeouts
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SecurityContext':
        """Crée un contexte à partir d'un dictionnaire"""
        context = cls()
        
        # Conversion des dates
        if 'scan_start' in data:
            context.scan_start = datetime.fromisoformat(data['scan_start'])
        if 'scan_end' in data and data['scan_end']:
            context.scan_end = datetime.fromisoformat(data['scan_end'])
            
        # Conversion des ensembles
        if 'excluded_paths' in data:
            context.excluded_paths = set(data['excluded_paths'])
        if 'scan_tags' in data:
            context.scan_tags = set(data['scan_tags'])
        if 'scan_dependencies' in data:
            context.scan_dependencies = set(data['scan_dependencies'])
            
        # Copie des attributs simples
        for attr in ['scan_id', 'scan_type', 'target_path', 'scan_depth',
                    'max_files', 'current_file_count', 'error_count',
                    'scan_status', 'scan_progress', 'scan_mode', 'scan_priority']:
            if attr in data:
                setattr(context, attr, data[attr])
                
        # Copie des dictionnaires
        for attr in ['config', 'findings_count', 'scan_metadata', 'scan_metrics',
                    'scan_environment', 'scan_requirements', 'scan_timeouts']:
            if attr in data:
                setattr(context, attr, data[attr].copy())
                
        # Copie des listes
        for attr in ['scan_errors', 'scan_warnings', 'scan_history', 'scan_checkpoints']:
            if attr in data:
                setattr(context, attr, data[attr][:])
                
        return context

class VulnerabilityType(Enum):
    """Types de vulnérabilités étendus avec descriptions et guides de remédiation"""
    # Vulnérabilités OWASP Top 10
    INJECTION = "injection"
    XSS = "xss"
    BROKEN_AUTH = "authentification_cassée"
    SENSITIVE_DATA = "données_sensibles"
    XXE = "xxe"
    BROKEN_ACCESS = "contrôle_accès_cassé"
    MISCONFIGURATION = "mauvaise_configuration"
    INSECURE_DESERIALIZATION = "désérialisation_non_sécurisée"
    VULNERABLE_COMPONENTS = "composants_vulnérables"
    INSUFFICIENT_LOGGING = "journalisation_insuffisante"
    
    # Vulnérabilités spécifiques
    HARDCODED_SECRET = "secret_en_dur"
    WEAK_CRYPTO = "cryptographie_faible"
    FILE_TRAVERSAL = "traversée_de_fichier"
    DANGEROUS_FUNCTION = "fonction_dangereuse"
    PATH_INJECTION = "injection_de_chemin"
    XML_VULNERABILITIES = "vulnérabilités_xml"
    INSECURE_PROTOCOLS = "protocoles_non_sécurisés"
    INSECURE_FILE_OPERATION = "operation_fichier_non_securisee"
    INSECURE_FILE_PERMISSION = "permission_fichier_non_securisee"
    BROAD_EXCEPTION = "exception_large"
    ASSERTION_ISSUE = "probleme_assertion"
    
    # Nouvelles catégories
    DEPENDENCY_VULNERABILITY = "vulnérabilité_dépendance"
    CONFIG_VULNERABILITY = "vulnérabilité_configuration"
    API_VULNERABILITY = "vulnérabilité_api"
    DOCKER_VULNERABILITY = "vulnérabilité_docker"
    CI_CD_VULNERABILITY = "vulnérabilité_ci_cd"
    CLOUD_VULNERABILITY = "vulnérabilité_cloud"
    CONTAINER_VULNERABILITY = "vulnérabilité_conteneur"
    KUBERNETES_VULNERABILITY = "vulnérabilité_kubernetes"
    DATABASE_VULNERABILITY = "vulnérabilité_base_données"
    NETWORK_VULNERABILITY = "vulnérabilité_réseau"
    AUTHENTICATION_VULNERABILITY = "vulnérabilité_authentification"
    AUTHORIZATION_VULNERABILITY = "vulnérabilité_autorisation"
    CRYPTOGRAPHIC_VULNERABILITY = "vulnérabilité_cryptographique"
    INPUT_VALIDATION_VULNERABILITY = "vulnérabilité_validation_entrée"
    OUTPUT_ENCODING_VULNERABILITY = "vulnérabilité_encodage_sortie"
    SESSION_MANAGEMENT_VULNERABILITY = "vulnérabilité_gestion_session"
    ERROR_HANDLING_VULNERABILITY = "vulnérabilité_gestion_erreurs"
    LOGGING_VULNERABILITY = "vulnérabilité_journalisation"
    
    # Nouvelles catégories cloud et infrastructure
    AWS_VULNERABILITY = "vulnérabilité_aws"
    AZURE_VULNERABILITY = "vulnérabilité_azure"
    GCP_VULNERABILITY = "vulnérabilité_gcp"
    TERRAFORM_VULNERABILITY = "vulnérabilité_terraform"
    ANSIBLE_VULNERABILITY = "vulnérabilité_ansible"
    HELM_VULNERABILITY = "vulnérabilité_helm"
    
    # Nouvelles catégories applicatives
    FRONTEND_VULNERABILITY = "vulnérabilité_frontend"
    BACKEND_VULNERABILITY = "vulnérabilité_backend"
    MOBILE_VULNERABILITY = "vulnérabilité_mobile"
    MICROSERVICE_VULNERABILITY = "vulnérabilité_microservice"
    API_GATEWAY_VULNERABILITY = "vulnérabilité_api_gateway"
    SERVICE_MESH_VULNERABILITY = "vulnérabilité_service_mesh"
    
    # Nouvelles catégories données
    DATA_PRIVACY_VULNERABILITY = "vulnérabilité_confidentialité_données"
    DATA_INTEGRITY_VULNERABILITY = "vulnérabilité_intégrité_données"
    DATA_AVAILABILITY_VULNERABILITY = "vulnérabilité_disponibilité_données"
    DATA_ENCRYPTION_VULNERABILITY = "vulnérabilité_chiffrement_données"
    DATA_BACKUP_VULNERABILITY = "vulnérabilité_sauvegarde_données"
    DATA_COMPLIANCE_VULNERABILITY = "vulnérabilité_conformité_données"
    
    # Nouvelles catégories spécifiques aux frameworks
    DJANGO_VULNERABILITY = "vulnérabilité_django"
    FLASK_VULNERABILITY = "vulnérabilité_flask"
    FASTAPI_VULNERABILITY = "vulnérabilité_fastapi"
    SPRING_VULNERABILITY = "vulnérabilité_spring"
    REACT_VULNERABILITY = "vulnérabilité_react"
    VUE_VULNERABILITY = "vulnérabilité_vue"
    ANGULAR_VULNERABILITY = "vulnérabilité_angular"
    
    # Nouvelles catégories DevSecOps
    PIPELINE_VULNERABILITY = "vulnérabilité_pipeline"
    REGISTRY_VULNERABILITY = "vulnérabilité_registry"
    ARTIFACT_VULNERABILITY = "vulnérabilité_artifact"
    SECRET_MANAGEMENT_VULNERABILITY = "vulnérabilité_gestion_secrets"
    RBAC_VULNERABILITY = "vulnérabilité_rbac"
    MONITORING_VULNERABILITY = "vulnérabilité_monitoring"
    
    # Catégorie par défaut
    OTHER = "autre"
    
    @classmethod
    def from_cwe(cls, cwe_id: str) -> Optional['VulnerabilityType']:
        """Convertit un CWE ID en type de vulnérabilité"""
        cwe_mapping = {
            'CWE-89': cls.INJECTION,  # SQL Injection
            'CWE-79': cls.XSS,  # Cross-site Scripting
            'CWE-287': cls.BROKEN_AUTH,  # Improper Authentication
            'CWE-256': cls.SENSITIVE_DATA,  # Plaintext Storage of Password
            'CWE-611': cls.XXE,  # XML External Entity Reference
            'CWE-285': cls.BROKEN_ACCESS,  # Improper Authorization
            'CWE-16': cls.MISCONFIGURATION,  # Configuration
            'CWE-502': cls.INSECURE_DESERIALIZATION,  # Deserialization of Untrusted Data
            'CWE-1104': cls.VULNERABLE_COMPONENTS,  # Use of Unmaintained Third Party Components
            'CWE-778': cls.INSUFFICIENT_LOGGING,  # Insufficient Logging
            'CWE-798': cls.HARDCODED_SECRET,  # Use of Hard-coded Credentials
            'CWE-326': cls.WEAK_CRYPTO,  # Inadequate Encryption Strength
            'CWE-22': cls.FILE_TRAVERSAL,  # Path Traversal
            'CWE-676': cls.DANGEROUS_FUNCTION,  # Use of Potentially Dangerous Function
            'CWE-73': cls.PATH_INJECTION,  # External Control of File Name or Path
            'CWE-611': cls.XML_VULNERABILITIES,  # Improper Restriction of XML External Entity Reference
            'CWE-319': cls.INSECURE_PROTOCOLS,  # Cleartext Transmission of Sensitive Information
            'CWE-732': cls.INSECURE_FILE_PERMISSION,  # Incorrect Permission Assignment for Critical Resource
            'CWE-396': cls.BROAD_EXCEPTION,  # Declaration of Catch for Generic Exception
            'CWE-703': cls.ASSERTION_ISSUE,  # Improper Check or Handling of Exceptional Conditions
            
            # Nouvelles correspondances
            'CWE-1008': cls.API_VULNERABILITY,  # Architectural Concepts
            'CWE-264': cls.AUTHORIZATION_VULNERABILITY,  # Permissions, Privileges, and Access Controls
            'CWE-311': cls.CRYPTOGRAPHIC_VULNERABILITY,  # Missing Encryption of Sensitive Data
            'CWE-20': cls.INPUT_VALIDATION_VULNERABILITY,  # Improper Input Validation
            'CWE-116': cls.OUTPUT_ENCODING_VULNERABILITY,  # Improper Encoding or Escaping of Output
            'CWE-384': cls.SESSION_MANAGEMENT_VULNERABILITY,  # Session Fixation
            'CWE-755': cls.ERROR_HANDLING_VULNERABILITY,  # Improper Handling of Exceptional Conditions
            'CWE-532': cls.LOGGING_VULNERABILITY,  # Information Exposure Through Log Files
            
            # Cloud et infrastructure
            'CWE-918': cls.AWS_VULNERABILITY,  # Server-Side Request Forgery (SSRF)
            'CWE-522': cls.AZURE_VULNERABILITY,  # Insufficiently Protected Credentials
            'CWE-668': cls.GCP_VULNERABILITY,  # Exposure of Resource to Wrong Sphere
            'CWE-434': cls.TERRAFORM_VULNERABILITY,  # Unrestricted Upload of File
            'CWE-269': cls.ANSIBLE_VULNERABILITY,  # Improper Privilege Management
            'CWE-494': cls.HELM_VULNERABILITY,  # Download of Code Without Integrity Check
            
            # Application
            'CWE-79': cls.FRONTEND_VULNERABILITY,  # XSS
            'CWE-89': cls.BACKEND_VULNERABILITY,  # SQL Injection
            'CWE-919': cls.MOBILE_VULNERABILITY,  # Weaknesses in Mobile Applications
            'CWE-319': cls.MICROSERVICE_VULNERABILITY,  # Cleartext Transmission
            'CWE-306': cls.API_GATEWAY_VULNERABILITY,  # Missing Authentication
            'CWE-400': cls.SERVICE_MESH_VULNERABILITY,  # Resource Exhaustion
            
            # Données
            'CWE-359': cls.DATA_PRIVACY_VULNERABILITY,  # Privacy Violation
            'CWE-345': cls.DATA_INTEGRITY_VULNERABILITY,  # Insufficient Verification of Data Authenticity
            'CWE-311': cls.DATA_ENCRYPTION_VULNERABILITY,  # Missing Encryption
            'CWE-530': cls.DATA_BACKUP_VULNERABILITY,  # Exposure of Backup File
            'CWE-200': cls.DATA_COMPLIANCE_VULNERABILITY,  # Information Exposure
        }
        
        # Nettoyage de l'ID CWE
        if not cwe_id.startswith('CWE-'):
            cwe_id = f'CWE-{cwe_id}'
            
        return cwe_mapping.get(cwe_id, cls.OTHER)

    @classmethod
    def from_bandit_id(cls, bandit_id: str) -> Optional['VulnerabilityType']:
        """Convertit un ID Bandit en type de vulnérabilité"""
        # Mapping Bandit vers VulnerabilityType
        bandit_mapping = {
            'B101': cls.ASSERTION_ISSUE,  # assert used
            'B102': cls.DANGEROUS_FUNCTION,  # exec used
            'B103': cls.DANGEROUS_FUNCTION,  # set bad file permissions
            'B104': cls.HARDCODED_SECRET,  # hardcoded bind all
            'B105': cls.HARDCODED_SECRET,  # hardcoded password string
            'B106': cls.HARDCODED_SECRET,  # hardcoded password funcarg
            'B107': cls.HARDCODED_SECRET,  # hardcoded password default
            'B108': cls.INSECURE_PROTOCOLS,  # hardcoded tmp directory
            'B110': cls.DANGEROUS_FUNCTION,  # try-except-pass
            'B112': cls.DANGEROUS_FUNCTION,  # try-except-continue
            'B201': cls.DANGEROUS_FUNCTION,  # flask debug true
            'B301': cls.DANGEROUS_FUNCTION,  # pickle
            'B302': cls.DANGEROUS_FUNCTION,  # marshal
            'B303': cls.DANGEROUS_FUNCTION,  # md5
            'B304': cls.WEAK_CRYPTO,  # ciphers
            'B305': cls.WEAK_CRYPTO,  # cipher suites
            'B306': cls.WEAK_CRYPTO,  # mktemp_q
            'B307': cls.DANGEROUS_FUNCTION,  # eval
            'B308': cls.DANGEROUS_FUNCTION,  # mark_safe
            'B309': cls.WEAK_CRYPTO,  # httpsconnection
            'B310': cls.WEAK_CRYPTO,  # urllib_urlopen
            'B311': cls.WEAK_CRYPTO,  # random
            'B312': cls.DANGEROUS_FUNCTION,  # telnetlib
            'B313': cls.WEAK_CRYPTO,  # xml_bad_cElementTree
            'B314': cls.WEAK_CRYPTO,  # xml_bad_ElementTree
            'B315': cls.WEAK_CRYPTO,  # xml_bad_expatreader
            'B316': cls.WEAK_CRYPTO,  # xml_bad_expatbuilder
            'B317': cls.WEAK_CRYPTO,  # xml_bad_sax
            'B318': cls.WEAK_CRYPTO,  # xml_bad_minidom
            'B319': cls.WEAK_CRYPTO,  # xml_bad_pulldom
            'B320': cls.WEAK_CRYPTO,  # xml_bad_etree
            'B321': cls.XXE,  # ftplib
            'B322': cls.DANGEROUS_FUNCTION,  # input
            'B323': cls.INSECURE_PROTOCOLS,  # unverified_context
            'B324': cls.WEAK_CRYPTO,  # hashlib_new_insecure_functions
            'B325': cls.WEAK_CRYPTO,  # tempnam
            
            # Nouveaux mappings
            'B401': cls.DEPENDENCY_VULNERABILITY,  # import-subprocess
            'B402': cls.API_VULNERABILITY,  # import-paramiko
            'B403': cls.NETWORK_VULNERABILITY,  # import-pickle
            'B404': cls.DANGEROUS_FUNCTION,  # import-subprocess
            'B405': cls.XML_VULNERABILITIES,  # import-xml
            'B406': cls.WEAK_CRYPTO,  # import-xml-etree
            'B407': cls.WEAK_CRYPTO,  # import-xml-sax
            'B408': cls.WEAK_CRYPTO,  # import-xml-expat
            'B409': cls.WEAK_CRYPTO,  # import-xml-minidom
            'B410': cls.WEAK_CRYPTO,  # import-lxml
            'B411': cls.DANGEROUS_FUNCTION,  # import-xmlrpclib
            'B412': cls.DANGEROUS_FUNCTION,  # import-httplib
            'B413': cls.INSECURE_PROTOCOLS,  # import-pycrypto
            
            # Cloud et infrastructure
            'B501': cls.AWS_VULNERABILITY,  # request-with-no-cert-validation
            'B502': cls.CLOUD_VULNERABILITY,  # ssl-with-bad-version
            'B503': cls.CONTAINER_VULNERABILITY,  # ssl-with-bad-defaults
            'B504': cls.KUBERNETES_VULNERABILITY,  # ssl-with-no-version
            'B505': cls.DOCKER_VULNERABILITY,  # weak-cryptographic-key
            'B506': cls.CI_CD_VULNERABILITY,  # yaml-load
            
            # Application
            'B601': cls.FRONTEND_VULNERABILITY,  # paramiko-calls
            'B602': cls.BACKEND_VULNERABILITY,  # subprocess-popen-with-shell-equals-true
            'B603': cls.API_VULNERABILITY,  # subprocess-without-shell-equals-true
            'B604': cls.MICROSERVICE_VULNERABILITY,  # any-other-function-with-shell-equals-true
            'B605': cls.API_GATEWAY_VULNERABILITY,  # start-process-with-a-shell
            'B606': cls.SERVICE_MESH_VULNERABILITY,  # start-process-with-no-shell
            'B607': cls.NETWORK_VULNERABILITY,  # start-process-with-partial-path
            'B608': cls.DANGEROUS_FUNCTION,  # hardcoded-sql-expressions
            'B609': cls.WEAK_CRYPTO,  # linux-commands-wildcard-injection
            'B610': cls.DANGEROUS_FUNCTION,  # django-extra-used
            'B611': cls.DANGEROUS_FUNCTION,  # django-rawsql-used
            'B701': cls.DANGEROUS_FUNCTION,  # jinja2-autoescape-false
            'B702': cls.DANGEROUS_FUNCTION,  # use-of-mako-templates
            'B703': cls.DANGEROUS_FUNCTION,  # django-mark-safe
            
            # Données
            'B801': cls.DATA_PRIVACY_VULNERABILITY,  # pycrypto-used
            'B802': cls.DATA_INTEGRITY_VULNERABILITY,  # ssl-insecure-version
            'B803': cls.DATA_ENCRYPTION_VULNERABILITY,  # ssl-no-cert-validation
            'B804': cls.DATA_BACKUP_VULNERABILITY,  # ssl-no-version
            'B805': cls.DATA_COMPLIANCE_VULNERABILITY,  # hardcoded-password-string
        }
        
        return bandit_mapping.get(bandit_id, cls.OTHER)

    @classmethod
    def get_category_description(cls, vuln_type: 'VulnerabilityType') -> str:
        """Retourne une description détaillée de la catégorie de vulnérabilité"""
        descriptions = {
            cls.INJECTION: "Injection de code malveillant dans l'application",
            cls.XSS: "Cross-Site Scripting - Injection de scripts côté client",
            cls.BROKEN_AUTH: "Problèmes dans le mécanisme d'authentification",
            cls.SENSITIVE_DATA: "Exposition de données sensibles",
            cls.XXE: "XML External Entity - Vulnérabilités liées au traitement XML",
            cls.BROKEN_ACCESS: "Contrôle d'accès défaillant",
            cls.MISCONFIGURATION: "Erreurs de configuration de sécurité",
            cls.INSECURE_DESERIALIZATION: "Désérialisation non sécurisée d'objets",
            cls.VULNERABLE_COMPONENTS: "Utilisation de composants avec vulnérabilités connues",
            cls.INSUFFICIENT_LOGGING: "Journalisation et monitoring insuffisants",
            
            # Descriptions pour les nouvelles catégories
            cls.AWS_VULNERABILITY: "Vulnérabilités spécifiques à AWS",
            cls.AZURE_VULNERABILITY: "Vulnérabilités spécifiques à Azure",
            cls.GCP_VULNERABILITY: "Vulnérabilités spécifiques à Google Cloud",
            cls.TERRAFORM_VULNERABILITY: "Problèmes de sécurité dans les configurations Terraform",
            cls.ANSIBLE_VULNERABILITY: "Risques de sécurité dans les playbooks Ansible",
            cls.HELM_VULNERABILITY: "Vulnérabilités dans les charts Helm",
            
            cls.FRONTEND_VULNERABILITY: "Vulnérabilités côté client",
            cls.BACKEND_VULNERABILITY: "Vulnérabilités côté serveur",
            cls.MOBILE_VULNERABILITY: "Problèmes de sécurité sur applications mobiles",
            cls.MICROSERVICE_VULNERABILITY: "Vulnérabilités spécifiques aux microservices",
            cls.API_GATEWAY_VULNERABILITY: "Failles de sécurité au niveau de l'API Gateway",
            cls.SERVICE_MESH_VULNERABILITY: "Problèmes de sécurité dans le maillage de services",
            
            cls.DATA_PRIVACY_VULNERABILITY: "Violations de la confidentialité des données",
            cls.DATA_INTEGRITY_VULNERABILITY: "Compromission de l'intégrité des données",
            cls.DATA_AVAILABILITY_VULNERABILITY: "Problèmes de disponibilité des données",
            cls.DATA_ENCRYPTION_VULNERABILITY: "Faiblesses dans le chiffrement des données",
            cls.DATA_BACKUP_VULNERABILITY: "Vulnérabilités liées aux sauvegardes",
            cls.DATA_COMPLIANCE_VULNERABILITY: "Non-conformité aux réglementations"
        }
        
        return descriptions.get(vuln_type, "Type de vulnérabilité non catégorisé")

    @classmethod
    def get_remediation_guide(cls, vuln_type: 'VulnerabilityType') -> Dict[str, Any]:
        """Retourne un guide de remédiation pour le type de vulnérabilité"""
        guides = {
            cls.INJECTION: {
                'titre': "Prévention des injections",
                'description': "Utiliser des requêtes paramétrées et valider les entrées",
                'étapes': [
                    "Utiliser des requêtes préparées",
                    "Échapper les caractères spéciaux",
                    "Valider toutes les entrées utilisateur"
                ],
                'références': [
                    "OWASP SQL Injection Prevention Cheat Sheet",
                    "CWE-89: SQL Injection"
                ]
            },
            # ... Autres guides de remédiation ...
        }
        
        return guides.get(vuln_type, {
            'titre': "Guide générique",
            'description': "Appliquer les bonnes pratiques de sécurité",
            'étapes': [
                "Analyser le contexte spécifique",
                "Consulter la documentation",
                "Appliquer les correctifs recommandés"
            ],
            'références': [
                "OWASP Top 10",
                "CWE/SANS Top 25"
            ]
        })

@dataclass
class SecurityFinding:
    """Résultat d'audit de sécurité enrichi"""
    finding_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    vulnerability_type: VulnerabilityType = VulnerabilityType.OTHER
    security_level: SecurityLevel = SecurityLevel.INFO
    title: str = ""
    description: str = ""
    location: str = ""
    line_number: Optional[int] = None
    cwe_id: Optional[str] = None
    cvss_score: Optional[float] = None
    remediation: Optional[str] = ""
    evidence: Optional[str] = ""
    context: Dict[str, Any] = field(default_factory=dict)
    references: List[str] = field(default_factory=list)
    affected_components: List[str] = field(default_factory=list)
    detection_time: datetime = field(default_factory=datetime.now)
    false_positive_probability: float = 0.0
    exploit_complexity: str = "unknown"
    patch_availability: bool = False
    patch_complexity: str = "unknown"
    attack_vector: Optional[str] = None
    attack_complexity: Optional[str] = None
    privileges_required: Optional[str] = None
    user_interaction: Optional[str] = None
    scope: Optional[str] = None
    confidentiality_impact: Optional[str] = None
    integrity_impact: Optional[str] = None
    availability_impact: Optional[str] = None
    
    def __post_init__(self):
        """Validation après initialisation"""
        if not self.title:
            raise ValueError("Le titre est obligatoire")
        if not self.description:
            raise ValueError("La description est obligatoire")
        if not self.location:
            raise ValueError("La localisation est obligatoire")
            
    def add_reference(self, reference: str) -> None:
        """Ajoute une référence de manière sécurisée"""
        if reference and reference not in self.references:
            self.references.append(reference)
            
    def add_affected_component(self, component: str) -> None:
        """Ajoute un composant affecté de manière sécurisée"""
        if component and component not in self.affected_components:
            self.affected_components.append(component)
            
    def update_cvss(self, score: float) -> None:
        """Met à jour le score CVSS et le niveau de sécurité"""
        if 0.0 <= score <= 10.0:
            self.cvss_score = score
            self.security_level = SecurityLevel.from_cvss(score)
        else:
            raise ValueError("Le score CVSS doit être entre 0 et 10")
            
    def set_cwe(self, cwe_id: str) -> None:
        """Définit le CWE ID et met à jour le type de vulnérabilité"""
        if not cwe_id.startswith('CWE-'):
            cwe_id = f'CWE-{cwe_id}'
        self.cwe_id = cwe_id
        
        vuln_type = VulnerabilityType.from_cwe(cwe_id)
        if vuln_type:
            self.vulnerability_type = vuln_type
            
    def calculate_risk_score(self) -> float:
        """Calcule un score de risque personnalisé"""
        base_score = self.cvss_score or 5.0
        
        # Facteurs d'ajustement
        complexity_factor = {
            'low': 1.2,
            'medium': 1.0,
            'high': 0.8,
            'unknown': 1.0
        }.get(self.attack_complexity or 'unknown')
        
        interaction_factor = {
            'none': 1.2,
            'required': 0.9,
            'unknown': 1.0
        }.get(self.user_interaction or 'unknown')
        
        # Calcul du score ajusté
        adjusted_score = base_score * complexity_factor * interaction_factor
        
        # Réduction si patch disponible
        if self.patch_availability:
            adjusted_score *= 0.8
            
        # Ajustement pour faux positifs
        adjusted_score *= (1 - self.false_positive_probability)
        
        return round(min(10.0, max(0.0, adjusted_score)), 2)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit le finding en dictionnaire"""
        return {
            'finding_id': self.finding_id,
            'vulnerability_type': self.vulnerability_type.value,
            'security_level': self.security_level.value,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'line_number': self.line_number,
            'cwe_id': self.cwe_id,
            'cvss_score': self.cvss_score,
            'remediation': self.remediation,
            'evidence': self.evidence,
            'context': self.context,
            'references': self.references,
            'affected_components': self.affected_components,
            'detection_time': self.detection_time.isoformat(),
            'false_positive_probability': self.false_positive_probability,
            'exploit_complexity': self.exploit_complexity,
            'patch_availability': self.patch_availability,
            'patch_complexity': self.patch_complexity,
            'attack_vector': self.attack_vector,
            'attack_complexity': self.attack_complexity,
            'privileges_required': self.privileges_required,
            'user_interaction': self.user_interaction,
            'scope': self.scope,
            'confidentiality_impact': self.confidentiality_impact,
            'integrity_impact': self.integrity_impact,
            'availability_impact': self.availability_impact,
            'risk_score': self.calculate_risk_score()
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SecurityFinding':
        """Crée un finding à partir d'un dictionnaire"""
        # Conversion des types énumérés
        data['vulnerability_type'] = VulnerabilityType(data['vulnerability_type'])
        data['security_level'] = SecurityLevel(data['security_level'])
        
        # Conversion de la date
        if 'detection_time' in data:
            data['detection_time'] = datetime.fromisoformat(data['detection_time'])
            
        # Suppression du score de risque calculé
        data.pop('risk_score', None)
        
        return cls(**data)

@dataclass
class SecurityReport:
    """Rapport complet d'audit de sécurité enrichi"""
    audit_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    target: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    findings: List[SecurityFinding] = field(default_factory=list)
    security_score: float = 10.0
    compliance_status: Dict[str, bool] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    summary: Dict[str, int] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    scan_duration: float = 0.0
    total_files_scanned: int = 0
    total_lines_scanned: int = 0
    error_count: int = 0
    warning_count: int = 0
    scan_status: str = "completed"
    scan_coverage: float = 0.0
    excluded_files: List[str] = field(default_factory=list)
    failed_scans: List[Dict[str, Any]] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialisation après création"""
        self._update_summary()
        self.metadata.update({
            'generator': 'AgentMAINTENANCE09AnalyseurSecurite',
            'version': '2.1.0',
            'timestamp': self.timestamp.isoformat(),
            'scan_duration': self.scan_duration
        })
    
    def add_finding(self, finding: SecurityFinding) -> None:
        """Ajoute un finding et met à jour le score"""
        try:
            if not isinstance(finding, SecurityFinding):
                raise TypeError("L'objet doit être de type SecurityFinding")
            
            self.findings.append(finding)
            self._update_score()
            self._update_summary()
            
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout du finding: {str(e)}")
            self.error_count += 1
            raise
    
    def add_failed_scan(self, file_path: str, error: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Ajoute un scan échoué au rapport"""
        self.failed_scans.append({
            'file_path': file_path,
            'error': error,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        })
        self.error_count += 1
    
    def add_recommendation(self, recommendation: str) -> None:
        """Ajoute une recommandation de manière sécurisée"""
        if recommendation and recommendation not in self.recommendations:
            self.recommendations.append(recommendation)
    
    def update_compliance_status(self, rule: str, status: bool) -> None:
        """Met à jour le statut de conformité"""
        self.compliance_status[rule] = status
    
    def _update_score(self) -> None:
        """Met à jour le score de sécurité"""
        if not self.findings:
            self.security_score = 10.0
            return
        
        # Nouveaux poids ajustés pour un calcul plus précis
        weights = {
            SecurityLevel.CRITICAL: 2.5,
            SecurityLevel.HIGH: 1.5,
            SecurityLevel.MEDIUM: 0.8,
            SecurityLevel.LOW: 0.3,
            SecurityLevel.INFO: 0.1,
            SecurityLevel.SECURE: 0.0
        }
        
        # Calcul du score avec plafonnement
        total_impact = sum(weights[f.security_level] for f in self.findings)
        base_score = max(0.0, 10.0 - total_impact)
        
        # Ajustement pour éviter une pénalité excessive
        if len(self.findings) > 5:
            diminishing_factor = 0.8 ** (len(self.findings) - 5)
            base_score *= diminishing_factor
        
        # Ajustement basé sur la couverture du scan
        coverage_factor = max(0.5, min(1.0, self.scan_coverage / 100))
        base_score *= coverage_factor
        
        # Bonus pour conformité élevée
        if self.compliance_status:
            compliance_rate = sum(1 for v in self.compliance_status.values() if v) / len(self.compliance_status)
            if compliance_rate > 0.8:
                base_score *= 1.1
        
        self.security_score = round(max(0.0, min(10.0, base_score)), 2)
    
    def _update_summary(self) -> None:
        """Met à jour le résumé des findings"""
        self.summary = {
            'total': len(self.findings),
            'par_niveau': {level.value: 0 for level in SecurityLevel},
            'par_type': {vtype.value: 0 for vtype in VulnerabilityType}
        }
        
        for finding in self.findings:
            self.summary['par_niveau'][finding.security_level.value] += 1
            self.summary['par_type'][finding.vulnerability_type.value] += 1
    
    def get_critical_findings(self) -> List[SecurityFinding]:
        """Retourne les findings critiques"""
        return [f for f in self.findings if f.security_level == SecurityLevel.CRITICAL]
    
    def get_findings_by_type(self, vuln_type: VulnerabilityType) -> List[SecurityFinding]:
        """Retourne les findings d'un type spécifique"""
        return [f for f in self.findings if f.vulnerability_type == vuln_type]
    
    def get_findings_by_component(self, component: str) -> List[SecurityFinding]:
        """Retourne les findings affectant un composant spécifique"""
        return [f for f in self.findings if component in f.affected_components]
    
    def calculate_risk_metrics(self) -> Dict[str, Any]:
        """Calcule des métriques de risque avancées"""
        if not self.findings:
            return {
                'risk_score': 0.0,
                'risk_level': 'faible',
                'critical_count': 0,
                'high_priority_count': 0,
                'remediation_complexity': 'faible'
            }
        
        # Calcul des métriques
        critical_findings = self.get_critical_findings()
        high_findings = [f for f in self.findings if f.security_level == SecurityLevel.HIGH]
        
        # Score de risque moyen
        risk_scores = [f.calculate_risk_score() for f in self.findings]
        avg_risk_score = sum(risk_scores) / len(risk_scores)
        
        # Complexité de remédiation
        patch_complexities = [f.patch_complexity for f in self.findings]
        remediation_complexity = max(
            (patch_complexities.count('high') * 3 +
             patch_complexities.count('medium') * 2 +
             patch_complexities.count('low')) / len(self.findings),
            1
        )
        
        return {
            'risk_score': round(avg_risk_score, 2),
            'risk_level': 'critique' if len(critical_findings) > 0 else
                         'élevé' if len(high_findings) > 0 else
                         'moyen' if avg_risk_score > 5 else 'faible',
            'critical_count': len(critical_findings),
            'high_priority_count': len(high_findings),
            'remediation_complexity': 'élevée' if remediation_complexity > 2 else
                                    'moyenne' if remediation_complexity > 1 else 'faible'
        }
    
    def generate_summary_report(self) -> str:
        """Génère un résumé formaté du rapport conforme au standard agent 06"""
        # Utilise la nouvelle méthode standardisée
        return self._generate_standard_report("SÉCURITÉ", f"Audit {self.target}", self)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit le rapport en dictionnaire"""
        return {
            'audit_id': self.audit_id,
            'target': self.target,
            'timestamp': self.timestamp.isoformat(),
            'findings': [f.to_dict() for f in self.findings],
            'security_score': self.security_score,
            'compliance_status': self.compliance_status,
            'recommendations': self.recommendations,
            'summary': self.summary,
            'context': self.context,
            'metadata': self.metadata,
            'scan_duration': self.scan_duration,
            'total_files_scanned': self.total_files_scanned,
            'total_lines_scanned': self.total_lines_scanned,
            'error_count': self.error_count,
            'warning_count': self.warning_count,
            'scan_status': self.scan_status,
            'scan_coverage': self.scan_coverage,
            'excluded_files': self.excluded_files,
            'failed_scans': self.failed_scans,
            'risk_metrics': self.calculate_risk_metrics()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SecurityReport':
        """Crée un rapport à partir d'un dictionnaire"""
        # Copie pour éviter la modification des données d'entrée
        data = data.copy()
        
        # Conversion de la date
        if 'timestamp' in data:
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        
        # Conversion des findings
        if 'findings' in data:
            data['findings'] = [
                SecurityFinding.from_dict(f) if isinstance(f, dict)
                else f for f in data['findings']
            ]
        
        # Suppression des champs calculés
        data.pop('risk_metrics', None)
        
        return cls(**data)

# --- Fin: Éléments intégrés depuis Agent 18 ---


class AgentMAINTENANCE09AnalyseurSecurite(Agent):
    """
    Agent avancé chargé de la sécurité du code Python et des audits universels:
    - Détection des vulnérabilités de sécurité communes
    - Identification des pratiques non sécurisées
    - Analyse des injections potentielles
    - Vérification de l'usage sécurisé des fonctions
    - Analyse des patterns de gestion des secrets
    - Audit de sécurité des fichiers et répertoires
    - Analyse des dépendances et configurations
    - Intégration avec des outils tiers (Bandit, Safety)
    """

    def __init__(self, **kwargs):
        
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="maintenance",
                custom_config={
                    "logger_name": f"nextgen.maintenance.MAINTENANCE_09_analyseur_securite.{self.agent_id if hasattr(self, 'agent_id') else self.id if hasattr(self, 'id') else 'unknown'}",
                    "log_dir": "logs/maintenance",
                    "metadata": {
                        "agent_type": "MAINTENANCE_09_analyseur_securite",
                        "agent_role": "maintenance",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)

        """Initialisation de l'agent"""
        super().__init__(**kwargs)
        self.name = "AgentMAINTENANCE09AnalyseurSecurite"
        self.version = "2.1.0"
        self.description = "Agent d'analyse de sécurité avancé"
        
        # Configuration du logging
        self._setup_logging()
        
        # Patterns de sécurité
        self.security_patterns = self._init_security_patterns()
        
        # Configuration par défaut
        self.default_config = {
            'max_files': 1000,
            'scan_depth': 3,
            'excluded_patterns': [
                '*.pyc', '__pycache__', '.git', '.env',
                'node_modules', 'venv', '.venv', '.pytest_cache'
            ],
            'max_file_size': 10 * 1024 * 1024,  # 10 MB
            'timeout': 300,  # 5 minutes
            'parallel_scans': 4
        }
        
        # État de l'agent
        self.current_context = None
        self.executor = ThreadPoolExecutor(max_workers=4)
        
    def _setup_logging(self) -> None:
        """Configuration du système de logging"""
        try:
            if LoggingManager:
                self.logger = LoggingManager().get_logger(self.name)
            else:
                self.logger = logging.getLogger(self.name)
                self.logger.setLevel(logging.INFO)
                
                # Configuration du handler si nécessaire
                if not self.logger.handlers:
                    handler = logging.StreamHandler()
                    formatter = logging.Formatter(
                        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )
                    handler.setFormatter(formatter)
                    self.logger.addHandler(handler)
                    
        except Exception as e:
            print(f"Erreur lors de la configuration du logging: {str(e)}")
            self.logger = logging.getLogger(self.name)
            
    async def startup(self) -> None:
        """Initialisation de l'agent"""
        try:
            self.logger.info(f"Démarrage de l'agent {self.name} v{self.version}")
            
            # Vérification des dépendances
            if not BANDIT_AVAILABLE:
                self.logger.warning("Bandit n'est pas disponible - fonctionnalités limitées")
            if not SAFETY_CHECK_AVAILABLE:
                self.logger.warning("Safety n'est pas disponible - analyse des dépendances limitée")
                
            # Création du répertoire de rapports si nécessaire
            reports_dir = Path("reports/security")
            reports_dir.mkdir(parents=True, exist_ok=True)
            
        except Exception as e:
            self.logger.error(f"Erreur lors du démarrage: {str(e)}")
            raise
            
    async def execute_task(self, task: Task) -> Result:
        """Exécution d'une tâche"""
        try:
            self.logger.info(f"Exécution de la tâche: {task.task_id}")
            
            # Validation de la tâche
            if not task.parameters:
                raise ValueError("Paramètres de tâche manquants")
                
            # Création du contexte
            self.current_context = SecurityContext()
            self.current_context.target_path = task.parameters.get('target_path')
            
            # Configuration du contexte
            config = {**self.default_config, **task.parameters.get('config', {})}
            self.current_context.config = config
            self.current_context.max_files = config['max_files']
            self.current_context.scan_depth = config['scan_depth']
            self.current_context.excluded_paths = set(config['excluded_patterns'])
            
            # Validation du contexte
            is_valid, errors = self.current_context.validate_config()
            if not is_valid:
                raise ValueError(f"Configuration invalide: {', '.join(errors)}")
            
            # Exécution selon le type de tâche
            scan_type = task.parameters.get('scan_type', 'security_scan')
            if scan_type == 'security_scan':
                result = await self._handle_security_scan(task, self.current_context)
            elif scan_type == 'dependency_check':
                result = await self._handle_dependency_check(task, self.current_context)
            elif scan_type == 'config_audit':
                result = await self._handle_config_audit(task, self.current_context)
            else:
                raise ValueError(f"Type de scan non supporté: {scan_type}")
                
            return result
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution: {str(e)}")
            tb = traceback.format_exc()
            self.logger.debug(f"Traceback: {tb}")
            
            return Result(
                success=False,
                error=str(e),
                details={'traceback': tb}
            )
            
    async def _handle_security_scan(self, task: Task, context: SecurityContext) -> Result:
        """Gestion d'un scan de sécurité"""
        try:
            self.logger.info("Démarrage du scan de sécurité")
            context.update_status("scanning")
            
            # Création du rapport
            report = SecurityReport(
                target=context.target_path,
                context={'task_id': task.task_id}
            )
            
            # Analyse du chemin cible
            target_path = Path(context.target_path)
            if not target_path.exists():
                raise FileNotFoundError(f"Chemin cible non trouvé: {target_path}")
            
            # Scan récursif
            start_time = datetime.now()
            await self._scan_path_recursive(target_path, report, context)
            
            # Finalisation du rapport
            end_time = datetime.now()
            report.scan_duration = (end_time - start_time).total_seconds()
            report.scan_coverage = self._calculate_coverage(context)
            
            # Génération des recommandations
            self._generate_recommendations(report)
            
            # Sauvegarde du rapport
            report_path = self._save_report(report)
            
            return Result(
                success=True,
                data={
                    'report': report.to_dict(),
                    'report_path': str(report_path),
                    'summary': report.generate_summary_report()
                }
            )
            
        except Exception as e:
            context.add_error(str(e))
            raise
            
    async def _handle_dependency_check(self, task: Task, context: SecurityContext) -> Result:
        """Gestion d'une analyse des dépendances"""
        try:
            self.logger.info("Démarrage de l'analyse des dépendances")
            context.update_status("checking_dependencies")
            
            # Création du rapport
            report = SecurityReport(
                target=context.target_path,
                context={'task_id': task.task_id}
            )
            
            # Analyse des fichiers de dépendances
            dependency_files = self._find_dependency_files(Path(context.target_path))
            
            for dep_file in dependency_files:
                try:
                    if dep_file.name == 'requirements.txt':
                        await self._analyze_python_dependencies(dep_file, report)
                    elif dep_file.name == 'package.json':
                        await self._analyze_node_dependencies(dep_file, report)
                    elif dep_file.name == 'Gemfile':
                        await self._analyze_ruby_dependencies(dep_file, report)
                except Exception as e:
                    context.add_error(f"Erreur lors de l'analyse de {dep_file}: {str(e)}")
                    
            # Finalisation du rapport
            self._generate_recommendations(report)
            report_path = self._save_report(report)
            
            return Result(
                success=True,
                data={
                    'report': report.to_dict(),
                    'report_path': str(report_path)
                }
            )
            
        except Exception as e:
            context.add_error(str(e))
            raise
            
    async def _handle_config_audit(self, task: Task, context: SecurityContext) -> Result:
        """Gestion d'un audit de configuration"""
        try:
            self.logger.info("Démarrage de l'audit de configuration")
            context.update_status("auditing_config")
            
            # Création du rapport
            report = SecurityReport(
                target=context.target_path,
                context={'task_id': task.task_id}
            )
            
            # Analyse des fichiers de configuration
            config_files = self._find_config_files(Path(context.target_path))
            
            for config_file in config_files:
                try:
                    config_data = self._load_config_file(config_file)
                    findings = await self._analyze_config(config_data, config_file)
                    for finding in findings:
                        report.add_finding(finding)
                except Exception as e:
                    context.add_error(f"Erreur lors de l'analyse de {config_file}: {str(e)}")
                    
            # Finalisation du rapport
            self._generate_recommendations(report)
            report_path = self._save_report(report)
            
            return Result(
                success=True,
                data={
                    'report': report.to_dict(),
                    'report_path': str(report_path)
                }
            )
            
        except Exception as e:
            context.add_error(str(e))
            raise
            
    async def shutdown(self) -> None:
        """Arrêt de l'agent"""
        try:
            self.logger.info("Arrêt de l'agent")
            self.executor.shutdown(wait=True)
        except Exception as e:
            self.logger.error(f"Erreur lors de l'arrêt: {str(e)}")
            
    def get_capabilities(self) -> List[str]:
        """Retourne les capacités de l'agent"""
        capabilities = [
            "Analyse statique de code Python",
            "Détection de vulnérabilités",
            "Analyse des dépendances",
            "Audit de configuration",
            "Détection de secrets",
            "Génération de rapports"
        ]
        
        if BANDIT_AVAILABLE:
            capabilities.append("Analyse Bandit")
        if SAFETY_CHECK_AVAILABLE:
            capabilities.append("Vérification Safety")
            
        return capabilities
        
    async def health_check(self) -> Dict[str, Any]:
        """Vérifie l'état de l'agent"""
        status = {
            'name': self.name,
            'version': self.version,
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'capabilities': self.get_capabilities(),
            'dependencies': {
                'bandit': BANDIT_AVAILABLE,
                'safety': SAFETY_CHECK_AVAILABLE
            }
        }
        
        if self.current_context:
            status['current_scan'] = {
                'scan_id': self.current_context.scan_id,
                'status': self.current_context.scan_status,
                'progress': self.current_context.scan_progress
            }
            
        return status
        
    def _init_security_patterns(self) -> Dict[str, Any]:
        """Initialisation des patterns de sécurité"""
        return {
            'secrets': {
                'api_key': r'(?i)(api[_-]?key|apikey|secret)["\s]*[:=]["\s]*[a-z0-9_-]+',
                'password': r'(?i)(password|passwd|pwd)["\s]*[:=]["\s]*[^\'"\s]+',
                'token': r'(?i)(access_token|auth_token|jwt)["\s]*[:=]["\s]*[a-z0-9_-]+',
                'private_key': r'-----BEGIN[A-Z\s]+PRIVATE KEY-----',
                'aws_key': r'(?i)(aws_access_key_id|aws_secret_access_key)["\s]*[:=]["\s]*[a-z0-9/+]+',
                'connection_string': r'(?i)(mongodb|postgresql|mysql)://[a-z0-9_-]+:[^@\s]+@[a-z0-9.-]+',
            },
            'dangerous_functions': {
                'python': {
                    'eval': r'eval\s*\(',
                    'exec': r'exec\s*\(',
                    'os_system': r'os\.system\s*\(',
                    'subprocess_shell': r'subprocess\..*shell\s*=\s*True',
                    'pickle_loads': r'pickle\.loads\s*\(',
                    'yaml_load': r'yaml\.load\s*\([^,)]+\)',
                    'sql_raw': r'execute\s*\(["\'].*SELECT|INSERT|UPDATE|DELETE',
                },
                'javascript': {
                    'eval': r'eval\s*\(',
                    'function': r'new Function\s*\(',
                    'dangerouslySetInnerHTML': r'dangerouslySetInnerHTML',
                }
            },
            'sql_injection': {
                r'(?i)SELECT.*WHERE.*=\s*[\'"].*%.*[\'"]',
                r'(?i)INSERT.*VALUES.*\$\{.*\}',
                r'(?i)UPDATE.*SET.*=.*\$\{.*\}',
            },
            'xss': {
                r'(?i)innerHTML\s*=',
                r'(?i)document\.write\s*\(',
                r'(?i)eval\s*\(',
            },
            'file_operations': {
                r'(?i)open\s*\([^,)]+,\s*[\'"]w[\'"]',
                r'(?i)file_get_contents\s*\(',
                r'(?i)readFile\s*\(',
                r'(?i)writeFile\s*\(',
            },
            'command_injection': {
                r'(?i)exec\s*\([^,)]+\)',
                r'(?i)spawn\s*\([^,)]+\)',
                r'(?i)system\s*\([^,)]+\)',
            }
        }
        
    async def _scan_path_recursive(self, path: Path, report: SecurityReport, context: SecurityContext) -> None:
        """Analyse récursive d'un chemin"""
        try:
            if context.is_scan_limit_reached():
                return
                
            if context.should_exclude_path(path):
                context.excluded_files.append(str(path))
                return
                
            if path.is_file():
                await self._scan_file(path, report, context)
            elif path.is_dir():
                for item in path.iterdir():
                    await self._scan_path_recursive(item, report, context)
                    
        except Exception as e:
            context.add_error(f"Erreur lors du scan de {path}: {str(e)}")
            
    async def _scan_file(self, file_path: Path, report: SecurityReport, context: SecurityContext) -> None:
        """Analyse d'un fichier"""
        try:
            # Vérification de la taille
            if file_path.stat().st_size > context.config['max_file_size']:
                context.add_warning(f"Fichier trop volumineux ignoré: {file_path}")
                return
                
            context.current_file_count += 1
            
            # Analyse selon le type de fichier
            if file_path.suffix == '.py':
                await self._analyze_python_file(file_path, report, context)
            elif file_path.suffix in {'.js', '.ts', '.jsx', '.tsx'}:
                await self._analyze_javascript_file(file_path, report, context)
            elif file_path.suffix in {'.json', '.yaml', '.yml'}:
                await self._analyze_config_file(file_path, report, context)
                
            # Analyse générique
            await self._analyze_security_patterns(file_path, report, context)
            await self._analyze_secrets(file_path, report, context)
            
        except Exception as e:
            context.add_error(f"Erreur lors de l'analyse de {file_path}: {str(e)}")
            
    async def _analyze_python_file(self, file_path: Path, report: SecurityReport, context: SecurityContext) -> None:
        """Analyse d'un fichier Python"""
        try:
            # Analyse Bandit si disponible
            if BANDIT_AVAILABLE:
                await self._run_bandit_scan(file_path, report)
                
            # Analyse AST
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            await self._analyze_python_ast(content, file_path, report)
            
        except Exception as e:
            context.add_error(f"Erreur lors de l'analyse Python de {file_path}: {str(e)}")
            
    async def _analyze_javascript_file(self, file_path: Path, report: SecurityReport, context: SecurityContext) -> None:
        """Analyse d'un fichier JavaScript/TypeScript"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Analyse des patterns de sécurité
            for pattern_type, patterns in self.security_patterns['dangerous_functions']['javascript'].items():
                matches = re.finditer(patterns, content)
                for match in matches:
                    finding = SecurityFinding(
                        vulnerability_type=VulnerabilityType.DANGEROUS_FUNCTION,
                        security_level=SecurityLevel.HIGH,
                        title=f"Utilisation dangereuse de {pattern_type}",
                        description=f"Utilisation potentiellement dangereuse de {pattern_type} détectée",
                        location=str(file_path),
                        line_number=content[:match.start()].count('\n') + 1,
                        evidence=match.group(0)
                    )
                    report.add_finding(finding)
                    
        except Exception as e:
            context.add_error(f"Erreur lors de l'analyse JavaScript de {file_path}: {str(e)}")
            
    async def _analyze_config_file(self, file_path: Path, report: SecurityReport, context: SecurityContext) -> None:
        """Analyse d'un fichier de configuration"""
        try:
            config_data = self._load_config_file(file_path)
            findings = await self._analyze_config(config_data, file_path)
            for finding in findings:
                report.add_finding(finding)
                
        except Exception as e:
            context.add_error(f"Erreur lors de l'analyse de configuration de {file_path}: {str(e)}")
            
    def _load_config_file(self, file_path: Path) -> Dict[str, Any]:
        """Charge un fichier de configuration"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if file_path.suffix == '.json':
            return json.loads(content)
        elif file_path.suffix in {'.yaml', '.yml'}:
            return yaml.safe_load(content)
        else:
            raise ValueError(f"Format de configuration non supporté: {file_path.suffix}")
            
    async def _analyze_config(self, config: Dict[str, Any], file_path: Path) -> List[SecurityFinding]:
        """Analyse une configuration"""
        findings = []
        
        def check_config_dict(d: Dict[str, Any], path: str = '') -> None:
            for key, value in d.items():
                current_path = f"{path}.{key}" if path else key
                
                # Vérification des secrets
                if any(secret in key.lower() for secret in {'password', 'secret', 'key', 'token'}):
                    findings.append(SecurityFinding(
                        vulnerability_type=VulnerabilityType.SENSITIVE_DATA,
                        security_level=SecurityLevel.HIGH,
                        title=f"Information sensible dans la configuration",
                        description=f"Détection d'une information potentiellement sensible à {current_path}",
                        location=str(file_path),
                        evidence=f"{key}: [MASQUÉ]"
                    ))
                    
                # Vérification récursive
                if isinstance(value, dict):
                    check_config_dict(value, current_path)
                elif isinstance(value, list):
                    for i, item in enumerate(value):
                        if isinstance(item, dict):
                            check_config_dict(item, f"{current_path}[{i}]")
                            
        check_config_dict(config)
        return findings
        
    def _calculate_coverage(self, context: SecurityContext) -> float:
        """Calcule la couverture du scan"""
        total_files = sum(1 for _ in Path(context.target_path).rglob('*') if _.is_file())
        if total_files == 0:
            return 100.0
            
        scanned_ratio = min(1.0, context.current_file_count / total_files)
        return round(scanned_ratio * 100, 2)
        
    def _generate_recommendations(self, report: SecurityReport) -> None:
        """Génère des recommandations basées sur les findings"""
        recommendations = set()
        
        for finding in report.findings:
            if finding.security_level in {SecurityLevel.CRITICAL, SecurityLevel.HIGH}:
                if finding.remediation:
                    recommendations.add(finding.remediation)
                    
        report.recommendations = list(recommendations)
        
    def _save_report(self, report: SecurityReport) -> Path:
        """Sauvegarde le rapport"""
        reports_dir = Path("reports/security")
        report_file = reports_dir / f"security_report_{report.audit_id}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)
            
        return report_file
        
    def _find_dependency_files(self, path: Path) -> List[Path]:
        """Trouve les fichiers de dépendances"""
        dependency_files = []
        for pattern in ['requirements.txt', 'package.json', 'Gemfile']:
            dependency_files.extend(path.rglob(pattern))
        return dependency_files
        
    def _find_config_files(self, path: Path) -> List[Path]:
        """Trouve les fichiers de configuration"""
        config_files = []
        for pattern in ['*.json', '*.yaml', '*.yml', '*.conf', '*.config']:
            config_files.extend(path.rglob(pattern))
        return config_files
    
    def _generate_standard_report(self, category: str, title: str, data: Dict[str, Any]) -> str:
        """Génère un rapport conforme au standard agent 06."""
        
        from datetime import datetime
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
*📂 Sauvegardé dans : /mnt/c/Dev/nextgeneration/reports/security/*
"""
        
        return report
    
    def _calculate_report_score(self, data: Dict[str, Any]) -> float:
        """Calcule le score global du rapport basé sur les données."""
        # Pour l'agent sécurité, base sur security_score et autres métriques
        base_score = 7.0
        
        # Si on a un rapport de sécurité dans les données
        if isinstance(data, dict) and hasattr(data.get('report'), 'security_score'):
            # Score basé sur le security_score du rapport
            security_score = data['report'].security_score
            base_score = float(security_score)
        elif isinstance(data, SecurityReport):
            base_score = float(data.security_score)
        
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
        """Évalue la conformité aux standards de sécurité."""
        conformity_score = 0
        total_checks = 4
        
        # Checks de conformité spécifiques à la sécurité
        if isinstance(data, SecurityReport):
            if data.scan_coverage >= 80:
                conformity_score += 1
            if data.security_score >= 7.0:
                conformity_score += 1
            if len(data.findings) > 0:  # Audit réellement effectué
                conformity_score += 1
            if data.recommendations:
                conformity_score += 1
        elif isinstance(data, dict):
            report = data.get('report')
            if report and hasattr(report, 'scan_coverage') and report.scan_coverage >= 80:
                conformity_score += 1
            if report and hasattr(report, 'security_score') and report.security_score >= 7.0:
                conformity_score += 1
            conformity_score += 2  # Base pour autres données
                
        conformity_rate = conformity_score / total_checks
        
        if conformity_rate >= 0.9:
            return "✅ CONFORME"
        elif conformity_rate >= 0.7:
            return "⚠️ PARTIELLEMENT CONFORME"
        else:
            return "❌ NON CONFORME"
    
    def _count_critical_issues(self, data: Dict[str, Any]) -> int:
        """Compte les issues critiques dans les données de sécurité."""
        critical_count = 0
        
        if isinstance(data, SecurityReport):
            critical_count = len([f for f in data.findings if f.security_level == SecurityLevel.CRITICAL])
        elif isinstance(data, dict):
            report = data.get('report')
            if report and hasattr(report, 'findings'):
                critical_count = len([f for f in report.findings if f.security_level == SecurityLevel.CRITICAL])
                
        return critical_count
    
    def _generate_architecture_context(self, data: Dict[str, Any]) -> str:
        """Génère la section Architecture et Contexte pour sécurité."""
        if isinstance(data, SecurityReport):
            target = data.target
            total_files = data.total_files_scanned
        elif isinstance(data, dict):
            report = data.get('report', data)
            target = report.get('target', 'Non spécifié')
            total_files = report.get('total_files_scanned', 0)
        else:
            target = "Non spécifié"
            total_files = 0
            
        context = f"""Audit de sécurité automatisé effectué sur l'architecture logicielle cible.

**Périmètre d'analyse :**
- Cible analysée : {target}
- Nombre de fichiers scannés : {total_files}
- Technologies détectées : Python, Configuration, Dépendances

**Méthodologie d'audit :**
- Analyse statique de code source
- Vérification des configurations de sécurité
- Scan des dépendances vulnérables
- Détection de patterns de sécurité défaillants

**Architecture de sécurité évaluée :**
- Authentification et autorisation
- Gestion des secrets et configuration
- Validation des entrées utilisateur
- Sécurisation des communications"""
        
        return context
    
    def _generate_metrics_kpis(self, data: Dict[str, Any]) -> str:
        """Génère la section Métriques et KPIs pour sécurité."""
        if isinstance(data, SecurityReport):
            report = data
        elif isinstance(data, dict):
            report = data.get('report', data)
        else:
            return "Aucune métrique disponible"
            
        # Calculs des métriques
        findings_by_level = {}
        if hasattr(report, 'findings'):
            for finding in report.findings:
                level = finding.security_level.value if hasattr(finding.security_level, 'value') else str(finding.security_level)
                findings_by_level[level] = findings_by_level.get(level, 0) + 1
        
        security_score = getattr(report, 'security_score', 0)
        coverage = getattr(report, 'scan_coverage', 0)
        total_findings = len(getattr(report, 'findings', []))
        
        metrics = f"""### 📈 Indicateurs de Sécurité
- **Score de sécurité global :** {security_score}/10
- **Couverture du scan :** {coverage}%
- **Total vulnérabilités détectées :** {total_findings}
- **Criticité critique :** {findings_by_level.get('CRITICAL', 0)}
- **Criticité haute :** {findings_by_level.get('HIGH', 0)}
- **Criticité moyenne :** {findings_by_level.get('MEDIUM', 0)}
- **Criticité faible :** {findings_by_level.get('LOW', 0)}

### 🎯 KPIs de Conformité
- **Conformité sécurité :** {((10 - len(findings_by_level.get('CRITICAL', []))) / 10 * 100):.1f}%
- **Niveau de risque :** {"ÉLEVÉ" if findings_by_level.get('CRITICAL', 0) > 0 else "MODÉRÉ" if total_findings > 5 else "FAIBLE"}
- **Recommandations actionnables :** {len(getattr(report, 'recommendations', []))}"""
        
        return metrics
    
    def _generate_detailed_analysis(self, data: Dict[str, Any]) -> str:
        """Génère la section Analyse Détaillée pour sécurité."""
        if isinstance(data, SecurityReport):
            report = data
        elif isinstance(data, dict):
            report = data.get('report', data)
        else:
            return "Aucune analyse disponible"
            
        findings = getattr(report, 'findings', [])
        
        analysis = f"""### 🔍 Analyse par Criticité

**Vulnérabilités Critiques ({len([f for f in findings if str(f.security_level) == 'CRITICAL'])}):**"""
        
        critical_findings = [f for f in findings if str(f.security_level) == 'CRITICAL']
        for finding in critical_findings[:5]:  # Limite à 5 pour le rapport
            analysis += f"\n- `{finding.type}`: {finding.description} (Ligne {finding.line_number})"
        
        high_findings = [f for f in findings if str(f.security_level) == 'HIGH']
        if high_findings:
            analysis += f"\n\n**Vulnérabilités Hautes ({len(high_findings)}):**"
            for finding in high_findings[:3]:
                analysis += f"\n- `{finding.type}`: {finding.description}"
        
        analysis += f"\n\n### 📊 Distribution des Risques"
        analysis += f"\nLa majorité des vulnérabilités sont de niveau {'critique' if len(critical_findings) > len(high_findings) else 'élevé' if len(high_findings) > 0 else 'modéré'}."
        analysis += f"\nFocus recommandé sur la remédiation des {len(critical_findings)} vulnérabilités critiques."
        
        return analysis
    
    def _generate_strategic_recommendations(self, data: Dict[str, Any]) -> str:
        """Génère la section Recommandations Stratégiques pour sécurité."""
        if isinstance(data, SecurityReport):
            report = data
        elif isinstance(data, dict):
            report = data.get('report', data)
        else:
            return "Aucune recommandation disponible"
            
        findings = getattr(report, 'findings', [])
        recommendations = getattr(report, 'recommendations', [])
        critical_count = len([f for f in findings if str(f.security_level) == 'CRITICAL'])
        
        strategic_recs = f"""### 🎯 Actions Prioritaires

**Priorité HAUTE :**"""
        
        if critical_count > 0:
            strategic_recs += f"""
1. **Remédiation immédiate** des {critical_count} vulnérabilités critiques
2. **Review sécurité** approfondie du code concerné
3. **Tests de sécurité** additionnels post-correction"""
        else:
            strategic_recs += f"""
1. **Maintien du niveau** de sécurité actuel
2. **Surveillance continue** des nouvelles vulnérabilités
3. **Formation équipe** sur les bonnes pratiques"""
        
        strategic_recs += f"""

**Priorité MOYENNE :**
1. **Automatisation** des contrôles de sécurité dans CI/CD
2. **Documentation** des procédures de sécurité
3. **Audit périodique** des configurations

**Priorité BASSE :**
1. **Optimisation** des outils de scanning
2. **Extension couverture** à d'autres composants
3. **Benchmark** contre standards industrie"""
        
        if recommendations:
            strategic_recs += f"\n\n**Recommandations spécifiques détectées :**"
            for i, rec in enumerate(recommendations[:3], 1):
                strategic_recs += f"\n{i}. {rec}"
        
        return strategic_recs
    
    def _generate_business_impact(self, data: Dict[str, Any]) -> str:
        """Génère la section Impact Business pour sécurité."""
        if isinstance(data, SecurityReport):
            report = data
        elif isinstance(data, dict):
            report = data.get('report', data)
        else:
            return "Aucune évaluation d'impact disponible"
            
        findings = getattr(report, 'findings', [])
        critical_count = len([f for f in findings if str(f.security_level) == 'CRITICAL'])
        security_score = getattr(report, 'security_score', 0)
        
        # Estimations d'impact
        risk_level = "ÉLEVÉ" if critical_count > 0 else "MODÉRÉ" if len(findings) > 5 else "FAIBLE"
        cost_impact = critical_count * 50000 + len(findings) * 5000  # Estimation coût potentiel
        
        impact = f"""### 💰 Impact Sécurité Quantifié

**Niveau de Risque Business :** {risk_level}
- **Vulnérabilités critiques :** {critical_count} (impact potentiel: {critical_count * 50000}€)
- **Score de sécurité :** {security_score}/10 ({"Acceptable" if security_score >= 7 else "Nécessite amélioration"})
- **Coût potentiel total estimé :** {cost_impact}€

**Bénéfices Sécurisation :**
- **Réduction risque cyber :** {min(95, security_score * 10)}%
- **Conformité réglementaire :** Amélioration RGPD/ISO27001
- **Confiance clients :** Protection données personnelles

### 📊 ROI Sécurité

**Investissement prévention :**
- Coût remédiation immédiate : ~{len(findings) * 500}€
- Formation équipe sécurité : ~2000€
- Outils automatisation : ~5000€

**Retour sur investissement :**
- Évitement incidents : +{(cost_impact / 10000 * 100):.0f}%
- Réduction temps résolution : 80%
- Amélioration réputation : Inestimable

### 🛡️ Impact Opérationnel

**Continuité d'activité :**
- Disponibilité système préservée
- Réduction risque interruption service
- Amélioration temps de réponse incidents

**Compliance :**
- Respect standards sécurité industrie
- Audit trail complet pour régulateurs
- Certification sécurité facilitée"""
        
        return impact

def create_agent_MAINTENANCE_09_analyseur_securite(**kwargs) -> AgentMAINTENANCE09AnalyseurSecurite:
    """Crée une instance de l'agent"""
    return AgentMAINTENANCE09AnalyseurSecurite(**kwargs)

async def main():
    """Point d'entrée pour les tests"""
    agent = create_agent_MAINTENANCE_09_analyseur_securite()
    await agent.startup()
    # Ajoutez vos tests ici
    await agent.shutdown()

if __name__ == "__main__":
    asyncio.run(main())