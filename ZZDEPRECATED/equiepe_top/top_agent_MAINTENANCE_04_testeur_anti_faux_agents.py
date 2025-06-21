#!/usr/bin/env python3
"""
🧪 TESTEUR AGENTS ENTERPRISE AMÉLIORÉ - DÉTECTION FAUX AGENTS SYNC
===============================================================

🎯 Mission : Détecter les FAUX AGENTS utilisant du code SYNC
⚠️  RÈGLE CRITIQUE : Si le code est 'SYNC' C'EST UN FAUX AGENT !

Détections spécialisées :
- ❌ Méthodes startup(), shutdown(), health_check() SANS async
- ❌ Méthodes execute_task() SANS async  
- ❌ Appels await dans des fonctions non-async
- ❌ Pattern Factory non respecté (Agent de base)
- ❌ Classes qui héritent d'Agent mais implémentent en SYNC

Author: Équipe de Maintenance NextGeneration
Version: 2.0.0 - Anti-Faux-Agents
Created: 2025-01-19
"""

import sys
import ast
import inspect
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import importlib
import time
import re

# 🔧 Correction PYTHONPATH pour imports
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

# Import Pattern Factory (OBLIGATOIRE selon guide)
try:
    from core.agent_factory_architecture import Agent, Task, Result
    PATTERN_FACTORY_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Pattern Factory non disponible: {e}")
    # Fallback pour compatibilité
    class Agent:
        def __init__(self, agent_type: str, **config):
            self.agent_id = f"testeur_anti_faux_agents_{int(time.time())}"
            self.agent_type = agent_type
            self.config = config
            self.logger = print  # Simple fallback pour logging
            
        async def startup(self): pass
        async def shutdown(self): pass
        async def health_check(self): return {"status": "healthy"}
        def get_capabilities(self): return []
    
    class Task:
        def __init__(self, task_id: str, description: str, **kwargs):
            self.task_id = task_id
            self.description = description
            
    class Result:
        def __init__(self, success: bool, data: Any = None, error: str = None):
            self.success = success
            self.data = data
            self.error = error
    
    PATTERN_FACTORY_AVAILABLE = False

@dataclass
class FakeAgentDetection:
    """Résultat de détection d'un faux agent"""
    agent_id: str
    agent_name: str
    is_fake_agent: bool
    sync_violations: List[str]
    async_violations: List[str]
    pattern_factory_violations: List[str]
    compliance_score: float
    recommendation: str
    details: Dict[str, Any]

class ImprovedEnterpriseAgentTester(Agent):
    """🔍 Testeur amélioré pour détecter les FAUX AGENTS SYNC - Pattern Factory"""
    
    def __init__(self, **config):
        # Initialisation Pattern Factory
        super().__init__("testeur_anti_faux_agents", **config)
        # Découverte automatique des agents à tester
        self.agents_directory = Path(".")
        self.agents_to_test = self._discover_agents_automatically()
        
        # Méthodes qui DOIVENT être async selon Pattern Factory
        self.required_async_methods = [
            'startup',
            'shutdown', 
            'health_check',
            'execute_task'
        ]
        
        # Patterns de détection de faux agents
        self.fake_agent_patterns = [
            r'def\s+(startup|shutdown|health_check|execute_task)\s*\(',  # Méthodes SYNC
            r'class\s+\w+\s*\([^)]*Agent[^)]*\).*?def\s+(startup|shutdown|health_check)\s*\(',  # Héritage Agent + SYNC
            r'await\s+.*?\s+def\s+\w+\s*\(',  # await dans fonction non-async
            r'return\s+\{.*"success".*\}.*def\s+startup\s*\(',  # Pattern typique faux agent
        ]
        
        self.test_results: List[FakeAgentDetection] = []
        
    def _discover_agents_automatically(self) -> List[str]:
        """Découverte automatique des agents à tester dans le répertoire"""
        try:
            agent_files = []
            
            # Scanner tous les fichiers agent_*.py dans le répertoire
            for agent_file in self.agents_directory.glob("agent_*.py"):
                # Exclure les agents de maintenance, fichiers de test, et backups_docteur
                if (not agent_file.name.startswith("agent_MAINTENANCE_") and 
                    not agent_file.name.startswith("test_") and
                    agent_file.name != "agent_config.py" and
                    "backups_docteur" not in str(agent_file.parent)):
                    
                    # Extraire le nom du module (sans .py)
                    agent_name = agent_file.stem
                    agent_files.append(agent_name)
            
            print(f"🔍 Découverte automatique: {len(agent_files)} agents trouvés")
            return sorted(agent_files)
            
        except Exception as e:
            print(f"⚠️ Erreur découverte automatique: {e}")
            return []
    
    # Implémentation méthodes abstraites OBLIGATOIRES Pattern Factory
    async def startup(self):
        """Démarrage testeur anti-faux-agents"""
        print(f"🚀 Testeur Anti-Faux-Agents {self.agent_id} - DÉMARRAGE")
        
    async def shutdown(self):
        """Arrêt testeur anti-faux-agents"""
        print(f"🛑 Testeur Anti-Faux-Agents {self.agent_id} - ARRÊT")
        
    async def health_check(self) -> Dict[str, Any]:
        """Vérification santé testeur anti-faux-agents"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": "healthy",
            "agents_to_test": len(self.agents_to_test),
            "last_test_results": len(self.test_results),
            "ready": True
        }
    
    async def execute_task(self, task: Task) -> Result:
        """Exécution des tâches de test anti-faux-agents - Pattern Factory OBLIGATOIRE"""
        try:
            print(f"🎯 Exécution tâche: {task.task_id}")
            
            if task.task_id == "run_fake_detection":
                # Tâche de détection de faux agents
                results = self.run_fake_agent_detection()
                
                return Result(
                    success=True,
                    data={
                        "detection_results": results,
                        "agent_id": self.agent_id,
                        "task_id": task.task_id
                    }
                )
                
            elif task.task_id == "test_single_agent":
                # Tâche de test d'agent unique
                agent_name = getattr(task, 'agent_name', None)
                if not agent_name:
                    return Result(success=False, error="agent_name requis pour test_single_agent")
                    
                detection = self.test_agent_for_fake_detection(agent_name)
                return Result(success=True, data=detection.__dict__)
                
            else:
                return Result(
                    success=False, 
                    error=f"Tâche non reconnue: {task.task_id}"
                )
                
        except Exception as e:
            print(f"❌ Erreur exécution tâche {task.task_id}: {e}")
            return Result(success=False, error=str(e))
    
    def get_capabilities(self) -> List[str]:
        """Retourne les capacités du testeur anti-faux-agents"""
        return [
            "run_fake_detection",
            "test_single_agent",
            "analyze_source_code",
            "detect_sync_violations",
            "calculate_compliance_score",
            "generate_recommendations"
        ]
        
    def analyze_agent_source_code(self, agent_file_path: Path) -> Dict[str, Any]:
        """Analyse du code source pour détecter les violations SYNC"""
        try:
            with open(agent_file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # Parse AST pour analyse structurelle
            tree = ast.parse(source_code)
            
            analysis = {
                'source_code': source_code,
                'ast_tree': tree,
                'classes': [],
                'methods': [],
                'async_methods': [],
                'sync_methods': [],
                'agent_inheritance': False,
                'pattern_factory_imports': False
            }
            
            # Analyse des classes et méthodes
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_info = {
                        'name': node.name,
                        'bases': [base.id if isinstance(base, ast.Name) else str(base) for base in node.bases],
                        'methods': []
                    }
                    
                    # Vérifier héritage Agent
                    if any('Agent' in base for base in class_info['bases']):
                        analysis['agent_inheritance'] = True
                    
                    # Analyser les méthodes de la classe
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_info = {
                                'name': item.name,
                                'is_async': isinstance(item, ast.AsyncFunctionDef),
                                'args': [arg.arg for arg in item.args.args],
                                'decorators': [d.id if isinstance(d, ast.Name) else str(d) for d in item.decorator_list]
                            }
                            class_info['methods'].append(method_info)
                            analysis['methods'].append(method_info)
                            
                            if method_info['is_async']:
                                analysis['async_methods'].append(method_info)
                            else:
                                analysis['sync_methods'].append(method_info)
                        
                        elif isinstance(item, ast.AsyncFunctionDef):
                            method_info = {
                                'name': item.name,
                                'is_async': True,
                                'args': [arg.arg for arg in item.args.args],
                                'decorators': [d.id if isinstance(d, ast.Name) else str(d) for d in item.decorator_list]
                            }
                            class_info['methods'].append(method_info)
                            analysis['methods'].append(method_info)
                            analysis['async_methods'].append(method_info)
                    
                    analysis['classes'].append(class_info)
                
                # Vérifier imports Pattern Factory
                elif isinstance(node, ast.ImportFrom):
                    if node.module and ('agent_factory_architecture' in node.module or 'core' in node.module):
                        analysis['pattern_factory_imports'] = True
            
            return analysis
            
        except Exception as e:
            return {'error': str(e)}
    
    def detect_sync_violations(self, analysis: Dict[str, Any]) -> List[str]:
        """Détection des violations SYNC (FAUX AGENTS)"""
        violations = []
        
        if not analysis.get('agent_inheritance'):
            return violations  # Pas un agent, pas de violation
        
        # Vérifier les méthodes obligatoires async
        sync_methods = analysis.get('sync_methods', [])
        
        for method in sync_methods:
            method_name = method['name']
            
            if method_name in self.required_async_methods:
                violations.append(
                    f"🚨 FAUX AGENT DÉTECTÉ: Méthode '{method_name}()' est SYNC mais DOIT être ASYNC selon Pattern Factory"
                )
        
        # Vérifier cohérence async/await
        source_code = analysis.get('source_code', '')
        
        # Détecter await dans fonctions non-async
        await_pattern = r'def\s+(\w+)\s*\([^)]*\):[^{]*await\s+'
        await_in_sync = re.findall(await_pattern, source_code, re.DOTALL)
        
        for func_name in await_in_sync:
            violations.append(
                f"🚨 FAUX AGENT DÉTECTÉ: Fonction '{func_name}()' utilise 'await' mais n'est pas déclarée 'async'"
            )
        
        # Détecter patterns typiques de faux agents
        for pattern in self.fake_agent_patterns:
            matches = re.findall(pattern, source_code, re.DOTALL | re.IGNORECASE)
            if matches:
                violations.append(
                    f"🚨 FAUX AGENT DÉTECTÉ: Pattern suspect trouvé - {pattern[:50]}..."
                )
        
        return violations
    
    def detect_async_violations(self, analysis: Dict[str, Any]) -> List[str]:
        """Détection des violations dans l'usage d'async"""
        violations = []
        
        async_methods = analysis.get('async_methods', [])
        source_code = analysis.get('source_code', '')
        
        # Vérifier que les méthodes async utilisent bien await
        for method in async_methods:
            method_name = method['name']
            
            # Extraire le corps de la méthode
            method_pattern = rf'async\s+def\s+{method_name}\s*\([^)]*\):(.*?)(?=\n\s*(?:def|class|$))'
            method_match = re.search(method_pattern, source_code, re.DOTALL)
            
            if method_match:
                method_body = method_match.group(1)
                
                # Vérifier présence d'await ou d'opérations async
                if method_name in self.required_async_methods:
                    if 'await' not in method_body and 'asyncio' not in method_body:
                        violations.append(
                            f"⚠️ Méthode async '{method_name}()' ne contient pas d'opérations asynchrones"
                        )
        
        return violations
    
    def detect_pattern_factory_violations(self, analysis: Dict[str, Any]) -> List[str]:
        """Détection des violations Pattern Factory"""
        violations = []
        
        if not analysis.get('pattern_factory_imports'):
            violations.append("❌ Imports Pattern Factory manquants (core.agent_factory_architecture)")
        
        classes = analysis.get('classes', [])
        agent_classes = [cls for cls in classes if any('Agent' in base for base in cls['bases'])]
        
        if not agent_classes:
            violations.append("❌ Aucune classe héritant d'Agent trouvée")
            return violations
        
        for agent_class in agent_classes:
            class_methods = {method['name']: method for method in agent_class['methods']}
            
            # Vérifier méthodes obligatoires Pattern Factory
            for required_method in self.required_async_methods:
                if required_method not in class_methods:
                    violations.append(f"❌ Méthode obligatoire '{required_method}()' manquante dans {agent_class['name']}")
                elif not class_methods[required_method]['is_async']:
                    violations.append(f"🚨 FAUX AGENT: Méthode '{required_method}()' doit être ASYNC dans {agent_class['name']}")
        
        return violations
    
    def calculate_compliance_score(self, sync_violations: List[str], async_violations: List[str], 
                                 pattern_violations: List[str]) -> float:
        """Calcul du score de conformité (0-100)"""
        total_violations = len(sync_violations) + len(async_violations) + len(pattern_violations)
        
        if total_violations == 0:
            return 100.0
        
        # Pénalités par type de violation
        sync_penalty = len(sync_violations) * 30  # Très grave
        async_penalty = len(async_violations) * 10  # Modéré  
        pattern_penalty = len(pattern_violations) * 20  # Grave
        
        total_penalty = sync_penalty + async_penalty + pattern_penalty
        score = max(0.0, 100.0 - total_penalty)
        
        return score
    
    def generate_recommendation(self, detection: FakeAgentDetection) -> str:
        """Génération de recommandation basée sur la détection"""
        if detection.is_fake_agent:
            return "🚨 FAUX AGENT CONFIRMÉ - SUPPRESSION IMMÉDIATE RECOMMANDÉE"
        elif detection.compliance_score < 70:
            return "⚠️ AGENT NON-CONFORME - CORRECTION URGENTE REQUISE"
        elif detection.compliance_score < 90:
            return "🔧 AGENT PARTIELLEMENT CONFORME - AMÉLIORATIONS NÉCESSAIRES"
        else:
            return "✅ AGENT CONFORME - AUCUNE ACTION REQUISE"
    
    def test_agent_for_fake_detection(self, agent_module_name: str) -> FakeAgentDetection:
        """Test complet de détection de faux agent"""
        print(f"🔍 Analyse anti-faux-agent: {agent_module_name}...")
        
        # Trouver le fichier source
        agent_file = Path(__file__).parent / f"{agent_module_name}.py"
        
        if not agent_file.exists():
            return FakeAgentDetection(
                agent_id="unknown",
                agent_name=agent_module_name,
                is_fake_agent=True,
                sync_violations=["Fichier agent introuvable"],
                async_violations=[],
                pattern_factory_violations=[],
                compliance_score=0.0,
                recommendation="🚨 FAUX AGENT CONFIRMÉ - FICHIER MANQUANT",
                details={"error": "Agent file not found"}
            )
        
        # Analyse du code source
        analysis = self.analyze_agent_source_code(agent_file)
        
        if 'error' in analysis:
            return FakeAgentDetection(
                agent_id="unknown",
                agent_name=agent_module_name,
                is_fake_agent=True,
                sync_violations=[f"Erreur analyse: {analysis['error']}"],
                async_violations=[],
                pattern_factory_violations=[],
                compliance_score=0.0,
                recommendation="🚨 FAUX AGENT CONFIRMÉ - ERREUR ANALYSE",
                details=analysis
            )
        
        # Détections des violations
        sync_violations = self.detect_sync_violations(analysis)
        async_violations = self.detect_async_violations(analysis)
        pattern_violations = self.detect_pattern_factory_violations(analysis)
        
        # Calcul score conformité
        compliance_score = self.calculate_compliance_score(sync_violations, async_violations, pattern_violations)
        
        # Détermination si c'est un faux agent
        is_fake_agent = (
            len(sync_violations) > 0 or  # Violations SYNC = faux agent
            compliance_score < 50.0  # Score très bas = suspect
        )
        
        detection = FakeAgentDetection(
            agent_id=agent_module_name.split('_')[1] if '_' in agent_module_name else 'unknown',
            agent_name=analysis.get('classes', [{'name': agent_module_name}])[0]['name'] if analysis.get('classes') else agent_module_name,
            is_fake_agent=is_fake_agent,
            sync_violations=sync_violations,
            async_violations=async_violations,
            pattern_factory_violations=pattern_violations,
            compliance_score=compliance_score,
            recommendation="",  # Sera rempli après
            details=analysis
        )
        
        detection.recommendation = self.generate_recommendation(detection)
        
        return detection
    
    def run_fake_agent_detection(self) -> Dict[str, Any]:
        """Exécution complète de la détection de faux agents"""
        print("🚨 DÉMARRAGE DÉTECTION FAUX AGENTS SYNC")
        print("=" * 60)
        print("⚠️  RÈGLE : Si le code est 'SYNC' C'EST UN FAUX AGENT !")
        print("=" * 60)
        
        fake_agents_detected = 0
        total_violations = 0
        
        for agent_module in self.agents_to_test:
            detection = self.test_agent_for_fake_detection(agent_module)
            self.test_results.append(detection)
            
            # Affichage résultat
            if detection.is_fake_agent:
                status = "🚨 FAUX AGENT DÉTECTÉ"
                fake_agents_detected += 1
            elif detection.compliance_score < 70:
                status = "⚠️ AGENT SUSPECT"
            else:
                status = "✅ AGENT LÉGITIME"
            
            print(f"{status} - {detection.agent_name}")
            print(f"   Score conformité: {detection.compliance_score:.1f}%")
            print(f"   Recommandation: {detection.recommendation}")
            
            # Détail des violations
            if detection.sync_violations:
                print(f"   🚨 Violations SYNC: {len(detection.sync_violations)}")
                for violation in detection.sync_violations[:2]:  # Limite affichage
                    print(f"      - {violation}")
            
            if detection.async_violations:
                print(f"   ⚠️ Violations ASYNC: {len(detection.async_violations)}")
            
            if detection.pattern_factory_violations:
                print(f"   ❌ Violations Pattern Factory: {len(detection.pattern_factory_violations)}")
            
            total_violations += len(detection.sync_violations) + len(detection.async_violations) + len(detection.pattern_factory_violations)
            print()
        
        # Rapport final
        legitimate_agents = len(self.test_results) - fake_agents_detected
        
        print("=" * 60)
        print(f"📊 RÉSULTATS DÉTECTION FAUX AGENTS:")
        print(f"   🚨 FAUX AGENTS DÉTECTÉS: {fake_agents_detected}")
        print(f"   ✅ AGENTS LÉGITIMES: {legitimate_agents}")
        print(f"   📊 TOTAL VIOLATIONS: {total_violations}")
        
        if fake_agents_detected > 0:
            print(f"   🔥 ACTION IMMÉDIATE REQUISE: Supprimer les {fake_agents_detected} faux agents !")
        else:
            print("   🎉 AUCUN FAUX AGENT DÉTECTÉ - Tous les agents sont conformes !")
        
        return {
            "fake_agents_detected": fake_agents_detected,
            "legitimate_agents": legitimate_agents,
            "total_violations": total_violations,
            "detection_results": self.test_results,
            "requires_immediate_action": fake_agents_detected > 0
        }

def main():
    """Test principal de détection de faux agents"""
    print("🔍 TESTEUR AGENTS ENTERPRISE AMÉLIORÉ - ANTI-FAUX-AGENTS")
    print("Version: 2.0.0 - Détection SYNC/ASYNC")
    print()
    
    tester = ImprovedEnterpriseAgentTester()
    results = tester.run_fake_agent_detection()
    
    # Code de sortie pour CI/CD
    if results["requires_immediate_action"]:
        print("\n❌ ÉCHEC: Faux agents détectés - Intervention requise")
        sys.exit(1)
    else:
        print("\n✅ SUCCÈS: Tous les agents sont légitimes")
        sys.exit(0)

if __name__ == "__main__":
    main() 