#!/usr/bin/env python3
"""
TEST VOLET 2 - MOTEUR DE CORRECTION D'INDENTATION AMÉLIORÉ
==========================================================

Test du cycle M-T-D complet pour les améliorations du Volet 2 :
- Moteur de correction d'indentation robuste
- Stratégies ciblées par type d'erreur
- Classification automatique et routage intelligent

Ce test valide les 3 cas d'erreur d'indentation :
1. "expected an indented block" → insertion 'pass'
2. "unexpected indent" → correction contextuelle
3. "unindent does not match" → normalisation globale

Author: Équipe NextGeneration
Version: Test Volet 2 - Journal Évolution Équipe
"""

import sys
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any

# Configuration du chemin d'import
project_root = Path(__file__).resolve().parents[0]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Imports des agents du cycle M-T-D
from agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import AgentMAINTENANCE00ChefEquipeCoordinateur
from agents.agent_MAINTENANCE_03_adaptateur_code import AgentMAINTENANCE03AdaptateurCode
from agents.agent_MAINTENANCE_04_testeur_anti_faux_agents import AgentMAINTENANCE04TesteurAntiFauxAgents
from agents.agent_MAINTENANCE_05_documenteur_peer_reviewer import AgentMAINTENANCE05DocumenteurPeerReviewer
from core.agent_factory_architecture import Task, Result

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestVolet2IndentationEngine:
    """
    Test du Volet 2 : Moteur de correction d'indentation amélioré
    
    Tests des 3 cas d'erreurs d'indentation avec le cycle M-T-D complet :
    M (Maintenance) : Chef Coordinateur + Adaptateur Code  
    T (Test) : Testeur Anti-Faux Agents
    D (Documentation) : Documenteur Peer-Reviewer
    """
    
    def __init__(self):
        self.coordinateur = AgentMAINTENANCE00ChefEquipeCoordinateur(id="coord_test")
        self.adaptateur = AgentMAINTENANCE03AdaptateurCode(id="adapt_test")
        self.testeur = AgentMAINTENANCE04TesteurAntiFauxAgents(id="test_test")
        self.documenteur = AgentMAINTENANCE05DocumenteurPeerReviewer(id="doc_test")
        
    def get_test_cases(self) -> Dict[str, Dict[str, Any]]:
        """
        Retourne les cas de test pour les 3 types d'erreurs d'indentation
        """
        return {
            "cas_1_expected_indented_block": {
                "description": "Test: expected an indented block",
                "code_defaillant": '''def test_function():
    if True:
    print("Hello")  # Erreur: bloc indenté attendu après if
    return True
''',
                "error_type": "indentation",
                "error_msg": "expected an indented block",
                "attendu": "Insertion de 'pass' avec indentation adaptée"
            },
            
            "cas_2_unexpected_indent": {
                "description": "Test: unexpected indent", 
                "code_defaillant": '''def test_function():
    print("Hello")
        print("World")  # Erreur: indentation inattendue
    return True
''',
                "error_type": "indentation", 
                "error_msg": "unexpected indent",
                "attendu": "Correction de l'indentation excessive"
            },
            
            "cas_3_unindent_does_not_match": {
                "description": "Test: unindent does not match",
                "code_defaillant": '''def test_function():
    if True:
        print("Hello")
      print("World")  # Erreur: désindentation incohérente
    return True
''',
                "error_type": "indentation",
                "error_msg": "unindent does not match",
                "attendu": "Normalisation globale de l'indentation"
            }
        }
    
    async def executer_cycle_mtd(self, cas_test: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute le cycle M-T-D complet pour un cas de test
        """
        logger.info(f"=== DÉBUT CYCLE M-T-D : {cas_test['description']} ===")
        
        # Simulation d'exception d'indentation
        class MockIndentationError(IndentationError):
            def __init__(self, msg, lineno=2):
                self.msg = msg
                self.lineno = lineno
                super().__init__(msg)
        
        fake_error = MockIndentationError(cas_test['error_msg'], 2)
        
        # M - MAINTENANCE : Classification et Adaptation
        logger.info("Phase M (Maintenance) : Classification + Adaptation")
        
        # Classification par le coordinateur
        error_type = self.coordinateur.classify_exception(fake_error)
        logger.info(f"Erreur classifiée comme: {error_type}")
        
        # Adaptation par l'adaptateur
        task_adapt = Task(
            id="adapt_task",
            params={
                "code": cas_test['code_defaillant'],
                "feedback": fake_error,
                "error_type": error_type
            }
        )
        
        result_adapt = await self.adaptateur.execute_task(task_adapt)
        logger.info(f"Résultat adaptation: {result_adapt.success}")
        
        if not result_adapt.success:
            return {
                "success": False,
                "phase": "Adaptation",
                "error": result_adapt.error
            }
        
        code_corrige = result_adapt.data.get("adapted_code", "")
        adaptations = result_adapt.data.get("adaptations", [])
        
        # T - TEST : Validation du code corrigé
        logger.info("Phase T (Test) : Validation du code corrigé")
        
        # Test de syntaxe basique
        try:
            compile(code_corrige, '<string>', 'exec')
            syntax_ok = True
            logger.info("✓ Code corrigé compile sans erreur de syntaxe")
        except SyntaxError as e:
            syntax_ok = False
            logger.warning(f"✗ Erreur de syntaxe persistante: {e}")
        
        # D - DOCUMENTATION : Génération rapport
        logger.info("Phase D (Documentation) : Génération rapport")
        
        task_doc = Task(
            id="doc_task",
            params={
                "code_original": cas_test['code_defaillant'],
                "code_corrige": code_corrige,
                "adaptations": adaptations,
                "test_resultat": syntax_ok,
                "error_type": error_type
            }
        )
        
        result_doc = await self.documenteur.execute_task(task_doc)
        
        logger.info(f"=== FIN CYCLE M-T-D : {cas_test['description']} ===")
        
        return {
            "success": syntax_ok,
            "phase": "Complet",
            "code_original": cas_test['code_defaillant'],
            "code_corrige": code_corrige,
            "adaptations": adaptations,
            "error_type": error_type,
            "syntax_ok": syntax_ok,
            "documentation": result_doc.data if result_doc.success else None
        }
    
    async def executer_tous_les_tests(self) -> Dict[str, Any]:
        """
        Exécute tous les cas de test du Volet 2
        """
        logger.info("🔧 DÉMARRAGE TEST VOLET 2 - MOTEUR INDENTATION AMÉLIORÉ 🔧")
        
        cas_tests = self.get_test_cases()
        resultats = {}
        
        for nom_cas, cas_test in cas_tests.items():
            try:
                resultat = await self.executer_cycle_mtd(cas_test)
                resultats[nom_cas] = resultat
                
                status = "✅ SUCCÈS" if resultat["success"] else "❌ ÉCHEC"
                logger.info(f"{status} - {cas_test['description']}")
                
            except Exception as e:
                logger.error(f"❌ ERREUR - {cas_test['description']}: {e}")
                resultats[nom_cas] = {
                    "success": False,
                    "phase": "Exception",
                    "error": str(e)
                }
        
        # Résumé final
        succes = sum(1 for r in resultats.values() if r["success"])
        total = len(resultats)
        
        logger.info(f"📊 RÉSUMÉ VOLET 2: {succes}/{total} tests réussis")
        
        return {
            "volet": "Volet 2 - Moteur Indentation Amélioré",
            "total_tests": total,
            "tests_reussis": succes,
            "tests_echoues": total - succes,
            "taux_reussite": f"{(succes/total)*100:.1f}%",
            "resultats_detailles": resultats
        }

async def main():
    """
    Point d'entrée principal du test Volet 2
    """
    test_engine = TestVolet2IndentationEngine()
    
    try:
        # Démarrage des agents
        await test_engine.coordinateur.startup()
        await test_engine.adaptateur.startup()
        await test_engine.testeur.startup()
        await test_engine.documenteur.startup()
        
        # Exécution des tests
        resultats = await test_engine.executer_tous_les_tests()
        
        # Affichage résultats
        print("\n" + "="*60)
        print("🎯 RÉSULTATS FINAUX VOLET 2")
        print("="*60)
        print(f"Volet testé: {resultats['volet']}")
        print(f"Tests réussis: {resultats['tests_reussis']}/{resultats['total_tests']}")
        print(f"Taux de réussite: {resultats['taux_reussite']}")
        print("="*60)
        
        # Détails par cas de test
        for nom_cas, resultat in resultats['resultats_detailles'].items():
            status = "✅" if resultat["success"] else "❌"
            print(f"{status} {nom_cas}: {resultat.get('phase', 'N/A')}")
            if resultat.get('adaptations'):
                for adaptation in resultat['adaptations']:
                    print(f"    → {adaptation}")
        
        # Validation finale selon méthodologie du journal
        if resultats['tests_reussis'] == resultats['total_tests']:
            print("\n🎉 VOLET 2 VALIDÉ - Moteur d'indentation amélioré fonctionne correctement!")
            print("📝 Mise à jour du journal: Volet 2 → IMPLÉMENTÉ ET VALIDÉ")
            return True
        else:
            print("\n⚠️  VOLET 2 EN ÉCHEC - Corrections nécessaires")
            print("📝 Mise à jour du journal: Volet 2 → ÉCHEC, corrections requises")
            return False
            
    except Exception as e:
        logger.error(f"Erreur fatale durant les tests: {e}")
        return False
        
    finally:
        # Arrêt des agents
        try:
            await test_engine.coordinateur.shutdown()
            await test_engine.adaptateur.shutdown()
            await test_engine.testeur.shutdown()
            await test_engine.documenteur.shutdown()
        except:
            pass

if __name__ == "__main__":
    import asyncio
    success = asyncio.run(main())
    sys.exit(0 if success else 1)