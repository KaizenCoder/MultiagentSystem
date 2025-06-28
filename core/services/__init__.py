"""
Core Services - NextGeneration Architecture

Services centraux pour l'architecture agentique hybride:
- LLMGateway: Service unifié pour modèles LLM
- MessageBus: Communication Agent-to-Agent  
- ContextStore: Mémoire tri-tiers des agents
- ShadowMode: Validation zero-risk pour migration
"""

# LLMGateway imports
from .llm_gateway_hybrid import (
    LLMGatewayHybrid,
    LLMRequest,
    LLMResponse, 
    GatewayConfig,
    create_llm_gateway,
    Priority as LLMPriority,
    ModelType
)

# MessageBus imports
from .message_bus_a2a import (
    MessageBusA2A,
    Envelope,
    PublishResult,
    MessageBusConfig,
    MessageType,
    Priority,
    LegacyAgentBridge,
    VoiceOptimizedMessageBus,
    create_message_bus,
    create_envelope
)

# ContextStore imports
from .context_store import (
    OptimizedContextStore,
    AgentContext,
    ContextType,
    ContextStoreConfig,
    ContextDiff,
    create_context_store,
    create_agent_context
)

# ShadowMode imports
from .shadow_mode_validator import (
    ShadowModeValidator,
    ShadowModeConfig,
    ValidationResult,
    ActivationDecision,
    AgentExecutionResult,
    ComparisonResult,
    ResultComparator,
    create_shadow_validator
)

__all__ = [
    # LLMGateway
    'LLMGatewayHybrid',
    'LLMRequest', 
    'LLMResponse',
    'GatewayConfig',
    'create_llm_gateway',
    'LLMPriority',
    'ModelType',
    
    # MessageBus
    'MessageBusA2A',
    'Envelope',
    'PublishResult',
    'MessageBusConfig',
    'MessageType',
    'Priority',
    'LegacyAgentBridge',
    'VoiceOptimizedMessageBus',
    'create_message_bus',
    'create_envelope',
    
    # ContextStore
    'OptimizedContextStore',
    'AgentContext',
    'ContextType',
    'ContextStoreConfig',
    'ContextDiff',
    'create_context_store',
    'create_agent_context',
    
    # ShadowMode
    'ShadowModeValidator',
    'ShadowModeConfig',
    'ValidationResult',
    'ActivationDecision',
    'AgentExecutionResult',
    'ComparisonResult',
    'ResultComparator',
    'create_shadow_validator'
]