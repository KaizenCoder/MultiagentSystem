from typing import Dict, List, Optional, Any, Union, Tuple
#!/usr/bin/env python3
"""
Agent Workspace Organizer - Organisation et maintenance du workspace PostgreSQL
Développé par l'équipe de maintenance NextGeneration
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

# Import avec fallback
try:
    from .agent_POSTGRESQL_base import AgentPostgreSQLBase
except ImportError:
    try:
        from agent_POSTGRESQL_base import AgentPostgreSQLBase
    except ImportError:
        # Fallback pour AgentPostgreSQLBase
        class AgentPostgreSQLBase:
            def __init__(self, *args, **kwargs):
                pass
from core.agent_factory_architecture import Task, Result

class AgentPostgresqlWorkspaceOrganizer(AgentPostgreSQLBase):
    """Agent spécialisé dans l'organisation et la maintenance du workspace PostgreSQL."""
    
    def __init__(self, workspace_root: Path = None):
        super().__init__(
            agent_type="postgresql_workspace_organizer",
            name="Agent Workspace Organizer"
        )
        
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="postgresql",
                custom_config={
                    "logger_name": f"nextgen.postgresql.agent_POSTGRESQL_workspace_organizer.{getattr(self, 'agent_id', 'unknown')}",
                    "log_dir": "logs/postgresql",
                    "metadata": {
                        "agent_type": "agent_POSTGRESQL_workspace_organizer",
                        "agent_role": "postgresql",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)
        self.workspace_root = workspace_root if workspace_root else Path(__file__).parent.parent
        self.rapport_file = self.workspace_root / "docs/agents_postgresql_resolution/rapports" / "workspace_organizer_rapport.md"
        self.rapport_file.parent.mkdir(parents=True, exist_ok=True)

    def get_capabilities(self) -> list:
        return [
            "analyser_structure_workspace",
            "organiser_fichiers",
            "creer_index_rapports"
        ]

    async def execute_task(self, task: Task) -> Result:
        try:
            handlers = {
                "analyser_structure_workspace": self._handle_analyser_structure_workspace,
                "organiser_fichiers": self._handle_organiser_fichiers,
                "creer_index_rapports": self._handle_creer_index_rapports
            }
            handler = handlers.get(task.type)
            if not handler:
                return Result(success=False, error=f"Type de tâche non supporté: {task.type}")
            return await handler(task)
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la tâche: {e}")
            return Result(success=False, error=str(e))

    async def _handle_analyser_structure_workspace(self, task: Task) -> Result:
        structure = await self.analyser_structure_workspace()
        return Result(success=True, data=structure)

    async def _handle_organiser_fichiers(self, task: Task) -> Result:
        structure = task.params.get("structure")
        organisation = await self.organiser_fichiers(structure)
        return Result(success=True, data=organisation)

    async def _handle_creer_index_rapports(self, task: Task) -> Result:
        index = await self.creer_index_rapports()
        return Result(success=True, data={"index_path": str(self.rapport_file), "index": index})

    async def analyser_structure_workspace(self) -> Dict[str, Any]:
        self.logger.info("Analyse de la structure du workspace")
        structure = {
            "timestamp": datetime.now().isoformat(),
            "repertoires": {},
            "fichiers_crees": [],
            "taille_totale": 0,
            "organisation_score": 0
        }
        for item in self.workspace_root.rglob("*"):
            if item.is_file():
                taille = item.stat().st_size
                structure["taille_totale"] += taille
                categorie = self.categoriser_fichier(item)
                structure["fichiers_crees"].append({
                    "chemin": str(item.relative_to(self.workspace_root)),
                    "taille": taille,
                    "modifie": datetime.fromtimestamp(item.stat().st_mtime).isoformat(),
                    "categorie": categorie
                })
            elif item.is_dir():
                fichiers_dans_rep = list(item.glob("*"))
                structure["repertoires"][str(item.relative_to(self.workspace_root))] = {
                    "nombre_fichiers": len([f for f in fichiers_dans_rep if f.is_file()]),
                    "sous_repertoires": len([f for f in fichiers_dans_rep if f.is_dir()]),
                    "taille": sum(f.stat().st_size for f in item.rglob("*") if f.is_file())
                }
        structure["organisation_score"] = self.calculer_score_organisation(structure)
        return structure

    async def organiser_fichiers(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info("Organisation des fichiers")
        organisation = {
            "timestamp": datetime.now().isoformat(),
            "actions_effectuees": [],
            "fichiers_organises": 0,
            "erreurs": []
        }
        try:
            await self.creer_index_rapports()
            organisation["actions_effectuees"].append("Index rapports créé/mis à jour")
            # Nettoyage fichiers temporaires (exemple)
            fichiers_nettoyes = await self.nettoyer_fichiers_temporaires()
            organisation["fichiers_organises"] += fichiers_nettoyes
            organisation["actions_effectuees"].append(f"Nettoyage {fichiers_nettoyes} fichiers temporaires")
        except Exception as e:
            organisation["erreurs"].append(str(e))
            self.logger.error(f"Erreur organisation: {e}")
        return organisation

    async def creer_index_rapports(self) -> str:
        index_content = f"""# Index des Rapports d'Agents PostgreSQL\n\n**Généré automatiquement le :** {datetime.now().isoformat()}\n\n## Rapports Disponibles\n"""
        rapports_dir = self.rapport_file.parent
        if rapports_dir.exists():
            for rapport_file in rapports_dir.glob("*.md"):
                if rapport_file.name != "index.md":
                    agent_name = rapport_file.stem.replace("_rapport", "").replace("_", " ").title()
                    index_content += f"\n### {agent_name}\n- **Fichier :** [{rapport_file.name}](./{rapport_file.name})\n- **Taille :** {rapport_file.stat().st_size} bytes\n- **Modifié :** {datetime.fromtimestamp(rapport_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}\n"
        index_content += f"\n## Statistiques Globales\n- **Nombre agents :** {len(list(rapports_dir.glob('*_rapport.md')))}\n- **Espace total :** {sum(f.stat().st_size for f in rapports_dir.glob('*.md'))} bytes\n- **Dernière mise à jour :** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n*Index généré automatiquement par Agent Workspace Organizer*\n"
        index_path = rapports_dir / "index.md"
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_content)
        return index_content

    async def nettoyer_fichiers_temporaires(self) -> int:
        # Exemple de nettoyage : suppression des fichiers *.tmp
        count = 0
        for tmp_file in self.workspace_root.rglob("*.tmp"):
            try:
                tmp_file.unlink()
                count += 1
            except Exception:
                pass
        return count

    def categoriser_fichier(self, fichier_path: Path) -> str:
        nom = fichier_path.name.lower()
        if nom.endswith('.py'):
            if 'agent_' in nom:
                return "agent_executable"
            elif 'test_' in nom:
                return "script_test"
            elif 'fix_' in nom:
                return "script_correction"
            else:
                return "script_python"
        elif nom.endswith('.md'):
            if 'rapport' in nom:
                return "rapport_agent"
            else:
                return "documentation"
        elif nom.endswith('.json'):
            return "donnees_json"
        elif nom.endswith('.log'):
            return "fichier_log"
        else:
            return "autre"

    def calculer_score_organisation(self, structure: Dict[str, Any]) -> int:
        score = 100
        fichiers_racine = len([f for f in structure["fichiers_crees"] if '/' not in f["chemin"] and f["chemin"] != "README.md"])
        score -= fichiers_racine * 5
        fichiers_par_categorie = {}
        for fichier in structure["fichiers_crees"]:
            cat = fichier["categorie"]
            fichiers_par_categorie[cat] = fichiers_par_categorie.get(cat, 0) + 1
        if fichiers_par_categorie.get("rapport_agent", 0) >= 4:
            score += 10
        return max(0, min(100, score))

    # ✅ MÉTHODES STANDARDISÉES DE RAPPORT

    def _calculate_report_score(self, metrics: Dict[str, Any]) -> int:
        """Calcule le score global du rapport basé sur les métriques."""
        score = 0
        issues_critiques = []
        
        # Logique de scoring spécifique à l'agent
        # À adapter selon le type d'agent
        
        return score
    
    def _assess_conformity(self, score: int) -> str:
        """Évalue la conformité basée sur le score."""
        if score >= 90:
            return "✅ CONFORME - OPTIMAL"
        elif score >= 70:
            return "✅ CONFORME - ACCEPTABLE"
        else:
            return "❌ NON CONFORME - CRITIQUE"
    
    def _get_quality_level(self, score: int) -> str:
        """Détermine le niveau de qualité."""
        if score >= 90:
            return "OPTIMAL"
        elif score >= 70:
            return "ACCEPTABLE"
        else:
            return "CRITIQUE"
    
    def _generate_recommendations(self, metrics: Dict[str, Any], issues: List[str]) -> List[str]:
        """Génère les recommandations basées sur l'analyse."""
        recommendations = []
        
        # Logique de génération de recommandations
        # À adapter selon le type d'agent
        
        return recommendations
    
    def _generate_standard_report(self, context: Dict, metrics: Dict, timestamp) -> Dict[str, Any]:
        """Génère un rapport selon le format standard de l'agent 06."""
        
        score = self._calculate_report_score(metrics)
        conformity = self._assess_conformity(score)
        quality_level = self._get_quality_level(score)
        
        agent_filename = Path(__file__).name
        
        # Issues critiques (à personnaliser selon l'agent)
        issues_critiques = []
        
        return {
            'agent_id': getattr(self, 'agent_id', 'unknown'),
            'agent_file_name': agent_filename,
            'type_rapport': 'standard',  # À personnaliser
            'timestamp': timestamp.isoformat(),
            'specialisation': 'Agent Spécialisé',  # À personnaliser
            'score_global': score,
            'niveau_qualite': quality_level,
            'conformite': conformity,
            'signature_cryptographique': 'N/A (Fonctionnalité non implémentée pour cet agent)',
            'issues_critiques_identifies': len(issues_critiques),
            'architecture': {
                'description': "Description de l'architecture de l'agent",
                'statut_operationnel': f"Système {getattr(self, 'agent_id', 'unknown')} opérationnel.",
                'confirmation_specialisation': f"{getattr(self, 'agent_id', 'unknown')} confirmé comme spécialiste.",
                'objectifs_principaux': [
                    "Objectif principal 1",
                    "Objectif principal 2",
                    "Objectif principal 3"
                ],
                'technologies_cles': ["Technologie 1", "Technologie 2"]
            },
            'recommandations': self._generate_recommendations(metrics, issues_critiques),
            'issues_critiques_details': issues_critiques if issues_critiques else [
                "Aucun issue critique majeur détecté. Le système fonctionne dans les paramètres attendus."
            ],
            'details_techniques': {
                'strategie': "Stratégie technique de l'agent",
                'composants_actifs': [],
                'metriques_collectees': metrics
            },
            'metriques_detaillees': {
                'score_global': {'actuel': score, 'cible': 100},
                'conformite_pourcentage': {'actuel': score, 'cible': 100, 'unite': '%'}
            },
            'impact_business': {
                'criticite': 'MOYENNE' if score >= 70 else 'HAUTE',
                'domaines_impactes': [],
                'actions_requises': []
            }
        }


    def _generate_markdown_report(self, rapport_json: Dict, context: Dict, timestamp) -> str:
        """Génère un rapport Markdown selon le format standard."""
        
        agent_name = rapport_json.get('agent_id', 'Agent Inconnu')
        type_rapport = rapport_json.get('type_rapport', 'standard')
        score = rapport_json.get('score_global', 0)
        quality = rapport_json.get('niveau_qualite', 'UNKNOWN')
        conformity = rapport_json.get('conformite', 'NON ÉVALUÉ')
        
        markdown_content = f"""# 📊 RAPPORT STRATÉGIQUE : {agent_name.upper()}

## 🎯 RÉSUMÉ EXÉCUTIF

**Agent :** {agent_name}  
**Type de Rapport :** {type_rapport}  
**Date de Génération :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Score Global :** {score}/100  
**Niveau de Qualité :** {quality}  
**Conformité :** {conformity}  

## 📈 ANALYSE GLOBALE

### Score de Performance
- **Score Actuel :** {score}/100
- **Objectif :** 100/100
- **Statut :** {'🟢 ACCEPTABLE' if score >= 70 else '🔴 CRITIQUE'}

### Architecture
{rapport_json.get('architecture', {}).get('description', 'Description non disponible')}

**Objectifs Principaux :**
"""
        
        # Ajouter les objectifs
        for obj in rapport_json.get('architecture', {}).get('objectifs_principaux', []):
            markdown_content += f"- {obj}\n"
        
        markdown_content += f"""
**Technologies Clés :**
"""
        
        # Ajouter les technologies
        for tech in rapport_json.get('architecture', {}).get('technologies_cles', []):
            markdown_content += f"- {tech}\n"
        
        markdown_content += f"""

## 🔍 RECOMMANDATIONS

"""
        
        # Ajouter les recommandations
        for reco in rapport_json.get('recommandations', []):
            markdown_content += f"- {reco}\n"
        
        markdown_content += f"""

## ⚠️ ISSUES CRITIQUES

"""
        
        # Ajouter les issues critiques
        for issue in rapport_json.get('issues_critiques_details', []):
            markdown_content += f"- {issue}\n"
        
        markdown_content += f"""

## 📊 MÉTRIQUES DÉTAILLÉES

### Performance Globale
- **Score Global :** {rapport_json.get('metriques_detaillees', {}).get('score_global', {}).get('actuel', 0)}/{rapport_json.get('metriques_detaillees', {}).get('score_global', {}).get('cible', 100)}
- **Conformité :** {rapport_json.get('metriques_detaillees', {}).get('conformite_pourcentage', {}).get('actuel', 0)}%

## 🎯 IMPACT BUSINESS

**Criticité :** {rapport_json.get('impact_business', {}).get('criticite', 'NON ÉVALUÉ')}

### Domaines Impactés
"""
        
        # Ajouter les domaines impactés
        for domaine in rapport_json.get('impact_business', {}).get('domaines_impactes', []):
            markdown_content += f"- {domaine}\n"
        
        markdown_content += f"""

### Actions Requises
"""
        
        # Ajouter les actions requises
        for action in rapport_json.get('impact_business', {}).get('actions_requises', []):
            markdown_content += f"- {action}\n"
        
        markdown_content += f"""

---
*Rapport généré automatiquement par {agent_name} - NextGeneration System*  
*Timestamp: {timestamp.isoformat()}*
"""
        
        return markdown_content

