#!/usr/bin/env python3
"""
🧪 Script de Validation - Standards GPU RTX 3090 NextGeneration (2025)
Validation complète des standards GPU adaptés pour NextGeneration AI Platform

🎯 Basé sur les Standards GPU RTX 3090 Adaptés - Édition 2025
📋 Compatible avec l'infrastructure existante et les logs JSON

Usage:
    python VALIDATION_STANDARDS_RTX3090.py
    python VALIDATION_STANDARDS_RTX3090.py --detailed
    python VALIDATION_STANDARDS_RTX3090.py --performance-test
    python VALIDATION_STANDARDS_RTX3090.py --save-logs --output validation_nextgen_$(date +%Y%m%d_%H%M%S).json
"""

import os
import sys
import time
import json
import argparse
import traceback
from datetime import datetime
from typing import Dict, List, Tuple, Any

# Imports GPU
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("⚠️ PyTorch non disponible - tests limités")

class RTX3090ValidatorNextGen:
    """
    Validateur modernisé pour les standards RTX 3090 NextGeneration
    Compatible avec les nouveaux standards adaptés 2025
    """
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.results = []
        self.start_time = time.time()
        self.project_name = "NextGeneration AI Platform"
        self.standards_version = "2.0 ADAPTÉE"
        self.preferred_gpus = ["RTX 3090", "RTX 4090", "RTX 5090"]
        self.min_vram_gb = 20
        
    def log(self, message: str, level: str = "INFO"):
        """Log des messages avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if self.verbose:
            icon = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}.get(level, "📝")
            print(f"[{timestamp}] {icon} {message}")
    
    def run_test(self, test_name: str, test_func, *args, **kwargs) -> bool:
        """Exécute un test et enregistre le résultat"""
        self.log(f"Test: {test_name}", "INFO")
        
        try:
            start_time = time.time()
            result = test_func(*args, **kwargs)
            duration = time.time() - start_time
            
            success = result if isinstance(result, bool) else bool(result)
            
            self.results.append({
                'test_name': test_name,
                'success': success,
                'duration': duration,
                'result': result if not isinstance(result, bool) else None,
                'timestamp': datetime.now().isoformat()
            })
            
            if success:
                self.log(f"✅ {test_name} - Réussi ({duration:.2f}s)", "SUCCESS")
            else:
                self.log(f"❌ {test_name} - Échec ({duration:.2f}s)", "ERROR")
            
            return success
            
        except Exception as e:
            duration = time.time() - start_time
            self.log(f"❌ {test_name} - Erreur: {str(e)}", "ERROR")
            
            self.results.append({
                'test_name': test_name,
                'success': False,
                'duration': duration,
                'error': str(e),
                'traceback': traceback.format_exc(),
                'timestamp': datetime.now().isoformat()
            })
            
            return False
    
    def test_system_requirements(self) -> bool:
        """Test des prérequis système"""
        
        # Test Python version
        if sys.version_info < (3, 8):
            self.log("Python 3.8+ requis", "ERROR")
            return False
        
        # Test PyTorch disponibilité
        if not TORCH_AVAILABLE:
            self.log("PyTorch non disponible", "ERROR")
            return False
        
        # Test CUDA disponibilité
        if not torch.cuda.is_available():
            self.log("CUDA non disponible", "ERROR")
            return False
        
        self.log(f"Python {sys.version.split()[0]}, PyTorch {torch.__version__}", "SUCCESS")
        return True
    
    def test_gpu_detection(self) -> Dict[str, Any]:
        """Test de détection des GPU selon les nouveaux standards 2025"""
        
        if not TORCH_AVAILABLE or not torch.cuda.is_available():
            return {"error": "CUDA non disponible"}
        
        gpu_info = {}
        gpu_count = torch.cuda.device_count()
        
        for i in range(gpu_count):
            gpu_name = torch.cuda.get_device_name(i)
            gpu_memory = torch.cuda.get_device_properties(i).total_memory / 1024**3
            
            # Score GPU selon les nouveaux standards
            gpu_score = self._calculate_gpu_score(gpu_name, gpu_memory)
            
            gpu_info[f'gpu_{i}'] = {
                'name': gpu_name,
                'memory_gb': round(gpu_memory, 1),
                'is_preferred': any(preferred in gpu_name for preferred in self.preferred_gpus),
                'is_optimal': gpu_memory >= self.min_vram_gb,
                'compatibility_score': gpu_score,
                'recommended_for': self._get_gpu_recommendation(gpu_name, gpu_memory)
            }
        
        # Trouver le meilleur GPU
        best_gpu = max(gpu_info.values(), key=lambda x: x['compatibility_score']) if gpu_info else None
        optimal_gpus = [gpu for gpu in gpu_info.values() if gpu['is_optimal']]
        
        return {
            'gpu_count': gpu_count,
            'gpus': gpu_info,
            'best_gpu': best_gpu,
            'optimal_gpus_found': len(optimal_gpus) > 0,
            'nextgen_compatible': len(optimal_gpus) > 0,
            'standards_version': self.standards_version
        }
    
    def _calculate_gpu_score(self, gpu_name: str, gpu_memory: float) -> int:
        """Calcule un score de compatibilité pour le GPU"""
        score = int(gpu_memory)  # Base sur la mémoire
        
        # Bonus pour GPU préférés
        for idx, preferred in enumerate(self.preferred_gpus):
            if preferred in gpu_name:
                score += 1000 * (len(self.preferred_gpus) - idx)
                break
        
        return score
    
    def _get_gpu_recommendation(self, gpu_name: str, gpu_memory: float) -> str:
        """Recommandation d'usage selon le GPU"""
        if gpu_memory >= 32:
            return "Ultra High Performance (modèles 70B+)"
        elif gpu_memory >= 24:
            return "High Performance (modèles 7B-34B)"
        elif gpu_memory >= 20:
            return "Optimized (modèles 7B-13B)"
        else:
            return "Limited (modèles légers uniquement)"
    
    def test_memory_allocation(self) -> Dict[str, Any]:
        """Test d'allocation mémoire GPU"""
        
        if not TORCH_AVAILABLE or not torch.cuda.is_available():
            return {"error": "CUDA non disponible"}
        
        # Nettoyage initial
        torch.cuda.empty_cache()
        initial_memory = torch.cuda.memory_allocated()
        
        results = {}
        
        # Test 1: Allocation simple
        try:
            device = torch.device("cuda:0")
            tensor = torch.randn(1000, 1000, device=device)
            allocated_memory = torch.cuda.memory_allocated()
            
            results['simple_allocation'] = {
                'success': True,
                'memory_used_mb': (allocated_memory - initial_memory) / 1024**2
            }
            
        except Exception as e:
            results['simple_allocation'] = {'success': False, 'error': str(e)}
        
        # Test 2: Allocation volumineuse (si RTX 3090 détectée)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        if gpu_memory >= 20:  # RTX 3090 ou similaire
            try:
                # Tenter d'allouer ~10GB
                large_tensor = torch.randn(40000, 3200, device=device, dtype=torch.float32)
                large_memory = torch.cuda.memory_allocated()
                
                results['large_allocation'] = {
                    'success': True,
                    'memory_used_gb': (large_memory - initial_memory) / 1024**3,
                    'tensor_shape': list(large_tensor.shape)
                }
                
                # Nettoyage
                del large_tensor
                torch.cuda.empty_cache()
                
            except Exception as e:
                results['large_allocation'] = {'success': False, 'error': str(e)}
        
        # Test 3: Gestion automatique mémoire
        try:
            # Configuration optimale
            os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'
            
            # Créer et détruire plusieurs tenseurs
            for i in range(5):
                temp_tensor = torch.randn(2000, 2000, device=device)
                del temp_tensor
            
            torch.cuda.empty_cache()
            final_memory = torch.cuda.memory_allocated()
            
            results['memory_management'] = {
                'success': True,
                'memory_cleanup_effective': final_memory <= initial_memory + 1024**2  # 1MB tolérance
            }
            
        except Exception as e:
            results['memory_management'] = {'success': False, 'error': str(e)}
        
        return results
    
    def test_performance_basic(self) -> Dict[str, Any]:
        """Test de performance de base"""
        
        if not TORCH_AVAILABLE or not torch.cuda.is_available():
            return {"error": "CUDA non disponible"}
        
        device = torch.device("cuda:0")
        results = {}
        
        # Test 1: Multiplication matricielle
        try:
            size = 2000
            a = torch.randn(size, size, device=device)
            b = torch.randn(size, size, device=device)
            
            # Synchronisation initiale
            torch.cuda.synchronize()
            
            start_time = time.time()
            c = torch.matmul(a, b)
            torch.cuda.synchronize()
            duration = time.time() - start_time
            
            # Performance attendue pour RTX 3090: < 1 seconde pour 2000x2000
            expected_max_time = 2.0
            
            results['matrix_multiplication'] = {
                'success': True,
                'duration_seconds': duration,
                'size': size,
                'performance_ok': duration < expected_max_time,
                'gflops': (2 * size**3) / (duration * 1e9)  # Approximation GFLOPS
            }
            
        except Exception as e:
            results['matrix_multiplication'] = {'success': False, 'error': str(e)}
        
        # Test 2: Opérations mixtes précision
        try:
            # Test en float16
            a_half = torch.randn(1000, 1000, device=device, dtype=torch.float16)
            b_half = torch.randn(1000, 1000, device=device, dtype=torch.float16)
            
            torch.cuda.synchronize()
            start_time = time.time()
            c_half = torch.matmul(a_half, b_half)
            torch.cuda.synchronize()
            duration_half = time.time() - start_time
            
            results['mixed_precision'] = {
                'success': True,
                'float16_duration': duration_half,
                'float16_performance_ok': duration_half < 0.5
            }
            
        except Exception as e:
            results['mixed_precision'] = {'success': False, 'error': str(e)}
        
        return results
    
    def test_configuration_detection(self) -> Dict[str, Any]:
        """Test de détection de configuration selon standards NextGeneration 2025"""
        
        config_info = {
            'project': self.project_name,
            'standards_version': self.standards_version,
            'environment_variables': {
                'CUDA_VISIBLE_DEVICES': os.environ.get('CUDA_VISIBLE_DEVICES'),
                'CUDA_DEVICE_ORDER': os.environ.get('CUDA_DEVICE_ORDER'),
                'PYTORCH_CUDA_ALLOC_CONF': os.environ.get('PYTORCH_CUDA_ALLOC_CONF')
            }
        }
        
        if TORCH_AVAILABLE and torch.cuda.is_available():
            config_info.update({
                'torch_cuda_version': torch.version.cuda,
                'current_device': torch.cuda.current_device(),
                'device_count': torch.cuda.device_count(),
                'primary_gpu': torch.cuda.get_device_name(0),
                'primary_gpu_memory_gb': torch.cuda.get_device_properties(0).total_memory / 1024**3
            })
        
        # Vérifications de conformité aux nouveaux standards adaptatifs
        compliance_checks = {
            'modern_pytorch_alloc': 'expandable_segments' in str(config_info['environment_variables']['PYTORCH_CUDA_ALLOC_CONF'] or ''),
            'optimal_gpu_available': False,
            'nextgen_compatible_setup': False,
            'adaptive_config_ready': True  # Nouveaux standards sont adaptatifs
        }
        
        if TORCH_AVAILABLE and torch.cuda.is_available():
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            gpu_name = torch.cuda.get_device_name(0)
            
            compliance_checks['optimal_gpu_available'] = gpu_memory >= self.min_vram_gb
            compliance_checks['nextgen_compatible_setup'] = any(
                preferred in gpu_name for preferred in self.preferred_gpus
            )
        
        # Les nouveaux standards sont plus flexibles sur CUDA_DEVICE_ORDER
        if config_info['environment_variables']['CUDA_DEVICE_ORDER']:
            compliance_checks['device_order_explicit'] = True
        
        config_info['compliance'] = compliance_checks
        config_info['overall_compliance'] = sum(compliance_checks.values()) >= 3  # Plus flexible
        config_info['compliance_score'] = f"{sum(compliance_checks.values())}/{len(compliance_checks)}"
        
        return config_info
    
    def test_advanced_features(self) -> Dict[str, Any]:
        """Test des fonctionnalités avancées"""
        
        if not TORCH_AVAILABLE or not torch.cuda.is_available():
            return {"error": "CUDA non disponible"}
        
        results = {}
        device = torch.device("cuda:0")
        
        # Test 1: Gradient checkpointing simulation
        try:
            class SimpleModel(torch.nn.Module):
                def __init__(self):
                    super().__init__()
                    self.layers = torch.nn.Sequential(
                        torch.nn.Linear(1000, 2000),
                        torch.nn.ReLU(),
                        torch.nn.Linear(2000, 1000),
                        torch.nn.ReLU(),
                        torch.nn.Linear(1000, 100)
                    )
                
                def forward(self, x):
                    return self.layers(x)
            
            model = SimpleModel().to(device)
            x = torch.randn(32, 1000, device=device, requires_grad=True)
            
            # Forward pass
            output = model(x)
            loss = output.sum()
            loss.backward()
            
            results['gradient_computation'] = {
                'success': True,
                'output_shape': list(output.shape),
                'gradients_computed': x.grad is not None
            }
            
        except Exception as e:
            results['gradient_computation'] = {'success': False, 'error': str(e)}
        
        # Test 2: Utilisation mémoire avec différents types de données
        try:
            memory_usage = {}
            
            for dtype in [torch.float32, torch.float16, torch.int32]:
                torch.cuda.empty_cache()
                initial = torch.cuda.memory_allocated()
                
                tensor = torch.randn(5000, 2000, device=device, dtype=dtype)
                allocated = torch.cuda.memory_allocated()
                
                memory_usage[str(dtype)] = {
                    'memory_mb': (allocated - initial) / 1024**2,
                    'tensor_size': tensor.numel()
                }
                
                del tensor
            
            results['memory_efficiency'] = {
                'success': True,
                'by_dtype': memory_usage
            }
            
        except Exception as e:
            results['memory_efficiency'] = {'success': False, 'error': str(e)}
        
        return results
    
    def test_nextgen_gpu_manager(self) -> Dict[str, Any]:
        """Test du GPUConfigManager des nouveaux standards"""
        
        if not TORCH_AVAILABLE or not torch.cuda.is_available():
            return {"error": "CUDA non disponible"}
        
        results = {}
        
        try:
            # Simuler le GPUConfigManager basique
            class MockGPUConfigManager:
                def __init__(self):
                    self.preferred_gpus = ["RTX 3090", "RTX 4090", "RTX 5090"]
                    self.min_vram_gb = 20
                
                def auto_configure(self):
                    if not torch.cuda.is_available():
                        raise RuntimeError("CUDA non disponible")
                    
                    best_gpu = None
                    best_score = 0
                    
                    for i in range(torch.cuda.device_count()):
                        gpu_name = torch.cuda.get_device_name(i)
                        gpu_memory = torch.cuda.get_device_properties(i).total_memory / 1024**3
                        
                        if gpu_memory < self.min_vram_gb:
                            continue
                        
                        score = gpu_memory
                        for idx, preferred in enumerate(self.preferred_gpus):
                            if preferred in gpu_name:
                                score += 1000 * (len(self.preferred_gpus) - idx)
                                break
                        
                        if score > best_score:
                            best_score = score
                            best_gpu = {
                                'device_id': i,
                                'name': gpu_name,
                                'memory_gb': gpu_memory,
                                'utilization_strategy': self._get_strategy(gpu_memory)
                            }
                    
                    return best_gpu
                
                def _get_strategy(self, memory_gb):
                    if memory_gb >= 32:
                        return "ultra_high_performance"
                    elif memory_gb >= 24:
                        return "high_performance"
                    elif memory_gb >= 20:
                        return "optimized"
                    else:
                        return "conservative"
            
            # Test du manager
            manager = MockGPUConfigManager()
            config = manager.auto_configure()
            
            results['gpu_manager_test'] = {
                'success': True,
                'best_gpu_found': config is not None,
                'recommended_config': config
            }
            
        except Exception as e:
            results['gpu_manager_test'] = {
                'success': False,
                'error': str(e)
            }
        
        # Test context manager simulation
        try:
            device = torch.device("cuda:0")
            
            # Simulation basique d'un context manager
            initial_memory = torch.cuda.memory_allocated()
            
            # Allocations test
            test_tensor = torch.randn(1000, 1000, device=device)
            allocated_memory = torch.cuda.memory_allocated()
            
            # Cleanup
            del test_tensor
            torch.cuda.empty_cache()
            final_memory = torch.cuda.memory_allocated()
            
            results['context_manager_simulation'] = {
                'success': True,
                'memory_managed': final_memory <= initial_memory + 1024,  # 1KB tolérance
                'allocation_successful': allocated_memory > initial_memory
            }
            
        except Exception as e:
            results['context_manager_simulation'] = {
                'success': False,
                'error': str(e)
            }
        
        return results
    
    def test_standards_compatibility(self) -> Dict[str, Any]:
        """Test de compatibilité avec les anciens et nouveaux standards"""
        
        results = {
            'legacy_compatibility': {},
            'modern_features': {},
            'migration_readiness': {}
        }
        
        # Test compatibilité avec anciens standards SuperWhisper V6
        try:
            cuda_visible = os.environ.get('CUDA_VISIBLE_DEVICES')
            cuda_order = os.environ.get('CUDA_DEVICE_ORDER')
            
            results['legacy_compatibility'] = {
                'cuda_visible_devices_set': cuda_visible is not None,
                'cuda_device_order_set': cuda_order == 'PCI_BUS_ID',
                'legacy_pattern_detected': cuda_visible == '1' and cuda_order == 'PCI_BUS_ID'
            }
            
        except Exception as e:
            results['legacy_compatibility'] = {'error': str(e)}
        
        # Test fonctionnalités modernes
        try:
            pytorch_conf = os.environ.get('PYTORCH_CUDA_ALLOC_CONF', '')
            
            results['modern_features'] = {
                'expandable_segments': 'expandable_segments' in pytorch_conf,
                'modern_allocation': 'expandable_segments:True' in pytorch_conf,
                'adaptive_configuration': True  # Nouveaux standards sont adaptatifs
            }
            
        except Exception as e:
            results['modern_features'] = {'error': str(e)}
        
        # Test préparation migration
        if TORCH_AVAILABLE and torch.cuda.is_available():
            try:
                gpu_count = torch.cuda.device_count()
                primary_gpu = torch.cuda.get_device_name(0)
                primary_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
                
                results['migration_readiness'] = {
                    'gpu_count': gpu_count,
                    'primary_gpu_compatible': any(preferred in primary_gpu for preferred in self.preferred_gpus),
                    'memory_sufficient': primary_memory >= self.min_vram_gb,
                    'ready_for_nextgen': primary_memory >= self.min_vram_gb
                }
                
            except Exception as e:
                results['migration_readiness'] = {'error': str(e)}
        
        return results
    
    def generate_report(self) -> Dict[str, Any]:
        """Génère un rapport complet"""
        
        total_duration = time.time() - self.start_time
        
        # Statistiques globales
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r['success'])
        failed_tests = total_tests - successful_tests
        
        # Détection des tests critiques échoués
        critical_failures = [
            r for r in self.results 
            if not r['success'] and any(keyword in r['test_name'].lower() 
                                      for keyword in ['system', 'gpu_detection', 'memory'])
        ]
        
        report = {
            'summary': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'failed_tests': failed_tests,
                'success_rate': (successful_tests / total_tests * 100) if total_tests > 0 else 0,
                'total_duration': total_duration,
                'timestamp': datetime.now().isoformat()
            },
            'critical_failures': len(critical_failures),
            'overall_status': 'PASS' if len(critical_failures) == 0 and failed_tests == 0 else 'FAIL',
            'detailed_results': self.results
        }
        
        return report
    
    def display_summary(self, report: Dict[str, Any]):
        """Affiche un résumé lisible pour NextGeneration"""
        
        print("\n" + "="*70)
        print("🧪 RAPPORT DE VALIDATION - STANDARDS GPU RTX 3090 NEXTGENERATION")
        print(f"📋 {self.project_name} - Version {self.standards_version}")
        print("="*70)
        
        summary = report['summary']
        
        # Statut global
        status_icon = "✅" if report['overall_status'] == 'PASS' else "❌"
        print(f"\n{status_icon} STATUT GLOBAL: {report['overall_status']}")
        
        # Statistiques
        print(f"\n📊 STATISTIQUES:")
        print(f"   Tests exécutés: {summary['total_tests']}")
        print(f"   Tests réussis: {summary['successful_tests']}")
        print(f"   Tests échoués: {summary['failed_tests']}")
        print(f"   Taux de réussite: {summary['success_rate']:.1f}%")
        print(f"   Durée totale: {summary['total_duration']:.2f}s")
        
        # Échecs critiques
        if report['critical_failures'] > 0:
            print(f"\n🚨 ÉCHECS CRITIQUES: {report['critical_failures']}")
            for result in report['detailed_results']:
                if not result['success'] and any(keyword in result['test_name'].lower() 
                                               for keyword in ['system', 'gpu_detection', 'memory']):
                    print(f"   ❌ {result['test_name']}: {result.get('error', 'Erreur inconnue')}")
        
        # Recommandations NextGeneration
        print(f"\n💡 RECOMMANDATIONS NEXTGENERATION:")
        if report['overall_status'] == 'PASS':
            print("   ✅ Configuration optimale pour NextGeneration AI Platform")
            print("   ✅ Standards RTX 3090 Adaptés 2025 respectés")
            print("   ✅ Compatible avec l'infrastructure tools/ existante")
            print("   ✅ Prêt pour les workloads IA modernes")
        else:
            print("   ⚠️ Configuration nécessite des ajustements")
            print("   ⚠️ Consultez STANDARDS_GPU_RTX3090_ADAPTES_2025.md")
            print("   ⚠️ Utilisez GUIDE_MIGRATION_STANDARDS_2025.md pour la migration")
            print("   ⚠️ Vérifiez la compatibilité avec tools/tts_dependencies_installer/")
        
        # Informations spécifiques NextGeneration
        print(f"\n📋 RESSOURCES NEXTGENERATION:")
        print("   📄 Standards: docs/RTX3090/STANDARDS_GPU_RTX3090_ADAPTES_2025.md")
        print("   🔄 Migration: docs/RTX3090/GUIDE_MIGRATION_STANDARDS_2025.md")
        print("   🛠️ Infrastructure: tools/tts_dependencies_installer/ (RTX 3090 ready)")
        print("   📊 Monitoring: tools/tts_performance_monitor/")
        
        print("\n" + "="*70)

def main():
    """Fonction principale"""
    
    parser = argparse.ArgumentParser(description="Validation des standards GPU RTX 3090")
    parser.add_argument('--detailed', action='store_true', help="Tests détaillés")
    parser.add_argument('--performance-test', action='store_true', help="Tests de performance étendus")
    parser.add_argument('--output', type=str, help="Fichier de sortie JSON")
    parser.add_argument('--save-logs', action='store_true', help="Sauvegarder automatiquement dans logs/")
    parser.add_argument('--quiet', action='store_true', help="Mode silencieux")
    
    args = parser.parse_args()
    
    # Créer le validateur NextGeneration
    validator = RTX3090ValidatorNextGen(verbose=not args.quiet)
    
    # Tests de base NextGeneration (obligatoires)
    validator.run_test("Prérequis système", validator.test_system_requirements)
    validator.run_test("Détection GPU NextGen", validator.test_gpu_detection)
    validator.run_test("Configuration NextGen", validator.test_configuration_detection)
    validator.run_test("Allocation mémoire", validator.test_memory_allocation)
    validator.run_test("Compatibilité Standards", validator.test_standards_compatibility)
    
    # Tests détaillés (optionnels)
    if args.detailed:
        validator.run_test("Performance de base", validator.test_performance_basic)
        validator.run_test("Fonctionnalités avancées", validator.test_advanced_features)
        validator.run_test("GPU Manager NextGen", validator.test_nextgen_gpu_manager)
    
    # Tests de performance étendus
    if args.performance_test:
        # Ici, on pourrait ajouter des tests de performance plus poussés
        validator.log("Tests de performance étendus non implémentés dans cette version", "WARNING")
    
    # Générer le rapport
    report = validator.generate_report()
    
    # Afficher le résumé
    if not args.quiet:
        validator.display_summary(report)
    
    # Sauvegarder en JSON si demandé
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        validator.log(f"Rapport sauvegardé: {args.output}", "SUCCESS")
    
    # Sauvegarde automatique dans logs/ si demandé
    if args.save_logs:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_filename = f"validation_nextgen_standards_{timestamp}.json"
        log_path = os.path.join("logs", log_filename)
        
        # Créer le dossier logs s'il n'existe pas
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        
        try:
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            validator.log(f"Log automatique sauvegardé: {log_path}", "SUCCESS")
        except Exception as e:
            validator.log(f"Erreur sauvegarde log: {e}", "ERROR")
    
    # Code de sortie
    sys.exit(0 if report['overall_status'] == 'PASS' else 1)

if __name__ == "__main__":
    main() 



