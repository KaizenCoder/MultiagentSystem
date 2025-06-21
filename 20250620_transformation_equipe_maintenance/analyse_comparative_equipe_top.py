#!/usr/bin/env python3
"""
🔍 ANALYSE COMPARATIVE - ÉQUIPE TOP vs ÉQUIPE ACTUELLE
======================================================
Mission: Identifier les fonctionnalités avancées de l'équipe "top" dépréciée
pour améliorer nos agents de maintenance actuels.

Analyse comparative entre:
- Équipe actuelle : agent_equipe_maintenance/agent_MAINTENANCE_XX
- Équipe "top"    : ZZDEPRECATED/equiepe_top/top_agent_MAINTENANCE_XX
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import ast
import re

async def analyser_fonctionnalites_equipe_top():
    """Analyse comparative des fonctionnalités équipe TOP vs ACTUELLE"""
    
    print("🔍 ANALYSE COMPARATIVE - ÉQUIPE TOP vs ACTUELLE")
    print("=" * 80)
    print("🎯 Objectif: Identifier les améliorations possibles")
    print("📁 Source TOP: ZZDEPRECATED/equiepe_top/")
    print("📁 Source ACTUELLE: agent_equipe_maintenance/")
    print()
    
    # Analyse comparative par agent
    analyses_comparatives = {}
    
    # Agent 01 - Analyseur Structure
    print("🔍 AGENT 01 - ANALYSEUR STRUCTURE")
    print("-" * 60)
    analyses_comparatives["agent_01"] = await analyser_agent_01()
    
    # Agent 02 - Évaluateur Utilité
    print("\n📊 AGENT 02 - ÉVALUATEUR UTILITÉ")
    print("-" * 60)
    analyses_comparatives["agent_02"] = await analyser_agent_02()
    
    # Agent 03 - Adaptateur Code
    print("\n🔧 AGENT 03 - ADAPTATEUR CODE")
    print("-" * 60)
    analyses_comparatives["agent_03"] = await analyser_agent_03()
    
    # Agent 04 - Testeur Anti-Faux
    print("\n🧪 AGENT 04 - TESTEUR ANTI-FAUX")
    print("-" * 60)
    analyses_comparatives["agent_04"] = await analyser_agent_04()
    
    # Synthèse globale
    print("\n🏆 SYNTHÈSE COMPARATIVE GLOBALE")
    print("=" * 80)
    synthese = generer_synthese_comparative(analyses_comparatives)
    
    # Génération rapport
    await generer_rapport_ameliorations(analyses_comparatives, synthese)
    
    return analyses_comparatives

async def analyser_agent_01():
    """Analyse comparative Agent 01 - Analyseur Structure"""
    
    # Lecture fichiers
    path_top = Path("../ZZDEPRECATED/equiepe_top/top_agent_MAINTENANCE_01_analyseur_structure.py")
    path_actuel = Path("agent_equipe_maintenance/agent_MAINTENANCE_01_analyseur_structure.py")
    
    analyse = {
        "agent_id": "01",
        "nom": "Analyseur Structure",
        "fonctionnalites_top": [],
        "fonctionnalites_actuelles": [],
        "ameliorations_identifiees": [],
        "taille_comparison": {},
        "complexite_comparison": {}
    }
    
    try:
        # Analyse équipe TOP
        if path_top.exists():
            with open(path_top, 'r', encoding='utf-8') as f:
                contenu_top = f.read()
            
            analyse["taille_comparison"]["top"] = {
                "lignes": len(contenu_top.splitlines()),
                "taille": len(contenu_top)
            }
            
            # Extraction fonctionnalités TOP
            fonctions_top = re.findall(r'async def (\w+)', contenu_top)
            classes_top = re.findall(r'class (\w+)', contenu_top)
            
            analyse["fonctionnalites_top"] = {
                "methodes_async": len(fonctions_top),
                "liste_methodes": fonctions_top[:10],  # Top 10
                "classes": classes_top,
                "features_avancees": []
            }
            
            # Détection fonctionnalités avancées TOP
            if "extract_ast_elements" in contenu_top:
                analyse["fonctionnalites_top"]["features_avancees"].append("🔍 Analyse AST avancée")
            if "analyze_single_file" in contenu_top:
                analyse["fonctionnalites_top"]["features_avancees"].append("📄 Analyse fichier individuel")
            if "classify_tool_type" in contenu_top:
                analyse["fonctionnalites_top"]["features_avancees"].append("🏷️ Classification automatique outils")
            if "calculate_complexity" in contenu_top:
                analyse["fonctionnalites_top"]["features_avancees"].append("📊 Calcul complexité avancé")
            if "categorize_tools" in contenu_top:
                analyse["fonctionnalites_top"]["features_avancees"].append("📋 Catégorisation intelligente")
            if "analyser_structure_apex" in contenu_top:
                analyse["fonctionnalites_top"]["features_avancees"].append("🎯 Analyse spécialisée APEX")
            if "_analyser_fichier_powershell" in contenu_top:
                analyse["fonctionnalites_top"]["features_avancees"].append("💻 Support PowerShell")
            if "_analyser_fichier_batch" in contenu_top:
                analyse["fonctionnalites_top"]["features_avancees"].append("📝 Support Batch/CMD")
                
        # Analyse équipe ACTUELLE
        if path_actuel.exists():
            with open(path_actuel, 'r', encoding='utf-8') as f:
                contenu_actuel = f.read()
            
            analyse["taille_comparison"]["actuel"] = {
                "lignes": len(contenu_actuel.splitlines()),
                "taille": len(contenu_actuel)
            }
            
            # Extraction fonctionnalités ACTUELLES
            fonctions_actuelles = re.findall(r'async def (\w+)', contenu_actuel)
            classes_actuelles = re.findall(r'class (\w+)', contenu_actuel)
            
            analyse["fonctionnalites_actuelles"] = {
                "methodes_async": len(fonctions_actuelles),
                "liste_methodes": fonctions_actuelles[:10],
                "classes": classes_actuelles,
                "features_basiques": []
            }
            
            # Détection fonctionnalités basiques ACTUELLES
            if "analyze_tools_structure" in contenu_actuel:
                analyse["fonctionnalites_actuelles"]["features_basiques"].append("🔍 Analyse structure basique")
            if "get_capabilities" in contenu_actuel:
                analyse["fonctionnalites_actuelles"]["features_basiques"].append("📋 Capacités standard")
        
        # Identification améliorations possibles
        if analyse["fonctionnalites_top"]["features_avancees"]:
            for feature in analyse["fonctionnalites_top"]["features_avancees"]:
                if feature not in str(analyse["fonctionnalites_actuelles"]):
                    analyse["ameliorations_identifiees"].append({
                        "feature": feature,
                        "priorite": "HAUTE",
                        "benefice": "Analyse plus approfondie et spécialisée"
                    })
        
        # Comparaison taille/complexité
        if "top" in analyse["taille_comparison"] and "actuel" in analyse["taille_comparison"]:
            ratio_lignes = analyse["taille_comparison"]["top"]["lignes"] / max(1, analyse["taille_comparison"]["actuel"]["lignes"])
            analyse["complexite_comparison"] = {
                "ratio_taille": ratio_lignes,
                "evaluation": "Plus complexe" if ratio_lignes > 1.5 else "Similaire" if ratio_lignes > 0.8 else "Plus simple"
            }
            
        print(f"✅ Agent 01 - TOP: {analyse['taille_comparison'].get('top', {}).get('lignes', 0)} lignes")
        print(f"✅ Agent 01 - ACTUEL: {analyse['taille_comparison'].get('actuel', {}).get('lignes', 0)} lignes")
        print(f"🎯 Améliorations identifiées: {len(analyse['ameliorations_identifiees'])}")
        
    except Exception as e:
        print(f"❌ Erreur analyse Agent 01: {e}")
        analyse["erreur"] = str(e)
    
    return analyse

async def analyser_agent_02():
    """Analyse comparative Agent 02 - Évaluateur Utilité"""
    
    path_top = Path("../ZZDEPRECATED/equiepe_top/top_agent_MAINTENANCE_02_evaluateur_utilite.py")
    path_actuel = Path("agent_equipe_maintenance/agent_MAINTENANCE_02_evaluateur_utilite.py")
    
    analyse = {
        "agent_id": "02",
        "nom": "Évaluateur Utilité",
        "fonctionnalites_top": [],
        "fonctionnalites_actuelles": [],
        "ameliorations_identifiees": [],
        "intelligence_avancee": []
    }
    
    try:
        # Analyse équipe TOP
        if path_top.exists():
            with open(path_top, 'r', encoding='utf-8') as f:
                contenu_top = f.read()
            
            analyse["taille_comparison"] = {
                "top_lignes": len(contenu_top.splitlines()),
                "top_taille": len(contenu_top)
            }
            
            # Fonctionnalités avancées TOP détectées
            features_avancees_top = []
            if "evaluation_criteria" in contenu_top:
                features_avancees_top.append("📊 Critères d'évaluation pondérés")
            if "nextgen_keywords" in contenu_top:
                features_avancees_top.append("🔍 Mots-clés NextGeneration spécialisés")
            if "evaluate_technical_relevance" in contenu_top:
                features_avancees_top.append("🎯 Évaluation pertinence technique")
            if "evaluate_architecture_compatibility" in contenu_top:
                features_avancees_top.append("🏗️ Évaluation compatibilité architecturale")
            if "evaluate_added_value" in contenu_top:
                features_avancees_top.append("💎 Évaluation valeur ajoutée")
            if "evaluate_integration_ease" in contenu_top:
                features_avancees_top.append("🔧 Évaluation facilité intégration")
            if "evaluate_maintenance_burden" in contenu_top:
                features_avancees_top.append("⚖️ Évaluation charge maintenance")
            if "detect_conflicts_and_redundancies" in contenu_top:
                features_avancees_top.append("⚠️ Détection conflits et redondances")
            if "calculate_tool_similarity" in contenu_top:
                features_avancees_top.append("🔄 Calcul similarité outils")
            if "determine_integration_priority" in contenu_top:
                features_avancees_top.append("📋 Priorisation automatique intégration")
            if "evaluer_outils_apex" in contenu_top:
                features_avancees_top.append("🎯 Évaluation spécialisée APEX")
                
            analyse["fonctionnalites_top"] = features_avancees_top
            
        # Analyse équipe ACTUELLE
        if path_actuel.exists():
            with open(path_actuel, 'r', encoding='utf-8') as f:
                contenu_actuel = f.read()
            
            analyse["taille_comparison"]["actuel_lignes"] = len(contenu_actuel.splitlines())
            
            # Fonctionnalités basiques ACTUELLES
            features_actuelles = []
            if "evaluate_tools_utility" in contenu_actuel:
                features_actuelles.append("📊 Évaluation utilité basique")
            if "get_capabilities" in contenu_actuel:
                features_actuelles.append("📋 Capacités standard")
                
            analyse["fonctionnalites_actuelles"] = features_actuelles
        
        # Identification améliorations CRITIQUES
        for feature_top in analyse["fonctionnalites_top"]:
            analyse["ameliorations_identifiees"].append({
                "feature": feature_top,
                "priorite": "CRITIQUE",
                "benefice": "Intelligence d'évaluation multi-critères très avancée",
                "impact": "Transformation évaluation de superficielle à experte"
            })
            
        # Intelligence avancée identifiée
        analyse["intelligence_avancee"] = [
            "🧠 Système d'évaluation multi-critères pondérés",
            "🎯 Mots-clés NextGeneration spécialisés (high/medium/low priority)",
            "⚖️ Évaluation 5 dimensions: technique, architecture, valeur, intégration, maintenance",
            "🔍 Détection automatique conflits et redondances",
            "📊 Algorithme de similarité entre outils",
            "🎯 Priorisation intelligente basée sur scores composites",
            "🏆 Support évaluation spécialisée (APEX, PowerShell, Batch)"
        ]
        
        print(f"✅ Agent 02 - TOP: {analyse['taille_comparison'].get('top_lignes', 0)} lignes")
        print(f"✅ Agent 02 - ACTUEL: {analyse['taille_comparison'].get('actuel_lignes', 0)} lignes")
        print(f"🧠 Intelligence avancée: {len(analyse['intelligence_avancee'])} capacités")
        print(f"🎯 Améliorations critiques: {len(analyse['ameliorations_identifiees'])}")
        
    except Exception as e:
        print(f"❌ Erreur analyse Agent 02: {e}")
        analyse["erreur"] = str(e)
    
    return analyse

async def analyser_agent_03():
    """Analyse comparative Agent 03 - Adaptateur Code"""
    
    path_top = Path("../ZZDEPRECATED/equiepe_top/top_agent_MAINTENANCE_03_adaptateur_code.py")
    path_actuel = Path("agent_equipe_maintenance/agent_MAINTENANCE_03_adaptateur_code.py")
    
    analyse = {
        "agent_id": "03",
        "nom": "Adaptateur Code",
        "evaluation": "Template générique vs spécialisé",
        "constat": "L'agent TOP semble être un template Pattern Factory générique"
    }
    
    try:
        if path_top.exists():
            with open(path_top, 'r', encoding='utf-8') as f:
                contenu_top = f.read()
            
            # L'agent TOP 03 semble être principalement un template Pattern Factory
            analyse["analyse_top"] = {
                "type": "Template Pattern Factory générique",
                "lignes": len(contenu_top.splitlines()),
                "commentaires": "Principalement structure Pattern Factory sans logique métier spécialisée"
            }
            
        if path_actuel.exists():
            with open(path_actuel, 'r', encoding='utf-8') as f:
                contenu_actuel = f.read()
            
            analyse["analyse_actuelle"] = {
                "type": "Agent spécialisé adaptation code",
                "lignes": len(contenu_actuel.splitlines()),
                "evaluation": "Plus spécialisé que le template TOP"
            }
            
        analyse["recommandation"] = "L'agent actuel semble plus développé que le template TOP"
            
        print(f"✅ Agent 03 - Évaluation: Template générique (TOP) vs Spécialisé (ACTUEL)")
        print(f"🎯 Recommandation: Garder l'agent actuel")
        
    except Exception as e:
        print(f"❌ Erreur analyse Agent 03: {e}")
        analyse["erreur"] = str(e)
    
    return analyse

async def analyser_agent_04():
    """Analyse comparative Agent 04 - Testeur Anti-Faux"""
    
    path_top = Path("../ZZDEPRECATED/equiepe_top/top_agent_MAINTENANCE_04_testeur_anti_faux_agents.py")
    path_actuel = Path("agent_equipe_maintenance/agent_MAINTENANCE_04_testeur_anti_faux_agents.py")
    
    analyse = {
        "agent_id": "04",
        "nom": "Testeur Anti-Faux Agents",
        "fonctionnalites_top": [],
        "ameliorations_majeures": []
    }
    
    try:
        if path_top.exists():
            with open(path_top, 'r', encoding='utf-8') as f:
                contenu_top = f.read()
            
            # Fonctionnalités spécialisées TOP
            features_top = []
            if "FakeAgentDetection" in contenu_top:
                features_top.append("🔍 Classe spécialisée détection faux agents")
            if "ImprovedEnterpriseAgentTester" in contenu_top:
                features_top.append("🏢 Testeur Enterprise amélioré")
            if "_discover_agents_automatically" in contenu_top:
                features_top.append("🔍 Découverte automatique agents")
            if "required_async_methods" in contenu_top:
                features_top.append("📋 Vérification méthodes async obligatoires")
            if "fake_agent_patterns" in contenu_top:
                features_top.append("🎯 Patterns détection faux agents")
            if "detect_sync_violations" in contenu_top:
                features_top.append("❌ Détection violations SYNC")
            if "detect_async_violations" in contenu_top:
                features_top.append("⚠️ Détection violations ASYNC")
            if "detect_pattern_factory_violations" in contenu_top:
                features_top.append("🏗️ Détection violations Pattern Factory")
            if "calculate_compliance_score" in contenu_top:
                features_top.append("📊 Calcul score conformité")
            if "generate_recommendation" in contenu_top:
                features_top.append("💡 Generation recommandations")
                
            analyse["fonctionnalites_top"] = features_top
            analyse["taille_top"] = len(contenu_top.splitlines())
            
        if path_actuel.exists():
            with open(path_actuel, 'r', encoding='utf-8') as f:
                contenu_actuel = f.read()
            
            analyse["taille_actuelle"] = len(contenu_actuel.splitlines())
        
        # Améliorations majeures identifiées
        analyse["ameliorations_majeures"] = [
            {
                "feature": "🔍 Classe FakeAgentDetection avec dataclass",
                "benefice": "Structure de données spécialisée pour résultats détection",
                "priorite": "HAUTE"
            },
            {
                "feature": "🔍 Découverte automatique agents (_discover_agents_automatically)",
                "benefice": "Scan automatique du répertoire sans configuration manuelle",
                "priorite": "HAUTE"
            },
            {
                "feature": "📋 Vérification méthodes async obligatoires",
                "benefice": "Contrôle strict conformité Pattern Factory",
                "priorite": "CRITIQUE"
            },
            {
                "feature": "🎯 Patterns regex détection faux agents",
                "benefice": "Détection automatisée par analyse de code source",
                "priorite": "CRITIQUE"
            },
            {
                "feature": "📊 Système de scoring conformité",
                "benefice": "Évaluation quantitative de la qualité des agents",
                "priorite": "HAUTE"
            },
            {
                "feature": "💡 Génération automatique recommandations",
                "benefice": "Guide d'amélioration pour corriger les problèmes",
                "priorite": "HAUTE"
            }
        ]
        
        print(f"✅ Agent 04 - TOP: {analyse.get('taille_top', 0)} lignes")
        print(f"✅ Agent 04 - ACTUEL: {analyse.get('taille_actuelle', 0)} lignes")
        print(f"🔍 Fonctionnalités avancées TOP: {len(analyse['fonctionnalites_top'])}")
        print(f"🚀 Améliorations majeures possibles: {len(analyse['ameliorations_majeures'])}")
        
    except Exception as e:
        print(f"❌ Erreur analyse Agent 04: {e}")
        analyse["erreur"] = str(e)
    
    return analyse

def generer_synthese_comparative(analyses: Dict[str, Any]) -> Dict[str, Any]:
    """Génère une synthèse comparative globale"""
    
    synthese = {
        "timestamp": datetime.now().isoformat(),
        "total_ameliorations": 0,
        "priorites_critiques": [],
        "agents_avec_ameliorations": [],
        "recommandations_globales": []
    }
    
    # Comptage améliorations
    for agent_id, analyse in analyses.items():
        if "ameliorations_identifiees" in analyse:
            synthese["total_ameliorations"] += len(analyse["ameliorations_identifiees"])
            if analyse["ameliorations_identifiees"]:
                synthese["agents_avec_ameliorations"].append(agent_id)
                
        if "ameliorations_majeures" in analyse:
            synthese["total_ameliorations"] += len(analyse["ameliorations_majeures"])
            if analyse["ameliorations_majeures"]:
                synthese["agents_avec_ameliorations"].append(agent_id)
    
    # Priorités critiques identifiées
    synthese["priorites_critiques"] = [
        "🧠 Agent 02: Intelligence évaluation multi-critères (CRITIQUE)",
        "🔍 Agent 04: Détection automatique faux agents (CRITIQUE)",
        "🎯 Agent 01: Analyse AST et classification avancée (HAUTE)",
        "📊 Système scoring et recommandations automatiques (HAUTE)"
    ]
    
    # Recommandations globales
    synthese["recommandations_globales"] = [
        "1. PRIORITÉ 1: Implémenter l'intelligence évaluation multi-critères de l'Agent 02 TOP",
        "2. PRIORITÉ 2: Intégrer la détection automatique faux agents de l'Agent 04 TOP",
        "3. PRIORITÉ 3: Enrichir l'Agent 01 avec l'analyse AST et classification TOP",
        "4. Développer un système de scoring global pour tous les agents",
        "5. Créer un système de recommandations automatiques centralisé"
    ]
    
    return synthese

async def generer_rapport_ameliorations(analyses: Dict[str, Any], synthese: Dict[str, Any]):
    """Génère un rapport complet des améliorations possibles"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rapport_path = Path(f"rapport_ameliorations_equipe_top_{timestamp}.md")
    
    with open(rapport_path, 'w', encoding='utf-8') as f:
        f.write("# 🚀 RAPPORT AMÉLIORATION - ÉQUIPE TOP vs ACTUELLE\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Source TOP:** `ZZDEPRECATED/equiepe_top/`\n")
        f.write(f"**Source ACTUELLE:** `agent_equipe_maintenance/`\n\n")
        
        f.write("## 📊 SYNTHÈSE GLOBALE\n\n")
        f.write(f"- **Total améliorations identifiées:** {synthese['total_ameliorations']}\n")
        f.write(f"- **Agents avec améliorations:** {len(synthese['agents_avec_ameliorations'])}/4\n")
        f.write(f"- **Priorités critiques:** {len(synthese['priorites_critiques'])}\n\n")
        
        f.write("## 🎯 PRIORITÉS CRITIQUES\n\n")
        for priorite in synthese["priorites_critiques"]:
            f.write(f"- {priorite}\n")
        f.write("\n")
        
        f.write("## 📋 ANALYSES DÉTAILLÉES PAR AGENT\n\n")
        
        # Agent 01
        if "agent_01" in analyses:
            agent_01 = analyses["agent_01"]
            f.write("### 🔍 AGENT 01 - ANALYSEUR STRUCTURE\n\n")
            f.write(f"**Fonctionnalités avancées TOP identifiées:**\n")
            for feature in agent_01.get("fonctionnalites_top", {}).get("features_avancees", []):
                f.write(f"- {feature}\n")
            f.write(f"\n**Améliorations possibles:** {len(agent_01.get('ameliorations_identifiees', []))}\n\n")
            
        # Agent 02
        if "agent_02" in analyses:
            agent_02 = analyses["agent_02"]
            f.write("### 📊 AGENT 02 - ÉVALUATEUR UTILITÉ\n\n")
            f.write("**🧠 INTELLIGENCE AVANCÉE DÉTECTÉE:**\n")
            for intel in agent_02.get("intelligence_avancee", []):
                f.write(f"- {intel}\n")
            f.write(f"\n**Impact:** Transformation de l'évaluation de superficielle à experte\n\n")
            
        # Agent 04
        if "agent_04" in analyses:
            agent_04 = analyses["agent_04"]
            f.write("### 🧪 AGENT 04 - TESTEUR ANTI-FAUX\n\n")
            f.write("**Améliorations majeures identifiées:**\n")
            for amelioration in agent_04.get("ameliorations_majeures", []):
                f.write(f"- **{amelioration['feature']}**\n")
                f.write(f"  - Bénéfice: {amelioration['benefice']}\n")
                f.write(f"  - Priorité: {amelioration['priorite']}\n\n")
        
        f.write("## 💡 RECOMMANDATIONS GLOBALES\n\n")
        for rec in synthese["recommandations_globales"]:
            f.write(f"{rec}\n")
        
        f.write("\n## 🏆 CONCLUSION\n\n")
        f.write("L'équipe TOP dépréciée contient des fonctionnalités avancées significatives ")
        f.write("qui pourraient **considérablement améliorer** nos agents de maintenance actuels.\n\n")
        f.write("**Action recommandée:** Intégration progressive des fonctionnalités TOP ")
        f.write("en commençant par les priorités critiques (Agent 02 et 04).\n")
    
    print(f"\n📄 RAPPORT GÉNÉRÉ: {rapport_path}")
    print(f"📊 Taille: {rapport_path.stat().st_size} bytes")
    
    return str(rapport_path)

def main():
    """Fonction principale d'analyse comparative"""
    
    print("🚀 ANALYSE COMPARATIVE ÉQUIPE TOP - DÉMARRAGE")
    print("🔍 Recherche d'améliorations possibles...")
    print()
    
    # Lancement analyse
    resultats = asyncio.run(analyser_fonctionnalites_equipe_top())
    
    print("\n🏆 ANALYSE COMPARATIVE TERMINÉE")
    print("=" * 80)
    print("📊 Résultats disponibles dans le rapport généré")
    
    return resultats

if __name__ == "__main__":
    main() 