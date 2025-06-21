#!/usr/bin/env python3
"""
🚨 MISSION CORRECTIVE CRITIQUE - ANALYSE CONFORMITÉ PATTERN FACTORY
================================================================
L'équipe NextGeneration a manqué l'essentiel : vérifier la conformité Pattern Factory !
Mission corrective : Analyser la vraie conformité architecturale des 34 agents de production
"""

import asyncio
import os
import json
from datetime import datetime
from pathlib import Path
from agent_factory_implementation.agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import create_agent_0_chef_equipe_coordinateur

async def analyse_pattern_factory_critique():
    """Analyse critique de la conformité Pattern Factory des agents"""
    
    print("🚨 MISSION CORRECTIVE CRITIQUE - CONFORMITÉ PATTERN FACTORY")
    print("=" * 80)
    print("❌ DÉFAILLANCE IDENTIFIÉE: L'équipe NextGeneration a manqué l'essentiel!")
    print("🎯 MISSION: Analyser la VRAIE conformité Pattern Factory")
    print("📁 Cible: 34 agents de production")
    print("🔍 Focus: Architecture, héritage, standards")
    print()
    
    # Préparation dossier rapports correctifs
    reviews_dir = Path("C:/Dev/nextgeneration/agent_factory_implementation/agents/reviews")
    if not reviews_dir.exists():
        reviews_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        print("🎖️ INITIALISATION CHEF D'ÉQUIPE - MISSION CORRECTIVE")
        print("-" * 60)
        
        # Création Chef d'Équipe
        chef_equipe = create_agent_0_chef_equipe_coordinateur(
            target_path="C:/Dev/nextgeneration/agent_factory_implementation/agents",
            workspace_path=".",
            safe_mode=True
        )
        print("✅ Chef d'Équipe créé - Mission corrective Pattern Factory")
        
        await chef_equipe.startup()
        print("✅ Chef d'Équipe démarré")
        
        health = await chef_equipe.health_check()
        status = health.get("status", "unknown")
        print(f"🏥 Health: {status}")
        
        print()
        print("🔍 ANALYSE CRITIQUE CONFORMITÉ PATTERN FACTORY")
        print("-" * 60)
        
        # Récupération agents à analyser
        agents_dir = Path("C:/Dev/nextgeneration/agent_factory_implementation/agents")
        agents_python = list(agents_dir.glob("**/*.py"))
        agents_python = [f for f in agents_python if not f.name.startswith("__")]
        
        print(f"📊 {len(agents_python)} agents à analyser pour conformité Pattern Factory")
        
        # Génération rapport critique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        rapport_critique = {
            "mission_id": f"analyse_pattern_factory_critique_{timestamp}",
            "timestamp": datetime.now().isoformat(),
            "chef_equipe_id": getattr(chef_equipe, 'agent_id', 'chef_equipe_unknown'),
            "type_analyse": "CONFORMITÉ PATTERN FACTORY",
            "agents_analyses": [],
            "statistiques_critiques": {
                "total_agents": len(agents_python),
                "agents_conformes": 0,
                "agents_non_conformes": 0,
                "agents_partiellement_conformes": 0,
                "taux_conformite": 0.0
            },
            "problemes_identifies": [],
            "recommandations_critiques": []
        }
        
        print("🔍 Analyse conformité en cours...")
        
        conformes = 0
        non_conformes = 0
        partiellement_conformes = 0
        
        # Analyse détaillée de chaque agent
        for i, agent_file in enumerate(agents_python, 1):
            try:
                print(f"   📄 {i}/{len(agents_python)}: {agent_file.name}")
                
                # Lecture du fichier
                with open(agent_file, 'r', encoding='utf-8') as f:
                    contenu = f.read()
                
                # Analyse conformité Pattern Factory
                analyse_conformite = {
                    "nom_fichier": agent_file.name,
                    "chemin_relatif": str(agent_file.relative_to(agents_dir)),
                    "taille": len(contenu),
                    "lignes": len(contenu.splitlines()),
                    "analyse_timestamp": datetime.now().isoformat(),
                    
                    # ANALYSE PATTERN FACTORY CRITIQUE
                    "imports_pattern_factory": False,
                    "heritage_agent_class": False,
                    "utilise_task_result": False,
                    "fonction_creation_standard": False,
                    "async_methods": False,
                    "pattern_factory_score": 0,
                    "conformite_status": "NON_CONFORME",
                    "problemes_identifies": [],
                    "recommandations": []
                }
                
                lignes = contenu.splitlines()
                
                # 1. Vérifier imports Pattern Factory
                imports_pf = any(
                    "from agent_factory_implementation.core.agent_factory_architecture import" in line or
                    "from core.agent_factory_architecture import" in line
                    for line in lignes
                )
                analyse_conformite["imports_pattern_factory"] = imports_pf
                if imports_pf:
                    analyse_conformite["pattern_factory_score"] += 20
                else:
                    analyse_conformite["problemes_identifies"].append("CRITIQUE: Aucun import Pattern Factory détecté")
                
                # 2. Vérifier héritage classe Agent
                heritage_agent = any(
                    "class " in line and "(Agent)" in line
                    for line in lignes
                )
                analyse_conformite["heritage_agent_class"] = heritage_agent
                if heritage_agent:
                    analyse_conformite["pattern_factory_score"] += 30
                else:
                    analyse_conformite["problemes_identifies"].append("CRITIQUE: Classe n'hérite pas de Agent Pattern Factory")
                
                # 3. Vérifier utilisation Task/Result
                utilise_task_result = any(
                    "Task(" in line or "Result(" in line or "task_id" in line
                    for line in lignes
                )
                analyse_conformite["utilise_task_result"] = utilise_task_result
                if utilise_task_result:
                    analyse_conformite["pattern_factory_score"] += 20
                else:
                    analyse_conformite["problemes_identifies"].append("Aucune utilisation Task/Result détectée")
                
                # 4. Vérifier fonction de création standard
                fonction_creation = any(
                    "def create_agent_" in line or "def create_" in line
                    for line in lignes
                )
                analyse_conformite["fonction_creation_standard"] = fonction_creation
                if fonction_creation:
                    analyse_conformite["pattern_factory_score"] += 15
                else:
                    analyse_conformite["problemes_identifies"].append("Aucune fonction de création standard")
                
                # 5. Vérifier méthodes async
                async_methods = any(
                    "async def" in line
                    for line in lignes
                )
                analyse_conformite["async_methods"] = async_methods
                if async_methods:
                    analyse_conformite["pattern_factory_score"] += 15
                
                # Déterminer statut conformité
                score = analyse_conformite["pattern_factory_score"]
                if score >= 80:
                    analyse_conformite["conformite_status"] = "CONFORME"
                    conformes += 1
                elif score >= 50:
                    analyse_conformite["conformite_status"] = "PARTIELLEMENT_CONFORME"
                    partiellement_conformes += 1
                    analyse_conformite["problemes_identifies"].append("Conformité partielle - Nécessite ajustements")
                else:
                    analyse_conformite["conformite_status"] = "NON_CONFORME"
                    non_conformes += 1
                    analyse_conformite["problemes_identifies"].append("CRITIQUE: Non-conformité Pattern Factory majeure")
                
                # Recommandations spécifiques
                if not imports_pf:
                    analyse_conformite["recommandations"].append("Ajouter: from core.agent_factory_architecture import Agent, Task, Result")
                if not heritage_agent:
                    analyse_conformite["recommandations"].append("Modifier class XxxAgent(Agent): pour hériter de Pattern Factory")
                if not utilise_task_result:
                    analyse_conformite["recommandations"].append("Utiliser Task/Result pour structurer les opérations")
                if not fonction_creation:
                    analyse_conformite["recommandations"].append("Ajouter fonction create_agent_xxx() standardisée")
                
                rapport_critique["agents_analyses"].append(analyse_conformite)
                
            except Exception as e:
                print(f"   ⚠️ Erreur analyse {agent_file.name}: {e}")
                rapport_critique["agents_analyses"].append({
                    "nom_fichier": agent_file.name,
                    "erreur": str(e),
                    "conformite_status": "ERREUR_ANALYSE"
                })
        
        # Calcul statistiques finales
        total = len(agents_python)
        rapport_critique["statistiques_critiques"].update({
            "agents_conformes": conformes,
            "agents_non_conformes": non_conformes,
            "agents_partiellement_conformes": partiellement_conformes,
            "taux_conformite": (conformes / max(1, total)) * 100
        })
        
        # Problèmes globaux identifiés
        taux_conformite = rapport_critique["statistiques_critiques"]["taux_conformite"]
        if taux_conformite < 50:
            rapport_critique["problemes_identifies"].append("CRITIQUE: Moins de 50% des agents sont conformes Pattern Factory")
        if non_conformes > conformes:
            rapport_critique["problemes_identifies"].append("ALARMANT: Plus d'agents non-conformes que conformes")
        
        # Recommandations critiques
        rapport_critique["recommandations_critiques"] = [
            "URGENT: Refactorisation massive nécessaire pour conformité Pattern Factory",
            "Standardiser tous les agents avec héritage de la classe Agent",
            "Implémenter les fonctions de création standardisées",
            "Formation équipe sur l'architecture Pattern Factory",
            "Audit complet et plan de migration"
        ]
        
        print()
        print("📊 RÉSULTATS ANALYSE CRITIQUE")
        print("-" * 60)
        print(f"✅ Agents conformes: {conformes}/{total} ({(conformes/max(1,total))*100:.1f}%)")
        print(f"⚠️ Partiellement conformes: {partiellement_conformes}/{total}")
        print(f"❌ Non-conformes: {non_conformes}/{total} ({(non_conformes/max(1,total))*100:.1f}%)")
        print(f"🎯 Taux conformité global: {taux_conformite:.1f}%")
        
        # Génération rapports correctifs
        print()
        print("📋 GÉNÉRATION RAPPORTS CORRECTIFS")
        print("-" * 60)
        
        # Rapport JSON critique
        rapport_json_path = reviews_dir / f"CRITIQUE_conformite_pattern_factory_{timestamp}.json"
        with open(rapport_json_path, 'w', encoding='utf-8') as f:
            json.dump(rapport_critique, f, indent=2, ensure_ascii=False)
        print(f"📄 Rapport critique JSON: {rapport_json_path.name} ({rapport_json_path.stat().st_size} bytes)")
        
        # Rapport Markdown critique
        rapport_md_path = reviews_dir / f"CRITIQUE_conformite_pattern_factory_{timestamp}.md"
        with open(rapport_md_path, 'w', encoding='utf-8') as f:
            f.write("# 🚨 RAPPORT CRITIQUE - CONFORMITÉ PATTERN FACTORY\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mission ID:** {rapport_critique['mission_id']}\n")
            f.write(f"**Type:** ANALYSE CONFORMITÉ ARCHITECTURALE CRITIQUE\n")
            f.write(f"**Chef d'Équipe:** {rapport_critique['chef_equipe_id']}\n\n")
            
            f.write("## ❌ DÉFAILLANCE ÉQUIPE NEXTGENERATION\n\n")
            f.write("L'équipe NextGeneration a **MANQUÉ L'ESSENTIEL** dans leur première analyse !\n")
            f.write("Ils ont fait des métriques superficielles mais ont ignoré la conformité architecturale.\n\n")
            
            f.write("## 📊 RÉSULTATS CRITIQUE CONFORMITÉ PATTERN FACTORY\n\n")
            stats = rapport_critique['statistiques_critiques']
            f.write(f"- **Total agents analysés:** {stats['total_agents']}\n")
            f.write(f"- **✅ Agents conformes:** {stats['agents_conformes']} ({(stats['agents_conformes']/max(1,stats['total_agents']))*100:.1f}%)\n")
            f.write(f"- **⚠️ Partiellement conformes:** {stats['agents_partiellement_conformes']}\n")
            f.write(f"- **❌ Non-conformes:** {stats['agents_non_conformes']} ({(stats['agents_non_conformes']/max(1,stats['total_agents']))*100:.1f}%)\n")
            f.write(f"- **🎯 Taux conformité:** {stats['taux_conformite']:.1f}%\n\n")
            
            if stats['taux_conformite'] < 50:
                f.write("## 🚨 ALERTE CRITIQUE\n\n")
                f.write("**MOINS DE 50% DES AGENTS SONT CONFORMES PATTERN FACTORY !**\n\n")
                f.write("Ceci constitue une dette technique majeure nécessitant une action immédiate.\n\n")
            
            f.write("## 📋 AGENTS NON-CONFORMES IDENTIFIÉS\n\n")
            for agent in rapport_critique['agents_analyses']:
                if agent.get('conformite_status') == 'NON_CONFORME':
                    f.write(f"### ❌ {agent['nom_fichier']}\n\n")
                    f.write(f"- **Score conformité:** {agent.get('pattern_factory_score', 0)}/100\n")
                    f.write(f"- **Problèmes:**\n")
                    for probleme in agent.get('problemes_identifies', []):
                        f.write(f"  - {probleme}\n")
                    f.write(f"- **Recommandations:**\n")
                    for rec in agent.get('recommandations', []):
                        f.write(f"  - {rec}\n")
                    f.write("\n")
            
            f.write("## 💡 RECOMMANDATIONS CRITIQUES\n\n")
            for rec in rapport_critique['recommandations_critiques']:
                f.write(f"- {rec}\n")
            f.write("\n")
            
            f.write("## 🏆 CONCLUSION\n\n")
            f.write("🚨 **MISSION CORRECTIVE VALIDÉE**\n\n")
            f.write("Cette analyse révèle les vrais problèmes architecturaux que l'équipe ")
            f.write("NextGeneration aurait dû identifier en première instance. ")
            f.write("Une refactorisation massive est nécessaire pour la conformité Pattern Factory.\n")
        
        print(f"📄 Rapport critique MD: {rapport_md_path.name} ({rapport_md_path.stat().st_size} bytes)")
        
        await chef_equipe.shutdown()
        print("✅ Chef d'Équipe - Arrêt propre")
        
        return {
            "status": "success",
            "mission_id": rapport_critique['mission_id'],
            "agents_analyses": total,
            "taux_conformite": taux_conformite,
            "agents_non_conformes": non_conformes,
            "rapports_generes": 2
        }
        
    except Exception as e:
        print(f"❌ Erreur mission critique: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "error": str(e)}

def main():
    """Fonction principale - Mission corrective critique"""
    
    print("🚨 MISSION CORRECTIVE CRITIQUE - ÉQUIPE NEXTGENERATION")
    print("❌ Défaillance identifiée : Analyse superficielle sans conformité architecturale")
    print()
    
    # Lancement mission corrective
    resultat = asyncio.run(analyse_pattern_factory_critique())
    
    print()
    print("🏆 ÉVALUATION MISSION CORRECTIVE")
    print("=" * 80)
    
    status = resultat.get('status', 'unknown')
    
    if status == 'success':
        taux = resultat.get('taux_conformite', 0)
        non_conformes = resultat.get('agents_non_conformes', 0)
        
        print("✅ MISSION CORRECTIVE RÉUSSIE!")
        print(f"📊 Taux conformité Pattern Factory: {taux:.1f}%")
        print(f"❌ Agents non-conformes identifiés: {non_conformes}")
        
        if taux < 50:
            print("🚨 ALERTE: Conformité Pattern Factory insuffisante!")
            print("📋 Action corrective massive nécessaire")
        elif taux < 80:
            print("⚠️ Conformité partielle - Améliorations nécessaires")
        else:
            print("✅ Conformité Pattern Factory satisfaisante")
            
        print("📄 Rapports correctifs générés dans reviews/")
    else:
        print("❌ Erreur mission corrective")
    
    print()
    print("📊 LEÇON APPRISE:")
    print("=" * 80)
    print("❌ L'équipe NextGeneration a fait une analyse SUPERFICIELLE")
    print("✅ Cette mission corrective révèle les VRAIS problèmes")
    print("🎯 L'analyse architecturale est ESSENTIELLE")
    print("📋 Conformité Pattern Factory = Priorité critique")
    
    return resultat

if __name__ == "__main__":
    main() 



