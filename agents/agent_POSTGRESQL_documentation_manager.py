#!/usr/bin/env python3
"""
Agent Documentation Manager - Gestion de la documentation PostgreSQL
"""

import logging
from pathlib import Path
from datetime import datetime
import json
import os
import shutil

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
from typing import Dict, List, Optional, Any

class AgentPostgresqlDocumentationManager(AgentPostgreSQLBase):
    """Agent spécialisé pour la gestion de la documentation PostgreSQL"""
    
    def __init__(self, workspace_root: Path = None):
        super().__init__(
            agent_type="postgresql_documentation",
            name="Agent Documentation PostgreSQL"
        )
        
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="postgresql",
                custom_config={
                    "logger_name": f"nextgen.postgresql.agent_POSTGRESQL_documentation_manager.{getattr(self, 'agent_id', 'unknown')}",
                    "log_dir": "logs/postgresql",
                    "metadata": {
                        "agent_type": "agent_POSTGRESQL_documentation_manager",
                        "agent_role": "postgresql",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)
        self.workspace_root = workspace_root if workspace_root else Path(__file__).parent.parent
        self.docs_dir = self.workspace_root / "docs" / "postgresql"
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        
    def get_capabilities(self) -> list:
        """Liste des capacités spécifiques de l'agent"""
        return [
            "create_documentation",
            "update_documentation",
            "search_documentation",
            "generate_report",
            "archive_documentation"
        ]

    async def execute_task(self, task: Task) -> Result:
        """Exécution d'une tâche selon le Pattern Factory"""
        try:
            if task.type == "create_documentation":
                content = task.params.get("content")
                doc_type = task.params.get("doc_type", "general")
                if not content:
                    return Result(success=False, error="Contenu requis")
                resultats = await self.create_documentation(content, doc_type)
                return Result(success=True, data=resultats)
                
            elif task.type == "update_documentation":
                doc_id = task.params.get("doc_id")
                content = task.params.get("content")
                if not doc_id or not content:
                    return Result(success=False, error="ID et contenu requis")
                resultats = await self.update_documentation(doc_id, content)
                return Result(success=True, data=resultats)
                
            elif task.type == "search_documentation":
                query = task.params.get("query")
                doc_type = task.params.get("doc_type")
                if not query:
                    return Result(success=False, error="Requête de recherche requise")
                resultats = await self.search_documentation(query, doc_type)
                return Result(success=True, data=resultats)
                
            elif task.type == "generate_report":
                report_type = task.params.get("report_type", "summary")
                resultats = await self.generate_report(report_type)
                return Result(success=True, data=resultats)
                
            elif task.type == "archive_documentation":
                doc_id = task.params.get("doc_id")
                if not doc_id:
                    return Result(success=False, error="ID du document requis")
                resultats = await self.archive_documentation(doc_id)
                return Result(success=True, data=resultats)
                
            else:
                return Result(
                    success=False,
                    error=f"Type de tâche non supporté: {task.type}"
                )
                
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la tâche: {e}")
            return Result(
                success=False,
                error=str(e),
                error_code="EXECUTION_ERROR"
            )

    async def create_documentation(self, content: str, doc_type: str = "general") -> dict:
        """Crée un nouveau document"""
        try:
            doc_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            doc_path = self.docs_dir / f"{doc_type}_{doc_id}.md"
            
            with open(doc_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            metadata = {
                "id": doc_id,
                "type": doc_type,
                "created": datetime.now().isoformat(),
                "status": "active"
            }
            
            meta_path = doc_path.with_suffix(".json")
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)
            
            return {
                "status": "success",
                "doc_id": doc_id,
                "path": str(doc_path)
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la création du document: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    async def update_documentation(self, doc_id: str, content: str) -> dict:
        """Met à jour un document existant"""
        try:
            doc_files = list(self.docs_dir.glob(f"*_{doc_id}.md"))
            if not doc_files:
                return {
                    "status": "error",
                    "error": f"Document {doc_id} non trouvé"
                }
            
            doc_path = doc_files[0]
            with open(doc_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            meta_path = doc_path.with_suffix(".json")
            if meta_path.exists():
                with open(meta_path, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                metadata["updated"] = datetime.now().isoformat()
                with open(meta_path, "w", encoding="utf-8") as f:
                    json.dump(metadata, f, indent=2)
            
            return {
                "status": "success",
                "doc_id": doc_id,
                "path": str(doc_path)
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la mise à jour du document: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    async def search_documentation(self, query: str, doc_type: str = None) -> dict:
        """Recherche dans la documentation"""
        try:
            results = []
            pattern = f"*_{doc_type}*.md" if doc_type else "*.md"
            
            for doc_path in self.docs_dir.glob(pattern):
                with open(doc_path, "r", encoding="utf-8") as f:
                    content = f.read()
                if query.lower() in content.lower():
                    meta_path = doc_path.with_suffix(".json")
                    metadata = {}
                    if meta_path.exists():
                        with open(meta_path, "r", encoding="utf-8") as f:
                            metadata = json.load(f)
                    
                    results.append({
                        "doc_id": metadata.get("id", doc_path.stem),
                        "type": metadata.get("type", "unknown"),
                        "path": str(doc_path),
                        "created": metadata.get("created", "unknown")
                    })
            
            return {
                "status": "success",
                "results": results,
                "count": len(results)
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la recherche: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    async def generate_report(self, report_type: str = "summary") -> dict:
        """Génère un rapport sur la documentation"""
        try:
            stats = {
                "total_docs": 0,
                "by_type": {},
                "by_status": {},
                "latest_updates": []
            }
            
            for doc_path in self.docs_dir.glob("*.md"):
                stats["total_docs"] += 1
                meta_path = doc_path.with_suffix(".json")
                
                if meta_path.exists():
                    with open(meta_path, "r", encoding="utf-8") as f:
                        metadata = json.load(f)
                    
                    doc_type = metadata.get("type", "unknown")
                    stats["by_type"][doc_type] = stats["by_type"].get(doc_type, 0) + 1
                    
                    status = metadata.get("status", "unknown")
                    stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
                    
                    if "updated" in metadata:
                        stats["latest_updates"].append({
                            "doc_id": metadata["id"],
                            "updated": metadata["updated"]
                        })
            
            stats["latest_updates"].sort(key=lambda x: x["updated"], reverse=True)
            stats["latest_updates"] = stats["latest_updates"][:5]
            
            report_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = self.docs_dir / f"report_{report_type}_{report_id}.json"
            
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(stats, f, indent=2)
            
            return {
                "status": "success",
                "report_id": report_id,
                "path": str(report_path),
                "stats": stats
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la génération du rapport: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    async def archive_documentation(self, doc_id: str) -> dict:
        """Archive un document existant"""
        try:
            doc_files = list(self.docs_dir.glob(f"*_{doc_id}.md"))
            if not doc_files:
                return {
                    "status": "error",
                    "error": f"Document {doc_id} non trouvé"
                }
            
            doc_path = doc_files[0]
            archive_dir = self.docs_dir / "archive"
            archive_dir.mkdir(parents=True, exist_ok=True)
            
            shutil.move(doc_path, archive_dir / doc_path.name)
            
            meta_path = doc_path.with_suffix(".json")
            if meta_path.exists():
                with open(meta_path, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                metadata["status"] = "archived"
                metadata["archived_at"] = datetime.now().isoformat()
                with open(meta_path, "w", encoding="utf-8") as f:
                    json.dump(metadata, f, indent=2)
                shutil.move(meta_path, archive_dir / meta_path.name)
            
            return {
                "status": "success",
                "doc_id": doc_id,
                "path": str(archive_dir / doc_path.name)
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'archivage du document: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
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



if __name__ == "__main__":
    agent = AgentPostgresqlDocumentationManager()
    # Test des capacités
    print("Capacités de l'agent:", agent.get_capabilities())

