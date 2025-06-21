#!/usr/bin/env python3
"""
⚡ AGENT 19 - AUDITEUR PERFORMANCE
Mission : Audit et optimisation des performances

Responsabilités :
- Analyse des performances du code
- Détection des goulots d'étranglement
- Optimisation algorithmes
- Monitoring ressources système
"""

import asyncio
from logging_manager_optimized import LoggingManager
import time
import psutil
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import json
import re
from dataclasses import dataclass
from enum import Enum
import sys

class PerformanceLevel(Enum):
    EXCELLENT = "excellent"
    GOOD = "bon"
    AVERAGE = "moyen"
    POOR = "faible"
    CRITICAL = "critique"

@dataclass
class PerformanceMetric:
    metric_id: str
    metric_type: str
    value: float
    benchmark: float
    level: PerformanceLevel
    location: str
    recommendations: List[str]

class Agent19AuditeurPerformance:
    """⚡ Agent 19 - Auditeur Performance"""
    
    def __init__(self):
        self.agent_id = "19"
        self.specialite = "Audit Performance"
        
        # Anti-patterns performance
        self.antipatterns = {
            'nested_loops': r'for\s+\w+.*:\s*\n\s*for\s+\w+',
            'inefficient_concat': r'\+\s*=\s*["\']',
            'blocking_calls': r'time\.sleep\(|requests\.',
            'large_files': r'\.read\(\)|\.readlines\(\)'
        }
        
        self.benchmarks = {
            'cpu_max': 80.0,
            'memory_max': 85.0,
            'execution_max': 5.0,
            'complexity_max': 10
        }
        
        self.logger = self._setup_logging()

    def _setup_logging(self):
        # LoggingManager NextGeneration - Agent
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_agent_logger(
            agent_name="from",
            role="ai_processor",
            domain="performance",
            async_enabled=True
        )
        log_dir = Path("nextgeneration/agent_factory_implementation/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        handler = logging.FileHandler(
            log_dir / f"agent_{self.agent_id}_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - Agent19 - %(levelname)s - %(message)s'
        ))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    async def auditer_performance(self, target_path: str) -> Dict[str, Any]:
        """Audit de performance complet"""
        self.logger.info(f"⚡ Audit performance : {target_path}")
        
        start_time = time.time()
        metrics = []
        
        target = Path(target_path)
        
        if target.is_file():
            metrics.extend(await self._audit_file(str(target)))
        elif target.is_dir():
            for file_path in target.rglob('*.py'):
                metrics.extend(await self._audit_file(str(file_path)))
        
        # Métriques système
        metrics.extend(self._collect_system_metrics())
        
        execution_time = time.time() - start_time
        
        rapport = {
            'audit_id': f"PERF_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'target': target_path,
            'execution_time': execution_time,
            'metrics': [self._serialize_metric(m) for m in metrics],
            'score': self._calculate_score(metrics),
            'bottlenecks': self._identify_bottlenecks(metrics),
            'recommendations': self._generate_recommendations(metrics)
        }
        
        await self._save_report(rapport)
        return rapport

    async def _audit_file(self, file_path: str) -> List[PerformanceMetric]:
        """Audit d'un fichier"""
        metrics = []
        
        try:
            content = Path(file_path).read_text(encoding='utf-8', errors='ignore')
            
            # Taille fichier
            line_count = len(content.splitlines())
            if line_count > 500:
                metrics.append(PerformanceMetric(
                    metric_id=f"SIZE_{hash(file_path)}",
                    metric_type="file_size",
                    value=float(line_count),
                    benchmark=500.0,
                    level=self._get_level(line_count, 500),
                    location=file_path,
                    recommendations=["Diviser en modules plus petits"]
                ))
            
            # Anti-patterns
            for pattern_name, pattern in self.antipatterns.items():
                matches = len(re.findall(pattern, content, re.MULTILINE))
                if matches > 0:
                    metrics.append(PerformanceMetric(
                        metric_id=f"PATTERN_{pattern_name}_{hash(file_path)}",
                        metric_type="antipattern",
                        value=float(matches),
                        benchmark=0.0,
                        level=PerformanceLevel.POOR if matches > 3 else PerformanceLevel.AVERAGE,
                        location=file_path,
                        recommendations=self._get_pattern_recommendations(pattern_name)
                    ))
            
        except Exception as e:
            self.logger.error(f"Erreur audit {file_path}: {e}")
        
        return metrics

    def _collect_system_metrics(self) -> List[PerformanceMetric]:
        """Collecte métriques système"""
        metrics = []
        
        # CPU
        cpu = psutil.cpu_percent(interval=1)
        if cpu > 50:
            metrics.append(PerformanceMetric(
                metric_id=f"CPU_{int(time.time())}",
                metric_type="system_cpu",
                value=cpu,
                benchmark=self.benchmarks['cpu_max'],
                level=self._get_level(cpu, self.benchmarks['cpu_max']),
                location="système",
                recommendations=["Optimiser les calculs intensifs"] if cpu > 80 else []
            ))
        
        # Mémoire
        memory = psutil.virtual_memory().percent
        if memory > 50:
            metrics.append(PerformanceMetric(
                metric_id=f"MEM_{int(time.time())}",
                metric_type="system_memory",
                value=memory,
                benchmark=self.benchmarks['memory_max'],
                level=self._get_level(memory, self.benchmarks['memory_max']),
                location="système",
                recommendations=["Optimiser gestion mémoire"] if memory > 85 else []
            ))
        
        return metrics

    def _get_level(self, value: float, benchmark: float) -> PerformanceLevel:
        """Détermine le niveau de performance"""
        ratio = value / benchmark
        
        if ratio <= 0.5:
            return PerformanceLevel.EXCELLENT
        elif ratio <= 0.7:
            return PerformanceLevel.GOOD
        elif ratio <= 1.0:
            return PerformanceLevel.AVERAGE
        elif ratio <= 1.5:
            return PerformanceLevel.POOR
        else:
            return PerformanceLevel.CRITICAL

    def _get_pattern_recommendations(self, pattern_name: str) -> List[str]:
        """Recommandations par anti-pattern"""
        recommendations = {
            'nested_loops': ["Optimiser algorithmes", "Utiliser structures données efficaces"],
            'inefficient_concat': ["Utiliser join() ou f-strings"],
            'blocking_calls': ["Utiliser opérations asynchrones"],
            'large_files': ["Traiter par chunks", "Utiliser générateurs"]
        }
        return recommendations.get(pattern_name, ["Optimiser le code"])

    def _calculate_score(self, metrics: List[PerformanceMetric]) -> float:
        """Calcule score global"""
        if not metrics:
            return 10.0
        
        scores = {
            PerformanceLevel.EXCELLENT: 10,
            PerformanceLevel.GOOD: 8,
            PerformanceLevel.AVERAGE: 6,
            PerformanceLevel.POOR: 4,
            PerformanceLevel.CRITICAL: 2
        }
        
        total = sum(scores.get(m.level, 6) for m in metrics)
        return round(total / len(metrics), 1)

    def _identify_bottlenecks(self, metrics: List[PerformanceMetric]) -> List[str]:
        """Identifie goulots d'étranglement"""
        bottlenecks = []
        
        critical = [m for m in metrics if m.level == PerformanceLevel.CRITICAL]
        poor = [m for m in metrics if m.level == PerformanceLevel.POOR]
        
        for m in critical:
            bottlenecks.append(f"🚨 CRITIQUE: {m.metric_type} ({m.location})")
        
        for m in poor[:3]:
            bottlenecks.append(f"⚠️ PROBLÈME: {m.metric_type} ({m.location})")
        
        return bottlenecks

    def _generate_recommendations(self, metrics: List[PerformanceMetric]) -> List[str]:
        """Génère recommandations"""
        recs = set()
        
        for m in metrics:
            if m.level in [PerformanceLevel.POOR, PerformanceLevel.CRITICAL]:
                recs.update(m.recommendations)
        
        recs.add("🔄 Implémenter cache pour opérations coûteuses")
        recs.add("📊 Monitoring performances continu")
        
        return list(recs)

    def _serialize_metric(self, metric: PerformanceMetric) -> Dict[str, Any]:
        """Sérialise métrique"""
        return {
            'metric_id': metric.metric_id,
            'metric_type': metric.metric_type,
            'value': metric.value,
            'benchmark': metric.benchmark,
            'level': metric.level.value,
            'location': metric.location,
            'recommendations': metric.recommendations
        }

    async def _save_report(self, rapport: Dict[str, Any]):
        """Sauvegarde rapport"""
        try:
            reports_dir = Path("nextgeneration/agent_factory_implementation/reports/performance")
            reports_dir.mkdir(parents=True, exist_ok=True)
            
            report_file = reports_dir / f"performance_report_{rapport['audit_id']}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(rapport, f, indent=2, ensure_ascii=False)
                
            self.logger.info(f"Rapport sauvegardé : {report_file}")
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde : {e}")

async def main():
    """Point d'entrée"""
    print("⚡ Agent 19 - Auditeur Performance")
    
    agent = Agent19AuditeurPerformance()
    
    target = "nextgeneration/agent_factory_implementation/agents"
    if Path(target).exists():
        rapport = await agent.auditer_performance(target)
        
        print(f"\n📊 AUDIT PERFORMANCE")
        print(f"Score : {rapport['score']}/10")
        print(f"Temps : {rapport['execution_time']:.2f}s")
        print(f"Métriques : {len(rapport['metrics'])}")
        
        if rapport['bottlenecks']:
            print(f"\n🚨 GOULOTS :")
            for bottleneck in rapport['bottlenecks'][:3]:
                print(f"  {bottleneck}")

if __name__ == "__main__":
    asyncio.run(main()) 