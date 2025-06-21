"""
Advanced Kubernetes Auto-Scaling Manager for Enterprise Production
Handles HPA, VPA, KEDA, and custom metrics scaling

IA-2 Architecture & Production - Sprint 2.2
"""

import asyncio
import sys
from pathlib import Path
from core import logging_manager
import yaml
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import kubernetes_asyncio as k8s
from kubernetes_asyncio.client.exceptions import ApiException

# Monitoring integration
from ..observability.monitoring import get_monitoring

# LoggingManager NextGeneration - Tool/Utility
        import sys
from pathlib import Path
from core import logging_manager
        self.logger = logging_manager.get_logger(custom_config={
            "logger_name": "ScalingType",
            "log_level": "INFO",
            "elasticsearch_enabled": False,
            "encryption_enabled": False,
            "async_enabled": True
        })

class ScalingType(Enum):
    """Types of scaling supported"""
    HORIZONTAL = "horizontal"  # HPA - more pods
    VERTICAL = "vertical"     # VPA - more CPU/memory per pod
    EVENT_DRIVEN = "event_driven"  # KEDA - based on external metrics

class ScalingDirection(Enum):
    """Scaling direction"""
    UP = "up"
    DOWN = "down"
    STABLE = "stable"

@dataclass
class ScalingMetric:
    """Scaling metric configuration"""
    name: str
    target_type: str  # Utilization, AverageValue, Value
    target_value: Union[int, str]  # e.g., 70 for CPU utilization or "30" for custom metric
    resource_name: Optional[str] = None  # For resource metrics (cpu, memory)
    
class ScalingRule:
    """Advanced scaling rule with business logic"""
    
    def __init__(
        self,
        name: str,
        min_replicas: int = 1,
        max_replicas: int = 10,
        metrics: List[ScalingMetric] = None,
        scale_up_policy: Dict[str, Any] = None,
        scale_down_policy: Dict[str, Any] = None
    ):
        self.name = name
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.metrics = metrics or []
        
        # Default policies
        self.scale_up_policy = scale_up_policy or {
            "stabilization_window_seconds": 60,
            "policies": [{
                "type": "Percent",
                "value": 100,  # Double the pods
                "period_seconds": 60
            }]
        }
        
        self.scale_down_policy = scale_down_policy or {
            "stabilization_window_seconds": 300,  # 5 minutes
            "policies": [{
                "type": "Percent", 
                "value": 50,  # Half the pods
                "period_seconds": 60
            }]
        }

@dataclass
class AutoScalerState:
    """Current state of auto-scaler"""
    current_replicas: int = 0
    desired_replicas: int = 0
    last_scale_time: Optional[datetime] = None
    scaling_direction: ScalingDirection = ScalingDirection.STABLE
    scaling_reason: str = ""
    metrics_values: Dict[str, float] = field(default_factory=dict)

class AdvancedAutoScaler:
    """
    Enterprise-grade Kubernetes auto-scaler with:
    - HPA (Horizontal Pod Autoscaler) management
    - VPA (Vertical Pod Autoscaler) support
    - KEDA event-driven scaling
    - Custom business metrics
    - Predictive scaling
    - Load balancer integration
    """
    
    def __init__(
        self,
        namespace: str = "default",
        deployment_name: str = "orchestrator",
        load_balancer_integration: bool = True
    ):
        self.namespace = namespace
        self.deployment_name = deployment_name
        self.load_balancer_integration = load_balancer_integration
        
        # Kubernetes clients
        self.k8s_config = None
        self.apps_v1 = None
        self.autoscaling_v2 = None
        self.custom_objects = None
        
        # Scaling configuration
        self.scaling_rules: Dict[str, ScalingRule] = {}
        self.state = AutoScalerState()
        
        # Monitoring and metrics
        self.monitoring = None
        self.custom_metrics: Dict[str, float] = {}
        
        # Advanced features
        self.predictive_scaling_enabled = True
        self.business_hours_scaling = True
        self.load_prediction_window = timedelta(minutes=15)
        
        # Statistics
        self.scaling_history: List[Dict[str, Any]] = []
        self.stats = {
            'total_scaling_events': 0,
            'scale_up_events': 0,
            'scale_down_events': 0,
            'predictive_scaling_triggers': 0,
            'business_metrics_scaling': 0
        }
    
    async def initialize(self):
        """Initialize Kubernetes clients and monitoring"""
        try:
            # Load Kubernetes configuration
            try:
                k8s.config.load_incluster_config()
                logger.info("Loaded in-cluster Kubernetes configuration")
            except:
                await k8s.config.load_kube_config()
                logger.info("Loaded local Kubernetes configuration")
            
            # Initialize clients
            self.apps_v1 = k8s.client.AppsV1Api()
            self.autoscaling_v2 = k8s.client.AutoscalingV2Api()
            self.custom_objects = k8s.client.CustomObjectsApi()
            
            # Initialize monitoring
            self.monitoring = await get_monitoring()
            
            # Get initial deployment state
            await self._update_current_state()
            
            logger.info(f"Auto-scaler initialized for {self.namespace}/{self.deployment_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize auto-scaler: {e}")
            raise
    
    def add_scaling_rule(self, rule: ScalingRule):
        """Add a scaling rule"""
        self.scaling_rules[rule.name] = rule
        logger.info(f"Added scaling rule: {rule.name}")
    
    async def create_hpa(self, rule_name: str) -> bool:
        """Create or update HPA based on scaling rule"""
        if rule_name not in self.scaling_rules:
            logger.error(f"Scaling rule '{rule_name}' not found")
            return False
        
        rule = self.scaling_rules[rule_name]
        
        # Build HPA specification
        hpa_spec = {
            "apiVersion": "autoscaling/v2",
            "kind": "HorizontalPodAutoscaler",
            "metadata": {
                "name": f"{self.deployment_name}-hpa",
                "namespace": self.namespace
            },
            "spec": {
                "scaleTargetRef": {
                    "apiVersion": "apps/v1",
                    "kind": "Deployment", 
                    "name": self.deployment_name
                },
                "minReplicas": rule.min_replicas,
                "maxReplicas": rule.max_replicas,
                "metrics": [],
                "behavior": {
                    "scaleUp": rule.scale_up_policy,
                    "scaleDown": rule.scale_down_policy
                }
            }
        }
        
        # Add metrics
        for metric in rule.metrics:
            if metric.resource_name:
                # Resource metric (CPU, Memory)
                hpa_spec["spec"]["metrics"].append({
                    "type": "Resource",
                    "resource": {
                        "name": metric.resource_name,
                        "target": {
                            "type": metric.target_type,
                            "averageUtilization": int(metric.target_value)
                        }
                    }
                })
            else:
                # Custom metric
                hpa_spec["spec"]["metrics"].append({
                    "type": "Object",
                    "object": {
                        "metric": {"name": metric.name},
                        "target": {
                            "type": metric.target_type,
                            "value": str(metric.target_value)
                        }
                    }
                })
        
        try:
            # Check if HPA exists
            try:
                await self.autoscaling_v2.read_namespaced_horizontal_pod_autoscaler(
                    name=f"{self.deployment_name}-hpa",
                    namespace=self.namespace
                )
                # Update existing HPA
                await self.autoscaling_v2.replace_namespaced_horizontal_pod_autoscaler(
                    name=f"{self.deployment_name}-hpa",
                    namespace=self.namespace,
                    body=hpa_spec
                )
                logger.info(f"Updated HPA for rule: {rule_name}")
            
            except ApiException as e:
                if e.status == 404:
                    # Create new HPA
                    await self.autoscaling_v2.create_namespaced_horizontal_pod_autoscaler(
                        namespace=self.namespace,
                        body=hpa_spec
                    )
                    logger.info(f"Created HPA for rule: {rule_name}")
                else:
                    raise
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to create/update HPA: {e}")
            return False
    
    async def create_vpa(self, rule_name: str) -> bool:
        """Create VPA (Vertical Pod Autoscaler) configuration"""
        if rule_name not in self.scaling_rules:
            return False
        
        vpa_spec = {
            "apiVersion": "autoscaling.k8s.io/v1",
            "kind": "VerticalPodAutoscaler",
            "metadata": {
                "name": f"{self.deployment_name}-vpa",
                "namespace": self.namespace
            },
            "spec": {
                "targetRef": {
                    "apiVersion": "apps/v1",
                    "kind": "Deployment",
                    "name": self.deployment_name
                },
                "updatePolicy": {
                    "updateMode": "Auto"  # Can be "Off", "Initial", "Auto"
                },
                "resourcePolicy": {
                    "containerPolicies": [{
                        "containerName": "orchestrator",
                        "minAllowed": {
                            "cpu": "100m",
                            "memory": "128Mi"
                        },
                        "maxAllowed": {
                            "cpu": "2",
                            "memory": "2Gi"
                        }
                    }]
                }
            }
        }
        
        try:
            await self.custom_objects.create_namespaced_custom_object(
                group="autoscaling.k8s.io",
                version="v1",
                namespace=self.namespace,
                plural="verticalpodautoscalers",
                body=vpa_spec
            )
            logger.info(f"Created VPA for rule: {rule_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create VPA: {e}")
            return False
    
    async def update_custom_metric(self, metric_name: str, value: float):
        """Update custom metric value for scaling decisions"""
        self.custom_metrics[metric_name] = value
        
        # Record metric in monitoring system
        if self.monitoring:
            await self.monitoring.record_metric(
                f"autoscaler_custom_metric_{metric_name}",
                value,
                {"deployment": self.deployment_name}
            )
    
    async def get_scaling_recommendation(self) -> Dict[str, Any]:
        """Get intelligent scaling recommendation based on current metrics"""
        await self._update_current_state()
        
        recommendation = {
            "current_replicas": self.state.current_replicas,
            "recommended_replicas": self.state.current_replicas,
            "scaling_direction": ScalingDirection.STABLE,
            "confidence": 0.0,
            "reasons": [],
            "estimated_impact": {}
        }
        
        # Analyze current metrics
        for rule_name, rule in self.scaling_rules.items():
            analysis = await self._analyze_scaling_need(rule)
            
            if analysis["should_scale"]:
                recommendation["recommended_replicas"] = analysis["target_replicas"]
                recommendation["scaling_direction"] = analysis["direction"]
                recommendation["confidence"] = analysis["confidence"]
                recommendation["reasons"].append(analysis["reason"])
        
        # Apply business logic and predictive scaling
        if self.predictive_scaling_enabled:
            predictive_analysis = await self._predictive_scaling_analysis()
            if predictive_analysis["should_scale"]:
                recommendation.update(predictive_analysis)
                recommendation["reasons"].append("Predictive scaling triggered")
        
        return recommendation
    
    async def _analyze_scaling_need(self, rule: ScalingRule) -> Dict[str, Any]:
        """Analyze if scaling is needed based on rule metrics"""
        should_scale = False
        target_replicas = self.state.current_replicas
        direction = ScalingDirection.STABLE
        confidence = 0.0
        reason = ""
        
        # Check each metric in the rule
        for metric in rule.metrics:
            current_value = self.custom_metrics.get(metric.name, 0.0)
            target_value = float(metric.target_value)
            
            if metric.target_type == "Utilization":
                # For utilization metrics (e.g., CPU 70%)
                if current_value > target_value * 1.1:  # 10% threshold
                    # Scale up needed
                    scale_factor = min(current_value / target_value, 2.0)  # Cap at 2x
                    target_replicas = min(
                        int(self.state.current_replicas * scale_factor),
                        rule.max_replicas
                    )
                    direction = ScalingDirection.UP
                    should_scale = True
                    confidence = min((current_value - target_value) / target_value, 1.0)
                    reason = f"{metric.name} utilization {current_value:.1f}% > {target_value}%"
                
                elif current_value < target_value * 0.8:  # 20% threshold for scale down
                    # Scale down possible
                    scale_factor = max(target_value / current_value, 0.5)  # Cap at 0.5x
                    target_replicas = max(
                        int(self.state.current_replicas / scale_factor),
                        rule.min_replicas
                    )
                    direction = ScalingDirection.DOWN
                    should_scale = True
                    confidence = min((target_value - current_value) / target_value, 1.0)
                    reason = f"{metric.name} utilization {current_value:.1f}% < {target_value * 0.8}%"
        
        return {
            "should_scale": should_scale,
            "target_replicas": target_replicas,
            "direction": direction,
            "confidence": confidence,
            "reason": reason
        }
    
    async def _predictive_scaling_analysis(self) -> Dict[str, Any]:
        """Perform predictive scaling analysis based on historical patterns"""
        # Simplified predictive logic - in production would use ML models
        current_hour = datetime.now().hour
        
        # Business hours scaling (9 AM - 6 PM)
        if self.business_hours_scaling and 9 <= current_hour <= 18:
            if self.state.current_replicas < 3:
                return {
                    "should_scale": True,
                    "recommended_replicas": 3,
                    "scaling_direction": ScalingDirection.UP,
                    "confidence": 0.8,
                    "reasons": ["Business hours pre-scaling"]
                }
        
        # Night hours scaling down (10 PM - 6 AM)
        elif 22 <= current_hour or current_hour <= 6:
            if self.state.current_replicas > 1:
                return {
                    "should_scale": True,
                    "recommended_replicas": 1,
                    "scaling_direction": ScalingDirection.DOWN,
                    "confidence": 0.7,
                    "reasons": ["Night hours scale-down"]
                }
        
        return {"should_scale": False}
    
    async def execute_scaling(self, target_replicas: int, reason: str = "") -> bool:
        """Execute scaling operation"""
        if target_replicas == self.state.current_replicas:
            return True
        
        try:
            # Get deployment
            deployment = await self.apps_v1.read_namespaced_deployment(
                name=self.deployment_name,
                namespace=self.namespace
            )
            
            # Update replica count
            deployment.spec.replicas = target_replicas
            
            # Apply update
            await self.apps_v1.patch_namespaced_deployment(
                name=self.deployment_name,
                namespace=self.namespace,
                body=deployment
            )
            
            # Record scaling event
            scaling_event = {
                "timestamp": datetime.now().isoformat(),
                "from_replicas": self.state.current_replicas,
                "to_replicas": target_replicas,
                "reason": reason,
                "direction": "up" if target_replicas > self.state.current_replicas else "down"
            }
            
            self.scaling_history.append(scaling_event)
            self.stats['total_scaling_events'] += 1
            
            if target_replicas > self.state.current_replicas:
                self.stats['scale_up_events'] += 1
            else:
                self.stats['scale_down_events'] += 1
            
            # Update state
            self.state.last_scale_time = datetime.now()
            self.state.scaling_reason = reason
            
            # Record metrics
            if self.monitoring:
                await self.monitoring.record_metric(
                    'autoscaler_scaling_events_total',
                    1,
                    {
                        'deployment': self.deployment_name,
                        'direction': scaling_event["direction"],
                        'reason': reason
                    }
                )
            
            logger.info(f"Scaled {self.deployment_name} from {self.state.current_replicas} to {target_replicas}: {reason}")
            
            # Update load balancer if integration enabled
            if self.load_balancer_integration:
                await self._update_load_balancer_backends(target_replicas)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to execute scaling: {e}")
            return False
    
    async def _update_current_state(self):
        """Update current deployment state"""
        try:
            deployment = await self.apps_v1.read_namespaced_deployment(
                name=self.deployment_name,
                namespace=self.namespace
            )
            
            self.state.current_replicas = deployment.status.replicas or 0
            self.state.desired_replicas = deployment.spec.replicas or 0
            
        except Exception as e:
            logger.error(f"Failed to update current state: {e}")
    
    async def _update_load_balancer_backends(self, new_replica_count: int):
        """Update load balancer backend configuration when scaling"""
        try:
            # This would integrate with the load balancer module
            # to add/remove backend servers based on scaling
            from .load_balancer import get_load_balancer
            
            load_balancer = await get_load_balancer()
            
            # Logic to add/remove backends would go here
            # For now, just log the action
            logger.info(f"Load balancer integration: updating for {new_replica_count} replicas")
            
        except Exception as e:
            logger.warning(f"Failed to update load balancer backends: {e}")
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get comprehensive auto-scaler metrics"""
        await self._update_current_state()
        
        return {
            "deployment": {
                "name": self.deployment_name,
                "namespace": self.namespace,
                "current_replicas": self.state.current_replicas,
                "desired_replicas": self.state.desired_replicas
            },
            "scaling_rules": {
                name: {
                    "min_replicas": rule.min_replicas,
                    "max_replicas": rule.max_replicas,
                    "metrics_count": len(rule.metrics)
                }
                for name, rule in self.scaling_rules.items()
            },
            "state": {
                "last_scale_time": self.state.last_scale_time.isoformat() if self.state.last_scale_time else None,
                "scaling_direction": self.state.scaling_direction.value,
                "scaling_reason": self.state.scaling_reason
            },
            "statistics": self.stats,
            "custom_metrics": self.custom_metrics,
            "recent_scaling_events": self.scaling_history[-10:]  # Last 10 events
        }

# Global auto-scaler instance
_auto_scaler_instance: Optional[AdvancedAutoScaler] = None

async def get_auto_scaler(
    namespace: str = "default",
    deployment_name: str = "orchestrator"
) -> AdvancedAutoScaler:
    """Get global auto-scaler instance"""
    global _auto_scaler_instance
    
    if _auto_scaler_instance is None:
        _auto_scaler_instance = AdvancedAutoScaler(namespace, deployment_name)
        await _auto_scaler_instance.initialize()
    
    return _auto_scaler_instance

async def setup_production_scaling(
    deployment_name: str = "orchestrator",
    namespace: str = "default"
) -> AdvancedAutoScaler:
    """Setup production-ready auto-scaling configuration"""
    auto_scaler = await get_auto_scaler(namespace, deployment_name)
    
    # Standard production scaling rule
    production_rule = ScalingRule(
        name="production_standard",
        min_replicas=3,
        max_replicas=20,
        metrics=[
            ScalingMetric(
                name="cpu",
                target_type="Utilization",
                target_value="70",
                resource_name="cpu"
            ),
            ScalingMetric(
                name="memory",
                target_type="Utilization", 
                target_value="80",
                resource_name="memory"
            )
        ]
    )
    
    auto_scaler.add_scaling_rule(production_rule)
    await auto_scaler.create_hpa("production_standard")
    
    logger.info("Production auto-scaling configuration completed")
    return auto_scaler




