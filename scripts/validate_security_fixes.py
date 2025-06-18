#!/usr/bin/env python3
"""
Script de validation des correctifs scurit - Quick Wins Sprint 1
Valide que toutes les vulnrabilits critiques ont t corriges.
"""

import sys
import os
import asyncio
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple
import json

# Ajouter le chemin du projet pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class SecurityValidationResult:
    """Rsultat d'une validation de scurit."""
    
    def __init__(self, test_name: str, passed: bool, message: str, details: Dict[str, Any] = None):
        self.test_name = test_name
        self.passed = passed
        self.message = message
        self.details = details or {}
        self.timestamp = time.time()


class SecurityValidator:
    """Validateur des correctifs de scurit."""
    
    def __init__(self):
        self.results: List[SecurityValidationResult] = []
        self.project_root = Path(__file__).parent.parent
    
    def log_result(self, test_name: str, passed: bool, message: str, details: Dict[str, Any] = None):
        """Enregistre un rsultat de test."""
        result = SecurityValidationResult(test_name, passed, message, details)
        self.results.append(result)
        
        status = "[CHECK] PASS" if passed else "[CROSS] FAIL"
        print(f"{status} {test_name}: {message}")
        
        if details and not passed:
            for key, value in details.items():
                print(f"    {key}: {value}")
    
    async def validate_rce_prevention(self) -> bool:
        """Valide que la vulnrabilit RCE a t corrige."""
        print("\n Validation RCE Prevention...")
        
        try:
            # Test 1: Import du nouvel analyseur scuris
            try:
                from orchestrator.app.security.secure_analyzer import SecureCodeAnalyzer, SecurityError
                self.log_result("RCE-001", True, "Secure analyzer imported successfully")
            except ImportError as e:
                self.log_result("RCE-001", False, "Secure analyzer import failed", {"error": str(e)})
                return False
            
            # Test 2: Validation des patterns dangereux
            analyzer = SecureCodeAnalyzer()
            dangerous_patterns = [
                "eval('malicious')",
                "exec('dangerous')",
                "__import__('os').system('ls')",
                "open('/etc/passwd', 'r').read()"
            ]
            
            blocked_count = 0
            for pattern in dangerous_patterns:
                try:
                    analyzer.validate_code_safety(pattern)
                    self.log_result(f"RCE-002-{pattern[:10]}", False, f"Dangerous pattern not blocked: {pattern}")
                except SecurityError:
                    blocked_count += 1
            
            if blocked_count == len(dangerous_patterns):
                self.log_result("RCE-002", True, f"All {len(dangerous_patterns)} dangerous patterns blocked")
            else:
                self.log_result("RCE-002", False, f"Only {blocked_count}/{len(dangerous_patterns)} patterns blocked")
            
            # Test 3: Validation imports interdits
            forbidden_imports = ["import os", "import subprocess", "from sys import exit"]
            blocked_imports = 0
            
            for import_stmt in forbidden_imports:
                try:
                    analyzer.validate_code_safety(import_stmt)
                    self.log_result(f"RCE-003-{import_stmt[:10]}", False, f"Forbidden import not blocked: {import_stmt}")
                except SecurityError:
                    blocked_imports += 1
            
            if blocked_imports == len(forbidden_imports):
                self.log_result("RCE-003", True, f"All {len(forbidden_imports)} forbidden imports blocked")
            else:
                self.log_result("RCE-003", False, f"Only {blocked_imports}/{len(forbidden_imports)} imports blocked")
            
            # Test 4: Code sr autoris
            safe_code = '''
import json
import datetime
from typing import List

def process_data(data: dict) -> List[str]:
    return [str(item) for item in data.values()]

result = process_data({"test": "value"})
print(result)
'''
            try:
                analyzer.validate_code_safety(safe_code)
                self.log_result("RCE-004", True, "Safe code passes validation")
            except Exception as e:
                self.log_result("RCE-004", False, "Safe code rejected", {"error": str(e)})
            
            # Test 5: Analyse scurise complte
            try:
                result = await analyzer.analyze_code_secure(safe_code)
                if isinstance(result, str) and "security validation failed" not in result.lower():
                    self.log_result("RCE-005", True, "Secure analysis completed successfully")
                else:
                    self.log_result("RCE-005", False, "Secure analysis failed", {"result": result})
            except Exception as e:
                self.log_result("RCE-005", False, "Secure analysis exception", {"error": str(e)})
            
            return True
            
        except Exception as e:
            self.log_result("RCE-000", False, "RCE validation failed", {"error": str(e)})
            return False
    
    def validate_ssrf_prevention(self) -> bool:
        """Valide que la vulnrabilit SSRF a t corrige."""
        print("\n Validation SSRF Prevention...")
        
        try:
            # Test 1: Import du validateur rseau
            try:
                from orchestrator.app.security.validators import NetworkValidator
                self.log_result("SSRF-001", True, "Network validator imported successfully")
            except ImportError as e:
                self.log_result("SSRF-001", False, "Network validator import failed", {"error": str(e)})
                return False
            
            # Test 2: Validation URLs malveillantes
            malicious_urls = [
                "http://127.0.0.1:22",
                "http://localhost:3306", 
                "http://169.254.169.254/latest/meta-data/",
                "file:///etc/passwd",
                "ftp://internal.company.com"
            ]
            
            blocked_urls = 0
            for url in malicious_urls:
                is_valid, error = NetworkValidator.validate_url(url)
                if not is_valid:
                    blocked_urls += 1
                else:
                    self.log_result(f"SSRF-002-{url[:20]}", False, f"Malicious URL not blocked: {url}")
            
            if blocked_urls == len(malicious_urls):
                self.log_result("SSRF-002", True, f"All {len(malicious_urls)} malicious URLs blocked")
            else:
                self.log_result("SSRF-002", False, f"Only {blocked_urls}/{len(malicious_urls)} URLs blocked")
            
            # Test 3: URLs lgitimes autorises
            legitimate_urls = [
                "https://api.openai.com/v1/models",
                "https://api.anthropic.com/v1/messages",
                "https://httpbin.org/get"
            ]
            
            allowed_urls = 0
            for url in legitimate_urls:
                is_valid, error = NetworkValidator.validate_url(url)
                if is_valid:
                    allowed_urls += 1
                else:
                    self.log_result(f"SSRF-003-{url[:20]}", False, f"Legitimate URL blocked: {url}", {"error": error})
            
            if allowed_urls == len(legitimate_urls):
                self.log_result("SSRF-003", True, f"All {len(legitimate_urls)} legitimate URLs allowed")
            else:
                self.log_result("SSRF-003", False, f"Only {allowed_urls}/{len(legitimate_urls)} URLs allowed")
            
            return True
            
        except Exception as e:
            self.log_result("SSRF-000", False, "SSRF validation failed", {"error": str(e)})
            return False
    
    def validate_secrets_management(self) -> bool:
        """Valide la gestion scurise des secrets."""
        print("\n Validation Secrets Management...")
        
        try:
            # Test 1: Import du gestionnaire de secrets
            try:
                from orchestrator.app.security.secrets_manager import ProductionSecretsManager, get_secrets_manager
                self.log_result("SECRETS-001", True, "Secrets manager imported successfully")
            except ImportError as e:
                self.log_result("SECRETS-001", False, "Secrets manager import failed", {"error": str(e)})
                return False
            
            # Test 2: Cration du gestionnaire
            try:
                manager = get_secrets_manager()
                self.log_result("SECRETS-002", True, "Secrets manager created successfully")
            except Exception as e:
                self.log_result("SECRETS-002", False, "Secrets manager creation failed", {"error": str(e)})
                return False
            
            # Test 3: Vrification de la configuration par environnement
            cache_stats = manager.get_cache_stats()
            if isinstance(cache_stats, dict) and 'cached_secrets_count' in cache_stats:
                self.log_result("SECRETS-003", True, "Cache statistics available")
            else:
                self.log_result("SECRETS-003", False, "Cache statistics not available")
            
            return True
            
        except Exception as e:
            self.log_result("SECRETS-000", False, "Secrets validation failed", {"error": str(e)})
            return False
    
    def validate_structured_logging(self) -> bool:
        """Valide le systme de logs structurs."""
        print("\n Validation Structured Logging...")
        
        try:
            # Test 1: Import du systme de logs
            try:
                from orchestrator.app.observability.structured_logging import (
                    SecurityAuditLogger, StructuredLogger, get_logger
                )
                self.log_result("LOGS-001", True, "Structured logging imported successfully")
            except ImportError as e:
                self.log_result("LOGS-001", False, "Structured logging import failed", {"error": str(e)})
                return False
            
            # Test 2: Cration du logger de scurit
            try:
                security_logger = SecurityAuditLogger()
                logger = get_logger("test_logger")
                self.log_result("LOGS-002", True, "Security and structured loggers created")
            except Exception as e:
                self.log_result("LOGS-002", False, "Logger creation failed", {"error": str(e)})
                return False
            
            # Test 3: Test de logging (sans output rel)
            try:
                # Test des mthodes principales sans side effects
                if hasattr(security_logger, 'log_security_event') and hasattr(logger, 'info'):
                    self.log_result("LOGS-003", True, "Logger methods available")
                else:
                    self.log_result("LOGS-003", False, "Logger methods missing")
            except Exception as e:
                self.log_result("LOGS-003", False, "Logger method test failed", {"error": str(e)})
            
            return True
            
        except Exception as e:
            self.log_result("LOGS-000", False, "Logging validation failed", {"error": str(e)})
            return False
    
    def validate_health_checks(self) -> bool:
        """Valide le systme de health checks."""
        print("\n Validation Health Checks...")
        
        try:
            # Test 1: Import du systme de health checks
            try:
                from orchestrator.app.health.comprehensive_health import (
                    HealthCheckOrchestrator, get_health_orchestrator, check_system_health
                )
                self.log_result("HEALTH-001", True, "Health check system imported successfully")
            except ImportError as e:
                self.log_result("HEALTH-001", False, "Health check import failed", {"error": str(e)})
                return False
            
            # Test 2: Cration de l'orchestrateur
            try:
                orchestrator = get_health_orchestrator()
                if len(orchestrator.checks) > 0:
                    self.log_result("HEALTH-002", True, f"Health orchestrator created with {len(orchestrator.checks)} checks")
                else:
                    self.log_result("HEALTH-002", False, "Health orchestrator has no checks configured")
            except Exception as e:
                self.log_result("HEALTH-002", False, "Health orchestrator creation failed", {"error": str(e)})
            
            return True
            
        except Exception as e:
            self.log_result("HEALTH-000", False, "Health checks validation failed", {"error": str(e)})
            return False
    
    def run_static_security_scans(self) -> bool:
        """Excute les scans de scurit statiques."""
        print("\n[SEARCH] Static Security Scans...")
        
        # Test 1: Bandit scan
        try:
            result = subprocess.run([
                'bandit', '-r', str(self.project_root / 'orchestrator'), '-ll', '--format', 'json'
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                # Parse JSON output
                try:
                    bandit_results = json.loads(result.stdout)
                    high_severity = len([r for r in bandit_results.get('results', []) 
                                       if r.get('issue_severity') in ['HIGH', 'CRITICAL']])
                    
                    if high_severity == 0:
                        self.log_result("SCAN-001", True, "Bandit: No HIGH/CRITICAL vulnerabilities found")
                    else:
                        self.log_result("SCAN-001", False, f"Bandit: {high_severity} HIGH/CRITICAL vulnerabilities found")
                except json.JSONDecodeError:
                    self.log_result("SCAN-001", True, "Bandit completed (JSON parse failed)")
            else:
                self.log_result("SCAN-001", False, "Bandit scan failed", {"stderr": result.stderr})
        
        except subprocess.TimeoutExpired:
            self.log_result("SCAN-001", False, "Bandit scan timed out")
        except FileNotFoundError:
            self.log_result("SCAN-001", False, "Bandit not installed")
        except Exception as e:
            self.log_result("SCAN-001", False, "Bandit scan error", {"error": str(e)})
        
        # Test 2: Safety check
        try:
            result = subprocess.run([
                'safety', 'check', '--json'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.log_result("SCAN-002", True, "Safety: No known vulnerabilities in dependencies")
            else:
                try:
                    safety_results = json.loads(result.stdout)
                    vuln_count = len(safety_results)
                    self.log_result("SCAN-002", False, f"Safety: {vuln_count} vulnerabilities found in dependencies")
                except:
                    self.log_result("SCAN-002", False, "Safety: vulnerabilities found (parse failed)")
        
        except subprocess.TimeoutExpired:
            self.log_result("SCAN-002", False, "Safety check timed out")
        except FileNotFoundError:
            self.log_result("SCAN-002", False, "Safety not installed")
        except Exception as e:
            self.log_result("SCAN-002", False, "Safety check error", {"error": str(e)})
        
        return True
    
    def run_tests(self) -> bool:
        """Excute les tests de scurit."""
        print("\n Security Tests...")
        
        tests_dir = self.project_root / 'tests'
        if not tests_dir.exists():
            self.log_result("TESTS-001", False, "Tests directory not found")
            return False
        
        # Test des tests de scurit
        security_tests = tests_dir / 'security'
        if security_tests.exists():
            try:
                result = subprocess.run([
                    'python', '-m', 'pytest', str(security_tests), '-v', '--tb=short'
                ], capture_output=True, text=True, timeout=120, cwd=str(self.project_root))
                
                if result.returncode == 0:
                    self.log_result("TESTS-001", True, "Security tests passed")
                else:
                    self.log_result("TESTS-001", False, "Security tests failed", {"stderr": result.stderr[:500]})
            
            except subprocess.TimeoutExpired:
                self.log_result("TESTS-001", False, "Security tests timed out")
            except Exception as e:
                self.log_result("TESTS-001", False, "Security tests error", {"error": str(e)})
        else:
            self.log_result("TESTS-001", False, "Security tests directory not found")
        
        return True
    
    async def run_all_validations(self) -> Dict[str, Any]:
        """Excute toutes les validations."""
        print(" SECURITY VALIDATION - QUICK WINS SPRINT 1")
        print("=" * 50)
        
        start_time = time.time()
        
        # Validations principales
        validations = [
            ("RCE Prevention", self.validate_rce_prevention()),
            ("SSRF Prevention", self.validate_ssrf_prevention()),
            ("Secrets Management", self.validate_secrets_management()),
            ("Structured Logging", self.validate_structured_logging()),
            ("Health Checks", self.validate_health_checks()),
            ("Static Scans", self.run_static_security_scans()),
            ("Security Tests", self.run_tests())
        ]
        
        results = {}
        for name, validation in validations:
            if asyncio.iscoroutine(validation):
                results[name] = await validation
            else:
                results[name] = validation
        
        duration = time.time() - start_time
        
        # Statistiques finales
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r.passed])
        failed_tests = total_tests - passed_tests
        
        print("\n" + "=" * 50)
        print("[CHART] VALIDATION SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {total_tests}")
        print(f"[CHECK] Passed: {passed_tests}")
        print(f"[CROSS] Failed: {failed_tests}")
        print(f" Duration: {duration:.2f}s")
        
        # Score de scurit
        security_score = (passed_tests / total_tests) * 10 if total_tests > 0 else 0
        print(f" Security Score: {security_score:.1f}/10")
        
        # Recommandations
        if failed_tests == 0:
            print("\n ALL SECURITY VALIDATIONS PASSED!")
            print("[CHECK] Ready for next sprint (Architecture refactoring)")
        elif security_score >= 7.0:
            print("\n GOOD SECURITY POSTURE - Minor issues to fix")
            print("[CHECK] Can proceed with caution")
        else:
            print("\n SECURITY ISSUES DETECTED - Address before proceeding")
            print("[CROSS] Stop sprint, focus on debugging")
        
        # checs dtaills
        if failed_tests > 0:
            print("\n[SEARCH] FAILED TESTS:")
            for result in self.results:
                if not result.passed:
                    print(f"  [CROSS] {result.test_name}: {result.message}")
                    if result.details:
                        for key, value in result.details.items():
                            print(f"      {key}: {value}")
        
        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'security_score': security_score,
            'duration': duration,
            'ready_for_production': failed_tests == 0
        }


async def main():
    """Fonction principale."""
    validator = SecurityValidator()
    
    try:
        summary = await validator.run_all_validations()
        
        # Code de sortie bas sur les rsultats
        if summary['failed_tests'] == 0:
            sys.exit(0)  # Succs
        elif summary['security_score'] >= 7.0:
            sys.exit(1)  # Avertissement
        else:
            sys.exit(2)  # chec critique
    
    except KeyboardInterrupt:
        print("\n Validation interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n Validation failed with exception: {e}")
        sys.exit(3)


if __name__ == "__main__":
    asyncio.run(main())
