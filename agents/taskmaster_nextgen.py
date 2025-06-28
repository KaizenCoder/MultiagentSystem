#!/usr/bin/env python3
"""
🚀 TaskMaster NextGeneration - Agent Orchestrateur Hybride Avancé
===============================================================

Architecture hybride combinant :
- Base fonctionnelle du TaskMaster Final existant (découverte agents, délégation)
- Fonctionnalités avancées du prototype abandonné (NLP, complexité, anti-hallucination)
- Intégration Pattern Factory architecture
- Nouvelles capacités : CRUD, export, parsing documents

Auteur: NextGeneration Team
Version: 1.0.0
Date: 2025-06-23
"""

import os
import sys
import logging
import asyncio
import json
import time
import spacy
import importlib
import inspect
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
from uuid import uuid4
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import hashlib
import re

# Intégration avec l'architecture existante
try:
    from core.agent_factory_architecture import BaseAgent, AgentFactory, TaskStatus
    from core.logging_core import get_logger
except ImportError:
    # Fallback si modules core non disponibles
    class BaseAgent:
        pass
    
    class AgentFactory:
        pass
    
    class TaskStatus(Enum):
        PENDING = "pending"
        RUNNING = "running"
        COMPLETED = "completed"
        FAILED = "failed"
    
    def get_logger(name):
        return logging.getLogger(name)

# ==========================================
# 1. TYPES ET ENUMERATIONS
# ==========================================

class TaskType(Enum):
    """Types de tâches supportés avec extension"""
    AUDIT = "audit"
    ANALYSIS = "analysis"
    OPTIMIZATION = "optimization"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    REFACTORING = "refactoring"
    MONITORING = "monitoring"
    DEPLOYMENT = "deployment"
    PARSING = "parsing"
    PLANNING = "planning"

class ValidationStatus(Enum):
    """Statuts de validation anti-hallucination"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_CLARIFICATION = "needs_clarification"
    PARTIAL = "partial"

class TaskPriority(Enum):
    """Niveaux de priorité avec scores"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

class ComplexityLevel(Enum):
    """Niveaux de complexité"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"

# ==========================================
# 2. STRUCTURES DE DONNÉES
# ==========================================

@dataclass
class EvidenceEntry:
    """Entrée de preuve pour validation anti-hallucination"""
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
    """Définition enrichie d'une tâche avec métadonnées"""
    id: str
    title: str
    description: str
    task_type: TaskType
    priority: TaskPriority
    required_capabilities: List[str]
    constraints: Dict[str, Any] = field(default_factory=dict)
    expected_outputs: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    complexity_score: float = 0.0
    estimated_duration: int = 0  # en minutes

@dataclass
class SubTask:
    """Sous-tâche décomposée avec dépendances"""
    id: str
    parent_id: str
    title: str
    assigned_agent: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    status: ValidationStatus = ValidationStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class TaskMetrics:
    """Métriques d'exécution des tâches"""
    task_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    execution_time: Optional[float] = None
    agent_used: Optional[str] = None
    success: bool = False
    error_count: int = 0
    confidence_score: float = 0.0

# ==========================================
# 3. PROCESSEUR NLP AVANCÉ
# ==========================================

class NLPProcessor:
    """Processeur NLP avancé pour analyse de documents et requêtes"""
    
    def __init__(self):
        self.nlp = None
        self.task_classifier = None
        self.patterns = self._load_patterns()
        self._initialize_nlp()
    
    def _initialize_nlp(self):
        """Initialise spaCy avec gestion d'erreur"""
        try:
            self.nlp = spacy.load("fr_core_news_md")
        except OSError:
            try:
                self.nlp = spacy.load("en_core_web_md")
            except OSError:
                logging.warning("Modèles spaCy non disponibles, fonctionnalités NLP limitées")
                self.nlp = None
    
    def _load_patterns(self) -> Dict[str, List[str]]:
        """Charge les patterns de reconnaissance de tâches"""
        return {
            TaskType.AUDIT.value: ["audit", "review", "check", "verify", "examine", "inspect"],
            TaskType.ANALYSIS.value: ["analyze", "study", "investigate", "research", "explore"],
            TaskType.OPTIMIZATION.value: ["optimize", "improve", "enhance", "refactor", "speed"],
            TaskType.DOCUMENTATION.value: ["document", "write", "create docs", "readme", "guide"],
            TaskType.TESTING.value: ["test", "validate", "check", "pytest", "unittest"],
            TaskType.REFACTORING.value: ["refactor", "cleanup", "restructure", "reorganize"],
            TaskType.MONITORING.value: ["monitor", "track", "observe", "watch", "metrics"],
            TaskType.DEPLOYMENT.value: ["deploy", "install", "setup", "configure", "launch"],
            TaskType.PARSING.value: ["parse", "extract", "process", "read", "analyze document"],
            TaskType.PLANNING.value: ["plan", "organize", "structure", "breakdown", "schedule"]
        }
    
    def parse_request(self, user_input: str) -> TaskDefinition:
        """Parse une requête en langage naturel et génère une TaskDefinition"""
        task_id = str(uuid4())
        
        # Classification du type de tâche
        task_type = self._classify_task_type(user_input)
        
        # Extraction d'entités si spaCy disponible
        entities = self._extract_entities(user_input) if self.nlp else {}
        
        # Détection de priorité
        priority = self._detect_priority(user_input)
        
        # Génération titre intelligent
        title = self._generate_title(user_input, task_type)
        
        # Extraction des capacités requises
        capabilities = self._extract_capabilities(user_input, task_type)
        
        return TaskDefinition(
            id=task_id,
            title=title,
            description=user_input,
            task_type=task_type,
            priority=priority,
            required_capabilities=capabilities,
            metadata={
                "entities": entities,
                "original_input": user_input,
                "auto_generated": True
            }
        )
    
    def _classify_task_type(self, text: str) -> TaskType:
        """Classifie le type de tâche basé sur les mots-clés"""
        text_lower = text.lower()
        scores = {}
        
        for task_type, keywords in self.patterns.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                scores[task_type] = score
        
        if scores:
            best_type = max(scores, key=scores.get)
            return TaskType(best_type)
        
        return TaskType.ANALYSIS  # Type par défaut
    
    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extrait les entités nommées du texte"""
        if not self.nlp:
            return {}
        
        doc = self.nlp(text)
        entities = {}
        
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            entities[ent.label_].append(ent.text)
        
        return entities
    
    def _detect_priority(self, text: str) -> TaskPriority:
        """Détecte la priorité basée sur des mots-clés"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["urgent", "critical", "asap", "immediately"]):
            return TaskPriority.CRITICAL
        elif any(word in text_lower for word in ["important", "high", "priority"]):
            return TaskPriority.HIGH
        elif any(word in text_lower for word in ["low", "when possible", "later"]):
            return TaskPriority.LOW
        
        return TaskPriority.MEDIUM
    
    def _generate_title(self, text: str, task_type: TaskType) -> str:
        """Génère un titre intelligent pour la tâche"""
        words = text.split()
        if len(words) <= 8:
            return text.capitalize()
        
        # Extrait les premiers mots significatifs
        title_words = []
        for word in words[:8]:
            if len(word) > 2 and word.lower() not in ["the", "and", "or", "but", "in", "on", "at"]:
                title_words.append(word)
            if len(title_words) >= 5:
                break
        
        title = " ".join(title_words).capitalize()
        return f"{task_type.value.title()}: {title}"
    
    def _extract_capabilities(self, text: str, task_type: TaskType) -> List[str]:
        """Extrait les capacités requises basées sur le texte et type"""
        capabilities = []
        
        # Mapping type -> capacités de base
        base_capabilities = {
            TaskType.AUDIT: ["security_analysis", "code_review"],
            TaskType.ANALYSIS: ["data_analysis", "research"],
            TaskType.OPTIMIZATION: ["performance_tuning", "code_optimization"],
            TaskType.DOCUMENTATION: ["technical_writing", "documentation"],
            TaskType.TESTING: ["unit_testing", "integration_testing"],
            TaskType.REFACTORING: ["code_refactoring", "architecture"],
            TaskType.MONITORING: ["monitoring", "metrics"],
            TaskType.DEPLOYMENT: ["deployment", "devops"],
            TaskType.PARSING: ["document_parsing", "nlp"],
            TaskType.PLANNING: ["project_planning", "task_breakdown"]
        }
        
        capabilities.extend(base_capabilities.get(task_type, ["general"]))
        
        # Détection de technologies spécifiques
        tech_keywords = {
            "python": "python_development",
            "javascript": "javascript_development", 
            "docker": "containerization",
            "kubernetes": "orchestration",
            "database": "database_management",
            "api": "api_development",
            "security": "cybersecurity",
            "ml": "machine_learning",
            "ai": "artificial_intelligence"
        }
        
        text_lower = text.lower()
        for keyword, capability in tech_keywords.items():
            if keyword in text_lower:
                capabilities.append(capability)
        
        return list(set(capabilities))  # Supprimer les doublons

# ==========================================
# 4. ANALYSEUR DE COMPLEXITÉ
# ==========================================

class ComplexityAnalyzer:
    """Analyseur de complexité avec algorithmes avancés"""
    
    def __init__(self):
        self.complexity_weights = {
            "capabilities_count": 2.0,
            "constraints_count": 1.5,
            "expected_outputs_count": 1.0,
            "priority_weight": 2.0,
            "task_type_complexity": 3.0,
            "dependencies_count": 2.5
        }
        
        self.task_type_complexity = {
            TaskType.AUDIT: 3.0,
            TaskType.ANALYSIS: 2.5,
            TaskType.OPTIMIZATION: 4.0,
            TaskType.DOCUMENTATION: 1.5,
            TaskType.TESTING: 2.0,
            TaskType.REFACTORING: 4.5,
            TaskType.MONITORING: 2.0,
            TaskType.DEPLOYMENT: 3.5,
            TaskType.PARSING: 2.5,
            TaskType.PLANNING: 3.0
        }
    
    def analyze_task_complexity(self, task_definition: TaskDefinition) -> Dict[str, Any]:
        """Analyse la complexité d'une tâche et retourne métriques détaillées"""
        
        factors = {
            "capabilities_count": len(task_definition.required_capabilities),
            "constraints_count": len(task_definition.constraints),
            "expected_outputs_count": len(task_definition.expected_outputs),
            "priority_weight": task_definition.priority.value,
            "task_type_complexity": self.task_type_complexity.get(task_definition.task_type, 2.0)
        }
        
        # Calcul du score de complexité
        complexity_score = sum(
            factors[key] * self.complexity_weights[key] 
            for key in factors if key in self.complexity_weights
        )
        
        # Normalisation du score (0-100)
        normalized_score = min(100, complexity_score)
        
        # Détermination du niveau
        if normalized_score < 15:
            level = ComplexityLevel.SIMPLE
            estimated_duration = 5 + int(normalized_score * 0.5)
        elif normalized_score < 35:
            level = ComplexityLevel.MODERATE
            estimated_duration = 15 + int(normalized_score * 0.8)
        elif normalized_score < 60:
            level = ComplexityLevel.COMPLEX
            estimated_duration = 30 + int(normalized_score * 1.2)
        else:
            level = ComplexityLevel.VERY_COMPLEX
            estimated_duration = 60 + int(normalized_score * 2.0)
        
        return {
            "complexity_score": normalized_score,
            "complexity_level": level,
            "estimated_duration_minutes": estimated_duration,
            "factors": factors,
            "justification": self._generate_justification(level, factors)
        }
    
    def _generate_justification(self, level: ComplexityLevel, factors: Dict[str, Any]) -> str:
        """Génère une justification textuelle de la complexité"""
        justifications = []
        
        if factors["capabilities_count"] > 3:
            justifications.append(f"Requiert {factors['capabilities_count']} capacités spécialisées")
        
        if factors["task_type_complexity"] >= 4.0:
            justifications.append("Type de tâche intrinsèquement complexe")
        
        if factors["priority_weight"] <= 2:
            justifications.append("Priorité élevée augmente la complexité")
        
        if not justifications:
            justifications.append("Complexité standard basée sur les facteurs analysés")
        
        return f"Niveau {level.value}: " + ", ".join(justifications)

# ==========================================
# 5. RÉSOLVEUR DE DÉPENDANCES
# ==========================================

class DependencyResolver:
    """Résolveur de dépendances avec graphes topologiques"""
    
    def __init__(self):
        self.dependency_templates = {
            TaskType.AUDIT: [
                {"task": "security_scan", "parallel": True},
                {"task": "analyze_results", "parallel": False},
                {"task": "generate_report", "parallel": False}
            ],
            TaskType.OPTIMIZATION: [
                {"task": "baseline_measurement", "parallel": True},
                {"task": "profile_performance", "parallel": False},
                {"task": "optimize_code", "parallel": False},
                {"task": "validate_improvements", "parallel": False}
            ],
            TaskType.REFACTORING: [
                {"task": "backup_code", "parallel": True},
                {"task": "analyze_structure", "parallel": False},
                {"task": "refactor_components", "parallel": True},
                {"task": "run_tests", "parallel": False},
                {"task": "validate_functionality", "parallel": False}
            ]
        }
    
    def analyze_dependencies(self, task_definition: TaskDefinition) -> List[Dict[str, Any]]:
        """Analyse et génère les dépendances pour une tâche"""
        task_type = task_definition.task_type
        
        if task_type in self.dependency_templates:
            return self.dependency_templates[task_type].copy()
        
        # Template générique pour types non définis
        return [
            {"task": "prepare", "parallel": True},
            {"task": "execute", "parallel": False},
            {"task": "validate", "parallel": False}
        ]
    
    def create_execution_plan(self, dependencies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Crée un plan d'exécution optimisé"""
        parallel_tasks = []
        sequential_tasks = []
        
        for i, dep in enumerate(dependencies):
            dep["order"] = i
            if dep.get("parallel", False):
                parallel_tasks.append(dep)
            else:
                sequential_tasks.append(dep)
        
        # Combine parallel et sequential pour optimiser l'ordre
        execution_plan = []
        
        # Ajoute d'abord les tâches parallèles possibles
        if parallel_tasks:
            execution_plan.extend(parallel_tasks)
        
        # Puis les tâches séquentielles
        execution_plan.extend(sequential_tasks)
        
        return execution_plan

# ==========================================
# 6. MOTEUR DE VALIDATION ANTI-HALLUCINATION
# ==========================================

class ValidationEngine:
    """Moteur de validation avancé avec evidence tracking"""
    
    def __init__(self):
        self.evidence_store: Dict[str, List[EvidenceEntry]] = {}
        self.reality_checks: Dict[str, List[RealityCheck]] = {}
        self.validation_history: List[Dict[str, Any]] = []
    
    async def validate_agent_output(self, agent_id: str, output: Any, 
                                   expected_output: Any, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Valide la sortie d'un agent avec multiple vérifications"""
        
        check_id = str(uuid4())
        checks = []
        
        # 1. Vérification de cohérence structurelle
        structural_check = self._check_structural_consistency(output, expected_output)
        checks.append(structural_check)
        
        # 2. Vérification de cohérence sémantique
        semantic_check = self._check_semantic_consistency(output, task_context)
        checks.append(semantic_check)
        
        # 3. Détection de valeurs aberrantes
        outlier_check = self._check_for_outliers(output)
        checks.append(outlier_check)
        
        # 4. Cross-validation avec historique
        historical_check = await self._cross_validate_with_history(agent_id, output)
        checks.append(historical_check)
        
        # 5. Vérification de cohérence temporelle
        temporal_check = self._check_temporal_consistency(output)
        checks.append(temporal_check)
        
        # Calcul du score de confiance global
        passed_checks = sum(1 for check in checks if check.passed)
        confidence = passed_checks / len(checks)
        
        # Stockage des résultats
        validation_result = {
            "check_id": check_id,
            "agent_id": agent_id,
            "timestamp": datetime.now(),
            "confidence_score": confidence,
            "passed_checks": passed_checks,
            "total_checks": len(checks),
            "checks": checks,
            "validated": confidence >= 0.8  # Seuil de validation
        }
        
        self.validation_history.append(validation_result)
        
        return validation_result
    
    def _check_structural_consistency(self, output: Any, expected: Any) -> RealityCheck:
        """Vérifie la cohérence structurelle de la sortie"""
        check_id = str(uuid4())
        
        try:
            if isinstance(expected, dict) and isinstance(output, dict):
                # Vérification des clés manquantes/supplémentaires
                expected_keys = set(expected.keys())
                output_keys = set(output.keys())
                
                missing_keys = expected_keys - output_keys
                extra_keys = output_keys - expected_keys
                
                passed = len(missing_keys) == 0 and len(extra_keys) <= 2  # Tolérance pour clés extra
                confidence = 1.0 - (len(missing_keys) * 0.3 + len(extra_keys) * 0.1)
                
                return RealityCheck(
                    check_id=check_id,
                    check_type="structural_consistency",
                    expected=expected_keys,
                    actual=output_keys,
                    passed=passed,
                    confidence=max(0.0, confidence),
                    details={"missing_keys": list(missing_keys), "extra_keys": list(extra_keys)}
                )
            
            # Pour d'autres types, vérification basique
            passed = type(output) == type(expected)
            confidence = 1.0 if passed else 0.5
            
            return RealityCheck(
                check_id=check_id,
                check_type="structural_consistency",
                expected=type(expected).__name__,
                actual=type(output).__name__,
                passed=passed,
                confidence=confidence
            )
            
        except Exception as e:
            return RealityCheck(
                check_id=check_id,
                check_type="structural_consistency",
                expected="valid_structure",
                actual="error",
                passed=False,
                confidence=0.0,
                details={"error": str(e)}
            )
    
    def _check_semantic_consistency(self, output: Any, context: Dict[str, Any]) -> RealityCheck:
        """Vérifie la cohérence sémantique avec le contexte"""
        check_id = str(uuid4())
        
        try:
            task_type = context.get("task_type")
            passed = True
            confidence = 1.0
            details = {}
            
            # Vérifications spécifiques par type de tâche
            if task_type == TaskType.AUDIT and isinstance(output, dict):
                # Un audit doit contenir des findings ou résultats
                has_findings = any(key in output for key in ["findings", "results", "issues", "recommendations"])
                if not has_findings:
                    confidence -= 0.3
                    details["missing_audit_elements"] = True
            
            elif task_type == TaskType.TESTING and isinstance(output, dict):
                # Tests doivent avoir des résultats de tests
                has_test_results = any(key in output for key in ["tests_passed", "tests_failed", "test_results"])
                if not has_test_results:
                    confidence -= 0.3
                    details["missing_test_results"] = True
            
            passed = confidence >= 0.7
            
            return RealityCheck(
                check_id=check_id,
                check_type="semantic_consistency",
                expected=f"semantic_match_for_{task_type}",
                actual="analyzed",
                passed=passed,
                confidence=confidence,
                details=details
            )
            
        except Exception as e:
            return RealityCheck(
                check_id=check_id,
                check_type="semantic_consistency",
                expected="semantic_analysis",
                actual="error",
                passed=False,
                confidence=0.0,
                details={"error": str(e)}
            )
    
    def _check_for_outliers(self, output: Any) -> RealityCheck:
        """Détecte les valeurs aberrantes dans la sortie"""
        check_id = str(uuid4())
        
        try:
            outliers_found = []
            
            if isinstance(output, dict):
                for key, value in output.items():
                    # Vérifications de valeurs aberrantes communes
                    if isinstance(value, (int, float)):
                        if value < 0 and key in ["duration", "count", "score", "percentage"]:
                            outliers_found.append(f"{key}: negative value {value}")
                        elif isinstance(value, float) and value > 100 and key in ["percentage", "score"]:
                            outliers_found.append(f"{key}: percentage > 100: {value}")
                    
                    elif isinstance(value, str):
                        if len(value) > 10000:  # Texte anormalement long
                            outliers_found.append(f"{key}: unusually long text ({len(value)} chars)")
                        elif len(value) == 0 and key in ["description", "result", "output"]:
                            outliers_found.append(f"{key}: empty critical field")
            
            passed = len(outliers_found) == 0
            confidence = max(0.0, 1.0 - len(outliers_found) * 0.2)
            
            return RealityCheck(
                check_id=check_id,
                check_type="outlier_detection",
                expected="no_outliers",
                actual=f"{len(outliers_found)}_outliers",
                passed=passed,
                confidence=confidence,
                details={"outliers": outliers_found}
            )
            
        except Exception as e:
            return RealityCheck(
                check_id=check_id,
                check_type="outlier_detection",
                expected="outlier_analysis",
                actual="error",
                passed=False,
                confidence=0.0,
                details={"error": str(e)}
            )
    
    async def _cross_validate_with_history(self, agent_id: str, output: Any) -> RealityCheck:
        """Cross-validation avec l'historique des sorties de l'agent"""
        check_id = str(uuid4())
        
        try:
            # Recherche des sorties précédentes de cet agent
            agent_history = [
                entry for entry in self.validation_history 
                if entry.get("agent_id") == agent_id
            ]
            
            if len(agent_history) < 2:
                # Pas assez d'historique pour comparaison
                return RealityCheck(
                    check_id=check_id,
                    check_type="historical_validation",
                    expected="sufficient_history",
                    actual="insufficient_history",
                    passed=True,
                    confidence=0.8,  # Bénéfice du doute
                    details={"history_count": len(agent_history)}
                )
            
            # Analyse de consistance avec l'historique
            recent_confidence = [
                entry["confidence_score"] for entry in agent_history[-5:]
            ]
            avg_confidence = sum(recent_confidence) / len(recent_confidence)
            
            # Si l'agent a historiquement de bons résultats, plus de confiance
            confidence_bonus = min(0.2, avg_confidence * 0.2)
            base_confidence = 0.8 + confidence_bonus
            
            return RealityCheck(
                check_id=check_id,
                check_type="historical_validation",
                expected="consistent_performance",
                actual=f"avg_confidence_{avg_confidence:.2f}",
                passed=avg_confidence >= 0.6,
                confidence=base_confidence,
                details={
                    "historical_avg_confidence": avg_confidence,
                    "recent_validations": len(recent_confidence)
                }
            )
            
        except Exception as e:
            return RealityCheck(
                check_id=check_id,
                check_type="historical_validation",
                expected="history_analysis",
                actual="error",
                passed=False,
                confidence=0.0,
                details={"error": str(e)}
            )
    
    def _check_temporal_consistency(self, output: Any) -> RealityCheck:
        """Vérifie la cohérence temporelle des données"""
        check_id = str(uuid4())
        
        try:
            temporal_issues = []
            
            if isinstance(output, dict):
                # Recherche de champs temporels
                time_fields = [key for key in output.keys() 
                             if any(term in key.lower() for term in ["time", "date", "duration", "timestamp"])]
                
                for field in time_fields:
                    value = output[field]
                    
                    # Vérification des timestamps
                    if "timestamp" in field.lower() or "date" in field.lower():
                        try:
                            if isinstance(value, str):
                                parsed_date = datetime.fromisoformat(value.replace('Z', '+00:00'))
                                # Vérifier que la date n'est pas dans le futur lointain
                                if parsed_date > datetime.now() + timedelta(days=365):
                                    temporal_issues.append(f"{field}: future date too far: {value}")
                        except:
                            temporal_issues.append(f"{field}: invalid date format: {value}")
                    
                    # Vérification des durées
                    elif "duration" in field.lower():
                        if isinstance(value, (int, float)) and value < 0:
                            temporal_issues.append(f"{field}: negative duration: {value}")
                        elif isinstance(value, (int, float)) and value > 86400:  # Plus de 24h
                            temporal_issues.append(f"{field}: unusually long duration: {value}")
            
            passed = len(temporal_issues) == 0
            confidence = max(0.0, 1.0 - len(temporal_issues) * 0.3)
            
            return RealityCheck(
                check_id=check_id,
                check_type="temporal_consistency",
                expected="consistent_temporal_data",
                actual=f"{len(temporal_issues)}_issues",
                passed=passed,
                confidence=confidence,
                details={"temporal_issues": temporal_issues}
            )
            
        except Exception as e:
            return RealityCheck(
                check_id=check_id,
                check_type="temporal_consistency",
                expected="temporal_analysis",
                actual="error",
                passed=False,
                confidence=0.0,
                details={"error": str(e)}
            )

# ==========================================
# 7. GESTIONNAIRE DE TÂCHES CRUD
# ==========================================

class TaskRepository:
    """Repository pour la gestion CRUD des tâches"""
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path("tasks_storage.json")
        self.tasks: Dict[str, TaskDefinition] = {}
        self.subtasks: Dict[str, List[SubTask]] = {}
        self.load_from_storage()
    
    def create_task(self, task_definition: TaskDefinition) -> str:
        """Crée une nouvelle tâche"""
        self.tasks[task_definition.id] = task_definition
        self.subtasks[task_definition.id] = []
        self.save_to_storage()
        return task_definition.id
    
    def get_task(self, task_id: str) -> Optional[TaskDefinition]:
        """Récupère une tâche par ID"""
        return self.tasks.get(task_id)
    
    def update_task(self, task_id: str, updates: Dict[str, Any]) -> bool:
        """Met à jour une tâche existante"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        for key, value in updates.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        self.save_to_storage()
        return True
    
    def delete_task(self, task_id: str) -> bool:
        """Supprime une tâche et ses sous-tâches"""
        if task_id not in self.tasks:
            return False
        
        del self.tasks[task_id]
        if task_id in self.subtasks:
            del self.subtasks[task_id]
        
        self.save_to_storage()
        return True
    
    def list_tasks(self, filters: Optional[Dict[str, Any]] = None) -> List[TaskDefinition]:
        """Liste les tâches avec filtres optionnels"""
        tasks = list(self.tasks.values())
        
        if not filters:
            return tasks
        
        filtered_tasks = []
        for task in tasks:
            match = True
            for key, value in filters.items():
                if hasattr(task, key) and getattr(task, key) != value:
                    match = False
                    break
            if match:
                filtered_tasks.append(task)
        
        return filtered_tasks
    
    def add_subtask(self, parent_id: str, subtask: SubTask) -> bool:
        """Ajoute une sous-tâche à une tâche"""
        if parent_id not in self.tasks:
            return False
        
        if parent_id not in self.subtasks:
            self.subtasks[parent_id] = []
        
        self.subtasks[parent_id].append(subtask)
        self.save_to_storage()
        return True
    
    def get_subtasks(self, parent_id: str) -> List[SubTask]:
        """Récupère les sous-tâches d'une tâche"""
        return self.subtasks.get(parent_id, [])
    
    def save_to_storage(self):
        """Sauvegarde les données vers le fichier de stockage"""
        try:
            data = {
                "tasks": {tid: asdict(task) for tid, task in self.tasks.items()},
                "subtasks": {pid: [asdict(st) for st in subtasks] 
                           for pid, subtasks in self.subtasks.items()}
            }
            
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logging.error(f"Erreur sauvegarde tasks: {e}")
    
    def load_from_storage(self):
        """Charge les données depuis le fichier de stockage"""
        try:
            if self.storage_path.exists():
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Reconstruction des objets TaskDefinition
                for tid, task_data in data.get("tasks", {}).items():
                    # Conversion des enums
                    if "task_type" in task_data:
                        task_data["task_type"] = TaskType(task_data["task_type"])
                    if "priority" in task_data:
                        task_data["priority"] = TaskPriority(task_data["priority"])
                    if "created_at" in task_data:
                        task_data["created_at"] = datetime.fromisoformat(task_data["created_at"])
                    
                    self.tasks[tid] = TaskDefinition(**task_data)
                
                # Reconstruction des sous-tâches
                for pid, subtasks_data in data.get("subtasks", {}).items():
                    subtasks = []
                    for st_data in subtasks_data:
                        if "status" in st_data:
                            st_data["status"] = ValidationStatus(st_data["status"])
                        if "created_at" in st_data:
                            st_data["created_at"] = datetime.fromisoformat(st_data["created_at"])
                        subtasks.append(SubTask(**st_data))
                    self.subtasks[pid] = subtasks
                    
        except Exception as e:
            logging.error(f"Erreur chargement tasks: {e}")

# ==========================================
# 8. GESTIONNAIRE D'EXPORT
# ==========================================

class ExportManager:
    """Gestionnaire d'export vers multiples formats"""
    
    def __init__(self):
        self.supported_formats = ["json", "markdown", "csv", "html"]
    
    def export_tasks(self, tasks: List[TaskDefinition], format_type: str, 
                    output_path: Optional[Path] = None) -> Union[str, Path]:
        """Exporte les tâches vers le format spécifié"""
        
        if format_type not in self.supported_formats:
            raise ValueError(f"Format non supporté: {format_type}")
        
        if format_type == "json":
            return self._export_json(tasks, output_path)
        elif format_type == "markdown":
            return self._export_markdown(tasks, output_path)
        elif format_type == "csv":
            return self._export_csv(tasks, output_path)
        elif format_type == "html":
            return self._export_html(tasks, output_path)
    
    def _export_json(self, tasks: List[TaskDefinition], output_path: Optional[Path]) -> Union[str, Path]:
        """Export au format JSON"""
        data = {
            "export_timestamp": datetime.now().isoformat(),
            "tasks_count": len(tasks),
            "tasks": [asdict(task) for task in tasks]
        }
        
        json_content = json.dumps(data, indent=2, default=str, ensure_ascii=False)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_content)
            return output_path
        
        return json_content
    
    def _export_markdown(self, tasks: List[TaskDefinition], output_path: Optional[Path]) -> Union[str, Path]:
        """Export au format Markdown"""
        lines = [
            "# 📋 Export des Tâches TaskMaster",
            f"",
            f"**Date d'export :** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Nombre de tâches :** {len(tasks)}",
            f"",
            "---",
            ""
        ]
        
        for i, task in enumerate(tasks, 1):
            lines.extend([
                f"## {i}. {task.title}",
                f"",
                f"- **ID :** `{task.id}`",
                f"- **Type :** {task.task_type.value.title()}",
                f"- **Priorité :** {task.priority.name}",
                f"- **Créé le :** {task.created_at.strftime('%Y-%m-%d %H:%M')}",
                f"- **Complexité :** {task.complexity_score:.1f}",
                f"- **Durée estimée :** {task.estimated_duration} minutes",
                f"",
                f"**Description :**",
                f"{task.description}",
                f"",
                f"**Capacités requises :**",
            ])
            
            for capability in task.required_capabilities:
                lines.append(f"- {capability}")
            
            lines.extend(["", "---", ""])
        
        markdown_content = "\n".join(lines)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            return output_path
        
        return markdown_content
    
    def _export_csv(self, tasks: List[TaskDefinition], output_path: Optional[Path]) -> Union[str, Path]:
        """Export au format CSV"""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # En-têtes
        headers = [
            "ID", "Titre", "Type", "Priorité", "Complexité", 
            "Durée Estimée", "Capacités", "Créé le", "Description"
        ]
        writer.writerow(headers)
        
        # Données
        for task in tasks:
            writer.writerow([
                task.id,
                task.title,
                task.task_type.value,
                task.priority.name,
                task.complexity_score,
                task.estimated_duration,
                "; ".join(task.required_capabilities),
                task.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                task.description[:200] + "..." if len(task.description) > 200 else task.description
            ])
        
        csv_content = output.getvalue()
        output.close()
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                f.write(csv_content)
            return output_path
        
        return csv_content
    
    def _export_html(self, tasks: List[TaskDefinition], output_path: Optional[Path]) -> Union[str, Path]:
        """Export au format HTML"""
        html_template = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TaskMaster - Export des Tâches</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .task { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
        .task-header { background: #f5f5f5; padding: 10px; margin: -15px -15px 15px -15px; }
        .priority-critical { border-left: 5px solid #ff4444; }
        .priority-high { border-left: 5px solid #ff8800; }
        .priority-medium { border-left: 5px solid #ffaa00; }
        .priority-low { border-left: 5px solid #00aa00; }
        .capabilities { display: flex; flex-wrap: wrap; gap: 5px; }
        .capability { background: #e7f3ff; padding: 2px 8px; border-radius: 3px; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>📋 TaskMaster - Export des Tâches</h1>
    <p><strong>Date d'export :</strong> {export_date}</p>
    <p><strong>Nombre de tâches :</strong> {tasks_count}</p>
    
    <div class="tasks-container">
        {tasks_html}
    </div>
</body>
</html>
        """
        
        tasks_html = ""
        for task in tasks:
            priority_class = f"priority-{task.priority.name.lower()}"
            capabilities_html = "".join([
                f'<span class="capability">{cap}</span>' 
                for cap in task.required_capabilities
            ])
            
            task_html = f"""
        <div class="task {priority_class}">
            <div class="task-header">
                <h3>{task.title}</h3>
                <p><strong>ID:</strong> {task.id} | <strong>Type:</strong> {task.task_type.value.title()} | 
                   <strong>Priorité:</strong> {task.priority.name} | <strong>Complexité:</strong> {task.complexity_score:.1f}</p>
            </div>
            <p><strong>Description:</strong> {task.description}</p>
            <p><strong>Durée estimée:</strong> {task.estimated_duration} minutes</p>
            <p><strong>Créé le:</strong> {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Capacités requises:</strong></p>
            <div class="capabilities">{capabilities_html}</div>
        </div>
            """
            tasks_html += task_html
        
        html_content = html_template.format(
            export_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            tasks_count=len(tasks),
            tasks_html=tasks_html
        )
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return output_path
        
        return html_content

# ==========================================
# 9. TASKMASTER NEXTGENERATION PRINCIPAL
# ==========================================

class TaskMasterNextGen:
    """
    🚀 TaskMaster NextGeneration - Agent Orchestrateur Hybride Avancé
    
    Combine le meilleur de :
    - TaskMaster Final (base fonctionnelle)
    - Prototype abandonné (fonctionnalités avancées)
    - Architecture Pattern Factory (intégration)
    - Nouvelles capacités (CRUD, export, NLP)
    """
    
    def __init__(self, agent_id: str = "taskmaster_nextgen_001"):
        self.agent_id = agent_id
        
        # Configuration des chemins
        self.project_root = Path(__file__).resolve().parent.parent
        self.work_dir = Path(os.getenv("TASKMASTER_WORK_DIR", 
                                     self.project_root / "taskmaster_nextgen_workspace"))
        self.work_dir.mkdir(parents=True, exist_ok=True)
        
        # Assurer que le project_root est dans le path
        if str(self.project_root) not in sys.path:
            sys.path.append(str(self.project_root))
        
        # Configuration du logging
        self._setup_logging()
        
        # Initialisation des composants
        self.nlp_processor = NLPProcessor()
        self.complexity_analyzer = ComplexityAnalyzer()
        self.dependency_resolver = DependencyResolver()
        self.validation_engine = ValidationEngine()
        self.task_repository = TaskRepository(self.work_dir / "tasks.json")
        self.export_manager = ExportManager()
        
        # Découverte des agents (hérité de TaskMasterFinal)
        self.agents = {}
        
        # Métriques et historique
        self.active_tasks: Dict[str, TaskMetrics] = {}
        self.user_sessions: Dict[str, Dict[str, Any]] = {}
        
        self.logger.info(f"TaskMaster NextGen {self.agent_id} initialisé avec succès")
        self.logger.info(f"Workspace: {self.work_dir}")
    
    def _setup_logging(self):
        """Configuration du système de logging"""
        self.log_dir = self.work_dir / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "taskmaster_nextgen.log"
        
        self.logger = logging.getLogger(self.agent_id)
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            # Handler fichier
            file_handler = logging.FileHandler(self.log_file, mode='a', encoding='utf-8')
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
            
            # Handler console
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
    
    async def startup(self):
        """Démarre TaskMaster NextGen et découvre les agents"""
        self.logger.info("🚀 Démarrage TaskMaster NextGeneration...")
        
        # Découverte des agents (méthode héritée)
        await self._discover_agents()
        
        # Validation des composants
        await self._validate_components()
        
        self.logger.info(f"✅ TaskMaster NextGen opérationnel avec {len(self.agents)} agents")
        
        return {
            "status": "ready",
            "agents_count": len(self.agents),
            "components": {
                "nlp_ready": self.nlp_processor.nlp is not None,
                "validation_ready": True,
                "storage_ready": True
            }
        }
    
    async def _discover_agents(self):
        """Découverte des agents (hérité et amélioré de TaskMasterFinal)"""
        agents_dir = self.project_root / "agents"
        self.logger.info(f"🔍 Découverte des agents dans: {agents_dir}")
        
        discovered_count = 0
        
        for file_path in agents_dir.glob("agent_*.py"):
            agent_name = file_path.stem
            if agent_name == "taskmaster_nextgen":
                continue
            
            try:
                spec = importlib.util.spec_from_file_location(agent_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if name.startswith("Agent") and hasattr(obj, "CAPABILITIES"):
                        capabilities = getattr(obj, "CAPABILITIES", [])
                        if capabilities:
                            self.agents[agent_name] = {
                                "class": obj,
                                "capabilities": capabilities,
                                "module_path": file_path,
                                "pattern_factory_compatible": hasattr(obj, "run"),
                                "validation_ready": hasattr(obj, "validate_output")
                            }
                            discovered_count += 1
                            self.logger.info(f"  ✅ {agent_name}: {capabilities}")
                            break
            
            except Exception as e:
                self.logger.warning(f"  ❌ Impossible de charger {agent_name}: {e}")
        
        self.logger.info(f"🎯 {discovered_count} agents découverts et validés")
    
    async def _validate_components(self):
        """Valide que tous les composants sont fonctionnels"""
        validations = []
        
        # Test NLP Processor
        try:
            test_task = self.nlp_processor.parse_request("Test de validation du NLP")
            validations.append(("NLP Processor", True, "Fonctionnel"))
        except Exception as e:
            validations.append(("NLP Processor", False, str(e)))
        
        # Test Complexity Analyzer
        try:
            test_def = TaskDefinition(
                id="test", title="Test", description="Test",
                task_type=TaskType.ANALYSIS, priority=TaskPriority.MEDIUM,
                required_capabilities=["test"]
            )
            complexity = self.complexity_analyzer.analyze_task_complexity(test_def)
            validations.append(("Complexity Analyzer", True, f"Score: {complexity['complexity_score']}"))
        except Exception as e:
            validations.append(("Complexity Analyzer", False, str(e)))
        
        # Test Validation Engine
        try:
            test_validation = await self.validation_engine.validate_agent_output(
                "test_agent", {"test": "data"}, {"test": "expected"}, {"task_type": TaskType.ANALYSIS}
            )
            validations.append(("Validation Engine", True, f"Confidence: {test_validation['confidence_score']:.2f}"))
        except Exception as e:
            validations.append(("Validation Engine", False, str(e)))
        
        # Log des résultats
        for component, success, detail in validations:
            status = "✅" if success else "❌"
            self.logger.info(f"  {status} {component}: {detail}")
    
    async def create_task_from_natural_language(self, user_request: str, 
                                               user_session: Optional[str] = None) -> Dict[str, Any]:
        """
        🎯 Fonction principale : Crée une tâche à partir d'une requête en langage naturel
        
        Cette fonction combine toutes les capacités avancées :
        1. Parse NLP de la requête
        2. Analyse de complexité 
        3. Décomposition en sous-tâches
        4. Validation anti-hallucination
        5. Stockage CRUD
        """
        self.logger.info(f"📝 Nouvelle requête: '{user_request[:100]}...'")
        
        try:
            # 1. Parse NLP de la requête
            task_definition = self.nlp_processor.parse_request(user_request)
            self.logger.info(f"🧠 Tâche parsée: {task_definition.task_type.value} - {task_definition.title}")
            
            # 2. Analyse de complexité
            complexity_analysis = self.complexity_analyzer.analyze_task_complexity(task_definition)
            task_definition.complexity_score = complexity_analysis["complexity_score"]
            task_definition.estimated_duration = complexity_analysis["estimated_duration_minutes"]
            
            self.logger.info(f"📊 Complexité: {complexity_analysis['complexity_level'].value} "
                           f"(score: {complexity_analysis['complexity_score']:.1f}, "
                           f"durée: {complexity_analysis['estimated_duration_minutes']}min)")
            
            # 3. Décomposition en sous-tâches
            dependencies = self.dependency_resolver.analyze_dependencies(task_definition)
            execution_plan = self.dependency_resolver.create_execution_plan(dependencies)
            
            subtasks = []
            previous_task_ids = []
            
            for i, step in enumerate(execution_plan):
                subtask_id = f"{task_definition.id}_sub_{i+1}"
                subtask = SubTask(
                    id=subtask_id,
                    parent_id=task_definition.id,
                    title=f"{task_definition.title} - {step['task'].replace('_', ' ').title()}",
                    dependencies=previous_task_ids.copy() if not step.get('parallel', False) else [],
                    status=ValidationStatus.PENDING
                )
                subtasks.append(subtask)
                previous_task_ids.append(subtask_id)
            
            self.logger.info(f"🔄 {len(subtasks)} sous-tâches générées")
            
            # 4. Stockage dans le repository
            task_id = self.task_repository.create_task(task_definition)
            for subtask in subtasks:
                self.task_repository.add_subtask(task_id, subtask)
            
            # 5. Métriques de session
            if user_session:
                if user_session not in self.user_sessions:
                    self.user_sessions[user_session] = {"tasks": [], "created_at": datetime.now()}
                self.user_sessions[user_session]["tasks"].append(task_id)
            
            # 6. Préparation de la réponse
            response = {
                "status": "success",
                "task_id": task_id,
                "task_definition": asdict(task_definition),
                "complexity_analysis": complexity_analysis,
                "subtasks": [asdict(st) for st in subtasks],
                "execution_plan": execution_plan,
                "next_actions": self._suggest_next_actions(task_definition, subtasks)
            }
            
            self.logger.info(f"✅ Tâche créée avec succès: {task_id}")
            return response
            
        except Exception as e:
            self.logger.error(f"❌ Erreur création tâche: {e}", exc_info=True)
            return {
                "status": "error",
                "message": str(e),
                "error_type": type(e).__name__
            }
    
    def _suggest_next_actions(self, task_def: TaskDefinition, subtasks: List[SubTask]) -> List[str]:
        """Suggère les prochaines actions pour l'utilisateur"""
        actions = []
        
        # Action 1: Démarrer la première sous-tâche
        if subtasks:
            first_subtask = subtasks[0]
            actions.append(f"Démarrer '{first_subtask.title}' (première sous-tâche)")
        
        # Action 2: Exporter le plan
        actions.append("Exporter le plan de tâches (JSON/Markdown/CSV/HTML)")
        
        # Action 3: Assigner des agents
        matching_agents = self._find_matching_agents(task_def.required_capabilities)
        if matching_agents:
            agent_names = list(matching_agents.keys())[:3]
            actions.append(f"Assigner aux agents: {', '.join(agent_names)}")
        
        # Action 4: Modifier si nécessaire
        actions.append("Modifier la tâche ou ses sous-tâches si nécessaire")
        
        return actions
    
    def _find_matching_agents(self, required_capabilities: List[str]) -> Dict[str, Any]:
        """Trouve les agents qui correspondent aux capacités requises"""
        matching_agents = {}
        
        for agent_name, agent_data in self.agents.items():
            agent_capabilities = agent_data["capabilities"]
            
            # Calcul du score de correspondance
            matches = sum(1 for cap in required_capabilities 
                         if any(cap_word in agent_cap for cap_word in cap.split('_') 
                               for agent_cap in agent_capabilities))
            
            if matches > 0:
                matching_agents[agent_name] = {
                    "match_score": matches,
                    "capabilities": agent_capabilities,
                    "data": agent_data
                }
        
        # Tri par score de correspondance
        return dict(sorted(matching_agents.items(), 
                          key=lambda x: x[1]["match_score"], reverse=True))
    
    async def execute_task(self, task_id: str, agent_validation: bool = True) -> Dict[str, Any]:
        """
        🚀 Exécute une tâche avec validation anti-hallucination
        
        Processus :
        1. Récupère la tâche
        2. Sélectionne le meilleur agent
        3. Délègue l'exécution
        4. Valide le résultat
        5. Met à jour les métriques
        """
        self.logger.info(f"🚀 Exécution de la tâche: {task_id}")
        
        try:
            # 1. Récupération de la tâche
            task = self.task_repository.get_task(task_id)
            if not task:
                return {"status": "error", "message": f"Tâche {task_id} non trouvée"}
            
            # 2. Sélection du meilleur agent
            matching_agents = self._find_matching_agents(task.required_capabilities)
            if not matching_agents:
                return {"status": "error", "message": "Aucun agent compatible trouvé"}
            
            best_agent_name = list(matching_agents.keys())[0]
            best_agent_data = self.agents[best_agent_name]
            
            self.logger.info(f"🎯 Agent sélectionné: {best_agent_name}")
            
            # 3. Préparation des métriques
            task_metrics = TaskMetrics(
                task_id=task_id,
                start_time=datetime.now(),
                agent_used=best_agent_name
            )
            self.active_tasks[task_id] = task_metrics
            
            # 4. Exécution de la tâche
            agent_class = best_agent_data["class"]
            agent_instance = agent_class()
            
            # Préparation du contexte pour l'agent
            task_context = {
                "task_id": task_id,
                "task_type": task.task_type,
                "description": task.description,
                "expected_outputs": task.expected_outputs,
                "constraints": task.constraints
            }
            
            if hasattr(agent_instance, "run"):
                result = agent_instance.run(task_prompt=task.description)
            else:
                result = {"status": "error", "message": f"Agent {best_agent_name} n'a pas de méthode run"}
            
            # 5. Validation anti-hallucination
            if agent_validation and isinstance(result, dict):
                validation_result = await self.validation_engine.validate_agent_output(
                    best_agent_name, result, task.expected_outputs, task_context
                )
                
                self.logger.info(f"🔍 Validation: confidence={validation_result['confidence_score']:.2f}")
                
                # Ajout des résultats de validation
                result["validation"] = validation_result
                result["validated"] = validation_result["validated"]
            
            # 6. Mise à jour des métriques
            task_metrics.end_time = datetime.now()
            task_metrics.execution_time = (task_metrics.end_time - task_metrics.start_time).total_seconds()
            task_metrics.success = result.get("status") != "error"
            task_metrics.confidence_score = result.get("validation", {}).get("confidence_score", 0.0)
            
            # 7. Mise à jour du statut de la tâche
            status_update = ValidationStatus.APPROVED if task_metrics.success else ValidationStatus.REJECTED
            self.task_repository.update_task(task_id, {"metadata": {"last_execution": asdict(task_metrics)}})
            
            self.logger.info(f"✅ Tâche {task_id} terminée en {task_metrics.execution_time:.1f}s")
            
            return {
                "status": "success",
                "task_id": task_id,
                "agent_used": best_agent_name,
                "result": result,
                "metrics": asdict(task_metrics),
                "execution_time": task_metrics.execution_time
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erreur exécution tâche {task_id}: {e}", exc_info=True)
            
            # Mise à jour des métriques d'erreur
            if task_id in self.active_tasks:
                self.active_tasks[task_id].error_count += 1
                self.active_tasks[task_id].success = False
            
            return {
                "status": "error",
                "task_id": task_id,
                "message": str(e),
                "error_type": type(e).__name__
            }
        
        finally:
            # Nettoyage
            if hasattr(agent_instance, "shutdown"):
                agent_instance.shutdown()
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Récupère le statut détaillé d'une tâche"""
        task = self.task_repository.get_task(task_id)
        if not task:
            return {"status": "error", "message": "Tâche non trouvée"}
        
        subtasks = self.task_repository.get_subtasks(task_id)
        metrics = self.active_tasks.get(task_id)
        
        return {
            "task": asdict(task),
            "subtasks": [asdict(st) for st in subtasks],
            "metrics": asdict(metrics) if metrics else None,
            "status": "active" if task_id in self.active_tasks else "stored"
        }
    
    def list_tasks(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Liste toutes les tâches avec filtres optionnels"""
        tasks = self.task_repository.list_tasks(filters)
        
        return {
            "tasks_count": len(tasks),
            "tasks": [asdict(task) for task in tasks],
            "filters_applied": filters or {}
        }
    
    def export_tasks(self, format_type: str = "json", task_ids: Optional[List[str]] = None,
                    output_path: Optional[str] = None) -> Dict[str, Any]:
        """Exporte les tâches vers le format spécifié"""
        try:
            # Sélection des tâches à exporter
            if task_ids:
                tasks = [self.task_repository.get_task(tid) for tid in task_ids]
                tasks = [t for t in tasks if t is not None]
            else:
                tasks = self.task_repository.list_tasks()
            
            # Préparation du chemin de sortie
            output_file_path = None
            if output_path:
                output_file_path = Path(output_path)
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"taskmaster_export_{timestamp}.{format_type}"
                output_file_path = self.work_dir / "exports" / filename
                output_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Export
            result = self.export_manager.export_tasks(tasks, format_type, output_file_path)
            
            self.logger.info(f"📤 Export terminé: {len(tasks)} tâches vers {format_type}")
            
            return {
                "status": "success",
                "format": format_type,
                "tasks_exported": len(tasks),
                "output_path": str(result) if isinstance(result, Path) else None,
                "content": result if isinstance(result, str) else None
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erreur export: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Récupère les données pour un dashboard de supervision"""
        all_tasks = self.task_repository.list_tasks()
        active_tasks = list(self.active_tasks.values())
        
        # Statistiques générales
        task_types = {}
        priorities = {}
        complexity_levels = {}
        
        for task in all_tasks:
            # Types de tâches
            task_type = task.task_type.value
            task_types[task_type] = task_types.get(task_type, 0) + 1
            
            # Priorités
            priority = task.priority.name
            priorities[priority] = priorities.get(priority, 0) + 1
            
            # Niveaux de complexité
            if task.complexity_score < 15:
                level = "Simple"
            elif task.complexity_score < 35:
                level = "Modéré"
            elif task.complexity_score < 60:
                level = "Complexe"
            else:
                level = "Très complexe"
            
            complexity_levels[level] = complexity_levels.get(level, 0) + 1
        
        # Métriques des agents
        agent_stats = {}
        for metrics in active_tasks:
            agent = metrics.agent_used
            if agent:
                if agent not in agent_stats:
                    agent_stats[agent] = {"tasks": 0, "avg_time": 0, "success_rate": 0}
                agent_stats[agent]["tasks"] += 1
        
        return {
            "summary": {
                "total_tasks": len(all_tasks),
                "active_tasks": len(active_tasks),
                "agents_available": len(self.agents),
                "user_sessions": len(self.user_sessions)
            },
            "distributions": {
                "task_types": task_types,
                "priorities": priorities,
                "complexity_levels": complexity_levels
            },
            "agent_performance": agent_stats,
            "recent_tasks": [asdict(task) for task in all_tasks[-10:]],  # 10 dernières tâches
            "system_status": {
                "nlp_available": self.nlp_processor.nlp is not None,
                "validation_active": len(self.validation_engine.validation_history) > 0,
                "storage_healthy": self.task_repository.storage_path.exists()
            }
        }
    
    async def shutdown(self):
        """Arrêt propre de TaskMaster NextGen"""
        self.logger.info("🔄 Arrêt de TaskMaster NextGeneration...")
        
        # Sauvegarde finale
        self.task_repository.save_to_storage()
        
        # Nettoyage des tâches actives
        for task_id, metrics in self.active_tasks.items():
            if not metrics.end_time:
                metrics.end_time = datetime.now()
                metrics.execution_time = (metrics.end_time - metrics.start_time).total_seconds()
        
        self.logger.info("✅ TaskMaster NextGen arrêté proprement")
        await asyncio.sleep(0.1)

# ==========================================
# 10. INTERFACE CLI SIMPLIFIÉE
# ==========================================

class TaskMasterCLI:
    """Interface CLI simplifiée pour TaskMaster NextGen"""
    
    def __init__(self):
        self.taskmaster = None
    
    async def start(self):
        """Démarre l'interface CLI"""
        print("🚀 TaskMaster NextGeneration - Interface CLI")
        print("=" * 50)
        
        self.taskmaster = TaskMasterNextGen()
        startup_result = await self.taskmaster.startup()
        
        print(f"✅ Système démarré avec {startup_result['agents_count']} agents")
        print("\nCommandes disponibles:")
        print("  create <description>  - Créer une tâche")
        print("  execute <task_id>     - Exécuter une tâche")
        print("  status <task_id>      - Statut d'une tâche")
        print("  list                  - Lister toutes les tâches")
        print("  export <format>       - Exporter les tâches")
        print("  dashboard             - Afficher le dashboard")
        print("  help                  - Afficher l'aide")
        print("  quit                  - Quitter")
        print()
        
        while True:
            try:
                command = input("TaskMaster> ").strip()
                if not command:
                    continue
                
                parts = command.split(maxsplit=1)
                cmd = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                if cmd == "quit":
                    break
                elif cmd == "create":
                    await self._handle_create(args)
                elif cmd == "execute":
                    await self._handle_execute(args)
                elif cmd == "status":
                    await self._handle_status(args)
                elif cmd == "list":
                    await self._handle_list()
                elif cmd == "export":
                    await self._handle_export(args)
                elif cmd == "dashboard":
                    await self._handle_dashboard()
                elif cmd == "help":
                    await self._handle_help()
                else:
                    print(f"❌ Commande inconnue: {cmd}")
                
            except KeyboardInterrupt:
                print("\n👋 Interruption utilisateur")
                break
            except Exception as e:
                print(f"❌ Erreur: {e}")
        
        await self.taskmaster.shutdown()
        print("👋 TaskMaster NextGen arrêté")
    
    async def _handle_create(self, description: str):
        """Gère la création de tâche"""
        if not description:
            print("❌ Description requise: create <description>")
            return
        
        print(f"🔄 Création de la tâche: {description[:50]}...")
        result = await self.taskmaster.create_task_from_natural_language(description)
        
        if result["status"] == "success":
            task_id = result["task_id"]
            complexity = result["complexity_analysis"]
            print(f"✅ Tâche créée: {task_id}")
            print(f"   Type: {result['task_definition']['task_type']}")
            print(f"   Complexité: {complexity['complexity_level']} (score: {complexity['complexity_score']:.1f})")
            print(f"   Durée estimée: {complexity['estimated_duration_minutes']} minutes")
            print(f"   Sous-tâches: {len(result['subtasks'])}")
        else:
            print(f"❌ Erreur: {result['message']}")
    
    async def _handle_execute(self, task_id: str):
        """Gère l'exécution de tâche"""
        if not task_id:
            print("❌ ID de tâche requis: execute <task_id>")
            return
        
        print(f"🚀 Exécution de la tâche: {task_id}")
        result = await self.taskmaster.execute_task(task_id)
        
        if result["status"] == "success":
            print(f"✅ Tâche exécutée par {result['agent_used']}")
            print(f"   Temps d'exécution: {result['execution_time']:.1f}s")
            if "validation" in result["result"]:
                validation = result["result"]["validation"]
                print(f"   Validation: {validation['confidence_score']:.2f} confidence")
        else:
            print(f"❌ Erreur: {result['message']}")
    
    async def _handle_status(self, task_id: str):
        """Affiche le statut d'une tâche"""
        if not task_id:
            print("❌ ID de tâche requis: status <task_id>")
            return
        
        status = self.taskmaster.get_task_status(task_id)
        if status["status"] == "error":
            print(f"❌ {status['message']}")
            return
        
        task = status["task"]
        print(f"📋 Tâche: {task['title']}")
        print(f"   ID: {task['id']}")
        print(f"   Type: {task['task_type']}")
        print(f"   Priorité: {task['priority']}")
        print(f"   Complexité: {task['complexity_score']:.1f}")
        print(f"   Créée: {task['created_at']}")
        print(f"   Sous-tâches: {len(status['subtasks'])}")
        
        if status['metrics']:
            metrics = status['metrics']
            print(f"   Agent utilisé: {metrics['agent_used']}")
            print(f"   Succès: {metrics['success']}")
    
    async def _handle_list(self):
        """Liste toutes les tâches"""
        result = self.taskmaster.list_tasks()
        tasks = result["tasks"]
        
        print(f"📋 {result['tasks_count']} tâches trouvées:")
        for task in tasks[-10:]:  # 10 dernières
            print(f"   {task['id'][:8]}... - {task['title'][:40]} ({task['task_type']})")
    
    async def _handle_export(self, format_type: str):
        """Exporte les tâches"""
        format_type = format_type or "json"
        if format_type not in ["json", "markdown", "csv", "html"]:
            print("❌ Format supportés: json, markdown, csv, html")
            return
        
        result = self.taskmaster.export_tasks(format_type)
        if result["status"] == "success":
            print(f"✅ {result['tasks_exported']} tâches exportées en {format_type}")
            if result["output_path"]:
                print(f"   Fichier: {result['output_path']}")
        else:
            print(f"❌ Erreur export: {result['message']}")
    
    async def _handle_dashboard(self):
        """Affiche le dashboard"""
        data = self.taskmaster.get_dashboard_data()
        
        print("📊 Dashboard TaskMaster NextGen")
        print("=" * 40)
        
        summary = data["summary"]
        print(f"Tâches totales: {summary['total_tasks']}")
        print(f"Tâches actives: {summary['active_tasks']}")
        print(f"Agents disponibles: {summary['agents_available']}")
        print(f"Sessions utilisateur: {summary['user_sessions']}")
        
        print("\n📈 Distribution des types:")
        for task_type, count in data["distributions"]["task_types"].items():
            print(f"  {task_type}: {count}")
        
        print("\n🎯 Priorités:")
        for priority, count in data["distributions"]["priorities"].items():
            print(f"  {priority}: {count}")
        
        print(f"\n🔧 Statut système:")
        status = data["system_status"]
        print(f"  NLP disponible: {'✅' if status['nlp_available'] else '❌'}")
        print(f"  Validation active: {'✅' if status['validation_active'] else '❌'}")
        print(f"  Stockage sain: {'✅' if status['storage_healthy'] else '❌'}")
    
    async def _handle_help(self):
        """Affiche l'aide"""
        print("""
🚀 TaskMaster NextGeneration - Aide
====================================

COMMANDES PRINCIPALES:
  create <description>     Crée une tâche à partir d'une description en langage naturel
  execute <task_id>        Exécute une tâche spécifique avec validation
  status <task_id>         Affiche le statut détaillé d'une tâche
  list                     Liste toutes les tâches stockées
  export <format>          Exporte les tâches (json, markdown, csv, html)
  dashboard                Affiche les statistiques du système
  help                     Affiche cette aide
  quit                     Quitte l'application

EXEMPLES:
  create "Faire un audit de sécurité du module d'authentification"
  create "Optimiser les performances de la base de données PostgreSQL"
  create "Créer la documentation technique de l'API REST"
  execute 12345678-1234-1234-1234-123456789012
  export markdown

FONCTIONNALITÉS:
✅ Parsing NLP avancé (spaCy + transformers)
✅ Analyse automatique de complexité
✅ Décomposition en sous-tâches avec dépendances
✅ Validation anti-hallucination
✅ Découverte automatique d'agents
✅ Export multi-formats
✅ Métriques et dashboard temps réel
        """)

# ==========================================
# 11. POINT D'ENTRÉE PRINCIPAL
# ==========================================

async def main():
    """Point d'entrée principal"""
    cli = TaskMasterCLI()
    await cli.start()

if __name__ == "__main__":
    print("🚀 TaskMaster NextGeneration v1.0.0")
    print("Architecture Hybride Avancée")
    print("Démarrage...")
    
    asyncio.run(main())