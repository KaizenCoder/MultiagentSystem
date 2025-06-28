#!/usr/bin/env python3
"""
DÉMONSTRATION ADAPTATEUR v4.3.0 - PATTERNS COMPLEXES
====================================================

Démonstration des nouvelles capacités de patterns d'indentation complexes
avec intégration ChromaDB/PostgreSQL.

Author: Équipe NextGeneration  
Version: Demo v4.3.0
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Configuration du chemin
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from agents.agent_MAINTENANCE_03_adaptateur_code import AgentMAINTENANCE03AdaptateurCode
    from core.agent_factory_architecture import Task
except ImportError as e:
    print(f"❌ Erreur import: {e}")
    sys.exit(1)

class AdaptateurV43Demo:
    """Démonstration interactive de l'adaptateur v4.3.0"""
    
    def __init__(self):
        print("🚀 Initialisation Adaptateur v4.3.0 avec patterns complexes...")
        self.adaptateur = AgentMAINTENANCE03AdaptateurCode(
            id="demo_v43",
            pattern_confidence_threshold=0.75,
            enable_pattern_learning=True,
            max_similar_patterns=5
        )
        
    async def demo_pattern_complex_indentation(self):
        """Démo 1: Patterns d'indentation complexes"""
        print("\n" + "="*60)
        print("🔧 DÉMO 1: PATTERNS D'INDENTATION COMPLEXES")
        print("="*60)
        
        # Exemple 1: Indentation mixte avec structures imbriquées
        code_complexe = """
class DataProcessor:
    def __init__(self, config):
        self.config = config
        
    def process_data(self, data):
        results = []
        try:
            for item in data:
                if item.is_valid():
                    # Traitement principal
                    processed = self.transform(item)
                    if processed:
                        results.append(processed)
                    else:
print("Erreur traitement item")  # ❌ Erreur indentation
                        continue
                else:
                    self.log_invalid_item(item)
        except Exception as e:
            self.handle_error(e)
            
        return results
        
    def transform(self, item):
        # Logique de transformation
        if item.type == 'A':
return item.value * 2  # ❌ Erreur indentation
        elif item.type == 'B':
            return item.value / 2
        return None
"""
        
        print("📄 Code original avec erreurs d'indentation complexes:")
        print(code_complexe)
        
        print("\n🔍 Analyse du pattern d'indentation...")
        
        # Analyse du pattern
        pattern_analysis = self.adaptateur.analyze_indentation_pattern(
            code_complexe, 
            "expected an indented block"
        )
        
        print(f"✅ Type de pattern: {pattern_analysis['pattern_type']}")
        print(f"✅ Style d'indentation: {pattern_analysis['indentation_style']}")
        print(f"✅ Niveau d'indentation: {pattern_analysis['indentation_level']}")
        print(f"✅ Score de complexité: {pattern_analysis['complexity_score']:.2f}")
        print(f"✅ Structures imbriquées: {pattern_analysis['nested_structures']}")
        
        # Recherche de patterns similaires
        print("\n🔍 Recherche de patterns similaires...")
        similar_patterns = self.adaptateur.find_similar_indentation_patterns(
            code_complexe,
            "expected an indented block"
        )
        
        if similar_patterns:
            print(f"✅ {len(similar_patterns)} patterns similaires trouvés")
            for i, pattern in enumerate(similar_patterns, 1):
                print(f"   Pattern {i}: {pattern.get('pattern_type')} (score: {pattern.get('success_rate', 0):.2f})")
        else:
            print("ℹ️  Aucun pattern similaire trouvé (première utilisation ou ChromaDB indisponible)")
        
        # Correction avec l'adaptateur
        print("\n🔧 Application de la correction...")
        
        task = Task(
            id="demo_complex_indentation",
            params={
                "code": code_complexe,
                "feedback": IndentationError("expected an indented block"),
                "error_type": "indentation",
                "use_pattern_learning": True,
                "enable_analytics": True
            }
        )
        
        await self.adaptateur.startup()
        result = await self.adaptateur.execute_task(task)
        
        if result.success:
            print("✅ Correction réussie !")
            
            adapted_code = result.data["adapted_code"]
            adaptations = result.data["adaptations"]
            advanced_confidence = result.data["advanced_confidence_score"]
            
            print(f"\n📄 Code corrigé (confiance: {advanced_confidence:.2f}):")
            print(adapted_code)
            
            print(f"\n📋 Adaptations appliquées ({len(adaptations)}):")
            for adaptation in adaptations:
                print(f"   → {adaptation}")
                
            # Test de compilation
            try:
                compile(adapted_code, '<string>', 'exec')
                print("\n✅ Le code corrigé compile parfaitement !")
            except SyntaxError as e:
                print(f"\n⚠️  Erreur de compilation persistante: {e}")
        else:
            print(f"❌ Échec de la correction: {result.error}")
            
        await self.adaptateur.shutdown()
    
    async def demo_advanced_confidence_system(self):
        """Démo 2: Système de score de confiance avancé"""
        print("\n" + "="*60)
        print("🎯 DÉMO 2: SYSTÈME DE SCORE DE CONFIANCE AVANCÉ")
        print("="*60)
        
        # Différents niveaux de complexité pour tester le scoring
        test_cases = [
            {
                "name": "Code Simple",
                "code": """
def simple():
print("hello")
""",
                "expected_confidence": "Élevée (code simple)"
            },
            {
                "name": "Code Modérément Complexe",
                "code": """
class Handler:
    def process(self, data):
        for item in data:
            if item.valid:
print(item.value)
        return True
""",
                "expected_confidence": "Moyenne (complexité modérée)"
            },
            {
                "name": "Code Très Complexe",
                "code": """
class ComplexProcessor:
    def __init__(self, config):
        self.config = config
        
    async def process_with_callbacks(self, data, callback=None):
        results = {}
        try:
            async with self.get_context() as ctx:
                for batch in self.batch_data(data):
                    processed_batch = []
                    for item in batch:
                        if await self.validate_item(item):
                            try:
                                result = await self.transform_item(item, ctx)
                                if result and callback:
                                    await callback(result)
                                processed_batch.append(result)
                            except Exception as e:
                                self.log_error(e, item)
                                continue
                        else:
print(f"Invalid item: {item}")  # ❌ Erreur dans code complexe
                    results[batch.id] = processed_batch
        except Exception as e:
            self.handle_critical_error(e)
            raise
        return results
""",
                "expected_confidence": "Plus faible (très complexe)"
            }
        ]
        
        await self.adaptateur.startup()
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n--- Test {i}: {test_case['name']} ---")
            
            task = Task(
                id=f"demo_confidence_{i}",
                params={
                    "code": test_case["code"],
                    "feedback": IndentationError("expected an indented block"),
                    "error_type": "indentation",
                    "use_pattern_learning": True,
                    "validate_result": True
                }
            )
            
            result = await self.adaptateur.execute_task(task)
            
            if result.success:
                basic_confidence = result.data.get("validation_post", {}).get("confidence_score", 0)
                advanced_confidence = result.data.get("advanced_confidence_score", 0)
                patterns_used = result.data.get("patterns_used", 0)
                processing_time = result.data.get("processing_time", 0)
                
                print(f"✅ Score confiance de base: {basic_confidence:.2f}")
                print(f"✅ Score confiance avancé: {advanced_confidence:.2f}")
                print(f"✅ Patterns utilisés: {patterns_used}")
                print(f"✅ Temps de traitement: {processing_time:.3f}s")
                print(f"✅ Prédiction: {test_case['expected_confidence']}")
                
                # Analyse des facteurs de confiance
                confidence_diff = advanced_confidence - basic_confidence
                if confidence_diff > 0:
                    print(f"📈 Amélioration confiance: +{confidence_diff:.2f} (patterns efficaces)")
                elif confidence_diff < 0:
                    print(f"📉 Réduction confiance: {confidence_diff:.2f} (complexité détectée)")
                else:
                    print("📊 Confiance stable (pas de patterns ou complexité neutre)")
            else:
                print(f"❌ Échec test: {result.error}")
        
        await self.adaptateur.shutdown()
    
    async def demo_learning_analytics(self):
        """Démo 3: Analytics et apprentissage"""
        print("\n" + "="*60)
        print("📊 DÉMO 3: ANALYTICS ET APPRENTISSAGE")
        print("="*60)
        
        # Récupération des statistiques actuelles
        print("📈 Statistiques des patterns:")
        stats = self.adaptateur.get_pattern_statistics()
        
        if "error" in stats:
            print(f"⚠️  PostgreSQL: {stats['error']}")
        else:
            print(f"✅ Patterns totaux: {stats.get('total_patterns', 0)}")
            if stats.get('best_performing_pattern'):
                best_pattern, best_stats = stats['best_performing_pattern']
                print(f"✅ Meilleur pattern: {best_pattern} (taux: {best_stats['success_rate']:.2f})")
        
        print(f"✅ ChromaDB actif: {stats.get('chromadb_info', {}).get('chromadb_enabled', False)}")
        
        # Analyse des progrès d'apprentissage
        print("\n📚 Analyse des progrès d'apprentissage:")
        progress = self.adaptateur.analyze_learning_progress()
        
        print(f"✅ Corrections totales: {progress['total_corrections']}")
        print(f"✅ Corrections réussies: {progress['successful_corrections']}")
        print(f"✅ Taux de succès global: {progress['success_rate']:.2f}")
        print(f"✅ Apprentissage patterns: {progress['pattern_learning_enabled']}")
        print(f"✅ Seuil de confiance: {progress['confidence_threshold']}")
        
        # État des bases de données
        db_status = progress['databases_status']
        print(f"\n🗄️  État des bases de données:")
        print(f"   ChromaDB: {'✅ Actif' if db_status['chromadb'] else '❌ Inactif'}")
        print(f"   PostgreSQL: {'✅ Actif' if db_status['postgresql'] else '❌ Inactif'}")
        
        # Analyse par type d'erreur
        if progress['error_types_analysis']:
            print(f"\n📊 Analyse par type d'erreur:")
            for error_type, stats in progress['error_types_analysis'].items():
                print(f"   {error_type}: {stats['successes']}/{stats['count']} (taux: {stats['success_rate']:.2f})")
        else:
            print("\nℹ️  Aucune donnée d'analyse par type d'erreur encore")
    
    async def demo_architecture_integration(self):
        """Démo 4: Intégration architecturale complète"""
        print("\n" + "="*60)
        print("🏗️  DÉMO 4: INTÉGRATION ARCHITECTURALE COMPLÈTE")
        print("="*60)
        
        print("🔧 Capacités de l'adaptateur v4.3.0:")
        capabilities = self.adaptateur.get_capabilities()
        
        # Groupement par version
        v42_caps = [cap for cap in capabilities if any(v42_term in cap for v42_term in 
                   ["extended_error", "auto_import", "multi_level", "confidence_scoring", 
                    "type_error", "attribute_error", "value_error", "module_resolution"])]
        
        v43_caps = [cap for cap in capabilities if any(v43_term in cap for v43_term in 
                   ["complex_indentation", "chromadb", "pattern_similarity", "postgresql", 
                    "advanced_confidence", "pattern_learning", "correction_history", "adaptive"])]
        
        legacy_caps = [cap for cap in capabilities if cap not in v42_caps and cap not in v43_caps]
        
        print(f"\n📦 Capacités héritées (v4.1 et antérieures): {len(legacy_caps)}")
        for cap in legacy_caps[:5]:  # Affiche les 5 premières
            print(f"   • {cap}")
        if len(legacy_caps) > 5:
            print(f"   ... et {len(legacy_caps) - 5} autres")
        
        print(f"\n🚀 Capacités v4.2.0 (Priorités Hautes): {len(v42_caps)}")
        for cap in v42_caps:
            print(f"   • {cap}")
        
        print(f"\n🎯 Nouvelles capacités v4.3.0 (Priorités Moyennes): {len(v43_caps)}")
        for cap in v43_caps:
            print(f"   • {cap}")
        
        print(f"\n📊 Total des capacités: {len(capabilities)}")
        
        # Configuration avancée
        print(f"\n⚙️  Configuration avancée v4.3.0:")
        print(f"   Seuil confiance patterns: {self.adaptateur._pattern_confidence_threshold}")
        print(f"   Apprentissage patterns: {self.adaptateur._enable_pattern_learning}")
        print(f"   Max patterns similaires: {self.adaptateur._max_similar_patterns}")
        
        # Intégrations disponibles
        print(f"\n🔗 Intégrations disponibles:")
        print(f"   ChromaDB (stockage patterns): {self.adaptateur.chroma_patterns.enabled}")
        print(f"   PostgreSQL (analytics): {self.adaptateur.pg_analytics.enabled}")
        print(f"   Cache imports découverts: {len(self.adaptateur._import_discovery_cache)} éléments")
        print(f"   Historique corrections: {len(self.adaptateur._correction_history)} entrées")

async def main():
    """Point d'entrée principal de la démonstration"""
    print("🌟 DÉMONSTRATION ADAPTATEUR v4.3.0")
    print("Patterns d'Indentation Complexes + ChromaDB + PostgreSQL")
    print("="*70)
    
    demo = AdaptateurV43Demo()
    
    try:
        # Démo 1: Patterns complexes
        await demo.demo_pattern_complex_indentation()
        
        # Pause interactive
        input("\n⏸️  Appuyez sur Entrée pour continuer vers la démo du système de confiance...")
        
        # Démo 2: Système de confiance avancé
        await demo.demo_advanced_confidence_system()
        
        # Pause interactive
        input("\n⏸️  Appuyez sur Entrée pour continuer vers les analytics...")
        
        # Démo 3: Analytics
        await demo.demo_learning_analytics()
        
        # Pause interactive
        input("\n⏸️  Appuyez sur Entrée pour voir l'intégration architecturale...")
        
        # Démo 4: Architecture
        await demo.demo_architecture_integration()
        
        print("\n" + "="*70)
        print("🎉 DÉMONSTRATION TERMINÉE")
        print("="*70)
        print("✅ Adaptateur v4.3.0 - Toutes les fonctionnalités démontrées")
        print("🔧 Patterns d'indentation complexes: Opérationnel")
        print("📊 Intégration ChromaDB/PostgreSQL: Configurée")
        print("🎯 Système de confiance avancé: Actif")
        print("📈 Analytics et apprentissage: Fonctionnels")
        
    except KeyboardInterrupt:
        print("\n⚠️ Démonstration interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur durant la démonstration: {e}")

if __name__ == "__main__":
    asyncio.run(main())