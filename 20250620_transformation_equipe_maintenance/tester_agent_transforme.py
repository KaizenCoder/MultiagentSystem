#!/usr/bin/env python3
"""
🧪 TEST AGENT TRANSFORMÉ - VALIDATION COMPLÈTE
Utilise l'Agent 04 Testeur Anti-Faux-Agents pour valider la transformation
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime
import sys
from pathlib import Path
from core import logging_manager
import json

# Configuration
AGENT_TRANSFORME = "agent_11_auditeur_qualite.py"
AGENTS_DIR = Path("C:/Dev/nextgeneration/agent_factory_implementation/agents")
REPORTS_DIR = Path("C:/Dev/nextgeneration/agent_factory_implementation/agents/reviews")

class TesteurAgentTransforme:
    def __init__(self):
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'logs/test_agent_transforme_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        # LoggingManager NextGeneration - Agent
        import sys
from pathlib import Path
from core import logging_manager
        self.logger = LoggingManager().get_agent_logger(
            agent_name="TesteurAgentTransforme",
            role="ai_processor",
            domain="testing",
            async_enabled=True
        )

    async def lancer_test_complet(self):
        """Lance un test complet de l'agent transformé"""
        print("🧪 TEST AGENT TRANSFORMÉ - VALIDATION COMPLÈTE")
        print("=" * 60)
        print(f"📁 Agent à tester: {AGENT_TRANSFORME}")
        print(f"🎯 Répertoire: {AGENTS_DIR}")
        print("🔬 VALIDATION AVEC AGENT 04 TESTEUR")
        print("=" * 60)
        
        try:
            # 1. Vérifications préliminaires
            print("\n🔍 PHASE 1: VÉRIFICATIONS PRÉLIMINAIRES")
            agent_path = AGENTS_DIR / AGENT_TRANSFORME
            
            if not agent_path.exists():
                raise Exception(f"❌ Agent transformé non trouvé: {agent_path}")
            
            print(f"✅ Agent transformé trouvé: {agent_path}")
            print(f"📏 Taille: {agent_path.stat().st_size:,} caractères")
            
            # 2. Initialiser Agent 04 Testeur
            print("\n🚀 PHASE 2: INITIALISATION AGENT 04 TESTEUR")
            agent04 = await self.initialiser_agent04_testeur()
            
            # 3. Test syntaxe Python
            print("\n🐍 PHASE 3: TEST SYNTAXE PYTHON")
            test_syntaxe = await self.tester_syntaxe_python(agent_path)
            
            # 4. Test conformité Pattern Factory
            print("\n🏭 PHASE 4: TEST CONFORMITÉ PATTERN FACTORY")
            test_conformite = await self.tester_conformite_pattern_factory(agent04, agent_path)
            
            # 5. Test fonctionnalité de base
            print("\n⚙️ PHASE 5: TEST FONCTIONNALITÉ DE BASE")
            test_fonctionnalite = await self.tester_fonctionnalite_base(agent_path)
            
            # 6. Génération rapport final
            print("\n📊 PHASE 6: GÉNÉRATION RAPPORT TEST FINAL")
            rapport_test = await self.generer_rapport_test_final({
                "syntaxe": test_syntaxe,
                "conformite": test_conformite,
                "fonctionnalite": test_fonctionnalite
            })
            
            # 7. Arrêt propre
            await agent04.shutdown()
            
            return rapport_test
            
        except Exception as e:
            self.logger.error(f"❌ Erreur test: {e}")
            print(f"\n💥 ERREUR FATALE TEST: {e}")
            return False

    async def initialiser_agent04_testeur(self):
        """Initialise l'Agent 04 Testeur Anti-Faux-Agents"""
        try:
            sys.path.append("agent_equipe_maintenance")
            from agent_MAINTENANCE_04_testeur_anti_faux_agents import ImprovedEnterpriseAgentTester
            
            agent04 = ImprovedEnterpriseAgentTester()
            await agent04.startup()
            
            print(f"✅ Agent 04 Testeur initialisé: {agent04.agent_id}")
            print(f"🔬 Capacités de test: {len(agent04.get_capabilities())}")
            
            return agent04
            
        except Exception as e:
            raise Exception(f"Erreur initialisation Agent 04: {e}")

    async def tester_syntaxe_python(self, agent_path):
        """Test de syntaxe Python de base"""
        try:
            print("🐍 Test syntaxe Python...")
            
            with open(agent_path, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Test compilation Python
            try:
                compile(contenu, str(agent_path), 'exec')
                syntaxe_valide = True
                erreur_syntaxe = None
                print("✅ Syntaxe Python valide")
            except SyntaxError as e:
                syntaxe_valide = False
                erreur_syntaxe = str(e)
                print(f"❌ Erreur syntaxe: {e}")
            
            # Test imports
            imports_detectes = []
            lignes = contenu.splitlines()
            for ligne in lignes:
                if ligne.strip().startswith(('import ', 'from ')):
                    imports_detectes.append(ligne.strip())
            
            print(f"📦 Imports détectés: {len(imports_detectes)}")
            
            # Vérifier import Pattern Factory
            pattern_factory_import = any('core.agent_factory_architecture' in imp or 'Agent' in imp for imp in imports_detectes)
            print(f"🏭 Import Pattern Factory: {'✅' if pattern_factory_import else '❌'}")
            
            return {
                "syntaxe_valide": syntaxe_valide,
                "erreur_syntaxe": erreur_syntaxe,
                "imports_detectes": len(imports_detectes),
                "pattern_factory_import": pattern_factory_import,
                "taille_fichier": len(contenu),
                "nombre_lignes": len(lignes)
            }
            
        except Exception as e:
            print(f"❌ Erreur test syntaxe: {e}")
            return {"erreur": str(e)}

    async def tester_conformite_pattern_factory(self, agent04, agent_path):
        """Test conformité Pattern Factory avec Agent 04"""
        try:
            print("🏭 Test conformité Pattern Factory...")
            
            # Utiliser l'Agent 04 pour vérifier la conformité
            conformite_result = await agent04.verify_pattern_factory_compliance(str(agent_path))
            
            print(f"📊 Score conformité: {conformite_result.get('conformity_score', 0):.1f}%")
            print(f"📋 Statut: {conformite_result.get('conformity_status', 'unknown')}")
            
            problemes = conformite_result.get('critical_issues', [])
            if problemes:
                print(f"🚨 Problèmes restants: {len(problemes)}")
                for i, probleme in enumerate(problemes[:3], 1):
                    print(f"   {i}. {probleme}")
                if len(problemes) > 3:
                    print(f"   ... et {len(problemes) - 3} autres")
            else:
                print("✅ Aucun problème critique détecté")
            
            return conformite_result
            
        except Exception as e:
            print(f"❌ Erreur test conformité: {e}")
            return {"erreur": str(e)}

    async def tester_fonctionnalite_base(self, agent_path):
        """Test de fonctionnalité de base"""
        try:
            print("⚙️ Test fonctionnalité de base...")
            
            with open(agent_path, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Vérifier présence méthodes essentielles
            methodes_essentielles = {
                'startup': 'async def startup(' in contenu,
                'shutdown': 'async def shutdown(' in contenu,
                'health_check': 'async def health_check(' in contenu,
                'execute_task': 'async def execute_task(' in contenu,
                'get_capabilities': 'def get_capabilities(' in contenu
            }
            
            methodes_presentes = sum(methodes_essentielles.values())
            total_methodes = len(methodes_essentielles)
            
            print(f"🔧 Méthodes essentielles: {methodes_presentes}/{total_methodes}")
            for methode, presente in methodes_essentielles.items():
                status = "✅" if presente else "❌"
                print(f"   {status} {methode}")
            
            # Vérifier structure classe
            has_class = 'class ' in contenu
            has_agent_inheritance = 'class ' in contenu and '(Agent)' in contenu
            
            print(f"🏗️ Structure classe: {'✅' if has_class else '❌'}")
            print(f"🧬 Héritage Agent: {'✅' if has_agent_inheritance else '❌'}")
            
            return {
                "methodes_essentielles": methodes_essentielles,
                "score_methodes": (methodes_presentes / total_methodes) * 100,
                "has_class": has_class,
                "has_agent_inheritance": has_agent_inheritance,
                "fonctionnalite_score": ((methodes_presentes / total_methodes) + has_class + has_agent_inheritance) / 3 * 100
            }
            
        except Exception as e:
            print(f"❌ Erreur test fonctionnalité: {e}")
            return {"erreur": str(e)}

    async def generer_rapport_test_final(self, resultats_tests):
        """Génère le rapport final des tests"""
        try:
            # Calculer score global
            scores = []
            
            if "syntaxe" in resultats_tests and "erreur" not in resultats_tests["syntaxe"]:
                score_syntaxe = 100 if resultats_tests["syntaxe"]["syntaxe_valide"] else 0
                scores.append(score_syntaxe)
            
            if "conformite" in resultats_tests and "erreur" not in resultats_tests["conformite"]:
                score_conformite = resultats_tests["conformite"].get("conformity_score", 0)
                scores.append(score_conformite)
            
            if "fonctionnalite" in resultats_tests and "erreur" not in resultats_tests["fonctionnalite"]:
                score_fonctionnalite = resultats_tests["fonctionnalite"].get("fonctionnalite_score", 0)
                scores.append(score_fonctionnalite)
            
            score_global = sum(scores) / len(scores) if scores else 0
            
            # Déterminer verdict final
            if score_global >= 90:
                verdict = "EXCELLENT"
                couleur = "🟢"
            elif score_global >= 70:
                verdict = "BON"
                couleur = "🟡"
            elif score_global >= 50:
                verdict = "MOYEN"
                couleur = "🟠"
            else:
                verdict = "ÉCHEC"
                couleur = "🔴"
            
            rapport = {
                "mission_id": f"test_agent_transforme_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "agent_teste": AGENT_TRANSFORME,
                "timestamp": datetime.now().isoformat(),
                "resultats_tests": resultats_tests,
                "score_global": score_global,
                "verdict_final": verdict,
                "couleur_verdict": couleur,
                "recommandations": []
            }
            
            # Générer recommandations
            if score_global >= 90:
                rapport["recommandations"].append("🎉 TRANSFORMATION PARFAITEMENT RÉUSSIE !")
                rapport["recommandations"].append("✅ Agent prêt pour production")
            elif score_global >= 70:
                rapport["recommandations"].append("✅ Transformation réussie avec quelques améliorations possibles")
                rapport["recommandations"].append("🔧 Corrections mineures recommandées")
            elif score_global >= 50:
                rapport["recommandations"].append("⚠️ Transformation partiellement réussie")
                rapport["recommandations"].append("🔧 Corrections importantes nécessaires")
            else:
                rapport["recommandations"].append("❌ TRANSFORMATION ÉCHOUÉE")
                rapport["recommandations"].append("🔄 Rollback recommandé")
            
            # Sauvegarder rapport
            rapport_file = REPORTS_DIR / f"test_agent_transforme_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(rapport_file, 'w', encoding='utf-8') as f:
                json.dump(rapport, f, indent=2, ensure_ascii=False)
            
            print(f"📊 Rapport test sauvé: {rapport_file.name}")
            
            # Afficher résumé final
            self.afficher_verdict_final(rapport)
            
            return rapport
            
        except Exception as e:
            print(f"❌ Erreur génération rapport: {e}")
            return {"erreur": str(e)}

    def afficher_verdict_final(self, rapport):
        """Affiche le verdict final des tests"""
        print("\n" + "="*70)
        print("🧪 VERDICT FINAL DES TESTS")
        print("="*70)
        print(f"📁 Agent testé: {rapport['agent_teste']}")
        print(f"📊 Score global: {rapport['score_global']:.1f}%")
        print(f"{rapport['couleur_verdict']} Verdict: {rapport['verdict_final']}")
        
        print("\n📋 Recommandations:")
        for rec in rapport.get('recommandations', []):
            print(f"   {rec}")
        
        print("\n📊 Détail des scores:")
        resultats = rapport.get('resultats_tests', {})
        
        if 'syntaxe' in resultats and 'erreur' not in resultats['syntaxe']:
            syntaxe_ok = resultats['syntaxe']['syntaxe_valide']
            print(f"   🐍 Syntaxe Python: {'✅ 100%' if syntaxe_ok else '❌ 0%'}")
        
        if 'conformite' in resultats and 'erreur' not in resultats['conformite']:
            score_conf = resultats['conformite'].get('conformity_score', 0)
            print(f"   🏭 Conformité PF: {score_conf:.1f}%")
        
        if 'fonctionnalite' in resultats and 'erreur' not in resultats['fonctionnalite']:
            score_fonc = resultats['fonctionnalite'].get('fonctionnalite_score', 0)
            print(f"   ⚙️ Fonctionnalité: {score_fonc:.1f}%")

async def main():
    """Point d'entrée principal"""
    try:
        testeur = TesteurAgentTransforme()
        resultat = await testeur.lancer_test_complet()
        
        return 0 if resultat else 1
        
    except Exception as e:
        print(f"💥 Erreur fatale test: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main())) 



