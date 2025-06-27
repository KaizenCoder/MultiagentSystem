#!/usr/bin/env python3
"""
AUDIT SIMPLIFIÉ DES 4 AGENTS CIBLES
===================================

Script d'audit simplifié pour analyser les 4 agents spécifiés :
- agent_SECURITY_21_supply_chain_enterprise.py
- agent_STORAGE_24_enterprise_manager.py  
- agent_test_models_integration.py
- agent_testeur_agents_complet.py

Version: 1.0.0
"""

import ast
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import tempfile

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = PROJECT_ROOT / "agents"

# Agents cibles
TARGET_AGENTS = [
    "agent_SECURITY_21_supply_chain_enterprise.py",
    "agent_STORAGE_24_enterprise_manager.py", 
    "agent_test_models_integration.py",
    "agent_testeur_agents_complet.py"
]

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AgentAuditor:
    """Auditeur simplifié pour les agents"""
    
    def __init__(self):
        self.audit_results = {}
        self.start_time = datetime.now()
        
    def analyze_syntax(self, file_path: Path) -> Dict[str, Any]:
        """Analyse syntaxique du fichier Python"""
        try:
            content = file_path.read_text(encoding='utf-8')
            ast.parse(content)
            return {
                "syntax_valid": True,
                "lines_count": len(content.split('\n')),
                "size_bytes": len(content.encode('utf-8'))
            }
        except SyntaxError as e:
            return {
                "syntax_valid": False,
                "error": str(e),
                "line": e.lineno
            }
        except Exception as e:
            return {
                "syntax_valid": False,
                "error": f"Erreur lecture: {str(e)}"
            }
    
    def analyze_structure(self, file_path: Path) -> Dict[str, Any]:
        """Analyse de la structure du code"""
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content)
            
            classes = []
            functions = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append({
                        "name": node.name,
                        "line": node.lineno,
                        "methods": len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                    })
                elif isinstance(node, ast.FunctionDef):
                    if not any(node.lineno >= cls_node.lineno and 
                             node.lineno <= (cls_node.end_lineno or float('inf')) 
                             for cls_node in ast.walk(tree) if isinstance(cls_node, ast.ClassDef)):
                        functions.append({
                            "name": node.name,
                            "line": node.lineno,
                            "is_async": isinstance(node, ast.AsyncFunctionDef)
                        })
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        imports.extend([alias.name for alias in node.names])
                    else:
                        module = node.module or ""
                        imports.extend([f"{module}.{alias.name}" if alias.name != "*" else f"{module}.*" 
                                      for alias in node.names])
            
            return {
                "classes_count": len(classes),
                "functions_count": len(functions),
                "imports_count": len(imports),
                "classes": classes,
                "functions": functions[:10],  # Top 10
                "imports": imports[:20]  # Top 20
            }
            
        except Exception as e:
            return {
                "error": f"Erreur analyse structure: {str(e)}"
            }
    
    def analyze_patterns(self, file_path: Path) -> Dict[str, Any]:
        """Analyse des patterns et bonnes pratiques"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Patterns recherchés
            patterns = {
                "pattern_factory": {
                    "keywords": ["factory", "create_agent", "Agent", "Pattern"],
                    "found": 0
                },
                "async_patterns": {
                    "keywords": ["async def", "await", "asyncio"],
                    "found": 0
                },
                "enterprise_features": {
                    "keywords": ["enterprise", "Enterprise", "monitoring", "metrics", "security"],
                    "found": 0
                },
                "logging": {
                    "keywords": ["logger", "logging", "log", "info", "error"],
                    "found": 0
                },
                "error_handling": {
                    "keywords": ["try:", "except", "finally:", "raise"],
                    "found": 0
                },
                "documentation": {
                    "keywords": ['"""', "'''", "# ", "Args:", "Returns:"],
                    "found": 0
                }
            }
            
            content_lower = content.lower()
            
            for pattern_name, pattern_info in patterns.items():
                for keyword in pattern_info["keywords"]:
                    pattern_info["found"] += content.count(keyword)
            
            # Calcul score qualité basique
            total_patterns = sum(p["found"] for p in patterns.values())
            quality_score = min(100, total_patterns * 2)  # Score basique
            
            return {
                "patterns": patterns,
                "quality_score": quality_score,
                "total_patterns_found": total_patterns
            }
            
        except Exception as e:
            return {
                "error": f"Erreur analyse patterns: {str(e)}"
            }
    
    def analyze_dependencies(self, file_path: Path) -> Dict[str, Any]:
        """Analyse des dépendances"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Dépendances détectées
            dependencies = {
                "core_dependencies": [],
                "external_dependencies": [],
                "local_dependencies": [],
                "potential_issues": []
            }
            
            lines = content.split('\n')
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if line.startswith(('import ', 'from ')):
                    if 'core.' in line:
                        dependencies["core_dependencies"].append({"line": line_num, "import": line})
                    elif any(pkg in line for pkg in ['asyncio', 'json', 'datetime', 'pathlib', 'typing']):
                        dependencies["external_dependencies"].append({"line": line_num, "import": line})
                    elif 'agents.' in line:
                        dependencies["local_dependencies"].append({"line": line_num, "import": line})
                    
                    # Détection de problèmes potentiels
                    if 'ImportError' in content and line.strip().startswith('except ImportError'):
                        dependencies["potential_issues"].append(f"Import conditionnel ligne {line_num}")
            
            return {
                "dependencies": dependencies,
                "core_deps_count": len(dependencies["core_dependencies"]),
                "external_deps_count": len(dependencies["external_dependencies"]),
                "local_deps_count": len(dependencies["local_dependencies"]),
                "issues_count": len(dependencies["potential_issues"])
            }
            
        except Exception as e:
            return {
                "error": f"Erreur analyse dépendances: {str(e)}"
            }
    
    def analyze_agent_capabilities(self, file_path: Path) -> Dict[str, Any]:
        """Analyse des capacités spécifiques de l'agent"""
        try:
            content = file_path.read_text(encoding='utf-8')
            agent_name = file_path.stem
            
            capabilities = {
                "agent_type": "unknown",
                "specialization": [],
                "new_features": [],
                "compliance_level": "basic"
            }
            
            # Détection du type d'agent
            if "security" in agent_name.lower():
                capabilities["agent_type"] = "security"
                if "enterprise" in content.lower():
                    capabilities["specialization"].append("enterprise_security")
                if "zero_trust" in content.lower():
                    capabilities["new_features"].append("zero_trust_architecture")
            
            elif "storage" in agent_name.lower():
                capabilities["agent_type"] = "storage"
                if "auto_scaling" in content.lower() or "autoscaling" in content.lower():
                    capabilities["new_features"].append("auto_scaling")
                if "enterprise" in content.lower():
                    capabilities["specialization"].append("enterprise_storage")
            
            elif "test" in agent_name.lower():
                capabilities["agent_type"] = "testing"
                if "models" in agent_name.lower():
                    capabilities["specialization"].append("models_integration")
                if "ollama" in content.lower():
                    capabilities["new_features"].append("ollama_integration")
                if "integration" in content.lower():
                    capabilities["new_features"].append("integration_testing")
            
            elif "testeur" in agent_name.lower():
                capabilities["agent_type"] = "validation"
                capabilities["specialization"].append("agent_testing")
                if "strategic" in content.lower():
                    capabilities["new_features"].append("strategic_reporting")
            
            # Détection niveau de compliance
            if "pattern_factory" in content.lower() and "enterprise" in content.lower():
                capabilities["compliance_level"] = "enterprise"
            elif "pattern_factory" in content.lower():
                capabilities["compliance_level"] = "standard"
            
            return capabilities
            
        except Exception as e:
            return {
                "error": f"Erreur analyse capacités: {str(e)}"
            }
    
    def audit_agent(self, agent_file: str) -> Dict[str, Any]:
        """Audit complet d'un agent"""
        agent_path = AGENTS_DIR / agent_file
        
        logger.info(f"🔍 Audit de {agent_file}...")
        
        audit_result = {
            "agent_file": agent_file,
            "agent_path": str(agent_path),
            "timestamp": datetime.now().isoformat(),
            "exists": agent_path.exists()
        }
        
        if not agent_path.exists():
            audit_result["error"] = f"Fichier non trouvé: {agent_path}"
            return audit_result
        
        try:
            # Analyses séquentielles
            audit_result["syntax"] = self.analyze_syntax(agent_path)
            audit_result["structure"] = self.analyze_structure(agent_path)
            audit_result["patterns"] = self.analyze_patterns(agent_path)
            audit_result["dependencies"] = self.analyze_dependencies(agent_path)
            audit_result["capabilities"] = self.analyze_agent_capabilities(agent_path)
            
            # Calcul score global
            syntax_score = 100 if audit_result["syntax"].get("syntax_valid", False) else 0
            pattern_score = audit_result["patterns"].get("quality_score", 0)
            structure_score = min(100, audit_result["structure"].get("classes_count", 0) * 20)
            
            audit_result["global_score"] = (syntax_score + pattern_score + structure_score) / 3
            audit_result["audit_status"] = "success"
            
            logger.info(f"✅ {agent_file}: Score global {audit_result['global_score']:.1f}/100")
            
        except Exception as e:
            audit_result["error"] = str(e)
            audit_result["audit_status"] = "failed"
            logger.error(f"❌ Erreur audit {agent_file}: {e}")
        
        return audit_result
    
    def run_full_audit(self) -> Dict[str, Any]:
        """Lance l'audit complet des 4 agents cibles"""
        logger.info("🎯 DÉBUT AUDIT DES 4 AGENTS CIBLES")
        logger.info("="*50)
        
        for agent_file in TARGET_AGENTS:
            logger.info(f"📋 Agent: {agent_file}")
        
        logger.info("="*50)
        
        # Audit de chaque agent
        for agent_file in TARGET_AGENTS:
            self.audit_results[agent_file] = self.audit_agent(agent_file)
        
        # Génération rapport consolidé
        audit_duration = (datetime.now() - self.start_time).total_seconds()
        
        # Calcul statistiques globales
        total_agents = len(TARGET_AGENTS)
        successful_audits = sum(1 for r in self.audit_results.values() 
                               if r.get("audit_status") == "success")
        existing_agents = sum(1 for r in self.audit_results.values() 
                             if r.get("exists", False))
        
        scores = [r.get("global_score", 0) for r in self.audit_results.values() 
                 if r.get("global_score") is not None]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        consolidated_report = {
            "audit_summary": {
                "timestamp": datetime.now().isoformat(),
                "total_agents": total_agents,
                "existing_agents": existing_agents,
                "successful_audits": successful_audits,
                "average_score": avg_score,
                "audit_duration": audit_duration,
                "success_rate": (successful_audits / total_agents * 100) if total_agents > 0 else 0
            },
            "agents_analysis": self.audit_results,
            "recommendations": self.generate_recommendations(),
            "new_capabilities_summary": self.analyze_new_capabilities()
        }
        
        return consolidated_report
    
    def generate_recommendations(self) -> List[str]:
        """Génère des recommandations basées sur l'audit"""
        recommendations = []
        
        # Analyse des résultats
        missing_agents = [agent for agent, result in self.audit_results.items() 
                         if not result.get("exists", False)]
        failed_audits = [agent for agent, result in self.audit_results.items() 
                        if result.get("audit_status") != "success"]
        low_scores = [agent for agent, result in self.audit_results.items() 
                     if result.get("global_score", 0) < 70]
        
        if missing_agents:
            recommendations.append(f"❌ CRITIQUE: {len(missing_agents)} agents manquants - Vérifier installation")
        
        if failed_audits:
            recommendations.append(f"🔧 RÉPARATION: {len(failed_audits)} agents avec erreurs d'audit")
        
        if low_scores:
            recommendations.append(f"📈 AMÉLIORATION: {len(low_scores)} agents avec scores < 70/100")
        
        # Analyse des nouvelles capacités
        enterprise_agents = sum(1 for result in self.audit_results.values() 
                               if result.get("capabilities", {}).get("compliance_level") == "enterprise")
        
        if enterprise_agents < len(TARGET_AGENTS):
            recommendations.append("🚀 UPGRADE: Migrer plus d'agents vers niveau Enterprise")
        
        if not recommendations:
            recommendations.append("✅ EXCELLENT: Tous les agents sont en bon état")
        
        return recommendations
    
    def analyze_new_capabilities(self) -> Dict[str, Any]:
        """Analyse des nouvelles capacités détectées"""
        capabilities_summary = {
            "enterprise_features": 0,
            "new_patterns": [],
            "advanced_features": [],
            "compliance_levels": {"basic": 0, "standard": 0, "enterprise": 0}
        }
        
        for agent_file, result in self.audit_results.items():
            capabilities = result.get("capabilities", {})
            
            # Comptage niveaux de compliance
            compliance_level = capabilities.get("compliance_level", "basic")
            capabilities_summary["compliance_levels"][compliance_level] += 1
            
            # Nouvelles fonctionnalités
            new_features = capabilities.get("new_features", [])
            capabilities_summary["advanced_features"].extend(new_features)
            
            # Patterns enterprise
            if "enterprise" in capabilities.get("specialization", []):
                capabilities_summary["enterprise_features"] += 1
        
        # Déduplication
        capabilities_summary["advanced_features"] = list(set(capabilities_summary["advanced_features"]))
        
        return capabilities_summary
    
    def save_report(self, report: Dict[str, Any]) -> str:
        """Sauvegarde le rapport d'audit"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = PROJECT_ROOT / f"audit_agents_cibles_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📊 Rapport sauvegardé: {report_file}")
        return str(report_file)

def main():
    """Point d'entrée principal"""
    print("🎯 AUDIT SIMPLIFIÉ DES 4 AGENTS CIBLES")
    print("="*60)
    
    auditor = AgentAuditor()
    
    try:
        # Exécution audit complet
        report = auditor.run_full_audit()
        
        # Sauvegarde rapport
        report_file = auditor.save_report(report)
        
        # Affichage résultats
        print("\n🎯 RÉSULTATS DE L'AUDIT")
        print("="*60)
        
        summary = report["audit_summary"]
        print(f"🔍 Agents audités: {summary['successful_audits']}/{summary['total_agents']}")
        print(f"📁 Agents existants: {summary['existing_agents']}/{summary['total_agents']}")
        print(f"📊 Score moyen: {summary['average_score']:.1f}/100")
        print(f"⏱️ Durée audit: {summary['audit_duration']:.2f}s")
        print(f"✅ Taux de succès: {summary['success_rate']:.1f}%")
        
        # Détails par agent
        print("\n📋 DÉTAILS PAR AGENT:")
        print("-" * 60)
        for agent_file, result in report["agents_analysis"].items():
            status = "✅" if result.get("exists", False) else "❌"
            score = result.get("global_score", 0)
            agent_type = result.get("capabilities", {}).get("agent_type", "unknown")
            print(f"{status} {agent_file}")
            print(f"    Type: {agent_type} | Score: {score:.1f}/100")
            
            if result.get("capabilities", {}).get("new_features"):
                features = ", ".join(result["capabilities"]["new_features"])
                print(f"    Nouvelles capacités: {features}")
        
        # Nouvelles capacités
        capabilities = report["new_capabilities_summary"]
        print(f"\n🚀 NOUVELLES CAPACITÉS DÉTECTÉES:")
        print(f"🏢 Agents Enterprise: {capabilities['compliance_levels']['enterprise']}")
        print(f"🎯 Fonctionnalités avancées: {len(capabilities['advanced_features'])}")
        if capabilities['advanced_features']:
            print(f"    - {', '.join(capabilities['advanced_features'])}")
        
        # Recommandations
        recommendations = report["recommendations"]
        print(f"\n🎯 RECOMMANDATIONS:")
        for rec in recommendations:
            print(f"   - {rec}")
        
        print(f"\n📊 Rapport détaillé: {report_file}")
        print("="*60)
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ Erreur durant l'audit: {e}")
        print(f"\n❌ ERREUR: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())