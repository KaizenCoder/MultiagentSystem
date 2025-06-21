#!/usr/bin/env python3
"""
🎯 SÉLECTION DIRECTE 3 CANDIDATS OPTIMAUX
Utilise les rapports d'audit existants pour proposer 3 candidats
"""
import json
import sys
from pathlib import Path
from datetime import datetime

# Chemins
REPORTS_DIR = Path("C:/Dev/nextgeneration/agent_factory_implementation/agents/reviews")
AGENTS_DIR = Path("C:/Dev/nextgeneration/agent_factory_implementation/agents")

def charger_dernier_rapport_audit():
    """Charge le dernier rapport d'audit Pattern Factory"""
    try:
        # Priorité au rapport de critique conformité
        critique_files = list(REPORTS_DIR.glob("CRITIQUE_conformite_pattern_factory_*.json"))
        if critique_files:
            dernier_rapport = max(critique_files, key=lambda x: x.stat().st_mtime)
            print(f"📊 Chargement rapport critique: {dernier_rapport.name}")
            
            with open(dernier_rapport, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Sinon chercher les autres rapports
        audit_files = list(REPORTS_DIR.glob("audit_pattern_factory_*.json"))
        mission_files = list(REPORTS_DIR.glob("mission_directe_results_*.json"))
        
        all_files = audit_files + mission_files
        
        if not all_files:
            print("❌ Aucun rapport d'audit trouvé")
            return None
        
        dernier_rapport = max(all_files, key=lambda x: x.stat().st_mtime)
        print(f"📊 Chargement rapport: {dernier_rapport.name}")
        
        with open(dernier_rapport, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    except Exception as e:
        print(f"❌ Erreur chargement rapport: {e}")
        return None

def analyser_candidats_potentiels(audit_data):
    """Analyse les agents pour identifier les meilleurs candidats"""
    # Adapter pour différents formats de rapport
    agents_analysis = {}
    
    if "agents_analysis" in audit_data:
        # Format d'audit standard
        agents_analysis = audit_data.get("agents_analysis", {})
    elif "agents_analyses" in audit_data:
        # Format de critique conformité
        agents_list = audit_data.get("agents_analyses", [])
        for agent_data in agents_list:
            agent_file = agent_data.get("nom_fichier", "")
            if agent_file:
                # Convertir au format standard
                agents_analysis[agent_file] = {
                    "conformity_status": convert_status(agent_data.get("conformite_status", "unknown")),
                    "critical_issues": agent_data.get("problemes_identifies", []),
                    "file_info": {
                        "size": agent_data.get("taille", 0)
                    },
                    "pattern_factory_score": agent_data.get("pattern_factory_score", 0),
                    "recommendations": agent_data.get("recommandations", [])
                }
    
    candidats_potentiels = []
    
    print(f"🔍 Analyse de {len(agents_analysis)} agents...")
    
    for agent_file, analysis in agents_analysis.items():
        if not isinstance(analysis, dict):
            continue
            
        conformity_status = analysis.get("conformity_status", "unknown")
        critical_issues = analysis.get("critical_issues", [])
        file_info = analysis.get("file_info", {})
        file_size = file_info.get("size", 0)
        
        # Calculer score de candidature (plus bas = meilleur)
        score = calculer_score_candidature(conformity_status, critical_issues, file_size)
        
        candidat = {
            "agent_file": agent_file,
            "score_candidature": score,
            "conformity_status": conformity_status,
            "critical_issues": critical_issues,
            "file_size": file_size,
            "file_path": str(AGENTS_DIR / agent_file),
            "pattern_factory_score": analysis.get("pattern_factory_score", 0),
            "recommendations": analysis.get("recommendations", []),
            "raisons_selection": []
        }
        
        candidats_potentiels.append(candidat)
    
    return candidats_potentiels

def convert_status(status):
    """Convertit le statut du rapport de critique au format standard"""
    if status == "NON_CONFORME":
        return "critical_errors"
    elif status == "PARTIELLEMENT_CONFORME":
        return "non_compliant"
    elif status == "CONFORME":
        return "compliant"
    else:
        return "unknown"

def calculer_score_candidature(status, issues, size):
    """Calcule un score de candidature (plus bas = meilleur candidat)"""
    score = 0
    
    # Status de conformité
    if status == "critical_errors":
        score += 5  # Erreurs critiques = facile à identifier
    elif status == "non_compliant":
        score += 15  # Non conforme mais sans erreurs critiques
    elif status == "compliant":
        score += 50  # Déjà conforme = moins intéressant
    else:
        score += 30  # Statut inconnu
    
    # Nombre d'erreurs critiques
    score += len(issues) * 3
    
    # Taille du fichier (favoriser taille moyenne)
    if 15000 <= size <= 40000:  # Taille idéale
        score -= 10
    elif size > 80000:  # Trop gros
        score += 25
    elif size < 8000:  # Trop petit
        score += 15
    
    return score

def generer_raisons_selection(candidat):
    """Génère les raisons de sélection pour un candidat"""
    raisons = []
    
    status = candidat["conformity_status"]
    issues = candidat["critical_issues"]
    size = candidat["file_size"]
    
    if status == "critical_errors":
        raisons.append("🚨 Erreurs critiques détectées - transformation prioritaire")
    elif status == "non_compliant":
        raisons.append("⚠️ Non-conforme Pattern Factory - bon candidat")
    
    if 15000 <= size <= 40000:
        raisons.append("📏 Taille optimale pour test de transformation")
    elif size < 15000:
        raisons.append("📏 Fichier compact - transformation rapide")
    
    if len(issues) <= 5:
        raisons.append(f"🔧 Nombre raisonnable d'erreurs ({len(issues)})")
    elif len(issues) > 5:
        raisons.append(f"🔥 Plusieurs erreurs à corriger ({len(issues)}) - bon test")
    
    if candidat["score_candidature"] < 20:
        raisons.append("⭐ Score de facilité élevé")
    
    # Analyser les types d'erreurs
    types_erreurs = set()
    for issue in issues:
        if "async async def" in issue:
            types_erreurs.add("syntaxe")
        if "import" in issue.lower():
            types_erreurs.add("imports")
        if "inherit" in issue.lower():
            types_erreurs.add("héritage")
    
    if types_erreurs:
        raisons.append(f"🎯 Types d'erreurs variés: {', '.join(types_erreurs)}")
    
    return raisons

def selectionner_top3_candidats(candidats_potentiels):
    """Sélectionne les 3 meilleurs candidats avec diversité"""
    # Trier par score (meilleurs en premier)
    candidats_tries = sorted(candidats_potentiels, key=lambda x: x["score_candidature"])
    
    # Sélectionner top 3 avec diversité de statuts
    candidats_finaux = []
    statuts_selectionnes = set()
    
    # Premier passage: prendre les meilleurs de chaque statut
    for candidat in candidats_tries:
        if len(candidats_finaux) >= 3:
            break
            
        status = candidat["conformity_status"]
        if status not in statuts_selectionnes:
            candidat["raisons_selection"] = generer_raisons_selection(candidat)
            candidats_finaux.append(candidat)
            statuts_selectionnes.add(status)
    
    # Deuxième passage: compléter si nécessaire
    for candidat in candidats_tries:
        if len(candidats_finaux) >= 3:
            break
            
        if candidat not in candidats_finaux:
            candidat["raisons_selection"] = generer_raisons_selection(candidat)
            candidats_finaux.append(candidat)
    
    return candidats_finaux[:3]

def afficher_candidats(candidats):
    """Affiche les candidats sélectionnés"""
    print("\n" + "="*70)
    print("🎯 TOP 3 CANDIDATS POUR TRANSFORMATION PATTERN FACTORY")
    print("="*70)
    
    for i, candidat in enumerate(candidats, 1):
        priorite = "🔥 PRIORITÉ HAUTE" if i == 1 else "⚡ PRIORITÉ MOYENNE" if i == 2 else "📋 PRIORITÉ NORMALE"
        
        print(f"\n🏆 CANDIDAT #{i} - {priorite}")
        print(f"📁 Agent: {candidat['agent_file']}")
        print(f"📊 Score candidature: {candidat['score_candidature']}")
        print(f"📋 Statut conformité: {candidat['conformity_status']}")
        print(f"📏 Taille fichier: {candidat['file_size']:,} caractères")
        print(f"🚨 Erreurs critiques: {len(candidat['critical_issues'])}")
        
        if candidat['critical_issues']:
            print("   Détail erreurs:")
            for issue in candidat['critical_issues'][:3]:  # Limiter à 3
                print(f"   • {issue}")
            if len(candidat['critical_issues']) > 3:
                print(f"   • ... et {len(candidat['critical_issues']) - 3} autres")
        
        print("✅ Raisons de sélection:")
        for raison in candidat['raisons_selection']:
            print(f"   {raison}")
    
    print(f"\n🎯 INSTRUCTIONS:")
    print(f"Sélectionnez le numéro du candidat à transformer (1-3)")
    print(f"Ou tapez 'all' pour voir tous les détails")

def sauvegarder_rapport_candidats(candidats):
    """Sauvegarde le rapport des candidats"""
    rapport = {
        "mission_id": f"selection_candidats_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "timestamp": datetime.now().isoformat(),
        "candidats_selectionnes": candidats,
        "criteres_selection": [
            "Facilité de transformation",
            "Diversité des types d'erreurs", 
            "Taille optimale du fichier",
            "Impact minimal"
        ],
        "recommandation": "Commencer par le candidat #1 (score le plus bas)"
    }
    
    rapport_file = REPORTS_DIR / f"candidats_transformation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(rapport_file, 'w', encoding='utf-8') as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Rapport sauvé: {rapport_file.name}")
    return rapport_file

def main():
    """Point d'entrée principal"""
    print("🚀 SÉLECTION DIRECTE 3 CANDIDATS OPTIMAUX")
    print("="*50)
    
    try:
        # 1. Charger le dernier rapport d'audit
        audit_data = charger_dernier_rapport_audit()
        if not audit_data:
            return 1
        
        # 2. Analyser les candidats potentiels
        print("\n🔍 ANALYSE DES CANDIDATS POTENTIELS")
        candidats_potentiels = analyser_candidats_potentiels(audit_data)
        
        if not candidats_potentiels:
            print("❌ Aucun candidat potentiel trouvé")
            return 1
        
        print(f"✅ {len(candidats_potentiels)} candidats potentiels identifiés")
        
        # 3. Sélectionner top 3
        print("\n🎯 SÉLECTION TOP 3 CANDIDATS")
        top3_candidats = selectionner_top3_candidats(candidats_potentiels)
        
        # 4. Afficher les résultats
        afficher_candidats(top3_candidats)
        
        # 5. Sauvegarder rapport
        sauvegarder_rapport_candidats(top3_candidats)
        
        return 0
        
    except Exception as e:
        print(f"💥 Erreur fatale: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 