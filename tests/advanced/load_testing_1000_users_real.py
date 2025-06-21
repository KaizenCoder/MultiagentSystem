"""
[ROCKET] LOAD TESTING 1000+ USERS REAL - PHASE 4 IA-1+IA-2
Tests de charge rels avec infrastructure production

Objectifs :
- Validation 1000+ utilisateurs simultans
- Latence P95 < 200ms
- Throughput > 1000 req/s
- Infrastructure IA-2 oprationnelle
"""

import asyncio
import aiohttp
import time
import random
import json
import statistics
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor
import sys
import os

# Golden Source Logging
from core import logging_manager

# Configuration du logging
logger = logging_manager.get_logger('load_test', custom_config={
    "logger_name": "LoadTest",
    "log_level": "INFO",
    "elasticsearch_enabled": False, # Important pour l'analyse des résultats, mais désactivé pour les tests locaux sans ES.
    "async_enabled": True,
})

# Import infrastructure IA-2
from orchestrator.app.performance.redis_cache_production import get_production_cache, CacheStrategy

@dataclass
class LoadTestConfig:
    """Configuration test de charge"""
    # Users & Load
    max_concurrent_users: int = 1000
    ramp_up_duration: int = 60  # secondes
    test_duration: int = 300    # 5 minutes
    ramp_down_duration: int = 30
    
    # Infrastructure endpoints (IA-2)
    orchestrator_api_url: str = "http://localhost:8002"
    memory_api_url: str = "http://localhost:8001"
    load_balancer_url: str = "http://localhost:8080"  # HAProxy
    
    # Performance thresholds
    target_latency_p95_ms: float = 200.0
    target_throughput_rps: float = 1000.0
    max_error_rate_percent: float = 1.0
    
    # Request patterns
    request_types: Dict[str, float] = None  # Pourcentages
    
    def __post_init__(self):
        if self.request_types is None:
            self.request_types = {
                "health_check": 10.0,      # 10% health checks
                "simple_query": 40.0,      # 40% queries simples
                "complex_analysis": 30.0,  # 30% analyses complexes
                "rag_search": 15.0,        # 15% recherches RAG
                "user_session": 5.0        # 5% gestion sessions
            }

@dataclass
class RequestResult:
    """Rsultat d'une requte individuelle"""
    timestamp: float
    request_type: str
    user_id: str
    response_time_ms: float
    status_code: int
    success: bool
    error_message: Optional[str] = None
    response_size_bytes: int = 0

@dataclass
class LoadTestResults:
    """Rsultats complets du test de charge"""
    config: LoadTestConfig
    start_time: datetime
    end_time: datetime
    total_requests: int
    successful_requests: int
    failed_requests: int
    
    # Performance metrics
    avg_response_time_ms: float
    p50_response_time_ms: float
    p95_response_time_ms: float
    p99_response_time_ms: float
    
    # Throughput
    requests_per_second: float
    peak_throughput_rps: float
    
    # Error analysis
    error_rate_percent: float
    error_types: Dict[str, int]
    
    # Pass/Fail criteria
    meets_latency_sla: bool
    meets_throughput_sla: bool
    meets_error_rate_sla: bool
    overall_success: bool

class UserSimulator:
    """Simulateur d'utilisateur individuel"""
    
    def __init__(self, user_id: str, config: LoadTestConfig):
        self.user_id = user_id
        self.config = config
        self.session = None
        self.results: List[RequestResult] = []
        
    async def initialize(self):
        """Initialise session HTTP"""
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            connector=aiohttp.TCPConnector(limit=10)
        )
        
    async def cleanup(self):
        """Nettoie ressources"""
        if self.session:
            await self.session.close()
    
    def _select_request_type(self) -> str:
        """Slectionne type de requte selon distribution"""
        rand = random.random() * 100
        cumulative = 0
        
        for req_type, percentage in self.config.request_types.items():
            cumulative += percentage
            if rand <= cumulative:
                return req_type
                
        return "simple_query"  # Fallback
    
    async def _make_health_check(self) -> RequestResult:
        """Health check simple"""
        start_time = time.time()
        request_type = "health_check"
        
        try:
            async with self.session.get(
                f"{self.config.orchestrator_api_url}/health"
            ) as response:
                content = await response.read()
                response_time_ms = (time.time() - start_time) * 1000
                
                return RequestResult(
                    timestamp=start_time,
                    request_type=request_type,
                    user_id=self.user_id,
                    response_time_ms=response_time_ms,
                    status_code=response.status,
                    success=response.status == 200,
                    response_size_bytes=len(content)
                )
                
        except Exception as e:
            response_time_ms = (time.time() - start_time) * 1000
            return RequestResult(
                timestamp=start_time,
                request_type=request_type,
                user_id=self.user_id,
                response_time_ms=response_time_ms,
                status_code=0,
                success=False,
                error_message=str(e)
            )
    
    async def _make_simple_query(self) -> RequestResult:
        """Requte simple  l'orchestrateur"""
        start_time = time.time()
        request_type = "simple_query"
        
        queries = [
            "Quelle est la mto aujourd'hui ?",
            "Explique-moi le machine learning",
            "Comment fonctionne Python ?",
            "Qu'est-ce que Docker ?",
            "Raconte-moi une blague"
        ]
        
        payload = {
            "user_input": random.choice(queries),
            "user_id": self.user_id,
            "session_id": f"{self.user_id}_{int(time.time())}"
        }
        
        try:
            async with self.session.post(
                f"{self.config.orchestrator_api_url}/process",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                content = await response.read()
                response_time_ms = (time.time() - start_time) * 1000
                
                return RequestResult(
                    timestamp=start_time,
                    request_type=request_type,
                    user_id=self.user_id,
                    response_time_ms=response_time_ms,
                    status_code=response.status,
                    success=response.status == 200,
                    response_size_bytes=len(content)
                )
                
        except Exception as e:
            response_time_ms = (time.time() - start_time) * 1000
            return RequestResult(
                timestamp=start_time,
                request_type=request_type,
                user_id=self.user_id,
                response_time_ms=response_time_ms,
                status_code=0,
                success=False,
                error_message=str(e)
            )
    
    async def _make_complex_analysis(self) -> RequestResult:
        """Analyse complexe qui sollicite les LLMs"""
        start_time = time.time()
        request_type = "complex_analysis"
        
        complex_queries = [
            "Analyse les tendances conomiques mondiales et leurs impacts sur l'IA",
            "Explique les diffrences entre les architectures de transformers",
            "Dveloppe une stratgie marketing complte pour une startup tech",
            "Compare les avantages et inconvnients de microservices vs monolithe",
            "Rdige un rapport sur l'impact environnemental du cloud computing"
        ]
        
        payload = {
            "user_input": random.choice(complex_queries),
            "user_id": self.user_id,
            "session_id": f"{self.user_id}_{int(time.time())}",
            "complexity": "high",
            "require_analysis": True
        }
        
        try:
            async with self.session.post(
                f"{self.config.orchestrator_api_url}/analyze",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                content = await response.read()
                response_time_ms = (time.time() - start_time) * 1000
                
                return RequestResult(
                    timestamp=start_time,
                    request_type=request_type,
                    user_id=self.user_id,
                    response_time_ms=response_time_ms,
                    status_code=response.status,
                    success=response.status in [200, 202],  # 202 = Accepted (async)
                    response_size_bytes=len(content)
                )
                
        except Exception as e:
            response_time_ms = (time.time() - start_time) * 1000
            return RequestResult(
                timestamp=start_time,
                request_type=request_type,
                user_id=self.user_id,
                response_time_ms=response_time_ms,
                status_code=0,
                success=False,
                error_message=str(e)
            )
    
    async def _make_rag_search(self) -> RequestResult:
        """Recherche dans la base de connaissances"""
        start_time = time.time()
        request_type = "rag_search"
        
        search_queries = [
            "Documentation API orchestrateur",
            "Architecture microservices best practices",
            "Tests de charge mtriques",
            "Scurit applications web",
            "Kubernetes deployment patterns"
        ]
        
        payload = {
            "query": random.choice(search_queries),
            "user_id": self.user_id,
            "limit": 10,
            "include_sources": True
        }
        
        try:
            async with self.session.post(
                f"{self.config.memory_api_url}/search",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                content = await response.read()
                response_time_ms = (time.time() - start_time) * 1000
                
                return RequestResult(
                    timestamp=start_time,
                    request_type=request_type,
                    user_id=self.user_id,
                    response_time_ms=response_time_ms,
                    status_code=response.status,
                    success=response.status == 200,
                    response_size_bytes=len(content)
                )
                
        except Exception as e:
            response_time_ms = (time.time() - start_time) * 1000
            return RequestResult(
                timestamp=start_time,
                request_type=request_type,
                user_id=self.user_id,
                response_time_ms=response_time_ms,
                status_code=0,
                success=False,
                error_message=str(e)
            )
    
    async def _make_user_session(self) -> RequestResult:
        """Gestion session utilisateur"""
        start_time = time.time()
        request_type = "user_session"
        
        # Test du cache Redis IA-2
        try:
            cache = await get_production_cache()
            
            # Test SET session
            session_data = {
                "user_id": self.user_id,
                "timestamp": time.time(),
                "preferences": {"theme": "dark", "language": "fr"}
            }
            
            set_success = await cache.set(
                CacheStrategy.USER_SESSIONS,
                f"session_{self.user_id}",
                session_data,
                user_id=self.user_id
            )
            
            # Test GET session
            get_result = await cache.get(
                CacheStrategy.USER_SESSIONS,
                f"session_{self.user_id}",
                user_id=self.user_id
            )
            
            response_time_ms = (time.time() - start_time) * 1000
            
            return RequestResult(
                timestamp=start_time,
                request_type=request_type,
                user_id=self.user_id,
                response_time_ms=response_time_ms,
                status_code=200 if set_success and get_result else 500,
                success=set_success and get_result is not None,
                response_size_bytes=len(json.dumps(session_data))
            )
            
        except Exception as e:
            response_time_ms = (time.time() - start_time) * 1000
            return RequestResult(
                timestamp=start_time,
                request_type=request_type,
                user_id=self.user_id,
                response_time_ms=response_time_ms,
                status_code=0,
                success=False,
                error_message=str(e)
            )
    
    async def run_user_simulation(self, duration: int) -> List[RequestResult]:
        """Excute simulation utilisateur pendant dure donne"""
        await self.initialize()
        end_time = time.time() + duration
        
        while time.time() < end_time:
            # Slectionner type de requte
            request_type = self._select_request_type()
            
            # Excuter requte correspondante
            if request_type == "health_check":
                result = await self._make_health_check()
            elif request_type == "simple_query":
                result = await self._make_simple_query()
            elif request_type == "complex_analysis":
                result = await self._make_complex_analysis()
            elif request_type == "rag_search":
                result = await self._make_rag_search()
            elif request_type == "user_session":
                result = await self._make_user_session()
            else:
                continue
            
            self.results.append(result)
            
            # Dlai variable entre requtes (simulation humaine)
            await asyncio.sleep(random.uniform(0.5, 3.0))
        
        await self.cleanup()
        return self.results

class LoadTestOrchestrator:
    """Orchestrateur principal des tests de charge"""
    
    def __init__(self, config: LoadTestConfig):
        self.config = config
        self.all_results: List[RequestResult] = []
        
    async def run_load_test(self) -> LoadTestResults:
        """Excute test de charge complet"""
        logger.info(f"🚀 Dmarrage du test de charge avec {self.config.max_concurrent_users} utilisateurs sur {self.config.test_duration}s...")
        start_time = datetime.now()
        
        # Phase 1: Ramp-up
        await self._ramp_up_phase()
        
        # Phase 2: Plateau
        plateau_results = await self._plateau_phase()
        self.all_results.extend(plateau_results)
        
        # Phase 3: Ramp-down
        await self._ramp_down_phase()
        
        end_time = datetime.now()
        logger.info("🏁 Test de charge termin.")
        
        # Analyse rsultats
        logger.info("📊 Analyse des rsultats...")
        results = self._analyze_results(self.all_results, start_time, end_time)
        
        return results
    
    async def _ramp_up_phase(self):
        """Phase monte en charge progressive"""
        logger.info(f"📈 Phase de Ramp-up: 0 -> {self.config.max_concurrent_users} utilisateurs en {self.config.ramp_up_duration}s")
        ramp_step_duration = self.config.ramp_up_duration / 10
        users_per_step = self.config.max_concurrent_users // 10
        
        for step in range(10):
            current_users = (step + 1) * users_per_step
            logger.info(f"  Ramp-up step {step+1}/10: {current_users} users")
            
            # Dmarrer utilisateurs pour cette tape
            tasks = []
            for i in range(users_per_step):
                user_id = f"rampup_user_{step}_{i}"
                simulator = UserSimulator(user_id, self.config)
                task = asyncio.create_task(
                    simulator.run_user_simulation(int(ramp_step_duration))
                )
                tasks.append(task)
            
            # Attendre fin de l'tape
            await asyncio.sleep(ramp_step_duration)
    
    async def _plateau_phase(self) -> List[RequestResult]:
        """Phase charge maximale (phase critique)"""
        logger.info(f"⛰️  Phase de Plateau: {self.config.max_concurrent_users} utilisateurs pendant {self.config.test_duration}s")
        tasks = []
        
        # Lancer tous les utilisateurs simultans
        for i in range(self.config.max_concurrent_users):
            user_id = f"load_user_{i}"
            simulator = UserSimulator(user_id, self.config)
            task = asyncio.create_task(
                simulator.run_user_simulation(self.config.test_duration)
            )
            tasks.append(task)
        
        logger.info(f"[LIGHTNING] {len(tasks)} utilisateurs actifs...")
        
        # Monitoring en temps rel
        monitor_task = asyncio.create_task(
            self._monitor_real_time(self.config.test_duration)
        )
        
        # Attendre completion
        all_user_results = await asyncio.gather(*tasks, return_exceptions=True)
        await monitor_task
        
        # Collecter rsultats
        plateau_results = []
        for user_results in all_user_results:
            if isinstance(user_results, list):
                plateau_results.extend(user_results)
            elif isinstance(user_results, Exception):
                logger.error(f"Erreur utilisateur : {user_results}")
        
        logger.info(f"✅ Plateau termin. {len(plateau_results)} requtes gnres.")
        return plateau_results
    
    async def _ramp_down_phase(self):
        """Phase descente de charge"""
        logger.info(f"📉 Phase de Ramp-down: {self.config.max_concurrent_users} -> 0 utilisateurs en {self.config.ramp_down_duration}s")
        # Simulation progressive reduction (pour stats)
        await asyncio.sleep(self.config.ramp_down_duration)
        logger.info(" Ramp-down termin")
    
    async def _monitor_real_time(self, duration: int):
        """Monitoring temps rel pendant test"""
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Log toutes les 30 secondes
            await asyncio.sleep(30)
            elapsed = time.time() - start_time
            logger.info(f" Test en cours : {elapsed:.0f}s / {duration}s")
    
    def _analyze_results(self, results: List[RequestResult], 
                        start_time: datetime, end_time: datetime) -> LoadTestResults:
        """Analyse complte des rsultats"""
        
        if not results:
            return LoadTestResults(
                config=self.config,
                start_time=start_time,
                end_time=end_time,
                total_requests=0,
                successful_requests=0,
                failed_requests=0,
                avg_response_time_ms=0,
                p50_response_time_ms=0,
                p95_response_time_ms=0,
                p99_response_time_ms=0,
                requests_per_second=0,
                peak_throughput_rps=0,
                error_rate_percent=100,
                error_types={},
                meets_latency_sla=False,
                meets_throughput_sla=False,
                meets_error_rate_sla=False,
                overall_success=False
            )
        
        # Mtriques de base
        total_requests = len(results)
        successful_requests = sum(1 for r in results if r.success)
        failed_requests = total_requests - successful_requests
        
        # Temps de rponse
        response_times = [r.response_time_ms for r in results if r.success]
        
        if response_times:
            avg_response_time_ms = statistics.mean(response_times)
            p50_response_time_ms = statistics.median(response_times)
            p95_response_time_ms = statistics.quantiles(response_times, n=20)[18]  # 95th percentile
            p99_response_time_ms = statistics.quantiles(response_times, n=100)[98]  # 99th percentile
        else:
            avg_response_time_ms = 0
            p50_response_time_ms = 0
            p95_response_time_ms = 0
            p99_response_time_ms = 0
        
        # Throughput
        test_duration_sec = (end_time - start_time).total_seconds()
        requests_per_second = total_requests / max(test_duration_sec, 1)
        
        # Peak throughput (fentre glissante 10s)
        peak_throughput_rps = self._calculate_peak_throughput(results)
        
        # Erreurs
        error_rate_percent = (failed_requests / total_requests) * 100 if total_requests > 0 else 100
        error_types = {}
        for result in results:
            if not result.success and result.error_message:
                error_types[result.error_message] = error_types.get(result.error_message, 0) + 1
        
        # SLA validation
        meets_latency_sla = p95_response_time_ms <= self.config.target_latency_p95_ms
        meets_throughput_sla = requests_per_second >= self.config.target_throughput_rps
        meets_error_rate_sla = error_rate_percent <= self.config.max_error_rate_percent
        
        overall_success = meets_latency_sla and meets_throughput_sla and meets_error_rate_sla
        
        return LoadTestResults(
            config=self.config,
            start_time=start_time,
            end_time=end_time,
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            avg_response_time_ms=avg_response_time_ms,
            p50_response_time_ms=p50_response_time_ms,
            p95_response_time_ms=p95_response_time_ms,
            p99_response_time_ms=p99_response_time_ms,
            requests_per_second=requests_per_second,
            peak_throughput_rps=peak_throughput_rps,
            error_rate_percent=error_rate_percent,
            error_types=error_types,
            meets_latency_sla=meets_latency_sla,
            meets_throughput_sla=meets_throughput_sla,
            meets_error_rate_sla=meets_error_rate_sla,
            overall_success=overall_success
        )
    
    def _calculate_peak_throughput(self, results: List[RequestResult]) -> float:
        """Calcule pic de throughput (fentre 10s)"""
        if not results:
            return 0.0
        
        # Regrouper par fentre de 10s
        window_size = 10.0
        min_timestamp = min(r.timestamp for r in results)
        max_timestamp = max(r.timestamp for r in results)
        
        max_throughput = 0.0
        
        current_time = min_timestamp
        while current_time < max_timestamp:
            window_end = current_time + window_size
            window_requests = [
                r for r in results 
                if current_time <= r.timestamp < window_end
            ]
            
            window_throughput = len(window_requests) / window_size
            max_throughput = max(max_throughput, window_throughput)
            
            current_time += 1.0  # Avancer par pas de 1s
        
        return max_throughput
    
    def print_detailed_report(self, results: LoadTestResults):
        """Affiche rapport dtaill"""
        logger.info("\n" + "="*80)
        logger.info(" DETAILED LOAD TEST REPORT")
        logger.info("="*80)
        
        logger.info("\n[CONFIG]")
        for key, value in asdict(results.config).items():
            logger.info(f"  {key:<25}: {value}")
        
        logger.info("\n[OVERALL RESULTS]")
        logger.info(f"  Duration: {(results.end_time - results.start_time).total_seconds():.2f}s")
        logger.info(f"  Total Requests: {results.total_requests}")
        logger.info(f"  Successful Requests: {results.successful_requests}")
        logger.info(f"  Failed Requests: {results.failed_requests}")
        logger.info(f"  Error Rate: {results.error_rate_percent:.2f}%")
        
        logger.info("\n[PERFORMANCE]")
        logger.info(f"  Avg Response Time: {results.avg_response_time_ms:.2f}ms")
        logger.info(f"  P50 Response Time: {results.p50_response_time_ms:.2f}ms")
        logger.info(f"  P95 Response Time: {results.p95_response_time_ms:.2f}ms")
        logger.info(f"  P99 Response Time: {results.p99_response_time_ms:.2f}ms")
        
        logger.info("\n[THROUGHPUT]")
        logger.info(f"  Avg Throughput: {results.requests_per_second:.2f} rps")
        logger.info(f"  Peak Throughput: {results.peak_throughput_rps:.2f} rps")
        
        logger.info("\n[SLA VALIDATION]")
        logger.info(f"  Latency SLA (P95 < {results.config.target_latency_p95_ms}ms): {'✅ PASS' if results.meets_latency_sla else '❌ FAIL'}")
        logger.info(f"  Throughput SLA (> {results.config.target_throughput_rps} rps): {'✅ PASS' if results.meets_throughput_sla else '❌ FAIL'}")
        logger.info(f"  Error Rate SLA (< {results.config.max_error_rate_percent}%): {'✅ PASS' if results.meets_error_rate_sla else '❌ FAIL'}")
        
        logger.info("\n[CONCLUSION]")
        logger.info(f"  Overall Result: {'✅✅✅ SUCCESS ✅✅✅' if results.overall_success else '❌❌❌ FAILURE ❌❌❌'}")
        
        if results.error_types:
            logger.warning("\n[ERROR DETAILS]")
            for error, count in results.error_types.items():
                logger.warning(f"  - {error}: {count} occurrences")
        
        logger.info("\n" + "="*80)

# Tests unitaires et fonctions utilitaires
async def run_quick_load_test(users: int = 100, duration: int = 60) -> LoadTestResults:
    """Test de charge rapide pour validation"""
    config = LoadTestConfig(
        max_concurrent_users=users,
        test_duration=duration,
        ramp_up_duration=10,
        ramp_down_duration=5
    )
    
    orchestrator = LoadTestOrchestrator(config)
    return await orchestrator.run_load_test()

async def run_full_load_test() -> LoadTestResults:
    """Test de charge complet 1000+ users"""
    config = LoadTestConfig(
        max_concurrent_users=1000,
        test_duration=300,  # 5 minutes
        ramp_up_duration=60,
        ramp_down_duration=30
    )
    
    orchestrator = LoadTestOrchestrator(config)
    return await orchestrator.run_load_test()

async def main():
    """Point d'entre principal pour les tests"""
    
    config = LoadTestConfig(
        max_concurrent_users=1000,
        test_duration=300,
        ramp_up_duration=30,
        ramp_down_duration=15
    )
    
    orchestrator = LoadTestOrchestrator(config)
    results = await orchestrator.run_load_test()
    
    orchestrator.print_detailed_report(results)
    
    # Dclencher une alerte si le test choue
    if not results.overall_success:
        logger.critical("LOAD TEST FAILED - PERFORMANCE REGRESSION DETECTED")
        # Ici, on pourrait intgrer un systme d'alerte (PagerDuty, Slack, etc.)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Test de charge interrompu par l'utilisateur.")
    except Exception as e:
        logger.critical(f"Erreur inattendue durant le test de charge: {e}", exc_info=True) 



