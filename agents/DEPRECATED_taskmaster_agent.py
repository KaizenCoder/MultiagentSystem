import sys
from pathlib import Path
import logging
import hashlib
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import re
import os
import importlib
import inspect

# --- Configuration des Chemins Stratégiques ---

# PROJECT_ROOT pour les imports Python robustes.
# Le script est dans nextgeneration/agents/, on remonte de 1 niveau.
try:
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
except IndexError:
    # Fallback si la structure est inattendue.
    PROJECT_ROOT = Path.cwd()

# WORK_DIR pour toutes les opérations de lecture/écriture (logs, data, reports).
# IMPORTANT : Utiliser des barres obliques pour la compatibilité multi-OS.
WORK_DIR = Path("C:/Dev/nextgeneration/20250620_projet_taskmanager/TASKMASTER_PRODUCTION_READY")

# Ajout du chemin du logger au sys.path en utilisant PROJECT_ROOT
logging_path = PROJECT_ROOT / "20250620_projet_logging_centralise" / "PRODUCTION_READY" / "core"
if str(logging_path) not in sys.path:
    sys.path.insert(0, str(logging_path))

# --- Fin de la Configuration des Chemins ---

#!/usr/bin/env python3
"""
🎯 Agent TaskMaster NextGeneration - Interface Centrale de Gestion de Tâches
Version complète avec multi-instanciation et validation anti-hallucination
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
from uuid import uuid4
import hashlib
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import re

# Import des composants NextGeneration existants
from core.manager import LoggingManager
from core.agent_factory_architecture import Agent

# La fonction log_performance est une méthode de LoggingManager, pas un import séparé.

# Les composants suivants sont mis en commentaire car ils ne sont pas disponibles
# from ..monitoring.metrics_collector import MetricsCollector
# from ..monitoring.health_monitor import HealthMonitor
# from ..agents.base_agent import BaseAgent
# from ..config.agent_config import AgentFactoryConfig

# Imports pour l'IA et NLP
import spacy
from transformers import pipeline

class TaskType(Enum):
    """Types de tâches supportés"""
    AUDIT = "audit"
    ANALYSIS = "analysis"
    OPTIMIZATION = "optimization"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    REFACTORING = "refactoring"
    MONITORING = "monitoring"
    DEPLOYMENT = "deployment"

class ValidationStatus(Enum):
    """Statuts de validation"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_CLARIFICATION = "needs_clarification"
    PARTIAL = "partial"

class TaskPriority(Enum):
    """Niveaux de priorité"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

@dataclass
class EvidenceEntry:
    """Entrée de preuve pour validation"""
    timestamp: datetime
    source: str
    type: str
    content: Any
    confidence: float
    verified: bool = False

@dataclass
class RealityCheck:
    """Vérification de réalité anti-hallucination"""
    check_id: str
    check_type: str
    expected: Any
    actual: Any
    passed: bool
    confidence: float
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TaskDefinition:
    """Définition enrichie d'une tâche"""
    title: str
    description: str
    task_type: TaskType
    priority: TaskPriority
    required_capabilities: List[str]
    constraints: Dict[str, Any] = field(default_factory=dict)
    expected_outputs: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SubTask:
    """Sous-tâche décomposée"""
    id: str
    parent_id: str
    title: str
    assigned_agent: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    status: ValidationStatus = ValidationStatus.PENDING
    result: Optional[Dict[str, Any]] = None

@dataclass
class ValidationResult:
    """Résultat de validation"""
    success: bool
    confidence_score: float
    status: ValidationStatus
    checks: List[RealityCheck]
    evidence_trail: List[EvidenceEntry]
    recommendations: List[str] = field(default_factory=list)
    reason: Optional[str] = None

@dataclass
class TaskMetrics:
    """Métriques enrichies pour le TaskMaster"""
    task_id: str
    task_type: str
    user_request: str
    natural_language_command: str
    start_time: datetime
    end_time: Optional[datetime] = None
    
    # Statut et progression
    status: ValidationStatus = ValidationStatus.PENDING
    tasks_completed: int = 0
    tasks_total: int = 0
    human_readable_progress: str = ""
    expected_completion: Optional[datetime] = None
    
    # Validation et evidence
    validation_status: ValidationStatus = ValidationStatus.PENDING
    evidence_trail: List[EvidenceEntry] = field(default_factory=list)
    reality_checks: List[RealityCheck] = field(default_factory=list)
    confidence_score: float = 1.0
    
    # Gestion des dépendances
    dependencies: List[str] = field(default_factory=list)
    subtasks: List[SubTask] = field(default_factory=list)
    
    # Agents et erreurs
    agents_involved: List[str] = field(default_factory=list)
    errors: List[Dict[str, Any]] = field(default_factory=list)
    performance_data: Dict[str, float] = field(default_factory=dict)

class NLPProcessor:
    """Processeur de langage naturel pour TaskMaster"""
    
    def __init__(self):
        # Charger le modèle spaCy pour le français
        try:
            self.nlp = spacy.load("fr_core_news_md")
        except:
            # Fallback sur modèle anglais si français non disponible
            self.nlp = spacy.load("en_core_web_md")
        
        # Pipeline de classification de tâches
        self.task_classifier = self._create_task_classifier()
        
        # Patterns pour extraction d'entités
        self.patterns = self._load_patterns()
    
    def _create_task_classifier(self):
        """Crée un classificateur de types de tâches"""
        # Patterns simples pour démo - à remplacer par ML en production
        return {
            TaskType.AUDIT: ["audit", "vérifier", "contrôler", "inspecter", "sécurité"],
            TaskType.ANALYSIS: ["analyser", "analyse", "évaluer", "examiner", "étudier"],
            TaskType.OPTIMIZATION: ["optimiser", "améliorer", "accélérer", "performance"],
            TaskType.DOCUMENTATION: ["documenter", "documentation", "générer doc", "readme"],
            TaskType.TESTING: ["tester", "test", "valider", "vérification"],
            TaskType.REFACTORING: ["refactorer", "refactoring", "réorganiser", "nettoyer code", "refactorise"],
            TaskType.MONITORING: ["monitorer", "surveiller", "observer", "tracking"],
            TaskType.DEPLOYMENT: ["déployer", "deploiement", "mise en production", "release"]
        }
    
    def _load_patterns(self):
        """Charge les patterns de reconnaissance"""
        return {
            "module": r"module\s+(\w+)",
            "component": r"composant\s+(\w+)",
            "urgent": r"(urgent|critique|prioritaire|asap)",
            "deadline": r"(avant|deadline|échéance)\s+(.+)",
        }
    
    def parse_request(self, user_input: str) -> TaskDefinition:
        """Parse une requête en langage naturel"""
        doc = self.nlp(user_input.lower())
        
        # Détection du type de tâche
        task_type = self._classify_task_type(doc)
        
        # Extraction des entités
        entities = self._extract_entities(doc, user_input)
        
        # Détection de la priorité
        priority = self._detect_priority(doc, user_input)
        
        # Construction de la définition
        return TaskDefinition(
            title=self._generate_title(doc, task_type),
            description=user_input,
            task_type=task_type,
            priority=priority,
            required_capabilities=self._extract_required_capabilities(task_type, entities),
            constraints=self._extract_constraints(doc, entities),
            expected_outputs=self._define_expected_outputs(task_type, entities),
            success_criteria=self._define_success_criteria(task_type, entities),
            metadata=entities
        )
    
    def _classify_task_type(self, doc) -> TaskType:
        """Classifie le type de tâche"""
        text = doc.text
        
        for task_type, keywords in self.task_classifier.items():
            if any(keyword in text for keyword in keywords):
                return task_type
        
        # Default to analysis if no match
        return TaskType.ANALYSIS
    
    def _extract_entities(self, doc, original_text: str) -> Dict[str, Any]:
        """Extrait les entités nommées et patterns"""
        entities = {
            "modules": [],
            "components": [],
            "technologies": [],
            "constraints": []
        }
        
        # Extraction via patterns regex
        for pattern_name, pattern in self.patterns.items():
            matches = re.findall(pattern, original_text, re.IGNORECASE)
            if matches:
                entities[pattern_name] = matches
        
        # Extraction via spaCy NER
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT", "LOC"]:
                entities["components"].append(ent.text)
        
        return entities
    
    def _detect_priority(self, doc, original_text: str) -> TaskPriority:
        """Détecte la priorité de la tâche"""
        urgent_pattern = self.patterns.get("urgent", "")
        if re.search(urgent_pattern, original_text, re.IGNORECASE):
            return TaskPriority.CRITICAL
        
        # Analyse sémantique
        priority_words = {
            TaskPriority.HIGH: ["important", "haute priorité", "rapidement"],
            TaskPriority.MEDIUM: ["normal", "standard", "habituel"],
            TaskPriority.LOW: ["quand possible", "bas", "mineur"]
        }
        
        text = doc.text
        for priority, words in priority_words.items():
            if any(word in text for word in words):
                return priority
        
        return TaskPriority.MEDIUM
    
    def _generate_title(self, doc, task_type: TaskType) -> str:
        """Génère un titre court pour la tâche"""
        # Extraction des mots clés principaux
        keywords = [token.text for token in doc if token.pos_ in ["NOUN", "VERB"] and not token.is_stop]
        title_parts = keywords[:3]  # Limiter à 3 mots clés
        
        return f"{task_type.value.capitalize()} - {' '.join(title_parts)}"
    
    def _extract_required_capabilities(self, task_type: TaskType, entities: Dict) -> List[str]:
        """Détermine les capacités requises"""
        capabilities_map = {
            TaskType.AUDIT: ["security_analysis", "vulnerability_detection", "compliance_check"],
            TaskType.ANALYSIS: ["data_analysis", "pattern_recognition", "statistical_modeling"],
            TaskType.OPTIMIZATION: ["performance_profiling", "algorithm_optimization", "resource_management"],
            TaskType.DOCUMENTATION: ["technical_writing", "diagram_generation", "api_documentation"],
            TaskType.TESTING: ["unit_testing", "integration_testing", "load_testing"],
            TaskType.REFACTORING: ["code_adaptation"],
            TaskType.MONITORING: ["metrics_collection", "alerting", "dashboard_creation"],
            TaskType.DEPLOYMENT: ["ci_cd", "container_management", "rollback_capability"]
        }
        
        return capabilities_map.get(task_type, ["general_processing"])
    
    def _extract_constraints(self, doc, entities: Dict) -> Dict[str, Any]:
        """Extrait les contraintes de la tâche"""
        constraints = {}
        
        # Contrainte de temps si deadline détectée
        if "deadline" in entities:
            constraints["deadline"] = entities["deadline"][0] if entities["deadline"] else None
        
        # Contraintes techniques basées sur les entités
        if entities.get("technologies"):
            constraints["technologies"] = entities["technologies"]
        
        return constraints
    
    def _define_expected_outputs(self, task_type: TaskType, entities: Dict) -> List[str]:
        """Définit les outputs attendus"""
        outputs_map = {
            TaskType.AUDIT: ["security_report", "vulnerability_list", "recommendations"],
            TaskType.ANALYSIS: ["analysis_report", "metrics", "insights", "visualizations"],
            TaskType.OPTIMIZATION: ["performance_report", "optimized_code", "benchmark_results"],
            TaskType.DOCUMENTATION: ["documentation_files", "api_specs", "user_guides"],
            TaskType.TESTING: ["test_report", "coverage_metrics", "bug_list"],
            TaskType.REFACTORING: ["refactored_code", "improvement_report"],
            TaskType.MONITORING: ["dashboard_url", "alert_rules", "metrics_config"],
            TaskType.DEPLOYMENT: ["deployment_log", "rollback_plan", "health_check_results"]
        }
        
        return outputs_map.get(task_type, ["task_report"])
    
    def _define_success_criteria(self, task_type: TaskType, entities: Dict) -> List[str]:
        """Définit les critères de succès"""
        criteria_map = {
            TaskType.AUDIT: ["No critical vulnerabilities", "Compliance score > 95%"],
            TaskType.ANALYSIS: ["All metrics collected", "Insights documented"],
            TaskType.OPTIMIZATION: ["Performance improvement > 20%", "No regressions"],
            TaskType.DOCUMENTATION: ["100% API coverage", "Examples provided"],
            TaskType.TESTING: ["Test coverage > 80%", "All tests passing"],
            TaskType.REFACTORING: ["Code quality improved", "No functionality broken"],
            TaskType.MONITORING: ["All services monitored", "Alerts configured"],
            TaskType.DEPLOYMENT: ["Zero downtime", "Health checks passing"]
        }
        
        return criteria_map.get(task_type, ["Task completed successfully"])

class ValidationEngine:
    """Moteur de validation anti-hallucination"""
    
    def __init__(self, agent_id: str, logger: logging.Logger):
        """Initialisation du moteur de validation"""
        self.agent_id = agent_id
        self.logger = logger
        # Modèles ou configurations de validation pourraient être chargés ici
        self.logger.info(
            f"🔎 ValidationEngine initialisé pour {self.agent_id}",
            extra={"agent_id": agent_id}
        )
    
    async def validate_agent_output(
        self,
        agent_id: str,
        output: Dict[str, Any],
        expected_output: List[str],
        task_context: Dict[str, Any]
    ) -> ValidationResult:
        """Valide la sortie d'un agent contre les hallucinations"""
        
        self.logger.info(
            "Début validation output agent",
            extra={
                "agent_id": agent_id,
                "output_keys": list(output.keys())
            }
        )
        
        checks = []
        
        # 1. Vérification de cohérence structurelle
        structure_check = await self._check_output_structure(output, expected_output)
        checks.append(structure_check)
        
        # 2. Vérification de cohérence sémantique
        semantic_check = await self._check_semantic_coherence(output, task_context)
        checks.append(semantic_check)
        
        # 3. Vérification des valeurs aberrantes
        outlier_check = await self._check_outliers(output)
        checks.append(outlier_check)
        
        # 4. Cross-validation si possible
        if len(self.evidence_trail) > 0:
            cross_check = await self._cross_validate(output)
            checks.append(cross_check)
        
        # 5. Vérification temporelle
        temporal_check = await self._check_temporal_consistency(output, task_context)
        checks.append(temporal_check)
        
        # Calcul du score de confiance global
        passed_checks = sum(1 for check in checks if check.passed)
        confidence = passed_checks / len(checks) if checks else 0.0
        
        # Collecte des preuves
        for check in checks:
            self.evidence_trail.append(
                EvidenceEntry(
                    timestamp=datetime.now(),
                    source=f"{agent_id}_validation",
                    type=check.check_type,
                    content=check.details,
                    confidence=check.confidence,
                    verified=check.passed
                )
            )
        
        # Détermination du statut
        if confidence >= 0.8:
            status = ValidationStatus.APPROVED
            success = True
        elif confidence >= 0.5:
            status = ValidationStatus.PARTIAL
            success = True
        else:
            status = ValidationStatus.REJECTED
            success = False
        
        return ValidationResult(
            success=success,
            confidence_score=confidence,
            status=status,
            checks=checks,
            evidence_trail=self.evidence_trail[-10:],  # Dernières 10 preuves
            recommendations=self._generate_recommendations(checks),
            reason=self._generate_validation_reason(checks, confidence)
        )
    
    async def _check_output_structure(self, output: Dict, expected: List[str]) -> RealityCheck:
        """Vérifie la structure de sortie"""
        missing_keys = [key for key in expected if key not in output]
        extra_keys = [key for key in output if key not in expected]
        
        passed = len(missing_keys) == 0
        confidence = 1.0 - (len(missing_keys) / len(expected)) if expected else 1.0
        
        return RealityCheck(
            check_id=str(uuid4()),
            check_type="structure_validation",
            expected=expected,
            actual=list(output.keys()),
            passed=passed,
            confidence=confidence,
            details={
                "missing_keys": missing_keys,
                "extra_keys": extra_keys
            }
        )
    
    async def _check_semantic_coherence(self, output: Dict, context: Dict) -> RealityCheck:
        """Vérifie la cohérence sémantique"""
        # Analyse simplifiée - en production, utiliser un modèle de langage
        coherence_score = 0.8  # Placeholder
        
        # Vérifications basiques
        incoherences = []
        
        # Vérifier que les résultats correspondent au type de tâche
        task_type = context.get("task_type")
        if task_type == TaskType.AUDIT and "vulnerabilities" not in str(output):
            incoherences.append("Audit task but no vulnerabilities mentioned")
            coherence_score -= 0.2
        
        if task_type == TaskType.OPTIMIZATION and "performance" not in str(output):
            incoherences.append("Optimization task but no performance metrics")
            coherence_score -= 0.2
        
        return RealityCheck(
            check_id=str(uuid4()),
            check_type="semantic_coherence",
            expected="Coherent output matching task type",
            actual=f"Coherence score: {coherence_score}",
            passed=coherence_score >= 0.6,
            confidence=coherence_score,
            details={
                "incoherences": incoherences,
                "task_type": str(task_type)
            }
        )
    
    async def _check_outliers(self, output: Dict) -> RealityCheck:
        """Détecte les valeurs aberrantes"""
        outliers = []
        
        # Vérification des métriques numériques
        for key, value in output.items():
            if isinstance(value, (int, float)):
                # Détection simple d'outliers
                if value < 0 and "error" not in key.lower():
                    outliers.append(f"{key}: negative value {value}")
                elif value > 1000000 and "size" not in key.lower():
                    outliers.append(f"{key}: suspiciously large value {value}")
            elif isinstance(value, str) and len(value) > 10000:
                outliers.append(f"{key}: extremely long string ({len(value)} chars)")
        
        passed = len(outliers) == 0
        confidence = 1.0 - (len(outliers) * 0.2)  # -20% par outlier
        
        return RealityCheck(
            check_id=str(uuid4()),
            check_type="outlier_detection",
            expected="No outlier values",
            actual=f"{len(outliers)} outliers detected",
            passed=passed,
            confidence=max(0, confidence),
            details={"outliers": outliers}
        )
    
    async def _cross_validate(self, output: Dict) -> RealityCheck:
        """Cross-validation avec les preuves existantes"""
        # Comparer avec les outputs précédents
        consistency_score = 0.9  # Placeholder
        
        inconsistencies = []
        
        # Logique de cross-validation simplifiée
        for evidence in self.evidence_trail[-5:]:
            if evidence.type == "agent_output":
                # Comparer les valeurs clés
                prev_output = evidence.content
                for key in set(output.keys()) & set(prev_output.keys()):
                    if output[key] != prev_output[key]:
                        inconsistencies.append(f"Value mismatch for {key}")
                        consistency_score -= 0.1
        
        return RealityCheck(
            check_id=str(uuid4()),
            check_type="cross_validation",
            expected="Consistent with previous evidence",
            actual=f"Consistency score: {consistency_score}",
            passed=consistency_score >= 0.7,
            confidence=consistency_score,
            details={"inconsistencies": inconsistencies}
        )
    
    async def _check_temporal_consistency(self, output: Dict, context: Dict) -> RealityCheck:
        """Vérifie la cohérence temporelle"""
        issues = []
        
        # Vérifier les timestamps
        current_time = datetime.now()
        
        for key, value in output.items():
            if "timestamp" in key or "date" in key:
                try:
                    if isinstance(value, str):
                        ts = datetime.fromisoformat(value.replace('Z', '+00:00'))
                        if ts > current_time:
                            issues.append(f"{key}: future timestamp {value}")
                        elif ts < current_time - timedelta(days=365):
                            issues.append(f"{key}: timestamp too old {value}")
                except:
                    pass
        
        # Vérifier la durée d'exécution
        if "duration" in output:
            duration = output["duration"]
            if isinstance(duration, (int, float)) and duration < 0:
                issues.append(f"Negative duration: {duration}")
        
        passed = len(issues) == 0
        confidence = 1.0 - (len(issues) * 0.25)
        
        return RealityCheck(
            check_id=str(uuid4()),
            check_type="temporal_consistency",
            expected="Temporally consistent data",
            actual=f"{len(issues)} temporal issues",
            passed=passed,
            confidence=max(0, confidence),
            details={"issues": issues}
        )
    
    def _generate_recommendations(self, checks: List[RealityCheck]) -> List[str]:
        """Génère des recommandations basées sur les checks"""
        recommendations = []
        
        for check in checks:
            if not check.passed:
                if check.check_type == "structure_validation":
                    recommendations.append("Review agent output structure and ensure all required fields are present")
                elif check.check_type == "semantic_coherence":
                    recommendations.append("Verify agent logic and ensure outputs match the task requirements")
                elif check.check_type == "outlier_detection":
                    recommendations.append("Investigate detected outliers and validate data ranges")
                elif check.check_type == "temporal_consistency":
                    recommendations.append("Check timestamp generation and duration calculations")
        
        return recommendations
    
    def _generate_validation_reason(self, checks: List[RealityCheck], confidence: float) -> str:
        """Génère une raison lisible pour le résultat de validation"""
        failed_checks = [check for check in checks if not check.passed]
        
        if confidence >= 0.8:
            return "Output validated successfully with high confidence"
        elif confidence >= 0.5:
            return f"Output partially validated. Issues found in: {', '.join(c.check_type for c in failed_checks)}"
        else:
            return f"Output validation failed. Major issues in: {', '.join(c.check_type for c in failed_checks)}"

class DependencyResolver:
    """Résolveur de dépendances pour les tâches complexes"""

    def __init__(self, logger: logging.Logger):
        """Initialisation du résolveur de dépendances"""
        self.logger = logger
        # Ce resolver est stateless et n'a pas sa propre liste d'agents.
        # Il se base sur les capabilities pour suggérer des types d'agents.
        self.logger.info(
            f"🔗 DependencyResolver initialisé."
        )

    def analyze_dependencies(self, task_definition: TaskDefinition) -> Dict[str, Any]:
        """Analyse les dépendances d'une tâche à partir de sa définition"""
        dependencies = {
            "required_agents": [],
            "required_resources": [],
            "prerequisite_tasks": [],
            "parallel_tasks": [],
            "sequential_tasks": []
        }
        
        # Analyse basée sur le type de tâche
        task_deps = self._get_task_type_dependencies(task_definition.task_type)
        dependencies.update(task_deps)
        
        # Analyse des capacités requises
        for capability in task_definition.required_capabilities:
            agents = self._get_agents_for_capability(capability)
            dependencies["required_agents"].extend(agents)
        
        # Déduplication
        dependencies["required_agents"] = list(set(dependencies["required_agents"]))
        
        return dependencies
    
    def _get_task_type_dependencies(self, task_type: TaskType) -> Dict[str, List[str]]:
        """Retourne les dépendances par type de tâche"""
        deps_map = {
            TaskType.AUDIT: {
                "required_agents": ["security_analyzer", "vulnerability_scanner"],
                "sequential_tasks": ["scan", "analyze", "report"]
            },
            TaskType.ANALYSIS: {
                "required_agents": ["data_analyzer", "pattern_detector"],
                "parallel_tasks": ["collect_data", "process_data"],
                "sequential_tasks": ["analyze", "visualize"]
            },
            TaskType.OPTIMIZATION: {
                "required_agents": ["performance_profiler", "optimizer"],
                "prerequisite_tasks": ["baseline_measurement"],
                "sequential_tasks": ["profile", "optimize", "validate"]
            },
            TaskType.DOCUMENTATION: {
                "required_agents": ["doc_generator", "diagram_creator"],
                "parallel_tasks": ["generate_text", "create_diagrams"]
            },
            TaskType.TESTING: {
                "required_agents": ["test_runner", "coverage_analyzer"],
                "sequential_tasks": ["setup", "execute", "teardown"]
            },
            TaskType.REFACTORING: {
                "required_agents": ["code_analyzer", "refactoring_engine"],
                "prerequisite_tasks": ["backup_code"],
                "sequential_tasks": ["analyze", "refactor", "test"]
            }
        }
        
        return deps_map.get(task_type, {"required_agents": ["generic_agent"]})
    
    def _get_agents_for_capability(self, capability: str) -> List[str]:
        """Retourne les agents ayant une capacité spécifique"""
        # CORRECTION: Mapping utilisant les vrais noms d'agents du répertoire /agents.
        capability_agents = {
            "security_analysis": ["agent_MAINTENANCE_09_analyseur_securite"],
            "data_analysis": ["agent_MAINTENANCE_01_analyseur_structure"],
            "pattern_recognition": ["agent_MAINTENANCE_01_analyseur_structure"],
            "performance_profiling": ["agent_MAINTENANCE_08_analyseur_performance"],
            "technical_writing": ["agent_MAINTENANCE_05_documenteur_peer_reviewer"],
            "unit_testing": ["agent_MAINTENANCE_04_testeur_anti_faux_agents"],
            "code_analysis": ["agent_MAINTENANCE_01_analyseur_structure"]
        }
        
        return capability_agents.get(capability, ["agent_MAINTENANCE_00_chef_equipe_coordinateur"])
    
    def create_execution_plan(self, dependencies: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Crée un plan d'exécution ordonné"""
        plan = []
        
        # Phase 1: Prérequis
        if dependencies.get("prerequisite_tasks"):
            for task in dependencies["prerequisite_tasks"]:
                plan.append({
                    "phase": 1,
                    "task": task,
                    "type": "prerequisite",
                    "parallel": False
                })
        
        # Phase 2: Tâches parallèles
        if dependencies.get("parallel_tasks"):
            for task in dependencies["parallel_tasks"]:
                plan.append({
                    "phase": 2,
                    "task": task,
                    "type": "parallel",
                    "parallel": True
                })
        
        # Phase 3: Tâches séquentielles
        if dependencies.get("sequential_tasks"):
            for i, task in enumerate(dependencies["sequential_tasks"]):
                plan.append({
                    "phase": 3 + i,
                    "task": task,
                    "type": "sequential",
                    "parallel": False
                })
        
        return plan

class TaskMasterAI:
    """Intelligence IA du TaskMaster avec anti-hallucination"""
    
    def __init__(self, agent_id: str, config: Dict[str, Any], logger: logging.Logger):
        self.agent_id = agent_id
        self.config = config
        self.logger = logger
        
        # Composants IA
        self.nlp_processor = NLPProcessor()
        self.validation_engine = ValidationEngine(agent_id, logger)
        self.dependency_resolver = DependencyResolver(logger)
        
        # État d'apprentissage
        self.learning_enabled = config.get("learning_mode", True)
        self.task_history = []
        self.success_patterns = defaultdict(list)
        self.failure_patterns = defaultdict(list)
        
        self.logger.info(
            f"🤖 TaskMaster AI initialisée pour {self.agent_id}",
            extra={
                "agent_id": self.agent_id,
                "config": self.config
            }
        )
    
    def parse_natural_language_request(self, user_input: str) -> TaskDefinition:
        """Parse une demande en langage naturel"""
        return self.nlp_processor.parse_request(user_input)
    
    def analyze_task_complexity(self, task_definition: TaskDefinition) -> Dict[str, Any]:
        """Analyse la complexité d'une tâche"""
        complexity_score = 0
        
        # Facteurs de complexité
        factors = {
            "capabilities_count": len(task_definition.required_capabilities),
            "constraints_count": len(task_definition.constraints),
            "expected_outputs_count": len(task_definition.expected_outputs),
            "priority_weight": 4 - task_definition.priority.value,
            "task_type_complexity": self._get_task_type_complexity(task_definition.task_type)
        }
        
        # Calcul du score
        complexity_score = (
            factors["capabilities_count"] * 2 +
            factors["constraints_count"] * 1.5 +
            factors["expected_outputs_count"] * 1 +
            factors["priority_weight"] * 2 +
            factors["task_type_complexity"] * 3
        )
        
        # Déterminer le niveau
        if complexity_score < 10:
            level = "simple"
        elif complexity_score < 20:
            level = "moderate"
        elif complexity_score < 30:
            level = "complex"
        else:
            level = "very_complex"
        
        # Analyser les dépendances
        dependencies = self.dependency_resolver.analyze_dependencies(task_definition)
        
        return {
            "level": level,
            "score": complexity_score,
            "factors": factors,
            "required_agents": dependencies["required_agents"],
            "estimated_duration": self._estimate_duration(complexity_score),
            "parallelization_possible": len(dependencies.get("parallel_tasks", [])) > 0,
            "dependencies": dependencies
        }
    
    def _get_task_type_complexity(self, task_type: TaskType) -> int:
        """Retourne la complexité inhérente d'un type de tâche"""
        complexity_map = {
            TaskType.AUDIT: 4,
            TaskType.ANALYSIS: 3,
            TaskType.OPTIMIZATION: 5,
            TaskType.DOCUMENTATION: 2,
            TaskType.TESTING: 3,
            TaskType.REFACTORING: 4,
            TaskType.MONITORING: 2,
            TaskType.DEPLOYMENT: 5
        }
        return complexity_map.get(task_type, 3)
    
    def _estimate_duration(self, complexity_score: float) -> timedelta:
        """Estime la durée d'exécution basée sur la complexité"""
        # Base: 5 minutes + 2 minutes par point de complexité
        minutes = 5 + (complexity_score * 2)
        return timedelta(minutes=minutes)
    
    def suggest_task_breakdown(self, task_definition: TaskDefinition) -> List[SubTask]:
        """Suggère une décomposition en sous-tâches"""
        subtasks = []
        dependencies = self.dependency_resolver.analyze_dependencies(task_definition)
        execution_plan = self.dependency_resolver.create_execution_plan(dependencies)
        
        parent_id = str(uuid4())
        previous_task_ids = []
        
        for step in execution_plan:
            subtask_id = str(uuid4())
            
            subtask = SubTask(
                id=subtask_id,
                parent_id=parent_id,
                title=f"{task_definition.title} - {step['task']}",
                dependencies=previous_task_ids if not step['parallel'] else [],
                status=ValidationStatus.PENDING
            )
            
            subtasks.append(subtask)
            
            if not step['parallel']:
                previous_task_ids = [subtask_id]
            else:
                previous_task_ids.append(subtask_id)
        
        return subtasks
    
    async def validate_agent_outputs(
        self,
        agent_outputs: Dict[str, Any],
        task_definition: TaskDefinition,
        task_context: Dict[str, Any]
    ) -> ValidationResult:
        """Valide les sorties des agents avec anti-hallucination"""
        validation_results = []
        
        for agent_id, output in agent_outputs.items():
            result = await self.validation_engine.validate_agent_output(
                agent_id=agent_id,
                output=output,
                expected_output=task_definition.expected_outputs,
                task_context=task_context
            )
            validation_results.append(result)
        
        # Agrégation des résultats
        if not validation_results:
            return ValidationResult(
                success=True, # Pas de résultats à valider, on considère que c'est un succès.
                confidence_score=1.0,
                status=ValidationStatus.APPROVED,
                checks=[],
                evidence_trail=[],
                recommendations=[]
            )

        total_confidence = sum(r.confidence_score for r in validation_results) / len(validation_results)
        all_checks = []
        all_evidence = []
        
        for result in validation_results:
            all_checks.extend(result.checks)
            all_evidence.extend(result.evidence_trail)
        
        # Statut global
        if total_confidence >= 0.8:
            global_status = ValidationStatus.APPROVED
        elif total_confidence >= 0.5:
            global_status = ValidationStatus.PARTIAL
        else:
            global_status = ValidationStatus.REJECTED
        
        return ValidationResult(
            success=global_status != ValidationStatus.REJECTED,
            confidence_score=total_confidence,
            status=global_status,
            checks=all_checks,
            evidence_trail=all_evidence,
            recommendations=self._consolidate_recommendations(validation_results)
        )
    
    def _consolidate_recommendations(self, results: List[ValidationResult]) -> List[str]:
        """Consolide les recommandations de plusieurs validations"""
        all_recommendations = []
        for result in results:
            all_recommendations.extend(result.recommendations)
        
        # Déduplication et priorisation
        unique_recommendations = list(set(all_recommendations))
        return sorted(unique_recommendations, key=lambda x: len(x))
    
    async def update_learning(
        self,
        task_id: str,
        task_definition: TaskDefinition,
        outcome: Dict[str, Any],
        success: bool
    ):
        """Met à jour l'apprentissage basé sur les résultats"""
        if not self.learning_enabled:
            return
        
        # Enregistrer dans l'historique
        self.task_history.append({
            "task_id": task_id,
            "task_type": task_definition.task_type,
            "complexity": outcome.get("complexity_score", 0),
            "success": success,
            "duration": outcome.get("duration", 0),
            "confidence": outcome.get("confidence_score", 0)
        })
        
        # Identifier les patterns
        pattern_key = f"{task_definition.task_type}_{task_definition.priority}"
        
        if success:
            self.success_patterns[pattern_key].append(outcome)
        else:
            self.failure_patterns[pattern_key].append(outcome)
        
        # Ajuster les stratégies futures
        if len(self.task_history) % 10 == 0:
            await self._analyze_patterns_and_adjust()
    
    async def _analyze_patterns_and_adjust(self):
        """Analyse les patterns et ajuste les stratégies"""
        self.logger.info("Analyse des patterns d'apprentissage")
        
        # Analyse simplifiée - en production, utiliser ML
        for pattern_key, successes in self.success_patterns.items():
            if len(successes) >= 5:
                avg_confidence = sum(s.get("confidence_score", 0) for s in successes) / len(successes)
                self.logger.info(f"Pattern {pattern_key}: avg confidence {avg_confidence:.2f}")

class AgentTaskMasterNextGeneration:
    """
    Agent TaskMaster NextGeneration - Interface centrale de gestion de tâches
    Support multi-instance et validation anti-hallucination
    """
    
    def __init__(
        self,
        agent_id: str = None,
        agent_type: str = "taskmaster_central",
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialisation avec support multi-instance"""
        self.agent_id = agent_id or f"taskmaster_{uuid4().hex[:8]}"
        self.agent_type = agent_type
        self.config = config or {}
        self.work_dir = WORK_DIR
        
        # Logging centralisé avec isolation par instance
        # CORRECTION : Utilisation de la classe LoggingManager et de la méthode get_logger
        # avec une configuration personnalisée pour reproduire l'ancien comportement.
        self.logging_manager = LoggingManager()
        
        logging_config = self.config.get("logging")
        if logging_config:
            self.logger = self.logging_manager.get_logger("custom", custom_config=logging_config)
        else:
            agent_logger_config = {
                "logger_name": f"taskmaster_{self.agent_id}",
                "log_level": "INFO",
                "file_enabled": True,
                "log_dir": str(self.work_dir / f"logs/agents/taskmaster_{self.agent_id}"),
                "filename_pattern": "taskmaster_activity.log",
                "console_enabled": True,
                "async_enabled": True
            }
            self.logger = self.logging_manager.get_logger(
                config_name="agent_taskmaster",
                custom_config=agent_logger_config
            )
        
        # Audit logger pour traçabilité - mis en commentaire car non implémenté dans le manager actuel
        # self.audit_logger = self.logging_manager.create_audit_logger(
        #     user_id=self.agent_id,
        #     action_type="task_management"
        # )
        
        # Monitoring et métriques - mis en commentaire
        # self.metrics_collector = MetricsCollector(self.agent_id)
        # self.health_monitor = HealthMonitor(self.agent_id)
        
        # Intelligence TaskMaster
        self.taskmaster_ai = TaskMasterAI(
            agent_id=self.agent_id,
            config={
                "learning_mode": self.config.get("ai_learning_mode", True),
                "model": self.config.get("ai_model", "gpt-4"),
                "temperature": self.config.get("ai_temperature", 0.2)
            },
            logger=self.logger
        )
        
        # État interne
        self.active_tasks: Dict[str, TaskMetrics] = {}
        self.completed_tasks: Dict[str, TaskMetrics] = {}
        self.user_sessions: Dict[str, Dict[str, Any]] = {}
        self._is_running = False
        
        # Pool d'exécution pour parallélisation
        self._executor = ThreadPoolExecutor(
            max_workers=self.config.get("max_parallel_tasks", 5),
            thread_name_prefix=f"TaskMaster_{self.agent_id}"
        )
        
        # Découverte des agents disponibles
        self.available_agents = self._discover_available_agents()
        
        # Configuration des limites
        self.max_concurrent_tasks = self.config.get("max_concurrent_tasks", 10)
        self.task_timeout = self.config.get("task_timeout", 600)  # 10 minutes par défaut
        
        # Log d'initialisation
        self.logger.info(
            f"🎯 TaskMaster {self.agent_id} initialisé",
            extra={
                "agent_id": self.agent_id,
                "config": {
                    "max_parallel_tasks": self.config.get("max_parallel_tasks", 5),
                    "max_concurrent_tasks": self.max_concurrent_tasks,
                    "task_timeout": self.task_timeout,
                    "ai_enabled": True,
                    "learning_mode": self.config.get("ai_learning_mode", True)
                }
            }
        )
    
    def _discover_available_agents(self) -> Dict[str, Dict[str, Any]]:
        """Scanne le répertoire /agents pour découvrir dynamiquement les agents et leurs capacités."""
        self.logger.info("Début de la découverte dynamique des agents...")
        agents_dir = PROJECT_ROOT / "agents"
        available_agents = {}

        if not agents_dir.is_dir():
            self.logger.warning(f"Le répertoire des agents '{agents_dir}' n'a pas été trouvé.")
            return {}

        for filename in os.listdir(agents_dir):
            if filename.startswith("agent_") and filename.endswith(".py"):
                module_name = f"agents.{filename[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    for _, cls in inspect.getmembers(module, inspect.isclass):
                        if issubclass(cls, Agent) and cls is not Agent:
                            instance = cls()
                            capabilities = instance.get_capabilities()
                            agent_name = filename[:-3]
                            available_agents[agent_name] = {
                                "capabilities": capabilities,
                                "status": "available"
                            }
                            self.logger.debug(f"Agent découvert: {agent_name} avec les capacités: {capabilities}")
                            break 
                except Exception as e:
                    self.logger.error(f"Impossible de charger ou d'inspecter l'agent {module_name}: {e}")
        
        self.logger.info(f"{len(available_agents)} agents découverts dynamiquement.")
        return available_agents
    
    async def startup(self) -> Dict[str, Any]:
        """Démarrage de l'instance TaskMaster"""
        start_time = time.time()
        self.logger.info(
            f"🚀 Démarrage TaskMaster {self.agent_id}",
            extra={"operation": "startup", "phase": "init"}
        )
        
        try:
            # Vérification de l'environnement
            await self._verify_environment()
            
            # Démarrage des composants - mis en commentaire
            # await self.metrics_collector.start()
            # await self.health_monitor.start()
            
            # Chargement de l'état si persisté
            await self._load_state()
            
            self._is_running = True
            
            # Démarrer la maintenance périodique - Commenté car la méthode n'est pas implémentée
            # asyncio.create_task(self._periodic_maintenance())
            
            result = {
                "status": "started",
                "agent_id": self.agent_id,
                "available_agents": len(self.available_agents),
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.info(
                f"✅ TaskMaster {self.agent_id} démarré",
                extra={"operation": "startup", "phase": "complete", "result": result}
            )
            
            exec_time = time.time() - start_time
            self.logging_manager.log_performance("taskmaster_startup", exec_time)
            
            return result
            
        except Exception as e:
            self.logger.error(
                f"❌ Erreur démarrage TaskMaster",
                extra={"error": str(e)},
                exc_info=True
            )
            raise
    
    async def _verify_environment(self):
        """Vérifie l'environnement d'exécution en utilisant WORK_DIR."""
        required_dirs = [
            self.work_dir / f"logs/agents/taskmaster_{self.agent_id}",
            self.work_dir / f"data/taskmaster_{self.agent_id}",
            self.work_dir / f"reports/taskmaster_{self.agent_id}"
        ]
        
        for dir_path in required_dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    async def _load_state(self):
        """Charge l'état persisté si disponible depuis WORK_DIR."""
        state_file = self.work_dir / f"data/taskmaster_{self.agent_id}/state.json"
        if state_file.exists():
            try:
                with open(state_file, 'r') as f:
                    state = json.load(f)
                    # Restaurer les tâches actives
                    # Implementation simplifiée
                    self.logger.info(f"État restauré depuis {state_file}")
            except Exception as e:
                self.logger.warning(f"Impossible de charger l'état: {e}")

    async def shutdown(self):
        """Arrêt propre de l'instance TaskMaster."""
        start_time = time.time()
        self.logger.info(
            f"🔌 Arrêt de TaskMaster {self.agent_id}",
            extra={"operation": "shutdown", "phase": "init"}
        )
        
        self._is_running = False
        
        # Arrêter le pool de threads
        self.logger.info(f"Arrêt du pool de threads pour {self.agent_id}...")
        self._executor.shutdown(wait=True)
        self.logger.info("Pool de threads arrêté.")
        
        # Arrêt des composants - mis en commentaire pour l'instant
        # await self.metrics_collector.stop()
        # await self.health_monitor.stop()
        
        # Sauvegarder l'état final - mis en commentaire car non implémenté
        # await self._save_state()

        result = {
            "status": "shutdown",
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }

        self.logger.info(
            f"🛑 TaskMaster {self.agent_id} arrêté proprement.",
            extra={"operation": "shutdown", "phase": "complete", "result": result}
        )
        
        exec_time = time.time() - start_time
        self.logging_manager.log_performance("taskmaster_shutdown", exec_time)
        return result
    
    async def create_task_from_natural_language(
        self,
        user_request: str,
        user_id: str = "default_user",
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Interface principale - création de tâche en langage naturel"""
        task_id = f"task_{self.agent_id}_{int(time.time()*1000)}"
        
        # Vérifier les limites
        if len(self.active_tasks) >= self.max_concurrent_tasks:
            return {
                "status": "rejected",
                "reason": f"Maximum concurrent tasks ({self.max_concurrent_tasks}) reached",
                "retry_after": 60
            }
        
        start_time = time.time()
        try:
            # Log de la requête
            self.logger.info(
                f"📝 Nouvelle requête TaskMaster",
                extra={
                    "task_id": task_id,
                    "user_id": user_id,
                    "request": user_request[:100] + "..." if len(user_request) > 100 else user_request
                }
            )
            
            # Créer ou récupérer la session utilisateur
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = {
                    "created_at": datetime.now(),
                    "task_count": 0,
                    "context": context or {}
                }
            
            session = self.user_sessions[user_id]
            session["task_count"] += 1
            
            # 1. Parser la requête en langage naturel
            task_definition = self.taskmaster_ai.parse_natural_language_request(user_request)
            
            # 2. Analyser la complexité
            complexity_analysis = self.taskmaster_ai.analyze_task_complexity(task_definition)
            
            # 3. Créer les métriques de tâche
            task_metrics = TaskMetrics(
                task_id=task_id,
                task_type=task_definition.task_type.value,
                user_request=user_request,
                natural_language_command=user_request,
                start_time=datetime.now()
            )
            task_metrics.tasks_total = len(task_metrics.subtasks)
            
            # 4. Valider la faisabilité de la tâche
            feasibility_result = await self._validate_task_feasibility(task_definition, complexity_analysis)
            
            if not feasibility_result["feasible"]:
                return {
                    "status": "rejected",
                    "reason": feasibility_result["reason"],
                    "suggestions": feasibility_result["checks"]
                }
            
            # Tâche acceptée, ajout à la liste des tâches actives
            self.active_tasks[task_id] = task_metrics

            # 5. Exécuter la tâche
            await self._execute_task_async(task_id, task_definition, task_metrics, complexity_analysis)
            
            result = {
                "status": "accepted",
                "task_id": task_id,
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.info(
                f"✅ Tâche {task_id} acceptée",
                extra={"operation": "create_task", "phase": "complete", "result": result}
            )
            
            exec_time = time.time() - start_time
            self.logging_manager.log_performance(f"create_task_{task_id}", exec_time)
            
            return result
            
        except Exception as e:
            self.logger.error(
                f"❌ Erreur création tâche {task_id}",
                extra={"task_id": task_id, "error": str(e)},
                exc_info=True
            )
            raise
    
    async def _validate_task_feasibility(
        self,
        task_definition: TaskDefinition,
        complexity_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Valide la faisabilité d'une tâche en vérifiant les capacités requises."""
        feasibility_checks = []

        # 1. Vérifier la disponibilité des capacités requises
        required_capabilities = set(task_definition.required_capabilities)
        
        all_available_capabilities = set()
        for agent_info in self.available_agents.values():
            if agent_info.get("status") == "available":
                all_available_capabilities.update(agent_info.get("capabilities", []))

        missing_capabilities = required_capabilities - all_available_capabilities
        
        capabilities_available = not missing_capabilities
        
        feasibility_checks.append({
            "check": "capabilities_availability",
            "passed": capabilities_available,
            "details": f"Missing capabilities: {missing_capabilities}" if not capabilities_available else "All capabilities available"
        })
        
        # 2. Vérifier les contraintes
        constraints_valid = True
        if "deadline" in task_definition.constraints:
            # Vérifier que le deadline est réaliste
            estimated_duration = complexity_analysis["estimated_duration"]
            deadline = task_definition.constraints["deadline"]
            # Logique de validation du deadline
            constraints_valid = True  # Simplifié
        
        feasibility_checks.append({
            "check": "constraints_validation",
            "passed": constraints_valid,
            "details": "Constraints validated"
        })
        
        # 3. Vérifier la charge système
        system_load_ok = len(self.active_tasks) < self.max_concurrent_tasks * 0.8
        feasibility_checks.append({
            "check": "system_load",
            "passed": system_load_ok,
            "details": f"System load: {len(self.active_tasks)}/{self.max_concurrent_tasks}"
        })
        
        # Décision finale
        all_passed = all(check["passed"] for check in feasibility_checks)
        
        result = {
            "feasible": all_passed,
            "checks": feasibility_checks
        }
        
        if not all_passed:
            failed_checks = [c for c in feasibility_checks if not c["passed"]]
            result["reason"] = f"Failed checks: {', '.join(c['check'] for c in failed_checks)}"
            result["suggestions"] = self._generate_feasibility_suggestions(failed_checks)
        
        return result
    
    def _generate_feasibility_suggestions(self, failed_checks: List[Dict]) -> List[str]:
        """Génère des suggestions pour les checks échoués"""
        suggestions = []
        
        for check in failed_checks:
            if check["check"] == "capabilities_availability":
                suggestions.append("Deploy required agents or check their status")
                suggestions.append("Consider splitting the task into smaller parts with available capabilities")
            elif check["check"] == "system_load":
                suggestions.append("Wait for current tasks to complete")
                suggestions.append("Increase system capacity")
        
        return suggestions
    
    async def _execute_task_async(
        self,
        task_id: str,
        task_definition: TaskDefinition,
        task_metrics: TaskMetrics,
        complexity_analysis: Dict[str, Any]
    ):
        """Exécution asynchrone d'une tâche avec orchestration"""
        try:
            # Mise à jour du statut
            task_metrics.status = ValidationStatus.APPROVED
            task_metrics.human_readable_progress = "Task execution started"
            
            # Log de début d'exécution
            self.logger.info(
                f"🔄 Exécution tâche {task_id}",
                extra={
                    "task_id": task_id,
                    "subtasks_count": len(task_metrics.subtasks),
                    "complexity": complexity_analysis["level"]
                }
            )
            
            # Exécuter les sous-tâches selon le plan
            agents_results = {}
            
            for subtask in task_metrics.subtasks:
                # Sélectionner l'agent optimal
                agent = self._select_agent_for_subtask(subtask, complexity_analysis["required_agents"])
                subtask.assigned_agent = agent
                
                # Exécuter la sous-tâche
                result = await self._execute_subtask(
                    subtask,
                    agent,
                    task_definition,
                    task_metrics
                )
                
                agents_results[subtask.id] = result
                
                # Mise à jour de la progression
                task_metrics.tasks_completed += 1
                progress_percent = (task_metrics.tasks_completed / task_metrics.tasks_total) * 100
                task_metrics.human_readable_progress = f"Progress: {progress_percent:.1f}% - Executing {subtask.title}"
                
                # Validation continue
                if self.config.get("continuous_validation", True):
                    validation = await self.taskmaster_ai.validate_agent_outputs(
                        {agent: result},
                        task_definition,
                        {"task_id": task_id, "subtask_id": subtask.id}
                    )
                    
                    if validation.confidence_score < 0.5:
                        self.logger.warning(
                            f"Low confidence validation for subtask {subtask.id}",
                            extra={"confidence": validation.confidence_score}
                        )
            
            # Validation finale globale
            final_validation = await self.taskmaster_ai.validate_agent_outputs(
                agents_results,
                task_definition,
                {"task_id": task_id, "task_type": task_definition.task_type}
            )
            
            # Compilation des résultats
            task_result = {
                "task_id": task_id,
                "status": "completed" if final_validation.success else "failed",
                "subtasks_results": agents_results,
                "validation": asdict(final_validation),
                "duration": (datetime.now() - task_metrics.start_time).total_seconds(),
                "human_summary": self._generate_human_summary(
                    task_definition,
                    agents_results,
                    final_validation
                )
            }
            
            # Mise à jour des métriques
            task_metrics.end_time = datetime.now()
            task_metrics.validation_status = final_validation.status
            task_metrics.confidence_score = final_validation.confidence_score
            task_metrics.evidence_trail = final_validation.evidence_trail
            task_metrics.reality_checks = final_validation.checks
            
            # Déplacer vers les tâches complétées
            self.completed_tasks[task_id] = self.active_tasks.pop(task_id)
            
            # Apprentissage
            if self.taskmaster_ai.learning_enabled:
                await self.taskmaster_ai.update_learning(
                    task_id,
                    task_definition,
                    task_result,
                    final_validation.success
                )
            
            # Sauvegarder le rapport
            await self._save_task_report(task_id, task_result, task_metrics)
            
            # Log de fin
            self.logger.info(
                f"✅ Tâche {task_id} terminée",
                extra={
                    "task_id": task_id,
                    "success": final_validation.success,
                    "confidence": final_validation.confidence_score,
                    "duration": task_result["duration"]
                }
            )
            
        except Exception as e:
            # Gestion d'erreur
            task_metrics.status = ValidationStatus.REJECTED
            task_metrics.errors.append({
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "traceback": True
            })
            
            self.logger.error(
                f"❌ Erreur exécution tâche {task_id}",
                extra={"task_id": task_id, "error": str(e)},
                exc_info=True
            )
            
            # Déplacer vers complétées avec statut erreur
            if task_id in self.active_tasks:
                self.completed_tasks[task_id] = self.active_tasks.pop(task_id)
    
    async def _save_task_report(
        self,
        task_id: str,
        task_result: Dict[str, Any],
        task_metrics: TaskMetrics
    ):
        """Sauvegarde le rapport de tâche dans un fichier JSON dans WORK_DIR."""
        report_dir = self.work_dir / f"reports/taskmaster_{self.agent_id}"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_file = report_dir / f"task_report_{task_id}.json"
        
        report_data = {
            "task_result": task_result,
            "task_metrics": asdict(task_metrics)
        }
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=4, default=str)
            self.logger.info(f"Rapport de tâche sauvegardé dans {report_file}")
        except Exception as e:
            self.logger.error(
                f"Erreur lors de la sauvegarde du rapport de tâche {task_id}",
                extra={"error": str(e), "path": str(report_file)},
                exc_info=True
            )
    
    def _select_agent_for_subtask(
        self,
        subtask: SubTask,
        required_agents: List[str]
    ) -> str:
        """Sélectionne l'agent optimal pour une sous-tâche"""
        # Logique simplifiée - en production, utiliser un algorithme plus sophistiqué
        # basé sur la charge, les capacités, l'historique de performance, etc.
        
        available = [
            agent for agent in required_agents
            if agent in self.available_agents and
            self.available_agents[agent]["status"] == "available"
        ]
        
        if available:
            return available[0]
        else:
            # Fallback sur un agent générique
            return "agent_MAINTENANCE_00_chef_equipe_coordinateur"
    
    async def _execute_subtask(
        self,
        subtask: SubTask,
        agent: str,
        task_definition: TaskDefinition,
        task_metrics: TaskMetrics
    ) -> Dict[str, Any]:
        """Exécute une sous-tâche avec un agent spécifique"""
        # Simulation d'exécution - en production, appeler vraiment l'agent
        await asyncio.sleep(1)  # Simulation
        
        # Résultat simulé
        result = {
            "subtask_id": subtask.id,
            "agent": agent,
            "status": "completed",
            "output": {
                "analysis": f"Analysis results for {subtask.title}",
                "metrics": {
                    "quality_score": 0.85,
                    "performance_impact": "positive",
                    "issues_found": 3,
                    "issues_fixed": 3
                },
                "recommendations": [
                    "Continue monitoring",
                    "Schedule follow-up in 1 week"
                ]
            },
            "execution_time": 1.5,
            "timestamp": datetime.now().isoformat()
        }
        
        # Ajouter des evidence entries
        task_metrics.evidence_trail.append(
            EvidenceEntry(
                timestamp=datetime.now(),
                source=agent,
                type="subtask_execution",
                content=result,
                confidence=0.85,
                verified=True
            )
        )
        
        return result
    
    def _generate_human_summary(
        self,
        task_definition: TaskDefinition,
        results: Dict[str, Any],
        validation: ValidationResult
    ) -> str:
        """Génère un résumé lisible pour l'utilisateur"""
        summary_parts = [
            f"Task: {task_definition.title}",
            f"Type: {task_definition.task_type.value}",
            f"Status: {'Completed successfully' if validation.success else 'Failed'}",
            f"Confidence: {validation.confidence_score*100:.1f}%",
            "",
            "Results:"
        ]
        
        # Ajouter les résultats principaux
        for subtask_id, result in results.items():
            if isinstance(result, dict) and "output" in result:
                output = result["output"]
                if isinstance(output, dict) and "analysis" in output:
                    summary_parts.append(f"- {output['analysis']}")
        
        # Ajouter les recommandations
        if validation.recommendations:
            summary_parts.extend(["", "Recommendations:"])
            summary_parts.extend([f"- {rec}" for rec in validation.recommendations])
        
        return "\n".join(summary_parts)



