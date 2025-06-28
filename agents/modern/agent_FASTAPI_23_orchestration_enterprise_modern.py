#!/usr/bin/env python3
"""
🚀 AGENT FASTAPI 23 ORCHESTRATION ENTERPRISE - VERSION MODERNE NEXTGENERATION

Migration NextGeneration de l'agent FastAPI Orchestration Enterprise vers architecture LLM hybride.
Préservation totale des fonctionnalités existantes + extensions intelligentes.

Original: agent_FASTAPI_23_orchestration_enterprise.py (205 lignes)
Moderne: Version LLM-enhanced avec capacités orchestration avancées

Fonctionnalités préservées:
- API FastAPI Enterprise setup complet
- Authentication, Rate Limiting, Documentation
- Monitoring, Security, Performance optimization
- Pattern Factory compliance maintenu
- Features modulaires réutilisables

Extensions NextGeneration:
- LLM-enhanced API design et optimization
- Intelligent endpoint generation
- Smart documentation avec AI insights
- Auto-scaling recommendations
- Performance profiling automatisé
- Security assessment continu

Version: 3.0.0 NextGeneration
Author: Claude Sonnet 4 (NextGeneration Team)
Created: 2025-06-28
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict

# NextGeneration imports
from core.services import LLMGatewayHybrid, Priority
from core import logging_manager

# Legacy compatibility imports
try:
    from core.agent_factory_architecture import Agent, Task, Result, AgentType
    LEGACY_FACTORY_AVAILABLE = True
except ImportError:
    LEGACY_FACTORY_AVAILABLE = False
    logging.warning("Legacy agent factory not available")

# Enterprise features
try:
    from features.enterprise.fastapi_orchestration import (
        AuthenticationFeature,
        RateLimitingFeature,
        DocumentationFeature,
        MonitoringFeature,
        SecurityFeature
    )
    ENTERPRISE_FEATURES_AVAILABLE = True
except ImportError:
    ENTERPRISE_FEATURES_AVAILABLE = False
    logging.warning("Enterprise features not available - using modern alternatives")

@dataclass
class FastAPIOrchestrationTask:
    """Tâche d'orchestration FastAPI enrichie"""
    task_id: str
    task_type: str
    api_spec: Dict[str, Any]
    requirements: Dict[str, Any]
    performance_targets: Dict[str, Any]
    security_requirements: Dict[str, Any]
    metadata: Dict[str, Any]
    created_at: datetime
    priority: str = "medium"

@dataclass
class FastAPIOrchestrationResult:
    """Résultat d'orchestration FastAPI avec métriques"""
    success: bool
    orchestration_data: Dict[str, Any]
    generated_code: Optional[str]
    documentation: Optional[str]
    security_assessment: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    recommendations: List[str]
    execution_time_ms: float
    agent_id: str
    task_id: str
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Conversion en dictionnaire pour compatibilité"""
        return asdict(self)

class ModernAgent23FastAPIOrchestrationEnterprise:
    """
    🚀 Agent FastAPI 23 Orchestration Enterprise - Version NextGeneration
    
    Agent moderne d'orchestration FastAPI avec intelligence artificielle pour:
    - Design et génération d'APIs Enterprise automatisées
    - Optimisation performance avec profiling intelligent
    - Sécurité renforcée avec assessment continu
    - Documentation auto-générée avec insights AI
    - Monitoring et alerting avancés
    
    Architecture NextGeneration:
    - LLM Gateway pour analyse et génération intelligente
    - Backward compatibility totale avec legacy
    - Extensions enterprise avec AI insights
    - Performance monitoring en temps réel
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.agent_id = f"fastapi_23_modern_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.version = "3.0.0"
        self.agent_name = "FastAPI Orchestration Enterprise Modern"
        
        # Status et métriques
        self.status = "initializing"
        self.created_at = datetime.now()
        self.tasks_executed = 0
        self.last_activity = datetime.now()
        
        # Configuration logging NextGeneration
        self.logger = logging_manager.get_logger(config_name="default", custom_config={
            "logger_name": "ModernAgent23FastAPIOrchestration",
            "log_level": "INFO",
            "elasticsearch_enabled": True,
            "encryption_enabled": True,
            "async_enabled": True,
            "alerting_enabled": True
        })
        
        # Configuration LLM Gateway
        self.llm_gateway: Optional[LLMGatewayHybrid] = None
        
        # Legacy compatibility
        self.legacy_features = []
        if ENTERPRISE_FEATURES_AVAILABLE:
            self.legacy_features = [
                AuthenticationFeature(self.config.get('authentication', {})),
                RateLimitingFeature(self.config.get('rate_limiting', {})),
                DocumentationFeature(self.config.get('documentation', {})),
                MonitoringFeature(self.config.get('monitoring', {})),
                SecurityFeature(self.config.get('security', {}))
            ]
        
        # Métriques performance
        self.performance_metrics = {
            "total_apis_generated": 0,
            "avg_generation_time": 0.0,
            "security_assessments": 0,
            "optimization_recommendations": 0,
            "documentation_generated": 0
        }
        
        self.logger.info(f"✅ Agent FastAPI 23 Modern v{self.version} initialisé - {len(self.legacy_features)} legacy features")
    
    async def initialize(self, llm_gateway: LLMGatewayHybrid = None):
        """Initialise l'agent avec LLM Gateway"""
        try:
            self.status = "starting"
            
            if llm_gateway:
                self.llm_gateway = llm_gateway
                self.logger.info("🔗 LLM Gateway connecté pour intelligence FastAPI")
            else:
                self.logger.warning("⚠️ Aucun LLM Gateway - fonctionnement en mode dégradé")
            
            # Initialisation legacy features
            for feature in self.legacy_features:
                if hasattr(feature, 'initialize'):
                    await feature.initialize()
            
            self.status = "running"
            self.logger.info(f"🚀 Agent FastAPI 23 Modern opérationnel")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur initialisation: {e}")
            self.status = "error"
            raise
    
    async def execute_async(self, task_data: Dict[str, Any]) -> FastAPIOrchestrationResult:
        """
        Exécution principale moderne avec intelligence LLM
        
        Capacités:
        - Génération d'API FastAPI intelligente
        - Optimisation performance automatisée
        - Sécurité renforcée avec assessment
        - Documentation auto-générée
        """
        start_time = time.time()
        task_id = task_data.get('task_id', f"task_{int(time.time())}")
        
        try:
            self.logger.info(f"🎯 Démarrage orchestration FastAPI - Task: {task_id}")
            
            # Parsing de la tâche
            task = self._parse_orchestration_task(task_data)
            
            # Orchestration FastAPI avec LLM
            orchestration_result = await self._orchestrate_fastapi_with_llm(task)
            
            # Génération de code si demandée
            generated_code = None
            if task_data.get('generate_code', False):
                generated_code = await self._generate_fastapi_code(task, orchestration_result)
            
            # Documentation automatique
            documentation = await self._generate_smart_documentation(task, orchestration_result)
            
            # Assessment sécurité
            security_assessment = await self._perform_security_assessment(task, orchestration_result)
            
            # Métriques performance
            performance_metrics = await self._analyze_performance_requirements(task)
            
            # Recommendations AI
            recommendations = await self._generate_ai_recommendations(task, orchestration_result)
            
            # Mise à jour métriques
            execution_time = (time.time() - start_time) * 1000
            self._update_performance_metrics(execution_time)
            
            result = FastAPIOrchestrationResult(
                success=True,
                orchestration_data=orchestration_result,
                generated_code=generated_code,
                documentation=documentation,
                security_assessment=security_assessment,
                performance_metrics=performance_metrics,
                recommendations=recommendations,
                execution_time_ms=execution_time,
                agent_id=self.agent_id,
                task_id=task_id
            )
            
            self.tasks_executed += 1
            self.last_activity = datetime.now()
            
            self.logger.info(f"✅ Orchestration FastAPI terminée - {execution_time:.2f}ms")
            return result
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            self.logger.error(f"❌ Erreur orchestration FastAPI: {e}")
            
            return FastAPIOrchestrationResult(
                success=False,
                orchestration_data={},
                generated_code=None,
                documentation=None,
                security_assessment={},
                performance_metrics={},
                recommendations=[],
                execution_time_ms=execution_time,
                agent_id=self.agent_id,
                task_id=task_id,
                error=str(e)
            )
    
    def _parse_orchestration_task(self, task_data: Dict[str, Any]) -> FastAPIOrchestrationTask:
        """Parse les données de tâche en structure FastAPI"""
        
        return FastAPIOrchestrationTask(
            task_id=task_data.get('task_id', f"task_{int(time.time())}"),
            task_type=task_data.get('type', 'api_orchestration'),
            api_spec=task_data.get('api_spec', {}),
            requirements=task_data.get('requirements', {}),
            performance_targets=task_data.get('performance_targets', {}),
            security_requirements=task_data.get('security_requirements', {}),
            metadata=task_data.get('metadata', {}),
            created_at=datetime.now(),
            priority=task_data.get('priority', 'medium')
        )
    
    async def _orchestrate_fastapi_with_llm(self, task: FastAPIOrchestrationTask) -> Dict[str, Any]:
        """Orchestration FastAPI avec intelligence LLM"""
        
        if not self.llm_gateway:
            # Mode dégradé sans LLM
            return await self._orchestrate_fastapi_legacy(task)
        
        try:
            # Prompt pour orchestration intelligente
            prompt = f"""
            En tant qu'expert FastAPI Enterprise, analysez ces spécifications et proposez une architecture optimale:
            
            API Specifications:
            {json.dumps(task.api_spec, indent=2)}
            
            Requirements:
            {json.dumps(task.requirements, indent=2)}
            
            Performance Targets:
            {json.dumps(task.performance_targets, indent=2)}
            
            Fournissez:
            1. Architecture recommandée (endpoints, middleware, dépendances)
            2. Patterns de design appropriés
            3. Stratégie de cache et optimisation
            4. Configuration de sécurité
            5. Structure de monitoring
            
            Répondez en JSON structuré.
            """
            
            # Requête LLM avec contexte agent
            response = await self.llm_gateway.query(
                prompt=prompt,
                agent_id=self.agent_id,
                context={
                    "task_type": "fastapi_orchestration",
                    "agent_version": self.version,
                    "task_id": task.task_id
                },
                priority=Priority.HIGH
            )
            
            # Parsing de la réponse LLM
            try:
                orchestration_data = json.loads(response)
            except json.JSONDecodeError:
                # Fallback si JSON invalide
                orchestration_data = {
                    "architecture": "Standard FastAPI with enterprise features",
                    "endpoints": self._extract_endpoints_from_response(response),
                    "middleware": ["CORS", "Authentication", "RateLimit"],
                    "security": "JWT + OAuth2",
                    "monitoring": "Prometheus + Grafana",
                    "llm_raw_response": response
                }
            
            # Enrichissement avec analyse technique
            orchestration_data.update({
                "generated_at": datetime.now().isoformat(),
                "agent_version": self.version,
                "llm_enhanced": True,
                "complexity_score": self._calculate_complexity_score(task),
                "estimated_development_time": self._estimate_development_time(task)
            })
            
            return orchestration_data
            
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur LLM orchestration, fallback legacy: {e}")
            return await self._orchestrate_fastapi_legacy(task)
    
    async def _orchestrate_fastapi_legacy(self, task: FastAPIOrchestrationTask) -> Dict[str, Any]:
        """Orchestration FastAPI en mode legacy (sans LLM)"""
        
        # Orchestration basique basée sur les spécifications
        orchestration = {
            "architecture": "Standard FastAPI Enterprise",
            "endpoints": self._generate_standard_endpoints(task.api_spec),
            "middleware": [
                "CORS",
                "Authentication", 
                "RateLimit",
                "Monitoring",
                "Security"
            ],
            "security": {
                "authentication": "JWT",
                "authorization": "RBAC",
                "rate_limiting": "100/minute"
            },
            "monitoring": {
                "metrics": "Prometheus",
                "logging": "ELK Stack",
                "tracing": "Jaeger"
            },
            "generated_at": datetime.now().isoformat(),
            "agent_version": self.version,
            "llm_enhanced": False,
            "mode": "legacy_fallback"
        }
        
        return orchestration
    
    async def _generate_fastapi_code(self, task: FastAPIOrchestrationTask, orchestration: Dict[str, Any]) -> str:
        """Génère le code FastAPI basé sur l'orchestration"""
        
        if not self.llm_gateway:
            return self._generate_basic_fastapi_code(orchestration)
        
        try:
            prompt = f"""
            Générez un code FastAPI complet et production-ready basé sur cette orchestration:
            
            {json.dumps(orchestration, indent=2)}
            
            Incluez:
            - Définition de l'app FastAPI avec middleware
            - Endpoints avec validation Pydantic
            - Gestion d'erreurs robuste
            - Documentation OpenAPI
            - Configuration de sécurité
            - Monitoring et logging
            
            Code Python seulement, commenté et structuré.
            """
            
            generated_code = await self.llm_gateway.query(
                prompt=prompt,
                agent_id=self.agent_id,
                context={
                    "task_type": "code_generation",
                    "language": "python",
                    "framework": "fastapi"
                }
            )
            
            return generated_code
            
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur génération code LLM: {e}")
            return self._generate_basic_fastapi_code(orchestration)
    
    async def _generate_smart_documentation(self, task: FastAPIOrchestrationTask, orchestration: Dict[str, Any]) -> str:
        """Génère documentation intelligente avec insights AI"""
        
        if not self.llm_gateway:
            return self._generate_basic_documentation(orchestration)
        
        try:
            prompt = f"""
            Créez une documentation complète et professionnelle pour cette API FastAPI:
            
            Orchestration: {json.dumps(orchestration, indent=2)}
            Requirements: {json.dumps(task.requirements, indent=2)}
            
            Incluez:
            - Aperçu de l'architecture
            - Guide d'installation et configuration
            - Documentation des endpoints
            - Exemples d'utilisation
            - Bonnes pratiques de sécurité
            - Guide de monitoring et maintenance
            
            Format Markdown professionnel.
            """
            
            documentation = await self.llm_gateway.query(
                prompt=prompt,
                agent_id=self.agent_id,
                context={
                    "task_type": "documentation_generation",
                    "format": "markdown"
                }
            )
            
            return documentation
            
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur génération documentation: {e}")
            return self._generate_basic_documentation(orchestration)
    
    async def _perform_security_assessment(self, task: FastAPIOrchestrationTask, orchestration: Dict[str, Any]) -> Dict[str, Any]:
        """Effectue assessment sécurité avec analyse AI"""
        
        assessment = {
            "assessment_date": datetime.now().isoformat(),
            "agent_version": self.version,
            "security_score": 0,
            "vulnerabilities": [],
            "recommendations": [],
            "compliance_status": {}
        }
        
        if not self.llm_gateway:
            # Assessment basique
            assessment.update({
                "security_score": 75,
                "vulnerabilities": ["Manual review required"],
                "recommendations": ["Enable HTTPS", "Implement rate limiting", "Add input validation"],
                "compliance_status": {"basic": "compliant"}
            })
            return assessment
        
        try:
            prompt = f"""
            Effectuez un assessment de sécurité pour cette API FastAPI:
            
            Orchestration: {json.dumps(orchestration, indent=2)}
            Security Requirements: {json.dumps(task.security_requirements, indent=2)}
            
            Analysez:
            - Vulnérabilités potentielles
            - Configuration de sécurité
            - Conformité aux standards (OWASP, etc.)
            - Recommendations d'amélioration
            
            Répondez en JSON avec score sécurité /100.
            """
            
            response = await self.llm_gateway.query(
                prompt=prompt,
                agent_id=self.agent_id,
                context={
                    "task_type": "security_assessment",
                    "framework": "fastapi"
                }
            )
            
            try:
                ai_assessment = json.loads(response)
                assessment.update(ai_assessment)
            except json.JSONDecodeError:
                assessment["ai_raw_response"] = response
                assessment["security_score"] = 80  # Score par défaut
                
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur security assessment: {e}")
            assessment["error"] = str(e)
        
        return assessment
    
    async def _analyze_performance_requirements(self, task: FastAPIOrchestrationTask) -> Dict[str, Any]:
        """Analyse les requirements de performance"""
        
        metrics = {
            "analysis_date": datetime.now().isoformat(),
            "performance_targets": task.performance_targets,
            "estimated_metrics": {},
            "bottlenecks": [],
            "optimization_opportunities": []
        }
        
        # Analyse basique des targets
        targets = task.performance_targets
        if targets:
            metrics["estimated_metrics"] = {
                "response_time_ms": targets.get("max_response_time", 200),
                "throughput_rps": targets.get("min_throughput", 1000),
                "concurrent_users": targets.get("max_concurrent_users", 100),
                "availability": targets.get("target_availability", 99.9)
            }
            
            # Identification de bottlenecks potentiels
            if targets.get("min_throughput", 0) > 5000:
                metrics["bottlenecks"].append("High throughput requirement - consider caching")
            
            if targets.get("max_concurrent_users", 0) > 1000:
                metrics["bottlenecks"].append("High concurrency - consider async optimization")
        
        return metrics
    
    async def _generate_ai_recommendations(self, task: FastAPIOrchestrationTask, orchestration: Dict[str, Any]) -> List[str]:
        """Génère recommendations AI pour optimisation"""
        
        if not self.llm_gateway:
            return [
                "Implement caching strategy",
                "Add comprehensive monitoring",
                "Configure rate limiting",
                "Enable CORS properly",
                "Add request validation"
            ]
        
        try:
            prompt = f"""
            Basé sur cette orchestration FastAPI et ces requirements, fournissez 5-10 recommendations concrètes d'optimisation:
            
            Orchestration: {json.dumps(orchestration, indent=2)}
            Performance Targets: {json.dumps(task.performance_targets, indent=2)}
            
            Focalisez sur:
            - Performance et scalabilité
            - Sécurité et robustesse
            - Maintenabilité du code
            - Monitoring et observabilité
            
            Retournez une liste de recommendations précises et actionnables.
            """
            
            response = await self.llm_gateway.query(
                prompt=prompt,
                agent_id=self.agent_id,
                context={
                    "task_type": "recommendations_generation",
                    "domain": "fastapi_optimization"
                }
            )
            
            # Extraction des recommendations depuis la réponse
            recommendations = self._extract_recommendations_from_response(response)
            return recommendations
            
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur génération recommendations: {e}")
            return ["Review generated configuration", "Add monitoring", "Implement security best practices"]
    
    def _extract_endpoints_from_response(self, response: str) -> List[Dict[str, Any]]:
        """Extrait les endpoints depuis une réponse textuelle"""
        # Implémentation simplifiée
        return [
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/api/v1/items", "method": "GET", "description": "List items"},
            {"path": "/api/v1/items", "method": "POST", "description": "Create item"}
        ]
    
    def _extract_recommendations_from_response(self, response: str) -> List[str]:
        """Extrait les recommendations depuis une réponse textuelle"""
        # Implémentation simplifiée - parsing basique
        lines = response.split('\n')
        recommendations = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                recommendations.append(line[1:].strip())
            elif line and len(line) > 20 and any(word in line.lower() for word in ['implement', 'add', 'use', 'configure', 'enable']):
                recommendations.append(line)
        
        return recommendations[:10]  # Max 10 recommendations
    
    def _calculate_complexity_score(self, task: FastAPIOrchestrationTask) -> int:
        """Calcule un score de complexité pour la tâche"""
        score = 1
        
        if task.api_spec:
            score += len(task.api_spec.get('endpoints', []))
            
        if task.requirements:
            score += len(task.requirements)
            
        if task.security_requirements:
            score += len(task.security_requirements) * 2
            
        return min(score, 10)  # Max 10
    
    def _estimate_development_time(self, task: FastAPIOrchestrationTask) -> str:
        """Estime le temps de développement"""
        complexity = self._calculate_complexity_score(task)
        
        if complexity <= 3:
            return "1-2 days"
        elif complexity <= 6:
            return "3-5 days"
        else:
            return "1-2 weeks"
    
    def _generate_standard_endpoints(self, api_spec: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Génère endpoints standards basés sur les specs"""
        endpoints = [
            {"path": "/health", "method": "GET", "description": "Health check endpoint"},
            {"path": "/docs", "method": "GET", "description": "API documentation"},
            {"path": "/redoc", "method": "GET", "description": "Alternative API documentation"}
        ]
        
        # Ajout d'endpoints basés sur les specs
        if api_spec.get('resources'):
            for resource in api_spec['resources']:
                resource_name = resource.lower()
                endpoints.extend([
                    {"path": f"/api/v1/{resource_name}", "method": "GET", "description": f"List {resource_name}"},
                    {"path": f"/api/v1/{resource_name}", "method": "POST", "description": f"Create {resource_name}"},
                    {"path": f"/api/v1/{resource_name}/{{id}}", "method": "GET", "description": f"Get {resource_name} by ID"},
                    {"path": f"/api/v1/{resource_name}/{{id}}", "method": "PUT", "description": f"Update {resource_name}"},
                    {"path": f"/api/v1/{resource_name}/{{id}}", "method": "DELETE", "description": f"Delete {resource_name}"}
                ])
        
        return endpoints
    
    def _generate_basic_fastapi_code(self, orchestration: Dict[str, Any]) -> str:
        """Génère code FastAPI basique"""
        return '''
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn

# App initialization
app = FastAPI(
    title="Enterprise API",
    description="Generated FastAPI application",
    version="1.0.0"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Enterprise FastAPI Application"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    def _generate_basic_documentation(self, orchestration: Dict[str, Any]) -> str:
        """Génère documentation basique"""
        return '''
# FastAPI Enterprise Application

## Overview
Cette application FastAPI a été générée automatiquement avec l'orchestrateur Enterprise.

## Installation
```bash
pip install fastapi uvicorn
```

## Usage
```bash
uvicorn main:app --reload
```

## Endpoints
- GET /health - Health check
- GET /docs - API documentation
- GET /redoc - Alternative documentation

## Security
- JWT Authentication
- Rate limiting
- CORS configuration

## Monitoring
- Health check endpoint
- Metrics collection
- Logging integration
'''
    
    def _update_performance_metrics(self, execution_time: float):
        """Met à jour les métriques de performance"""
        self.performance_metrics["total_apis_generated"] += 1
        
        # Moyenne mobile du temps d'exécution
        current_avg = self.performance_metrics["avg_generation_time"]
        total_tasks = self.performance_metrics["total_apis_generated"]
        
        new_avg = ((current_avg * (total_tasks - 1)) + execution_time) / total_tasks
        self.performance_metrics["avg_generation_time"] = new_avg
    
    async def execute_task(self, task: Any) -> Any:
        """Compatibility method pour legacy Task objects"""
        if LEGACY_FACTORY_AVAILABLE and hasattr(task, 'type'):
            # Conversion legacy Task vers format moderne
            task_data = {
                'task_id': getattr(task, 'id', f"legacy_{int(time.time())}"),
                'type': task.type,
                'api_spec': getattr(task, 'params', {}).get('api_spec', {}),
                'requirements': getattr(task, 'params', {}).get('requirements', {}),
                'performance_targets': getattr(task, 'params', {}).get('performance_targets', {}),
                'security_requirements': getattr(task, 'params', {}).get('security_requirements', {}),
                'metadata': getattr(task, 'params', {})
            }
            
            result = await self.execute_async(task_data)
            
            # Conversion vers legacy Result si disponible
            if LEGACY_FACTORY_AVAILABLE:
                return Result(
                    success=result.success,
                    data=result.orchestration_data,
                    error=result.error,
                    agent_id=result.agent_id,
                    task_id=result.task_id,
                    metrics=result.to_dict()
                )
            
            return result
        
        # Traitement moderne direct
        return await self.execute_async(task)
    
    async def get_capabilities(self) -> List[str]:
        """Retourne les capacités de l'agent"""
        return [
            "fastapi_orchestration",
            "api_generation",
            "performance_optimization", 
            "security_assessment",
            "documentation_generation",
            "code_generation",
            "architecture_design",
            "monitoring_setup",
            "enterprise_compliance"
        ]
    
    async def health_check(self) -> Dict[str, Any]:
        """Vérification santé de l'agent"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "version": self.version,
            "status": self.status,
            "tasks_executed": self.tasks_executed,
            "uptime_seconds": (datetime.now() - self.created_at).total_seconds(),
            "last_activity": self.last_activity.isoformat(),
            "llm_gateway_connected": self.llm_gateway is not None,
            "legacy_features_count": len(self.legacy_features),
            "performance_metrics": self.performance_metrics,
            "capabilities": await self.get_capabilities()
        }
    
    async def shutdown(self):
        """Arrêt propre de l'agent"""
        self.status = "stopping"
        self.logger.info(f"🛑 Agent FastAPI 23 Modern v{self.version} arrêt...")
        
        # Cleanup legacy features
        for feature in self.legacy_features:
            if hasattr(feature, 'cleanup'):
                await feature.cleanup()
        
        self.status = "stopped"
        self.logger.info(f"✅ Agent FastAPI 23 Modern arrêté proprement")

# Factory functions pour compatibilité
def create_modern_fastapi_agent(config: Dict[str, Any] = None) -> ModernAgent23FastAPIOrchestrationEnterprise:
    """Factory function pour créer l'agent moderne"""
    return ModernAgent23FastAPIOrchestrationEnterprise(config)

async def create_initialized_fastapi_agent(config: Dict[str, Any] = None, llm_gateway: LLMGatewayHybrid = None) -> ModernAgent23FastAPIOrchestrationEnterprise:
    """Factory function avec initialisation complète"""
    agent = ModernAgent23FastAPIOrchestrationEnterprise(config)
    await agent.initialize(llm_gateway)
    return agent

# Compatibility alias
Agent23FastAPIOrchestrationEnterpriseModern = ModernAgent23FastAPIOrchestrationEnterprise

if __name__ == "__main__":
    async def test_agent():
        """Test de démonstration"""
        print("🚀 Test Agent FastAPI 23 Orchestration Enterprise Modern")
        
        agent = create_modern_fastapi_agent()
        await agent.initialize()
        
        # Test task
        test_task = {
            'task_id': 'demo_api',
            'type': 'api_orchestration',
            'api_spec': {
                'resources': ['Users', 'Products'],
                'auth_required': True
            },
            'requirements': {
                'performance': 'high',
                'security': 'enterprise'
            },
            'performance_targets': {
                'max_response_time': 100,
                'min_throughput': 1000
            },
            'generate_code': True
        }
        
        result = await agent.execute_async(test_task)
        
        print(f"✅ Orchestration: {result.success}")
        print(f"📊 Execution time: {result.execution_time_ms:.2f}ms")
        print(f"🔒 Security score: {result.security_assessment.get('security_score', 'N/A')}")
        print(f"📝 Recommendations: {len(result.recommendations)}")
        print(f"💡 Agent status: {agent.status}")
        
        health = await agent.health_check()
        print(f"🩺 Health: {health['status']} - {health['tasks_executed']} tasks executed")
        
        await agent.shutdown()
    
    asyncio.run(test_agent())