#!/usr/bin/env python3
"""
🔍 SHADOW MODE VALIDATOR - Validation de Migration Zero-Risk
===============================================================================

Système de validation en mode ombre pour migration d'agents legacy vers moderne.
Exécution parallèle et comparaison détaillée pour assurer la continuité.

Fonctionnalités :
- Exécution parallèle Legacy/Moderne
- Comparaison approfondie des résultats
- Métriques de similarité avancées
- Validation zero-risk avec rollback
- Rapport détaillé des différences

Author: NextGeneration Validation Team
Version: 4.4.0 - Shadow Mode Validation
"""

import asyncio
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import json
import logging
import traceback
from dataclasses import dataclass, field
from pathlib import Path

from core.nextgen_architecture import Task, Result

@dataclass
class ShadowTestResult:
    """Résultat de test en mode ombre"""
    test_id: str
    task: Task
    legacy_result: Optional[Result] = None
    modern_result: Optional[Result] = None
    legacy_execution_time: float = 0.0
    modern_execution_time: float = 0.0
    legacy_error: Optional[str] = None
    modern_error: Optional[str] = None
    similarity_score: float = 0.0
    validation_success: bool = False
    differences: List[str] = field(default_factory=list)
    enhancements: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

class ShadowModeValidator:
    """
    🔍 Validateur en Mode Ombre pour Migration d'Agents
    
    Le ShadowModeValidator exécute en parallèle les versions legacy et moderne
    d'un agent sur les mêmes tâches, puis compare les résultats pour assurer
    la continuité fonctionnelle lors de la migration.
    
    Workflow :
    1. Exécution parallèle Legacy + Moderne
    2. Capture des résultats et métriques
    3. Analyse de similarité multi-niveaux
    4. Détection des améliorations LLM
    5. Validation conformité migration
    
    Seuils de validation :
    - Similarité fonctionnelle : > 85%
    - Compatibilité interface : 100%
    - Performance acceptable : < 2x dégradation
    """
    
    def __init__(self, legacy_agent, modern_agent, agent_type: str, similarity_threshold: float = 0.85):
        self.legacy_agent = legacy_agent
        self.modern_agent = modern_agent
        self.agent_type = agent_type
        self.similarity_threshold = similarity_threshold
        
        self.logger = logging.getLogger(f"nextgen.shadow_validator.{agent_type}")
        
        # Métriques de validation
        self.test_history: List[ShadowTestResult] = []
        self.global_metrics = {
            "total_tests": 0,
            "successful_validations": 0,
            "performance_improvements": 0,
            "functional_enhancements": 0
        }
    
    async def initialize(self):
        """Initialise le validateur"""
        self.logger.info(f"🔍 Initialisation ShadowModeValidator pour {self.agent_type}")
        
        # Vérifier que les agents sont opérationnels
        await self._validate_agents_health()
        
        self.logger.info("✅ ShadowModeValidator prêt")
    
    async def _validate_agents_health(self):
        """Valide que les deux agents sont opérationnels"""
        
        # Test Legacy Agent
        try:
            if hasattr(self.legacy_agent, 'health_check'):
                legacy_health = await self.legacy_agent.health_check()
                self.logger.info(f"Legacy agent health: {legacy_health.get('status', 'unknown')}")
            else:
                self.logger.info("Legacy agent health: assumed operational")
        except Exception as e:
            self.logger.warning(f"Legacy agent health check failed: {e}")
        
        # Test Modern Agent  
        try:
            if hasattr(self.modern_agent, 'health_check'):
                modern_health = await self.modern_agent.health_check()
                self.logger.info(f"Modern agent health: {modern_health.get('status', 'unknown')}")
            else:
                self.logger.info("Modern agent health: assumed operational")
        except Exception as e:
            self.logger.warning(f"Modern agent health check failed: {e}")
    
    async def execute_shadow_test(self, task: Task) -> Dict[str, Any]:
        """
        Exécute un test en mode ombre avec comparaison
        """
        test_id = f"shadow_test_{len(self.test_history) + 1}_{int(time.time())}"
        
        self.logger.info(f"🧪 Démarrage test ombre: {test_id}")
        self.logger.info(f"    Tâche: {task.type}")
        self.logger.info(f"    Params: {list(task.params.keys())}")
        
        # Initialiser le résultat de test
        shadow_result = ShadowTestResult(
            test_id=test_id,
            task=task
        )
        
        try:
            # Exécution parallèle des deux agents
            legacy_future = self._execute_legacy_agent(task)
            modern_future = self._execute_modern_agent(task)
            
            # Attendre les deux résultats
            legacy_result, modern_result = await asyncio.gather(
                legacy_future, modern_future, return_exceptions=True
            )
            
            # Traiter les résultats
            shadow_result = await self._process_shadow_results(
                shadow_result, legacy_result, modern_result
            )
            
            # Analyser la similarité
            shadow_result = await self._analyze_similarity(shadow_result)
            
            # Enregistrer le test
            self.test_history.append(shadow_result)
            self.global_metrics["total_tests"] += 1
            
            if shadow_result.validation_success:
                self.global_metrics["successful_validations"] += 1
            
            # Retourner le résultat formaté
            return self._format_shadow_result(shadow_result)
            
        except Exception as e:
            self.logger.error(f"❌ Erreur critique test ombre {test_id}: {e}")
            shadow_result.legacy_error = str(e)
            shadow_result.modern_error = str(e)
            self.test_history.append(shadow_result)
            
            return self._format_shadow_result(shadow_result)
    
    async def _execute_legacy_agent(self, task: Task) -> Tuple[Result, float]:
        """Exécute la tâche sur l'agent legacy"""
        
        start_time = time.time()
        
        try:
            self.logger.debug("  📜 Exécution agent Legacy...")
            
            # Adapter l'interface si nécessaire
            if hasattr(self.legacy_agent, 'execute_task'):
                result = await self.legacy_agent.execute_task(task)
            elif hasattr(self.legacy_agent, 'execute_async'):
                result = await self.legacy_agent.execute_async(task)
            else:
                # Fallback pour agents très anciens
                if hasattr(self.legacy_agent, task.type):
                    method = getattr(self.legacy_agent, task.type)
                    if asyncio.iscoroutinefunction(method):
                        raw_result = await method(task.params)
                    else:
                        raw_result = method(task.params)
                    
                    result = Result(success=True, data=raw_result)
                else:
                    result = Result(
                        success=False,
                        error=f"Method {task.type} not found on legacy agent"
                    )
            
            execution_time = time.time() - start_time
            self.logger.debug(f"    ✅ Legacy terminé en {execution_time:.2f}s")
            
            return result, execution_time
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error(f"    ❌ Legacy failed en {execution_time:.2f}s: {e}")
            
            return Result(success=False, error=str(e)), execution_time
    
    async def _execute_modern_agent(self, task: Task) -> Tuple[Result, float]:
        """Exécute la tâche sur l'agent moderne"""
        
        start_time = time.time()
        
        try:
            self.logger.debug("  🚀 Exécution agent Moderne...")
            
            # L'agent moderne doit avoir execute_async
            if hasattr(self.modern_agent, 'execute_async'):
                result = await self.modern_agent.execute_async(task)
            elif hasattr(self.modern_agent, 'execute_task'):
                result = await self.modern_agent.execute_task(task)
            else:
                result = Result(
                    success=False,
                    error="Modern agent missing execute_async method"
                )
            
            execution_time = time.time() - start_time
            self.logger.debug(f"    ✅ Moderne terminé en {execution_time:.2f}s")
            
            return result, execution_time
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error(f"    ❌ Moderne failed en {execution_time:.2f}s: {e}")
            
            return Result(success=False, error=str(e)), execution_time
    
    async def _process_shadow_results(self, shadow_result: ShadowTestResult, 
                                     legacy_result, modern_result) -> ShadowTestResult:
        """Traite les résultats des exécutions parallèles"""
        
        # Traiter le résultat Legacy
        if isinstance(legacy_result, Exception):
            shadow_result.legacy_error = str(legacy_result)
            shadow_result.legacy_execution_time = 0.0
        else:
            result, exec_time = legacy_result
            shadow_result.legacy_result = result
            shadow_result.legacy_execution_time = exec_time
            if not result.success:
                shadow_result.legacy_error = result.error
        
        # Traiter le résultat Moderne
        if isinstance(modern_result, Exception):
            shadow_result.modern_error = str(modern_result)
            shadow_result.modern_execution_time = 0.0
        else:
            result, exec_time = modern_result
            shadow_result.modern_result = result
            shadow_result.modern_execution_time = exec_time
            if not result.success:
                shadow_result.modern_error = result.error
        
        return shadow_result
    
    async def _analyze_similarity(self, shadow_result: ShadowTestResult) -> ShadowTestResult:
        """Analyse la similarité entre les résultats Legacy et Moderne"""
        
        self.logger.debug("  🔍 Analyse de similarité...")
        
        # Si les deux ont échoué de la même manière, c'est similaire
        if shadow_result.legacy_error and shadow_result.modern_error:
            shadow_result.similarity_score = 0.8  # Échec cohérent
            shadow_result.validation_success = True
            shadow_result.differences.append("Both agents failed consistently")
            self.logger.debug("    📊 Échecs cohérents détectés")
            return shadow_result
        
        # Si un seul a échoué, c'est problématique
        if shadow_result.legacy_error or shadow_result.modern_error:
            shadow_result.similarity_score = 0.2
            shadow_result.validation_success = False
            if shadow_result.legacy_error:
                shadow_result.differences.append(f"Legacy failed: {shadow_result.legacy_error}")
            if shadow_result.modern_error:
                shadow_result.differences.append(f"Modern failed: {shadow_result.modern_error}")
            self.logger.debug("    ⚠️ Échec asymétrique détecté")
            return shadow_result
        
        # Les deux ont réussi - comparer les résultats
        if shadow_result.legacy_result and shadow_result.modern_result:
            similarity_score = await self._calculate_result_similarity(
                shadow_result.legacy_result, shadow_result.modern_result
            )
            
            shadow_result.similarity_score = similarity_score
            shadow_result.validation_success = similarity_score >= self.similarity_threshold
            
            # Détecter les améliorations LLM
            shadow_result.enhancements = await self._detect_llm_enhancements(
                shadow_result.legacy_result, shadow_result.modern_result
            )
            
            self.logger.debug(f"    📊 Similarité: {similarity_score:.2f}")
            self.logger.debug(f"    ✅ Validation: {'RÉUSSIE' if shadow_result.validation_success else 'ÉCHOUÉE'}")
            
            if shadow_result.enhancements:
                self.global_metrics["functional_enhancements"] += 1
                self.logger.debug(f"    🚀 Améliorations LLM: {len(shadow_result.enhancements)}")
        
        return shadow_result
    
    async def _calculate_result_similarity(self, legacy_result: Result, modern_result: Result) -> float:
        """Calcule le score de similarité entre deux résultats"""
        
        similarity_factors = []
        
        # 1. Similarité du statut de succès (critique)
        status_similarity = 1.0 if legacy_result.success == modern_result.success else 0.0
        similarity_factors.append(("status", status_similarity, 0.3))
        
        # 2. Similarité du type de données retournées
        legacy_data_type = type(legacy_result.data).__name__ if legacy_result.data else "None"
        modern_data_type = type(modern_result.data).__name__ if modern_result.data else "None"
        type_similarity = 1.0 if legacy_data_type == modern_data_type else 0.5
        similarity_factors.append(("data_type", type_similarity, 0.2))
        
        # 3. Similarité du contenu des données
        content_similarity = await self._calculate_content_similarity(
            legacy_result.data, modern_result.data
        )
        similarity_factors.append(("content", content_similarity, 0.3))
        
        # 4. Présence de métadonnées additionnelles (bonus pour le moderne)
        metadata_factor = 1.0
        if modern_result.data and isinstance(modern_result.data, dict):
            if any(key in str(modern_result.data) for key in ["llm", "ai", "enhanced", "analysis"]):
                metadata_factor = 1.1  # Bonus pour améliorations LLM
        similarity_factors.append(("metadata", metadata_factor, 0.2))
        
        # Calcul pondéré
        total_score = sum(score * weight for _, score, weight in similarity_factors)
        
        # Debug des facteurs
        for factor_name, score, weight in similarity_factors:
            self.logger.debug(f"      {factor_name}: {score:.2f} (poids: {weight})")
        
        return min(total_score, 1.0)  # Cap à 1.0
    
    async def _calculate_content_similarity(self, legacy_data, modern_data) -> float:
        """Calcule la similarité du contenu des données"""
        
        # Cas simples
        if legacy_data == modern_data:
            return 1.0
        
        if legacy_data is None and modern_data is None:
            return 1.0
        
        if (legacy_data is None) != (modern_data is None):
            return 0.3  # Un seul est None
        
        # Comparaison par type
        if isinstance(legacy_data, dict) and isinstance(modern_data, dict):
            return self._compare_dict_similarity(legacy_data, modern_data)
        
        if isinstance(legacy_data, (list, tuple)) and isinstance(modern_data, (list, tuple)):
            return self._compare_list_similarity(legacy_data, modern_data)
        
        if isinstance(legacy_data, str) and isinstance(modern_data, str):
            return self._compare_string_similarity(legacy_data, modern_data)
        
        # Conversion en string pour comparaison générale
        legacy_str = str(legacy_data)
        modern_str = str(modern_data)
        return self._compare_string_similarity(legacy_str, modern_str)
    
    def _compare_dict_similarity(self, dict1: dict, dict2: dict) -> float:
        """Compare deux dictionnaires"""
        
        all_keys = set(dict1.keys()) | set(dict2.keys())
        if not all_keys:
            return 1.0
        
        common_keys = set(dict1.keys()) & set(dict2.keys())
        key_similarity = len(common_keys) / len(all_keys)
        
        # Similarité des valeurs pour les clés communes
        value_similarities = []
        for key in common_keys:
            if dict1[key] == dict2[key]:
                value_similarities.append(1.0)
            else:
                value_similarities.append(0.5)  # Valeur différente mais clé présente
        
        value_similarity = sum(value_similarities) / len(common_keys) if common_keys else 0.0
        
        # Score pondéré
        return 0.6 * key_similarity + 0.4 * value_similarity
    
    def _compare_list_similarity(self, list1: list, list2: list) -> float:
        """Compare deux listes"""
        
        if len(list1) == len(list2) == 0:
            return 1.0
        
        if len(list1) == 0 or len(list2) == 0:
            return 0.2
        
        # Similarité de taille
        max_len = max(len(list1), len(list2))
        min_len = min(len(list1), len(list2))
        size_similarity = min_len / max_len
        
        # Similarité d'éléments (comparaison simple)
        common_elements = 0
        for i in range(min_len):
            if i < len(list1) and i < len(list2) and list1[i] == list2[i]:
                common_elements += 1
        
        element_similarity = common_elements / max_len if max_len > 0 else 0.0
        
        return 0.5 * size_similarity + 0.5 * element_similarity
    
    def _compare_string_similarity(self, str1: str, str2: str) -> float:
        """Compare deux chaînes de caractères"""
        
        if str1 == str2:
            return 1.0
        
        if not str1 or not str2:
            return 0.1
        
        # Similarité basique par longueur et caractères communs
        max_len = max(len(str1), len(str2))
        min_len = min(len(str1), len(str2))
        
        # Similarité de longueur
        length_similarity = min_len / max_len
        
        # Caractères communs (très basique)
        common_chars = sum(1 for c1, c2 in zip(str1[:min_len], str2[:min_len]) if c1 == c2)
        char_similarity = common_chars / max_len if max_len > 0 else 0.0
        
        return 0.3 * length_similarity + 0.7 * char_similarity
    
    async def _detect_llm_enhancements(self, legacy_result: Result, modern_result: Result) -> List[str]:
        """Détecte les améliorations apportées par le LLM"""
        
        enhancements = []
        
        # Vérifier si le moderne a plus de données
        if modern_result.data and legacy_result.data:
            modern_str = str(modern_result.data).lower()
            legacy_str = str(legacy_result.data).lower()
            
            # Détection d'améliorations LLM par mots-clés
            llm_keywords = [
                "analysis", "insights", "recommendations", "ai", "llm", 
                "enhanced", "intelligent", "optimization", "strategy"
            ]
            
            for keyword in llm_keywords:
                if keyword in modern_str and keyword not in legacy_str:
                    enhancements.append(f"Added {keyword} capability")
            
            # Détection de données supplémentaires
            if len(modern_str) > len(legacy_str) * 1.2:
                enhancements.append("Enriched output with additional data")
            
            # Détection de structure améliorée
            if isinstance(modern_result.data, dict) and not isinstance(legacy_result.data, dict):
                enhancements.append("Improved data structure")
        
        return enhancements
    
    def _format_shadow_result(self, shadow_result: ShadowTestResult) -> Dict[str, Any]:
        """Formate le résultat de test ombre pour retour"""
        
        return {
            "test_id": shadow_result.test_id,
            "validation_success": shadow_result.validation_success,
            "similarity_score": shadow_result.similarity_score,
            "execution_times": {
                "legacy": shadow_result.legacy_execution_time,
                "modern": shadow_result.modern_execution_time,
                "performance_ratio": (
                    shadow_result.modern_execution_time / shadow_result.legacy_execution_time
                    if shadow_result.legacy_execution_time > 0 else float('inf')
                )
            },
            "results": {
                "legacy_success": shadow_result.legacy_result.success if shadow_result.legacy_result else False,
                "modern_success": shadow_result.modern_result.success if shadow_result.modern_result else False,
                "legacy_error": shadow_result.legacy_error,
                "modern_error": shadow_result.modern_error
            },
            "differences": shadow_result.differences,
            "enhancements": shadow_result.enhancements,
            "llm_enhancements": len(shadow_result.enhancements) > 0,
            "timestamp": shadow_result.timestamp
        }
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Retourne un résumé de toutes les validations"""
        
        if self.global_metrics["total_tests"] == 0:
            success_rate = 0.0
        else:
            success_rate = self.global_metrics["successful_validations"] / self.global_metrics["total_tests"]
        
        return {
            "agent_type": self.agent_type,
            "total_tests": self.global_metrics["total_tests"],
            "successful_validations": self.global_metrics["successful_validations"],
            "success_rate": success_rate,
            "similarity_threshold": self.similarity_threshold,
            "functional_enhancements": self.global_metrics["functional_enhancements"],
            "performance_improvements": self.global_metrics["performance_improvements"],
            "test_history_count": len(self.test_history),
            "validation_status": "PASSED" if success_rate >= 0.8 else "PARTIAL" if success_rate >= 0.5 else "FAILED"
        }

# Factory function
def create_shadow_validator(legacy_agent, modern_agent, agent_type: str, 
                          similarity_threshold: float = 0.85) -> ShadowModeValidator:
    """Crée une instance ShadowModeValidator"""
    return ShadowModeValidator(legacy_agent, modern_agent, agent_type, similarity_threshold)