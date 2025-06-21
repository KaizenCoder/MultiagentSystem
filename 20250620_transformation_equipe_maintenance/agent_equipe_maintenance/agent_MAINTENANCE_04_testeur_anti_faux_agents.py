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
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import importlib
import time
import re
from logging_manager_optimized import LoggingManager

# 🔧 Correction PYTHONPATH pour imports
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

# Import Pattern Factory (OBLIGATOIRE selon guide)
try:
    from agent_factory_implementation.core.agent_factory_architecture import Agent, Task, Result
    PATTERN_FACTORY_AVAILABLE = True
except ImportError:
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
        
        # S'assurer que le logger est disponible (fallback si nécessaire)
        if not hasattr(self, 'logger') or self.logger == print:
            # S'assurer que agent_id existe
            if not hasattr(self, 'agent_id'):
                self.agent_id = f"testeur_anti_faux_agents_{int(time.time())}"
            
            logging.basicConfig(level=logging.INFO)
            # LoggingManager NextGeneration - Agent
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_agent_logger(
            agent_name="import",
            role="ai_processor",
            domain="testing",
            async_enabled=True
        )
        
        # Configuration logging Pattern Factory
        self.logger.info(f"🔍 TesteurAntiFauxAgents initialisé - ID: {self.agent_id}")
        
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
        self.logger.info(f"🚀 Testeur Anti-Faux-Agents {self.agent_id} - DÉMARRAGE")
        self.logger.info("✅ Agent démarré avec succès")
        
    async def shutdown(self):
        """Arrêt testeur anti-faux-agents"""
        self.logger.info(f"🛑 Testeur Anti-Faux-Agents {self.agent_id} - ARRÊT")
        
    async def health_check(self) -> Dict[str, Any]:
        """Vérification santé testeur anti-faux-agents"""
        # S'assurer que agent_id existe
        if not hasattr(self, 'agent_id'):
            self.agent_id = f"testeur_anti_faux_agents_{int(time.time())}"
        
        # S'assurer que agent_type existe
        if not hasattr(self, 'agent_type'):
            self.agent_type = "testeur_anti_faux_agents"
        
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
            
            elif task.task_id == "pattern_factory_audit":
                # 🚨 NOUVELLE TÂCHE : Audit conformité Pattern Factory
                target_directory = getattr(task, 'target_directory', None)
                audit_results = self.run_pattern_factory_audit(target_directory)
                
                return Result(
                    success=True,
                    data={
                        "audit_results": audit_results,
                        "agent_id": self.agent_id,
                        "task_id": task.task_id,
                        "audit_summary": {
                            "agents_found": audit_results.get('agents_found', 0),
                            "agents_analyzed": audit_results.get('agents_analyzed', 0),
                            "critical_errors": audit_results.get('conformity_summary', {}).get('critical_errors', 0),
                            "non_compliant": audit_results.get('conformity_summary', {}).get('non_compliant', 0)
                        }
                    }
                )
                
            elif task.task_id == "test_single_agent":
                # Tâche de test d'agent unique
                agent_name = getattr(task, 'agent_name', None)
                if not agent_name:
                    return Result(
                        success=False,
                        error="Nom d'agent requis pour test_single_agent"
                    )
                
                detection = self.test_agent_for_fake_detection(agent_name)
                
                return Result(
                    success=True,
                    data={
                        "detection": detection.__dict__,
                        "agent_id": self.agent_id,
                        "task_id": task.task_id
                    }
                )
            
            elif task.task_id == "verify_compliance":
                # 🚨 NOUVELLE TÂCHE : Vérification conformité fichier spécifique
                file_path = getattr(task, 'file_path', None)
                if not file_path:
                    return Result(
                        success=False,
                        error="Chemin fichier requis pour verify_compliance"
                    )
                
                compliance_report = self.verify_pattern_factory_compliance(Path(file_path))
                
                return Result(
                    success=True,
                    data={
                        "compliance_report": compliance_report,
                        "agent_id": self.agent_id,
                        "task_id": task.task_id
                    }
                )
                
            else:
                return Result(
                    success=False,
                    error=f"Tâche inconnue: {task.task_id}"
                )
                
        except Exception as e:
            return Result(
                success=False,
                error=f"Erreur exécution tâche {task.task_id}: {str(e)}"
            )
    
    def get_capabilities(self) -> List[str]:
        """Retourne les capacités du testeur anti-faux-agents"""
        return [
            "run_fake_detection",
            "test_single_agent",
            "analyze_source_code",
            "detect_sync_violations",
            "calculate_compliance_score",
            "generate_recommendations",
            # 🆕 NOUVELLES CAPACITÉS AVANCÉES
            "async_sync_validation",
            "compliance_scoring",
            "advanced_static_analysis",
            "suspicious_patterns_detection",
            "mandatory_methods_validation",
            "import_validation",
            "enterprise_grade_validation",
            "security_patterns_detection"
        ]

    async def tester_integration(self) -> Dict[str, Any]:
        """Méthode de test d'intégration pour le workflow du chef d'équipe"""
        try:
            self.logger.info("🧪 Démarrage tests d'intégration anti-faux-agents")
            
            # Exécuter les tests de détection de faux agents
            detection_results = self.run_fake_agent_detection()
            
            result = {
                "status": "completed",
                "tests_executed": len(self.agents_to_test),
                "fake_agents_detected": len([r for r in self.test_results if r.is_fake_agent]),
                "detection_results": detection_results,
                "timestamp": time.time(),
                "agent_id": self.agent_id
            }
            
            self.logger.info("✅ Tests d'intégration terminés")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Erreur tests d'intégration: {e}")
            return {
                "status": "error",
                "error": str(e),
                "agent_id": getattr(self, 'agent_id', 'unknown')
            }
        
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
        """Détection des violations Pattern Factory - AMÉLIORÉ pour détecter les vrais problèmes"""
        violations = []
        source_code = analysis.get('source_code', '')
        tree = analysis.get('ast_tree')
        
        # 🚨 NOUVELLE DÉTECTION : Erreurs syntaxe "async async def"
        if 'async async def' in source_code:
            violations.append("CRITIQUE: Erreur syntaxe 'async async def' détectée - Code non-fonctionnel")
        
        # 🚨 NOUVELLE DÉTECTION : Fallback Pattern Factory utilisé
        if 'PATTERN_FACTORY_AVAILABLE = False' in source_code:
            violations.append("MAJEUR: Pattern Factory non disponible - Utilisation du fallback")
        
        # 🚨 NOUVELLE DÉTECTION : Import Pattern Factory échoue
        if 'Pattern Factory non disponible' in source_code:
            violations.append("MAJEUR: Échec import Pattern Factory - Framework non accessible")
        
        # 🚨 NOUVELLE DÉTECTION : Héritage Agent non conforme
        if tree:
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Vérifier si la classe hérite réellement d'Agent du Pattern Factory
                    if node.bases:
                        for base in node.bases:
                            if isinstance(base, ast.Name) and base.id == 'Agent':
                                # Classe hérite d'Agent mais utilise sa propre implémentation
                                if 'class Agent:' in source_code and 'fallback' in source_code.lower():
                                    violations.append(f"MAJEUR: Classe {node.name} hérite d'Agent fallback local au lieu du Pattern Factory")
        
        # 🚨 NOUVELLE DÉTECTION : Architecture hybride détectée
        if 'try:' in source_code and 'ImportError' in source_code and 'Agent' in source_code:
            if not any('super().__init__' in line for line in source_code.split('\n')):
                violations.append("MAJEUR: Architecture hybride - Pas d'héritage réel du Pattern Factory")
        
        # Détections existantes améliorées
        if tree:
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Vérifier si hérite d'Agent
                    inherits_agent = any(isinstance(base, ast.Name) and base.id == "Agent" for base in node.bases)
                    
                    if inherits_agent:
                        # Vérifier les méthodes requises
                        methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                        
                        for required_method in self.required_async_methods:
                            if required_method not in methods:
                                violations.append(f"Méthode requise manquante: {required_method}")
                            else:
                                # Vérifier si la méthode est async
                                for method_node in node.body:
                                    if (isinstance(method_node, ast.FunctionDef) and 
                                        method_node.name == required_method):
                                        if not isinstance(method_node, ast.AsyncFunctionDef):
                                            violations.append(f"Méthode {required_method} n'est pas async")
        
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
    
    # 🆕 NOUVELLES MÉTHODES AVANCÉES
    
    def async_sync_validation(self, agent_file_path: Path) -> Dict[str, Any]:
        """Validation avancée async/sync avec détection de patterns complexes"""
        try:
            with open(agent_file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # Patterns async/sync avancés
            async_sync_issues = []
            
            # Détecter await dans fonctions sync
            await_in_sync_pattern = r'def\s+(\w+)\s*\([^)]*\):[^{]*?await\s+'
            matches = re.findall(await_in_sync_pattern, source_code, re.DOTALL)
            for func_name in matches:
                async_sync_issues.append(f"await dans fonction sync: {func_name}()")
            
            # Détecter fonctions async sans await
            async_without_await = r'async\s+def\s+(\w+)\s*\([^)]*\):[^{]*?(?!.*await)'
            matches = re.findall(async_without_await, source_code, re.DOTALL)
            for func_name in matches:
                if func_name not in ['startup', 'shutdown']:  # Exceptions autorisées
                    async_sync_issues.append(f"Fonction async sans await: {func_name}()")
            
            return {
                "async_sync_issues": async_sync_issues,
                "compliance_level": "HIGH" if not async_sync_issues else "LOW",
                "recommendations": self._generate_async_sync_recommendations(async_sync_issues)
            }
            
        except Exception as e:
            return {"error": f"Erreur validation async/sync: {e}"}
    
    def advanced_static_analysis(self, agent_file_path: Path) -> Dict[str, Any]:
        """Analyse statique avancée du code agent"""
        try:
            with open(agent_file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            tree = ast.parse(source_code)
            
            analysis_results = {
                "code_complexity": self._calculate_code_complexity(tree),
                "security_patterns": self._detect_security_patterns(source_code),
                "performance_patterns": self._detect_performance_patterns(source_code),
                "maintainability_score": self._calculate_maintainability_score(tree),
                "enterprise_readiness": self._assess_enterprise_readiness(source_code)
            }
            
            return analysis_results
            
        except Exception as e:
            return {"error": f"Erreur analyse statique: {e}"}
    
    def suspicious_patterns_detection(self, agent_file_path: Path) -> Dict[str, Any]:
        """Détection de patterns suspects dans le code"""
        try:
            with open(agent_file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            suspicious_patterns = []
            
            # Patterns suspects
            suspect_patterns = {
                "hardcoded_credentials": r'(password|secret|key)\s*=\s*["\'][^"\']+["\']',
                "eval_usage": r'\beval\s*\(',
                "exec_usage": r'\bexec\s*\(',
                "shell_injection": r'subprocess\.(call|run|Popen).*shell\s*=\s*True',
                "sql_injection_risk": r'["\'].*%s.*["\']|f["\'].*\{.*\}.*["\'].*sql',
                "unsafe_pickle": r'pickle\.loads?\s*\(',
                "debug_code": r'print\s*\(.*debug|pdb\.set_trace|breakpoint\(\)'
            }
            
            for pattern_name, pattern in suspect_patterns.items():
                matches = re.findall(pattern, source_code, re.IGNORECASE)
                if matches:
                    suspicious_patterns.append({
                        "pattern": pattern_name,
                        "occurrences": len(matches),
                        "severity": self._get_pattern_severity(pattern_name)
                    })
            
            return {
                "suspicious_patterns": suspicious_patterns,
                "risk_level": self._calculate_risk_level(suspicious_patterns),
                "security_recommendations": self._generate_security_recommendations(suspicious_patterns)
            }
            
        except Exception as e:
            return {"error": f"Erreur détection patterns suspects: {e}"}
    
    def mandatory_methods_validation(self, agent_file_path: Path) -> Dict[str, Any]:
        """Validation des méthodes obligatoires Pattern Factory"""
        try:
            analysis = self.analyze_agent_source_code(agent_file_path)
            
            mandatory_methods = {
                "startup": {"required": True, "async": True, "params": []},
                "shutdown": {"required": True, "async": True, "params": []},
                "health_check": {"required": True, "async": True, "return_type": "Dict"},
                "execute_task": {"required": True, "async": True, "params": ["task"]},
                "get_capabilities": {"required": True, "async": False, "return_type": "List"}
            }
            
            validation_results = {}
            
            classes = analysis.get('classes', [])
            agent_classes = [cls for cls in classes if any('Agent' in base for base in cls['bases'])]
            
            for agent_class in agent_classes:
                class_validation = {}
                class_methods = {method['name']: method for method in agent_class['methods']}
                
                for method_name, requirements in mandatory_methods.items():
                    method_validation = {
                        "present": method_name in class_methods,
                        "async_compliant": False,
                        "signature_valid": False,
                        "issues": []
                    }
                    
                    if method_name in class_methods:
                        method_info = class_methods[method_name]
                        
                        # Vérifier async
                        if requirements["async"] and not method_info["is_async"]:
                            method_validation["issues"].append(f"Méthode {method_name}() doit être async")
                        elif not requirements["async"] and method_info["is_async"]:
                            method_validation["issues"].append(f"Méthode {method_name}() ne doit pas être async")
                        else:
                            method_validation["async_compliant"] = True
                        
                        # Vérifier signature (simplifié)
                        method_validation["signature_valid"] = True  # Validation basique
                    else:
                        method_validation["issues"].append(f"Méthode obligatoire {method_name}() manquante")
                    
                    class_validation[method_name] = method_validation
                
                validation_results[agent_class['name']] = class_validation
            
            return {
                "validation_results": validation_results,
                "overall_compliance": self._calculate_methods_compliance(validation_results)
            }
            
        except Exception as e:
            return {"error": f"Erreur validation méthodes: {e}"}
    
    def import_validation(self, agent_file_path: Path) -> Dict[str, Any]:
        """Validation des imports Pattern Factory et dépendances"""
        try:
            with open(agent_file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            import_analysis = {
                "pattern_factory_imports": [],
                "missing_imports": [],
                "deprecated_imports": [],
                "security_risk_imports": [],
                "recommendations": []
            }
            
            # Vérifier imports Pattern Factory
            required_imports = [
                "from core.agent_factory_architecture import Agent",
                "from core.agent_factory_architecture import Task", 
                "from core.agent_factory_architecture import Result"
            ]
            
            for required_import in required_imports:
                if required_import in source_code:
                    import_analysis["pattern_factory_imports"].append(required_import)
                else:
                    import_analysis["missing_imports"].append(required_import)
            
            # Détecter imports à risque
            risky_imports = ["os.system", "subprocess.call", "eval", "exec", "pickle"]
            for risky in risky_imports:
                if risky in source_code:
                    import_analysis["security_risk_imports"].append(risky)
            
            # Générer recommandations
            if import_analysis["missing_imports"]:
                import_analysis["recommendations"].append("Ajouter les imports Pattern Factory manquants")
            if import_analysis["security_risk_imports"]:
                import_analysis["recommendations"].append("Réviser les imports à risque de sécurité")
            
            return import_analysis
            
        except Exception as e:
            return {"error": f"Erreur validation imports: {e}"}
    
    def enterprise_grade_validation(self, agent_file_path: Path) -> Dict[str, Any]:
        """Validation complète niveau enterprise"""
        try:
            # Combiner toutes les validations
            async_sync_results = self.async_sync_validation(agent_file_path)
            static_analysis = self.advanced_static_analysis(agent_file_path)
            suspicious_patterns = self.suspicious_patterns_detection(agent_file_path)
            methods_validation = self.mandatory_methods_validation(agent_file_path)
            import_validation = self.import_validation(agent_file_path)
            
            # Calculer score enterprise global
            enterprise_score = self._calculate_enterprise_score(
                async_sync_results, static_analysis, suspicious_patterns,
                methods_validation, import_validation
            )
            
            return {
                "enterprise_score": enterprise_score,
                "async_sync_validation": async_sync_results,
                "static_analysis": static_analysis,
                "suspicious_patterns": suspicious_patterns,
                "methods_validation": methods_validation,
                "import_validation": import_validation,
                "enterprise_ready": enterprise_score >= 85.0,
                "certification_level": self._determine_certification_level(enterprise_score)
            }
            
        except Exception as e:
            return {"error": f"Erreur validation enterprise: {e}"}
    
    # Méthodes utilitaires pour les nouvelles fonctionnalités
    
    def _generate_async_sync_recommendations(self, issues: List[str]) -> List[str]:
        """Génère des recommandations pour les problèmes async/sync"""
        recommendations = []
        for issue in issues:
            if "await dans fonction sync" in issue:
                recommendations.append("Convertir la fonction en async def")
            elif "async sans await" in issue:
                recommendations.append("Ajouter await ou retirer async")
        return recommendations
    
    def _calculate_code_complexity(self, tree: ast.AST) -> int:
        """Calcule la complexité cyclomatique simplifiée"""
        complexity = 1  # Base
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        return complexity
    
    def _detect_security_patterns(self, source_code: str) -> List[str]:
        """Détecte les patterns de sécurité"""
        security_patterns = []
        if "password" in source_code.lower():
            security_patterns.append("Référence mot de passe détectée")
        if "sql" in source_code.lower() and "%" in source_code:
            security_patterns.append("Risque injection SQL")
        return security_patterns
    
    def _detect_performance_patterns(self, source_code: str) -> List[str]:
        """Détecte les patterns de performance"""
        performance_patterns = []
        if "time.sleep" in source_code:
            performance_patterns.append("Utilisation de sleep détectée")
        if source_code.count("for") > 3:
            performance_patterns.append("Boucles multiples - optimisation possible")
        return performance_patterns
    
    def _calculate_maintainability_score(self, tree: ast.AST) -> float:
        """Calcule un score de maintenabilité"""
        # Simplifié : basé sur le nombre de classes et fonctions
        classes = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
        functions = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
        return min(100.0, (classes * 10 + functions * 5))
    
    def _assess_enterprise_readiness(self, source_code: str) -> str:
        """Évalue la préparation enterprise"""
        if "async def" in source_code and "Pattern Factory" in source_code:
            return "HIGH"
        elif "async def" in source_code:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _get_pattern_severity(self, pattern_name: str) -> str:
        """Détermine la sévérité d'un pattern suspect"""
        high_severity = ["hardcoded_credentials", "eval_usage", "exec_usage", "shell_injection"]
        if pattern_name in high_severity:
            return "HIGH"
        return "MEDIUM"
    
    def _calculate_risk_level(self, suspicious_patterns: List[Dict]) -> str:
        """Calcule le niveau de risque global"""
        if not suspicious_patterns:
            return "LOW"
        high_risk_count = len([p for p in suspicious_patterns if p["severity"] == "HIGH"])
        if high_risk_count > 0:
            return "HIGH"
        return "MEDIUM"
    
    def _generate_security_recommendations(self, patterns: List[Dict]) -> List[str]:
        """Génère des recommandations de sécurité"""
        recommendations = []
        for pattern in patterns:
            if pattern["pattern"] == "hardcoded_credentials":
                recommendations.append("Utiliser des variables d'environnement pour les credentials")
            elif pattern["pattern"] == "eval_usage":
                recommendations.append("Éviter eval() - utiliser des alternatives sécurisées")
        return recommendations
    
    def _calculate_methods_compliance(self, validation_results: Dict) -> float:
        """Calcule le taux de conformité des méthodes"""
        if not validation_results:
            return 0.0
        
        total_methods = 0
        compliant_methods = 0
        
        for class_name, methods in validation_results.items():
            for method_name, validation in methods.items():
                total_methods += 1
                if validation["present"] and validation["async_compliant"] and not validation["issues"]:
                    compliant_methods += 1
        
        return (compliant_methods / total_methods * 100) if total_methods > 0 else 0.0
    
    def _calculate_enterprise_score(self, async_sync: Dict, static: Dict, 
                                  suspicious: Dict, methods: Dict, imports: Dict) -> float:
        """Calcule le score enterprise global"""
        scores = []
        
        # Score async/sync
        if async_sync.get("compliance_level") == "HIGH":
            scores.append(95.0)
        elif async_sync.get("compliance_level") == "MEDIUM":
            scores.append(75.0)
        else:
            scores.append(50.0)
        
        # Score méthodes
        methods_score = methods.get("overall_compliance", 0.0)
        scores.append(methods_score)
        
        # Score sécurité (basé sur patterns suspects)
        risk_level = suspicious.get("risk_level", "HIGH")
        if risk_level == "LOW":
            scores.append(95.0)
        elif risk_level == "MEDIUM":
            scores.append(75.0)
        else:
            scores.append(40.0)
        
        # Score imports
        missing_imports = len(imports.get("missing_imports", []))
        import_score = max(50.0, 100.0 - (missing_imports * 20))
        scores.append(import_score)
        
        return sum(scores) / len(scores)
    
    def _determine_certification_level(self, score: float) -> str:
        """Détermine le niveau de certification"""
        if score >= 95.0:
            return "ENTERPRISE_PREMIUM"
        elif score >= 85.0:
            return "ENTERPRISE_STANDARD"
        elif score >= 70.0:
            return "BUSINESS_READY"
        elif score >= 50.0:
            return "DEVELOPMENT"
        else:
            return "NON_COMPLIANT"

    def verify_pattern_factory_compliance(self, agent_file_path: Path) -> Dict[str, Any]:
        """🚨 NOUVELLE MÉTHODE : Vérification complète conformité Pattern Factory"""
        try:
            source_code = agent_file_path.read_text(encoding='utf-8')
            
            compliance_report = {
                "agent_file": str(agent_file_path),
                "pattern_factory_available": False,
                "inherits_from_agent": False,
                "uses_fallback": False,
                "syntax_errors": [],
                "import_errors": [],
                "architecture_issues": [],
                "compliance_score": 0.0,
                "recommendation": "",
                "critical_issues": []
            }
            
            # 1. Vérifier syntaxe Python basique
            syntax_issues = self._check_python_syntax(source_code)
            compliance_report["syntax_errors"] = syntax_issues
            
            # 2. Vérifier imports Pattern Factory
            import_analysis = self._analyze_pattern_factory_imports(source_code)
            compliance_report.update(import_analysis)
            
            # 3. Vérifier héritage réel
            inheritance_analysis = self._analyze_agent_inheritance(source_code)
            compliance_report.update(inheritance_analysis)
            
            # 4. Vérifier architecture
            architecture_analysis = self._analyze_architecture_compliance(source_code)
            compliance_report["architecture_issues"] = architecture_analysis
            
            # 5. Calculer score de conformité
            compliance_report["compliance_score"] = self._calculate_pattern_factory_score(compliance_report)
            
            # 6. Générer recommandations
            compliance_report["recommendation"] = self._generate_pattern_factory_recommendations(compliance_report)
            
            return compliance_report
            
        except Exception as e:
            return {
                "agent_file": str(agent_file_path),
                "error": f"Erreur analyse conformité: {e}",
                "compliance_score": 0.0,
                "critical_issues": [f"Impossible d'analyser le fichier: {e}"]
            }
    
    def _check_python_syntax(self, source_code: str) -> List[str]:
        """Vérification syntaxe Python basique"""
        syntax_errors = []
        
        # Détecter async async def
        if 'async async def' in source_code:
            lines = source_code.split('\n')
            for i, line in enumerate(lines, 1):
                if 'async async def' in line:
                    syntax_errors.append(f"CRITIQUE ligne {i}: 'async async def' - Syntaxe Python invalide")
        
        # Tenter compilation AST
        try:
            ast.parse(source_code)
        except SyntaxError as e:
            syntax_errors.append(f"CRITIQUE: Erreur syntaxe Python - {e}")
        
        return syntax_errors
    
    def _analyze_pattern_factory_imports(self, source_code: str) -> Dict[str, Any]:
        """Analyse des imports Pattern Factory"""
        result = {
            "pattern_factory_available": False,
            "uses_fallback": False,
            "import_errors": []
        }
        
        # Détecter tentative d'import
        if 'from agent_factory_implementation.core.agent_factory_architecture import' in source_code:
            result["pattern_factory_available"] = True
        elif 'from core.agent_factory_architecture import' in source_code:
            result["pattern_factory_available"] = True
        
        # Détecter utilisation fallback
        if 'PATTERN_FACTORY_AVAILABLE = False' in source_code:
            result["uses_fallback"] = True
            result["import_errors"].append("Pattern Factory non disponible - Fallback utilisé")
        
        # Détecter échec import explicite
        if 'Pattern Factory non disponible' in source_code:
            result["import_errors"].append("Échec import Pattern Factory explicite")
        
        return result
    
    def _analyze_agent_inheritance(self, source_code: str) -> Dict[str, Any]:
        """Analyse de l'héritage réel des classes Agent"""
        result = {
            "inherits_from_agent": False,
            "uses_super_init": False,
            "agent_classes": []
        }
        
        try:
            tree = ast.parse(source_code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Vérifier héritage Agent
                    for base in node.bases:
                        if isinstance(base, ast.Name) and base.id == 'Agent':
                            result["inherits_from_agent"] = True
                            result["agent_classes"].append(node.name)
                            
                            # Vérifier utilisation super().__init__
                            for method in node.body:
                                if isinstance(method, ast.FunctionDef) and method.name == '__init__':
                                    for stmt in ast.walk(method):
                                        if isinstance(stmt, ast.Call):
                                            if (isinstance(stmt.func, ast.Attribute) and
                                                isinstance(stmt.func.value, ast.Call) and
                                                isinstance(stmt.func.value.func, ast.Name) and
                                                stmt.func.value.func.id == 'super'):
                                                result["uses_super_init"] = True
                                                break
        
        except Exception as e:
            result["error"] = f"Erreur analyse AST: {e}"
        
        return result
    
    def _analyze_architecture_compliance(self, source_code: str) -> List[str]:
        """Analyse conformité architecture"""
        issues = []
        
        # Détecter classe Agent définie localement (fallback)
        if 'class Agent:' in source_code and 'fallback' in source_code.lower():
            issues.append("MAJEUR: Classe Agent définie localement - Pas d'utilisation du Pattern Factory")
        
        # Détecter pattern try/except sans super()
        if ('try:' in source_code and 'ImportError' in source_code and 
            'super()' not in source_code):
            issues.append("MAJEUR: Import conditionnel sans héritage réel")
        
        # Détecter méthodes avec erreur syntaxe
        if 'async async def' in source_code:
            issues.append("CRITIQUE: Méthodes avec syntaxe invalide - Code non-fonctionnel")
        
        return issues
    
    def _calculate_pattern_factory_score(self, report: Dict[str, Any]) -> float:
        """Calcul score conformité Pattern Factory"""
        score = 100.0
        
        # Pénalités
        if report.get("syntax_errors"):
            score -= 50.0  # Erreur syntaxe = très grave
        
        if not report.get("pattern_factory_available"):
            score -= 30.0  # Pattern Factory non disponible
        
        if report.get("uses_fallback"):
            score -= 25.0  # Utilise fallback
        
        if not report.get("inherits_from_agent"):
            score -= 20.0  # Pas d'héritage
        
        if not report.get("uses_super_init"):
            score -= 15.0  # Pas de super().__init__
        
        if report.get("architecture_issues"):
            score -= len(report["architecture_issues"]) * 10.0
        
        return max(0.0, score)
    
    def _generate_pattern_factory_recommendations(self, report: Dict[str, Any]) -> str:
        """Génération recommandations conformité Pattern Factory"""
        recommendations = []
        
        if report.get("syntax_errors"):
            recommendations.append("🚨 URGENT: Corriger erreurs syntaxe Python")
        
        if not report.get("pattern_factory_available"):
            recommendations.append("📦 Installer/Configurer Pattern Factory")
        
        if report.get("uses_fallback"):
            recommendations.append("🔧 Migrer du fallback vers Pattern Factory réel")
        
        if not report.get("inherits_from_agent"):
            recommendations.append("🏗️ Implémenter héritage classe Agent")
        
        if not report.get("uses_super_init"):
            recommendations.append("⚡ Ajouter super().__init__() dans constructeur")
        
        if not recommendations:
            recommendations.append("✅ Agent conforme au Pattern Factory")
        
        return " | ".join(recommendations)
    
    def run_pattern_factory_audit(self, target_directory: str = None) -> Dict[str, Any]:
        """🚨 NOUVELLE MÉTHODE : Audit complet conformité Pattern Factory"""
        if target_directory:
            audit_directory = Path(target_directory)
        else:
            # Utiliser le répertoire des agents factory par défaut
            audit_directory = Path("../nextgeneration/agent_factory_implementation/agents")
        
        audit_results = {
            "audit_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "directory_scanned": str(audit_directory),
            "agents_found": 0,
            "agents_analyzed": 0,
            "conformity_summary": {
                "compliant": 0,
                "partially_compliant": 0,
                "non_compliant": 0,
                "critical_errors": 0
            },
            "detailed_results": [],
            "critical_issues": [],
            "recommendations": []
        }
        
        try:
            if not audit_directory.exists():
                audit_results["error"] = f"Répertoire non trouvé: {audit_directory}"
                return audit_results
            
            # Scanner tous les fichiers agent_*.py
            agent_files = list(audit_directory.glob("agent_*.py"))
            audit_results["agents_found"] = len(agent_files)
            
            for agent_file in agent_files:
                try:
                    # Analyser conformité Pattern Factory
                    compliance_report = self.verify_pattern_factory_compliance(agent_file)
                    audit_results["detailed_results"].append(compliance_report)
                    audit_results["agents_analyzed"] += 1
                    
                    # Classifier selon conformité
                    score = compliance_report.get("compliance_score", 0)
                    if score >= 90:
                        audit_results["conformity_summary"]["compliant"] += 1
                    elif score >= 50:
                        audit_results["conformity_summary"]["partially_compliant"] += 1
                    else:
                        audit_results["conformity_summary"]["non_compliant"] += 1
                    
                    # Identifier problèmes critiques
                    if compliance_report.get("syntax_errors"):
                        audit_results["conformity_summary"]["critical_errors"] += 1
                        audit_results["critical_issues"].extend(compliance_report["syntax_errors"])
                
                except Exception as e:
                    audit_results["critical_issues"].append(f"Erreur analyse {agent_file.name}: {e}")
            
            # Générer recommandations globales
            audit_results["recommendations"] = self._generate_audit_recommendations(audit_results)
            
            # Sauvegarder rapport
            self._save_pattern_factory_audit_report(audit_results)
            
        except Exception as e:
            audit_results["error"] = f"Erreur audit: {e}"
        
        return audit_results
    
    def _generate_audit_recommendations(self, audit_results: Dict[str, Any]) -> List[str]:
        """Génération recommandations audit global"""
        recommendations = []
        summary = audit_results["conformity_summary"]
        
        if summary["critical_errors"] > 0:
            recommendations.append(f"🚨 URGENT: {summary['critical_errors']} agents avec erreurs critiques")
        
        if summary["non_compliant"] > 0:
            recommendations.append(f"🔧 {summary['non_compliant']} agents non-conformes nécessitent migration")
        
        if summary["partially_compliant"] > 0:
            recommendations.append(f"⚡ {summary['partially_compliant']} agents partiellement conformes à améliorer")
        
        if summary["compliant"] == audit_results["agents_analyzed"]:
            recommendations.append("✅ Tous les agents sont conformes au Pattern Factory")
        
        return recommendations
    
    def _save_pattern_factory_audit_report(self, audit_results: Dict[str, Any]):
        """Sauvegarde rapport audit Pattern Factory"""
        try:
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            report_file = reports_dir / f"pattern_factory_audit_{timestamp}.json"
            
            import json
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(audit_results, f, indent=2, ensure_ascii=False)
            
            print(f"📋 Rapport audit sauvegardé: {report_file}")
            
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde rapport: {e}")

# Fonction factory pour créer l'agent (Pattern Factory)
def create_agent_testeur_anti_faux(**config) -> ImprovedEnterpriseAgentTester:
    """Factory function pour créer un Agent Testeur Anti-Faux conforme Pattern Factory"""
    return ImprovedEnterpriseAgentTester(**config)

def main():
    """Point d'entrée principal - Test complet avec nouvelles fonctionnalités Pattern Factory"""
    print("🧪 DÉMARRAGE TESTEUR ANTI-FAUX-AGENTS - VERSION AMÉLIORÉE")
    print("=" * 80)
    
    # Créer instance testeur amélioré
    testeur = ImprovedEnterpriseAgentTester()
    
    print(f"\n📋 Agent ID: {testeur.agent_id}")
    print(f"🎯 Agents à tester découverts: {len(testeur.agents_to_test)}")
    print(f"🔧 Pattern Factory disponible: {PATTERN_FACTORY_AVAILABLE}")
    
    # 🚨 NOUVELLE FONCTIONNALITÉ : Test audit conformité Pattern Factory
    print("\n" + "=" * 80)
    print("🔍 AUDIT CONFORMITÉ PATTERN FACTORY")
    print("=" * 80)
    
    try:
        # Lancer audit Pattern Factory sur le répertoire des agents
        audit_results = testeur.run_pattern_factory_audit()
        
        print(f"\n📊 RÉSULTATS AUDIT PATTERN FACTORY:")
        print(f"   📂 Répertoire scanné: {audit_results.get('directory_scanned', 'N/A')}")
        print(f"   🔍 Agents trouvés: {audit_results.get('agents_found', 0)}")
        print(f"   ✅ Agents analysés: {audit_results.get('agents_analyzed', 0)}")
        
        summary = audit_results.get('conformity_summary', {})
        print(f"\n📋 RÉSUMÉ CONFORMITÉ:")
        print(f"   ✅ Conformes: {summary.get('compliant', 0)}")
        print(f"   ⚠️  Partiellement conformes: {summary.get('partially_compliant', 0)}")
        print(f"   ❌ Non-conformes: {summary.get('non_compliant', 0)}")
        print(f"   🚨 Erreurs critiques: {summary.get('critical_errors', 0)}")
        
        # Afficher problèmes critiques
        critical_issues = audit_results.get('critical_issues', [])
        if critical_issues:
            print(f"\n🚨 PROBLÈMES CRITIQUES DÉTECTÉS:")
            for issue in critical_issues[:5]:  # Afficher max 5 problèmes
                print(f"   • {issue}")
            if len(critical_issues) > 5:
                print(f"   ... et {len(critical_issues) - 5} autres problèmes")
        
        # Afficher recommandations
        recommendations = audit_results.get('recommendations', [])
        if recommendations:
            print(f"\n💡 RECOMMANDATIONS:")
            for rec in recommendations:
                print(f"   • {rec}")
        
    except Exception as e:
        print(f"⚠️ Erreur lors de l'audit Pattern Factory: {e}")
    
    # Test original - Détection faux agents
    print("\n" + "=" * 80)
    print("🎯 DÉTECTION FAUX AGENTS (Tests originaux)")
    print("=" * 80)
    
    try:
        # Exécuter détection faux agents
        results = testeur.run_fake_agent_detection()
        
        print(f"\n📊 Résultats détection faux agents:")
        print(f"   🎯 Agents testés: {results.get('agents_tested', 0)}")
        print(f"   🚨 Faux agents détectés: {results.get('fake_agents_detected', 0)}")
        print(f"   ✅ Agents conformes: {results.get('valid_agents', 0)}")
        
        # Afficher quelques détails des faux agents
        fake_agents = results.get('fake_agents', [])
        if fake_agents:
            print(f"\n🚨 FAUX AGENTS DÉTECTÉS:")
            for fake_agent in fake_agents[:3]:  # Afficher max 3
                print(f"   • {fake_agent.get('agent_name', 'N/A')}: {fake_agent.get('recommendation', 'N/A')}")
        
    except Exception as e:
        print(f"⚠️ Erreur lors de la détection faux agents: {e}")
    
    print("\n" + "=" * 80)
    print("✅ TESTS TERMINÉS - Agent 04 amélioré opérationnel")
    print("📋 Rapports détaillés sauvegardés dans ./reports/")
    print("=" * 80)

if __name__ == "__main__":
    main() 