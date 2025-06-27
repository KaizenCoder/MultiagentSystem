"""
Circuit Breaker Pattern Implementation
NextGeneration Maintenance Team - Robustesse et Gestion d'Erreurs

Implémentation du pattern Circuit Breaker pour:
- Protection contre les cascades de pannes
- Retry avec exponential backoff
- Gestion intelligente des échecs
- Monitoring des états du circuit
"""

from enum import Enum
import time
import asyncio
from typing import Callable, Any, Optional
import logging
from functools import wraps

class CircuitState(Enum):
    """États du circuit breaker"""
    CLOSED = "closed"        # Fonctionnement normal
    OPEN = "open"           # Circuit ouvert - rejet immédiat
    HALF_OPEN = "half_open" # Test de récupération

class CircuitBreakerOpenException(Exception):
    """Exception levée quand le circuit breaker est ouvert"""
    def __init__(self, message: str, retry_after: int = 60):
        super().__init__(message)
        self.retry_after = retry_after

class CircuitBreaker:
    """Circuit breaker avec retry exponential backoff"""
    
    def __init__(self, 
                 failure_threshold: int = 5,
                 timeout_seconds: int = 60,
                 retry_multiplier: float = 2.0,
                 max_retry_delay: int = 300,
                 success_threshold: int = 3):
        """
        Initialise le circuit breaker
        
        Args:
            failure_threshold: Nombre d'échecs avant ouverture du circuit
            timeout_seconds: Durée avant tentative de récupération
            retry_multiplier: Multiplicateur pour exponential backoff
            max_retry_delay: Délai maximum entre les retries
            success_threshold: Nombre de succès requis pour fermer le circuit
        """
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.retry_multiplier = retry_multiplier
        self.max_retry_delay = max_retry_delay
        self.success_threshold = success_threshold
        
        # État du circuit
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.next_retry_delay = 1
        
        # Métriques
        self.total_calls = 0
        self.total_failures = 0
        self.total_successes = 0
        self.circuit_opens = 0
        
        # Logger
        self.logger = logging.getLogger(f"{__name__}.CircuitBreaker")
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Exécution avec protection circuit breaker"""
        self.total_calls += 1
        
        # Vérification de l'état du circuit
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._transition_to_half_open()
            else:
                time_until_retry = self._time_until_retry()
                raise CircuitBreakerOpenException(
                    f"Circuit breaker ouvert - retry dans {time_until_retry}s",
                    retry_after=time_until_retry
                )
        
        try:
            # Exécution de la fonction
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            # Succès - gestion de l'état
            self._handle_success()
            return result
            
        except Exception as e:
            # Échec - gestion de l'état
            self._handle_failure(e)
            raise
    
    def _should_attempt_reset(self) -> bool:
        """Détermine si une tentative de reset doit être effectuée"""
        if self.last_failure_time is None:
            return True
        
        time_since_failure = time.time() - self.last_failure_time
        return time_since_failure >= self.timeout_seconds
    
    def _transition_to_half_open(self):
        """Transition vers l'état HALF_OPEN"""
        self.state = CircuitState.HALF_OPEN
        self.success_count = 0
        self.logger.info("🔄 Circuit breaker: Transition vers HALF_OPEN - Tentative de récupération")
    
    def _handle_success(self):
        """Gestion d'un succès"""
        self.total_successes += 1
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            self.logger.debug(f"✅ Succès en HALF_OPEN: {self.success_count}/{self.success_threshold}")
            
            if self.success_count >= self.success_threshold:
                self._transition_to_closed()
        
        elif self.state == CircuitState.CLOSED:
            # Reset du compteur d'échecs en cas de succès
            if self.failure_count > 0:
                self.failure_count = max(0, self.failure_count - 1)
                self.next_retry_delay = 1  # Reset du délai
    
    def _handle_failure(self, exception: Exception):
        """Gestion d'un échec"""
        self.total_failures += 1
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        self.logger.warning(f"❌ Échec circuit breaker: {exception} (échecs: {self.failure_count})")
        
        # Transition vers OPEN si seuil atteint
        if self.failure_count >= self.failure_threshold:
            self._transition_to_open()
        
        # Exponential backoff
        self.next_retry_delay = min(
            self.next_retry_delay * self.retry_multiplier,
            self.max_retry_delay
        )
    
    def _transition_to_closed(self):
        """Transition vers l'état CLOSED (récupération réussie)"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.next_retry_delay = 1
        self.logger.info("✅ Circuit breaker: Transition vers CLOSED - Récupération réussie")
    
    def _transition_to_open(self):
        """Transition vers l'état OPEN (circuit ouvert)"""
        self.state = CircuitState.OPEN
        self.circuit_opens += 1
        self.logger.error(f"💥 Circuit breaker: Transition vers OPEN après {self.failure_count} échecs")
    
    def _time_until_retry(self) -> int:
        """Calcule le temps restant avant le prochain retry"""
        if self.last_failure_time is None:
            return 0
        
        elapsed = time.time() - self.last_failure_time
        remaining = max(0, self.timeout_seconds - elapsed)
        return int(remaining)
    
    def reset(self):
        """Reset manuel du circuit breaker"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.next_retry_delay = 1
        self.logger.info("🔄 Circuit breaker: Reset manuel effectué")
    
    def get_state(self) -> dict:
        """Retourne l'état actuel du circuit breaker"""
        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "total_calls": self.total_calls,
            "total_failures": self.total_failures,
            "total_successes": self.total_successes,
            "circuit_opens": self.circuit_opens,
            "failure_rate": (self.total_failures / self.total_calls * 100) if self.total_calls > 0 else 0,
            "next_retry_delay": self.next_retry_delay,
            "time_until_retry": self._time_until_retry() if self.state == CircuitState.OPEN else 0
        }
    
    def get_metrics(self) -> dict:
        """Retourne les métriques détaillées"""
        state = self.get_state()
        
        return {
            **state,
            "availability": (self.total_successes / self.total_calls * 100) if self.total_calls > 0 else 100,
            "reliability_score": max(0, 100 - (self.circuit_opens * 10)),  # Pénalité par ouverture
            "last_failure_time": self.last_failure_time,
            "uptime_percentage": self._calculate_uptime(),
            "avg_failure_recovery_time": self.timeout_seconds
        }
    
    def _calculate_uptime(self) -> float:
        """Calcule le pourcentage d'uptime"""
        if self.total_calls == 0:
            return 100.0
        
        # Estimation basée sur les succès vs échecs
        return (self.total_successes / self.total_calls) * 100

# Décorateur pour circuit breaker automatique
def circuit_breaker(failure_threshold: int = 5, 
                   timeout_seconds: int = 60,
                   retry_multiplier: float = 2.0):
    """Décorateur pour appliquer un circuit breaker à une fonction"""
    
    def decorator(func: Callable) -> Callable:
        # Circuit breaker spécifique à cette fonction
        cb = CircuitBreaker(
            failure_threshold=failure_threshold,
            timeout_seconds=timeout_seconds,
            retry_multiplier=retry_multiplier
        )
        
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                return await cb.call(func, *args, **kwargs)
            
            # Ajout des méthodes de monitoring
            async_wrapper.circuit_breaker = cb
            async_wrapper.get_circuit_state = cb.get_state
            async_wrapper.get_circuit_metrics = cb.get_metrics
            async_wrapper.reset_circuit = cb.reset
            
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                return asyncio.run(cb.call(func, *args, **kwargs))
            
            # Ajout des méthodes de monitoring
            sync_wrapper.circuit_breaker = cb
            sync_wrapper.get_circuit_state = cb.get_state
            sync_wrapper.get_circuit_metrics = cb.get_metrics
            sync_wrapper.reset_circuit = cb.reset
            
            return sync_wrapper
    
    return decorator

class CircuitBreakerManager:
    """Gestionnaire centralisé des circuit breakers"""
    
    def __init__(self):
        self.circuit_breakers: dict[str, CircuitBreaker] = {}
        self.logger = logging.getLogger(f"{__name__}.CircuitBreakerManager")
    
    def get_or_create(self, name: str, **kwargs) -> CircuitBreaker:
        """Récupère ou crée un circuit breaker nommé"""
        if name not in self.circuit_breakers:
            self.circuit_breakers[name] = CircuitBreaker(**kwargs)
            self.logger.info(f"🔧 Circuit breaker créé: {name}")
        
        return self.circuit_breakers[name]
    
    def get_all_states(self) -> dict:
        """Retourne l'état de tous les circuit breakers"""
        return {
            name: cb.get_state()
            for name, cb in self.circuit_breakers.items()
        }
    
    def get_all_metrics(self) -> dict:
        """Retourne les métriques de tous les circuit breakers"""
        return {
            name: cb.get_metrics()
            for name, cb in self.circuit_breakers.items()
        }
    
    def reset_all(self):
        """Reset tous les circuit breakers"""
        for name, cb in self.circuit_breakers.items():
            cb.reset()
            self.logger.info(f"🔄 Circuit breaker reseté: {name}")
    
    def get_health_summary(self) -> dict:
        """Résumé de santé de tous les circuit breakers"""
        total_circuits = len(self.circuit_breakers)
        open_circuits = sum(1 for cb in self.circuit_breakers.values() 
                           if cb.state == CircuitState.OPEN)
        half_open_circuits = sum(1 for cb in self.circuit_breakers.values() 
                                if cb.state == CircuitState.HALF_OPEN)
        
        return {
            "total_circuits": total_circuits,
            "healthy_circuits": total_circuits - open_circuits - half_open_circuits,
            "open_circuits": open_circuits,
            "half_open_circuits": half_open_circuits,
            "overall_health": "🟢" if open_circuits == 0 else "🟡" if open_circuits < total_circuits / 2 else "🔴"
        }

# Instance globale
global_circuit_manager = CircuitBreakerManager()

def get_global_circuit_manager() -> CircuitBreakerManager:
    """Récupère l'instance globale du gestionnaire de circuit breakers"""
    return global_circuit_manager

# Exemple d'usage
if __name__ == "__main__":
    # Test du circuit breaker
    import random
    
    cb = CircuitBreaker(failure_threshold=3, timeout_seconds=5)
    
    async def test_function():
        """Fonction de test qui échoue parfois"""
        if random.random() < 0.7:  # 30% de chance d'échec
            raise Exception("Erreur de test")
        return "Succès!"
    
    async def run_test():
        """Test du circuit breaker"""
        for i in range(20):
            try:
                result = await cb.call(test_function)
                print(f"✅ Appel {i+1}: {result}")
            except CircuitBreakerOpenException as e:
                print(f"🚨 Appel {i+1}: Circuit ouvert - {e}")
            except Exception as e:
                print(f"❌ Appel {i+1}: Erreur - {e}")
            
            # État du circuit
            state = cb.get_state()
            print(f"   État: {state['state']} (échecs: {state['failure_count']})")
            
            await asyncio.sleep(0.5)
        
        # Métriques finales
        metrics = cb.get_metrics()
        print(f"\n📊 Métriques finales:")
        print(f"   Disponibilité: {metrics['availability']:.1f}%")
        print(f"   Ouvertures circuit: {metrics['circuit_opens']}")
        print(f"   Score fiabilité: {metrics['reliability_score']}")
    
    # Exécution du test
    asyncio.run(run_test()) 