"""
Documentation Generator - NextGeneration SuperWhisper_V6 Transposition
Équipe d'agents spécialisés pour la transposition SuperWhisper_V6 vers NextGeneration

Agents disponibles:
- Agent Coordinateur: Orchestration mission complète
- Agent Analyseur: Analyse structure projet NextGeneration  
- Agent Générateur: Génération documentation automatique
- Agent Workflow: Création workflows PowerShell
- Agent GPU: Standards RTX 3090 optimisés
- Agent Validation: Tests et validation finale

Version: 1.0.0
Date: 2025-01-19
"""

__version__ = "1.0.0"
__author__ = "NextGeneration SuperWhisper_V6 Transposition Team"

from .coordinateur_transposition_superwhisper import CoordinateurTranspositionSuperWhisper
from .agent_analyseur_nextgeneration import AgentAnalyseurNextGeneration
from .agent_generateur_documentation import AgentGenerateurDocumentation
from .agent_workflow_powershell import AgentWorkflowPowerShell
from .agent_standards_gpu import AgentStandardsGPU
from .agent_validation_finale import AgentValidationFinale

__all__ = [
    "CoordinateurTranspositionSuperWhisper",
    "AgentAnalyseurNextGeneration", 
    "AgentGenerateurDocumentation",
    "AgentWorkflowPowerShell",
    "AgentStandardsGPU",
    "AgentValidationFinale"
] 



