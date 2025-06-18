#!/usr/bin/env python3
"""
Système d'Agents Parallèles pour Validation du Plan de Travail
Orchestrateur NextGeneration - Validation des Prochaines Étapes
"""

import asyncio
import json
import subprocess
import time
import os
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

@dataclass
class RapportAgent:
    """Structure standardisée pour les rapports d'agents."""
    agent_nom: str
    mission: str
    statut: str  # SUCCESS, FAILURE, WARNING
    temps_execution: float
    resultats: Dict[str, Any]
    problemes: List[str]
    recommandations: List[str]
    prochaines_actions: List[str]
    timestamp: str

class AgentTesteur:
    """Agent spécialisé dans les tests de validation."""
    
    def __init__(self):
        self.nom = "Agent Testeur"
        self.mission = "Exécuter test_gemini_key_validation_windows.py et analyser les résultats"
    
    async def executer_mission(self) -> RapportAgent:
        """Exécute la mission de test et génère un rapport."""
        print(f"🤖 {self.nom} : Démarrage de la mission...")
        debut = time.time()
        
        resultats = {}
        problemes = []
        recommandations = []
        prochaines_actions = []
        
        try:
            # Exécution du test de validation Gemini (version Windows)
            print(f"   📋 Exécution de test_gemini_key_validation_windows.py...")
            result = subprocess.run(
                ["python", "test_gemini_key_validation_windows.py"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            resultats["exit_code"] = result.returncode
            resultats["stdout"] = result.stdout
            resultats["stderr"] = result.stderr
            
            # Analyse des résultats
            if result.returncode == 0:
                statut = "SUCCESS"
                if "✅ Au moins une clé Gemini fonctionne!" in result.stdout:
                    resultats["gemini_fonctionnel"] = True
                    if "38 modèles Gemini disponibles" in result.stdout:
                        resultats["modeles_disponibles"] = 38
                        recommandations.append("Excellent ! 38 modèles Gemini détectés")
                    prochaines_actions.append("Procéder à l'intégration dans l'orchestrateur")
                else:
                    problemes.append("Clé Gemini non fonctionnelle")
                    prochaines_actions.append("Vérifier la configuration de GEMINI_API_KEY")
            else:
                statut = "FAILURE"
                problemes.append(f"Test échoué avec code {result.returncode}")
                if result.stderr:
                    problemes.append(f"Erreur: {result.stderr}")
                prochaines_actions.append("Corriger les erreurs de configuration")
            
            # Vérification de la présence des fichiers
            if os.path.exists("test_gemini_key_validation_windows.py"):
                resultats["script_present"] = True
            else:
                problemes.append("Script test_gemini_key_validation_windows.py manquant")
                statut = "FAILURE"
        
        except subprocess.TimeoutExpired:
            statut = "FAILURE"
            problemes.append("Timeout lors de l'exécution du test")
            prochaines_actions.append("Vérifier la connectivité réseau")
        
        except Exception as e:
            statut = "FAILURE"
            problemes.append(f"Erreur inattendue: {str(e)}")
            prochaines_actions.append("Déboguer l'environnement d'exécution")
        
        temps_execution = time.time() - debut
        
        return RapportAgent(
            agent_nom=self.nom,
            mission=self.mission,
            statut=statut,
            temps_execution=temps_execution,
            resultats=resultats,
            problemes=problemes,
            recommandations=recommandations,
            prochaines_actions=prochaines_actions,
            timestamp=datetime.now().isoformat()
        )

class AgentDocumentaliste:
    """Agent spécialisé dans l'analyse de documentation."""
    
    def __init__(self):
        self.nom = "Agent Documentaliste"
        self.mission = "Analyser GUIDE_FOURNISSEURS_MODELES_ORCHESTRATEUR.md et vérifier sa complétude"
    
    async def executer_mission(self) -> RapportAgent:
        """Analyse la documentation et génère un rapport."""
        print(f"🤖 {self.nom} : Démarrage de la mission...")
        debut = time.time()
        
        resultats = {}
        problemes = []
        recommandations = []
        prochaines_actions = []
        
        try:
            fichier_guide = "GUIDE_FOURNISSEURS_MODELES_ORCHESTRATEUR.md"
            
            if not os.path.exists(fichier_guide):
                statut = "FAILURE"
                problemes.append(f"Fichier {fichier_guide} introuvable")
                prochaines_actions.append("Créer la documentation manquante")
            else:
                # Lecture et analyse du contenu
                with open(fichier_guide, 'r', encoding='utf-8') as f:
                    contenu = f.read()
                
                resultats["taille_fichier"] = len(contenu)
                resultats["nombre_lignes"] = len(contenu.split('\n'))
                
                # Vérification des sections essentielles
                sections_requises = [
                    "OpenAI",
                    "Anthropic",
                    "Google Gemini",
                    "Ollama",
                    "Configuration",
                    "Variables d'environnement",
                    "Scripts de test"
                ]
                
                sections_trouvees = []
                sections_manquantes = []
                
                for section in sections_requises:
                    if section.lower() in contenu.lower():
                        sections_trouvees.append(section)
                    else:
                        sections_manquantes.append(section)
                
                resultats["sections_trouvees"] = sections_trouvees
                resultats["sections_manquantes"] = sections_manquantes
                resultats["completude"] = len(sections_trouvees) / len(sections_requises) * 100
                
                # Vérification des fournisseurs documentés
                fournisseurs = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY", "GEMINI_API_KEY", "OLLAMA"]
                fournisseurs_documentes = []
                
                for fournisseur in fournisseurs:
                    if fournisseur in contenu:
                        fournisseurs_documentes.append(fournisseur)
                
                resultats["fournisseurs_documentes"] = fournisseurs_documentes
                resultats["nombre_fournisseurs"] = len(fournisseurs_documentes)
                
                # Évaluation du statut
                if resultats["completude"] >= 90:
                    statut = "SUCCESS"
                    recommandations.append("Documentation excellente et complète")
                    prochaines_actions.append("Documentation prête pour utilisation")
                elif resultats["completude"] >= 70:
                    statut = "WARNING"
                    problemes.append(f"Documentation incomplète ({resultats['completude']:.1f}%)")
                    prochaines_actions.append("Compléter les sections manquantes")
                else:
                    statut = "FAILURE"
                    problemes.append("Documentation insuffisante")
                    prochaines_actions.append("Réécrire la documentation")
                
                if sections_manquantes:
                    problemes.append(f"Sections manquantes: {', '.join(sections_manquantes)}")
                
                # Recommandations spécifiques
                if "GEMINI_API_KEY" in fournisseurs_documentes:
                    recommandations.append("Support Gemini correctement documenté")
                else:
                    problemes.append("Documentation Gemini incomplète")
        
        except Exception as e:
            statut = "FAILURE"
            problemes.append(f"Erreur lors de l'analyse: {str(e)}")
            prochaines_actions.append("Vérifier l'accès au fichier")
        
        temps_execution = time.time() - debut
        
        return RapportAgent(
            agent_nom=self.nom,
            mission=self.mission,
            statut=statut,
            temps_execution=temps_execution,
            resultats=resultats,
            problemes=problemes,
            recommandations=recommandations,
            prochaines_actions=prochaines_actions,
            timestamp=datetime.now().isoformat()
        )

class AgentExperimentateur:
    """Agent spécialisé dans les expérimentations."""
    
    def __init__(self):
        self.nom = "Agent Expérimentateur"
        self.mission = "Lancer test_gemini_rapide_windows.py et évaluer les performances"
    
    async def executer_mission(self) -> RapportAgent:
        """Exécute les expérimentations et génère un rapport."""
        print(f"🤖 {self.nom} : Démarrage de la mission...")
        debut = time.time()
        
        resultats = {}
        problemes = []
        recommandations = []
        prochaines_actions = []
        
        try:
            # Vérification de l'existence du script
            if not os.path.exists("test_gemini_rapide_windows.py"):
                statut = "FAILURE"
                problemes.append("Script test_gemini_rapide_windows.py manquant")
                prochaines_actions.append("Créer le script de test rapide")
            else:
                # Exécution du test rapide
                print(f"   📋 Exécution de test_gemini_rapide_windows.py...")
                result = subprocess.run(
                    ["python", "test_gemini_rapide_windows.py"],
                    capture_output=True,
                    text=True,
                    timeout=45
                )
                
                resultats["exit_code"] = result.returncode
                resultats["stdout"] = result.stdout
                resultats["stderr"] = result.stderr
                
                # Analyse des performances
                if result.returncode == 0:
                    # Recherche de métriques de performance
                    if "Test réussi" in result.stdout or "✅" in result.stdout:
                        statut = "SUCCESS"
                        resultats["tests_reussis"] = True
                        
                        # Extraction des temps de réponse si disponibles
                        if "0.6s" in result.stdout or "rapide" in result.stdout.lower():
                            resultats["performance_excellente"] = True
                            recommandations.append("Performances Gemini excellentes détectées")
                        
                        # Comptage des tests réussis
                        nb_succes = result.stdout.count("✅")
                        if nb_succes > 0:
                            resultats["nombre_tests_reussis"] = nb_succes
                            recommandations.append(f"{nb_succes} tests réussis")
                        
                        prochaines_actions.append("Gemini prêt pour usage production")
                    else:
                        statut = "WARNING"
                        problemes.append("Tests partiellement réussis")
                        prochaines_actions.append("Analyser les échecs de tests")
                else:
                    statut = "FAILURE"
                    problemes.append(f"Tests échoués avec code {result.returncode}")
                    if "API key" in result.stderr:
                        problemes.append("Problème de clé API")
                        prochaines_actions.append("Vérifier la configuration API")
                    else:
                        prochaines_actions.append("Déboguer les erreurs de test")
                
                # Analyse des modèles testés
                if "gemini" in result.stdout.lower():
                    modeles_testes = result.stdout.lower().count("gemini")
                    resultats["modeles_testes"] = modeles_testes
                    if modeles_testes > 0:
                        recommandations.append(f"{modeles_testes} modèles Gemini testés")
        
        except subprocess.TimeoutExpired:
            statut = "FAILURE"
            problemes.append("Timeout lors des tests de performance")
            prochaines_actions.append("Optimiser les timeouts de test")
        
        except Exception as e:
            statut = "FAILURE"
            problemes.append(f"Erreur lors de l'expérimentation: {str(e)}")
            prochaines_actions.append("Vérifier l'environnement de test")
        
        temps_execution = time.time() - debut
        
        return RapportAgent(
            agent_nom=self.nom,
            mission=self.mission,
            statut=statut,
            temps_execution=temps_execution,
            resultats=resultats,
            problemes=problemes,
            recommandations=recommandations,
            prochaines_actions=prochaines_actions,
            timestamp=datetime.now().isoformat()
        )

class AgentIntegrateur:
    """Agent spécialisé dans l'intégration technique."""
    
    def __init__(self):
        self.nom = "Agent Intégrateur"
        self.mission = "Concevoir et implémenter l'agent Gemini dans l'orchestrateur"
    
    async def executer_mission(self) -> RapportAgent:
        """Conçoit l'intégration Gemini et génère un rapport."""
        print(f"🤖 {self.nom} : Démarrage de la mission...")
        debut = time.time()
        
        resultats = {}
        problemes = []
        recommandations = []
        prochaines_actions = []
        
        try:
            # Analyse de l'architecture existante
            fichiers_orchestrateur = [
                "orchestrator/app/agents/workers.py",
                "orchestrator/app/config.py",
                "orchestrator/app/agents/supervisor.py"
            ]
            
            fichiers_presents = []
            fichiers_manquants = []
            
            for fichier in fichiers_orchestrateur:
                if os.path.exists(fichier):
                    fichiers_presents.append(fichier)
                else:
                    fichiers_manquants.append(fichier)
            
            resultats["fichiers_presents"] = fichiers_presents
            resultats["fichiers_manquants"] = fichiers_manquants
            
            if len(fichiers_presents) >= 2:
                # Analyse du fichier workers.py
                if "orchestrator/app/agents/workers.py" in fichiers_presents:
                    with open("orchestrator/app/agents/workers.py", 'r', encoding='utf-8') as f:
                        contenu_workers = f.read()
                    
                    # Vérification de la structure existante
                    agents_existants = []
                    if "code_generation" in contenu_workers:
                        agents_existants.append("code_generation")
                    if "documentation" in contenu_workers:
                        agents_existants.append("documentation")
                    if "testing" in contenu_workers:
                        agents_existants.append("testing")
                    if "diag_postgresql" in contenu_workers:
                        agents_existants.append("diag_postgresql")
                    
                    resultats["agents_existants"] = agents_existants
                    resultats["nombre_agents"] = len(agents_existants)
                    
                    # Vérification si Gemini est déjà intégré
                    if "gemini" in contenu_workers.lower():
                        resultats["gemini_deja_integre"] = True
                        statut = "SUCCESS"
                        recommandations.append("Gemini déjà partiellement intégré")
                        prochaines_actions.append("Vérifier et optimiser l'intégration existante")
                    else:
                        resultats["gemini_deja_integre"] = False
                        
                        # Conception de l'intégration
                        integration_plan = {
                            "nouveau_agent": "gemini_rapid",
                            "modele_recommande": "gemini-1.5-flash",
                            "cas_usage": ["prototypage", "analyse_rapide", "economie_couts"],
                            "modification_requise": "workers.py",
                            "dependance": "langchain-google-genai"
                        }
                        
                        resultats["plan_integration"] = integration_plan
                        statut = "SUCCESS"
                        recommandations.append("Plan d'intégration Gemini conçu")
                        prochaines_actions.append("Implémenter l'agent gemini_rapid")
                        prochaines_actions.append("Installer langchain-google-genai")
                        prochaines_actions.append("Tester l'intégration")
                
                # Vérification de la configuration
                if "orchestrator/app/config.py" in fichiers_presents:
                    with open("orchestrator/app/config.py", 'r', encoding='utf-8') as f:
                        contenu_config = f.read()
                    
                    if "GOOGLE_API_KEY" in contenu_config:
                        resultats["config_gemini_presente"] = True
                        recommandations.append("Configuration Gemini déjà présente")
                    else:
                        resultats["config_gemini_presente"] = False
                        problemes.append("Configuration Gemini manquante dans config.py")
                        prochaines_actions.append("Ajouter GOOGLE_API_KEY dans config.py")
                
                if "statut" not in locals():
                    statut = "WARNING"
            else:
                statut = "FAILURE"
                problemes.append("Fichiers orchestrateur manquants")
                prochaines_actions.append("Vérifier l'installation de l'orchestrateur")
        
        except Exception as e:
            statut = "FAILURE"
            problemes.append(f"Erreur lors de l'analyse d'intégration: {str(e)}")
            prochaines_actions.append("Vérifier l'accès aux fichiers")
        
        temps_execution = time.time() - debut
        
        return RapportAgent(
            agent_nom=self.nom,
            mission=self.mission,
            statut=statut,
            temps_execution=temps_execution,
            resultats=resultats,
            problemes=problemes,
            recommandations=recommandations,
            prochaines_actions=prochaines_actions,
            timestamp=datetime.now().isoformat()
        )

class CoordinateurAgents:
    """Coordinateur principal pour orchestrer les agents."""
    
    def __init__(self):
        self.agents = [
            AgentTesteur(),
            AgentDocumentaliste(),
            AgentExperimentateur(),
            AgentIntegrateur()
        ]
    
    async def executer_plan_travail(self) -> Dict[str, Any]:
        """Exécute le plan de travail avec tous les agents en parallèle."""
        print("🚀 VALIDATION DU PLAN DE TRAVAIL - AGENTS PARALLÈLES")
        print("=" * 60)
        print(f"📅 Démarrage: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🤖 Nombre d'agents: {len(self.agents)}")
        print()
        
        # Exécution parallèle des agents
        debut_global = time.time()
        
        taches = [agent.executer_mission() for agent in self.agents]
        rapports = await asyncio.gather(*taches)
        
        temps_total = time.time() - debut_global
        
        # Génération du rapport consolidé
        rapport_consolide = self.generer_rapport_consolide(rapports, temps_total)
        
        return rapport_consolide
    
    def generer_rapport_consolide(self, rapports: List[RapportAgent], temps_total: float) -> Dict[str, Any]:
        """Génère un rapport consolidé à partir des rapports individuels."""
        
        # Statistiques globales
        statuts = [r.statut for r in rapports]
        nb_success = statuts.count("SUCCESS")
        nb_warning = statuts.count("WARNING")
        nb_failure = statuts.count("FAILURE")
        
        statut_global = "SUCCESS" if nb_success == len(rapports) else \
                       "WARNING" if nb_failure == 0 else "FAILURE"
        
        # Consolidation des problèmes et recommandations
        tous_problemes = []
        toutes_recommandations = []
        toutes_actions = []
        
        for rapport in rapports:
            tous_problemes.extend(rapport.problemes)
            toutes_recommandations.extend(rapport.recommandations)
            toutes_actions.extend(rapport.prochaines_actions)
        
        # Analyse des résultats par tâche
        resultats_par_tache = {}
        for rapport in rapports:
            resultats_par_tache[rapport.agent_nom] = {
                "statut": rapport.statut,
                "temps": rapport.temps_execution,
                "resultats_cles": rapport.resultats,
                "problemes": rapport.problemes,
                "recommandations": rapport.recommandations
            }
        
        rapport_final = {
            "timestamp": datetime.now().isoformat(),
            "statut_global": statut_global,
            "temps_execution_total": temps_total,
            "statistiques": {
                "agents_total": len(rapports),
                "succes": nb_success,
                "avertissements": nb_warning,
                "echecs": nb_failure,
                "taux_reussite": (nb_success / len(rapports)) * 100
            },
            "resultats_par_tache": resultats_par_tache,
            "synthese": {
                "problemes_identifies": list(set(tous_problemes)),
                "recommandations_globales": list(set(toutes_recommandations)),
                "prochaines_actions_prioritaires": list(set(toutes_actions))
            },
            "rapports_detailles": [asdict(r) for r in rapports]
        }
        
        return rapport_final
    
    def afficher_rapport_utilisateur(self, rapport: Dict[str, Any]) -> None:
        """Affiche le rapport final pour l'utilisateur."""
        print("\n" + "=" * 60)
        print("📊 RAPPORT CONSOLIDÉ - VALIDATION PLAN DE TRAVAIL")
        print("=" * 60)
        
        # Statut global
        statut_emoji = {"SUCCESS": "✅", "WARNING": "⚠️", "FAILURE": "❌"}
        print(f"\n🎯 STATUT GLOBAL: {statut_emoji[rapport['statut_global']]} {rapport['statut_global']}")
        
        # Statistiques
        stats = rapport['statistiques']
        print(f"\n📈 STATISTIQUES:")
        print(f"   🤖 Agents exécutés: {stats['agents_total']}")
        print(f"   ✅ Succès: {stats['succes']}")
        print(f"   ⚠️ Avertissements: {stats['avertissements']}")
        print(f"   ❌ Échecs: {stats['echecs']}")
        print(f"   📊 Taux de réussite: {stats['taux_reussite']:.1f}%")
        print(f"   ⏱️ Temps total: {rapport['temps_execution_total']:.2f}s")
        
        # Résultats par tâche
        print(f"\n📋 RÉSULTATS PAR TÂCHE:")
        for nom_agent, resultats in rapport['resultats_par_tache'].items():
            emoji = statut_emoji[resultats['statut']]
            print(f"   {emoji} {nom_agent}: {resultats['statut']} ({resultats['temps']:.2f}s)")
            
            # Résultats clés
            if resultats['resultats_cles']:
                for cle, valeur in list(resultats['resultats_cles'].items())[:2]:  # Limiter l'affichage
                    print(f"      📌 {cle}: {valeur}")
        
        # Synthèse
        synthese = rapport['synthese']
        
        if synthese['problemes_identifies']:
            print(f"\n🚨 PROBLÈMES IDENTIFIÉS:")
            for probleme in synthese['problemes_identifies'][:5]:  # Top 5
                print(f"   ❗ {probleme}")
        
        if synthese['recommandations_globales']:
            print(f"\n💡 RECOMMANDATIONS GLOBALES:")
            for recommandation in synthese['recommandations_globales'][:5]:  # Top 5
                print(f"   💡 {recommandation}")
        
        if synthese['prochaines_actions_prioritaires']:
            print(f"\n🔧 PROCHAINES ACTIONS PRIORITAIRES:")
            for action in synthese['prochaines_actions_prioritaires'][:5]:  # Top 5
                print(f"   🎯 {action}")
        
        # Conclusion
        print(f"\n🎉 CONCLUSION:")
        if rapport['statut_global'] == "SUCCESS":
            print("   ✅ Plan de travail validé avec succès!")
            print("   🚀 Prêt pour la mise en production")
        elif rapport['statut_global'] == "WARNING":
            print("   ⚠️ Plan de travail partiellement validé")
            print("   🔧 Corrections mineures requises")
        else:
            print("   ❌ Plan de travail nécessite des corrections")
            print("   🛠️ Actions correctives requises")
        
        print("\n" + "=" * 60)

async def main():
    """Fonction principale d'exécution."""
    coordinateur = CoordinateurAgents()
    
    # Exécution du plan de travail
    rapport = await coordinateur.executer_plan_travail()
    
    # Affichage du rapport utilisateur
    coordinateur.afficher_rapport_utilisateur(rapport)
    
    # Sauvegarde du rapport détaillé
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fichier_rapport = f"rapport_validation_plan_travail_{timestamp}.json"
    
    with open(fichier_rapport, 'w', encoding='utf-8') as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Rapport détaillé sauvegardé: {fichier_rapport}")
    
    return rapport['statut_global'] == "SUCCESS"

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1) 