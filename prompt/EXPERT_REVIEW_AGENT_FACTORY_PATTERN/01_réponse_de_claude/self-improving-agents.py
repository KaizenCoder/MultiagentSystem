from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import asyncio
import json
from collections import defaultdict

# === Learning Components ===

@dataclass
class Experience:
    """Représente une expérience d'apprentissage"""
    agent_id: str
    task_type: str
    input_features: Dict[str, Any]
    strategy_used: str
    outcome: str  # success, partial, failure
    performance_metrics: Dict[str, float]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    context: Dict[str, Any] = field(default_factory=dict)

class ExperienceBuffer:
    """Buffer d'expériences pour apprentissage"""
    
    def __init__(self, max_size: int = 10000):
        self.max_size = max_size
        self.experiences: List[Experience] = []
        self.by_agent: Dict[str, List[Experience]] = defaultdict(list)
        self.by_task: Dict[str, List[Experience]] = defaultdict(list)
    
    def add_experience(self, experience: Experience):
        """Ajoute une expérience au buffer"""
        self.experiences.append(experience)
        self.by_agent[experience.agent_id].append(experience)
        self.by_task[experience.task_type].append(experience)
        
        # Maintenir la taille maximale (FIFO)
        if len(self.experiences) > self.max_size:
            removed = self.experiences.pop(0)
            self.by_agent[removed.agent_id].remove(removed)
            self.by_task[removed.task_type].remove(removed)
    
    def get_experiences_for_learning(
        self,
        agent_id: Optional[str] = None,
        task_type: Optional[str] = None,
        min_experiences: int = 100
    ) -> List[Experience]:
        """Récupère les expériences pour apprentissage"""
        if agent_id:
            experiences = self.by_agent.get(agent_id, [])
        elif task_type:
            experiences = self.by_task.get(task_type, [])
        else:
            experiences = self.experiences
        
        # Filtrer les expériences récentes
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        recent_experiences = [
            exp for exp in experiences 
            if exp.timestamp > cutoff_date
        ]
        
        return recent_experiences if len(recent_experiences) >= min_experiences else []

# === Strategy Learning ===

class StrategyOptimizer:
    """Optimise les stratégies basé sur l'apprentissage"""
    
    def __init__(self):
        self.models: Dict[str, Any] = {}  # task_type -> model
        self.strategy_performance: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.feature_importance: Dict[str, Dict[str, float]] = {}
    
    async def learn_from_experiences(
        self,
        experiences: List[Experience],
        task_type: str
    ):
        """Apprend des expériences pour optimiser les stratégies"""
        if len(experiences) < 50:
            return  # Pas assez de données
        
        # Préparer les données
        X, y = self._prepare_training_data(experiences)
        
        # Entraîner le modèle
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        # Sauvegarder le modèle
        self.models[task_type] = model
        
        # Analyser l'importance des features
        feature_names = self._get_feature_names(experiences[0])
        self.feature_importance[task_type] = dict(
            zip(feature_names, model.feature_importances_)
        )
        
        # Calculer les performances par stratégie
        for strategy in set(exp.strategy_used for exp in experiences):
            strategy_exps = [exp for exp in experiences if exp.strategy_used == strategy]
            success_rate = sum(1 for exp in strategy_exps if exp.outcome == "success") / len(strategy_exps)
            self.strategy_performance[task_type][strategy] = success_rate
    
    def recommend_strategy(
        self,
        task_type: str,
        input_features: Dict[str, Any],
        available_strategies: List[str]
    ) -> str:
        """Recommande la meilleure stratégie pour une tâche"""
        # Si pas de modèle, utiliser les performances historiques
        if task_type not in self.models:
            if task_type in self.strategy_performance:
                perfs = self.strategy_performance[task_type]
                best_strategy = max(
                    (s for s in available_strategies if s in perfs),
                    key=lambda s: perfs[s],
                    default=available_strategies[0]
                )
                return best_strategy
            return available_strategies[0]  # Stratégie par défaut
        
        # Utiliser le modèle pour prédire
        model = self.models[task_type]
        
        # Tester chaque stratégie
        predictions = {}
        for strategy in available_strategies:
            features = self._extract_features({**input_features, "strategy": strategy})
            prob_success = model.predict_proba([features])[0][1]  # Probabilité de succès
            predictions[strategy] = prob_success
        
        # Choisir la meilleure
        return max(predictions, key=predictions.get)
    
    def _prepare_training_data(
        self,
        experiences: List[Experience]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Prépare les données pour l'entraînement"""
        X = []
        y = []
        
        for exp in experiences:
            features = self._extract_features({
                **exp.input_features,
                "strategy": exp.strategy_used
            })
            X.append(features)
            y.append(1 if exp.outcome == "success" else 0)
        
        return np.array(X), np.array(y)
    
    def _extract_features(self, data: Dict[str, Any]) -> List[float]:
        """Extrait les features numériques des données"""
        features = []
        for key, value in sorted(data.items()):
            if isinstance(value, (int, float)):
                features.append(value)
            elif isinstance(value, bool):
                features.append(1.0 if value else 0.0)
            elif isinstance(value, str):
                # Simple hash pour les catégories
                features.append(hash(value) % 1000 / 1000.0)
        return features
    
    def _get_feature_names(self, experience: Experience) -> List[str]:
        """Obtient les noms des features"""
        data = {**experience.input_features, "strategy": experience.strategy_used}
        return sorted(data.keys())

# === Self-Improving Agent ===

class SelfImprovingAgent(BaseAgent):
    """Agent capable d'auto-amélioration"""
    
    def __init__(
        self,
        name: str,
        role: str,
        domain: str,
        experience_buffer: ExperienceBuffer,
        strategy_optimizer: StrategyOptimizer
    ):
        super().__init__(name, role, domain)
        self.experience_buffer = experience_buffer
        self.strategy_optimizer = strategy_optimizer
        self.strategies = self._initialize_strategies()
        self.learning_enabled = True
        self.exploration_rate = 0.1  # 10% d'exploration
        self.performance_history = []
    
    def _initialize_strategies(self) -> Dict[str, Any]:
        """Initialise les stratégies disponibles"""
        return {
            "fast": self._fast_strategy,
            "thorough": self._thorough_strategy,
            "balanced": self._balanced_strategy,
            "experimental": self._experimental_strategy
        }
    
    async def _process_implementation(
        self,
        input_data: Any,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Traitement avec sélection de stratégie intelligente"""
        task_type = context.get("task_type", "general")
        
        # Extraction des features
        input_features = self._extract_input_features(input_data, context)
        
        # Sélection de la stratégie
        if np.random.random() < self.exploration_rate and self.learning_enabled:
            # Exploration : choisir aléatoirement
            strategy_name = np.random.choice(list(self.strategies.keys()))
        else:
            # Exploitation : utiliser la recommandation
            strategy_name = self.strategy_optimizer.recommend_strategy(
                task_type,
                input_features,
                list(self.strategies.keys())
            )
        
        # Exécuter la stratégie
        start_time = asyncio.get_event_loop().time()
        try:
            strategy_func = self.strategies[strategy_name]
            result = await strategy_func(input_data, context)
            outcome = "success"
        except Exception as e:
            result = {"error": str(e)}
            outcome = "failure"
        
        processing_time = asyncio.get_event_loop().time() - start_time
        
        # Enregistrer l'expérience
        if self.learning_enabled:
            experience = Experience(
                agent_id=self.metadata.id,
                task_type=task_type,
                input_features=input_features,
                strategy_used=strategy_name,
                outcome=outcome,
                performance_metrics={
                    "processing_time": processing_time,
                    "success": outcome == "success"
                },
                context=context
            )
            self.experience_buffer.add_experience(experience)
        
        # Mise à jour des métriques
        self._update_performance_metrics(outcome, processing_time)
        
        # Apprentissage périodique
        if len(self.experience_buffer.by_agent[self.metadata.id]) % 100 == 0:
            await self._periodic_learning()
        
        return {
            "result": result,
            "strategy_used": strategy_name,
            "processing_time": processing_time
        }
    
    async def _fast_strategy(
        self,
        input_data: Any,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Stratégie rapide mais moins précise"""
        # Implémentation simplifiée
        return {"status": "completed_fast", "data": str(input_data)[:100]}
    
    async def _thorough_strategy(
        self,
        input_data: Any,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Stratégie approfondie mais plus lente"""
        await asyncio.sleep(0.1)  # Simulation de traitement complexe
        return {"status": "completed_thorough", "data": str(input_data)}
    
    async def _balanced_strategy(
        self,
        input_data: Any,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Stratégie équilibrée"""
        return {"status": "completed_balanced", "data": str(input_data)[:200]}
    
    async def _experimental_strategy(
        self,
        input_data: Any,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Stratégie expérimentale pour exploration"""
        # Essayer des approches nouvelles
        if "priority" in context and context["priority"] == "high":
            return await self._thorough_strategy(input_data, context)
        return await self._fast_strategy(input_data, context)
    
    def _extract_input_features(
        self,
        input_data: Any,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extrait les features de l'input"""
        features = {
            "data_size": len(str(input_data)),
            "has_priority": "priority" in context,
            "is_complex": len(str(input_data)) > 1000,
            "hour_of_day": datetime.utcnow().hour,
            "day_of_week": datetime.utcnow().weekday()
        }
        
        # Ajouter des features du contexte
        for key in ["priority", "deadline", "retry_count"]:
            if key in context:
                features[f"context_{key}"] = context[key]
        
        return features
    
    def _update_performance_metrics(self, outcome: str, processing_time: float):
        """Met à jour les métriques de performance"""
        self.performance_metrics["tasks_completed"] += 1
        if outcome == "success":
            self.performance_metrics["successful_requests"] += 1
        
        # Moyenne mobile du temps de traitement
        current_avg = self.performance_metrics.get("avg_processing_time", 0)
        self.performance_metrics["avg_processing_time"] = (
            current_avg * 0.9 + processing_time * 0.1
        )
        
        # Taux de succès
        self.performance_metrics["success_rate"] = (
            self.performance_metrics["successful_requests"] /
            self.performance_metrics["tasks_completed"]
        )
    
    async def _periodic_learning(self):
        """Apprentissage périodique des expériences"""
        experiences = self.experience_buffer.get_experiences_for_learning(
            agent_id=self.metadata.id
        )
        
        if experiences:
            # Grouper par type de tâche
            task_experiences = defaultdict(list)
            for exp in experiences:
                task_experiences[exp.task_type].append(exp)
            
            # Apprendre pour chaque type
            for task_type, task_exps in task_experiences.items():
                await self.strategy_optimizer.learn_from_experiences(
                    task_exps, task_type
                )
            
            # Ajuster le taux d'exploration
            avg_success_rate = np.mean([
                self.strategy_optimizer.strategy_performance.get(task_type, {}).get(s, 0)
                for task_type in task_experiences
                for s in self.strategies.keys()
            ])
            
            # Réduire l'exploration si performance stable
            if avg_success_rate > 0.8:
                self.exploration_rate = max(0.05, self.exploration_rate * 0.9)
            elif avg_success_rate < 0.6:
                self.exploration_rate = min(0.3, self.exploration_rate * 1.1)

# === A/B Testing Framework ===

class ABTestingFramework:
    """Framework pour A/B testing d'agents"""
    
    def __init__(self):
        self.active_tests: Dict[str, 'ABTest'] = {}
        self.test_results: Dict[str, 'TestResult'] = {}
    
    async def create_test(
        self,
        test_name: str,
        control_agent: BaseAgent,
        variant_agents: List[BaseAgent],
        traffic_split: List[float] = None,
        duration_hours: int = 24,
        min_samples: int = 1000
    ) -> 'ABTest':
        """Crée un nouveau test A/B"""
        if traffic_split is None:
            # Répartition égale par défaut
            n_variants = len(variant_agents) + 1
            traffic_split = [1.0 / n_variants] * n_variants
        
        test = ABTest(
            name=test_name,
            control_agent=control_agent,
            variant_agents=variant_agents,
            traffic_split=traffic_split,
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(hours=duration_hours),
            min_samples=min_samples
        )
        
        self.active_tests[test_name] = test
        return test
    
    async def route_request(
        self,
        test_name: str,
        request_id: str,
        input_data: Any,
        context: Dict[str, Any]
    ) -> Tuple[BaseAgent, str]:
        """Route une requête vers un agent selon le test A/B"""
        test = self.active_tests.get(test_name)
        if not test or not test.is_active():
            raise ValueError(f"No active test: {test_name}")
        
        # Sélection de la variante
        variant_idx = self._select_variant(test.traffic_split)
        
        if variant_idx == 0:
            agent = test.control_agent
            variant_name = "control"
        else:
            agent = test.variant_agents[variant_idx - 1]
            variant_name = f"variant_{variant_idx}"
        
        # Enregistrer l'assignation
        test.assignments[request_id] = variant_name
        
        return agent, variant_name
    
    def _select_variant(self, traffic_split: List[float]) -> int:
        """Sélectionne une variante selon la répartition du trafic"""
        r = np.random.random()
        cumulative = 0.0
        
        for i, split in enumerate(traffic_split):
            cumulative += split
            if r < cumulative:
                return i
        
        return len(traffic_split) - 1
    
    async def record_result(
        self,
        test_name: str,
        request_id: str,
        metrics: Dict[str, float]
    ):
        """Enregistre le résultat d'une requête"""
        test = self.active_tests.get(test_name)
        if not test:
            return
        
        variant_name = test.assignments.get(request_id)
        if not variant_name:
            return
        
        test.results[variant_name].append(metrics)
        
        # Vérifier si le test est terminé
        if await self._should_stop_test(test):
            await self.conclude_test(test_name)
    
    async def _should_stop_test(self, test: 'ABTest') -> bool:
        """Détermine si un test doit être arrêté"""
        # Vérifier la durée
        if datetime.utcnow() > test.end_time:
            return True
        
        # Vérifier le nombre d'échantillons
        min_samples_reached = all(
            len(results) >= test.min_samples
            for results in test.results.values()
        )
        
        if not min_samples_reached:
            return False
        
        # Arrêt précoce si différence significative
        if len(test.results) >= 2:
            control_metrics = test.results.get("control", [])
            if control_metrics and len(control_metrics) >= 100:
                for variant_name, variant_metrics in test.results.items():
                    if variant_name != "control" and len(variant_metrics) >= 100:
                        p_value = self._calculate_significance(
                            control_metrics, variant_metrics
                        )
                        if p_value < 0.001:  # Très significatif
                            return True
        
        return False
    
    def _calculate_significance(
        self,
        control_metrics: List[Dict[str, float]],
        variant_metrics: List[Dict[str, float]]
    ) -> float:
        """Calcule la significance statistique (p-value simplifiée)"""
        # Utiliser scipy.stats.ttest_ind en production
        control_success = [m.get("success", 0) for m in control_metrics]
        variant_success = [m.get("success", 0) for m in variant_metrics]
        
        control_mean = np.mean(control_success)
        variant_mean = np.mean(variant_success)
        
        # P-value simplifiée (utiliser un vrai test statistique en prod)
        diff = abs(control_mean - variant_mean)
        return 1.0 - min(diff * 10, 0.99)  # Simplification
    
    async def conclude_test(self, test_name: str) -> 'TestResult':
        """Conclut un test et génère les résultats"""
        test = self.active_tests.pop(test_name, None)
        if not test:
            return None
        
        # Analyser les résultats
        result = TestResult(
            test_name=test_name,
            start_time=test.start_time,
            end_time=datetime.utcnow(),
            total_requests=sum(len(r) for r in test.results.values())
        )
        
        # Calculer les métriques pour chaque variante
        for variant_name, metrics_list in test.results.items():
            if metrics_list:
                variant_stats = {
                    "sample_size": len(metrics_list),
                    "success_rate": np.mean([m.get("success", 0) for m in metrics_list]),
                    "avg_processing_time": np.mean([m.get("processing_time", 0) for m in metrics_list]),
                    "error_rate": np.mean([m.get("error", 0) for m in metrics_list])
                }
                result.variant_results[variant_name] = variant_stats
        
        # Déterminer le gagnant
        if "control" in result.variant_results:
            control_success = result.variant_results["control"]["success_rate"]
            best_variant = "control"
            best_improvement = 0.0
            
            for variant_name, stats in result.variant_results.items():
                if variant_name != "control":
                    improvement = (stats["success_rate"] - control_success) / control_success
                    if improvement > best_improvement:
                        best_variant = variant_name
                        best_improvement = improvement
            
            result.winner = best_variant
            result.improvement = best_improvement
        
        self.test_results[test_name] = result
        return result

@dataclass
class ABTest:
    """Représente un test A/B actif"""
    name: str
    control_agent: BaseAgent
    variant_agents: List[BaseAgent]
    traffic_split: List[float]
    start_time: datetime
    end_time: datetime
    min_samples: int
    assignments: Dict[str, str] = field(default_factory=dict)
    results: Dict[str, List[Dict[str, float]]] = field(default_factory=lambda: defaultdict(list))
    
    def is_active(self) -> bool:
        """Vérifie si le test est actif"""
        return datetime.utcnow() < self.end_time

@dataclass
class TestResult:
    """Résultat d'un test A/B"""
    test_name: str
    start_time: datetime
    end_time: datetime
    total_requests: int
    variant_results: Dict[str, Dict[str, float]] = field(default_factory=dict)
    winner: Optional[str] = None
    improvement: Optional[float] = None

# === Continuous Learning Pipeline ===

class ContinuousLearningPipeline:
    """Pipeline d'apprentissage continu pour les agents"""
    
    def __init__(
        self,
        experience_buffer: ExperienceBuffer,
        strategy_optimizer: StrategyOptimizer,
        ab_testing: ABTestingFramework
    ):
        self.experience_buffer = experience_buffer
        self.strategy_optimizer = strategy_optimizer
        self.ab_testing = ab_testing
        self.learning_schedule = {
            "hourly": timedelta(hours=1),
            "daily": timedelta(days=1),
            "weekly": timedelta(weeks=1)
        }
        self.last_learning: Dict[str, datetime] = {}
        self.model_versions: Dict[str, int] = defaultdict(int)
    
    async def start_pipeline(self):
        """Démarre le pipeline d'apprentissage continu"""
        # Tâches d'apprentissage périodiques
        asyncio.create_task(self._hourly_learning())
        asyncio.create_task(self._daily_learning())
        asyncio.create_task(self._weekly_learning())
        
        # Monitoring et alertes
        asyncio.create_task(self._monitor_performance())
    
    async def _hourly_learning(self):
        """Apprentissage horaire - ajustements rapides"""
        while True:
            await asyncio.sleep(3600)  # 1 heure
            
            # Mise à jour des stratégies pour les tâches fréquentes
            for task_type, experiences in self._get_recent_experiences_by_task(hours=1).items():
                if len(experiences) >= 10:
                    await self.strategy_optimizer.learn_from_experiences(
                        experiences, task_type
                    )
            
            self.last_learning["hourly"] = datetime.utcnow()
    
    async def _daily_learning(self):
        """Apprentissage quotidien - optimisations moyennes"""
        while True:
            await asyncio.sleep(86400)  # 24 heures
            
            # Réévaluation complète des modèles
            all_tasks = self._get_all_task_types()
            
            for task_type in all_tasks:
                experiences = self.experience_buffer.get_experiences_for_learning(
                    task_type=task_type
                )
                
                if len(experiences) >= 100:
                    # Créer un nouveau modèle
                    await self.strategy_optimizer.learn_from_experiences(
                        experiences, task_type
                    )
                    self.model_versions[task_type] += 1
                    
                    # Lancer un A/B test si amélioration significative
                    await self._create_ab_test_for_improved_model(task_type)
            
            self.last_learning["daily"] = datetime.utcnow()
    
    async def _weekly_learning(self):
        """Apprentissage hebdomadaire - refonte majeure"""
        while True:
            await asyncio.sleep(604800)  # 7 jours
            
            # Analyse approfondie et refonte des stratégies
            await self._deep_strategy_analysis()
            
            # Nettoyage des anciennes expériences
            self._cleanup_old_experiences()
            
            self.last_learning["weekly"] = datetime.utcnow()
    
    def _get_recent_experiences_by_task(
        self,
        hours: int
    ) -> Dict[str, List[Experience]]:
        """Récupère les expériences récentes par type de tâche"""
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        recent_by_task = defaultdict(list)
        
        for exp in self.experience_buffer.experiences:
            if exp.timestamp > cutoff:
                recent_by_task[exp.task_type].append(exp)
        
        return recent_by_task
    
    def _get_all_task_types(self) -> List[str]:
        """Obtient tous les types de tâches connus"""
        return list(self.experience_buffer.by_task.keys())
    
    async def _create_ab_test_for_improved_model(self, task_type: str):
        """Crée un test A/B pour un modèle amélioré"""
        # Logique pour créer des agents avec ancien/nouveau modèle
        # et lancer un test A/B
        pass
    
    async def _deep_strategy_analysis(self):
        """Analyse approfondie des stratégies"""
        # Analyser les patterns de succès/échec
        # Identifier les nouvelles opportunités d'optimisation
        # Proposer de nouvelles stratégies expérimentales
        pass
    
    def _cleanup_old_experiences(self):
        """Nettoie les expériences anciennes"""
        cutoff = datetime.utcnow() - timedelta(days=90)
        self.experience_buffer.experiences = [
            exp for exp in self.experience_buffer.experiences
            if exp.timestamp > cutoff
        ]
    
    async def _monitor_performance(self):
        """Monitore la performance et génère des alertes"""
        while True:
            await asyncio.sleep(300)  # 5 minutes
            
            # Vérifier les dégradations de performance
            for task_type in self._get_all_task_types():
                recent_perf = self._calculate_recent_performance(task_type)
                historical_perf = self._calculate_historical_performance(task_type)
                
                if recent_perf < historical_perf * 0.9:  # Dégradation de 10%
                    await self._trigger_performance_alert(
                        task_type, recent_perf, historical_perf
                    )
    
    def _calculate_recent_performance(
        self,
        task_type: str,
        hours: int = 1
    ) -> float:
        """Calcule la performance récente"""
        recent_exps = self._get_recent_experiences_by_task(hours).get(task_type, [])
        if not recent_exps:
            return 0.0
        
        success_count = sum(1 for exp in recent_exps if exp.outcome == "success")
        return success_count / len(recent_exps)
    
    def _calculate_historical_performance(
        self,
        task_type: str,
        days: int = 7
    ) -> float:
        """Calcule la performance historique"""
        cutoff = datetime.utcnow() - timedelta(days=days)
        historical_exps = [
            exp for exp in self.experience_buffer.by_task.get(task_type, [])
            if exp.timestamp > cutoff
        ]
        
        if not historical_exps:
            return 0.0
        
        success_count = sum(1 for exp in historical_exps if exp.outcome == "success")
        return success_count / len(historical_exps)
    
    async def _trigger_performance_alert(
        self,
        task_type: str,
        recent_perf: float,
        historical_perf: float
    ):
        """Déclenche une alerte de performance"""
        alert = {
            "type": "performance_degradation",
            "task_type": task_type,
            "recent_performance": recent_perf,
            "historical_performance": historical_perf,
            "degradation": (historical_perf - recent_perf) / historical_perf,
            "timestamp": datetime.utcnow()
        }
        
        # En production : envoyer à un système d'alerting
        print(f"ALERT: Performance degradation for {task_type}: {alert}")

# === Exemple d'utilisation ===

async def self_improving_example():
    """Exemple d'utilisation du framework d'auto-amélioration"""
    
    # Initialisation des composants
    experience_buffer = ExperienceBuffer(max_size=10000)
    strategy_optimizer = StrategyOptimizer()
    ab_testing = ABTestingFramework()
    
    # Pipeline d'apprentissage continu
    pipeline = ContinuousLearningPipeline(
        experience_buffer,
        strategy_optimizer,
        ab_testing
    )
    await pipeline.start_pipeline()
    
    # Créer des agents auto-améliorants
    agent1 = SelfImprovingAgent(
        "agent_v1",
        "processor",
        "data_processing",
        experience_buffer,
        strategy_optimizer
    )
    
    agent2 = SelfImprovingAgent(
        "agent_v2",
        "processor",
        "data_processing",
        experience_buffer,
        strategy_optimizer
    )
    agent2.exploration_rate = 0.2  # Plus d'exploration
    
    # Créer un test A/B
    ab_test = await ab_testing.create_test(
        "strategy_optimization_test",
        control_agent=agent1,
        variant_agents=[agent2],
        traffic_split=[0.5, 0.5],
        duration_hours=24,
        min_samples=1000
    )
    
    # Simulation de charge
    for i in range(2000):
        request_id = f"req_{i}"
        input_data = {
            "data": f"sample_data_{i}",
            "size": np.random.randint(100, 1000)
        }
        context = {
            "task_type": "data_processing",
            "priority": np.random.choice(["low", "medium", "high"])
        }
        
        # Router via A/B test
        agent, variant = await ab_testing.route_request(
            "strategy_optimization_test",
            request_id,
            input_data,
            context
        )
        
        # Traiter la requête
        result = await agent.process(input_data, context)
        
        # Enregistrer les métriques
        metrics = {
            "success": "error" not in result,
            "processing_time": result.get("processing_time", 0),
            "error": "error" in result
        }
        
        await ab_testing.record_result(
            "strategy_optimization_test",
            request_id,
            metrics
        )
        
        # Afficher les progrès
        if i % 100 == 0:
            print(f"Processed {i} requests")
            print(f"Agent 1 success rate: {agent1.performance_metrics.get('success_rate', 0):.2%}")
            print(f"Agent 2 success rate: {agent2.performance_metrics.get('success_rate', 0):.2%}")
            
            # Afficher les stratégies préférées
            if strategy_optimizer.strategy_performance:
                print("Strategy performance:")
                for task, strategies in strategy_optimizer.strategy_performance.items():
                    print(f"  {task}: {strategies}")
    
    # Conclure le test A/B
    test_result = await ab_testing.conclude_test("strategy_optimization_test")
    
    print("\n=== A/B Test Results ===")
    print(f"Winner: {test_result.winner}")
    print(f"Improvement: {test_result.improvement:.2%}")
    for variant, stats in test_result.variant_results.items():
        print(f"\n{variant}:")
        for metric, value in stats.items():
            print(f"  {metric}: {value}")

if __name__ == "__main__":
    asyncio.run(self_improving_example())