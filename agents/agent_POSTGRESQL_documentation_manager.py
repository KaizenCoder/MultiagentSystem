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

from .agent_POSTGRESQL_base import AgentPostgreSQLBase
from core.agent_factory_architecture import Task, Result

class AgentPostgresqlDocumentationManager(AgentPostgreSQLBase):
    """Agent spécialisé pour la gestion de la documentation PostgreSQL"""
    
    def __init__(self, workspace_root: Path = None):
        super().__init__(
            agent_type="postgresql_documentation",
            name="Agent Documentation PostgreSQL"
        )
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

if __name__ == "__main__":
    agent = AgentPostgresqlDocumentationManager()
    # Test des capacités
    print("Capacités de l'agent:", agent.get_capabilities())

