#!/usr/bin/env python3
"""
Analyse stratégique de la documentation agent_19_auditeur_performance.md 
en utilisant les agents enrichis avec génération de rapports stratégiques

Agents utilisés:
- agent_01_coordinateur_principal.py (rapports coordination/orchestration)
- agent_02_architecte_code_expert.py (rapports architecture/intégration)
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# Configuration des chemins
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Classes Task/Result simples pour les tests
class Task:
    def __init__(self, task_id: str, description: str = None, name: str = None, **kwargs):
        self.task_id = task_id
        self.description = description
        self.name = name or description
        for key, value in kwargs.items():
            setattr(self, key, value)

class Result:
    def __init__(self, success: bool, data=None, error=None):
        self.success = success
        self.data = data
        self.error = error

async def analyser_avec_agent_01(doc_content: str) -> dict:
    """Analyse avec l'agent coordinateur principal (perspective coordination)"""
    print("🎯 Analyse avec Agent 01 - Coordinateur Principal")
    print("-" * 60)
    
    try:
        # Import dynamique pour éviter les dépendances
        from agents.agent_01_coordinateur_principal import Agent01CoordinateurPrincipal
        
        agent = Agent01CoordinateurPrincipal()
        await agent.startup()
        
        # Contexte d'analyse spécialisé pour agent_19
        context_analyse = {
            'document_analyse': 'agent_19_auditeur_performance.md',
            'type_analyse': 'coordination_audit_performance',
            'objectif': 'evaluer_integration_equipe',
            'focus': 'coordination_audits_sprint',
            'periode': 'sprint_3_5'
        }
        
        # 1. Rapport Global - Vision coordination d'équipe
        print("📊 Génération rapport global - Vision coordination...")
        task_global = Task(
            task_id="analyse_agent19_global",
            description="GENERATE_STRATEGIC_REPORT"
        )
        task_global.context = context_analyse
        task_global.type_rapport = 'global'
        
        result_global = await agent.execute_task(task_global)
        
        # 2. Rapport Performance - Focus coordination audits
        print("⚡ Génération rapport performance - Coordination audits...")
        task_perf = Task(
            task_id="analyse_agent19_perf",
            description="GENERATE_STRATEGIC_REPORT"
        )
        task_perf.context = {**context_analyse, 'focus_performance': 'coordination_audits'}
        task_perf.type_rapport = 'performance'
        
        result_perf = await agent.execute_task(task_perf)
        
        await agent.shutdown()
        
        if result_global.success and result_perf.success:
            print("✅ Analyse Agent 01 terminée avec succès")
            return {
                'agent': 'agent_01_coordinateur_principal',
                'perspective': 'coordination_orchestration',
                'rapport_global': result_global.data,
                'rapport_performance': result_perf.data,
                'analyse_succes': True
            }
        else:
            error_msg = result_global.error or result_perf.error
            print(f"❌ Erreur analyse Agent 01: {error_msg}")
            return {'agent': 'agent_01', 'erreur': error_msg, 'analyse_succes': False}
            
    except Exception as e:
        print(f"💥 Exception Agent 01: {e}")
        return {'agent': 'agent_01', 'exception': str(e), 'analyse_succes': False}

async def analyser_avec_agent_02(doc_content: str) -> dict:
    """Analyse avec l'agent architecte code expert (perspective architecture)"""
    print("\n🏗️ Analyse avec Agent 02 - Architecte Code Expert")
    print("-" * 60)
    
    try:
        from agents.agent_02_architecte_code_expert import Agent02ArchitecteCodeExpert
        
        agent = Agent02ArchitecteCodeExpert()
        await agent.startup()
        
        # Contexte d'analyse spécialisé architecture pour agent_19
        context_analyse = {
            'document_analyse': 'agent_19_auditeur_performance.md',
            'type_analyse': 'architecture_audit_performance',
            'objectif': 'evaluer_patterns_design',
            'focus': 'pattern_factory_audit',
            'integration_cible': 'audit_performance_ecosystem'
        }
        
        # 1. Rapport Architecture - Analyse patterns et design
        print("🏛️ Génération rapport architecture - Patterns audit...")
        task_arch = Task(
            task_id="analyse_agent19_arch",
            name="generate_strategic_report"
        )
        task_arch.context = context_analyse
        task_arch.type_rapport = 'architecture'
        
        result_arch = await agent.execute_task(task_arch)
        
        # 2. Rapport Qualité Code - Focus robustesse audit
        print("🎯 Génération rapport qualité code - Robustesse audit...")
        task_qualite = Task(
            task_id="analyse_agent19_qualite",
            name="generate_strategic_report"
        )
        task_qualite.context = {**context_analyse, 'focus_qualite': 'robustesse_audit_performance'}
        task_qualite.type_rapport = 'qualite_code'
        
        result_qualite = await agent.execute_task(task_qualite)
        
        await agent.shutdown()
        
        if result_arch.success and result_qualite.success:
            print("✅ Analyse Agent 02 terminée avec succès")
            return {
                'agent': 'agent_02_architecte_code_expert',
                'perspective': 'architecture_integration',
                'rapport_architecture': result_arch.data,
                'rapport_qualite_code': result_qualite.data,
                'analyse_succes': True
            }
        else:
            error_msg = result_arch.error or result_qualite.error
            print(f"❌ Erreur analyse Agent 02: {error_msg}")
            return {'agent': 'agent_02', 'erreur': error_msg, 'analyse_succes': False}
            
    except Exception as e:
        print(f"💥 Exception Agent 02: {e}")
        return {'agent': 'agent_02', 'exception': str(e), 'analyse_succes': False}

def analyser_contenu_documentation(doc_content: str) -> dict:
    """Analyse basique du contenu de la documentation"""
    print("\n📋 Analyse basique contenu documentation")
    print("-" * 50)
    
    lignes = doc_content.split('\n')
    
    # Extraction d'informations clés
    infos = {
        'titre': 'agent_19_auditeur_performance',
        'total_lignes': len(lignes),
        'sections': [],
        'capabilities': [],
        'patterns_detectes': [],
        'statut': 'inconnu'
    }
    
    for ligne in lignes:
        if ligne.strip().startswith('##'):
            section = ligne.strip().replace('#', '').strip()
            infos['sections'].append(section)
        elif 'Pattern Factory' in ligne:
            infos['patterns_detectes'].append('Pattern Factory')
        elif '**Statut :**' in ligne:
            infos['statut'] = ligne.split('**Statut :**')[1].strip()
        elif ligne.strip().startswith('- ') and 'audit' in ligne.lower():
            infos['capabilities'].append(ligne.strip()[2:])
    
    print(f"📄 Document: {infos['titre']}")
    print(f"📝 Lignes: {infos['total_lignes']}")
    print(f"📑 Sections: {len(infos['sections'])}")
    print(f"🎯 Capacités: {len(infos['capabilities'])}")
    print(f"📐 Patterns: {infos['patterns_detectes']}")
    print(f"✅ Statut: {infos['statut']}")
    
    return infos

async def generer_synthese_strategique(analyse_01: dict, analyse_02: dict, analyse_doc: dict) -> dict:
    """Génère une synthèse stratégique combinant les analyses des 2 agents"""
    print("\n🎯 Génération synthèse stratégique combinée")
    print("=" * 60)
    
    timestamp = datetime.now()
    
    # Scores consolidés
    score_coordination = 0
    score_architecture = 0
    
    if analyse_01.get('analyse_succes'):
        rapport_global = analyse_01.get('rapport_global', {})
        resume_exec = rapport_global.get('resume_executif', {})
        score_coordination = resume_exec.get('score_coordination_global', 0)
    
    if analyse_02.get('analyse_succes'):
        rapport_arch = analyse_02.get('rapport_architecture', {})
        resume_exec = rapport_arch.get('resume_executif', {})
        score_architecture = resume_exec.get('score_architecture_global', 0)
    
    score_global = (score_coordination + score_architecture) / 2
    
    # Recommandations consolidées
    recommandations_strategiques = []
    
    if score_coordination < 80:
        recommandations_strategiques.append("🔄 COORDINATION: Améliorer intégration agent_19 dans workflows équipe")
    if score_architecture < 80:
        recommandations_strategiques.append("🏗️ ARCHITECTURE: Renforcer patterns audit performance")
    
    # Analyse documentation
    if analyse_doc.get('statut') == 'Production Ready':
        recommandations_strategiques.append("✅ DOCUMENTATION: Agent prêt production selon docs")
    
    if not recommandations_strategiques:
        recommandations_strategiques.append("🚀 EXCELLENT: Agent_19 optimal selon analyse bi-agents")
    
    synthese = {
        'analyse_strategique_agent_19': {
            'timestamp': timestamp.isoformat(),
            'agents_analyseurs': ['agent_01_coordinateur_principal', 'agent_02_architecte_code_expert'],
            'document_analyse': 'agent_19_auditeur_performance.md',
            
            'scores_consolides': {
                'score_global_bi_agents': round(score_global, 1),
                'score_coordination': score_coordination,
                'score_architecture': score_architecture,
                'fiabilite_analyse': 'haute' if analyse_01.get('analyse_succes') and analyse_02.get('analyse_succes') else 'partielle'
            },
            
            'evaluation_documentation': analyse_doc,
            
            'perspective_coordination': {
                'agent_source': 'agent_01_coordinateur_principal',
                'succes': analyse_01.get('analyse_succes', False),
                'rapport_disponible': 'rapport_global' in analyse_01 and 'rapport_performance' in analyse_01
            },
            
            'perspective_architecture': {
                'agent_source': 'agent_02_architecte_code_expert', 
                'succes': analyse_02.get('analyse_succes', False),
                'rapport_disponible': 'rapport_architecture' in analyse_02 and 'rapport_qualite_code' in analyse_02
            },
            
            'recommandations_strategiques_consolidees': recommandations_strategiques,
            
            'prochaines_actions': [
                "Valider implémentation agent_19 selon patterns identifiés",
                "Intégrer agent_19 dans workflows coordination",
                "Tester audit performance en conditions réelles",
                "Documenter intégration avec équipe audit"
            ],
            
            'metadonnees': {
                'methode_analyse': 'bi_agents_strategiques',
                'version_analyse': '1.0',
                'agents_version': ['coordinateur_v3.5', 'architecte_v2.1'],
                'couverture_analyse': 'complete'
            }
        },
        
        'donnees_brutes': {
            'analyse_agent_01': analyse_01,
            'analyse_agent_02': analyse_02,
            'analyse_documentation': analyse_doc
        }
    }
    
    return synthese

async def main():
    """Fonction principale d'analyse"""
    print("🚀 ANALYSE STRATÉGIQUE AGENT_19 AVEC AGENTS ENRICHIS")
    print("=" * 80)
    print("🎯 Utilisation des agents enrichis pour analyser agent_19_auditeur_performance.md")
    print()
    
    # Lecture du document
    doc_path = "/mnt/c/Dev/nextgeneration/docs/3_Agents_et_Modeles_IA/agents/agent_19_auditeur_performance.md"
    
    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            doc_content = f.read()
        print(f"✅ Document lu: {len(doc_content)} caractères")
    except Exception as e:
        print(f"❌ Erreur lecture document: {e}")
        return
    
    # Analyse basique de la documentation
    analyse_doc = analyser_contenu_documentation(doc_content)
    
    # Analyses avec les agents enrichis
    analyse_01 = await analyser_avec_agent_01(doc_content)
    analyse_02 = await analyser_avec_agent_02(doc_content)
    
    # Synthèse stratégique
    synthese = await generer_synthese_strategique(analyse_01, analyse_02, analyse_doc)
    
    # Sauvegarde des résultats
    output_file = f"/mnt/c/Dev/nextgeneration/analyse_strategique_agent_19_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(synthese, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Analyse sauvegardée: {output_file}")
    except Exception as e:
        print(f"⚠️ Erreur sauvegarde: {e}")
    
    # Affichage du résumé
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ DE L'ANALYSE STRATÉGIQUE")
    print("=" * 80)
    
    scores = synthese['analyse_strategique_agent_19']['scores_consolides']
    print(f"🎯 Score global bi-agents: {scores['score_global_bi_agents']}")
    print(f"🔄 Score coordination: {scores['score_coordination']}")
    print(f"🏗️ Score architecture: {scores['score_architecture']}")
    print(f"📊 Fiabilité analyse: {scores['fiabilite_analyse']}")
    
    recommandations = synthese['analyse_strategique_agent_19']['recommandations_strategiques_consolidees']
    print(f"\n📋 Recommandations stratégiques ({len(recommandations)}):")
    for i, rec in enumerate(recommandations, 1):
        print(f"  {i}. {rec}")
    
    print(f"\n✅ ANALYSE TERMINÉE - Agent_19 évalué par 2 agents stratégiques")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"💥 ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        exit(1)