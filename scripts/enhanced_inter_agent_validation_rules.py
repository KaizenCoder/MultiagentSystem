#!/usr/bin/env python3
"""
🔒 RÈGLES VALIDATION INTER-AGENT DURCIES
Système de validation renforcé avec auditeurs et reviewers spécialisés

Contraintes durcies:
- Validation obligatoire par 2+ agents spécialisés
- Au moins 1 auditeur (type AUDIT) 
- Au moins 1 reviewer (type REVIEW/TESTING)
- Escalade automatique si non-conformité
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from enum import Enum

class AgentType(Enum):
    """Types d'agents avec spécialisations validation"""
    AUDIT = "audit"              # Auditeurs qualité/sécurité
    REVIEW = "review"            # Reviewers code/architecture  
    TESTING = "testing"          # Testeurs fonctionnels
    COORDINATION = "coordination" # Coordinateurs workflow
    FACTORY = "factory"          # Générateurs patterns
    PRODUCTION = "production"    # Agents métier
    UNKNOWN = "unknown"          # Type non défini

@dataclass
class ValidationRule:
    """Règle de validation inter-agent durcie"""
    min_validators: int
    required_auditors: int
    required_reviewers: int
    compatibility_threshold: float
    escalation_threshold: float
    mandatory_agent_types: Set[AgentType]
    optional_agent_types: Set[AgentType]

class EnhancedInterAgentValidationRules:
    """
    🔒 Système Validation Inter-Agent Durci
    
    Règles progressivement durcies selon criticité et développement:
    - Agents Production: Validation max security 
    - Agents Infrastructure: Validation renforcée
    - Agents Métier: Validation standard durcie
    """
    
    def __init__(self):
        self.validation_rules = self._define_hardened_rules()
        self.agent_type_registry = self._initialize_agent_types()
        self.validation_matrix = self._build_validation_matrix()
        
    def _define_hardened_rules(self) -> Dict[str, ValidationRule]:
        """Définit règles validation durcies par niveau criticité"""
        
        return {
            # NIVEAU CRITIQUE - Agents Infrastructure/Sécurité
            "CRITICAL": ValidationRule(
                min_validators=3,              # 3 validateurs minimum
                required_auditors=2,          # 2 auditeurs obligatoires
                required_reviewers=1,         # 1 reviewer obligatoire  
                compatibility_threshold=0.85, # 85% minimum
                escalation_threshold=0.75,    # Escalade si <75%
                mandatory_agent_types={AgentType.AUDIT, AgentType.REVIEW},
                optional_agent_types={AgentType.TESTING, AgentType.COORDINATION}
            ),
            
            # NIVEAU ÉLEVÉ - Agents Production/Métier
            "HIGH": ValidationRule(
                min_validators=3,              # 3 validateurs minimum
                required_auditors=1,          # 1 auditeur obligatoire
                required_reviewers=1,         # 1 reviewer obligatoire
                compatibility_threshold=0.80, # 80% minimum
                escalation_threshold=0.70,    # Escalade si <70%
                mandatory_agent_types={AgentType.AUDIT, AgentType.REVIEW},
                optional_agent_types={AgentType.TESTING}
            ),
            
            # NIVEAU STANDARD - Agents Normaux
            "STANDARD": ValidationRule(
                min_validators=2,              # 2 validateurs minimum
                required_auditors=1,          # 1 auditeur obligatoire
                required_reviewers=1,         # 1 reviewer obligatoire
                compatibility_threshold=0.75, # 75% minimum
                escalation_threshold=0.65,    # Escalade si <65%
                mandatory_agent_types={AgentType.AUDIT, AgentType.REVIEW},
                optional_agent_types=set()
            ),
            
            # NIVEAU DÉVELOPPEMENT - Phase pilote seulement
            "DEVELOPMENT": ValidationRule(
                min_validators=2,              # 2 validateurs minimum
                required_auditors=1,          # 1 auditeur obligatoire
                required_reviewers=1,         # 1 reviewer obligatoire
                compatibility_threshold=0.70, # 70% minimum
                escalation_threshold=0.60,    # Escalade si <60%
                mandatory_agent_types={AgentType.AUDIT},
                optional_agent_types={AgentType.REVIEW, AgentType.TESTING}
            )
        }
    
    def _initialize_agent_types(self) -> Dict[str, AgentType]:
        """Registre types agents avec spécialisations"""
        
        return {
            # Auditeurs spécialisés
            "agent_111": AgentType.AUDIT,           # Auditeur qualité principal
            "agent_18": AgentType.AUDIT,            # Auditeur sécurité
            "agent_19": AgentType.AUDIT,            # Auditeur performance  
            "agent_20": AgentType.AUDIT,            # Auditeur conformité
            
            # Reviewers spécialisés
            "agent_16": AgentType.REVIEW,           # Peer reviewer senior
            "agent_17": AgentType.REVIEW,           # Peer reviewer technique
            "agent_02": AgentType.REVIEW,           # Architecte code expert
            
            # Testeurs fonctionnels
            "agent_05": AgentType.TESTING,          # Maître tests validation
            "agent_15": AgentType.TESTING,          # Testeur spécialisé
            
            # Coordinateurs
            "agent_00": AgentType.COORDINATION,     # Chef équipe coordinateur
            "agent_01": AgentType.COORDINATION,     # Coordinateur principal
            
            # Factory/Générateurs
            "agent_109": AgentType.FACTORY,         # Pattern factory
            "agent_09": AgentType.FACTORY,          # Spécialiste plans
            
            # Agents production (métier)
            "agent_03": AgentType.PRODUCTION,       # Spécialiste configuration
            "agent_04": AgentType.PRODUCTION,       # Expert sécurité crypto
            "agent_06": AgentType.PRODUCTION,       # Spécialiste monitoring
            "agent_07": AgentType.PRODUCTION,       # Expert déploiement K8s
            "agent_08": AgentType.PRODUCTION,       # Performance optimizer
        }
    
    def _build_validation_matrix(self) -> Dict[str, Dict[str, List[str]]]:
        """Construit matrice validation avec auditeurs/reviewers spécialisés"""
        
        # Auditeurs disponibles par spécialisation
        auditors = {
            "quality": ["agent_111"],           # Audit qualité
            "security": ["agent_18"],           # Audit sécurité
            "performance": ["agent_19"],        # Audit performance
            "compliance": ["agent_20"],         # Audit conformité
            "universal": ["agent_111"]          # Audit universel
        }
        
        # Reviewers disponibles par spécialisation
        reviewers = {
            "senior": ["agent_16"],             # Review senior
            "technical": ["agent_17"],          # Review technique
            "architecture": ["agent_02"],       # Review architecture
            "testing": ["agent_05"]             # Review fonctionnel
        }
        
        # Matrice validation spécialisée
        validation_matrix = {}
        
        # Pour chaque agent, définir validateurs spécialisés
        for agent_id, agent_type in self.agent_type_registry.items():
            
            if agent_type == AgentType.PRODUCTION:
                # Agents production: validation max sécurité
                validation_matrix[agent_id] = {
                    "primary_auditors": [auditors["quality"][0], auditors["security"][0]],
                    "primary_reviewers": [reviewers["senior"][0], reviewers["architecture"][0]],
                    "backup_auditors": [auditors["compliance"][0]],
                    "backup_reviewers": [reviewers["technical"][0]],
                    "validation_level": "HIGH"
                }
                
            elif agent_type == AgentType.AUDIT:
                # Auditeurs: validation par peers + reviewers
                validation_matrix[agent_id] = {
                    "primary_auditors": [a for a in auditors["universal"] if a != agent_id],
                    "primary_reviewers": [reviewers["senior"][0], reviewers["technical"][0]],
                    "backup_auditors": [auditors["compliance"][0]],
                    "backup_reviewers": [reviewers["architecture"][0]],
                    "validation_level": "CRITICAL"
                }
                
            elif agent_type == AgentType.REVIEW:
                # Reviewers: validation par auditeurs + peer reviewers
                validation_matrix[agent_id] = {
                    "primary_auditors": [auditors["quality"][0]],
                    "primary_reviewers": [r for r in reviewers["senior"] + reviewers["technical"] if r != agent_id],
                    "backup_auditors": [auditors["security"][0]],
                    "backup_reviewers": [reviewers["architecture"][0]],
                    "validation_level": "HIGH"
                }
                
            elif agent_type == AgentType.TESTING:
                # Testeurs: validation qualité + review fonctionnel
                validation_matrix[agent_id] = {
                    "primary_auditors": [auditors["quality"][0]],
                    "primary_reviewers": [reviewers["technical"][0]],
                    "backup_auditors": [auditors["performance"][0]],
                    "backup_reviewers": [reviewers["senior"][0]],
                    "validation_level": "STANDARD"
                }
                
            elif agent_type == AgentType.COORDINATION:
                # Coordinateurs: validation workflow + architecture
                validation_matrix[agent_id] = {
                    "primary_auditors": [auditors["quality"][0]],
                    "primary_reviewers": [reviewers["architecture"][0]],
                    "backup_auditors": [auditors["compliance"][0]],
                    "backup_reviewers": [reviewers["senior"][0]],
                    "validation_level": "HIGH"
                }
                
            elif agent_type == AgentType.FACTORY:
                # Factory: validation patterns + architecture
                validation_matrix[agent_id] = {
                    "primary_auditors": [auditors["quality"][0]],
                    "primary_reviewers": [reviewers["architecture"][0]],
                    "backup_auditors": [auditors["compliance"][0]],
                    "backup_reviewers": [reviewers["technical"][0]],
                    "validation_level": "STANDARD"
                }
                
            else:
                # Agents inconnus: validation minimale
                validation_matrix[agent_id] = {
                    "primary_auditors": [auditors["universal"][0]],
                    "primary_reviewers": [reviewers["senior"][0]],
                    "backup_auditors": [],
                    "backup_reviewers": [],
                    "validation_level": "DEVELOPMENT"
                }
        
        return validation_matrix
    
    def get_validation_requirements(self, agent_id: str) -> Dict[str, Any]:
        """Retourne exigences validation durcies pour agent"""
        
        if agent_id not in self.validation_matrix:
            # Agent inconnu: règles de développement
            rule = self.validation_rules["DEVELOPMENT"]
            mandatory_validators = ["agent_111"]  # Au minimum un auditeur
            return {
                "agent_id": agent_id,
                "agent_type": "UNKNOWN",
                "validation_level": "DEVELOPMENT",
                "rule": rule,
                "mandatory_validators": mandatory_validators,
                "validation_matrix": {"validation_level": "DEVELOPMENT"},
                "compliance_check": self._check_compliance(agent_id, mandatory_validators, rule),
                "error": f"Agent {agent_id} not in registry - using development rules"
            }
        
        matrix_entry = self.validation_matrix[agent_id]
        validation_level = matrix_entry["validation_level"]
        rule = self.validation_rules[validation_level]
        
        # Construire liste validateurs obligatoires
        mandatory_validators = []
        
        # Auditeurs obligatoires
        primary_auditors = matrix_entry.get("primary_auditors", [])
        mandatory_validators.extend(primary_auditors[:rule.required_auditors])
        
        # Reviewers obligatoires  
        primary_reviewers = matrix_entry.get("primary_reviewers", [])
        mandatory_validators.extend(primary_reviewers[:rule.required_reviewers])
        
        # Backup si pas assez de validateurs
        if len(mandatory_validators) < rule.min_validators:
            backup_auditors = matrix_entry.get("backup_auditors", [])
            backup_reviewers = matrix_entry.get("backup_reviewers", [])
            
            for backup in backup_auditors + backup_reviewers:
                if backup not in mandatory_validators:
                    mandatory_validators.append(backup)
                    if len(mandatory_validators) >= rule.min_validators:
                        break
        
        return {
            "agent_id": agent_id,
            "agent_type": self.agent_type_registry.get(agent_id, AgentType.UNKNOWN).value,
            "validation_level": validation_level,
            "rule": rule,
            "mandatory_validators": mandatory_validators,
            "validation_matrix": matrix_entry,
            "compliance_check": self._check_compliance(agent_id, mandatory_validators, rule)
        }
    
    def _check_compliance(self, agent_id: str, validators: List[str], rule: ValidationRule) -> Dict[str, Any]:
        """Vérifie conformité règles validation durcies"""
        
        # Compter types validateurs
        auditor_count = sum(1 for v in validators if self.agent_type_registry.get(v) == AgentType.AUDIT)
        reviewer_count = sum(1 for v in validators if self.agent_type_registry.get(v) == AgentType.REVIEW)
        testing_count = sum(1 for v in validators if self.agent_type_registry.get(v) == AgentType.TESTING)
        
        compliance = {
            "total_validators": len(validators),
            "auditor_count": auditor_count,
            "reviewer_count": reviewer_count,
            "testing_count": testing_count,
            "min_validators_met": len(validators) >= rule.min_validators,
            "required_auditors_met": auditor_count >= rule.required_auditors,
            "required_reviewers_met": reviewer_count >= rule.required_reviewers,
            "mandatory_types_met": True,  # Will be checked below
            "compliance_status": "UNKNOWN",
            "issues": [],
            "recommendations": []
        }
        
        # Vérifier types obligatoires
        validator_types = {self.agent_type_registry.get(v, AgentType.UNKNOWN) for v in validators}
        missing_mandatory = rule.mandatory_agent_types - validator_types
        
        if missing_mandatory:
            compliance["mandatory_types_met"] = False
            compliance["issues"].append(f"Missing mandatory validator types: {missing_mandatory}")
        
        # Vérifier conformité globale
        issues = []
        if not compliance["min_validators_met"]:
            issues.append(f"Insufficient validators: {len(validators)}/{rule.min_validators}")
        if not compliance["required_auditors_met"]:
            issues.append(f"Insufficient auditors: {auditor_count}/{rule.required_auditors}")
        if not compliance["required_reviewers_met"]:
            issues.append(f"Insufficient reviewers: {reviewer_count}/{rule.required_reviewers}")
        
        compliance["issues"].extend(issues)
        
        # Status conformité
        if not issues and compliance["mandatory_types_met"]:
            compliance["compliance_status"] = "COMPLIANT"
        elif len(issues) <= 1:
            compliance["compliance_status"] = "PARTIAL_COMPLIANCE"
            compliance["recommendations"].append("Consider adding backup validators")
        else:
            compliance["compliance_status"] = "NON_COMPLIANT"
            compliance["recommendations"].append("CRITICAL: Must fix validation requirements before deployment")
        
        return compliance
    
    def generate_validation_plan(self, agent_id: str) -> Dict[str, Any]:
        """Génère plan validation durci pour agent"""
        
        requirements = self.get_validation_requirements(agent_id)
        
        validation_plan = {
            "agent_id": agent_id,
            "plan_generated": datetime.now().isoformat(),
            "validation_requirements": requirements,
            "execution_sequence": [],
            "quality_gates": [],
            "escalation_triggers": [],
            "monitoring_requirements": []
        }
        
        # Séquence exécution validation
        rule = requirements["rule"]
        validators = requirements["mandatory_validators"]
        
        validation_plan["execution_sequence"] = [
            {
                "phase": "PRE_VALIDATION",
                "description": "Verify validator availability and readiness",
                "validators": validators,
                "estimated_duration": "15 minutes"
            },
            {
                "phase": "AUDIT_PHASE",
                "description": "Execute mandatory audit validations",
                "validators": [v for v in validators if self.agent_type_registry.get(v) == AgentType.AUDIT],
                "min_score": rule.compatibility_threshold,
                "estimated_duration": "45 minutes"
            },
            {
                "phase": "REVIEW_PHASE", 
                "description": "Execute mandatory review validations",
                "validators": [v for v in validators if self.agent_type_registry.get(v) == AgentType.REVIEW],
                "min_score": rule.compatibility_threshold,
                "estimated_duration": "30 minutes"
            },
            {
                "phase": "INTEGRATION_VALIDATION",
                "description": "Cross-validation with ecosystem",
                "validators": validators,
                "min_score": rule.compatibility_threshold,
                "estimated_duration": "20 minutes"
            },
            {
                "phase": "FINAL_APPROVAL",
                "description": "Consolidate results and deployment decision",
                "min_overall_score": rule.compatibility_threshold,
                "estimated_duration": "10 minutes"
            }
        ]
        
        # Quality gates
        validation_plan["quality_gates"] = [
            {
                "gate": "AUDITOR_APPROVAL",
                "requirement": f"All {rule.required_auditors} auditors must approve with >{rule.compatibility_threshold*100}% score",
                "blocking": True
            },
            {
                "gate": "REVIEWER_APPROVAL", 
                "requirement": f"All {rule.required_reviewers} reviewers must approve with >{rule.compatibility_threshold*100}% score",
                "blocking": True
            },
            {
                "gate": "COMPATIBILITY_THRESHOLD",
                "requirement": f"Overall compatibility >{rule.compatibility_threshold*100}%",
                "blocking": True
            },
            {
                "gate": "NO_CRITICAL_ISSUES",
                "requirement": "Zero critical security or quality issues",
                "blocking": True
            }
        ]
        
        # Triggers escalade
        validation_plan["escalation_triggers"] = [
            {
                "trigger": "COMPATIBILITY_BELOW_ESCALATION",
                "condition": f"Any validator score <{rule.escalation_threshold*100}%",
                "action": "Immediate senior review required",
                "notification": ["team_lead", "security_team"]
            },
            {
                "trigger": "AUDITOR_REJECTION",
                "condition": "Any mandatory auditor rejects deployment",
                "action": "Block deployment until resolution",
                "notification": ["team_lead", "qa_team"]
            },
            {
                "trigger": "CRITICAL_ISSUE_FOUND",
                "condition": "Security or quality critical issue detected",
                "action": "Emergency review process activated",
                "notification": ["security_team", "architecture_team"]
            }
        ]
        
        # Monitoring continu
        validation_plan["monitoring_requirements"] = [
            {
                "metric": "Inter-agent compatibility degradation",
                "frequency": "Real-time",
                "threshold": f"<{rule.compatibility_threshold*100}%",
                "action": "Trigger re-validation"
            },
            {
                "metric": "Validator consensus drift",
                "frequency": "Daily",
                "threshold": ">10% variance between validators",
                "action": "Review validation criteria"
            },
            {
                "metric": "Ecosystem health impact",
                "frequency": "Continuous",
                "threshold": "Any negative impact on ecosystem metrics",
                "action": "Investigate and mitigate"
            }
        ]
        
        return validation_plan

async def demonstrate_hardened_rules():
    """Démonstration règles validation durcies"""
    
    print("🔒 DÉMONSTRATION RÈGLES VALIDATION DURCIES")
    print("=" * 70)
    
    rules_system = EnhancedInterAgentValidationRules()
    
    # Test agents différents niveaux
    test_agents = [
        "agent_111",  # Auditeur critique
        "agent_05",   # Testeur standard  
        "agent_02",   # Reviewer architecture
        "agent_03",   # Agent production
        "agent_999"   # Agent inconnu
    ]
    
    validation_reports = []
    
    for agent_id in test_agents:
        print(f"\n🔍 Agent: {agent_id}")
        print("-" * 50)
        
        # Obtenir exigences validation
        requirements = rules_system.get_validation_requirements(agent_id)
        
        print(f"Type: {requirements['agent_type'].upper()}")
        print(f"Niveau: {requirements['validation_level']}")
        print(f"Validateurs obligatoires: {len(requirements['mandatory_validators'])}")
        
        compliance = requirements['compliance_check']
        print(f"Status: {compliance['compliance_status']}")
        
        # Générer plan validation
        validation_plan = rules_system.generate_validation_plan(agent_id)
        
        print(f"Phases validation: {len(validation_plan['execution_sequence'])}")
        print(f"Quality gates: {len(validation_plan['quality_gates'])}")
        print(f"Triggers escalade: {len(validation_plan['escalation_triggers'])}")
        
        if compliance['issues']:
            print(f"⚠️ Issues: {', '.join(compliance['issues'])}")
        
        validation_reports.append({
            "agent_id": agent_id,
            "requirements": requirements,
            "validation_plan": validation_plan
        })
    
    # Résumé global
    print(f"\n📊 RÉSUMÉ VALIDATION DURCIE")
    print("=" * 70)
    
    compliant_agents = sum(1 for r in validation_reports 
                          if r['requirements']['compliance_check']['compliance_status'] == 'COMPLIANT')
    
    print(f"Agents conformes: {compliant_agents}/{len(validation_reports)}")
    print(f"Règles implémentées: {len(rules_system.validation_rules)}")
    print(f"Types validateurs: {len(set(rules_system.agent_type_registry.values()))}")
    
    # Statistiques validation
    total_auditors = sum(r['requirements']['compliance_check']['auditor_count'] for r in validation_reports)
    total_reviewers = sum(r['requirements']['compliance_check']['reviewer_count'] for r in validation_reports)
    
    print(f"Total auditeurs requis: {total_auditors}")
    print(f"Total reviewers requis: {total_reviewers}")
    
    print(f"\n✅ RÈGLES VALIDATION DURCIES OPÉRATIONNELLES")
    print("🚀 Prêt pour Wave 1 avec validation renforcée")
    
    return validation_reports

async def main():
    """Point d'entrée règles validation durcies"""
    
    try:
        # Démonstration système
        reports = await demonstrate_hardened_rules()
        
        # Sauvegarde configuration
        config_file = Path(__file__).parent.parent / "config" / "enhanced_validation_rules.json"
        config_file.parent.mkdir(exist_ok=True)
        
        rules_system = EnhancedInterAgentValidationRules()
        
        config_data = {
            "validation_rules": {k: {
                "min_validators": v.min_validators,
                "required_auditors": v.required_auditors, 
                "required_reviewers": v.required_reviewers,
                "compatibility_threshold": v.compatibility_threshold,
                "escalation_threshold": v.escalation_threshold,
                "mandatory_agent_types": [t.value for t in v.mandatory_agent_types],
                "optional_agent_types": [t.value for t in v.optional_agent_types]
            } for k, v in rules_system.validation_rules.items()},
            "agent_type_registry": {k: v.value for k, v in rules_system.agent_type_registry.items()},
            "validation_matrix": rules_system.validation_matrix,
            "configuration_date": datetime.now().isoformat(),
            "version": "2.0.0-hardened"
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Configuration sauvegardée: {config_file}")
        
        return reports
        
    except Exception as e:
        print(f"❌ Erreur règles validation: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

if __name__ == "__main__":
    asyncio.run(main())