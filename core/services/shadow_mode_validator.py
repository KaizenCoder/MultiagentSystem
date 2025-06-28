#!/usr/bin/env python3
"""
ShadowModeValidator - Phase 0 Semaine 3
Système de validation zero-risk pour migration d'agents

Objectifs:
- Exécution parallèle agent legacy + agent migré sans impact production
- Comparaison automatisée des résultats avec scoring de similarité
- Activation conditionnelle si parité >99.9%
- Métriques détaillées pour validation migration
- Rollback immédiat en cas de problème
"""

import asyncio
import json
import time
import hashlib
import difflib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Callable, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
import logging
from abc import ABC, abstractmethod

# Imports pour les services centraux
try:
    from .llm_gateway_hybrid import LLMGatewayHybrid
    from .message_bus_a2a import MessageBusA2A, Envelope, MessageType, Priority
    from .context_store import OptimizedContextStore, AgentContext, ContextType
except ImportError:
    # Fallback pour tests isolés
    pass

class ValidationResult(Enum):
    """Résultats de validation"""
    IDENTICAL = "identical"           # Résultats identiques
    SIMILAR = "similar"              # Résultats très similaires (>99.9%)
    ACCEPTABLE = "acceptable"        # Résultats acceptables (>95%)
    DIFFERENT = "different"          # Résultats différents (<95%)
    ERROR_LEGACY = "error_legacy"    # Erreur agent legacy
    ERROR_MODERN = "error_modern"    # Erreur agent moderne
    ERROR_BOTH = "error_both"        # Erreur les deux agents

class ActivationDecision(Enum):
    """Décisions d'activation"""
    ACTIVATE_IMMEDIATELY = "activate_immediately"    # Parité parfaite
    SCHEDULE_ACTIVATION = "schedule_activation"      # Parité >99.9%
    MANUAL_REVIEW = "manual_review"                  # Parité >95%
    REJECT_MIGRATION = "reject_migration"            # Parité <95%
    ROLLBACK_IMMEDIATELY = "rollback_immediately"    # Erreurs critiques

@dataclass
class AgentExecutionResult:
    """Résultat d'exécution d'un agent"""
    agent_id: str
    agent_type: str  # "legacy" | "modern"
    success: bool
    result: Any
    execution_time_ms: int
    memory_used_mb: float
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ComparisonResult:
    """Résultat de comparaison entre agents legacy et moderne"""
    legacy_result: AgentExecutionResult
    modern_result: AgentExecutionResult
    similarity_score: float  # 0.0 à 1.0
    validation_result: ValidationResult
    activation_decision: ActivationDecision
    differences: List[str]
    detailed_comparison: Dict[str, Any]
    comparison_time_ms: int
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Sérialise pour logging"""
        data = asdict(self)
        data['validation_result'] = self.validation_result.value
        data['activation_decision'] = self.activation_decision.value
        data['timestamp'] = self.timestamp.isoformat()
        data['legacy_result']['timestamp'] = self.legacy_result.timestamp.isoformat()
        data['modern_result']['timestamp'] = self.modern_result.timestamp.isoformat()
        return data

@dataclass
class ShadowModeConfig:
    """Configuration du mode shadow"""
    similarity_threshold_activate: float = 0.999     # >99.9% pour activation auto
    similarity_threshold_acceptable: float = 0.95    # >95% pour review manuelle
    max_execution_time_ms: int = 30000               # 30s timeout
    enable_auto_activation: bool = True              # Activation automatique
    enable_rollback_on_error: bool = True           # Rollback automatique
    comparison_sample_size: int = 100                # Échantillons pour validation
    voice_request_bypass: bool = True                # Bypass shadow pour vocal urgent

class ResultComparator:
    """Comparateur intelligent de résultats d'agents"""
    
    def __init__(self):
        self.logger = logging.getLogger("ResultComparator")
    
    def compare_results(self, legacy_result: AgentExecutionResult, 
                       modern_result: AgentExecutionResult) -> ComparisonResult:
        """Compare deux résultats d'agents et calcule la similarité"""
        
        start_time = time.time()
        
        # Vérifier les erreurs
        if not legacy_result.success and not modern_result.success:
            validation_result = ValidationResult.ERROR_BOTH
            similarity_score = 1.0  # Les deux ont échoué de manière similaire
        elif not legacy_result.success:
            validation_result = ValidationResult.ERROR_LEGACY
            similarity_score = 0.0
        elif not modern_result.success:
            validation_result = ValidationResult.ERROR_MODERN
            similarity_score = 0.0
        else:
            # Comparer les résultats réussis
            similarity_score = self._compute_similarity(
                legacy_result.result, 
                modern_result.result
            )
            validation_result = self._classify_similarity(similarity_score)
        
        # Calculer les différences détaillées
        differences = self._compute_differences(
            legacy_result.result, 
            modern_result.result
        )
        
        # Analyse détaillée
        detailed_comparison = self._detailed_analysis(
            legacy_result, 
            modern_result, 
            similarity_score
        )
        
        # Décision d'activation
        activation_decision = self._make_activation_decision(
            validation_result, 
            similarity_score,
            legacy_result,
            modern_result
        )
        
        comparison_time = int((time.time() - start_time) * 1000)
        
        return ComparisonResult(
            legacy_result=legacy_result,
            modern_result=modern_result,
            similarity_score=similarity_score,
            validation_result=validation_result,
            activation_decision=activation_decision,
            differences=differences,
            detailed_comparison=detailed_comparison,
            comparison_time_ms=comparison_time
        )
    
    def _compute_similarity(self, result1: Any, result2: Any) -> float:
        """Calcule la similarité entre deux résultats"""
        
        try:
            # Convertir en strings pour comparaison
            str1 = self._normalize_result(result1)
            str2 = self._normalize_result(result2)
            
            if str1 == str2:
                return 1.0
            
            # Utiliser difflib pour calculer la similarité
            similarity = difflib.SequenceMatcher(None, str1, str2).ratio()
            
            # Bonus pour structures similaires
            if isinstance(result1, dict) and isinstance(result2, dict):
                key_similarity = self._compare_dict_keys(result1, result2)
                similarity = (similarity + key_similarity) / 2
            
            return similarity
            
        except Exception as e:
            self.logger.warning(f"Similarity computation error: {e}")
            return 0.0
    
    def _normalize_result(self, result: Any) -> str:
        """Normalise un résultat pour comparaison"""
        
        if isinstance(result, str):
            return result.strip().lower()
        elif isinstance(result, (dict, list)):
            return json.dumps(result, sort_keys=True, indent=2).lower()
        else:
            return str(result).strip().lower()
    
    def _compare_dict_keys(self, dict1: dict, dict2: dict) -> float:
        """Compare la similarité des clés de dictionnaires"""
        
        keys1 = set(dict1.keys())
        keys2 = set(dict2.keys())
        
        if not keys1 and not keys2:
            return 1.0
        
        intersection = keys1 & keys2
        union = keys1 | keys2
        
        return len(intersection) / len(union) if union else 0.0
    
    def _classify_similarity(self, similarity_score: float) -> ValidationResult:
        """Classifie le score de similarité"""
        
        if similarity_score >= 0.999:
            return ValidationResult.IDENTICAL
        elif similarity_score >= 0.999:
            return ValidationResult.SIMILAR
        elif similarity_score >= 0.95:
            return ValidationResult.ACCEPTABLE
        else:
            return ValidationResult.DIFFERENT
    
    def _compute_differences(self, result1: Any, result2: Any) -> List[str]:
        """Calcule les différences détaillées"""
        
        differences = []
        
        try:
            str1 = self._normalize_result(result1)
            str2 = self._normalize_result(result2)
            
            # Utiliser difflib pour identifier les différences
            diff = list(difflib.unified_diff(
                str1.splitlines(keepends=True),
                str2.splitlines(keepends=True),
                fromfile='legacy',
                tofile='modern',
                lineterm=''
            ))
            
            # Extraire seulement les lignes de différence
            for line in diff:
                if line.startswith('+ ') or line.startswith('- '):
                    differences.append(line.strip())
            
            return differences[:10]  # Limiter à 10 différences
            
        except Exception as e:
            return [f"Error computing differences: {e}"]
    
    def _detailed_analysis(self, legacy_result: AgentExecutionResult,
                          modern_result: AgentExecutionResult,
                          similarity_score: float) -> Dict[str, Any]:
        """Analyse détaillée des résultats"""
        
        return {
            "performance_comparison": {
                "legacy_time_ms": legacy_result.execution_time_ms,
                "modern_time_ms": modern_result.execution_time_ms,
                "performance_improvement": (
                    legacy_result.execution_time_ms - modern_result.execution_time_ms
                ) / max(legacy_result.execution_time_ms, 1),
                "memory_legacy_mb": legacy_result.memory_used_mb,
                "memory_modern_mb": modern_result.memory_used_mb
            },
            "result_analysis": {
                "similarity_score": similarity_score,
                "legacy_success": legacy_result.success,
                "modern_success": modern_result.success,
                "result_types_match": type(legacy_result.result).__name__ == type(modern_result.result).__name__
            },
            "quality_metrics": {
                "data_integrity": similarity_score,
                "error_consistency": legacy_result.success == modern_result.success,
                "performance_regression": modern_result.execution_time_ms > legacy_result.execution_time_ms * 1.5
            }
        }
    
    def _make_activation_decision(self, validation_result: ValidationResult,
                                 similarity_score: float,
                                 legacy_result: AgentExecutionResult,
                                 modern_result: AgentExecutionResult) -> ActivationDecision:
        """Prend la décision d'activation"""
        
        # Erreurs critiques = rollback
        if validation_result in [ValidationResult.ERROR_BOTH, ValidationResult.ERROR_MODERN]:
            return ActivationDecision.ROLLBACK_IMMEDIATELY
        
        # Erreur legacy seulement = activation (moderne fonctionne mieux)
        if validation_result == ValidationResult.ERROR_LEGACY and modern_result.success:
            return ActivationDecision.ACTIVATE_IMMEDIATELY
        
        # Basé sur la similarité
        if similarity_score >= 0.999:
            return ActivationDecision.ACTIVATE_IMMEDIATELY
        elif similarity_score >= 0.999:
            return ActivationDecision.SCHEDULE_ACTIVATION
        elif similarity_score >= 0.95:
            return ActivationDecision.MANUAL_REVIEW
        else:
            return ActivationDecision.REJECT_MIGRATION

class ShadowModeValidator:
    """
    Validateur en mode shadow pour migration zero-risk
    """
    
    def __init__(self, config: ShadowModeConfig,
                 llm_gateway: LLMGatewayHybrid = None,
                 message_bus: MessageBusA2A = None,
                 context_store: OptimizedContextStore = None):
        self.config = config
        self.llm_gateway = llm_gateway
        self.message_bus = message_bus
        self.context_store = context_store
        
        # Services
        self.comparator = ResultComparator()
        
        # Registres
        self.legacy_agents: Dict[str, Any] = {}
        self.modern_agents: Dict[str, Any] = {}
        self.migration_status: Dict[str, str] = {}  # agent_id -> status
        
        # Métriques
        self.metrics = {
            "comparisons_total": 0,
            "activations_auto": 0,
            "activations_manual": 0,
            "rollbacks": 0,
            "avg_similarity_score": 0.0,
            "performance_improvements": 0,
            "validation_results": {result.value: 0 for result in ValidationResult}
        }
        
        # Historique comparaisons pour tendances
        self.comparison_history: List[ComparisonResult] = []
        
        self.logger = logging.getLogger("ShadowModeValidator")
    
    def register_legacy_agent(self, agent_id: str, agent_instance: Any):
        """Enregistre un agent legacy"""
        self.legacy_agents[agent_id] = agent_instance
        self.migration_status[agent_id] = "legacy"
        self.logger.info(f"📦 Legacy agent registered for shadow mode: {agent_id}")
    
    def register_modern_agent(self, agent_id: str, agent_instance: Any):
        """Enregistre un agent moderne"""
        self.modern_agents[agent_id] = agent_instance
        self.migration_status[agent_id] = "shadow_testing"
        self.logger.info(f"🔬 Modern agent registered for shadow testing: {agent_id}")
    
    async def dual_execution(self, agent_id: str, envelope: Envelope) -> ComparisonResult:
        """Exécute en parallèle agent legacy et moderne avec comparaison"""
        
        # Vérifier si l'agent est en mode shadow
        if self.migration_status.get(agent_id) != "shadow_testing":
            raise ValueError(f"Agent {agent_id} not in shadow testing mode")
        
        # Bypass shadow pour requêtes vocales urgentes
        if (self.config.voice_request_bypass and 
            envelope.is_voice_request and 
            envelope.priority == Priority.VOICE_REALTIME):
            
            # Exécuter seulement le moderne pour respecter la latence
            modern_result = await self._execute_modern_agent(agent_id, envelope)
            
            # Créer un résultat de comparaison fictif
            legacy_result = AgentExecutionResult(
                agent_id=agent_id,
                agent_type="legacy",
                success=True,
                result="bypassed_for_voice",
                execution_time_ms=0,
                memory_used_mb=0.0
            )
            
            comparison = ComparisonResult(
                legacy_result=legacy_result,
                modern_result=modern_result,
                similarity_score=1.0,
                validation_result=ValidationResult.IDENTICAL,
                activation_decision=ActivationDecision.ACTIVATE_IMMEDIATELY,
                differences=[],
                detailed_comparison={"voice_bypass": True},
                comparison_time_ms=0
            )
            
            return comparison
        
        # Exécution parallèle normale
        legacy_task = self._execute_legacy_agent(agent_id, envelope)
        modern_task = self._execute_modern_agent(agent_id, envelope)
        
        try:
            # Exécuter en parallèle avec timeout
            legacy_result, modern_result = await asyncio.wait_for(
                asyncio.gather(legacy_task, modern_task, return_exceptions=True),
                timeout=self.config.max_execution_time_ms / 1000
            )
            
            # Gérer les exceptions
            if isinstance(legacy_result, Exception):
                legacy_result = AgentExecutionResult(
                    agent_id=agent_id,
                    agent_type="legacy",
                    success=False,
                    result=None,
                    execution_time_ms=0,
                    memory_used_mb=0.0,
                    error=str(legacy_result)
                )
            
            if isinstance(modern_result, Exception):
                modern_result = AgentExecutionResult(
                    agent_id=agent_id,
                    agent_type="modern",
                    success=False,
                    result=None,
                    execution_time_ms=0,
                    memory_used_mb=0.0,
                    error=str(modern_result)
                )
            
            # Comparer les résultats
            comparison = self.comparator.compare_results(legacy_result, modern_result)
            
            # Mettre à jour les métriques
            self._update_metrics(comparison)
            
            # Ajouter à l'historique
            self.comparison_history.append(comparison)
            if len(self.comparison_history) > 1000:  # Limiter la taille
                self.comparison_history = self.comparison_history[-500:]
            
            # Logging détaillé
            self.logger.info(
                f"🔬 Shadow comparison - {agent_id}: "
                f"Similarity: {comparison.similarity_score:.3f}, "
                f"Decision: {comparison.activation_decision.value}"
            )
            
            # Traiter la décision d'activation
            if self.config.enable_auto_activation:
                await self._process_activation_decision(agent_id, comparison)
            
            return comparison
            
        except asyncio.TimeoutError:
            self.logger.error(f"⏱️ Shadow execution timeout for {agent_id}")
            
            # Créer un résultat d'erreur de timeout
            error_result = AgentExecutionResult(
                agent_id=agent_id,
                agent_type="timeout",
                success=False,
                result=None,
                execution_time_ms=self.config.max_execution_time_ms,
                memory_used_mb=0.0,
                error="Execution timeout"
            )
            
            return ComparisonResult(
                legacy_result=error_result,
                modern_result=error_result,
                similarity_score=0.0,
                validation_result=ValidationResult.ERROR_BOTH,
                activation_decision=ActivationDecision.ROLLBACK_IMMEDIATELY,
                differences=["Execution timeout"],
                detailed_comparison={"timeout": True},
                comparison_time_ms=0
            )
    
    async def _execute_legacy_agent(self, agent_id: str, envelope: Envelope) -> AgentExecutionResult:
        """Exécute l'agent legacy"""
        
        start_time = time.time()
        
        try:
            agent = self.legacy_agents.get(agent_id)
            if not agent:
                raise Exception(f"Legacy agent {agent_id} not found")
            
            # Adapter l'enveloppe pour l'interface legacy
            legacy_params = self._envelope_to_legacy_params(envelope)
            
            # Exécution (synchrone typique pour agents legacy)
            if hasattr(agent, 'execute'):
                result = await asyncio.get_event_loop().run_in_executor(
                    None, agent.execute, legacy_params
                )
            elif hasattr(agent, 'run'):
                result = await asyncio.get_event_loop().run_in_executor(
                    None, agent.run, legacy_params
                )
            else:
                raise Exception(f"Legacy agent {agent_id} has no execute/run method")
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return AgentExecutionResult(
                agent_id=agent_id,
                agent_type="legacy",
                success=True,
                result=result,
                execution_time_ms=execution_time,
                memory_used_mb=0.0,  # Difficult à mesurer pour legacy
                metadata={"method": "legacy_execution"}
            )
            
        except Exception as e:
            execution_time = int((time.time() - start_time) * 1000)
            
            return AgentExecutionResult(
                agent_id=agent_id,
                agent_type="legacy",
                success=False,
                result=None,
                execution_time_ms=execution_time,
                memory_used_mb=0.0,
                error=str(e),
                metadata={"error_type": type(e).__name__}
            )
    
    async def _execute_modern_agent(self, agent_id: str, envelope: Envelope) -> AgentExecutionResult:
        """Exécute l'agent moderne"""
        
        start_time = time.time()
        
        try:
            agent = self.modern_agents.get(agent_id)
            if not agent:
                raise Exception(f"Modern agent {agent_id} not found")
            
            # Charger le contexte si disponible
            context = None
            if self.context_store:
                context = await self.context_store.get_agent_context_complete(agent_id)
            
            # Exécution moderne (async)
            if hasattr(agent, 'execute_async'):
                result = await agent.execute_async(envelope, context)
            elif hasattr(agent, 'execute'):
                result = await agent.execute(envelope, context)
            else:
                raise Exception(f"Modern agent {agent_id} has no execute method")
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return AgentExecutionResult(
                agent_id=agent_id,
                agent_type="modern",
                success=True,
                result=result,
                execution_time_ms=execution_time,
                memory_used_mb=0.0,  # À implémenter si nécessaire
                metadata={"method": "modern_execution", "context_used": context is not None}
            )
            
        except Exception as e:
            execution_time = int((time.time() - start_time) * 1000)
            
            return AgentExecutionResult(
                agent_id=agent_id,
                agent_type="modern",
                success=False,
                result=None,
                execution_time_ms=execution_time,
                memory_used_mb=0.0,
                error=str(e),
                metadata={"error_type": type(e).__name__}
            )
    
    def _envelope_to_legacy_params(self, envelope: Envelope) -> Dict[str, Any]:
        """Convertit une enveloppe moderne vers paramètres legacy"""
        
        return {
            "task_id": envelope.task_id,
            "action": envelope.message_type.value,
            "data": envelope.payload,
            "source": envelope.source_agent,
            "priority": envelope.priority.value,
            "voice_mode": envelope.is_voice_request
        }
    
    async def _process_activation_decision(self, agent_id: str, comparison: ComparisonResult):
        """Traite la décision d'activation automatique"""
        
        decision = comparison.activation_decision
        
        if decision == ActivationDecision.ACTIVATE_IMMEDIATELY:
            await self._activate_modern_agent(agent_id, comparison)
            self.metrics["activations_auto"] += 1
            
        elif decision == ActivationDecision.SCHEDULE_ACTIVATION:
            # Vérifier l'historique pour confirmation
            if self._should_auto_activate_based_on_history(agent_id):
                await self._activate_modern_agent(agent_id, comparison)
                self.metrics["activations_auto"] += 1
            else:
                self.logger.info(f"📋 Scheduled activation for {agent_id} - need more samples")
                
        elif decision == ActivationDecision.ROLLBACK_IMMEDIATELY:
            await self._rollback_modern_agent(agent_id, comparison)
            self.metrics["rollbacks"] += 1
            
        elif decision == ActivationDecision.MANUAL_REVIEW:
            self.logger.warning(f"👤 Manual review required for {agent_id}")
            self.metrics["activations_manual"] += 1
    
    def _should_auto_activate_based_on_history(self, agent_id: str) -> bool:
        """Vérifie si l'activation automatique est justifiée par l'historique"""
        
        # Récupérer les dernières comparaisons pour cet agent
        recent_comparisons = [
            comp for comp in self.comparison_history[-20:]
            if comp.legacy_result.agent_id == agent_id
        ]
        
        if len(recent_comparisons) < 5:
            return False  # Pas assez d'échantillons
        
        # Vérifier la consistance
        avg_similarity = sum(comp.similarity_score for comp in recent_comparisons) / len(recent_comparisons)
        
        return avg_similarity >= 0.999  # 99.9% en moyenne
    
    async def _activate_modern_agent(self, agent_id: str, comparison: ComparisonResult):
        """Active l'agent moderne en production"""
        
        self.migration_status[agent_id] = "modern_active"
        
        # Notifier via message bus si disponible
        if self.message_bus:
            activation_envelope = Envelope(
                task_id=f"activation_{agent_id}",
                message_type=MessageType.AGENT_DISCOVERY,
                source_agent="shadow_validator",
                target_agent="system",
                payload={
                    "event": "agent_activated",
                    "agent_id": agent_id,
                    "similarity_score": comparison.similarity_score,
                    "decision": comparison.activation_decision.value
                }
            )
            await self.message_bus.publish(activation_envelope)
        
        self.logger.info(f"🚀 Agent {agent_id} activated in production (similarity: {comparison.similarity_score:.3f})")
    
    async def _rollback_modern_agent(self, agent_id: str, comparison: ComparisonResult):
        """Rollback vers l'agent legacy"""
        
        self.migration_status[agent_id] = "rollback_to_legacy"
        
        # Notifier le rollback
        if self.message_bus:
            rollback_envelope = Envelope(
                task_id=f"rollback_{agent_id}",
                message_type=MessageType.AGENT_DISCOVERY,
                source_agent="shadow_validator",
                target_agent="system",
                payload={
                    "event": "agent_rollback",
                    "agent_id": agent_id,
                    "reason": comparison.validation_result.value,
                    "error": comparison.modern_result.error
                }
            )
            await self.message_bus.publish(rollback_envelope)
        
        self.logger.error(f"🔙 Agent {agent_id} rolled back to legacy (reason: {comparison.validation_result.value})")
    
    def _update_metrics(self, comparison: ComparisonResult):
        """Met à jour les métriques du shadow mode"""
        
        self.metrics["comparisons_total"] += 1
        
        # Similarité moyenne
        total = self.metrics["comparisons_total"]
        current_avg = self.metrics["avg_similarity_score"]
        self.metrics["avg_similarity_score"] = (
            (current_avg * (total - 1) + comparison.similarity_score) / total
        )
        
        # Amélioration performance
        if (comparison.modern_result.success and comparison.legacy_result.success and
            comparison.modern_result.execution_time_ms < comparison.legacy_result.execution_time_ms):
            self.metrics["performance_improvements"] += 1
        
        # Résultats de validation
        self.metrics["validation_results"][comparison.validation_result.value] += 1
    
    def get_agent_migration_status(self, agent_id: str) -> Dict[str, Any]:
        """Retourne le statut de migration d'un agent"""
        
        status = self.migration_status.get(agent_id, "unknown")
        
        # Récupérer les comparaisons récentes
        recent_comparisons = [
            comp for comp in self.comparison_history[-10:]
            if comp.legacy_result.agent_id == agent_id
        ]
        
        avg_similarity = 0.0
        if recent_comparisons:
            avg_similarity = sum(comp.similarity_score for comp in recent_comparisons) / len(recent_comparisons)
        
        return {
            "agent_id": agent_id,
            "status": status,
            "comparisons_count": len(recent_comparisons),
            "avg_similarity_score": avg_similarity,
            "last_comparison": recent_comparisons[-1].to_dict() if recent_comparisons else None,
            "ready_for_activation": avg_similarity >= 0.999 and len(recent_comparisons) >= 5
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Retourne les métriques du shadow mode"""
        
        success_rate = 0.0
        if self.metrics["comparisons_total"] > 0:
            successful_comparisons = (
                self.metrics["validation_results"]["identical"] +
                self.metrics["validation_results"]["similar"] +
                self.metrics["validation_results"]["acceptable"]
            )
            success_rate = successful_comparisons / self.metrics["comparisons_total"]
        
        return {
            **self.metrics,
            "success_rate": success_rate,
            "agents_in_shadow": len([s for s in self.migration_status.values() if s == "shadow_testing"]),
            "agents_activated": len([s for s in self.migration_status.values() if s == "modern_active"]),
            "agents_rolled_back": len([s for s in self.migration_status.values() if s == "rollback_to_legacy"])
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Vérification de santé du shadow mode"""
        
        health = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "components": {}
        }
        
        # Vérifier les services connectés
        health["components"]["llm_gateway"] = "connected" if self.llm_gateway else "not_connected"
        health["components"]["message_bus"] = "connected" if self.message_bus else "not_connected"
        health["components"]["context_store"] = "connected" if self.context_store else "not_connected"
        
        # Vérifier les agents enregistrés
        health["agents"] = {
            "legacy_registered": len(self.legacy_agents),
            "modern_registered": len(self.modern_agents),
            "in_shadow_testing": len([s for s in self.migration_status.values() if s == "shadow_testing"])
        }
        
        return health

# Factory functions

async def create_shadow_validator(config: ShadowModeConfig = None,
                                llm_gateway: LLMGatewayHybrid = None,
                                message_bus: MessageBusA2A = None,
                                context_store: OptimizedContextStore = None) -> ShadowModeValidator:
    """Crée un ShadowModeValidator"""
    
    if config is None:
        config = ShadowModeConfig()
    
    return ShadowModeValidator(config, llm_gateway, message_bus, context_store)

# Démonstration et tests

async def demo_shadow_mode():
    """Démonstration du ShadowModeValidator"""
    
    print("🚀 ShadowModeValidator Demo - Phase 0 Week 3")
    print("=" * 60)
    
    # Configuration
    config = ShadowModeConfig(
        similarity_threshold_activate=0.999,
        enable_auto_activation=True,
        comparison_sample_size=10
    )
    
    try:
        # Création du validator
        validator = await create_shadow_validator(config)
        
        # Mock agents pour démonstration
        class MockLegacyAgent:
            def execute(self, params):
                return {
                    "status": "completed",
                    "files_analyzed": ["main.py", "utils.py"],
                    "issues_found": 3,
                    "recommendations": ["Fix variable naming", "Add error handling"]
                }
        
        class MockModernAgent:
            async def execute(self, envelope, context=None):
                # Simulation de l'agent moderne avec légère amélioration
                return {
                    "status": "completed",
                    "files_analyzed": ["main.py", "utils.py"],
                    "issues_found": 3,
                    "recommendations": ["Fix variable naming", "Add error handling"],
                    "performance_score": 0.92,  # Amélioration moderne
                    "execution_time": "1.2s"
                }
        
        # Enregistrer les agents
        legacy_agent = MockLegacyAgent()
        modern_agent = MockModernAgent()
        
        validator.register_legacy_agent("agent_111_auditeur_qualite", legacy_agent)
        validator.register_modern_agent("agent_111_auditeur_qualite", modern_agent)
        
        # Test 1: Comparaison normale
        print("\n🧪 Test 1: Shadow Mode Comparison")
        
        from .message_bus_a2a import Envelope, MessageType, Priority
        
        test_envelope = Envelope(
            task_id="shadow_test_001",
            message_type=MessageType.TASK_START,
            source_agent="test_runner",
            target_agent="agent_111_auditeur_qualite",
            payload={
                "action": "analyze_code",
                "files": ["main.py", "utils.py"]
            }
        )
        
        comparison = await validator.dual_execution("agent_111_auditeur_qualite", test_envelope)
        print(f"Similarity score: {comparison.similarity_score:.3f}")
        print(f"Validation result: {comparison.validation_result.value}")
        print(f"Activation decision: {comparison.activation_decision.value}")
        
        # Test 2: Requête vocale (bypass)
        print("\n🧪 Test 2: Voice Request Bypass")
        
        voice_envelope = Envelope(
            task_id="voice_test_001",
            message_type=MessageType.VOICE_CMD,
            source_agent="voice_interface",
            target_agent="agent_111_auditeur_qualite",
            payload={"command": "quick_status"},
            priority=Priority.VOICE_REALTIME,
            is_voice_request=True
        )
        
        voice_comparison = await validator.dual_execution("agent_111_auditeur_qualite", voice_envelope)
        print(f"Voice bypass activated: {'voice_bypass' in voice_comparison.detailed_comparison}")
        
        # Test 3: Simulation de comparaisons multiples
        print("\n🧪 Test 3: Multiple Comparisons for Trend Analysis")
        
        for i in range(5):
            test_envelope.task_id = f"trend_test_{i:03d}"
            comparison = await validator.dual_execution("agent_111_auditeur_qualite", test_envelope)
            print(f"Comparison {i+1}: {comparison.similarity_score:.3f}")
        
        # Test 4: Statut de migration
        print("\n🧪 Test 4: Migration Status")
        
        status = validator.get_agent_migration_status("agent_111_auditeur_qualite")
        print(f"Agent status: {status['status']}")
        print(f"Comparisons count: {status['comparisons_count']}")
        print(f"Average similarity: {status['avg_similarity_score']:.3f}")
        print(f"Ready for activation: {status['ready_for_activation']}")
        
        # Métriques
        print("\n📊 Métriques Shadow Mode")
        metrics = validator.get_metrics()
        print(f"Total comparisons: {metrics['comparisons_total']}")
        print(f"Success rate: {metrics['success_rate']:.2%}")
        print(f"Auto activations: {metrics['activations_auto']}")
        print(f"Average similarity: {metrics['avg_similarity_score']:.3f}")
        print(f"Agents in shadow: {metrics['agents_in_shadow']}")
        
        # Health check
        print("\n🏥 Health Check")
        health = await validator.health_check()
        print(f"Status: {health['status']}")
        print(f"Components: {health['components']}")
        print(f"Agents: {health['agents']}")
        
        print("\n✅ Demo completed successfully")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(demo_shadow_mode())